---
name: implement-feature
description: Implement non-trivial production-code features or behavior changes through test writing, implementation, review, and test cleanup, using separate subagents when available. Use when a requested code change needs coordinated implementation and verification; skip trivial edits, documentation, plans, and research.
---

# Implement Feature

Act as an **orchestrator**: define the task, delegate each role below in sequence to its own subagent when available and permitted, mediate handoffs, and report to the user. Leave implementation to the implementer role.

A subagent means a separate context scoped to one role, using the harness's supported delegation mechanism. If delegation is unavailable or prohibited, run the roles yourself as separate sequential passes. Record each handoff and re-read the requirements and diff at each transition; this fallback does not provide independent review. No particular language, package manager, or companion skill is required.

## Prepare the handoffs

1. Read applicable project instructions and inspect the affected code, tests, manifests, and validation configuration. Derive test, lint, type-check, and build commands from the project rather than assuming tools or source paths.
2. Define the requested behavior, acceptance criteria, likely error cases, and scope. Resolve material ambiguities before dependent implementation; proceed with routine choices supported by project conventions.
3. Record the starting worktree state and known validation failures. Track task-owned changes separately from pre-existing edits; a current diff alone is not proof of ownership. Preserve unrelated work.
4. Give each role the requirements, applicable instructions, affected paths, task-owned changes, validation commands, and prior role's findings. Run roles sequentially so their edits do not race. Require each handoff to report changes, checks and outcomes, and unresolved issues.

## Select models per role

Each role below names a capability tier and a reasoning level. When the harness lets you choose a model or reasoning effort for each subagent, request them, translating the tier with this mapping. Use the latest version available in each of the model families.

| Tier | Claude Code | Codex |
| --- | --- | --- |
| standard | `sonnet` | Terra |
| strong | `opus` | Sol |

Rules:

- Request only models and reasoning levels the harness actually offers, using the exact identifier it lists. Never invent an identifier.
- If the mapped model is unavailable and per-subagent selection is supported, propose to the user a model of comparable strength for each of the two tiers.
- Treat the table as a preference, not a gate. If per-subagent selection is unsupported, you are running the sequential-pass fallback, or the user declines or does not answer the proposal above, inherit the current settings and continue. Do not switch the session's own model.
- Stay within any model limits the user or project has set.
- Record the model and reasoning effort each role actually ran with, or that it was inherited.

## Run the four roles

### 1. Test-writer

Model: standard tier, medium reasoning.

Inspect existing coverage before writing tests. Consult `check-test-coverage` if available; otherwise follow project guidance and inspect the relevant tests directly. Do not install a missing skill. Extend existing parameterized or table-driven cases when natural, and add tests only for uncovered behavior.

Run the relevant tests before implementation and confirm that new or extended cases fail for the missing behavior, not because of setup, syntax, or unrelated baseline failures. If existing tests already demonstrate the gap, reuse them. If the behavior is already implemented and covered, report that evidence before making unnecessary changes. If execution is blocked, record the cause and unverified expectations; do not claim a demonstrated failing test.

### 2. Implementer

Model: standard tier, medium reasoning.

Make the smallest coherent production change that satisfies the requirements and tests. Follow the project's design and dependency conventions below. Change tests only to correct a demonstrated error, explain the correction, and rerun affected cases; do not weaken assertions to make the implementation pass. Run relevant validation and report remaining failures.

### 3. Reviewer

Model: strong tier, high reasoning.

Review the requirements and task-owned diff for correctness beyond the tests, edge cases, error paths, resource handling, and maintainability. Check naming, cohesion, dead code, dependency declarations, and comments added by earlier roles. Look for duplicated tests that should extend existing cases.

Send concrete findings to the implementer, including test gaps for the test-writer where needed. Recheck fixes and their validation before proceeding. Report unresolved findings explicitly; do not describe the task as complete while material issues remain.

### 4. Test cleanup

Model: standard tier, medium reasoning.

After review fixes, edit **task-owned tests and test-only helpers, fixtures, and imports only**. Do not edit production code or unrelated tests. Judge each added or changed test by:

- What concrete regression would make it fail? Remove tests that merely mirror internal literals or restate the implementation without guarding a requirement. Keep simple tests of contractual values or plausible future mistakes.
- Does another test catch the same regression? Merge near-duplicates, extending existing parameterized cases where natural.
- Does it test application behavior or integration, rather than just a language, library, or mocking tool?
- Does it pin internal structure instead of behavior? Keep structural checks only when the structure is itself a required public contract.
- Are its assertions strong enough to catch the intended bug? Strengthen weak checks such as a bare failure exit code or an overly broad substring assertion when they can accept the wrong failure.

Remove test-only helpers, fixtures, and imports made unused by cleanup. Report what was removed, merged, or strengthened and why. If cleanup exposes a production defect, return it to implementation and review rather than fixing production code in this role.

Rerun affected tests and the project's required validation after cleanup. Report exact commands and outcomes, distinguishing new failures, baseline failures, and checks that could not run.

## Finish

Spot-check the cleanup report and final diff against the acceptance criteria. Report the delivered behavior, validation evidence, unresolved findings, the model and reasoning effort each role ran with, and any sequential-pass fallback used. Do not claim checks passed when execution was unavailable. This workflow does not itself authorize commits, publication, deployment, or destructive actions; follow the user's authorization and project rules for those steps.

## Dependency declarations

Declare a newly required runtime dependency in the consuming package's runtime manifest in the same change that first uses it. Use the ecosystem's appropriate runtime, optional, peer, or platform-specific mechanism; do not rely on a development-only dependency for a normal installation. Update lockfiles according to project conventions and verify the relevant build or installation path when feasible. For example, a required Python runtime import belongs in `[project].dependencies`, not solely in a development dependency group.

## Code comments

Explain hidden constraints, subtle invariants, and workarounds rather than restating visible code. Keep the explanation understandable without a transient plan or task number. Follow project conventions for durable references such as ADRs or issue links documenting an active workaround; a reference should supplement the explanation. Enforce this during review for comments and docstrings added by every role.

## Scope

Use this workflow for non-trivial production-code changes. Handle trivial edits, documentation, plans, ADRs, and exploratory research through the applicable project workflow without invoking these four roles.
