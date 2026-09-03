---
layer: frameworks
stage: DESIGN
gate: 3
feeds: ["templates/execution/tech-debt-register.md", "templates/planning/capacity-plan.md", "frameworks/prioritization/wsjf-cost-of-delay.md"]
method: "knowledge/shape-up.md"
aliases: ["Tech Debt Assessment", "tech-debt-assessment"]
---
# Tech Debt Assessment

The debt metaphor comes from Ward Cunningham's experience report at OOPSLA in 1992; the quadrant that sorts debt as deliberate or inadvertent and as prudent or reckless comes from Martin Fowler's 2009 post on the technical debt quadrant. Explained here in this repository's own words.

## What it is for

The planning meeting where engineering asks for a slice of the next cycle and product asks what that slice buys, and neither side can put a number on the arrangement they already have. This sheet gives every known compromise two numbers, what it costs per quarter to leave standing and what it costs once to remove, and one quadrant that says whether removing it is enough. It ends the argument between "the codebase is a mess" and "we have features to ship", because both of those are unfalsifiable and the ratio of two team-day figures is not.

Two people wrote the halves of this method, seventeen years apart, and they are routinely treated as one. Keep them apart. Ward Cunningham gave the metaphor in 1992 and meant something narrow: code shipped before the team fully understood the domain, shipped knowingly, with the intention of bringing it back in line as understanding improved. The interest was the drag you pay until you do. He did not mean careless work, because careless work is not a loan. Martin Fowler added the quadrant in 2009, sorting an item by whether it was taken on deliberately or discovered later, and by whether the choice was prudent or reckless. That grid covers far more ground than Cunningham's original, which is useful here and is also how the term went slack everywhere else. This sheet uses both for different jobs: Cunningham's meaning decides what belongs on the register at all, Fowler's quadrant decides what to change besides the code.

## Run it when

- The next planning cycle is being sized and engineering has asked for debt capacity
- Before Gate 3, when the architecture set goes to review and the known compromises need owners and numbers
- The same area of the system shows up in three consecutive postmortems, slipped estimates, or on-call handovers
- An initiative is about to open code somebody has been warning about, which is the cheapest hour this work will ever cost

**Skip it when:** the system has a dated sunset inside two quarters, or the item is one incident's root cause. Interest stops being paid when the system goes off, and an incident cause belongs in the postmortem's actions, where it gets attention this month rather than at the next quarterly review.

## Inputs you need first

- Last quarter's tickets and on-call hours, tagged by area, because interest is counted and not remembered
- Principal ranges from the [estimation sheet](../execution/estimation-sheet.md), low to likely to high
- The [ADR](../../templates/architecture/adr.md) set, which is the evidence that an item was taken on deliberately rather than found
- This cycle's debt budget from the [capacity plan](../../templates/planning/capacity-plan.md), section 4
- The initiative list for the cycle, so that bundling an item into work already opening the file is a real option

## The worksheet

### Step 1: the Cunningham test, which decides what is on the sheet at all

<!-- Run all three questions on every candidate row. Three yeses, it is debt and it
     gets scored. One no, it belongs somewhere else, and the sheet says where. This
     step is the whole defence against a register that fills up with preferences. -->

| Question | Yes looks like | No means it goes to |
|---|---|---|
| Is it a fact a new engineer could verify in an afternoon | "the parser has no test harness, so every change is checked by hand" | nowhere; rewrite it as a fact or drop it. "The parser is messy" is an opinion |
| Does it cost measurable time every quarter it stands | hours in tickets, on-call, or manual steps somebody can point at | the backlog as a preference. No interest, no loan |
| Does the team now know what the right shape is | a design somebody could implement this quarter | the architecture set as an open design question, not a debt row |

### Step 2: the Fowler quadrant, which decides what else has to change

