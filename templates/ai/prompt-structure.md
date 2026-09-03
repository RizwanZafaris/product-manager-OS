---
layer: templates
stage: AI OVERLAY
gate: 4
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Prompt Structure", "prompt-structure"]
---
# Prompt Structure: [feature name]

Stage: AI overlay, active whenever the product contains a model; feeds Gate 4 (acceptance criteria met)
Knowledge: ../../knowledge/INDEX.md
Skill: ../../skills/ai-prd/SKILL.md

<!-- The system prompt is production code that happens to be prose. It gets a version,
     an owner, a change process, and a test suite (the eval spec), or it gets edited
     live in a dashboard at 6pm and nobody can say why Tuesday's outputs differ from
     Monday's. This document is the source of truth for one prompt; one file per prompt. -->

**Prompt ID:** [stable identifier, e.g. support-triage-v3]
**Current version:** [n] · **Pinned model version:** [exact version string]
**Prompt owner:** [name] · **Document date:** [YYYY-MM-DD]

## 1. Prompt sections, in order

<!-- Write the actual prompt content into each field, or link the file that holds it.
     The section order below is deliberate: role before task, constraints before
     examples, output contract last so it is nearest the generation. -->

- **Role:** [who the model is, one paragraph, no superlatives]
- **Task:** [what it does with each input, stated as behavior, not aspiration]
- **Constraints and guardrails:** [the prompt-level rails, mirrored from the filled guardrails.md; every rail here has a backstop outside the prompt]
- **Grounding and abstain rules:** [what it may state facts from and what it says when it cannot, mirrored from hallucination-controls.md]
- **Few-shot slots:** [n examples; each slot lists the case it teaches and why it earns its tokens]
- **Output contract:** [exact format: schema, fields, length bounds; the thing code parses]

## 2. Few-shot inventory

| Slot | Example teaches | Source (real case, sanitized / synthetic) | Last reviewed |
|---|---|---|---|
| 1 | [e.g. the correct abstain wording] | [synthetic] | [date] |
| 2 | [e.g. a refusal done right] | [real, sanitized by [name]] | [date] |
| [add] | | | |

## 3. Change process

- A prompt change is a version bump, never an in-place edit: [where versions live]
- Every version bump re-runs the eval spec (eval-spec.md) before deploy; the result is linked in the change log
- Who can approve a prompt change: [role]
- Rollback: previous version deployable in [n minutes], by [role]

## 4. Change log

| Version | Date | Change (one sentence) | Reason | Eval result link | Approved by |
|---|---|---|---|---|---|
| [n] | [YYYY-MM-DD] | [what changed] | [why] | [link] | [name] |

## Worked micro-example

Change-log row: version 4, 2026-08-12, "moved the abstain rule above the few-shot block", reason "abstain rate dropped after examples were added; position fixed it", eval run 2026-08-12 linked green, approved by A. Reviewer. Six months later this row is the answer to "why is the abstain rule up there", which otherwise costs an afternoon of archaeology.

## Exit gate

- [ ] The prompt has a stable ID, a version, and a pinned model version
- [ ] Every section 1 field contains real content or a resolving link, not a summary of intent
- [ ] Every few-shot slot says what it teaches; no example rides along unexplained
- [ ] The change process makes an untested prompt change impossible, not just discouraged
- [ ] The change log has an entry for the current version
