---
name: write-ai-prd
description: "Router row: A PRD for an AI-powered feature, or any spec where a model produces the output. DEFINE stage, Gate 2, drafting tier. Say: a PRD for an AI feature; a spec where a model produces the output; an AI PRD."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: write-ai-prd

| Field | Value |
|---|---|
| Route id | `write-ai-prd` |
| Router row | A PRD for an AI-powered feature, or any spec where a model produces the output |
| Stage | DEFINE |
| Gate | 2 |
| Tier | drafting. A tier name, never a model. |
| Skill | `skills/ai-prd/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

The overlay's eval thresholds become blocking checks at Gate 4 and Gate 5. The gate named here is the one that signs the requirements.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/ai-prd/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 2 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `knowledge/domains/ai-products.md`
- `os/WHICH-DOCUMENT.md`

## Templates the output lands in

- `templates/definition/prd.md`
- `templates/ai/eval-spec.md`
- `templates/ai/guardrails.md`
- `templates/ai/hallucination-controls.md`
- `templates/ai/human-approval-gates.md`
- `templates/ai/prompt-structure.md`
- `templates/ai/context-management.md`
- `templates/ai/model-card.md`
- `templates/ai/agent-architecture.md`
- `templates/ai/multi-agent-workflow.md`
- `templates/ai/red-team-review.md`

## Invariants that bind this route

- `no-fabrication`
- `human-signs-gate`
- `human-approves-send`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `a PRD for an AI feature`
- `a spec where a model produces the output`
- `an AI PRD`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
