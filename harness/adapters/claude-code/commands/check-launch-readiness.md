---
name: check-launch-readiness
description: "Router row: \"Are we ready to ship\", a go or no-go, or a Gate 5 walk. DELIVER stage, Gate 5, judgment tier. Say: are we ready to ship; a go or no-go; walk Gate 5."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: check-launch-readiness

| Field | Value |
|---|---|
| Route id | `check-launch-readiness` |
| Router row | "Are we ready to ship", a go or no-go, or a Gate 5 walk |
| Stage | DELIVER |
| Gate | 5 |
| Tier | judgment. A tier name, never a model. |
| Skill | `skills/launch-readiness/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## Note from the manifest

The harness reports which boxes pass and which do not. It never signs, and a missing piece of evidence is reported missing rather than assumed present.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/launch-readiness/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 5 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `os/STAGE-GATES.md`
- `templates/operate/operational-readiness-review.md`

## Templates the output lands in

- `templates/delivery/release-readiness.md`

## Invariants that bind this route

- `no-fabrication`
- `human-signs-gate`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `are we ready to ship`
- `a go or no-go`
- `walk Gate 5`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
