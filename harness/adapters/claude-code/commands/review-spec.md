---
name: review-spec
description: "Router row: \"Is this spec any good\", a requirements review, or a draft that reads clear but cannot be tested. DEFINE stage, Gate 2, judgment tier. Say: is this spec any good; review these requirements; this reads clear but cannot be tested."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: review-spec

| Field | Value |
|---|---|
| Route id | `review-spec` |
| Router row | "Is this spec any good", a requirements review, or a draft that reads clear but cannot be tested |
| Stage | DEFINE |
| Gate | 2 |
| Tier | judgment. A tier name, never a model. |
| Skill | `skills/spec-review/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

Reports findings and never rewrites. This is the testability check, the second of the three separate checks in harness/INVARIANTS.md; a document that passes lint.py has not passed this.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/spec-review/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. This route produces no template artifact. Say what you found and stop.
4. Take the output to Gate 2 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `templates/definition/prd.md`
- `templates/definition/acceptance-criteria.md`
- `os/STAGE-GATES.md`

## Templates the output lands in

None. This route writes no template.

## Invariants that bind this route

- `no-fabrication`
- `human-signs-gate`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `is this spec any good`
- `review these requirements`
- `this reads clear but cannot be tested`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
