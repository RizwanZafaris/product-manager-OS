---
name: write-stakeholder-update
description: "Router row: An executive or board update, or a narrative that has to land in one read. No stage and no gate, judgment tier. Say: an executive update; a board update; a narrative that lands in one read."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: write-stakeholder-update

| Field | Value |
|---|---|
| Route id | `write-stakeholder-update` |
| Router row | An executive or board update, or a narrative that has to land in one read |
| Stage | None. See the note below. |
| Gate | None. See the note below. |
| Tier | judgment. A tier name, never a model. |
| Skill | `skills/stakeholder-update/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

PLANNING cadence, not a gate. A human sends this under their own name, which is exactly the class of artifact the judgment tier exists to protect.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/stakeholder-update/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. There is no gate on this output. Do not invent one, and do not report a gate as passed.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `templates/operate/metrics-review.md`
- `templates/execution/status-report.md`

## Templates the output lands in

- `templates/planning/exec-update.md`
- `templates/operate/qbr-board-update.md`

## Invariants that bind this route

- `no-fabrication`
- `human-approves-send`
- `no-blind-retry`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `an executive update`
- `a board update`
- `a narrative that lands in one read`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
