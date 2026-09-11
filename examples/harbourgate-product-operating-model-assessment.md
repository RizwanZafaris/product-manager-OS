# Harbourgate Product Operating Model Assessment

Fills [frameworks/assessment/product-operating-model-assessment.md](../frameworks/assessment/product-operating-model-assessment.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe, Tidewater and every person are fictional, and every number, date and rate is ILLUSTRATIVE, chosen to reconcile with the [Harbourgate journey](harbourgate-journey.md) and the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md).

**Owner:** Ife Adeyemi, Product Manager · **Scored with:** Tomasz Wierzbicki, Engineering Lead · **Date:** 2026-10-15 · **Plan assessed:** Q4 2026, including the sunset, peak freeze, DEP-4 support and table-shape preparation · **Output:** Q4 capacity plan

## What it is for

This assessment asks whether Harbourgate's product operating model can carry the Q4 2026 plan. The plan includes the legacy payment path sunset, the peak change freeze, support for DEP-4, and preparation for removal of the old table shape on 2027-03-31.

The assessment was scored against observable behavior in the last two planning periods, not against stated intent. The dated evidence includes D-019, the rehearsal evidence, the Gate 6 outcome, D-022 and D-024. The result is readiness 23 of 27, pressure 2, and no blocker.

The two deficits are:

1. **Risk retired before commitment:** D-019 was committed on 2026-06-02, eleven days before rehearsal 1 on 2026-06-13. **Owner:** Tomasz Wierzbicki.
2. **Funding and staffing shape:** the caretaker role named on 2026-04-24 has no funded successor, and 0.4 FTE of on-call capacity remains borrowed by the legacy path. **Owner:** Tomasz Wierzbicki.

## Run it when

- A plan is drafted and is about to be committed for a planning period
- The organization needs to know whether the sunset, peak freeze, DEP-4 support and table-shape preparation fit the capacity it actually has
- The last two planning periods contain evidence that can distinguish capability from intention
- Funding, staffing, risk retirement or plan scope can still be changed

**Skip it when:** the answer cannot change funding, staffing, or what the plan promises. This assessment is useful here because its output feeds the Q4 capacity plan.

## Inputs you need first

- The Q4 2026 plan: sunset, peak freeze, DEP-4 support and table-shape preparation
- The last two planning periods' observed results
- D-019 and the evidence from rehearsal 1
- D-022 and D-024, which show the accepted peak-freeze and sunset decisions
- N18 and N19, the Gate 6 outcome measures
- N40, the rollback rehearsal evidence
- N54, the on-call share consumed by the legacy path
- The [Harbourgate journey](harbourgate-journey.md) and its [supplementary coverage sheet](harbourgate-coverage-sheet.md)

## The worksheet

### Step 1: the dimensions

| # | Dimension | The behavior being scored for Harbourgate |
|---|---|---|
| 1 | Problem ownership | The payments team owns the problem and measure, rather than receiving a feature list with a date |
| 2 | The product seat is filled | The team has a trusted product owner who knows the customer, data, constraints and industry well enough to accept a no |
| 3 | Design and engineering are in early | Design and engineering participate while the problem is still open |
| 4 | Risk retired before commitment | Value, usability, feasibility and business risk are tested before a quarter of work is promised |
| 5 | Small releases the team owns | The team can release and roll back without a standing committee |
| 6 | A strategy that refuses | The plan has explicit bets and a maintained out-of-scope list |
| 7 | Outcome accounting | Reviews use outcome measures and learning, not only shipped work |
| 8 | Sponsor behavior | Leaders bring outcomes and constraints rather than a solution and date together |
| 9 | Funding and staffing shape | Funding and people follow a durable team rather than a one-off project staffed by borrowing |

### Step 2: the scale

The scoring uses the worksheet scale and the dated observables in HC45. A score of 2 or 3 has a dated observable. No dimension receives 0 or 1 without a named recent case.

- **0:** the opposite behavior is the norm, and a recent case can be named
- **1:** the behavior is endorsed and talked about, but is not observable
- **2:** true for some teams, or some of the time
- **3:** true across the teams this plan depends on, with a dated observable

The assessment is measured rather than target-based. The scores describe what Harbourgate did in the last two planning periods.

### Step 3: the deficit sheet

Deficit equals required minus actual, floored at zero.

