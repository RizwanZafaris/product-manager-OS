---
name: product-review
description: Run the weekly product review as a truth-seeking WIP walk instead of a pitch meeting. Use when a product org needs a standing review ritual, when existing reviews have decayed into status theater or demo days, or when leadership keeps discovering work at launch that they should have shaped at the idea stage. Enforces the 48-hour pre-read, the per-team 20-minute walk across pre-build, in-progress, and post-build work, and decisions that land in the decision log the same day.
---

# Product Review: the weekly WIP walk

A product review exists to change decisions while they are cheap. The version that fails is the pitch meeting: teams present finished thinking, leaders react to polish, and the only work ever inspected is the work already too expensive to stop. This skill runs the other version. The shape of the walk follows the WIP review practice taught in Reforge's product leadership material; the pre-read and truth-seeking rules restate the review discipline Shreyas Doshi has described publicly. Both are rendered here in this repository's own words.

## Files this skill drives

- [../../templates/execution/decision-log.md](../../templates/execution/decision-log.md), where every review decision lands the same day
- [../../templates/operate/metrics-review.md](../../templates/operate/metrics-review.md), the only source post-build numbers may come from
- [../../templates/execution/state.md](../../templates/execution/state.md), the status channel, so the review never becomes one

## When to use

- Standing, weekly, once the org has two or more teams shipping
- When reviews have drifted into demos, status, or theater and need a reset
- When leaders first meet work at Gate 5 and wish they had met it at the idea stage

## The three rules

1. **48-hour pre-read.** The team circulates the written material two full days ahead: the relevant discovery document, one-pager, or metrics review, not a deck built for the meeting. The review starts from questions, never from a recap. If the reviewers did not read, the item is rescheduled; the review does not degrade into a presentation to compensate.
2. **Truth-seeking, not pitching.** The team opens with the weakest part: the assumption most likely to be wrong, the number that disappointed, the thing they would kill first. Reviewers ask outcome questions and offer "how might we" alternatives; nobody wins a review, and a review nobody ever loses is a ceremony.
3. **Decisions land in writing.** Every decision, including "no decision needed", goes into the decision log the same day with the decider named. A review whose decisions live in memory made none.

## The walk

Twenty minutes per team, three buckets in this order:

- **Pre-build** (5 min): ideas and discovery work. The cheapest place to kill or redirect, so it goes first, while attention is fresh. What opportunity, what evidence, what would make you drop it?
- **In-progress** (10 min): work between Gate 2 and Gate 5. Scope drift against the signed definition, gate position, the risk that moved this week. Not a status recital; status lives in STATE.md.
- **Post-build** (5 min): shipped work against its metrics review. Did the metric move, and what does the team do about it? Numbers come from the filled metrics review, never from slides assembled for the room.

## Workflow

1. Set the roster and cadence: which teams, which reviewers, weekly slot, 20 minutes per team. Reviewers are the people who can actually redirect the work.
2. Enforce the pre-read: material out 48 hours ahead; unread items reschedule.
3. Run the walk per team, three buckets, weakest thing first.
4. Record: decisions to the decision log same day, each with decider and rationale; new risks to the [risk register](../../templates/execution/risk-register.md) with owners.
5. Follow through: open last week's decisions at the start of each review; a decision nobody executed is this week's first agenda item.

## Exit gate

The ritual is real, not ceremonial, when all three hold over a rolling month: every session produced decision-log entries or an explicit "no decision needed"; at least one pre-build item was killed or redirected (a review that cannot kill anything is a calendar invite); and the pre-read SLA held without exception. Miss any of the three, and the fix is this skill's rules, not a longer meeting.
