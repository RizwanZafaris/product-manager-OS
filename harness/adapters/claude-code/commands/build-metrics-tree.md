---
name: build-metrics-tree
description: "Router row: A north star, a metrics tree, a metric definition, or a dashboard. OPERATE stage, Gate 6, judgment tier. Say: a north star; a metrics tree; a metric definition; a dashboard."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: build-metrics-tree

| Field | Value |
|---|---|
| Route id | `build-metrics-tree` |
| Router row | A north star, a metrics tree, a metric definition, or a dashboard |
| Stage | OPERATE |
| Gate | 6 |
| Tier | judgment. A tier name, never a model. |
| Skill | `skills/metrics-tree/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

A metric definition is never invented and never back-filled from a dashboard that already exists. A baseline with no source is an open field.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/metrics-tree/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 6 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `knowledge/north-star-metric.md`
- `frameworks/metrics/north-star-input-tree.md`

## Templates the output lands in

- `templates/planning/north-star-metric.md`
- `templates/operate/metrics-dictionary.md`
- `templates/operate/dashboard-spec.md`

## Invariants that bind this route

- `no-fabrication`
- `human-signs-gate`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `a north star`
- `a metrics tree`
- `a metric definition`
- `a dashboard`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
