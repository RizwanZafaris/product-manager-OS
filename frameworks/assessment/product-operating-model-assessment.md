---
layer: frameworks
stage: DEFINE
gate: 2
feeds: ["templates/planning/product-strategy.md", "templates/planning/capacity-plan.md", "templates/planning/roadmap.md"]
method: "knowledge/cagan-product-teams.md"
aliases: ["Product Operating Model Assessment", "product-operating-model-assessment"]
---
# Product Operating Model Assessment

Based on the account of how companies move to a product way of working given by Marty Cagan with Lea Hickman, Chris Jones, Christian Idiodi and Jon Moore, in Transformed (2024). Explained here in this repository's own words.

## What it is for

Scoring whether the organization can execute the plan it just wrote. A strategy and a roadmap describe intended behavior; this sheet scores the behavior the company actually shows, dimension by dimension, against the level each dimension would have to reach for the plan to land. The output is a deficit per dimension, so the planning meeting stops arguing about ambition and starts choosing between three named moves: change the organization, cut the plan, or write down the risk and sign it. It resolves the argument where an executive says the teams are not delivering and the teams say they were handed a feature list with a date, because both are describing the same measurable thing from opposite ends.

## Run it when

- A strategy or a roadmap is drafted and about to be committed for a planning period
- A leader is new in the seat and needs a baseline before promising anything, alongside the [first 90 days plan](../../templates/planning/first-90-days.md)
- The last two planning periods both missed and nobody can say whether the plan or the organization was wrong
- Someone proposes a transformation, a reorganization, or a new way of working, and the case rests on which dimensions are actually weak

**Skip it when:** one team is running one bounded piece of work with a sponsor who leaves it alone. The dimensions below all score the same and the sheet tells you what the team already knows. Also skip it when the answer changes nothing, because nobody in the room can alter funding, staffing, or what the plan promises.

## Inputs you need first

- The plan itself: the [product strategy](../../templates/planning/product-strategy.md) bets and sequencing, or the [roadmap](../../templates/planning/roadmap.md) commitments
- The last two planning periods' results, so a score can cite what happened rather than what is felt
- The [capacity plan](../../templates/planning/capacity-plan.md), for who is actually assigned to what
- Named observables with dates: a decision, a release, a review, a funding call. A score with no observable is a mood

## The worksheet

### Step 1: the dimensions

Nine dimensions, named here in this repository's words. Each one is a behavior somebody can witness, not a value somebody can endorse.

| # | Dimension | The behavior being scored |
|---|---|---|
| 1 | Problem ownership | Teams are given a problem and a measure, not a feature list with dates already attached |
| 2 | The product seat is filled | Each team has someone who knows the customer, the data, the business constraints, and the industry well enough to be trusted with a no |
| 3 | Design and engineering are in early | Both are in the room while the problem is still open, not briefed after the decision |
| 4 | Risk retired before commitment | Value, usability, feasibility, and business risk are tested cheaply before a quarter of build is promised |
| 5 | Small releases the team owns | The team can ship and roll back within its own week, without a standing committee |
| 6 | A strategy that refuses | A short written set of bets with the not-now list attached, so focus survives the next request |
| 7 | Outcome accounting | Teams are reviewed on what moved and what was learned, not on the count of things shipped |
| 8 | Sponsor behavior | Leaders bring outcomes and constraints; they do not arrive with the solution and the date together |
| 9 | Funding and staffing shape | Money and people follow durable teams rather than one-off projects staffed by borrowing |

### Step 2: the scale

<!-- Score the organization as it behaved in the last two planning periods, not as it
     intends to behave. Rules that make the scores comparable between two scorers:
     a 2 or a 3 needs one dated observable, or it drops to 1; a 0 needs a named recent
     case, or it rises to 1. Score the teams this plan depends on, not the company average. -->

- **0** the opposite behavior is the norm, and you can name the recent case
- **1** the behavior is endorsed and talked about, and not observable
- **2** true for some of the teams, or some of the time
- **3** true across the teams this plan depends on, with a dated observable

