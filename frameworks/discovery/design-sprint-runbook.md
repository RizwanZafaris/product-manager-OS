---
layer: frameworks
stage: DISCOVER
gate: 1
feeds: ["templates/discovery/discovery-document.md", "templates/definition/assumptions-register.md", "templates/execution/decision-log.md"]
method: "knowledge/INDEX.md"
aliases: ["Design sprint runbook", "design-sprint-runbook"]
---
# Design sprint runbook

Based on the ideas of Jake Knapp, with John Zeratsky and Braden Kowitz, from Sprint (2016), developed at Google Ventures. Explained here in this repository's own words.

## What it is for

A design sprint compresses months of debate into five working days: map the problem on Monday, sketch competing solutions on Tuesday, decide on Wednesday, build a realistic facade on Thursday, and test it with five customers on Friday. The point is not the prototype. The point is that on Friday afternoon the team has watched five real people react to a concrete thing, and the decider can choose with evidence instead of seniority. It answers one question well: before we commit a quarter to this, do customers respond to it the way we hope? This runbook lists the schedule, the roles, what must be ready before Monday, what comes out, and the cases where a sprint is the wrong tool.

## Run it when

- A problem is framed, the stakes are high, and the team is stuck between two or three directions.
- A big bet is about to enter the roadmap on the strength of a slide.
- Interviews confirmed the pain but nobody knows whether the proposed shape of the solution lands.

**Skip it when:** the risk is feasibility or scale rather than desirability. Five sessions cannot tell you whether extraction accuracy holds or whether the model cost works at volume; that is a spike or an experiment, and a sprint spent on it produces a pretty facade of an unanswered question.

## Inputs you need first

- A [problem framing](../../templates/discovery/problem-framing.md) with an evidenced problem statement.
- Evidence notes and the job map, so Monday's map starts from sessions rather than memory.
- Five Friday participants recruited against the screener and confirmed before Monday; recruiting on Thursday fails.
- A decider who will be in the room Monday and Wednesday and has the authority to kill the idea.
- Five whole days blocked per team member; a shared room; prototype tooling chosen.

## The worksheet

### 1. Roles

| Role | Who | Must attend |
|---|---|---|
| Decider | [the person whose call it is] | Monday, Wednesday, Friday afternoon |
| Facilitator | [neutral; runs the clock, not the content] | All five days |
| Interviewer | [runs Friday's five sessions] | Thursday afternoon, Friday |
| Team | [five to seven: product, design, engineering, customer-facing, finance or ops] | All five days |
| Experts | [ask-the-experts guests] | Monday afternoon only |

### 2. Schedule

| Day | Goal | Key exercises | Output |
|---|---|---|---|
| Monday | Map | Long-term goal; sprint questions; the map from actor to outcome; ask the experts; pick the target moment | The map with one target circled; two to three sprint questions |
| Tuesday | Sketch | Lightning demos from other products; four-step solo sketch (notes, ideas, variations, one solution sketch) | One anonymous solution sketch per person |
| Wednesday | Decide | Silent review; heat-map dots; speed critique; straw poll; the decider's supervote; storyboard of about fifteen panels | The storyboard |
| Thursday | Prototype | Facade only; split into maker, stitcher, writer, asset collector, interviewer; trial run at the end of the day | A prototype that survives five sessions; the interview script |
| Friday | Test | Five one-on-one sessions, team watching from another room, notes on the grid | The pattern grid; the decision |

### 3. Friday grid

<!-- One column per participant, one row per sprint question. Mark positive, negative, or
     neutral per cell with the quote that justifies it. -->

| Sprint question | P1 | P2 | P3 | P4 | P5 | Pattern |
|---|---|---|---|---|---|---|
| | | | | | | |

**Decision rule:** a sprint question is answered when four or five of the five sessions point the same way. Three against two is "unclear": iterate the prototype and test again within a week rather than arguing about it. The decider makes the call on Friday afternoon, in the room, and it goes into the decision log the same day.

## Reading the result

Three outcomes. Proceed: the target moment landed and the sprint questions came back positive; the storyboard becomes the discovery document's hypothesis and the prototype's flow seeds the PRD's user stories. Iterate: mixed results on a question that matters; keep the map, change the storyboard, and run a two-day re-test. Drop: five people flinched at the same place; count the week as the one that saved a quarter, log the assumption as busted, and return to the opportunity tree. Every result also produces new assumptions for the register, usually about trust and consent, which the sprint surfaced but could not settle.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. Long-term goal: in two years a filer never touches a receipt. Sprint questions: will filers trust the copilot to submit on their behalf; will they grant card feed and inbox access. Target moment: a charge posts on the corporate card. Prototype: a click-through in which a charge appears, the receipt is found, and the copilot proposes a submission. Friday, five frequent travelers: five of five granted card feed access; two of five granted inbox access; four of five wanted a review step before anything was submitted. The decider ruled: proceed with card feed only, add a review step, and move inbox access to the assumptions register as untested.

## The trap

The decider who delegates. They attend Monday, send a deputy on Wednesday, and on Thursday morning veto the storyboard the deputy approved; the week is lost. The second failure is the prototype that turns into a build: Thursday's facade is so convincing that someone proposes shipping it, and a two-week production effort replaces the test. A facade is disposable by design; if it cannot be thrown away on Saturday, it was not a prototype.

## Feeds

- [Discovery document](../../templates/discovery/discovery-document.md): section 4 (hypothesis) and section 7 (go or no-go)
- [Assumptions register](../../templates/definition/assumptions-register.md): the new and the busted assumptions
- [Decision log](../../templates/execution/decision-log.md): Friday's call as an entry
- [User research plan](../../templates/discovery/user-research-plan.md): section 3 (screener) for Friday's recruit
- DISCOVER, feeding [Gate 1: problem worth solving](../../os/STAGE-GATES.md)
- Method background: [knowledge index, Design Sprint entry](../../knowledge/INDEX.md); [assumption mapping](assumption-mapping.md) for what the sprint could not settle
