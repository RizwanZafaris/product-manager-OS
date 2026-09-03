---
name: run-premortem
description: "Router row: A premortem, \"what could kill this\", or any risk pass before Gate 3. DESIGN stage, Gate 3, judgment tier. Say: a premortem; what could kill this; a risk pass before Gate 3."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: run-premortem

| Field | Value |
|---|---|
| Route id | `run-premortem` |
| Router row | A premortem, "what could kill this", or any risk pass before Gate 3 |
| Stage | DESIGN |
| Gate | 3 |
| Tier | judgment. A tier name, never a model. |
| Skill | `skills/program-premortem/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

Fail closed matters here more than anywhere: a premortem rerouted to a cheaper tier produces a document that looks reviewed and is not, which is worse than a late one. Queue instead.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/program-premortem/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 3 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `frameworks/execution/premortem-worksheet.md`
- `frameworks/execution/risk-matrix.md`

## Templates the output lands in

- `templates/execution/risk-register.md`
- `templates/execution/dependency-register.md`

## Invariants that bind this route

- `no-fabrication`
- `human-signs-gate`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `a premortem`
- `what could kill this`
- `a risk pass before Gate 3`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
