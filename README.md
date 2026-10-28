# AI Skills Library

A personal, open-source collection of reusable AI-agent skills and related tooling.

Skills in this repository are written once and distributed to the agent harnesses where they are useful. The initial targets are [OpenAI Codex](https://openai.com/codex/) and [Claude Code](https://docs.anthropic.com/en/docs/claude-code), with the [Skills CLI](https://skills.sh/) providing a portable installation path for those and other supported agents.

## Repository layout

```text
skills/
  <skill-name>/
    SKILL.md          # required skill definition
    scripts/          # optional executable helpers
    references/       # optional supporting material, loaded only when needed
AGENTS.md             # contributor and agent guidance
LICENSE               # Apache-2.0
```

Each directory directly beneath `skills/` is one independently installable skill. `SKILL.md` uses the open Agent Skills format: YAML frontmatter with a `name` and concise `description`, followed by the instructions an agent needs when it invokes the skill.

## Install a skill

After this repository is published to GitHub, install all or selected skills with the Skills CLI:

```bash
# Browse skills exposed by the repository
npx skills add triskeldeian/ai-skills-library --list

# Install interactively (the CLI detects supported local agents)
npx skills add triskeldeian/ai-skills-library

# Install all skills for Codex or Claude Code
npx skills add triskeldeian/ai-skills-library --agent codex --all
npx skills add triskeldeian/ai-skills-library --agent claude-code --all
```

Use `-g` for a user-level installation. Run `npx skills --help` for the current agent list and options.

## Adding a skill

1. Create `skills/<kebab-case-name>/SKILL.md`.
2. Give it a unique `name` and an explicit, action-oriented `description`.
3. Keep the main instructions focused; put detailed reference material under `references/` and automation under `scripts/`.
4. Test it with the intended agent(s), then run `npx skills add . --list` to confirm the CLI discovers it.

Read [AGENTS.md](AGENTS.md) before contributing. It defines the conventions that keep skills portable across harnesses.

## License

Licensed under the [Apache License 2.0](LICENSE).
