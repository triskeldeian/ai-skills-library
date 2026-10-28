# Contributor and Agent Guide

This repository is the source of truth for reusable AI-agent skills. It is designed for OpenAI Codex, Claude Code, and other harnesses supported by the [Skills CLI](https://skills.sh/).

## Principles

- Keep a single canonical implementation of each skill in `skills/`.
- Write harness-neutral instructions unless a capability genuinely belongs to only one harness.
- Prefer explicit, safe workflows over assumptions about shell, OS, account, or installed tools.
- Keep each skill small, focused, and independently useful.
- Treat scripts and references as part of the skill's public API: document inputs, outputs, prerequisites, and failure modes.

## Skill structure

Create skills using this layout:

```text
skills/
  my-skill/
    SKILL.md
    scripts/              # optional helpers; use portable runtimes where practical
    references/           # optional detail loaded on demand
    assets/               # optional static files used by the skill
```

The directory name must be kebab-case. `SKILL.md` must be uppercase and contain valid YAML frontmatter:

```markdown
---
name: my-skill
description: Helps an agent do a specific task. Use when the user asks to do that task.
---

# My Skill
```

`name` must be unique, lowercase, and match the directory name unless there is a compelling compatibility reason not to. The description is the discovery mechanism: state what the skill does and when an agent should use it.

## Authoring guidance

Always use the `writing-skills` skill to review every new or modified skill, including changes to its scripts, references, or assets and changes to `writing-skills` itself. Check the result against its authoring and validation guidelines. If the skill is not installed in the current harness, read and apply the canonical [skills/writing-skills/SKILL.md](skills/writing-skills/SKILL.md) directly.

- Put essential workflow instructions in `SKILL.md`; avoid long background material there.
- Link to files in `references/` only when they are needed for a particular branch of the workflow.
- Use relative paths within the skill directory and state required runtimes or environment variables.
- Do not commit credentials, access tokens, private URLs, or machine-specific paths.
- Make destructive or external side effects opt-in and require clear user confirmation where appropriate.
- When a workflow differs by harness, use a clearly labelled section rather than duplicating the entire skill.

## Compatibility and distribution

Edit the canonical source in `skills/`, rather than installed copies under `.agents/skills/` or `.claude/skills/`. Keep generated installation copies out of commits. The Skills CLI installs the canonical `skills/*/SKILL.md` into the selected agent's expected location, including Codex (`--agent codex`) and Claude Code (`--agent claude-code`).

Useful checks while developing:

```bash
# Verify the repository's skills can be discovered
npx skills add . --list

# Test a local skill in a chosen harness
npx skills add . --agent codex --skill my-skill
npx skills add . --agent claude-code --skill my-skill
```

Use the current `npx skills --help` output as the authority for CLI flags and the supported-agent matrix; the tooling evolves independently of this repo.

## Change checklist

Before submitting a skill or tooling change:

1. For every new or modified skill, complete the `writing-skills` review described above. Address findings and report any unresolved issues or checks that could not be run.
2. Verify frontmatter and paths are correct.
3. Exercise the normal path and at least one likely failure path.
4. Confirm the skill can be discovered with the Skills CLI.
5. Update the README if installation, prerequisites, or the repository layout changes.
6. Keep the change scoped; avoid unrelated formatting or generated files.
