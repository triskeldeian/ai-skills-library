---
name: manage-open-issues
description: Use this skill to create, update, or close repository-local issue records and keep their index consistent. It does not decide which concerns warrant an issue.
---

# Managing open issues

Maintain the repository's issue records once the user or calling workflow has identified what to track, update, or close. The caller supplies the scope and known context; this skill handles the record and its lifecycle.

## 1. Establish the conventions and target

Read applicable project and agent guidance, then locate the issue index, relevant records, and any project template. Follow existing paths, metadata, numbering, and closure rules. Do not migrate an existing system to the defaults below or create a parallel local tracker when the project uses another system.

For a repository-local issue without established conventions, use `docs/open-issues/`, one `NNNN-short-kebab-summary.md` file per issue, and a `README.md` index. Create the directory and index when filing the first issue. This default needs no runtime, environment variables, or external service.

Read the index and relevant issues before changing anything. Update an existing record when it already covers the item. Check any plan or decision record identified by the caller so the issue adds no competing status for work already tracked there. If the intended issue is ambiguous, clarify the target before editing or deleting a record.

## 2. File an issue

For the default layout:

1. Choose one more than the highest number among existing issue files, starting at `0001`. Recheck the index and filenames before saving; never overwrite a record. Numbers may be reused after closure and are not durable identifiers.
2. Copy [assets/issue-template.md](assets/issue-template.md) to `NNNN-short-kebab-summary.md`. Fill in the title, current gap and impact, origin, and date noted; delete guidance comments and omit the optional next step if unknown. Describe what is known, including what works today when relevant. Do not invent a cause or fix.
3. Keep `Status` as `Open`, optionally followed by a short qualifier. Closure removes the record rather than changing its status.
4. Add a row in number order to `README.md`, creating this table if needed:

   ```markdown
   # Open issues

   | Number | Summary | Origin |
   | --- | --- | --- |
   | [NNNN](NNNN-short-kebab-summary.md) | Short description of the gap | Origin description or link |
   ```

The file and index must describe the same origin. Make each relative link valid from its containing file. If the origin plan will move or be compacted, link to its final path and describe the gap independently of sections that may disappear. When the caller will perform that move, mark origin-link verification as pending in the handoff; the caller must verify it after moving the plan before reporting completion.

Keep essential context in prose wherever the issue is discussed. Under this default, avoid adding inbound links or number-only references from code or durable documentation: closure removes the file and a later issue may reuse its number. Stable references permitted by the project's own lifecycle remain valid.

## 3. Update an issue

Rewrite the record in place to reflect current facts, scope, and known next steps. Preserve its original date noted and origin unless correcting an error; do not append a dated activity log. Update the index row when its summary or origin changes.

When only part is resolved, retain the issue with the remaining gap and enough context to understand it. Do not close it merely because a related plan is complete or a fix is proposed.

## 4. Close an issue

Confirm that the tracked gap is resolved using the work's verification evidence, or that the user explicitly decided to drop it. Follow project closure rules; for the default layout:

1. Search the repository for the issue's filename, path, and number-based mentions such as `open issue NNNN`. Use `rg` or an available equivalent, including relevant hidden documentation and agent guidance; do not limit the search to tracked files. Inspect number matches in context to avoid changing unrelated records.
2. Rewrite references as self-contained statements of the resolution or disposition, optionally linking durable supporting documentation. Preserve historical meaning and essential context; repair links inside other issues too.
3. Delete the issue file and remove its index row in the same change. Do not leave a resolved status, stub, or strike-through. Retain the index and table headers when no issues remain. Use version history and any durable outcome documentation as the record.
4. If the repository maintains a changelog and the resolution is user-visible, follow its changelog workflow. Do not create a changelog solely for closing an issue.

## 5. Verify and report

Validate records against the project's conventions. For the default layout, check that each open issue has exactly one matching index row and numbers are unique among current records. Check that all changed links resolve, except origin links explicitly awaiting the caller's planned move; report those as pending until the caller verifies them. Confirm that no placeholders or guidance comments remain in a new issue. After closure, repeat the reference search and ensure no stale references remain; report any locations that could not be inspected or repaired.

In the task's final response, identify issues created, updated, partially resolved, or closed by the project's identifier (the number in the default layout) and summary, with paths for records that remain. A calling workflow may include this in its own report. Surface new issues so the user can review where they are tracked; do not silently file them or publish them to an external service.
