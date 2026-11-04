---
layer: frameworks
stage: PLANNING
gate: null
feeds: ["templates/planning/portfolio-review.md", "templates/planning/roadmap.md", "templates/planning/capacity-plan.md", "templates/planning/business-case.md"]
method: "knowledge/INDEX.md"
aliases: ["Portfolio allocation", "portfolio-allocation"]
---
# Portfolio allocation

Based on two sources. The three horizons come from Mehrdad Baghai, Stephen Coley and David White, The Alchemy of Growth (1999). The core, adjacent and transformational split comes from Bansi Nagji and Geoff Tuff, "Managing Your Innovation Portfolio", Harvard Business Review (2012). Explained here in this repository's own words. The distance score, the evidence-level tranche caps, the move limit and the review cadence below are this repository's own conventions; neither source sets them.

## What it is for

Deciding how one pool of people or money is split across bets of different maturity, and then keeping the split honest from one review to the next. Two lenses do different jobs. The horizons sort bets by how close they are to earning: Horizon 1 extends and defends the businesses that pay the bills today, Horizon 2 builds businesses that have early customers and need scale, Horizon 3 seeds options that may become businesses later. Baghai, Coley and White's central point is that all three run at the same time, not in sequence, because a company that funds only what earns today has no next business ready when the core flattens. The ambition matrix sorts bets by distance instead: how far each sits from today's products and assets (how to win) and from today's customers and markets (where to play). Core bets improve what exists for the people already served, adjacent bets step out one notch on either axis, transformational bets create a new offer or reach a market the company does not serve. Read it as the [Ansoff matrix](ansoff-matrix.md) with a middle step added on each axis.

This sheet uses distance to place each bet in a horizon, compares the current allocation by horizon with a target, prices the gap, caps each bet's next tranche by the evidence it holds, and fixes when each bet is next judged. The output is a short table a [portfolio review](../../templates/planning/portfolio-review.md) can decide from.

On 70/20/10. Nagji and Tuff reported that, among the companies they studied, those allocating roughly 70 percent of innovation investment to core, 20 percent to adjacent and 10 percent to transformational initiatives tended to outperform their peers, and they said themselves that the right mix differs by industry, competitive position and company. It is a pattern reported from one study's sample, not a law and not a default. Use it as a question, "why is our target different from this, and by how much", answered in writing for each horizon.

## Run it when

- Two or more products or bets draw on one pool of people or money, and the split was last set by whoever asked loudest
- A portfolio review is due and nobody can say what share of capacity goes to work that does not earn yet
- A Horizon 3 bet has been "promising" for three periods and still holds its team
- The core has stalled and someone proposes moving half the engineers into new ventures in one go

**Skip it when:** there is one product and one team, or everything the pool can carry is already spoken for by contracts, mandates and run cost. Splitting a pool with no discretionary capacity across horizons is arithmetic on zero; the question there is the [capacity plan](../../templates/planning/capacity-plan.md), not this sheet.

## Inputs you need first

- Every bet and product line that draws on the pool, with what it holds now, from the [capacity plan](../../templates/planning/capacity-plan.md) or finance's cost-centre report
- Fixed work priced in the same unit: security, compliance mandates, platform on-call. It is excluded from the ratio in Part 2
- For each bet, the evidence it actually holds, dated, from the discovery documents, pilots and metrics reviews behind it
- The last review's verdicts, so a kill criterion written then is read now and not rewritten

## The worksheet

### Part 1: place each bet

<!-- Score each axis 0, 1 or 2. Where to play: 0, the customers and markets served today; 1, an adjacent group whose buyer or job overlaps today's (a new segment, the same buyer in a new geography); 2, a market or buyer the company does not serve. How to win: 0, existing products and assets; 1, an incremental addition built mostly from what exists; 2, a new offer or capability the company has not shipped and measured. -->

| Bet or line | Where to play (0 to 2, why) | How to win (0 to 2, why) | Distance | Horizon | Earning at its own target for two reviews? | Final horizon | Scored by |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**Arithmetic.** Distance = the larger of the two axis scores. Horizon = H1 at distance 0, H2 at distance 1, H3 at distance 2. Graduation: a bet that has earned repeatable revenue, or retained usage, at its own stated target for two consecutive reviews moves one horizon inward, whatever its distance. The published matrix draws core, adjacent and transformational as bands across the grid, not by formula. The larger-score rule is this repository's simplification, and it errs toward the further horizon on purpose: a bet misfiled inward gets funded without the evidence bar its distance needs.

"Scored by" names someone outside the team proposing the bet; the trap below says why.

### Part 2: current allocation against target

<!-- One unit for the whole sheet: people, person-weeks, or money for the period. Fixed work is listed once and excluded, because a ratio that includes mandates moves when the auditor calls, not when strategy changes. -->

