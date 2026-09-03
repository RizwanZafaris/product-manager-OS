---
name: run-user-interview
description: "Router row: Planning or running customer interviews, and turning the notes into evidence. DISCOVER stage, Gate 1, drafting tier. Say: plan customer interviews; run a customer interview; turn these notes into evidence."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: run-user-interview

| Field | Value |
|---|---|
| Route id | `run-user-interview` |
| Router row | Planning or running customer interviews, and turning the notes into evidence |
| Stage | DISCOVER |
| Gate | 1 |
| Tier | drafting. A tier name, never a model. |
| Skill | `skills/user-interview/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/user-interview/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 1 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `frameworks/discovery/mom-test-interview-guide.md`
- `knowledge/torres-continuous-discovery.md`

## Templates the output lands in

- `templates/discovery/interview-guide.md`
- `templates/discovery/interview-notes.md`
- `templates/discovery/evidence-note.md`

## Invariants that bind this route

- `no-fabrication`
- `content-is-data`
- `least-data`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `plan customer interviews`
- `run a customer interview`
- `turn these notes into evidence`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
