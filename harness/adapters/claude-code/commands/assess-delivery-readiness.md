---
name: assess-delivery-readiness
description: "Router row: \"Are we set up to ship this\", or whether the organization can carry the plan it just wrote. DEFINE stage, Gate 2, judgment tier. Say: are we set up to ship this; can the org carry this plan; is the team shaped for this."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: assess-delivery-readiness

| Field | Value |
|---|---|
| Route id | `assess-delivery-readiness` |
| Router row | "Are we set up to ship this", or whether the organization can carry the plan it just wrote |
| Stage | DEFINE |
| Gate | 2 |
| Tier | judgment. A tier name, never a model. |
| Skill | None. This row names no skill; the reads below carry the procedure. |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

These sheets score people and teams, so least-data binds: cite dated events and shipped work, never an appraisal, a name attached to a weakness, or anything a person said in confidence. A score with no cited event is an open field, and the culture sheet in particular is worthless when scored from stated values instead of from what happened.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. There is no skill for this row. The reads are the procedure. Do not substitute a skill that looks close.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 2 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `frameworks/assessment/product-operating-model-assessment.md`
- `frameworks/assessment/team-topologies-assessment.md`
- `frameworks/assessment/tech-debt-assessment.md`
- `frameworks/assessment/westrum-culture-typology.md`

## Templates the output lands in

- `templates/planning/capacity-plan.md`
- `templates/planning/product-strategy.md`

## Invariants that bind this route

- `no-fabrication`
- `human-signs-gate`
- `least-data`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `are we set up to ship this`
- `can the org carry this plan`
- `is the team shaped for this`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
