---
name: pick-document-weight
description: "Router row: \"How much document does this need\", or a request for a spec whose weight is unclear. DEFINE stage, Gate 2, drafting tier. Say: how much document does this need; does this need a full PRD."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: pick-document-weight

| Field | Value |
|---|---|
| Route id | `pick-document-weight` |
| Router row | "How much document does this need", or a request for a spec whose weight is unclear |
| Stage | DEFINE |
| Gate | 2 |
| Tier | drafting. A tier name, never a model. |
| Skill | `skills/write-prd/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

Read the weight decision first, then draft at that weight. Defaulting to the heaviest artifact is a real failure mode, and so is a ticket for a quarter of work.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/write-prd/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 2 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `os/WHICH-DOCUMENT.md`

## Templates the output lands in

- `templates/definition/one-pager.md`
- `templates/definition/prd.md`

## Invariants that bind this route

- `no-fabrication`
- `human-signs-gate`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `how much document does this need`
- `does this need a full PRD`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
