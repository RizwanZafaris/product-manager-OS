# JTBD job map and forces of progress

Based on the ideas of Tony Ulwick and Lance Bettencourt, from The Customer-Centered Innovation Map (Harvard Business Review, 2008), and of Bob Moesta, from Demand-Side Sales 101 (2020). Explained here in this repository's own words.

## What it is for

A job map breaks a customer's job into the eight steps every job shares, so you can see where the struggle sits instead of assuming it sits where your product happens to be. The steps are define, locate, prepare, confirm, execute, monitor, modify, and conclude; most products crowd the execute step while the customer bleeds time in locate and monitor. The four forces worksheet answers the companion question: if the job is badly served, why has nobody switched? Moesta's forces are the push of the current struggle, the pull of the new way, the anxiety about the new, and the habit of the old. Progress happens when the first pair outweighs the second. Together the two sheets decide where in the job to build and what the launch has to overcome.

## Run it when

- A job statement exists in the [JTBD spec](../../templates/discovery/jtbd-spec.md) and you need to choose which part of the job to serve first.
- Interviews keep surfacing struggle in a step your product does not touch.
- Adoption is slow although the pain is confirmed; the forces sheet locates the drag.

**Skip it when:** the job is settled and the work is a fix, a mandate, or a migration. Mapping a known job to rediscover it costs interview sessions you will want for the next open question.

## Inputs you need first

- A job statement written from the customer's life, from the JTBD spec section 1.
- Five or more interviews about a real past occurrence of the job, run under the [Mom Test guide](mom-test-interview-guide.md), with session IDs.
- Evidence notes for every quote you intend to place on the map.
- The current alternatives in use, from the JTBD spec section 2.

## The worksheet

### 1. Job statement

**Job:** [verb] + [object] + [context], for example "get reimbursed for business spend without losing money or standing". No product name, no solution.

### 2. Job map

<!-- One row per step. The struggle score is a judgment from evidence, not a vote:
     0 = no struggle observed; 1 = annoyance, no workaround; 2 = a workaround exists
     and costs time or money; 3 = the step fails or the job is abandoned. -->

| Step | What the performer does today | Where it goes wrong | Struggle (0 to 3) | Sessions citing it | Evidence IDs |
|---|---|---|---|---|---|
| Define (decide what the job requires) | | | | | |
| Locate (gather the inputs) | | | | | |
| Prepare (set up, organize) | | | | | |
| Confirm (check readiness) | | | | | |
| Execute (do the core task) | | | | | |
| Monitor (watch progress) | | | | | |
| Modify (adjust, fix) | | | | | |
| Conclude (finish, close out) | | | | | |

**Decision rule:** rank steps by struggle score times sessions citing it. The top step is the opportunity to serve first; a step with struggle 3 and one session is a lead to verify, not a result.

### 3. Four forces

<!-- Verbatim-grounded entries only. Strength: 0 = absent; 1 = mentioned; 2 = volunteered
     with a specific incident; 3 = the participant acted on it. -->

| Force | Definition | What we heard | Strength (0 to 3) | Evidence IDs |
|---|---|---|---|---|
| Push of the current struggle | What makes the present way intolerable | | | |
| Pull of the new way | What the new way promises, in their words | | | |
| Anxiety about the new | What could go wrong if they switch | | | |
| Habit of the old | What keeps the present way comfortable | | | |

**Decision rule:** switch side = push + pull; stay side = anxiety + habit. If the switch side is not larger by at least two points, adding pull will not move adoption; the work is reducing anxiety or breaking habit.

## Reading the result

A lopsided map is a good map; eight steps with the same struggle score mean the evidence was averaged in a conference room. The top step names the first release scope and the metric that proves it (time spent in that step, failures at that step). The forces tell you what the launch must do. Push-heavy with weak pull: the pain is real and your promise is unclear; fix positioning. Pull-heavy with no push evidence: a solution looking for a problem; go back to interviews. Anxiety high: trust features, reversibility, a review step. Habit high: migration, defaults, and a first run that lives inside the old tool.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. Job: get reimbursed for business spend without losing money or standing. Eight interviews. Locate scored 3 (receipts lost between the trip and the report; cited in seven sessions). Prepare scored 2 (categorizing lines against a policy PDF; six sessions). Monitor scored 2 (no way to see approval status; five sessions). Execute scored 0: submitting the form was never the problem, which is where the previous tool spent its budget. Forces: push 3 (a quarter-end Sunday and a rejected report repaid out of pocket), pull 2 (charge appears, receipt attached, one tap), anxiety 3 (the copilot files a personal charge as business and the filer is the one audited), habit 1 (a phone folder of receipt photos). Switch side 5, stay side 4: not enough. Decision: build for locate first, and make the review step and the undo path the launch story, not the automation.

## The trap

The map that starts at "open the app". A team maps its own workflow, labels the steps define through conclude, and produces a feature list wearing Ulwick's headings. The job begins when the spend happens and ends when the money is back and the record is filed; most of it happens nowhere near your product. The second failure lives in the forces: anxieties get written by the team, in the team's words, because participants rarely volunteer them. Ask for the last time they almost switched tools and did not, and write down why.

## Feeds

- [JTBD spec](../../templates/discovery/jtbd-spec.md): section 1 (job statement) and section 3 (forces on the switch)
- [Journey map](../../templates/discovery/journey-map.md): section 1 (current journey), one column per step
- [Opportunity solution tree](../../templates/discovery/opportunity-solution-tree.md): section 2 (opportunity branches) from the top-scoring steps
- [Opportunity scoring](opportunity-scoring.md): the outcomes inside each step, scored across respondents
- DISCOVER, feeding [Gate 1: problem worth solving](../../os/STAGE-GATES.md)
- Worked fill: [Ledgerline job map example](../../examples/ledgerline-jtbd-job-map.md)
- Method background: [jobs to be done](../../knowledge/jobs-to-be-done.md)
