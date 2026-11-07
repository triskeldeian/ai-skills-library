"""Read-only checker for the record-decision skill's default ADR format.

Verifies, across docs/design/active/, docs/design/archive/, and
docs/design/index.md. Use --design-root PATH for another decision directory;
relative paths are resolved from the current working directory.

1. ADR numbers are unique across active/ and archive/ combined. Optionally
   require a contiguous 1..max range with --require-contiguous.
2. Every `supersedes` reference points at an ADR that exists, lives under
   archive/, and has status `superseded`.
3. Every active/ ADR has status `accepted`; every archive/ ADR has status
   `superseded` or `deprecated`.
4. Every active/ ADR has exactly one heading row in index.md, and every
   index.md heading row refers to a number that exists under active/.

Requires Python 3.10+ and PyYAML. No environment variables required.
Prints findings and exits 1 for inconsistencies, confirmation and exits 0
on success, or a diagnostic and exits 2 for unavailable prerequisites,
invalid arguments, or unreadable inputs. Does not modify files.
"""

import argparse
import re
import sys

if sys.version_info < (3, 10):
    print("Python 3.10+ is required; use the skill's manual validation checklist.", file=sys.stderr)
    sys.exit(2)

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

try:
    import yaml
except ModuleNotFoundError:
    print("PyYAML is unavailable; use the skill's manual validation checklist.", file=sys.stderr)
    sys.exit(2)

ADR_FILENAME_RE = re.compile(r"^(\d{4})-.+\.md$")
VALID_ARCHIVE_STATUSES = ("superseded", "deprecated")

Folder = Literal["active", "archive"]


# pyyaml's default int resolver treats a bare scalar like "0011" as octal
# (yaml.safe_load("x: 0011") -> 9), and a scalar like "0009" doesn't match
# that resolver at all and comes back as str - two different behaviours for
# what should be the same kind of value. Dropping the int resolver makes
# every bare numeric-looking scalar load as str, decoded with int() instead.
class _NoImplicitIntLoader(yaml.SafeLoader):
    pass


