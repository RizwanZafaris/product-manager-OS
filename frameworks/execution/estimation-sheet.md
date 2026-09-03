---
layer: frameworks
stage: PLANNING
gate: 2
feeds: ["templates/planning/capacity-plan.md", "templates/planning/roadmap.md", "frameworks/prioritization/rice-scoring-sheet.md"]
method: "knowledge/shape-up.md"
aliases: ["Estimation Sheet", "estimation-sheet"]
---
# Estimation Sheet

Based on the ideas of several sources: three-point estimates from the PERT method of the US Navy Special Projects Office (1958), story points from Mike Cohn's Agile Estimating and Planning (2005), and reference-class forecasting from Bent Flyvbjerg (2006), building on the outside view of Daniel Kahneman and Amos Tversky (1979). Explained here in this repository's own words.

## What it is for

An estimate that leaves this sheet is a range with a stated confidence, never a single number. Four methods run in sequence, each catching what the last one missed: t-shirt sizes for triage, story points for relative size within one team, three-point estimates for a calendar answer with a spread, and a reference class for the reality check from the outside. The decision it improves is what to commit, to whom, with how much buffer, and the sheet's last line is written so a stakeholder cannot quote the low end alone.

## Run it when

- A roadmap row is about to move from Next to Now
- The capacity plan needs demand in weeks per team
- Someone asks for a date, and "it depends" is true but unhelpful
- Scoring the effort column of a RICE sheet

**Skip it when:** the work is under a week for one person, or the appetite is fixed. In a fixed-appetite bet the question is what fits in six weeks, not how long the scope takes; scope to the appetite and skip the sheet.

## Inputs you need first

- The scope, from PRD section 4 or the story map slices
- The team's velocity for the last six sprints, measured, not remembered
- A reference class: past projects of the same kind with their original estimate and actual duration
- The [dependency register](../../templates/execution/dependency-register.md), for waits that are not work

## The worksheet

### Step 1: t-shirt size for triage

XS under a week, no further estimation. S, one to two weeks: story points. M, three to six weeks: story points plus three-point. L, seven to twelve weeks: all four steps. XL, over a quarter: split before estimating.

| Item | Size | Past item of the same size it was compared to |
|---|---|---|
| | | |

### Step 2: story points, one team only

Scale 1, 2, 3, 5, 8, 13; a 13 is split. Points are relative to a reference story, never hours, and never compared across teams. Velocity is measured; a negotiated velocity is a wish.

| Story | Points | Reference story compared to | Velocity per sprint, last six: low / median / high | Sprints needed: points / high, points / median, points / low |
|---|---|---|---|---|
| | | | | |

### Step 3: three-point (PERT)

Per component: optimistic O, most likely M, pessimistic P, in the same unit. Set P first, by asking what happened the last time this kind of work went wrong; a P set after M is anchored to it.

Expected E = (O + 4M + P) / 6. Standard deviation SD = (P minus O) / 6. Total E is the sum of the E's; total SD is the square root of the sum of the squared SD's. The date you can defend is E plus 2 SD.

| Component | O | M | P | E | SD |
|---|---|---|---|---|---|
| | | | | | |
| Total | | | | | |

### Step 4: reference class

| Reference class (past projects like this one) | Count | Actual / estimate at P50 | Actual / estimate at P80 | Source |
|---|---|---|---|---|
| | | | | |

Outside-view estimate = inside-view total x ratio at the chosen confidence. Fewer than five past projects: say so, and widen the range by hand.

### Step 5: missing work

| Work the stories did not price | Included / excluded / not applicable because | Weeks if excluded |
|---|---|---|
| Compliance or security review | | |
| Operational readiness and runbooks | | |
| Data migration | | |
| Instrumentation | | |
| Customer comms and training | | |
| Rollback and rehearsal | | |
| Accessibility | | |

### The only output

"[Item] will take between [low] and [high] weeks. We plan the team at [P50 outside view] and commit externally to [P80 outside view]. The single number nobody may quote is [E]."

## Reading the result

When the story-point range and the three-point range do not overlap, the stories never priced the pessimistic case; trust the wider one. When the reference-class ratio at P50 sits outside the three-point band, the team is optimistic in the way its history predicts; the outside view wins. When the velocity spread is wider than two to one, the sprint data is noise and step 2 is dropped. When step 5 adds more than step 3 estimated, the scope was a feature and the estimate is for a release; say which one the stakeholder asked for.

## ILLUSTRATIVE example

Invented estimate for multi-currency receipts in Ledgerline's expense-report copilot. Size M, compared with the mileage feature, which took five weeks. Story points: 34 across nine stories; velocity low 11, median 15, high 19 per two-week sprint, so 3.6 to 6.2 weeks.

| Component | O | M | P | E | SD |
|---|---|---|---|---|---|
| Exchange-rate service integration | 1 | 2 | 5 | 2.33 | 0.67 |
| Receipt parsing for currency formats | 1 | 1.5 | 4 | 1.83 | 0.50 |
| Policy rules per currency | 0.5 | 1 | 3 | 1.25 | 0.42 |
| Approval flow and UI | 1 | 2 | 3 | 2.00 | 0.33 |
| Total (weeks) | | | | 7.4 | 1.0 |

The two ranges do not overlap; the stories had no pessimistic case for the rate provider. Missing work: compliance review of the rate source (one week), ops readiness (half), customer comms (half), so the inside view is 9.4 weeks. Reference class: seven past integrations with an external data provider, actual over estimate 1.4 at P50 and 1.8 at P80. Outside view: 13.2 and 16.9 weeks. The output line: between 9 and 17 weeks; the team is planned at 13, the external commitment is 17, and the number nobody may quote is 7.

## The trap

The symmetric three-point. M is set first, O and P are set one week either side of it, the SD comes out small, and the sheet has produced a single number wearing a range as a disguise. Real pessimistic cases are several times the likely case, because they include the provider whose sandbox never arrived and the review nobody scheduled. Set P first from memory of the last bad case, and if P is not at least twice M, ask what has been forgotten.

## Feeds

- [Capacity plan](../../templates/planning/capacity-plan.md), the demand rows, in weeks per team with the range
- [Roadmap](../../templates/planning/roadmap.md): a Now row carries the P80 figure and the confidence
- [RICE scoring sheet](../prioritization/rice-scoring-sheet.md), the effort column
- [Dependency register](../../templates/execution/dependency-register.md), for waits found in step 5
- The [estimator agent](../../agents/estimator-agent.md) runs this sheet and flags the missing work
- PLANNING track; the committed figure is read at [Gate 2](../../os/STAGE-GATES.md) with the requirements it prices
- Method background: [Shape Up](../../knowledge/shape-up.md) for the fixed-appetite alternative, [RICE](../../knowledge/rice-prioritization.md) for where effort lands
