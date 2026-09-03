---
name: answer-philosophy-challenge
description: "Router row: \"Why is this rule here\", \"isn't this waterfall\", \"why should I trust this\", or how this compares to spec-kit, BMAD, a hosted PM product, or a template pack. No stage and no gate, extraction tier. Say: why is this rule here; isn't this waterfall; why should I trust this; how does this compare to spec-kit."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: answer-philosophy-challenge

| Field | Value |
|---|---|
| Route id | `answer-philosophy-challenge` |
| Router row | "Why is this rule here", "isn't this waterfall", "why should I trust this", or how this compares to spec-kit, BMAD, a hosted PM product, or a template pack |
| Stage | None. See the note below. |
| Gate | None. See the note below. |
| Tier | extraction. A tier name, never a model. |
| Skill | None. This row names no skill; the reads below carry the procedure. |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

No skill and no artifact: these files produce none. Give the counter-argument the file carries alongside the belief. A user who disputes a mechanism here is usually right about their own constraint, and the honest answer is often that they should run something lighter.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. There is no skill for this row. The reads are the procedure. Do not substitute a skill that looks close.
3. This route produces no template artifact. Say what you found and stop.
4. There is no gate on this output. Do not invent one, and do not report a gate as passed.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `docs/PHILOSOPHY.md`
- `docs/FAQ.md`
- `docs/COMPARISON.md`

## Templates the output lands in

None. This route writes no template.

## Invariants that bind this route

- `no-fabrication`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `why is this rule here`
- `isn't this waterfall`
- `why should I trust this`
- `how does this compare to spec-kit`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