The scale is four points on purpose. These behaviors are countable, so the honest resolution is coarse: either a team owned a problem last quarter or it was handed a list. A finer scale invites a twenty-minute argument about whether sponsor behavior is a 6 or a 7, which produces a decimal and no decision.

### Step 3: the deficit sheet

Required level is read off the plan, not off an ideal. Deficit = required minus actual, floored at zero. Readiness = the sum of the actual column, from 0 to 27. Pressure = the sum of the deficit column.

| # | Dimension | Required by this plan (1 to 3) | Actual (0 to 3) | Dated observable behind the actual score | Deficit | Load bearing | The move (change the org / cut the plan / accept and sign) | Owner |
|---|---|---|---|---|---|---|---|---|
| 1 | Problem ownership | [ ] | [ ] | [ ] | [ ] | yes | [ ] | [ ] |
| 2 | Product seat filled | [ ] | [ ] | [ ] | [ ] | yes | [ ] | [ ] |
| 3 | Design and engineering early | [ ] | [ ] | [ ] | [ ] | no | [ ] | [ ] |
| 4 | Risk retired before commitment | [ ] | [ ] | [ ] | [ ] | yes | [ ] | [ ] |
| 5 | Small releases the team owns | [ ] | [ ] | [ ] | [ ] | no | [ ] | [ ] |
| 6 | A strategy that refuses | [ ] | [ ] | [ ] | [ ] | no | [ ] | [ ] |
| 7 | Outcome accounting | [ ] | [ ] | [ ] | [ ] | no | [ ] | [ ] |
| 8 | Sponsor behavior | [ ] | [ ] | [ ] | [ ] | no | [ ] | [ ] |
| 9 | Funding and staffing shape | [ ] | [ ] | [ ] | [ ] | yes | [ ] | [ ] |

**Blocker rule:** a deficit of 2 or more on any load-bearing dimension is a blocker whatever the totals say. Those four gate the other five: an unfunded team with no product seat cannot own a problem, and cannot retire a risk before someone else commits its quarter. The rule exists instead of weights, because weights get renegotiated by whoever dislikes the answer.

The deficit-of-2 blocker threshold and the pressure bands below are a local heuristic authored here, not part of Cagan, Hickman, Jones, Idiodi, and Moore's account in Transformed; the book describes the nine dimensions and the failure modes, and sets no numeric blocker rule or pressure scale. Treat both as this repository's own scoring convention.

## How to read the result

Read pressure first, then blockers, then readiness.

| Pressure | What it means | The action it implies |
|---|---|---|
| 0 to 2 | The organization can carry this plan | Commit it, and put the one or two gaps in the plan's risk section |
| 3 to 5 | The plan is bigger than the organization by a known amount | Cut or stage the plan to what the weak dimensions can carry this period |
| 6 or more | The plan is a description of a different company | Write a smaller plan for this period, and a separate change plan with its own owner for the dimensions |

Any blocker overrides the band above it: with a blocker open, the only honest commitments are the ones that do not depend on that dimension. Readiness is the trend line, not the verdict. Re-scored each period against the same observables, it shows whether the change is real; a readiness that climbs while pressure stays flat means the plan grew as fast as the capability, which is worth naming out loud. Two dimensions moving from 1 to 2 in one period is fast. Nine dimensions at 3 means your scorers stopped needing observables.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. The plan under assessment: extend the copilot to every filer this period and enter a new customer segment at the same time. All numbers below are ILLUSTRATIVE.

