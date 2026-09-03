---
name: conduct-product-journey
description: "Router row: \"start\", \"start a product\", or any wish to be interviewed through the loop. DISCOVER stage, Gate 1, judgment tier. Say: start; start a product; interview me through the loop."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: conduct-product-journey

| Field | Value |
|---|---|
| Route id | `conduct-product-journey` |
| Router row | "start", "start a product", or any wish to be interviewed through the loop |
| Stage | DISCOVER |
| Gate | 1 |
| Tier | judgment. A tier name, never a model. |
| Skill | `skills/conductor/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

Cross-examination and gate evaluation are the load-bearing calls, so the tier is judgment. Transcribing an accepted answer into STATE.md is extraction; both assignments are recorded in the taskMap in routing/omniroute.config.json.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/conductor/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 1 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `os/CONDUCTOR.md`
- `os/OPERATING-LOOP.md`
- `skills/conductor/questions/discover.md`

## Templates the output lands in

- `templates/execution/state.md`

## Invariants that bind this route

- `no-fabrication`
- `human-signs-gate`
- `fail-closed`
- `no-blind-retry`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `start`
- `start a product`
- `interview me through the loop`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
