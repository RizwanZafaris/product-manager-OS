---
name: explain-role-scope
description: "Router row: \"What does a <title> do\", ladder, leveling, PM vs PMM, or role-scope questions. No stage and no gate, extraction tier. Say: what does a head of product do; leveling; PM vs PMM; what is in scope for this role."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: explain-role-scope

| Field | Value |
|---|---|
| Route id | `explain-role-scope` |
| Router row | "What does a <title> do", ladder, leveling, PM vs PMM, or role-scope questions |
| Stage | None. See the note below. |
| Gate | None. See the note below. |
| Tier | extraction. A tier name, never a model. |
| Skill | None. This row names no skill; the reads below carry the procedure. |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

No skill: the role cards answer the question and the two templates are what a reader does next.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. There is no skill for this row. The reads are the procedure. Do not substitute a skill that looks close.
3. Land the output in the template below that fits the request. One template, not all of them.
4. There is no gate on this output. Do not invent one, and do not report a gate as passed.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `knowledge/roles/README.md`
- `knowledge/roles/INDEX.md`

## Templates the output lands in

- `templates/planning/first-90-days.md`
- `templates/execution/stakeholder-map.md`

## Invariants that bind this route

- `no-fabrication`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `what does a head of product do`
- `leveling`
- `PM vs PMM`
- `what is in scope for this role`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
