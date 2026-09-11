---
layer: frameworks
stage: DESIGN
gate: 3
feeds: ["templates/architecture/design-review-record.md", "templates/discovery/usability-test-plan.md", "templates/execution/risk-register.md"]
method: "knowledge/design/usability-heuristics.md"
aliases: ["Heuristic Evaluation", "heuristic-evaluation", "Cognitive Walkthrough"]
---
# Heuristic Evaluation

Based on the ideas of Jakob Nielsen and Rolf Molich, from "Heuristic evaluation of user interfaces", ACM CHI 1990, and of Jakob Nielsen's 1994 revision of the ten heuristics. The worksheet's own procedure, panel size, independent passes with no peeking, and consolidate-then-rate scoring, follows [How to Conduct a Heuristic Evaluation](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/), Kate Moran and Kelley Gordon, Nielsen Norman Group, 2023, all rights reserved, cite-only per [docs/REFERENCES-DESIGN.md](../../docs/REFERENCES-DESIGN.md). Explained here in this repository's own words.

## What it is for

A small panel of evaluators walks a flow, screen by screen, against a fixed list of general principles and writes down where the design breaks each one, with no participant recruited and no session scheduled. This worksheet runs that panel: it scores each finding independently, consolidates the panel's findings by arithmetic rather than by argument, and offers a second, task-based mode (the cognitive walkthrough) for the narrower question of whether one specific user could complete one specific task. Both modes produce a findings list scored on the same 1 to 4 severity scale as [Usability Test Plan](../../templates/discovery/usability-test-plan.md) section 6, so a heuristic finding and a moderated-test finding can sit in the same risk conversation without a unit conversion.

## Run it when

- A clickable prototype or a shipped screen exists and needs a first, cheap filter before a moderated usability round is booked
- A design review at Gate 3 needs a structured pass with a shared vocabulary, not a pile of individual taste opinions
- A flow was just fixed after a usability finding and the team wants a quick recheck before committing a second moderated round to the same screen
- The task is well defined and the audience is a first-time or occasional user: run the cognitive walkthrough variant in section 5 instead of, or alongside, the general pass

**Skip it when:** nothing concrete exists yet to inspect: no static mock, no clickable prototype, no shipped screen. The task-based variant in section 5 additionally needs a walkable flow, since its four questions test whether one step leads correctly into the next; a single static screen supports the general pass in sections 1 to 4 (consistency, match with the real world, error-message wording and the rest of Nielsen's and Shneiderman's lists all apply to one screen on its own) but not the walkthrough. Skip it too when the team will not change the design this cycle: a findings list nobody will act on is a violation count for its own sake. Skip the task-based variant for expert users on a familiar flow, since the walkthrough's questions (would a new user guess this, notice this, connect it to the goal) are built around a first encounter and score an expert's fluency as failure.

## Inputs you need first

- The scope: which screens, and which tasks the evaluation will walk. This worksheet's convention is 3 to 5 tasks (evidence class: this repository's convention; NN/g recommends a narrow scope but does not fix a number)
- 3 to 5 evaluators who can work independently, with no peeking at another's notes until each finishes their own pass (evidence class: research evidence, Nielsen and Molich 1990, plus NN/g practice, Moran and Gordon 2023)
- Access to the same build or prototype for every evaluator, so a difference in findings reflects the evaluator, not a difference in what they saw
- For the task-based variant: one named user profile (first-time or occasional) and the correct action sequence for the task, written down before anyone walks it

## The worksheet

### 1. Scope

<!-- Name the screens and the 3 to 5 tasks before evaluators start. A scope
     agreed after the fact tends to expand to cover whatever was found. -->

**Product or flow:** `<name>` · **Screens in scope:** `<list>` · **Build or prototype link:** `<url>`

| Task | Screens it touches | In scope |
|---|---|---|
| T1 | | |

### 2. Evaluators

<!-- 3 to 5 evaluators, working independently (after Moran and Gordon, 2023).
     No evaluator sees another's findings until every evaluator has
     submitted their own pass; a shared screen or a live discussion during
     the walk collapses independent judgments into one, which is the exact
     effect the arithmetic in section 4 depends on not happening. -->

| Evaluator | Role or background | Pass completed (date) |
|---|---|---|
| E1 | | |

