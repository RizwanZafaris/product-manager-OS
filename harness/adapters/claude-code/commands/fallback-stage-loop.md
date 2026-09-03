---
name: fallback-stage-loop
description: "Router row: Anything else in the product loop. No stage and no gate, drafting tier. Say: anything else in the product loop."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: fallback-stage-loop

| Field | Value |
|---|---|
| Route id | `fallback-stage-loop` |
| Router row | Anything else in the product loop |
| Stage | None. See the note below. |
| Gate | None. See the note below. |
| Tier | drafting. A tier name, never a model. |
| Skill | None. This row names no skill; the reads below carry the procedure. |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

The catch-all, and the only entry whose stage is decided at run time: find the stage in os/OPERATING-LOOP.md, fill that stage's template, take it to that stage's gate. Offer the Conductor once first, per load order step 0 in AGENTS.md. An unroutable request is queued and this table is amended, never guessed at.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. There is no skill for this row. The reads are the procedure. Do not substitute a skill that looks close.
3. Land the output in the template below that fits the request. One template, not all of them.
4. There is no gate on this output. Do not invent one, and do not report a gate as passed.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `AGENTS.md`
- `os/OPERATING-LOOP.md`
- `os/STAGE-GATES.md`
- `skills/conductor/SKILL.md`

## Templates the output lands in

- `templates/README.md`

## Invariants that bind this route

- `no-fabrication`
- `human-signs-gate`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `anything else in the product loop`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
