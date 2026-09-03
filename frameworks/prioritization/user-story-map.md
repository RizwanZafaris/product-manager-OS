---
layer: frameworks
stage: DEFINE
gate: 2
feeds: ["templates/definition/acceptance-criteria.md", "templates/definition/prd.md", "templates/planning/roadmap.md"]
method: "knowledge/INDEX.md"
aliases: ["User story map", "user-story-map"]
---
# User story map

Based on the ideas of Jeff Patton, from his story mapping practice (2005) and the book User Story Mapping (2014). Explained here in this repository's own words.

## What it is for

A flat backlog sorted by priority has a defect: the top ten items rarely form something a user can use end to end. A story map fixes that by laying stories out in two dimensions. Left to right is the user's journey, the backbone of activities and the steps inside each; top to bottom under each step is necessity, the most essential story first. A release is then a horizontal slice across every step, and the thinnest slice that works from the first step to the last is the walking skeleton. The map answers "what is the smallest thing that works end to end," which is the question a first release has to answer and a backlog cannot.

## Run it when

- Turning a PRD or one-pager into stories, before anyone writes acceptance criteria.
- Planning a first release and the team cannot say which stories must ship together.
- A backlog has grown to the point that nobody can see the journey in it.

**Skip it when:** there is no journey. A platform migration, a machine-facing API, or a single-screen change has a backbone of one card; a mapping workshop on it costs a day and produces a list with a heading.

## Inputs you need first

- The user's journey, current and future, from the [journey map](../../templates/discovery/journey-map.md).
- The actors, from the [personas](../../templates/discovery/personas.md).
- Functional scope, from the [PRD](../../templates/definition/prd.md) section 4 or the [one-pager](../../templates/definition/one-pager.md) section 3.
- The outcome the first release must produce: the Gate 1 success signal from the [discovery document](../../templates/discovery/discovery-document.md).
- Capacity per release.

## The worksheet

### Step 1: the backbone

Activities are the big things the user does, in the order they happen; steps are what they do inside each. Write them as verbs from the user's side, not the system's.

| Activity (left to right) | Actor | Steps, in order |
|---|---|---|
| [activity] | [actor] | [step 1; step 2; step 3] |

### Step 2: the map

Columns are steps; rows are slices. Slice 1 is the walking skeleton: one story per step, however narrow (one case, one currency, a manual process behind the screen). No column in slice 1 may be empty; an empty column means the skeleton does not walk.

| Slice | Step: [name] | Step: [name] | Step: [name] | Step: [name] |
|---|---|---|---|---|
| 1, walking skeleton | [story] | [story] | [story] | [story] |
| 2 | [story] | [story] | | [story] |
| 3 | | [story] | [story] | |
| Parking lot (no step) | [idea that sits under no step; it is not on the map] | | | |

Within a column, stories are ordered by necessity from the top, not by how much anyone wants them.

### Step 3: the release line

| Release | Slices included | Outcome it must produce | Test that it walked | Capacity used |
|---|---|---|---|---|
| 1 | [1, plus what the outcome needs] | [signal from the discovery document] | [one user completes the journey end to end, observed] | [n of capacity] |
| 2 | [2] | | | |

### Story cards

| ID | Story (as a [actor], I need [step] so that [outcome]) | Step | Slice | Acceptance criteria ref | Size |
|---|---|---|---|---|---|
| US-1 | [story] | [step] | [1] | [AC-n] | [S / M / L] |

## Reading the result

If the walking skeleton does not fit in the first release, narrow the journey rather than thinning the steps: one actor, one receipt type, one currency, and still every step. A column with ten stories beside columns with one shows where the complexity, or the fear, lives; ask which it is. Every release names the outcome it produces and the observation that proves the journey walked. Ideas in the parking lot are not on the map, and the map is what gets built.

## ILLUSTRATIVE example

Ledgerline's expense-report copilot, the filer's journey, everything invented.

Backbone: capture receipt, draft report, review draft, submit, reviewer approves, reimbursed. The last step already exists and stays untouched.

| Slice | Capture | Draft | Review | Submit | Approve |
|---|---|---|---|---|---|
| 1, skeleton | Photograph one printed receipt | Extract merchant, date, amount, one currency | Filer edits any field before continuing | Hand to the existing submit flow | Reviewer sees a "drafted by copilot" flag |
| 2 | Multiple receipts per report | Foreign currency; category suggestion with the policy line | Show which fields the filer changed | | Reviewer sees the audit trail of drafted versus edited fields |
| 3 | Mileage from calendar entries | | | | Bulk approve for drafted reports |
| Parking lot | Filing on behalf of another employee | | | | |

Release 1 is slice 1 plus the audit trail from slice 2, because the contract with finance's audit firm requires it. Outcome: first-submission approval rate on copilot-drafted reports. Test: five filers complete a real report end to end in the pilot week. Capacity: 17 of 30 person-weeks.

## The trap

Building down the most interesting column. Capture is where the model lives, so the team builds all six capture stories first: multiple receipts, crumpled receipts, foreign currency, mileage. At the release date, capture is superb and nothing can be submitted, because the review and submit columns never got their one story each. The map made the skeleton visible; the sprint plan ignored it. The rule that protects against this is mechanical: no story from slice 2 starts until every column in slice 1 is done and the journey has been walked once.

## Feeds

- [Acceptance criteria](../../templates/definition/acceptance-criteria.md): one AC set per story card, feeding [Gate 2: requirements signed off](../../os/STAGE-GATES.md)
- [PRD](../../templates/definition/prd.md) section 3 users and stories, and section 4 functional scope, where the release line becomes the scope statement
- [Story writer](../../skills/story-writer/SKILL.md), the skill that drives this map from a PRD
- [Roadmap](../../templates/planning/roadmap.md): each release is a Now or Next row
- Method background: the user story mapping entry in the [knowledge index](../../knowledge/INDEX.md)
