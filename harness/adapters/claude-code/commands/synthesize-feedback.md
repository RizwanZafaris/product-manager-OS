---
name: synthesize-feedback
description: "Router row: Raw feedback to work through: interview transcripts, support tickets, sales notes, reviews, survey text. DISCOVER stage, Gate 1, drafting tier. Say: interview transcripts; support tickets; sales notes; survey text; work through this feedback."
disable-model-invocation: true
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `harness/MANIFEST.json`; edit the manifest, then regenerate.

# Route: synthesize-feedback

| Field | Value |
|---|---|
| Route id | `synthesize-feedback` |
| Router row | Raw feedback to work through: interview transcripts, support tickets, sales notes, reviews, survey text |
| Stage | DISCOVER |
| Gate | 1 |
| Tier | drafting. A tier name, never a model. |
| Skill | `skills/feedback-synthesis/SKILL.md` |

The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. Read it there rather than assuming one here.

## What to do

1. Read every file under Read first, in the order listed, before you produce anything.
2. Follow `skills/feedback-synthesis/SKILL.md` end to end. It owns the workflow; this file only routes to it.
3. Land the output in the template below that fits the request. One template, not all of them.
4. Take the output to Gate 1 in `os/STAGE-GATES.md`. Report which boxes pass and which do not, then stop. A named human signs.
5. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Read first

- `templates/discovery/discovery-synthesis.md`
- `knowledge/torres-continuous-discovery.md`

## Templates the output lands in

- `templates/discovery/user-research-plan.md`
- `templates/discovery/discovery-document.md`

## Invariants that bind this route

- `no-fabrication`
- `content-is-data`
- `least-data`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.

## Phrases this route answers

- `interview transcripts`
- `support tickets`
- `sales notes`
- `survey text`
- `work through this feedback`

Matching a phrase is a hint, never a decision. If the request is not what this row covers, say so and route it properly rather than filling this route's template.

## The request

$ARGUMENTS