| Quadrant | What happened | What paying the principal buys | The second action it demands |
|---|---|---|---|
| DP, deliberate and prudent | The shortcut was chosen with open eyes and written down | The full benefit. This is the loan Cunningham described | Check the ADR's revisit trigger has a date and an owner, and that the date has not passed |
| DR, deliberate and reckless | Chosen under deadline pressure, with no design time and no record | The benefit, until the next deadline recreates the same item | Change what produced the pressure: the commitment cadence, or the design time inside the estimate |
| IP, inadvertent and prudent | The team learned the right shape only after building the wrong one | The full benefit. This quadrant is not a failure | None. This is what learning costs. Refactor when the code is next open |
| IR, inadvertent and reckless | Nobody saw the shape was wrong, and nobody in the room would have | Nothing durable. The same shape returns in the next service | A capability change: a review step, a pairing, or a named owner for that part of the design |

### Step 3: the arithmetic

Interest, in whole team-days per quarter, is the time lost because the item exists: workarounds, slower changes in the affected code, incidents it causes, manual operations, onboarding. Sum it across every team that pays it, not only the team that owns the code. Under one team-day per quarter rounds to zero and the row leaves the sheet.

Principal, in team-days, is the cost to remove the item, written low to likely to high from the estimation sheet.

Ratio = interest / likely principal, reported to one decimal. Payback in quarters = likely principal / interest.

The scale is deliberately coarse. Interest comes from tickets that were tagged inconsistently and principal comes from an estimate whose ends differ by a third or more, so a two-decimal ratio claims a precision neither input carries. Three bands, one decimal, whole days: the sheet has to survive being wrong by a third and still order the queue correctly.

| Ratio | What it means | The action |
|---|---|---|
| 1.0 and above | Removal pays for itself inside one quarter | Schedule it in the next cycle. It does not wait for a convenient moment |
| 0.3 to under 1.0 | Removal pays back over two to three quarters | Bundle it with the next initiative that opens the same code. Standalone only when the trend is growing |
| Under 0.3 | The interest is real and small | Accept it by name with a revisit trigger, or delete the row |

### Step 4: the sheet

<!-- Both basis columns are load-bearing. An interest figure with no basis is the
     loudest voice in the room wearing a number, and next quarter it will be a
     different number. Where the basis is an estimate rather than a count, label the
     figure ILLUSTRATIVE and put a date on the sheet by which it will be measured. -->

| # | Item, as a verifiable fact | Where | Quadrant | Recorded in | Interest (team-days per quarter) | Teams paying | Basis for interest | Principal, low to likely to high | Basis for principal | Ratio | Trend | Second action (from step 2) | Owner | Decision (pay now / bundle / accept, signed) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [n] | [fact] | [service] | [DP / DR / IP / IR] | [ADR id, or "found in review"] | [n] | [n] | [ticket tag, incident log, or ILLUSTRATIVE with a date to measure] | [n to n to n] | [estimation sheet ref] | [x.x] | [growing / flat / shrinking] | [what changes besides the code] | [role] | [decision] |

Totals to carry: open rows, interest total, debt budget this cycle, and the difference between the last two.

## ILLUSTRATIVE example

Invented rows for Ledgerline's expense-report copilot, sized before a planning cycle. Every number here is invented for the example.

| # | Item (ILLUSTRATIVE) | Quadrant | Interest | Likely principal | Ratio | Trend | Decision |
|---|---|---|---|---|---|---|---|
| 1 | Approval events and draft events share one table with no type column, so every audit query scans the whole history | IR | 9 | 7 | 1.3 | growing | pay now |
| 2 | Category thresholds live in a spreadsheet one engineer edits by hand before each release | DR | 4 | 4 | 1.0 | flat | pay now |
| 3 | The copilot prompt template is duplicated across three services | DP | 2 | 3 | 0.7 | flat | bundle with the multi-currency work |
| 4 | Receipt parser has no test harness, so every change is verified by hand | DP | 6 | 10 | 0.6 | growing | bundle; the ADR's revisit date has passed |
| 5 | Two currency rounding paths, one in the copilot and one in the legacy report builder | IP | 3 | 15 | 0.2 | flat | accept, signed by the engineering lead, revisit when the third country opens |

Interest total is 24 team-days per quarter against a debt budget of 12 (both ILLUSTRATIVE). Rows 1 and 2 fit that budget at 11 team-days of principal and remove 13 team-days per quarter of interest, so the cycle earns back more than it spends before the cycle ends. Row 1 is where the quadrant earns its place on the page: paying the principal without adding a design review for event schemas means the same table shape appears in the next service, and this sheet grows a row 6 next year. Row 5 is the honest accept, because three quarters or more to pay back deserves a signature and a trigger rather than a slot.