| # | Dimension | Required by this plan (1 to 3) | Actual (0 to 3) | Dated observable behind the actual score | Deficit arithmetic | Deficit | Load bearing | The move | Owner |
|---|---|---:|---:|---|---:|---:|---|---|---|
| 1 | Problem ownership | 3 | 3 | Gate 2 attempt 2, 2026-04-07 | 3 - 3 = 0 | 0 | yes | Accept and sign, with the existing evidence carried into the Q4 plan | Ife Adeyemi |
| 2 | Product seat filled | 3 | 3 | D-024, 2026-10-14, names Ife Adeyemi as owner of the legacy retirement | 3 - 3 = 0 | 0 | yes | Accept and sign | Ife Adeyemi |
| 3 | Design and engineering early | 2 | 2 | The STRIDE walk of 2026-04-08 shows design informed, not in the room | 2 - 2 = 0 | 0 | no | Accept and sign, while recording the evidence limitation | Ines Castellanos and Tomasz Wierzbicki |
| 4 | Risk retired before commitment | 3 | 2 | D-019 was committed on 2026-06-02, eleven days before rehearsal 1 on 2026-06-13 | 3 - 2 = 1 | 1 | yes | Accept and sign the gap, and require risk retirement before the next comparable commitment | Tomasz Wierzbicki |
| 5 | Small releases the team owns | 2 | 3 | The rollback rehearsal on 2026-07-04 took 3 min 50 s to flip to legacy and 22 minutes to restore | 2 - 3 = -1, floored at 0 | 0 | no | Accept and sign | Tomasz Wierzbicki |
| 6 | A strategy that refuses | 2 | 3 | The out-of-scope table was held at Gate 5 on 2026-07-08 | 2 - 3 = -1, floored at 0 | 0 | no | Accept and sign | Ife Adeyemi |
| 7 | Outcome accounting | 2 | 3 | Gate 6 on 2026-10-14 used the measured decline rates and payment-step non-completion, N18 and N19 | 2 - 3 = -1, floored at 0 | 0 | no | Accept and sign | Ife Adeyemi and Priya Raman |
| 8 | Sponsor behavior | 2 | 3 | D-022 on 2026-08-24 accepted R4 with the kiosk fallback, peak freeze and quarterly review | 2 - 3 = -1, floored at 0 | 0 | no | Accept and sign | Rohan Iyer |
| 9 | Funding and staffing shape | 2 | 1 | The caretaker role of 2026-04-24 has no funded successor, and N54 records 0.4 FTE borrowed from on-call | 2 - 1 = 1 | 1 | yes | Accept and sign the gap in the Q4 capacity plan, with a funded successor or an explicit capacity trade-off | Tomasz Wierzbicki |
|  | **Total** |  | **3 + 3 + 2 + 2 + 3 + 3 + 3 + 3 + 1 = 23** |  | **0 + 0 + 0 + 1 + 0 + 0 + 0 + 0 + 1 = 2** | **2** | **No deficit is 2 or more** | **Commit the plan with the two named gaps recorded** |  |

**Readiness arithmetic:** 3 + 3 + 2 + 2 + 3 + 3 + 3 + 3 + 1 = **23 of 27**.

**Pressure arithmetic:** 0 + 0 + 0 + 1 + 0 + 0 + 0 + 0 + 1 = **2**.

**Blocker check:** the load-bearing deficits are 0, 0, 1 and 1. The largest deficit is 1, so there is **no blocker** under the deficit-of-2 rule.

The two deficits are not reasons to cut the Q4 plan. They are named risks to carry into the Q4 capacity plan:

- **Risk retired before commitment, owner Tomasz Wierzbicki:** D-019 committed the one-weekend shape before rehearsal 1 showed that settlement files and in-flight work could not be verified in that shape. D-021 replaced it with the phased traffic shift and legacy drain.
- **Funding and staffing shape, owner Tomasz Wierzbicki:** the caretaker role has no funded successor, while N54 records 0.4 FTE of on-call capacity consumed by the legacy path. The capacity plan must show how this load is released by the sunset or what work is traded.

## How to read the result

Read pressure first, then blockers, then readiness.

| Pressure | What it means | The action it implies | Harbourgate reading |
|---|---|---|---|
| 0 to 2 | The organization can carry this plan | Commit it, and put the one or two gaps in the plan's risk section | Pressure is 2, so Harbourgate can carry the Q4 plan with the two gaps recorded |
| 3 to 5 | The plan is bigger than the organization by a known amount | Cut or stage the plan to what the weak dimensions can carry this period | Not applicable |
| 6 or more | The plan is a description of a different company | Write a smaller plan and a separate change plan | Not applicable |

No blocker overrides the pressure band. Readiness is 23 of 27, and the pressure of 2 is the decision signal. The plan can be committed because the two deficits are each 1, neither is a blocker, and both have named owners.

The result does not mean that risk retirement or staffing shape are solved. It means they are small enough to carry as explicit Q4 capacity risks rather than requiring the sunset, peak freeze, DEP-4 support or table-shape preparation to be cut before commitment.

## ILLUSTRATIVE example

The assessed plan is Harbourgate's Q4 2026 plan: retire the legacy payment path, hold the peak change freeze, support DEP-4, and prepare for removal of the old table shape on 2027-03-31. All numbers and dates below are ILLUSTRATIVE.

