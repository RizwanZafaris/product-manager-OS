---
name: plan-gtm-launch
description: "Router row: A launch plan, go-to-market, or channel and comms sequencing. DELIVER stage, Gate 5, drafting tier. Say: a launch plan; go-to-market; channel and comms sequencing."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: plan-gtm-launch

| Field | Value |
|---|---|
| Route id | `plan-gtm-launch` |
| Router row | A launch plan, go-to-market, or channel and comms sequencing |
| Stage | DELIVER |
| Gate | 5 |
| Tier | drafting. A tier name, never a model. |
| Skill | `skills/gtm-launch-planner/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

This route drafts text that leaves the building. Nothing in the comms plan is sent by the harness; the plan is queued and a named human releases it.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/gtm-launch-planner/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 5 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `templates/delivery/customer-comms.md`
- `knowledge/crossing-the-chasm.md`

## Templates the output lands in

- `templates/planning/gtm-plan.md`
- `templates/delivery/launch-comms-plan.md`

## Invariants that bind this route

- `no-fabrication`
- `human-approves-send`
- `human-signs-gate`
- `no-blind-retry`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `a launch plan`
- `go-to-market`
- `channel and comms sequencing`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
