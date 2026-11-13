---
name: deep-factual-research
disable-model-invocation: true
description: >-
  Conduct or refresh a source-backed research study on a well-defined topic,
  recording verified findings, sources, assumptions, and open questions in a
  structured folder. Use only when the user explicitly asks for a deep or
  systematic factual study, in a harness that supports subagents.
---

# Deep Factual Research

Produce a research study folder that separates evidence from interpretation: a README entry point, neutral findings per subtopic, a source register, an analysis of implications and options, and an uncertainty record. A study is done when every claim traces to an inspected source, and every gap is recorded as a question rather than filled by inference.

Each study file has a template in `assets/`, named in the step that creates it; fill in the placeholders and delete its comments. When refining, keep the existing study's conventions where they differ.

## Shared rules

- **Evidence:** Only source text actually fetched and inspected supports a claim; prefer primary sources and label secondary ones. Search snippets, agent conclusions, user reports, and earlier findings are leads. Failing to verify a claim does not make it false, and absence from the inspected sources is not proof of absence.
- **Separation:** Findings files state what sources establish, with scope and limits, attribute a source's own assertions, and contain no recommendations. Assumptions, interpretations, and proposals are labeled and kept apart from sourced facts. Keep relevant, supported counterevidence to a preferred conclusion; drop superseded, irrelevant, or unverifiable claims, recording a still-relevant question as an uncertainty.
- **IDs:** Findings are `F<N>`, sources `S<N>`, uncertainties `U<N>`, unique study-wide; follow an existing convention if there is one.
  - Never renumber a retained record. Reuse a number only after every reference to the removed record is deleted.
  - Qualify a reference to another study's ID with a link to that study.
  - Delegates draft with provisional labels prefixed by their subtopic (`[memory-S1]`, `[memory-F1]`) and return any new ones.
  - The coordinating agent assigns final `F` and `S` IDs and is the only one to edit `sources.md`. The analyst assigns `U` IDs.
- **Statuses:** Label at-a-glance bullets and analytical statements with one of `Verified` (supported by inspected sources, not necessarily independently confirmed), `Reported` (attributed but unverified), `Assumption` (a working premise), `Unknown` (an unresolved question), `Interpretation` (an analytical judgment), or `Proposal` (a possible course of action). Cite the evidence behind an interpretation's premises, which does not mean the source endorses the conclusion; omit the citation on `Assumption` and `Proposal` rather than inventing one.
- **Dates:** Record actual consultation dates as `YYYY-MM-DD`; copying or reformatting evidence does not refresh them.
- **Delegation:** Never run the three roles below inline in the coordinating context. Give each delegate these shared rules and the template for the file it writes.
- **Scope:** Open new branches without asking when needed to answer the agreed questions within the user's boundaries and effort limits; defer nonessential ones as follow-up questions. Ask before materially expanding purpose, audience, or scope.
- **Gaps:** When a later step finds an evidence gap, the coordinator launches at most one bounded, targeted explorer for that gap within the user's effort limits, then reruns synthesis and analysis only for the affected subtopics. If the gap remains unresolved or the effort limit prevents follow-up, record it in `uncertainties.md`, keep affected conclusions conditional, and continue toward completion without retrying the same gap.

## Agent roles

A role names the capability a task needs, not a vendor or model; the level is a cost preference.

- `research-explorer` (step 4): bounded evidence collection for one subtopic. An economical model with low-to-moderate reasoning should suffice.
- `research-synthesizer` (step 5): assessing what recorded evidence supports, with targeted re-checks. Prefer a capable model with moderate-to-high reasoning.
- `research-analyst` (step 6): cross-subtopic analysis and uncertainty consolidation. Prefer the most capable model available with high reasoning.

Follow an explicit user instruction, else a harness agent definition named exactly like the role (used as defined; unavailable if it lacks tools the step needs), else the harness's own per-delegation model or reasoning options, else the session's model without asking; never guess identifiers. Rerun weak or unsupported output at a more capable level, or record the weakness as an uncertainty if none is available. Report only what was set or observed.

## 1. Establish the scope

Confirm that the harness can launch subagents and that you are allowed to. If not, stop and tell the user this skill needs a harness with subagent support.