### 3. Findings grid

<!-- One row per evaluator per finding. "Element" names the specific control
     or region the finding is about, checkable, and is part of the dedupe
     key section 4 applies. "Heuristic" is the Nielsen or Shneiderman name
     from knowledge/design/usability-heuristics.md; "ISO principle" is the
     nearest name from that card's crosswalk table, listed for vocabulary
     only, never as a compliance claim. Severity uses the SAME 1 to 4 scale
     as templates/discovery/usability-test-plan.md section 6 (4 blocker, 3
     major, 2 minor, 1 cosmetic): never NN/g's own severity wording, so a
     finding here and a moderated-test finding compare directly. Evidence is
     a screenshot id or a numbered step, checkable by someone who was not in
     the room. -->

| Evaluator | Screen | Element | Heuristic (name) | ISO 9241-110 principle | What happened | Evidence (screenshot id or step) | Severity (1 to 4) |
|---|---|---|---|---|---|---|---|
| E1 | | | | | | | |

### 4. Consolidation arithmetic

<!-- Consolidate after every evaluator has submitted independently. -->

**Dedupe rule:** two rows describe the same finding only when all three match: same screen, same element, same violated expectation. A finding two evaluators phrased differently but pointed at the same control, over the same violated expectation, counts once, consolidated; a finding one evaluator alone caught stays a row of its own.

**Consolidated severity:** the median of the independent severities given by every evaluator who found it. An even count of evaluators (a 4-evaluator panel finding a 2-2 split) takes the higher of the two middle values, since the worksheet's purpose is to surface risk, not average it away.

**Count found:** the number of evaluators, out of the panel, who independently reported the finding. A count of 1 does not by itself mean the finding is weak, nor that it is confirmed; it means only one evaluator's independent judgment supports it so far. See [Reading the result](#reading-the-result) below for how count feeds routing.

| Finding | Screen | Element | Consolidated severity | Count found (of N evaluators) |
|---|---|---|---|---|
| F1 | | | | |

### 5. Task-based variant: cognitive walkthrough

<!-- Run this instead of, or alongside, sections 1 to 4 when the question is
     narrower: not "does this screen honor general principles" but "would
     this one user complete this one task." The method originates with
     Lewis, Polson, Wharton and Rieman (1990), cited by title and year, not
     fetched, no DOI on file. The four-question form used below is the
     later practitioner's version of that method, Wharton, Rieman, Lewis and
     Polson (1994), cited by title and year only, not fetched, no DOI on
     file, pending its own row in docs/REFERENCES-DESIGN.md: do not cite it
     as the 1990 original. Skip this variant for expert users on a familiar
     flow (see "Skip it when" above): its four questions are built around a
     first encounter. -->

**User profile:** `<first-time or occasional user, named by role, e.g. "a filer submitting their first expense report">`
**Task:** `<one task>` · **Correct action sequence:** `<numbered steps an expert would take>`

For each step, ask all four questions and map each to the gulf it tests, after Norman's gulfs of execution and evaluation ([Interaction Design Principles](../../knowledge/design/interaction-design-principles.md)):

| Step | Would they try to achieve the right effect (gulf of execution: intent to action)? | Would they notice the correct action is available (gulf of execution: action to interface)? | Would they connect the action to their goal (gulf of execution: mapping the action to the goal)? | Would the feedback show progress toward the goal (gulf of evaluation)? | Success or failure story | Severity (1 to 4) |
|---|---|---|---|---|---|---|
| S1 | | | | | | |

**Arithmetic:** failure stories per step (count of "no" answers across the four questions, per step), and the share of steps in the task with at least one failure story (steps with a failure divided by total steps). A task with failures concentrated in one step names a specific redesign target; a task with one failure scattered across every step names a pattern worth checking against gulf of execution: action to interface, meaning the next control may not be visible, rather than five separate problems.

### 6. Coverage caveat

<!-- Write this into the findings summary every time, not only when asked.
     One evaluator, or one AI pass, is one evaluator; see
     knowledge/design/usability-heuristics.md "The trap" for the full
     argument this caveat compresses. -->

