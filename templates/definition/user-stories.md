---
layer: templates
stage: DEFINE
gate: 2
feeds: []
method: "knowledge/INDEX.md"
aliases: ["User Stories", "user-stories", "story register", "backlog stories"]
---
# User Stories: [feature or product name]

Stage: DEFINE, feeds Gate 2 (requirements signed off), worked continuously through BUILD
Knowledge: [Knowledge index](../../knowledge/INDEX.md)
Skill: [story-writer](../../skills/story-writer/SKILL.md)

<!-- What this file is for, and why it exists separately from the PRD.

     The PRD's section 3 holds a story table because a reader of the PRD needs
     to see, in one glance, who the product is for and what they will be able
     to do. That table is a summary. It is not where stories are worked.

     Stories are the highest-frequency artifact a product manager touches:
     they change during refinement, they split when they turn out to be too
     big, they get re-pointed, and they carry the acceptance criteria a tester
     runs. Doing that inside a PRD section means editing a signed document
     every sprint, which is how a signed document stops meaning anything.

     So: US ids are DEFINED here and QUOTED everywhere else. The PRD's table,
     acceptance-criteria.md, frd.md's traceability matrix, the test plan and
     the release readiness pack all cite ids from this file. Once an id is
     circulated it is never renumbered and never reused, including for a story
     that was killed. A dead id with a line saying why is cheap; a recycled id
     is a defect somebody finds in production. -->

**Feature:** [name] · **PRD:** [prd.md](prd.md) · **Owner:** [name]
**Personas:** [personas.md](../discovery/personas.md) · **Last refined:** [YYYY-MM-DD]

## 1. The slice this release ships

<!-- Fill this before writing a single story. A story list with no slice is a
     pile of parts, and the team will build them in the order they were
     written, which is never the order that produces something usable.

     A slice is thin and vertical: it crosses every layer and leaves a user
     able to do something end to end. "The database work" is not a slice.
     "Priya can photograph a receipt and see the amount filled in, for one
     currency, on one platform" is a slice.

     The map this hangs on is frameworks/prioritization/user-story-map.md. If
     you have not built one, build it first: the map is what tells you which
     stories are the walking skeleton and which are refinements of it. -->

**Walking skeleton (the thinnest end-to-end path):** [one sentence, the whole journey at its most primitive]

| Release | What a user can do afterwards that they could not before | Stories included |
|---|---|---|
| R1 | | |
| R2 | | |
| Later | | |

## 2. Epics

<!-- An epic is a container, not a big story. It exists so the register stays
     readable, and it is deleted when its last story ships. If an epic has one
     story it was not an epic; if it has thirty it is a project and needs a
     PRD of its own. -->

| Epic | Objective it serves (from prd.md section 2) | Stories | Status |
|---|---|---|---|
| E1 | | US1, US2 | |

## 3. The story register

<!-- The canonical definition of every story id. One row per story, and the
     row is the story: if the text lives in a tracker and this file holds a
     link, the two will disagree within a month and the tracker will win
     silently.

     Priority uses MoSCoW and matches prd.md section 3 exactly. A must with no
     acceptance criteria id cannot pass Gate 2, because a must without
     testable acceptance is a hope with a deadline.

     Estimate is whatever unit the team actually uses. Leave it blank rather
     than guessing: an invented number is worse than an absent one, because
     somebody will plan against it. -->

| ID | Story | Persona | Priority | Acceptance criteria | Estimate | Status | Notes |
|---|---|---|---|---|---|---|---|
| US1 | As a [persona], I want [action], so that [outcome]. | | must | AC-[n] | | | |
| US2 | | | should | | | | |

**Killed or superseded stories.** Never delete a row; move it here so the id stays spent.

| ID | Story | Why it is dead | Superseded by |
|---|---|---|---|
| | | | |

## 4. INVEST check

<!-- Bill Wake's INVEST, 2003: Independent, Negotiable, Valuable, Estimable,
     Small, Testable. Six letters, and there is no seventh, which matters
     because the checklist is often quoted with invented ones.

     Run this on every must before Gate 2. The check is not a formality: each
     letter catches a specific and common way a story fails, and the failures
     below are the ones that actually appear in real backlogs rather than the
     tidy ones in the textbook. Record the verdict; a check nobody wrote down
     did not happen. -->

| Letter | It fails when | The question to ask |
|---|---|---|
| **I**ndependent | It cannot ship unless another story ships first, and the order was not designed | What breaks if this ships alone? |
| **N**egotiable | It dictates the implementation, so there is nothing left to discuss with the team | Does this name a technology or a screen instead of a behaviour? |
| **V**aluable | Nobody outside the team is better off when it ships | Who can do something new, and what? |
| **E**stimable | The team cannot size it because something is unknown | What do we not know, and can we spike it instead? |
| **S**mall | It cannot finish inside one iteration | Which of the splitting patterns in section 5 applies? |
| **T**estable | No criterion could fail | Write the criterion that fails. If you cannot, the story is a wish |

