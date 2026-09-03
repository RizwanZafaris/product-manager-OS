---
name: check-regulatory-gaps
description: "Router row: Anything touching a regulator, license condition, scheme rule, or compliance question. DEFINE stage, Gate 2, judgment tier. Say: a regulator; a license condition; a scheme rule; a compliance question."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: check-regulatory-gaps

| Field | Value |
|---|---|
| Route id | `check-regulatory-gaps` |
| Router row | Anything touching a regulator, license condition, scheme rule, or compliance question |
| Stage | DEFINE |
| Gate | 2 |
| Tier | judgment. A tier name, never a model. |
| Skill | `skills/reg-gap-check/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

The overlay hooks the loop at Gate 2 and again at Gate 5; the gate named here is the earlier one, because a precondition constrains the solution space and is cheapest to find before requirements freeze. Files under modules/regulated/ are quoted verbatim and never edited here; the sha256 pins in lint.py enforce that.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/reg-gap-check/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 2 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `modules/regulated/README.md`
- `modules/regulated/SKILL.md`
- `templates/operate/compliance-impact-assessment.md`

## Templates the output lands in

- `modules/regulated/templates/regulated-ai-prd-template.md`

## Invariants that bind this route

- `no-fabrication`
- `human-signs-gate`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `a regulator`
- `a license condition`
- `a scheme rule`
- `a compliance question`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