## How to read the result

Rows are queued by ratio and nothing else, because the ratio is the only column that compares a recurring cost with a one-off one. Read the aggregates next. An interest total more than double the debt budget means the cycle is already paying for the debt, unplanned, as slower delivery; take the difference to the capacity plan as standing demand instead of relitigating it in a sprint. A quadrant mix weighted to DR is a finding about the commitment cadence, and no amount of principal fixes it. Weighted to IR is a capability gap, and the fix is who reviews design, not who refactors. Weighted to IP on a young system is healthy. Nothing above 0.3 anywhere is either a clean system or an interest column filled in from memory, so read the basis column before believing the good news. A row that has carried no interest figure through two reviews gets deleted: it is a preference that learned the vocabulary.

## The decision it feeds

How many team-days of the next planning cycle go to debt, which items get them, and in what order. For every item that does not get a slot, the same output forces the second decision: bundled into an initiative that opens the code anyway, or accepted by a named person with a revisit trigger. Nothing stays unowned. When the interest total dwarfs the capacity for two cycles running, the decision moves up a level and the plan itself goes back to DESIGN.

## Where the output lands

- [Tech debt register](../../templates/execution/tech-debt-register.md): rows into section 2, the queue into sections 3 and 4, signed accepts into section 5, the interest total into section 6
- [Capacity plan](../../templates/planning/capacity-plan.md), section 4, where the interest total is standing demand rather than a surprise
- [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md), which asks that every compromise in the architecture set has a number and an owner

## Re-run trigger

Re-run at the start of every planning cycle, and out of cycle the first time a postmortem, a slipped estimate, or a security finding names an area already on the sheet, because that event has just measured the interest column for you and the figure on the sheet is now too low. A sheet with no re-run trigger becomes a one-time exercise: the ratios freeze, the trend column stops meaning anything, and within two cycles the register is quoted as history rather than used as a queue.

## When this method misleads you

The ratio is a fraction of two estimates, and interest is the softer one by a distance. Guess it, and the ranking is a popularity contest with a decimal point on it; the discipline that saves the sheet is mechanical, in that interest comes from last quarter's tagged tickets and on-call hours or the figure is labeled ILLUSTRATIVE with a date to measure. The second failure is shared cost: one team scores the tickets it can see, four teams pay the item, and the row that hurts the organisation most lands mid-table. That is what the teams-paying column is for, and the sheet is worth little without it. The third is social. Put a name in a reckless cell once, and every future row is filed inadvertent and prudent, the process signal disappears, and what is left is a schedule pretending to be a diagnosis. The fourth is the word itself: stretch the metaphor to code that was never a loan and "debt" becomes the term for everything anyone dislikes about the codebase, at which point the interest total is fiction and the budget funds tidying while the audit query still scans the whole history. Cunningham's third question is the gate that holds this back, and it only holds if you actually ask it. Last, the arithmetic assumes the interest is paid indefinitely; on a system with a dated sunset, multiply interest by the quarters remaining before comparing it with principal, or the sheet will cheerfully schedule a rebuild of something about to be switched off.

## Feeds

- [Tech debt register](../../templates/execution/tech-debt-register.md), which is the durable artifact this sheet fills, and the [capacity plan](../../templates/planning/capacity-plan.md), which takes its total
- [WSJF and cost of delay](../prioritization/wsjf-cost-of-delay.md), when debt rows compete with feature rows for the same cycle rather than for a ring-fenced budget
- [Estimation sheet](../execution/estimation-sheet.md) for every principal range, and the [risk matrix](../execution/risk-matrix.md) for the items whose failure mode is an event rather than a drag
- [Incident postmortem](../../templates/operate/incident-postmortem.md) and [ADR](../../templates/architecture/adr.md), which feed rows in; the [spec review skill](../../skills/spec-review/SKILL.md), which catches the next one before it is written
- Method background: [Shape Up](../../knowledge/shape-up.md) on fixed appetite, and the [architect agent](../../agents/architect-agent.md), which owns the architecture set this sheet reports against
