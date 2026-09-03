---
name: tutor-learning-path
description: "Router row: \"learn\", \"teach me\", \"quiz me\", \"study\", or practice on a fictional product. No stage and no gate, drafting tier. Say: learn; teach me; quiz me; study; practice on a fictional product."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: tutor-learning-path

| Field | Value |
|---|---|
| Route id | `tutor-learning-path` |
| Router row | "learn", "teach me", "quiz me", "study", or practice on a fictional product |
| Stage | None. See the note below. |
| Gate | None. See the note below. |
| Tier | drafting. A tier name, never a model. |
| Skill | `learn/skills/tutor/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

Practice artifacts go under learn/products/, never under products/, and never into templates/. The learn lane depends downward only, so nothing here writes back into the OS.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `learn/skills/tutor/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. This route produces no template artifact. Say what you found and stop.
4. There is no gate on this output. Do not invent one, and do not report a gate as passed.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `learn/README.md`
- `learn/path-foundations.md`
- `learn/path-senior.md`
- `learn/path-transitioning.md`
- `learn/library.md`

## Templates the output lands in

None. This route writes no template.

## Invariants that bind this route

- `no-fabrication`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `learn`
- `teach me`
- `quiz me`
- `study`
- `practice on a fictional product`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
