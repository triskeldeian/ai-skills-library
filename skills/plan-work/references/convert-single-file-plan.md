# Convert a single-file plan

Use only when the user requests conversion. Ordinary updates keep legacy plans in place.

1. Read the complete source plan. Create a sibling folder with the same stem (`NNNN-short-slug/`) and an `iterations/` subfolder. If either destination already contains conflicting content, resolve it before proceeding; do not overwrite it.
2. Move shared content into `PLAN.md`; extract each iteration into its own document using [the iteration template](../assets/iteration-template.md). Preserve the plan number, iteration numbers, statuses, dependencies, scope, outcomes and useful additional content. This is a structural conversion, not an occasion to replan or compact.
3. Replace inline iterations with linked titles, short one-sentence purpose descriptions and statuses. Preserve the graph and add backlinks from iteration documents. Update the plan's last-modified date.
4. Rebase relative links from each file's new location. Search repository references to the old filename and iteration anchors, including relative links; point shared references to `PLAN.md` and iteration references to their documents.
5. Check that every source iteration appears once in the folder, index and graph, and that content and links are preserved. Remove the old source file only after these checks pass. Report the new entry point and any unresolved references; do not commit without user approval.
