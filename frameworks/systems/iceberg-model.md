---
layer: frameworks
stage: DISCOVER
gate: 1
feeds: ["templates/discovery/problem-framing.md", "frameworks/execution/five-whys-fishbone.md", "frameworks/strategy/strategy-kernel.md"]
method: "knowledge/INDEX.md"
aliases: ["The Iceberg Model", "iceberg-model"]
---
# The Iceberg Model

Based on the four-level diagnostic set out by Michael Goodman of Innovation Associates Organizational Learning in "The Iceberg Model" (2002), whose levels are events, patterns and trends, systemic structures, and mental models. Explained here in this repository's own words.

Two things this file will not claim. The four-tier diagram is a later teaching artifact: it is not from Peter Senge's The Fifth Discipline, and it is not Donella Meadows'. The idea underneath it, that you explain behavior by structure rather than by blaming a person, is Senge's, from 1990.

## What it is for

Separating a symptom from the structure that produces it, before anyone plans a fix. This repository is otherwise all planning instruments, and a planning instrument aimed at a symptom produces a confident quarter of work on the wrong problem. The meeting it resolves is the one where a number moved the wrong way, the first explanation offered was a person or a one-off, and someone is already drafting the remediation. You run this sheet to force the same failure up four levels: what happened once, what has been happening, what arrangement makes that normal, and what belief makes the arrangement look reasonable. The output is a diagnosis with a named level, not an action list.

The separation is the whole point. A symptom is what you noticed. A structure is a policy, an incentive, a queue, a handoff, a delay, or a tool default that would produce the same symptom again next month with a different cast of people in it.

## Run it when

- A metric moved and the first explanation offered names a person, a vendor, or bad luck
- The same class of defect, escalation, or missed date has recurred after a fix shipped
- A planning cycle is about to commit a quarter to a problem statement nobody has diagnosed
- Two functions describe the same failure and their two descriptions have no overlap

**Skip it when:** the cause is single, mechanical, and undisputed. A dependency shipped late because it was never funded needs a decision, not four levels. Run this on recurrence and on confusion, not on every incident.

## Inputs you need first

- The symptom stated as an observation with a number and a date, not an interpretation, from the [problem framing](../../templates/discovery/problem-framing.md) section 1 or the [incident postmortem](../../templates/operate/incident-postmortem.md) section 1
- A time series long enough to show whether the event is a spike or a level, at least three periods
- The written rules that touch the symptom: the policy, the target, the queue limits, the tool defaults
- The people who work inside the structure, plus a facilitator who does not
- One rule agreed aloud before starting: no names in any cell, at any level

## The worksheet

### Step 1: the event, stripped of story

<!-- One row per observation. Keep interpretation out of the second column; it belongs in
     column four, where it can be examined. Column five is a gate, not a judgment: if the
     first explanation offered is a person, a one-off, or "they need reminding", the team
     is standing at level one and does not yet have a diagnosis. -->

| # | Event as observed (date, number, source) | Who noticed | First explanation offered | Does that explanation name a person or a one-off? |
|---|---|---|---|---|
| | [what happened] | [role] | [the explanation, verbatim] | [yes / no] |

### Step 2: the climb

<!-- Fill top to bottom. You may not skip a level: a structure named without a pattern
     underneath it is a hunch, and a mental model named without a structure underneath it
     is an accusation with better manners. -->

| Level | The question it answers | What you write | Evidence it needs |
|---|---|---|---|
| 1. Events | What happened, once? | [the observation from step 1] | [log, ticket, dashboard reading] |
| 2. Patterns and trends | How often, over what window, and moving which way? | [the series, with the window and the direction] | [three or more periods from one source] |
| 3. Systemic structures | What arrangement makes that pattern the normal outcome? | [the policy, incentive, queue, handoff, delay, or default] | [the written rule or the measured target, quoted] |
| 4. Mental models | What belief makes that arrangement look reasonable to the people inside it? | [one sentence someone would agree with out loud] | [a quote from someone inside the structure] |

### Step 3: structure candidates

<!-- Level 3 is where teams stall, so this is a checklist rather than a blank. Tick every
     one that is true and quote the rule. Most recurring symptoms have two or three. -->

| Candidate | Ask | Present? | The rule, quoted |
|---|---|---|---|
| Policy or rule | What are people required or forbidden to do here? | [y / n] | |
| Incentive or measured target | What is the only thing measured about this work? | [y / n] | |
| Capacity or queue | What arrives faster than it can be worked? | [y / n] | |
| Handoff or ownership | Where does the work change hands with no owner across the seam? | [y / n] | |
| Feedback delay | How long between the mistake and the person who made it learning of it? | [y / n] | |
| Tool default | What does the software do when nobody chooses? | [y / n] | |

### Step 4: the readiness score

Two coarse scales, added.

Depth reached, D, 1 to 4: 1 you have an event; 2 you have a named pattern with a series behind it; 3 you have a structure named as something changeable, with its rule quoted; 4 you have the mental model written as a sentence someone inside would say.

Evidence, C, 1 to 3: 1 asserted in the room; 2 one witness, one chart, or one document; 3 two independent sources that do not share an author.

Readiness = D + C, from 2 to 7.