| # | Dimension | Required | Actual | Observable | Deficit |
|---|---|---|---|---|---|
| 1 | Problem ownership | 3 | 2 | copilot team owned the auto-categorization measure; the mobile team got a dated feature list in the same period | 1 |
| 2 | Product seat filled | 3 | 2 | copilot team has one; the new segment has no named product person | 1 |
| 3 | Design and engineering early | 2 | 2 | engineering lead was in the consent-screen sessions before scoping | 0 |
| 4 | Risk retired before commitment | 3 | 1 | the segment entry is committed with no test run; nobody could name a killed idea from last period | 2 |
| 5 | Small releases the team owns | 2 | 3 | copilot shipped nine times last period and rolled back once, same day | 0 |
| 6 | A strategy that refuses | 2 | 1 | four bets written, no not-now list; two mid-period additions accepted | 1 |
| 7 | Outcome accounting | 2 | 2 | last review opened with the categorization measure, then walked the shipped list | 0 |
| 8 | Sponsor behavior | 2 | 1 | segment entry arrived as a solution with a date from the sponsor | 1 |
| 9 | Funding and staffing shape | 3 | 1 | the segment work is funded as a project staffed by borrowing two engineers from the copilot team | 2 |

Readiness 15 of 27. Pressure 8. Two blockers: dimensions 4 and 9. The read: the copilot half of the plan is executable and the segment entry is not, because it is unfunded, unstaffed, unowned, and untested. Pressure 8 sits in the band of 6 or more, so the sheet records two moves rather than one. The smaller plan: keep the copilot commitment, and replace the segment commitment with one funded discovery team and a decision date. The separate change plan, with its own owner: dimensions 9 and 4, funding shape and risk retirement, owned by the head of product with a checkpoint each period, because neither is fixable by cutting scope inside this planning period. Recording only the first move is the common error here, and it is what turns a pressure of 8 into a pressure of 8 again next period. The sponsor's date is not a capability, so it does not raise the score.

## The decision it feeds

Whether to commit this plan for the coming planning period as written, cut it to what the organization can carry, or fund a change to a dimension before promising the work that depends on it. It also decides which commitments are safe to repeat in an [exec update](../../templates/planning/exec-update.md), because a commitment resting on an open blocker is a forecast of somebody else's behavior.

## Where the output lands

The [product strategy](../../templates/planning/product-strategy.md), section 4 for the re-cut sequencing and section 6 for each open blocker written as a risk with an owner. The gap rows that need money or headcount land in the [capacity plan](../../templates/planning/capacity-plan.md), section 6.

## Re-run trigger

Re-run at the start of each planning period, and immediately when the organization changes shape: a reorganization, a funding model change, a new sponsor over the portfolio, or the departure of a person who was holding a dimension up on their own.

## When this method misleads you

Scored by the leader whose behavior dimension 8 is about, it produces a confident sheet with the sponsor at 3 and the teams at 1, and reads as a delivery problem. Get the scores from the people who witness the behavior, and require the dated observable in every row from everyone.

It also misleads at both edges. A company with genuinely low scores in a market with no competition can miss on every dimension and keep winning for years, so a high pressure score is not a prediction of failure; it is a statement about this plan. And a plan that promises little sets low required levels, so a feature factory running a feature-factory plan scores near zero pressure and looks healthy. Read the required column as a claim about ambition before you read the deficits, and if every required level is a 1, the sheet you needed was a strategy critique, not an assessment. The last failure mode is treating a dimension as a switch: staffing a product seat does not fill it, and the score should not move until somebody can point at a no that was accepted.

## Feeds

- [Product strategy](../../templates/planning/product-strategy.md), sections 4 and 6; [capacity plan](../../templates/planning/capacity-plan.md), section 6
- [Roadmap](../../templates/planning/roadmap.md) and [program charter](../../templates/planning/program-charter.md), where a cut plan gets rewritten
- [Gate 2: requirements signed off](../../os/STAGE-GATES.md), which should not pass on a commitment resting on an open blocker
- [Risk matrix](../execution/risk-matrix.md) for scoring the accepted gaps, and [RACI](../execution/raci.md) when dimension 1 or 8 is the weak one
- [Strategy kernel](../strategy/strategy-kernel.md), which tests whether the plan being assessed is a strategy at all
- Method background: [Cagan's four risks](../../knowledge/cagan-product-teams.md) for dimension 4, and [triad decision rights](../../knowledge/roles/triad-decision-rights.md) for dimensions 1 and 3
