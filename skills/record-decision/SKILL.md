---
name: record-decision
description: Create, supersede, or deprecate architecture decision records (ADRs). Use when the user asks to record a design decision, write an ADR, revisit a recorded decision, or capture a settled decision that will guide future work.
---

# Recording a decision

Record one independent decision per ADR, with enough context to explain what was decided and why. Preserve accepted decisions as history: replace a substantive change with a successor rather than rewriting the original reasoning.

## 1. Establish the project's conventions

Read applicable project and agent guidance, then locate its decision index, existing ADRs, and templates. Follow its paths, metadata, numbering, lifecycle, and indexing conventions. The layout and formats below are defaults for a project without an established convention; do not migrate existing records to fit them.

If there is no convention, use this default layout for an explicitly requested ADR. If you noticed a decision during other work, confirm that the user wants it recorded before establishing a new decision-record system. Ask only about missing information that changes the decision, its ownership, or how it should be retired.

```text
docs/design/
  index.md       one entry per active ADR, with a short statement of the decision
  overview.md    optional human-facing introduction; not an authoritative index
  active/        decisions currently in force
  archive/       superseded and deprecated decisions; historical reference only
```

In this default, the index mirrors `active/` exactly. An archived record never has an index entry. Read the index first and open the specific records relevant to the question; consult archived records when tracing history, not as current guidance. When initializing this layout, create the index and both directories, even if one is empty. Do not create an overview solely for this workflow.

Number new records from the highest existing number across active and archived records, starting at `0001` for an empty set. Never reuse a number. Use the project's existing documentation and issue locations for supporting material; paths below refer to the chosen decision directory.

## 2. Classify the change

- **New decision:** no existing ADR settles this question. Create a record.
- **Replacement:** an active ADR answers this question, but its decision or substantive rationale changes. Create a successor and retire the predecessor in the same change.
- **Deprecation:** the subject no longer exists or the rule no longer applies, and no successor replaces it. Retire the record with a reason.
- **Already covered:** the existing decision still stands. Reference it; do not create a duplicate.

Split independently changeable decisions into separate records. Ask the user if the scope or replacement relationship remains ambiguous after reading the relevant records. A proposal or unresolved discussion is not an accepted decision; use the project's proposal workflow or clarify what has actually been settled.

Immutability protects a decision's meaning. Minimal corrections to renamed identifiers or relocated links are allowed when they preserve that meaning. Changes to the rule, rationale, options, or consequences require a successor. Retirement metadata is the other explicit exception described below.

## 3. Write the ADR

For the default format, create `active/NNNN-short-slug.md` with YAML frontmatter and a matching heading:

```markdown
---
title: Shared Configuration Format
status: accepted
date: YYYY-MM-DD
authored-by: <decision owner>
tags: [configuration, interoperability]
---

# ADR-NNNN: Shared Configuration Format

## Context

## Decision

## Options considered

## Consequences
```

Replace placeholders before saving. Use the date the decision was made, not the last-edit date. Identify the owner from project guidance or the user; do not invent a person or treat authorship as approval. Optional `consulted` names people who shaped the decision. Reuse existing lowercase tags where possible.

- **Context:** the constraints or problem requiring the decision.
- **Decision:** a concrete rule future work can follow, with explicit scope.
- **Options considered:** a table of actual alternatives and a short verdict for each. Do not invent discussions or evidence.
- **Consequences:** commitments, costs, and limitations accepted with the decision.

Keep detailed investigations and raw benchmark or probe output in the project's durable supporting documentation and link to it when useful. Preserve enough rationale in the ADR to understand the decision independently. A deliberate deferral that defines the decision's scope belongs in the Decision section. Track independently actionable unresolved questions in the project's issue system, checking for an existing record first.

For repository-local issues, use `manage-open-issues` if available and compatible with project guidance. Pass the gap, its impact, the originating ADR, and any known next step; let that skill maintain the record and index. Otherwise, follow the project's issue workflow. If none exists, keep the unresolved question visible in the response and ask where to track it before establishing a new system. When the decision resolves an existing issue, use the same handoff or project workflow to update or close it, retaining any unresolved portion. Report issue changes in the final response.

Prefer durable links to other ADRs and supporting documentation. Avoid dependencies on transient plans or issues that may be compacted, renumbered, or deleted: incorporate essential context as prose. Follow project policy for stable external issue references.

## 4. Update the index and optional overview