Establish the topic, purpose, questions, boundaries, and exclusions from the request and context; for a refinement, also what is revisited, finding the existing study in the research folder (step 3) or asking for its path. Note the user's decision context (goals and constraints the study should inform), if any; if the request implies a decision but gives no criteria, ask once what the study should inform. List existing evidence, user-reported information, assumptions, and open questions, none of which is verified merely by being in context.

Confirm you can read sources: the web, or local copies with a full bibliographic reference or stored in the repository (a loose file with neither is not a source). Without source access, stop and report it, and offer a structural-only pass (steps 3 and 7 plus the link checks in step 8) that leaves findings, sources, and dates unchanged and notes in the README that the study was not re-verified.

Ask other questions only when an ambiguity could materially change the scope. State the resulting scope and unresolved assumptions, then continue unless the user objects.

Done when the scope, decision context (or its absence), and open assumptions are stated.

## 2. Map topics and supporting questions

Turn the request into a question-led map organized around capabilities, constraints, and decisions to inform, including alternatives and disconfirming evidence. A **topic** answers a substantial, standalone part of the request and is a study with its own numbered folder and README; split topics when they answer different questions or have materially different boundaries. A **subtopic** is a focused question suited to a bounded investigation and its own findings file, not a product, a source, or an arbitrary slice. Reuse existing studies.

Briefly present topics, questions, dependencies, and likely gaps or overlap; no user approval is needed when the scope is clear. Let the map grow as investigation shows dependencies: record each child question's parent and what it supports, and promote it to a topic if it warrants a standalone study or supports several. The coordinator reconciles proposed branches before assigning work, linking shared evidence instead of researching it twice, and stops branching when the evidence answers the parent question or a concrete unresolved item can be recorded. Folders stay flat; steps 5 to 8 run once per topic study, with no parent index unless the user asks.

Done when the map is presented and every question in the agreed scope is assigned to a topic.

## 3. Establish the research directory

