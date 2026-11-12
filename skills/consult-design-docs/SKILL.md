---
name: consult-design-docs
description: Use when consulting recorded architecture or design decisions to guide implementation, evaluate a proposed change, or explain an existing design.
---

# Consulting recorded design decisions

Before writing code, proposing a design, or explaining why something works the way it does, check whether the ground is already covered by recorded decisions.

## Layout

Read applicable project and agent guidance, then locate the project's decision index and ADR directories. Follow its established paths, metadata, and index format. The layout and summary format below are the defaults used by `record-decision`; adapt the steps to the project's conventions without reorganizing its records. This workflow assumes a well-formed decision system.

```
docs/design/
  index.md     one entry per active ADR — read this first, always
  active/      current, authoritative ADRs — open only the ones index.md points to
  archive/     superseded and deprecated ADRs — history only, never guidance
```

In this default, `index.md` carries a 2-4 sentence, tagged summary of every active decision. Read the project's index in full and use it as the only source for judging relevance — never grep the ADR files directly, and never rely on a filename or a memory of a previous conversation, since current decisions can have superseded what was true then.

## Steps

1. **Read the decision index in full** (`docs/design/index.md` in the default layout).
2. **Decide relevance from the summaries alone.** Each entry's summary and any tags determine whether it bears on the task at hand — most entries won't.
3. **Open only the specific current ADRs that step 2 marked relevant.** Read the full decision and rationale (Context, Decision, Options considered, Consequences in the default format); the index entry alone is not enough to implement against or reason about the decision.
4. **Never open or cite archived ADRs unless the user explicitly requests them, and never implement against them as current guidance.** An archived ADR is history only — it records what was decided and why *at the time* and may assert things that are no longer true. This holds even if a filename or search result surfaces one; archived records do not apply to present-day behavior.
5. **If the task touches ground no active ADR covers, and the decision looks like it will bind future work, say so** rather than deciding it silently. Follow the recording handoff below when recording or changing a decision is needed.

## Scope

This skill is read-side only. For writing, superseding, or deprecating an ADR, prefer `record-decision` if available. Otherwise, follow applicable project and agent guidance for recording the settled decision and updating its index. If no recording workflow is available, report the need and ask how to proceed before establishing a new system. Do not install a companion skill just to complete this handoff.

In the default layout, `docs/design/overview.md`, if present, is a non-authoritative human-onboarding document and is never loaded by this skill or treated as a substitute for the index.