Update the index in the same change as the record. For the default format, add exactly one entry per active ADR:

```markdown
### [ADR-NNNN: Title](active/NNNN-short-slug.md)
**Tags:** tag1, tag2

<2–4 sentences stating the decision as an instruction.>
```

Match the title and tags to the ADR. State the rule directly, using the actual names of relevant mechanisms or conventions. Keep rejected alternatives, ordinary trade-offs, and supersession history in the full record. Include a critical correctness or safety boundary when a reader acting on the summary alone could otherwise cross it.

If an overview exists, update the affected prose in the same change so it describes the current decisions. Edit only the relevant section; do not regenerate it or impose an entry-per-ADR structure. Use the index and ADRs to determine current guidance.

## 5. Retire a record when needed

Follow the project's lifecycle if it differs. With the default layout:

**Supersession**

1. Add `supersedes: ['0002']` to the successor's frontmatter, listing the numbers it replaces as quoted strings.
2. Move the predecessor from `active/` to `archive/`, retaining its filename and number. Use `git mv` for tracked files when Git is available, or the environment's file-move operation otherwise.
3. Change only its `status` to `superseded`; preserve its date and body. The successor holds the relationship; do not add `superseded-by` to the predecessor.
4. Replace the predecessor's index entry with the successor's entry and update the optional overview.

**Deprecation**

Move the record to `archive/`, change its `status` to `deprecated`, and add a one-line `deprecated-because` frontmatter field. Preserve the original date and body. Remove its index entry and revise the optional overview; there is no successor.

**References after either move**

Search the repository's documentation and agent instructions for the old path and ADR number, using `rg` or the available search tool. Point current guidance to the successor only when it still supports the referencing statement. If the statement itself needs a substantive change in another accepted ADR, flag it for a separate supersession rather than silently rewriting it. For deliberately historical references, link to the archive. Recheck relative links inside the moved file because its location changed; repair paths without changing their meaning.

## 6. Validate

Use the project's existing validator when available. Otherwise, for the default layout, optionally run [the Python checker](scripts/check_decisions.py) if **Python 3.10+ and PyYAML are already available**. There is no mandatory runtime, environment variable, or package installation for this skill. Do not install Python, PyYAML, or a runtime manager just to validate ADRs; use the manual checks below when prerequisites are missing or the project's format differs.

From the target project's root, substitute the checker's actual path in the installed skill; do not assume a harness-specific installation directory:

```text
python "<skill-directory>/scripts/check_decisions.py" --design-root "docs/design"
```

Use the environment's existing Python command if it has another name. `--design-root` accepts an absolute path or a path relative to the working directory and defaults to `docs/design`. The checker supports the default `active/`, `archive/`, four-digit filenames, YAML frontmatter, and index headings above. It reports Markdown files in those folders whose names do not match `NNNN-short-slug.md`, and checks number uniqueness, supersession targets, status/location consistency, and index membership and link targets. Add `--require-contiguous` only if the project requires an unbroken sequence starting at `0001`; gaps alone do not imply a broken decision history.

The checker is read-only. It prints confirmation and exits `0` on success, findings and exits `1` for inconsistencies, or a diagnostic and exits `2` for missing prerequisites, invalid arguments, or unreadable inputs. It does not replace the following content review.

**Always review these; if automation is unavailable, check every item manually:**

- Numbers are unique across active and archived records; new numbers continue above the previous maximum. Check contiguity only if required by the project.
- In the default layout, active records have `status: accepted`; archived records have `superseded` or `deprecated`. Each `supersedes` number exists in the archive with `status: superseded`. Deprecations include a reason.
- Each active ADR has exactly one index entry pointing to its actual file, and archived ADRs have none. Titles and tags match. Entries state current instructions without rejected options or ordinary trade-offs.
- Each record captures one settled decision with its context, alternatives, and consequences. Dates and authorship are grounded in the available information.
- Current guidance does not rely on archived decisions. Links to moved records and links inside those records resolve correctly.
- An existing overview reflects the decisions affected by this change.

Fix findings introduced by the current change and recheck. Report unrelated pre-existing drift without rewriting other decisions or renumbering history. If validation cannot be completed, say which checks remain unverified.

## 7. Report back

Summarize the records created or retired, the decision each captures, index and overview changes, and references repaired. State whether validation was automated or manual, its result, any unrelated drift, and consequential judgment calls the user should review.
