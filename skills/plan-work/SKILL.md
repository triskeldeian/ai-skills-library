---
name: plan-work
description: Use when creating a project work plan from a request or discussion, reading a plan to identify scope or next work, or maintaining its iterations, dependencies, status and outcomes as work proceeds.
---

# Planning work

Keep plans as current intent and progress, edited in place. Version history carries the story of how they changed.

## 1. Locate and read the plan

New plans use this layout, including small plans:

```text
docs/plans/
  NNNN-short-slug/
    PLAN.md
    iterations/
      01-short-slug.md
      02-short-slug.md
  completed/
    NNNN-short-slug.md
```

Use the title `# Plan NNNN: <Title>`. Assign the next four-digit number above all existing active folders, legacy plan files and completed files; never reuse a plan number. Create directories as needed. Use another location or naming only at the user's request.

Maintain existing single-file plans in place, with iterations as inline sections. Do not convert them as part of an ordinary update. Only when conversion is requested, read [references/convert-single-file-plan.md](references/convert-single-file-plan.md).

For a folder plan, start with `PLAN.md` and its essential **Read first** documents. Use its iteration index and graph for progress and dependencies; load only the iteration being worked on and the references needed for that task. Open other iterations when their details affect the work, not merely because they are linked. A parent-plan link requires its shared scope and constraints, not all its iterations. For legacy files, read the shared sections and relevant iteration sections.

For a whole-plan review or completion check, read all iterations, including dropped ones. If an indexed file is missing or an iteration file is absent from the index, resolve the discrepancy before relying on the plan's completeness.

## 2. Create the plan

Copy [assets/plan-template.md](assets/plan-template.md) to `PLAN.md` and [assets/iteration-template.md](assets/iteration-template.md) once per iteration under `iterations/`. Fill in the templates, removing comments, unused examples and empty optional sections. Resolve links relative to the file containing them.

Before writing or changing an approach that may touch settled decisions, consult relevant project decisions using the handoff below.

- **Goal, non-goals and exit criteria:** draft from the request and discussion. Get the user's confirmation before starting an iteration. Once confirmed, propose changes and wait for agreement; never rewrite them to match what happened to get built.
- **Read first:** only documents essential to understanding or safely changing the whole plan, normally three or fewer. Link iteration-specific context inside that iteration.
- **Status:** `draft`, `in progress`, `blocked` or `done`, optionally followed by one sentence about next work or a blocker. Keep it out of changelog territory.
- **Last modified:** update `PLAN.md` whenever any part of the plan changes, including iteration-only edits. For legacy plans, update the date in the file.
- **Dependencies:** prerequisites for starting or finishing, with ownership and the effect of delay. Background reading belongs in Read first or inline.

### Iterations and graph

Each iteration must be implementable and verifiable in one pass. Use the iteration template's intent, optional approach, checkable done conditions and outcome. Keep options, constraints and relevant code or decision links in Approach; leave Outcome empty until completion, except for blocking or dropping reasons.

Give each iteration a permanent integer label and a filename such as `01-short-slug.md`. Additions take the next unused number; never renumber or rename existing files to reflect execution order. In `PLAN.md`, list each iteration's linked title, a short one-sentence description of its purpose, and status without duplicating its approach or outcome. The iteration document owns its detail; the index and graph summarize it.

The **Iteration graph** defines dependencies, not numerical or preferred order. Include every iteration, even independent and dropped ones, with no cycles. An edge means the successor cannot start or be verified until its predecessor is done. Use the project's diagram convention, otherwise the template's Mermaid example when supported or a textual dependency list with statuses.

Propose any extra section to the user with its purpose, such as background, settled minor choices, a special verification approach or risks. Put it at plan or iteration level according to its scope, and keep it only while useful.

## 3. Maintain the plan

Update documentation with the work when possible. Never commit plan edits or other work without the user's approval. In the same edit, synchronize the affected iteration, index entry and graph, and update the plan's status and last-modified date. Legacy plans use their inline sections instead of an index.

| Event | Required update |
| --- | --- |
| Start | Set iteration to `in progress`. |
| Finish | Set to `done`; write two or three lines of Outcome: what exists and any deviation a later reader needs. Omit file walkthroughs, test counts and attempt histories. |
| Add | Create the next-numbered iteration document and append its index entry; add its graph node and dependencies. For a legacy plan, append an inline iteration. |
| Block | Set to `blocked`, explain in Outcome, and block the plan if nothing else can proceed. Clear the reason and restore appropriate statuses when resolved. |
| Drop | Set to `dropped` with a one-line reason in Outcome. Retain the document, index entry and graph node; reassess dependent work rather than silently treating the dropped prerequisite as complete. |
| Change approach | Rewrite affected content as current intent. Explain the reason to the user and, if a commit is approved, in its message. |

Keep unsettled questions with what they block: shared questions in `PLAN.md`, iteration-specific ones in that document. Once answered, fold the answer into the affected content and remove the question. Record decisions that bind future work outside the plan and link them from the iteration that settled them.

Track out-of-scope follow-ups using the issue handoff below, checking for existing coverage first. When work resolves an issue, update it with verification evidence and retain any unresolved portion. Report issue changes by identifier and summary; the plan must remain understandable without transient issue links.

## 4. Use related workflows

Use these skills when available and compatible with project instructions. Otherwise follow the project's corresponding workflow; if none exists, ask for direction before inventing a process. Do not install a missing skill. If the user supplies a reusable convention, ask before recording it in project guidance; otherwise treat it as specific to this plan.

| When | Preferred skill and context |
| --- | --- |
| Planning or changing an approach that may touch settled decisions | `consult-design-docs`: identify the relevant binding decisions. If no workflow exists, suggest reading the decision index and only relevant records, treating superseded or archived records as history. |
| Starting non-trivial production implementation | `implement-feature`: pass the shared plan constraints and selected iteration; implement one iteration at a time. |
| Settling a decision that binds future work | `record-decision`: preserve context, decision, alternatives and consequences outside the plan. |
| Tracking or resolving repository-local issues | `manage-open-issues`: pass the gap, impact, originating plan, known next step or resolution evidence. |
| Closing a fulfilled plan | `finalize-plan`: compact and archive the whole plan, preserving decisions and loose ends through the project's workflows. |

When every exit criterion appears met, read the whole plan, verify each criterion and show the user evidence before setting status to `done`. Offer finalization; marking a plan done does not itself authorize compaction. If no close-out workflow exists, suggest one compact file under `docs/plans/completed/` with goal, non-goals, exit criteria as facts and outcome, plus reference cleanup, decision approval, issue tracking and any required changelog entries.