| Band | Readiness | What it means | What you may do |
|---|---|---|---|
| Symptom | 2 to 3 | You have noticed something | Contain it, and keep digging. No plan, no quarter, no roadmap row |
| Pattern | 4 to 5 | You know it recurs and roughly when | Fund the investigation, and a containment with an end date |
| Structure | 6 to 7 | You can name the arrangement and quote its rule | Change the structure, and say which level you are changing |

The scales are deliberately coarse, and they add rather than multiply. The only distinctions that change what you are allowed to do next are which rung you reached and whether anybody checked, and both of those are close to binary at each step. A 1 to 10 depth score buys a twenty-minute argument about a 6 against a 7 and buys no decision. Addition is right because nothing here compounds: a deep read on no evidence and a shallow read on strong evidence are both half a diagnosis, and they should score the same.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot, eight weeks after the first wave.

Step 1. Event: on one Tuesday, a manager approved 34 copilot-drafted reports in under 6 minutes (ILLUSTRATIVE). Noticed by the finance controller. First explanation offered: "that manager rubber-stamps everything." Names a person: yes, so the team is at level one.

Step 2, the climb.

| Level | What the team wrote |
|---|---|
| Events | 34 approvals in 6 minutes by one approver, one day (ILLUSTRATIVE) |
| Patterns | Median approver review time 9 seconds; 38 percent of approvals land inside 15 seconds; flat across eight weeks and across nine approvers, so it is a level, not a spike (ILLUSTRATIVE) |
| Structures | Three, quoted below |
| Mental models | "The copilot is the control and the approval is the paperwork." Said out loud by two approvers |

Step 3, structure candidates ticked: incentive (approver turnaround time is the only approval metric on the finance dashboard); tool default (the copilot's confidence badge renders the approve button as the primary action and pre-focuses it); feedback delay (corrections route back to the filer, so an approver never sees a report they waved through come back wrong). Capacity is also true at month end, when the queue arrives in one burst.

Step 4: D = 4, C = 2 (one dashboard series plus two approver quotes, one author), so readiness 6, the structure band.

The symptom-level fix on the table that morning was approver training plus a reminder in the tool. The structural fix the sheet produced instead: route corrections to the approver who cleared the report, add a sampling target beside the turnaround target so speed stops being the only measured thing, and remove default-accept from the confidence badge. Training was kept, ranked last, and no longer described as the fix.

## Reading the result

A readiness of 2 or 3 is the common and dangerous outcome, because it feels like a finding. It is a symptom, and the honest report is "we do not have a diagnosis yet", which is a legitimate thing to take to a review. A 4 or 5 licenses containment and further work, not a quarter of build. Only 6 or 7 licenses a structural change, and the change should name the level it operates on, because a structural symptom fixed at event level returns with a new name.

Read the mental-model row for tone. If it is written as a sentence someone would actually say, it is a finding. If it reads as an insult, level 4 has been used as a place to store blame and the row should be deleted rather than argued about.

If the pattern row cannot be filled, you have one event and there may be nothing systemic here at all. Say that. A single event with a plausible one-off explanation is allowed to be a single event.

## The decision it feeds

Whether the next planning cycle commits to the symptom or to the structure. Concretely: what goes into the problem statement, and therefore what the roadmap row is allowed to say. A diagnosis in the structure band changes the target of the work, not merely its wording, and it usually moves the owner too, because the incentive or the tool default belongs to someone other than the team feeling the pain.

## Where the output lands

- [Problem framing](../../templates/discovery/problem-framing.md), section 3 (problem statement) and section 4 (evidence), which is what Gate 1 reads
- [Decision log](../../templates/execution/decision-log.md), one entry naming the level chosen and the level rejected, so a later reader can see the symptom fix was considered and declined
- [Incident postmortem](../../templates/operate/incident-postmortem.md), section 3 (contributing causes), when the run started from an incident

## Re-run trigger

Re-run when the symptom recurs after a fix has shipped, and at the start of each planning period for any problem statement carried over from the last one. Both are the same signal: a structure that was diagnosed once is being planned against as though the diagnosis is still current, and structures change shape when the org, the incentive, or the tool default changes under them.

## When this method misleads you

It produces confident nonsense in three conditions. First, when the pattern row is faked: one event plus a hunch, written up as a trend, and everything above it inherits the invention while gaining the authority of a four-level diagram. Second, when there is genuinely no system, only a person with a problem, and the climb converts a management conversation into an org-design proposal so that nobody has to have the conversation. Third, when level 4 becomes a weapon: "their mental model is that quality does not matter" is not a finding, it is a fight, and it makes the sheet unusable in that room for a year.

There is a quieter failure worth naming. This instrument is diagnostic, and a tired team that runs it well will still have four levels of writing and no plan. It is a gate, not a work item. If it does not produce a level you commit to within one session, stop, contain the symptom, and book the investigation.

## Feeds

- [Problem framing](../../templates/discovery/problem-framing.md), then [Gate 1: problem worth solving](../../os/STAGE-GATES.md)
- [Five whys and fishbone](../execution/five-whys-fishbone.md), which walks a single chain once you know the chain is worth walking
- [Strategy kernel](../strategy/strategy-kernel.md), part 1 (the diagnosis), which will not survive a symptom-level input
- [Retrospective](../../templates/execution/retrospective.md), section 4 (themes and root causes), where a recurring theme is the trigger to run this
- Method background: [knowledge index](../../knowledge/INDEX.md); [Cagan's product teams](../../knowledge/cagan-product-teams.md) for why structural causes usually sit outside the team