In Nielsen and Molich's four 1990 experiments, single evaluators working alone caught only 20 to 51 percent of the usability problems actually present in the interfaces they reviewed (evidence class: research evidence). This applies to the cognitive walkthrough as much as to the general pass: the evaluator effect, average agreement between any two evaluators looking at the same system ranged from 5 to 65 percent across heuristic evaluation, cognitive walkthrough and think-aloud testing alike (Hertzum and Jacobsen, 2001; evidence class: research evidence), is a property of usability evaluation methods generally, not of inspection alone and not of any one list. An AI pass, run once against a screenshot or a prototype, is one evaluator's judgment running faster than a person's; pool it with the panel's other independent passes in section 3 or 4, never report it as coverage equal to a 3 to 5 person panel.

## Reading the result

Every consolidated severity 3 or 4 finding goes to the next moderated usability round, scoped by the [usability test plan](../../templates/discovery/usability-test-plan.md). Inspection alone never closes a severity 3 or 4 finding, and it is never marked "fixed" on the strength of this worksheet's pass by itself: [Design Review Record](../../templates/architecture/design-review-record.md) section 3 holds a severity 3 or 4, inspection-class row "open, routed to usability test" until a user session confirms the fix or the problem's absence, and this worksheet uses the same rule. It may also get a [risk register](../../templates/execution/risk-register.md) row with a named owner in parallel: the register tracks and assigns the risk while the test is pending, and does not substitute for the test. A finding with count 1, whatever its severity, gets the same routing: one evaluator caught it, and section 6's evidence cuts both ways, since a single evaluator catches only a minority of what is actually present. A count of 1 may mean a real problem the rest of the panel missed, or it may mean nobody else could confirm it; that unresolved uncertainty, not a presumption in either direction, is why it goes to a usability round rather than being called fixed or dismissed. Severity 1 and 2 findings with count 2 or higher across the panel are strong enough to fix directly, no test needed. Everything section 3, 4 or 5 produces, whatever its severity, writes into the [Design Review Record](../../templates/architecture/design-review-record.md) as the screen-level evidence a Gate 3 review brings forward.

## ILLUSTRATIVE example

Invented, a loan-application status screen for a consumer lending product. Scope: the "application status" screen, task "check whether my application needs anything from me." Panel of 4 evaluators.

| Finding | Screen | Element | Consolidated severity | Count found (of 4) |
|---|---|---|---|---|
| F1: status label "Pending Review" gives no next action | Status screen | Status banner | 3 | 4 |
| F2: "Upload" button style matches disabled buttons elsewhere in the product | Status screen | Upload CTA | 3 | 1 |
| F3: page title differs from the label used in the email that linked here | Status screen | Page title | 2 | 2 |

F1, found by every evaluator at severity 3, gets a risk register row with an owner and a fix date, and a probe scoped into the next moderated usability round: consolidated severity 3 closes only on a user session, whatever the count. F2 is severity 3 and count 1: per the reading-the-result rule above, it goes into the same usability round's scope and stays open until tested: one evaluator caught it, and the evidence does not say whether that means the other three missed something real or that nobody else could confirm it. F3 is minor and corroborated twice: fixed directly.

## The trap

An expert review recorded as user evidence at Gate 3 or 4. A heuristic pass, however well run, is trained judgment applied by people who already know how the product is supposed to work; it substitutes for a data-gathering method, it does not become one by being written up carefully. The tell is a Design Review Record or a Gate 4 readiness note that cites this worksheet's findings as if they showed real users succeeding at real tasks. They show where a screen predictably breaks a general principle, nothing about whether the specific people who will use this specific product can get their specific job done. That claim needs the [usability test plan](../../templates/discovery/usability-test-plan.md), run with real participants, cited by name.

## Feeds

- [Design Review Record](../../templates/architecture/design-review-record.md): every consolidated finding from section 4, and every failure story from section 5, is the screen-level evidence the record carries to Gate 3
- [Usability Test Plan](../../templates/discovery/usability-test-plan.md): every consolidated severity 3 or 4 finding, whatever its count, scopes what the next moderated round needs to probe; the plan's own section 6 severity scale is the scale this worksheet reuses
- [Risk register](../../templates/execution/risk-register.md): every consolidated severity 3 or 4 finding gets a named owner directly, tracked there while the usability round it was routed to is still pending
- DESIGN stage, feeding [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md)
- Method background: [Usability Heuristics](../../knowledge/design/usability-heuristics.md)
