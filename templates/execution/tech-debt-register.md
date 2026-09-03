---
layer: templates
stage: BUILD
gate: 3
feeds: []
method: ""
aliases: ["Tech Debt Register", "tech-debt-register"]
---
# Tech Debt Register: [product or system]

Stage: BUILD, reviewed every planning cycle; feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md) and the standing-demand row of the [capacity plan](../planning/capacity-plan.md)
Knowledge: [WSJF and cost of delay](../../frameworks/prioritization/wsjf-cost-of-delay.md)
Skill: [architect agent](../../agents/architect-agent.md)

> **Delete any section you do not need.** One service with three known problems needs sections 2 and 4. The full form is for a product where debt is contested at every planning meeting and nobody can say what it costs. Never leave a heading standing over white space.

<!-- Debt as a ledger with an interest rate. Every item states what it costs the
     team each quarter while it stands (interest, in team-days) and what it costs
     once to remove (principal). The ratio between them is the payoff order, and the
     interest total is a line in the capacity plan, which is what stops debt from
     being paid out of the 20 percent nobody planned.

     Neighbours: the risk register (risk-register.md) owns things that might happen;
     debt is happening now and is paid weekly. ADRs (../architecture/adr.md) record
     the decision to take debt on; this file tracks it afterward. The capacity plan
     (../planning/capacity-plan.md) takes the section 6 total as standing demand.

     See also the tech debt assessment
     (../../frameworks/assessment/tech-debt-assessment.md), which decides what
     belongs on this register at all and gives each item its quadrant. Cunningham's
     original meaning sorts admissions from careless work; Fowler's quadrant says
     whether removing the code is enough or whether something upstream produced it.

     Fill first: the register rows in section 2 with an interest figure each, the
     payoff plan in section 4, and the quarter's debt budget in section 3. -->

**Owner:** [name] · **Engineering lead:** [name] · **Last reviewed:** [YYYY-MM-DD] · **Cadence:** every planning cycle · **Unit:** team-days per quarter

## 1. How interest is counted

<!-- Interest is team-days per quarter spent because the item exists: workarounds,
     slower changes in the affected code, incidents it causes, manual steps, and
     onboarding time. Measure it from last quarter's tickets and incident hours
     where you can; estimate it and label it ILLUSTRATIVE where you cannot, with a
     date to measure. An item with zero interest is not debt, it is a preference,
     and it leaves the register. Principal is the team-days to remove the item, as a
     range from the estimation sheet. -->

- **Interest sources counted here:** [workaround time / change slowdown / incidents / manual operations / onboarding]
- **Measured from:** [ticket tags, incident log, on-call notes]

## 2. The register

<!-- Items are facts about the system, stated so that a new engineer could verify
     them. "The parser is messy" is an opinion; "the parser has no test harness, so
     every change is verified by hand" is debt. The italic row is ILLUSTRATIVE. -->

| # | Item (a fact about the system) | Where | Taken on when, why, and where recorded | Interest (team-days per quarter) | Principal (team-days, low to high) | Ratio (interest / likely principal) | Trend (growing / flat / shrinking) | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |
| *1* | *receipt parser has no test harness; every change is verified by hand (ILLUSTRATIVE)* | *extraction service* | *two quarters ago, to hit the pilot date, ADR-[n]* | *6* | *8 to 12* | *0.6* | *growing* | *[name]* | *scheduled next quarter* |

## 3. Payoff rule and budget

- **Order:** highest ratio first. An item with a ratio above 1 pays for itself inside a quarter and does not wait for a convenient moment.
- **Bundling:** an item whose code an initiative is about to touch is paid inside that initiative, and the initiative's estimate says so.
- **Budget this quarter:** [n] team-days, agreed in the capacity plan and not borrowed against.
- **Exception:** an item with a growing trend and a ratio above 1 that is not in the payoff plan needs a name in section 5 by the next review.

## 4. Payoff plan

| Register # | Quarter | Team-days budgeted | Bundled with (initiative touching the same code, or "standalone") | Done when (the verification) | Status |
|---|---|---|---|---|---|
| | | | | | |

## 5. Accepted debt

<!-- Debt someone chose to carry, signed. The signature is what makes "later" honest.
     Revisit when names an event, not a season. -->

| Register # | Accepted by (name, role) | Rationale in one sentence | Revisit when | Date |
|---|---|---|---|---|
| | | | | |

## 6. Interest total

<!-- The sum of the interest column for every open item, copied into section 4 of
     the capacity plan as standing demand. If the total exceeds the debt budget by a
     wide margin, the plan is paying interest it never scheduled. -->

- **Open items:** [n] · **Interest total this quarter:** [n] team-days · **Debt budget:** [n] team-days · **Copied to capacity plan on:** [YYYY-MM-DD]

## 7. Retired

| Register # | Paid off on | Interest saved per quarter | Estimated principal | Actual principal | What we learned about the estimate |
|---|---|---|---|---|---|
| | | | | | |

---

## Exit gate (feeds Gate 3: architecture and risks reviewed)

Done when every box is honestly ticked. The register goes to [Gate 3](../../os/STAGE-GATES.md) with the architecture set, and its interest total goes to [capacity-plan.md](../planning/capacity-plan.md).

- [ ] Every item is a verifiable fact about the system, not a preference
- [ ] Every item has an interest figure in team-days per quarter, measured or labeled ILLUSTRATIVE with a date to measure
- [ ] Every principal is a range, not a single number
- [ ] Every item with a ratio above 1 is in the payoff plan or accepted by name
- [ ] The interest total appears in the capacity plan's standing demand
- [ ] The debt budget is the figure agreed in the capacity plan
- [ ] Retired items record actual against estimated principal
- [ ] The ILLUSTRATIVE row has been deleted
- [ ] Signed by [name], [date]