Use the research folder named in the agent instructions (project guidance file or user's prompt); otherwise `docs/research/` under the project root (the working directory if there is none). Create it without asking if missing. If the user states a location as a reusable preference, ask whether to record it in the agent guidance file, and do so only with approval.

For each new topic, create `<number>-<kebab-title>` (for example `003-caching-strategies`). The number is the next integer after the highest numeric study prefix among existing folders and files (start at `001`, keep the existing digit width, minimum three). Never overwrite another study. When refining, reuse the existing folder, README, and source register without overwriting or relocating them unless asked.

Create `README.md` from [assets/readme-template.md](assets/readme-template.md) with only the title, `Scope` (only what was agreed in step 1), and `Sources`; do not link subtopic files from it before step 7. Create `sources.md` from [assets/sources-template.md](assets/sources-template.md) with the heading and no entries.
Done when each topic has its folder with `README.md` and `sources.md`, or, for a refinement, when the existing ones are located and reused.

## 4. Explore and record evidence

**Refreshing an existing study:** treat earlier findings and sources as leads and verify retained claims against currently accessible evidence, correcting wording, scope, versions, and citations. Remove superseded or contradicted claims; keep no historical snapshots or legacy sections, but age alone does not make evidence obsolete. A claim whose source is merely inaccessible now (blocked, paywalled) is not removed: leave it out of the findings and record the question as unverified. Give each explorer the existing findings file to edit in place, keeping retained IDs; step 5 then rewrites its summary paragraphs. Once claims are verified, keep the sources that support the output with their IDs, remove the rest, and repair references. Revise an existing `implications-and-options.md` and `uncertainties.md` in place, keeping their IDs, and create any missing study file from its template.

Run `research-explorer` subagents on the subtopics, in parallel where possible. Give each the topic scope, its parent question, relevant context, and a research question rather than a preferred conclusion, and ask for supporting and challenging evidence, overlooked alternatives, and conflicting sources. Prefer current primary sources; check dates, versions, and applicability; record inaccessible or partial evidence, conflicts, and gaps.

Each explorer writes one kebab-case findings file in the study folder from [assets/findings-template.md](assets/findings-template.md) using provisional labels, and returns exact source references (with publisher and primary or secondary, version or date, and access level), consultation dates, evidence limits, and a finding-to-source mapping. The coordinator assigns final IDs, reconciles sources into `sources.md`, and ensures every finding cites its sources.

Done when every subtopic has a findings file whose findings all cite registered sources.

## 5. Synthesize neutral topic summaries

For each subtopic, assign a fresh `research-synthesizer` separate from its explorer, giving it the scope, the findings file, and the relevant `sources.md` entries, not the explorer's narrative or unrelated study files.

It assesses what the recorded evidence supports, keeping qualifications, contradictions, and gaps. It consults original sources for consequential, ambiguous, or contested claims, and follows up on unsupported claims instead of inferring, omitting those that stay unsupported and recording the question. Evidence it recovers goes into the study files with provisional labels and updated dates, which the coordinator finalizes as in step 4. Above the findings, it writes the cited Context and Evidence synthesis paragraphs described in the template.

Done when each findings file opens with both paragraphs and no provisional labels remain.

## 6. Analyze implications and choices

Assign a fresh `research-analyst`, giving it the scope, the user's decision context, all findings and summaries, the source register, and relevant assumptions and open questions. Do not have it infer priorities or policy from the sources. It connects evidence across subtopics, identifying dependencies, tensions, and combined constraints; independently supported components do not show their combination works, and repeated claims from one underlying source are not independent corroboration.

The analyst writes `implications-and-options.md` from [assets/implications-and-options-template.md](assets/implications-and-options-template.md): implications of the evidence across subtopics and, only with a decision context, possible choices (including keeping the current approach or deferring, compared on criteria from that context, without arbitrary scores) and conditional recommendations (which alternative appears preferable, under what assumptions, and what evidence would change that; if the evidence cannot distinguish them, name the validation needed). Label judgments, assumptions, and proposals with the Statuses above. Do not invent findings to fill a comparison; report material gaps to the coordinator (see Gaps). Recommendations are proposals, not authorization to implement.

It also consolidates open questions from all earlier steps, including unverified assumptions and unresolved source conflicts, into `uncertainties.md` from [assets/uncertainties-template.md](assets/uncertainties-template.md). Drop inherited questions that no longer affect the study, merge duplicates keeping provenance, and mark nothing resolved without evidence. If the user names a tracker holding a question's canonical record, link to it instead of keeping a competing status. A proposed follow-up does not expand scope or authorize an experiment or prototype. Then link the `U` IDs from the findings files' "Assumptions and open questions" and from caveats on conclusions.

Done when both files exist and every caveat on a conclusion links to its uncertainty record.

## 7. Finalize the research entry point

Complete the remaining sections of [assets/readme-template.md](assets/readme-template.md) from the summaries, analysis, and uncertainty records. Preserve the original scope: flag any evidence-driven scope change for clarification instead of absorbing it. Keep detailed findings in their files and material caveats visible. If the user gave no decision context, say so in Scope and summarize only the implications of the evidence.

Each at-a-glance bullet carries one status (see Statuses).

Done when the reading guide links every findings file, `implications-and-options.md`, and `uncertainties.md`, and the README summaries match the detailed files.

## 8. Review consistency

Run one bounded review (not a new research round) of all generated or revised study documents; the coordinator performs it and does not claim it is independent. Check scope fidelity and topic-map coverage, README agreement with the detailed files, traceability of findings, dates, and comparisons to sources, and local links, anchors, and IDs, plus external reachability where possible (a working URL does not verify its claims). Preserve genuine source conflicts. For a refreshed study, also check for stale or unchecked inherited claims, obsolete questions, and legacy sections.

Fix unambiguous editorial, citation, and navigation errors without changing scope or conclusions, and recheck them; handle evidence gaps as under Gaps.

Report issues by file and section, with significance and whether corrected or open, separating those affecting meaning, confidence, or choices from minor edits; otherwise state "no findings", with coverage and checks not performed. For each role, say whether it ran from a defined agent, a requested level, or the inherited session model, and any rerun at a higher level. Do not invent timing or token costs, or create a separate review document unless asked.

Done when the corrections are rechecked and the report has been given to the user.
