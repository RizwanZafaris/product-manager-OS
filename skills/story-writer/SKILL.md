---
name: story-writer
description: Turn a signed PRD into epics, user stories, and acceptance criteria that a tester can run and a team can slice into releases. Use when a PRD or one-pager is approved and engineering needs a backlog, when stories in the tracker have no acceptance criteria, when a release plan cannot say which slice ships first, or when a story is too big to estimate. Takes the PRD, the personas, and the FRD where one exists; returns a story map, INVEST-checked stories with IDs, and given/when/then criteria in the acceptance criteria template.
---

# Story Writer: from PRD to stories a tester can fail

The backlog that fails Gate 2 was decomposed by feature, not by user behavior: stories are screens, criteria restate the story title, and the first release is whatever got built first. This skill decomposes along the user's journey, so every story names a behavior change, every criterion can fail, and the first release is a thin working slice, not a pile of finished parts.

## Files this skill drives

- [../../templates/definition/acceptance-criteria.md](../../templates/definition/acceptance-criteria.md), where every criterion lands with a permanent ID
- [../../templates/definition/prd.md](../../templates/definition/prd.md), section 3, whose story table gets its criterion IDs here
- [../../frameworks/prioritization/user-story-map.md](../../frameworks/prioritization/user-story-map.md), the map the stories hang on
- Reads: [../../templates/definition/frd.md](../../templates/definition/frd.md) for requirement IDs, [../../templates/discovery/personas.md](../../templates/discovery/personas.md) for actors
- Method background: story mapping (Jeff Patton, 2005; book 2014), INVEST (Bill Wake, 2003), given/when/then (Dan North, behavior-driven development, 2006); story mapping is indexed in [../../knowledge/INDEX.md](../../knowledge/INDEX.md). Explained here in this repository's own words.

## When to use

- A PRD is signed and the tracker is empty, or full of tickets nobody can test
- A story has sat unestimated for two sprints because it is an epic
- A release plan lists features but cannot name the thinnest slice that works end to end
- Gate 2 returned the definition set because the criteria could not fail

## Inputs

The PRD or one-pager, with its persona links and its functional scope table. Ask for these when missing: the primary persona (a story without an actor is a feature request), the FRD requirement IDs the stories must trace to, the out-of-scope list (so the map does not grow it back), and the release constraint (a date, a pilot cohort, a dependency) that decides where the first slice line goes. If the PRD has no signed problem statement, stop; stories written against an unsigned PRD get rewritten, unbudgeted.

## Workflow

### 1. Build the backbone

Walk the primary persona's journey left to right as activities (the big things they do) and steps under each activity, in the order they happen. Use the persona's verbs, not the product's: "reconcile the month", not "open the dashboard". Every activity must trace to a PRD story or a functional scope row. An activity that traces to nothing is scope creep arriving early; it goes to the PRD's open questions, never into the tracker.

### 2. Slice stories under each step

Under each step, list the stories that make it work, best version at the top, fallbacks below. One story per behavior, as "As a [persona], I want [action], so that [outcome the persona would recognize]". The outcome clause is the test: if it restates the action ("so that I can submit"), delete the story or find the real outcome.

### 3. Check INVEST and split what fails

Score each story against INVEST: independent, negotiable, valuable, estimable, small, testable. A story that fails small or estimable splits by one of four rules, in this order of preference: by workflow step (submit now, approve later), by business rule (domestic receipts first, foreign currency second), by data variation (one file type, then the rest), by happy path and then the unhappy paths. Never split by layer: "build the API" is a task, and no user can accept it. A story that fails valuable merges into the story it serves.

### 4. Write the criteria

For every must story, at least one happy-path criterion, one edge case, and one negative case, in the acceptance criteria template's block: GIVEN one state, WHEN one action, THEN one observable outcome with its threshold. Three rules: one behavior per criterion, so an "and" in the THEN line becomes a second criterion; numbers, not adjectives, with unagreed numbers labeled ILLUSTRATIVE; IDs are permanent and only ever appended. For model-driven behavior the criterion is necessary and not sufficient: pair it with an eval set per [../../templates/ai/eval-spec.md](../../templates/ai/eval-spec.md).

### 5. Draw the release lines

Draw the first line across the map at the thinnest set of stories that lets the persona complete the whole journey, badly if necessary: the walking skeleton. Later lines add fallbacks and polish. Decision rule: a release line that does not cross every activity is a feature drop, not a release, and the line moves. Record the slice each story sits in.

### 6. Trace and hand off

Fill the PRD's story table with the criterion IDs and the coverage summary in the acceptance criteria template, then list every must story with zero negative cases by name. That list is "none" or carries an owner and a date.

## Output format

1. The story map: activities as columns, steps beneath, stories under steps, release lines drawn, in the story map worksheet
2. Story table: | ID | As a / I want / so that | Persona | Traces to (PRD story, FR) | Slice | INVEST fails and split applied |
3. Criteria blocks in the acceptance criteria template, grouped by story, each with type, threshold, test data, automatable
4. Coverage summary per story: happy, edge, and negative counts, plus gaps
5. Must stories with zero negative cases, with owner and date, or "none"

## Failure modes this skill guards against

- **Stories that are screens.** "I want a settings page" names a component, not a behavior; the outcome clause catches it.
- **Criteria that cannot fail.** "The upload works correctly" is a hope; every THEN line carries a number or a binary observable.
- **Splitting by layer.** Front-end and back-end tickets nobody can accept.
- **The happy-path spec.** Demos pass; production fails at the boundaries.
- **Release by completion order.** The first release is the walking skeleton, never whatever finished first.
- **Silent scope growth.** Map activities that trace to nothing in the PRD.

## Exit gate

The stories and criteria feed Gate 2 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md). Do not report the backlog done until every must story carries a criterion ID, every criterion can fail, the walking skeleton line is drawn, and the acceptance criteria template's exit gate is honestly checkable.
