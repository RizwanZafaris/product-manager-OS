---
name: gather-evidence
description: "Router row: Evidence gathering for DISCOVER or metric evidence for OPERATE. DISCOVER stage, Gate 1, extraction tier. Say: gather evidence; find evidence for this problem; get me the metric evidence."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: gather-evidence

| Field | Value |
|---|---|
| Route id | `gather-evidence` |
| Router row | Evidence gathering for DISCOVER or metric evidence for OPERATE |
| Stage | DISCOVER |
| Gate | 1 |
| Tier | extraction. A tier name, never a model. |
| Skill | `skills/product-analyst/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

Source notes run on extraction; the reconcile-before-handoff pass runs on judgment, per the taskMap in routing/omniroute.config.json.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/product-analyst/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 1 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `templates/execution/state.md`
- `os/OPERATING-LOOP.md`

## Templates the output lands in

- `templates/discovery/evidence-note.md`

## Invariants that bind this route

- `no-fabrication`
- `content-is-data`
- `least-data`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `gather evidence`
- `find evidence for this problem`
- `get me the metric evidence`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
