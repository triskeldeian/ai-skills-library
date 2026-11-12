---
name: finalize-plan
description: Use it when the user confirms an existing plan is fulfilled, asks to archive, close out, or compact a plan, or when you notice that the plan's exit criteria are all met.
---

# Finalizing a completed plan

Compact a fulfilled plan into one historical record, preserving lasting decisions and tracking loose ends outside it. If the user has not explicitly requested finalization, ask for confirmation before compaction; a `done` status alone is not authorization.

Read the complete source before changing it:

- **Single-file plan:** read the file in full; keep its filename for the completed record.
- **Folder plan:** whether given the folder or its `PLAN.md`, read `PLAN.md` and every iteration document, including dropped iterations and any omitted from the index. Check the index, graph and files agree; resolve missing files or discrepancies before proceeding. Inspect any other folder contents before removal, preserving material that still has a purpose outside the compact record. Use the folder name for the completed filename: `NNNN-short-slug/PLAN.md` becomes `completed/NNNN-short-slug.md`.

Confirm that every exit criterion is satisfied. If the plan is still in progress or a criterion is unmet, stop and report the gap; a stale `done` label does not override it.

Before replacing or removing any source, resolve decision-record questions (step 3) and secure loose-end tracking (step 4). Use the completed path for origin links. Preserve the source context while any required answer or tracking location is pending.

## 1. Compact the plan itself

Draft one completed document from the whole source using [the completed-plan template](assets/completed-plan-template.md). For a folder plan, synthesize the iteration outcomes rather than concatenating documents. Keep the plan number and title, mark it `done`, record the completion date and use these sections in order:

- **Goal** — one short paragraph. What this slice was trying to prove or deliver, and why (tie back to the ADR or requirement it served). Cut the surrounding scene-setting.
- **Non-goals** — keep as a bullet list if the original plan had one. This is cheap to keep and useful later: it tells a reader what boundary was deliberately drawn, without them having to guess whether something missing was an oversight or a choice. Trim per-bullet rationale down to a clause, not a paragraph.
- **Exit criteria** — keep as a checklist, restated as verified facts now that the plan is done. This preserves the plan's own definition of success.
- **Outcome** — what was actually shipped, described as current-state fact ("Shipped X that does Y"), not as a diff against the plan. Do not itemize every deviation from the original plan and explain why each happened — that's process narrative. If a deviation left a lasting fact worth knowing (a stage name, a version pin), fold it into the Outcome sentence itself rather than listing it separately.

Drop entirely: file-by-file implementation walkthroughs, rationale for micro-decisions that are just visible in the code (naming, layout), "what happens next" speculation (superseded by whatever plan actually came next — link forward if useful, don't re-narrate it), and any options-considered tables (that reasoning either made it into an ADR already or wasn't important enough to).

## 2. Move it and fix links

Follow the project's existing archive location or an explicit user-selected destination; otherwise use `docs/plans/completed/`. Keep the source filename for a single-file plan; use `<plan-folder-name>.md` for a folder plan. Create the destination directory if needed. If a different record already occupies that path, resolve the conflict rather than overwriting it.

- Search the whole repository for references to the old filename or folder, `PLAN.md`, individual iteration filenames and the plan number, accounting for relative links and anchors.
- For each reference found, don't just repoint the path. A completed plan is historical reference only — it may be trimmed or deleted later — so no other document should depend on a reader opening it to understand what it says. Rewrite the reference into a self-contained statement, in that document's own words, of what was decided or shipped and the current status of the system. Keep an actual link to the completed record only where there's a real reason to point a reader at the full historical record (e.g. a plans index) — not as a stand-in for stating the outcome in place.
- In current-state summaries such as an AGENTS.md Status section, keep only relevant facts about what now exists or behaves differently; remove iteration lists and historical plan links.
- Remove dependencies on discarded section or iteration anchors. Rebase retained relative links, including links copied from iteration documents, from the completed file's location. Verify links in the completed record and all changed references, including issue origin links.

Only after the compact record and reference updates are verified, decisions and loose ends are handled, and any other folder material is preserved where needed, remove the original plan file or folder. Do not delete unrelated content or commit without the user's approval.

## 3. Decisions worth an ADR — ask, don't decide

While reading the plan, flag anything that reads as a real design decision: an architectural choice, a library/API commitment, a convention meant to bind future work — as opposed to implementation trivia that's obvious from the code.

For each candidate:

- First check whether it is already captured in a current decision record, such as an ADR. If so, there is nothing to do.
- If not, **do not silently create or edit a decision record.** Ask the user (with your harness's structured-question tool if it has one, otherwise in plain text) to choose: record the decision, supersede an existing decision record, or skip it as not worth recording.
- Once the user has picked, use the `record-decision` skill if it is available to create or supersede the decision record. Otherwise, follow applicable agent or project guidance; if none covers decision records, ask the user for direction before creating one. Never amend an accepted decision record — a changed decision is recorded by superseding it.
- Only create or edit a decision record after the user has answered.

If nothing in the plan rises to this level, say so rather than asking a question with no real candidates behind it.

## 4. Loose ends — file them, then report them

Before discarding plan detail, identify unresolved follow-ups that need tracking beyond this plan. Keep a deliberate scope deferral in the relevant decision record; do not create a duplicate for work already covered by an issue or another plan. An unmet exit criterion is a reason to revisit completion, not something to hide in a new issue.

For repository-local issues, use `manage-open-issues` if available and compatible with project guidance. Pass each gap, its impact, the completed plan's final path, and any known next step. Also hand off existing issues resolved by the plan, with verification evidence, keeping partially unresolved ones open. Otherwise, follow the project's issue workflow. If neither is available, report the follow-ups and ask where to track them before creating a new system; preserve their context until that is settled. Do not discard loose ends during compaction before their tracking is secured.

Do not just file these quietly — after finalizing, **tell the user which new open issues were identified**, by name/summary, so they can decide whether each one stays here or gets moved to a different tracking system.

## 5. Changelog

If the repository maintains a changelog, verify that it records the user-visible work shipped by the plan and add any missing entry. Use the repository's preferred changelog-management skill or workflow, if one is available; otherwise follow applicable agent or project guidance and the repository's documented format and conventions. Write from the user's point of view — what can now be done or behaves differently — and clearly identify breaking changes according to those conventions. Do not link to the plan or describe its implementation process. If the plan shipped nothing user-visible, or the repository does not maintain a changelog, add nothing and say so in the report. Do not create a changelog solely for this process.

## 6. Report back

Summarize: what the plan was compacted to, which ADR question(s) (if any) were asked and how they were answered, which issues (if any) were created, updated, or closed, any follow-ups still awaiting a tracking location, and which changelog entries (if any) were added. Report issues by identifier and summary. Distinguish the approval required for ADRs from reporting issue maintenance.