Total pool: [n] · Fixed work, excluded: [n] · Allocatable = total - fixed: [n] · Unit: [people / person-weeks / money]

| Horizon | Target share (percent) | Why this target and not 70/20/10 | Current units | Current share (percent) | Gap (points) | Gap (units) | Move this period (units) |
|---|---|---|---|---|---|---|---|
| H1 | | | | | | | |
| H2 | | | | | | | |
| H3 | | | | | | | |
| Total | 100 | | | 100 | 0 | 0 | 0 |

**Arithmetic.**

- Current share = current units / allocatable x 100.
- Gap (points) = target share - current share. Gap (units) = gap (points) / 100 x allocatable. The three gaps sum to zero; when they do not, a bet is missing from Part 1 or the current units do not add up to allocatable.
- Move limit: no more than M points of allocatable move between horizons in one period. This repository's default is M = 5. Periods to close = the sum of the positive gaps / M, rounded up. The limit exists because people moved faster than the receiving bets can use them become idle capacity under a new cost-centre code.

### Part 3: size each bet's next tranche by its evidence

<!-- Evidence levels. E0, belief: an argument and no external evidence. E1, problem evidence: the problem observed in the target group, at least the first two parts of the Ansoff band 3 bar (five or more conversations, one named alternative they use today). E2, solution evidence: a prototype test, pilot or concierge run in which target users behaved (paid, switched, came back), not merely said they would. E3, traction: repeatable revenue or retained usage at a stated target for at least one review period. -->

| Bet | Horizon | Evidence level (E0 to E3), with its dated source | Cap for that level | Tranche asked | Tranche granted | Milestone: the evidence that earns the next level | Kill criterion, written now | Next review |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

Tranche caps, this repository's defaults. Edit the numbers to the size of your pool; keep the shape.

| Level | Largest tranche | Length | What it may be spent on |
|---|---|---|---|
| E0 | 2 people | 6 weeks | Discovery only: interviews, data pulls, a fake door |
| E1 | 4 people | One review period of the bet's horizon | Discovery plus a prototype or concierge test |
| E2 | One team, about 8 people | One review period | A pilot built to be kept or thrown away |
| E3 | Sized by a [business case](../../templates/planning/business-case.md) | Per the case | Build and scale |

**Arithmetic.** For each bet, tranche granted is no larger than the cap for its level. For each horizon, the sum of tranches granted is no larger than that horizon's allocation after this period's move. A bet rises at most one level per review. When the capped tranches in a horizon sum to less than its target, the shortfall is not spread over the bets already there: it is lent to another horizon for one period, written down as a loan, and reported at the next review. A horizon that cannot spend its target on evidence-backed bets has a discovery problem, not a funding problem.

### Part 4: review cadence and verdicts

| Horizon | Review period | Read against |
|---|---|---|
| H1 | Every quarter, at the portfolio review | The line's outcome metric and its contribution |
| H2 | Every 8 weeks, or at each milestone, whichever comes first | Adoption or revenue against the bet's own target |
| H3 | At the end of each tranche, at most 8 weeks | The milestone written when the tranche was granted |

One verdict per bet per review, recorded in the [decision log](../../templates/execution/decision-log.md):

- **Continue.** The milestone was met. The bet now holds the level that milestone evidences, and its next tranche is capped at that level.
- **Pivot.** The milestone was missed and the evidence points at a different problem worth testing. The bet restarts as a new row at the E1 cap at most; the old row closes.
- **Kill.** The milestone was missed twice, or the evidence says no. Its people return to the pool at this review, not at the end of the quarter.

One rule catches the slow death none of the three verdicts names: a bet granted three tranches in a row at the same level is killed, or argued afresh in a [decision memo](../../templates/planning/decision-memo.md). By then sponsorship is keeping it alive, not evidence.

## Reading the result

- **H1 far above target and H3 near zero.** The portfolio is being harvested without anyone saying so. Write that choice into the [product strategy](../../templates/planning/product-strategy.md) as a decision, or fund E0 discovery this period. Both are honest; the silence is not.
- **H3 at target and every bet at E0.** The allocation is met and the evidence is not: a lottery budget. The caps should have prevented it, so check whether they were applied.
- **H2 starved while H3 is busy.** The missing middle. H3 bets that work have nowhere funded to grow, so they stall at E2 or get pushed into H1 before they earn. Fund H2 before adding H3 bets.
- **A gap that needs more than three periods at the move limit.** The target describes a different company. Re-set it, or write the change as its own plan with an owner, the way the [product operating model assessment](../assessment/product-operating-model-assessment.md) treats a pressure of 6 or more.
- **A shortfall in the same horizon two reviews running.** Discovery is not producing fundable bets. That is a finding about the discovery cadence, not a reason to raise the caps.

## ILLUSTRATIVE example

