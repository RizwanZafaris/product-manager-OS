---
name: design-experiment
description: "Router row: An A/B test, an experiment, or \"how would we know if this worked\". OPERATE stage, Gate 6, judgment tier. Say: an A/B test; an experiment; how would we know if this worked."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: design-experiment

| Field | Value |
|---|---|
| Route id | `design-experiment` |
| Router row | An A/B test, an experiment, or "how would we know if this worked" |
| Stage | OPERATE |
| Gate | 6 |
| Tier | judgment. A tier name, never a model. |
| Skill | `skills/experiment-designer/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/experiment-designer/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 6 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `templates/operate/metrics-dictionary.md`
- `frameworks/metrics/aarrr-funnel.md`

## Templates the output lands in

- `templates/operate/experiment-brief.md`

## Invariants that bind this route

- `no-fabrication`
- `human-signs-gate`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `an A/B test`
- `an experiment`
- `how would we know if this worked`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
