---
name: facilitate-postmortem
description: "Router row: An incident to review, a blameless postmortem, or a root cause to find. OPERATE stage, Gate 6, judgment tier. Say: review this incident; run a blameless postmortem; find the root cause."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: facilitate-postmortem

| Field | Value |
|---|---|
| Route id | `facilitate-postmortem` |
| Router row | An incident to review, a blameless postmortem, or a root cause to find |
| Stage | OPERATE |
| Gate | 6 |
| Tier | judgment. A tier name, never a model. |
| Skill | `skills/postmortem-facilitator/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

Blameless means the record names systems and decisions, not people to blame. Customer data pulled in to reconstruct a timeline is minimized, never bulk ingested.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/postmortem-facilitator/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 6 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `templates/execution/decision-log.md`
- `templates/delivery/failure-scenarios.md`

## Templates the output lands in

- `templates/operate/incident-postmortem.md`
- `frameworks/execution/five-whys-fishbone.md`

## Invariants that bind this route

- `no-fabrication`
- `least-data`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `review this incident`
- `run a blameless postmortem`
- `find the root cause`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