Invented, for Tallowmere, a fictional maker of practice software for independent veterinary clinics; every figure is ILLUSTRATIVE. The pool is 90 product and engineering people for the quarter, 10 of them on fixed work (security, compliance and platform on-call), so allocatable = 90 - 10 = 80 people.

Part 1, placement:

| Bet or line | Where to play | How to win | Distance | Horizon |
|---|---|---|---|---|
| Clinic, the practice management suite | 0 | 0 | 0 | H1 |
| Reminders, the paid SMS add-on | 0 | 0 | 0 | H1 |
| Desktop, the on-premise edition | 0 | 0 | 0 | H1 |
| Pay, card payments inside Clinic billing | 0 | 1 | 1 | H2 |
| Owner app, self-booking for pet owners | 2, pet owners are a buyer Tallowmere does not serve | 2, a consumer app, never shipped | 2 | H3 |
| Claims link, claims data sold to pet insurers | 2, insurers are a new buyer | 1, built from Clinic's billing records | 2 | H3 |

Pay earns, but below its own adoption target, so it does not graduate.

Part 2, allocation in people. The target is 75/15/10, not 70/20/10, because Pay is the only H2 line and can put two more people to work this quarter, not ten.

| Horizon | Target share | Current | Current share | Gap (points) | Gap (people) | Move this quarter |
|---|---|---|---|---|---|---|
| H1 | 75 percent | 68 | 85.0 percent | -10.0 | -8 | -4 |
| H2 | 15 percent | 10 | 12.5 percent | +2.5 | +2 | +2 |
| H3 | 10 percent | 2 | 2.5 percent | +7.5 | +6 | +2 |

Current share: 68 / 80 x 100 = 85.0; 10 / 80 x 100 = 12.5; 2 / 80 x 100 = 2.5. Gap in people: -10.0 / 100 x 80 = -8; 2.5 / 100 x 80 = +2; 7.5 / 100 x 80 = +6; the three sum to zero. The positive gaps total 10 points, so at M = 5 closing takes 10 / 5 = 2 quarters. This quarter moves 5 points, which is 5 / 100 x 80 = 4 people: two from Reminders and two from Desktop leave H1, two join Pay, two join H3.

Part 3, sizing. After the move H3 holds 4 people, against a target of 8.

| Bet | Level | Cap | Asked | Granted | Kill criterion |
|---|---|---|---|---|---|
| Owner app | E1: seven owner interviews, phone booking named as the alternative, front-desk tickets asking for self-booking | 4 people | 4 | 3 | Fewer than 10 percent of invited owners book through the app at least once during a six-week, three-clinic pilot |
| Claims link | E0: one insurer's interest at a trade conference | 2 people, 6 weeks | 2 | 1 | No insurer shares its claim format within the tranche |

Granted: 3 + 1 = 4, inside H3's allocation of 4. The owner app asked for its full cap and got 3 because the move limit, not its evidence, was the binding constraint; the claims link got 1 so the cheap E0 question starts now. Even with no move limit, the two caps total 4 + 2 = 6 people, two short of the target of 8. That shortfall is a discovery problem no reallocation fixes this quarter, and it goes into the review as an open item with an owner.

## The trap

Relabeling to hit the ratio. When a target says 10 percent transformational, the fastest way to meet it is to rename core work: a scheduling improvement for existing clinics becomes "AI scheduling", gets filed in H3, the share rises, and nothing new is being learned. The tell: an H3 bet whose Part 1 "why" cells describe a change to an existing product for existing customers, whose evidence plan names only those customers, or which already holds a committed date in the roadmap's Now column. The rule: someone outside the proposing team sets the Part 1 scores from the two definitions above Part 1, before Part 2 is computed, and a bet's horizon is never edited after anyone has seen the allocation.

The quieter version is copying 70/20/10 with the reason column blank. A target nobody can justify per horizon gets met by relabeling, because the number is the only thing anyone was asked to hit.

## Feeds

- [Portfolio review](../../templates/planning/portfolio-review.md): Part 2 is its investment-by-horizon section, Parts 3 and 4 its bets table
- [Roadmap](../../templates/planning/roadmap.md): at portfolio level, which bets enter Now and which wait in Parked
- [Capacity plan](../../templates/planning/capacity-plan.md): every move between horizons is a supply change for the teams involved
- [Business case](../../templates/planning/business-case.md): required for any E3 tranche, which the caps do not size
- [Ansoff matrix](ansoff-matrix.md): its band 3 evidence bar is this sheet's E1 level, and its four cells are a coarser Part 1
- [Decision log](../../templates/execution/decision-log.md) for every verdict, and the [sunset plan](../../templates/operate/sunset-eol-plan.md) when a killed line still has customers
- PLANNING track, reviewed on its own cadence rather than at a gate
- Method background: no knowledge card exists for either source; see the [knowledge index](../../knowledge/INDEX.md)