## 5. Splitting a story that is too big

<!-- The patterns below are the ones that produce vertical slices. Splitting
     by layer, "the API story" and "the UI story", is the most common split
     and the wrong one: neither half is shippable, neither changes anything
     for a user, and the team discovers the integration cost after both are
     called done.

     Split, then re-run INVEST on each half. A split that produces two stories
     that both still fail S was a rename. -->

| Pattern | Split it by | Use it when |
|---|---|---|
| Workflow step | The steps of the user's journey | The story spans a whole journey |
| Happy path first | The path where nothing goes wrong, then each failure | Error handling is most of the size |
| Business rule variation | One rule now, the variants later | Rules differ by market, plan or tier |
| Effort | The cheap majority of cases, then the expensive tail | A small share of cases carries most of the cost |
| Data variation | One data type, format or currency, then the rest | The work scales with the number of input shapes |
| Interface | One platform or surface first | The behaviour is the same across several surfaces |

### Worked micro-example (ILLUSTRATIVE, invented)

<!-- Kept deliberately: it shows the shape of a real split and the shape of
     four real INVEST failures. Delete it when the register has real rows. -->

**Feature:** receipt auto-extraction. **Persona:** Priya, a field sales rep filing expenses from her phone between client visits.

**Too big:** *As Priya, I want the app to scan my receipt, extract every field, handle every error, sync to accounting and submit the expense, so that I never touch the form again.*

Split into three slices, each shippable alone:

| Slice | Story | Pattern |
|---|---|---|
| US1 | As Priya, I want to photograph a receipt, so that I start an expense without typing the amount | Workflow step |
| US2 | As Priya, I want merchant, date and total filled in from the photo, so that I submit a clean expense in one pass | Happy path first |
| US3 | As Priya, I want a low-confidence extraction flagged for review, so that I do not file a wrong expense | Business rule variation |

Four stories that fail INVEST, and why:

| Story as written | Fails | Why | The fix |
|---|---|---|---|
| As Priya, I want the scanner screen with capture, preview, crop and confirm | **V** | It is a screen. Nothing Priya can do changes until a field is extracted | State the outcome: the form fills itself from the photo |
| As Priya, I want the extraction to use a specific OCR library with custom preprocessing | **N** | It dictates the implementation, leaving the team nothing to negotiate, and names no user value | Restate as behaviour: a crumpled or dim photo still extracts, so she does not retype |
| As Priya, I want full extraction across all clients, currencies and languages | **S**, **E** | Too big to finish in an iteration and carries several unknowns at once | Use the split above, then re-run this check on each slice |
| As Priya, I want extraction to always be correct | **T** | No criterion could fail, so nothing can be accepted or rejected | Give it a boundary: named fields extracted on a labelled sample, or flagged for manual entry |

## 6. Traceability

<!-- Filled at Gate 2 and kept current through BUILD. This is the section that
     makes the stack real: a criterion that cannot name its story, or a
     requirement that no story delivers, is where scope quietly enters or
     quietly disappears. Both directions are checked, because only one of them
     is usually noticed. -->

| Story | Serves objective | Detailed by (FRD requirement) | Verified by (AC) | Covered by test |
|---|---|---|---|---|
| US1 | O[n] in [prd.md](prd.md) | FR-[nnn] in [frd.md](frd.md) | AC-[n] in [acceptance-criteria.md](acceptance-criteria.md) | |

**Orphan check.** Run both directions and record the answer, not the intention.

- Stories serving no objective: [list, or "none"]
- Objectives with no story: [list, or "none"]
- FRD requirements no story delivers: [list, or "none"]
- Must-priority stories with no acceptance criteria: [list, or "none"]

## 7. Open questions

<!-- An open question with no owner and no needed-by date is not open, it is
     abandoned. Cap this table: if it passes about ten rows the feature is not
     ready to be sliced and the honest move is to go back to discovery. -->

| # | Question | Blocks which stories | Owner | Needed by |
|---|---|---|---|---|
| | | | | |

## Exit gate (feeds Gate 2: requirements signed off)

<!-- Every box here is checkable by a person who did not write the stories,
     which is the test of whether a gate is a gate. "INVEST has been run" is
     checkable because section 4 asks for recorded verdicts; "the stories are
     good" would not be, and is deliberately absent. -->

- [ ] Every must-priority story has an acceptance criteria id that could fail
- [ ] Every story names a persona that exists in [personas.md](../discovery/personas.md)
- [ ] Every story states an outcome, not a screen and not a technology
- [ ] INVEST has been run on every must, and the verdicts are recorded rather than assumed
- [ ] No story in this release is too big to finish in one iteration, or it has been split and both halves re-checked
- [ ] The walking skeleton is named and R1 delivers it end to end
- [ ] Traceability is filled in both directions, and every orphan list says "none" or names an owner
- [ ] Killed stories are in the dead table with their ids spent, not deleted
- [ ] The worked example above has been removed
