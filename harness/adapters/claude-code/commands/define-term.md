---
name: define-term
description: "Router row: \"What does <term> mean here\", or a word being used in a narrower sense than the industry uses it. No stage and no gate, extraction tier. Say: what does this term mean here; you are using that word narrowly."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: define-term

| Field | Value |
|---|---|
| Route id | `define-term` |
| Router row | "What does <term> mean here", or a word being used in a narrower sense than the industry uses it |
| Stage | None. See the note below. |
| Gate | None. See the note below. |
| Tier | extraction. A tier name, never a model. |
| Skill | None. This row names no skill; the reads below carry the procedure. |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

No skill: read the entry, then follow its link, because the governing file wins over the definition.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. There is no skill for this row. The reads are the procedure. Do not substitute a skill that looks close.
3. This route produces no template artifact. Say what you found and stop.
4. There is no gate on this output. Do not invent one, and do not report a gate as passed.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `GLOSSARY.md`

## Templates the output lands in

None. This route writes no template.

## Invariants that bind this route

- `no-fabrication`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `what does this term mean here`
- `you are using that word narrowly`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
