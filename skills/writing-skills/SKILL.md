---
name: writing-skills
description: Draft, review, and refine reusable agent skills. Use when creating a SKILL.md, turning a workflow or notes into a skill, or improving an existing skill's instructions and supporting resources.
---

# Writing Skills

Write concise guidance that changes how an agent approaches a recurring class of problems. Use the user's notes and demonstrated workflow as the starting point; preserve their priorities when choosing structure and detail.

## Workflow

### 1. Establish the scope

Read the user's source material, the existing skill if any, and applicable repository instructions. Identify the requests the skill should handle, the reusable approach it should teach, and what successful execution looks like.

Proceed from the available context. Ask only when missing information would materially change the skill's scope or behavior. Keep project-specific facts in project instructions unless they are necessary to the skill's reusable workflow.

Finish with a clear purpose and an observable outcome. A particular example can illustrate the approach; it should not silently become the only supported case.

### 2. Select what the agent needs

Include domain knowledge, decisions, conventions, and failure modes that the agent would otherwise miss. Assume familiarity with the task's basic concepts; spend words on information that changes execution.

When unsure whether background is necessary, probe the agent's unaided understanding if a separate context is available. Compare its answer with the required knowledge. Otherwise, treat the assumption as unverified and use concrete execution failures to decide what to add.

Remove introductions, repeated rules, and explanations that merely restate common knowledge. Keep the material needed to perform the workflow and recognize success.

### 3. Choose the instruction style

Default to concise, ordered steps. For each step, make the action and its completion condition clear.

- **Prescribe the procedure** when the answer is known, reproducibility matters, or the operation depends on a particular sequence. Specify the relevant inputs, actions, and checks so the agent need not rediscover them.
- **State intent and decision criteria** when several approaches can work. Give the desired outcome and constraints, leaving implementation choices to the agent.
- **Provide one sensible default** for routine choices. Introduce an alternative only when a concrete condition makes the default unsuitable, and state that condition next to the alternative.

Teach how to solve the class of problems. Use examples and output templates only where they clarify a decision or a required deliverable.

### 4. Organize the skill

Create `<kebab-case-name>/SKILL.md` in the user's requested location, following the target repository's conventions. Use YAML frontmatter with a unique `name` matching the directory and a concise `description` stating the capability and when to use it.

Keep the entrypoint comfortably below 500 lines and 5,000 tokens; these are ceilings to stay under, not targets to fill. Prefer a single focused document until the content justifies supporting files.

- Keep the essential workflow, shared constraints, and gotchas in `SKILL.md`.
- Move substantial guidance for conditional situations into `references/`. Link each reference where its branch becomes relevant, stating when to read it. Keep information in one authoritative place.
- Add `scripts/` when repeated or fragile operations benefit from a tested implementation. Document inputs, outputs, prerequisites, and failure modes.
- Add `assets/` only for static material the workflow actually uses.

Keep common instructions harness-neutral. Label any necessary harness-specific sections and verify the relevant capabilities rather than assuming tool names, paths, shell behavior, or invocation controls are universal.

### 5. Review and exercise

Review the draft against the user's source material. Check that each important preference changes an instruction or decision, without turning every observation into an absolute rule.

Check frontmatter, names, local links, required resources, and any commands or scripts. Exercise a representative request and one likely failure or boundary case, checking whether the agent follows the intended approach and recognizes completion. When evaluating behavior, compare with an unaided run or the previous version where practical; distinguish actual execution from a document walkthrough.

Verify discovery using the target environment's tooling. Keep installation separate from discovery.

Prune instructions that add noise or unnecessarily constrain reasonable solutions. Finish by stating what was drafted, what was checked, and what still needs behavioral validation. A request for an initial draft does not require a full evaluation framework.

## Gotchas

Keep surprising conventions visible here when the agent needs them to recognize a problem. Conditional reference material is suitable only when the agent can reliably recognize its trigger without reading that material first.

- A valid file and successful discovery establish packaging, not usefulness. Verify the approach on realistic requests before claiming the skill improves results.
- Add a gotcha when an observed interaction reveals a reusable trap. State the condition and the corrective action; consolidate or remove entries as the workflow changes.