_NoImplicitIntLoader.yaml_implicit_resolvers = {
    first_char: [resolver for resolver in resolvers if resolver[0] != "tag:yaml.org,2002:int"]
    for first_char, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


@dataclass
class AdrRecord:
    number: int
    path: Path
    folder: Folder
    status: str | None
    supersedes: list[int] | None


def parse_frontmatter(text: str) -> tuple[dict[str, object] | None, str | None]:
    """Returns (frontmatter_dict, None) on success, or (None, error_message)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "does not start with a '---' frontmatter block"

    closing_index: int | None = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            closing_index = i
            break
    if closing_index is None:
        return None, "frontmatter block has no closing '---'"

    block = "\n".join(lines[1:closing_index])
    try:
        data = yaml.load(block, Loader=_NoImplicitIntLoader)
    except yaml.YAMLError as error:
        return None, f"frontmatter is not valid YAML: {error}"

    if not isinstance(data, dict):
        return None, "frontmatter does not contain a YAML mapping"
    return data, None


def _display_status(status: str | None) -> str:
    return status if status is not None else "<missing>"


def load_adr_records(folder_path: Path, folder: Folder, violations: list[str]) -> list[AdrRecord]:
    records: list[AdrRecord] = []
    if not folder_path.is_dir():
        violations.append(f"{folder_path} does not exist or is not a directory")
        return records

    for path in sorted(folder_path.glob("*.md")):
        match = ADR_FILENAME_RE.match(path.name)
        if not match:
            violations.append(f"{path}: filename must match NNNN-short-slug.md")
            continue
        number = int(match.group(1))

        text = path.read_text(encoding="utf-8")
        frontmatter, error = parse_frontmatter(text)
        if error is not None:
            violations.append(f"{path}: {error}")
            records.append(AdrRecord(number=number, path=path, folder=folder, status=None, supersedes=None))
            continue

        status_raw = frontmatter.get("status")
        status = status_raw if isinstance(status_raw, str) else None

        supersedes: list[int] | None = None
        if "supersedes" in frontmatter:
            supersedes_raw = frontmatter["supersedes"]
            if not isinstance(supersedes_raw, list):
                violations.append(f"{path}: 'supersedes' is not a list ({supersedes_raw!r})")
            else:
                supersedes = []
                for item in supersedes_raw:
                    try:
                        supersedes.append(int(str(item)))
                    except ValueError:
                        violations.append(f"{path}: 'supersedes' entry {item!r} is not a number")

        records.append(
            AdrRecord(number=number, path=path, folder=folder, status=status, supersedes=supersedes)
        )

    return records


def check_numbering(
    records: list[AdrRecord], violations: list[str], require_contiguous: bool = False
) -> None:
    numbers_seen: dict[int, list[Path]] = {}
    for record in records:
        numbers_seen.setdefault(record.number, []).append(record.path)

    for number, paths in sorted(numbers_seen.items()):
        if len(paths) > 1:
            joined = ", ".join(str(p) for p in paths)
            violations.append(f"ADR number {number:04d} is used by more than one file: {joined}")

    if not numbers_seen:
        violations.append("no ADR files found under active/ or archive/")
        return

    if 0 in numbers_seen:
        violations.append("ADR number 0000 is invalid; numbering starts at 0001")
    if not require_contiguous:
        return

    highest = max(numbers_seen)
    missing = [n for n in range(1, highest + 1) if n not in numbers_seen]
    if missing:
        missing_str = ", ".join(f"{n:04d}" for n in missing)
        violations.append(
            f"ADR numbering has gap(s) - missing number(s) {missing_str} "
            f"(numbers in use range from 0001 to {highest:04d})"
        )


def check_supersedes(records: list[AdrRecord], violations: list[str]) -> None:
    by_number: dict[int, list[AdrRecord]] = {}
    for record in records:
        by_number.setdefault(record.number, []).append(record)

    for record in records:
        if not record.supersedes:
            continue
        for target_number in record.supersedes:
            targets = by_number.get(target_number, [])
            if not targets:
                violations.append(
                    f"{record.path} (ADR-{record.number:04d}) declares supersedes: [{target_number:04d}], "
                    f"but no ADR file with number {target_number:04d} exists"
                )
                continue
            for target in targets:
                if target.folder != "archive":
                    violations.append(
                        f"{record.path} (ADR-{record.number:04d}) claims to supersede ADR-{target_number:04d}, "
                        f"but {target.path} is under '{target.folder}/', not 'archive/'"
                    )
                if target.status != "superseded":
                    violations.append(
                        f"{record.path} (ADR-{record.number:04d}) claims to supersede ADR-{target_number:04d}, "
                        f"but {target.path} has status '{_display_status(target.status)}' "
                        f"(expected 'superseded')"
                    )


def check_status_consistency(records: list[AdrRecord], violations: list[str]) -> None:
    for record in records:
        if record.folder == "active":
            if record.status != "accepted":
                violations.append(
                    f"{record.path} is under active/ but has status '{_display_status(record.status)}' "
                    f"(expected 'accepted')"
                )
        else:
            if record.status not in VALID_ARCHIVE_STATUSES:
                violations.append(
                    f"{record.path} is under archive/ but has status '{_display_status(record.status)}' "
                    f"(expected 'superseded' or 'deprecated')"
                )


HEADING_RE = re.compile(r"^### \[ADR-(\d{4}):[^\]]*\]\(([^)]+)\)\s*$")
HEADING_LINE_PREFIX = "### [ADR-"
HREF_RE = re.compile(r"^(active|archive)/(\d{4})-.+\.md$")


def check_index(
    active_records: list[AdrRecord], design_root: Path, violations: list[str]
) -> None:
    index_path = design_root / "index.md"
    active_dir = design_root / "active"
    if not index_path.is_file():
        violations.append(f"{index_path} does not exist")
        return

    active_numbers = {record.number for record in active_records}
    numbers_in_index: list[int] = []

    for line in index_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith(HEADING_LINE_PREFIX):
            continue
        match = HEADING_RE.match(line)
        if not match:
            violations.append(f"{index_path}: heading line could not be parsed: '{line}'")
            continue

        heading_number = int(match.group(1))
        href = match.group(2)
        numbers_in_index.append(heading_number)

        href_match = HREF_RE.match(href)
        if not href_match:
            violations.append(
                f"{index_path}: entry for ADR-{heading_number:04d} has an unparseable link path '{href}'"
            )
            continue

        href_folder, href_number_str = href_match.group(1), href_match.group(2)
        href_number = int(href_number_str)
        if href_number != heading_number:
            violations.append(
                f"{index_path}: entry titled 'ADR-{heading_number:04d}' links to a different "
                f"number in its path ('{href}')"
            )
        if href_folder == "archive":
            violations.append(
                f"{index_path}: entry for ADR-{heading_number:04d} links into archive/ ('{href}'), "
                f"but index.md must only list active ADRs"
            )
        if not (design_root / href).is_file():
            violations.append(f"{index_path}: link target does not exist: '{href}'")

    counts: dict[int, int] = {}
    for number in numbers_in_index:
        counts[number] = counts.get(number, 0) + 1

    for number, count in sorted(counts.items()):
        if number not in active_numbers:
            violations.append(
                f"{index_path}: lists ADR-{number:04d}, but no such ADR exists under {active_dir}/"
            )
        elif count > 1:
            violations.append(
                f"{index_path}: has {count} entries for ADR-{number:04d}, expected exactly one"
            )

    for number in sorted(active_numbers):
        if number not in counts:
            violations.append(
                f"ADR-{number:04d} is under {active_dir}/ but has no entry in {index_path}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design-root", type=Path, default=Path("docs/design"))
    parser.add_argument("--require-contiguous", action="store_true")
    args = parser.parse_args()
    violations: list[str] = []

    try:
        active_records = load_adr_records(args.design_root / "active", "active", violations)
        archive_records = load_adr_records(args.design_root / "archive", "archive", violations)
        check_index(active_records, args.design_root, violations)
    except (OSError, UnicodeError) as error:
        print(f"Unable to read ADR inputs: {error}", file=sys.stderr)
        return 2
    all_records = active_records + archive_records

    check_numbering(all_records, violations, args.require_contiguous)
    check_supersedes(all_records, violations)
    check_status_consistency(all_records, violations)

    if violations:
        for violation in violations:
            print(violation)
        return 1

    print(f"{args.design_root} ADRs are internally consistent: numbering, supersedes, status, and index all check out.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