| # | Dimension | Required | Actual | Observable | Deficit |
|---|---|---:|---:|---|---:|
| 1 | Problem ownership | 3 | 3 | Gate 2 attempt 2, 2026-04-07 | 0 |
| 2 | Product seat filled | 3 | 3 | D-024, 2026-10-14 | 0 |
| 3 | Design and engineering early | 2 | 2 | STRIDE walk, 2026-04-08; design was informed, not in the room | 0 |
| 4 | Risk retired before commitment | 3 | 2 | D-019 was committed on 2026-06-02, eleven days before rehearsal 1 | 1 |
| 5 | Small releases the team owns | 2 | 3 | Rollback rehearsal, 2026-07-04, took 3 min 50 s | 0 |
| 6 | A strategy that refuses | 2 | 3 | Out-of-scope table held at Gate 5, 2026-07-08 | 0 |
| 7 | Outcome accounting | 2 | 3 | Gate 6 used N18 and N19, 2026-10-14 | 0 |
| 8 | Sponsor behavior | 2 | 3 | D-022, 2026-08-24 | 0 |
| 9 | Funding and staffing shape | 2 | 1 | Caretaker role has no funded successor; N54 records 0.4 FTE borrowed from on-call | 1 |

Readiness arithmetic: 3 + 3 + 2 + 2 + 3 + 3 + 3 + 3 + 1 = **23 of 27**.

Pressure arithmetic: 0 + 0 + 0 + 1 + 0 + 0 + 0 + 0 + 1 = **2**.

There is no blocker because neither load-bearing deficit reaches 2. The read is that Harbourgate can carry the plan, provided the Q4 capacity plan carries two explicit actions: Tomasz Wierzbicki owns the risk-retirement gap, and Tomasz Wierzbicki owns the funding and staffing shape gap.

The plan does not need to be cut. The sunset, peak freeze, DEP-4 support and table-shape preparation remain committed. The capacity plan must show how the 0.4 FTE legacy on-call share is released by the sunset and how the caretaker responsibility is funded or replaced.

## The decision it feeds

Commit the Q4 2026 plan as written, with two named capacity risks:

1. **Risk retired before commitment**, owned by Tomasz Wierzbicki. Future comparable commitments must have risk evidence before commitment, rather than relying on a rehearsal after the decision.
2. **Funding and staffing shape**, owned by Tomasz Wierzbicki. The Q4 plan must show the treatment of the caretaker role and the 0.4 FTE on-call share consumed by the legacy path.

The assessment does not change D-022 or D-024. D-022 remains the sponsor's accepted decision for R4, and D-024 remains the decision to persist with Quay and retire the legacy path by 2026-12-15.

## Where the output lands

The [Q4 capacity plan](harbourgate-capacity-plan.md), where the two deficits are recorded as capacity risks and the sunset load is reconciled against available supply.

The sunset work includes the legacy path shutdown on 2026-12-15. DEP-4 remains in progress, with reporting due off the legacy table shape by 2027-02-27 and the old table shape removal date on 2027-03-31.

## Re-run trigger

Re-run at the start of the next planning period, and immediately if any of the following changes:

- The funding or staffing shape changes
- The caretaker role gains or loses a funded successor
- The 0.4 FTE on-call share changes before the legacy path shutdown
- The peak change freeze changes from 2026-11-13 to 2026-12-04
- DEP-4 changes scope, owner or committed date
- The legacy path shutdown date changes from 2026-12-15
- A new commitment is made before its material risks are retired

## When this method misleads you

The assessment can make a plan look safe when the required levels are too low. Here, the required level for funding and staffing shape is 2, not 3, because the Q4 plan can carry the known caretaker and borrowed on-call arrangement only if the capacity plan makes the trade-off explicit. That does not mean the arrangement is durable.

It can also over-credit a dated decision. D-024 gives evidence for the product seat, but a named owner alone does not prove that every staffing or funding problem is solved. The funding and staffing score remains 1 because the caretaker role has no funded successor and N54 records 0.4 FTE borrowed from on-call.

The risk-retirement score is also deliberately coarse. D-019 and rehearsal 1 show that a risk was committed before it was retired. D-021, ADR-0004, N40 and the later delivery evidence show that Harbourgate learned and changed the operating model. The score of 2 records both facts, rather than treating the later recovery as proof that the earlier commitment behavior was strong.

Finally, a pressure of 2 is not a prediction that the Q4 plan will succeed. It says the observed capability can carry the stated plan with two open gaps. If the gaps become blockers, the decision changes even if readiness remains 23.

## Feeds

- [Q4 capacity plan](harbourgate-capacity-plan.md), for the sunset, peak freeze, DEP-4 support, table-shape preparation and the 0.4 FTE on-call share
- [Harbourgate journey](harbourgate-journey.md), for D-019, D-022, D-024, N18, N19, N40 and N54
- [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), for HC45 and the assessment record
- [Product strategy](../templates/planning/product-strategy.md), for any change to sequencing or open risks
- [Roadmap](../templates/planning/roadmap.md), if the Q4 plan is staged or cut
- [Risk matrix](../frameworks/execution/risk-matrix.md), if the accepted gaps need a separate risk treatment
- [RACI](../frameworks/execution/raci.md), if the caretaker role or the funding and staffing owner changes
- Method background: [Cagan product teams](../knowledge/cagan-product-teams.md) and [triad decision rights](../knowledge/roles/triad-decision-rights.md)

**Exit gate walk, 2026-10-15:** Ife Adeyemi, Product Manager, and Tomasz Wierzbicki, Engineering Lead, confirm readiness **23 of 27**, pressure **2**, **no blocker**, and commit the Q4 2026 plan with the two deficits recorded in the Q4 capacity plan.
