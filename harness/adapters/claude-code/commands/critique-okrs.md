---
name: critique-okrs
description: "Router row: Drafting or critiquing OKRs. No stage and no gate, judgment tier. Say: draft our OKRs; critique these OKRs."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: critique-okrs

| Field | Value |
|---|---|
| Route id | `critique-okrs` |
| Router row | Drafting or critiquing OKRs |
| Stage | None. See the note below. |
| Gate | None. See the note below. |
| Tier | judgment. A tier name, never a model. |
| Skill | `skills/okr-critic/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

PLANNING overlay. OKRs supply the targets Gate 6 verifies; the OKR set itself is not gated.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/okr-critic/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. There is no gate on this output. Do not invent one, and do not report a gate as passed.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `knowledge/okrs.md`

## Templates the output lands in

- `templates/planning/okrs.md`

## Invariants that bind this route

- `no-fabrication`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `draft our OKRs`
- `critique these OKRs`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
