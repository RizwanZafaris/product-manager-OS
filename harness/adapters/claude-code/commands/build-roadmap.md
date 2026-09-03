---
name: build-roadmap
description: "Router row: A roadmap, quarterly plan, OKR set, or a stress-test of an existing one. No stage and no gate, judgment tier. Say: a roadmap; a quarterly plan; an OKR set; stress-test our roadmap."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: build-roadmap

| Field | Value |
|---|---|
| Route id | `build-roadmap` |
| Router row | A roadmap, quarterly plan, OKR set, or a stress-test of an existing one |
| Stage | None. See the note below. |
| Gate | None. See the note below. |
| Tier | judgment. A tier name, never a model. |
| Skill | `skills/roadmap-builder/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

PLANNING overlay: reviewed on its own cadence, not at a gate, per os/OPERATING-LOOP.md.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/roadmap-builder/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. There is no gate on this output. Do not invent one, and do not report a gate as passed.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `frameworks/prioritization/rice-scoring-sheet.md`
- `knowledge/rice-prioritization.md`

## Templates the output lands in

- `templates/planning/roadmap.md`
- `templates/planning/okrs.md`

## Invariants that bind this route

- `no-fabrication`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `a roadmap`
- `a quarterly plan`
- `an OKR set`
- `stress-test our roadmap`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
