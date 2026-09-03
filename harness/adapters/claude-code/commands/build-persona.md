---
name: build-persona
description: "Router row: Who this is for, a persona, a job story, a journey map, or an opportunity tree. DISCOVER stage, Gate 1, drafting tier. Say: who this is for; a persona; a job story; a journey map; an opportunity tree."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: build-persona

| Field | Value |
|---|---|
| Route id | `build-persona` |
| Router row | Who this is for, a persona, a job story, a journey map, or an opportunity tree |
| Stage | DISCOVER |
| Gate | 1 |
| Tier | drafting. A tier name, never a model. |
| Skill | `skills/persona-builder/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

A persona built on fewer than five cited interviews is marked as an assumption at Gate 1. The manifest cannot enforce that; the gate checklist does.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/persona-builder/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 1 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `knowledge/jobs-to-be-done.md`
- `templates/discovery/evidence-note.md`

## Templates the output lands in

- `templates/discovery/personas.md`
- `templates/discovery/jtbd-spec.md`
- `templates/discovery/journey-map.md`
- `templates/discovery/problem-framing.md`
- `templates/discovery/opportunity-solution-tree.md`

## Invariants that bind this route

- `no-fabrication`
- `human-signs-gate`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `who this is for`
- `a persona`
- `a job story`
- `a journey map`
- `an opportunity tree`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
