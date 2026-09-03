---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["templates/planning/business-case.md", "templates/planning/pricing-packaging.md", "templates/planning/growth-plan.md"]
method: ""
aliases: ["Unit Economics", "unit-economics"]
---
# Unit Economics

Based on the ideas of David Skok, from the "SaaS Metrics 2.0" essays on forEntrepreneurs (2013), with contribution margin taken from standard managerial accounting. Explained here in this repository's own words.

## What it is for

Whether one customer pays back what it cost to win and serve them, and how fast. Four numbers: contribution margin per account per period, customer acquisition cost (CAC), lifetime value (LTV), and payback period. Every growth plan, pricing change, and business case rests on these four whether or not anyone wrote them down; this sheet writes them down with the formula beside each value, so the arithmetic can be checked and the assumptions can be argued about separately from the conclusion.

## Run it when

- Writing a business case, before the benefits column gets a number
- Deciding whether a channel can be scaled, or whether a free tier is affordable
- Pricing and packaging work, to see what a price change does to payback
- A board update needs to say the growth is paid for

**Skip it when:** there are fewer than a handful of paying accounts or fewer than two completed retention periods. Every line would be an assumption, and a sheet full of assumptions with decimals launders guesses into facts. Put the guesses in the assumptions register with an expiry date and come back.

## Inputs you need first

- Billed revenue per account per period, from the billing system
- Variable cost to serve per account: hosting, model inference, support time, payment fees, from finance
- Sales and marketing spend by channel and period, and new accounts by channel and period, lagged by the sales cycle
- The survival curve from the [cohort table](cohort-retention.md), not just its plateau: you need the month-by-month retention inside the flat region to get a monthly rate out of it, plus the oldest cohort age actually observed
- The contract term, from the standard agreement, because it sets how far this sheet is allowed to forecast; LTV read from a curve that has not flattened, or run past the horizon, is the sheet's oldest lie

## The worksheet

Every line carries its formula. Fill the source and a confidence rating (high: system of record; medium: derived; low: estimate).

Two numbers go in the sheet's header before any line is filled, beside the LTV-to-CAC hurdle agreed with finance:

| Header field | Value | Rule |
|---|---|---|
| Contract term | | from the standard agreement |
| Horizon (months) | | may not exceed the oldest cohort age you have actually observed plus one contract term |

The horizon is what makes line F an estimate rather than an extrapolation. Everything past it is a forecast, and this sheet does not price forecasts.

| Line | Quantity | Formula | Value | Source | Confidence |
|---|---|---|---|---|---|
| A | Revenue per account per month | billed revenue / paying accounts | | | |
| B | Variable cost to serve per account per month | (hosting + inference + support + fees) / paying accounts | | | |
| C | Contribution margin per account per month | A minus B | | | |
| D | Contribution margin ratio | C / A | | | |
| E | Monthly logo churn, tail hazard | 1 minus (retention at month m+1 / retention at month m), read inside the flat region of the cohort curve and averaged across it; valid only once the curve has flattened | | | |
| F | Expected lifetime (months) | the lower of 1 / E and the horizon | | | |
| G | LTV, contribution basis | C x F | | | |
| H | CAC, per channel | channel spend in the period / new accounts from that channel in the period, with the lag matching the sales cycle | | | |
| I | Payback (months) | H / C | | | |
| J | LTV to CAC | G / H | | | |

Rules: E is a rate and the plateau is not. The plateau is a level, the share of a cohort still present once the curve flattens; 1 minus the plateau is the cumulative loss spread across all the months the decay took. Using it as a monthly rate compresses that whole decay into one month and collapses the lifetime by roughly the number of months it ran, so a healthy 56 percent plateau reads as 44 percent monthly churn and a lifetime near two months. Take the rate from consecutive months inside the flat region instead. F states its model openly: 1 / E is the mean lifetime of a survival curve whose monthly hazard stays at E, which is an assumption about the future shape of a curve you have only observed to the horizon minus one contract term, and the cap at the horizon is what keeps the assumption from doing the work. G is built on C, never on A; revenue-based LTV ignores the cost of serving the customer for the whole lifetime. H is computed per channel first; a blended H is allowed only as a second line labelled blended. Expansion revenue goes on a separate line, not folded into A, until it has its own cohort evidence.

### Sensitivity

| Change | Payback (I) | LTV to CAC (J) |
|---|---|---|
| Tail churn (E) one point higher | | |
| Horizon one contract term shorter | | |
| CAC one fifth higher | | |
| Cost to serve one fifth higher | | |

The horizon row is there because it is often the binding one. While 1 / E sits above the horizon, a churn change moves nothing at all and the LTV is a statement about how far you chose to forecast. Run both rows and see which one the decision actually rests on.

## Reading the result

Payback is the number finance reads first, because it says how long cash is tied up per account; compare it with how long the company can carry that cash, which is the company's hurdle and not an industry rule. The often-quoted three-to-one LTV-to-CAC ratio is a venture rule of thumb, not a law; set your own hurdle with finance and record it in the sheet's header. A channel whose payback exceeds the contract length is betting on the renewal, and the sheet should say that out loud, because every month of LTV past the first term rests on the renewal assumption rather than on anything billed. A channel whose payback exceeds the horizon is paying to lose money on any evidence this sheet holds. Report G with the horizon beside it always; an LTV quoted without its horizon is a number whose size the author chose. A sensitivity row that flips the decision means the decision rests on an assumption, and that assumption goes into the assumptions register with an owner and an expiry.

## ILLUSTRATIVE example

Invented figures for Ledgerline's expense-report copilot, sold per seat to mid-market accounts on a 12-month agreement. The cohort curve is the one in the [cohort table](cohort-retention.md) example, read a further seven months on, so the oldest cohort has been observed to month 12.

Header: contract term 12 months; horizon, 24 months (12 observed plus one term); LTV-to-CAC hurdle set with finance at 3.

| Line | Value | Working |
|---|---|---|
| A | $1,150 | monthly billing across paying accounts |
| B | $445 | inference $210, hosting $60, support $140, fees $35 |
| C | $705 | 1,150 minus 445 |
| D | 0.61 | 705 / 1,150 |
| E | 1.6% per month | tail hazard: the flat region holds 56% at month 5 and 50% at month 12, so the monthly survival ratio is (50 / 56) to the power of one seventh, 0.984, and E is 1 minus that |
| F | 24 months | 1 / 0.016 is 62.5 months under a constant hazard, capped at the 24-month horizon |
| G | $16,920 | 705 x 24 |
| H, outbound sales | $9,500 | $190,000 in the quarter / 20 new accounts, lagged one quarter |
| H, accounting-firm partners | $4,000 | $48,000 / 12 new accounts |
| H, blended | $7,438 | $238,000 / 32 |
| I, outbound | 13.5 months | 9,500 / 705 |
| I, partners | 5.7 months | 4,000 / 705 |
| J, outbound | 1.8 | 16,920 / 9,500 |
| J, partners | 4.2 | 16,920 / 4,000 |

Sensitivity, horizon held at 24 months: tail churn one point higher, 2.6% per month, gives 1 / 0.026 = 38.5 months, still past the horizon, so F stays 24 and G, I and J do not move at all. Churn only begins to bite once 1 / E falls under the horizon, which is E above 4.2% per month (1 / 24 = 0.042). Cut the horizon instead to one contract term, 12 months, and G falls to 705 x 12 = $8,460, outbound J to 8,460 / 9,500 = 0.9, partner J to 8,460 / 4,000 = 2.1. CAC one fifth higher takes outbound CAC to $11,400, payback to 11,400 / 705 = 16.2 months and J to 16,920 / 11,400 = 1.5. Cost to serve one fifth higher takes B to $534 and C to $616, payback to 9,500 / 616 = 15.4 months and J to (616 x 24) / 9,500 = 1.6.

What the sheet supports: outbound payback of 13.5 months does not fit inside the 12-month term, so outbound is funded on the strength of the first renewal rather than the first contract, and at 1.8 it sits under the hurdle of 3 that finance set. The 1.6% tail hazard is the whole evidence for that renewal, and the horizon is the assumption that decides the channel, which the churn row above would never have revealed. The partner channel pays back in 5.7 months, inside the term, but produced 12 accounts and cannot be scaled by spending more.

## The trap

Blended CAC. The blended $7,438 above hides a $9,500 channel that scales and a $4,000 channel that does not. Plans built on the blended number promise that the next hundred accounts cost what the last thirty-two did, and the next hundred come almost entirely from the expensive channel. The companion trap is a lifetime read off the wrong part of the curve, and it misses in both directions. Read it off the young end: the cohort fell from 63% to 58% between months 2 and 3, which is 5 of the 63 still there, 7.9% in that month, and 1 / 0.079 = 12.6 months, about half the horizon-capped answer. Read the plateau itself as a rate, which is the error this worksheet used to instruct: 1 minus a plateau of 0.56 is 0.44, and 1 / 0.44 = 2.3 months, a ten-week lifetime for a product whose cohorts are still 56% alive at month 5. Neither is the tail hazard. Measure the rate between consecutive months inside the flat region, cap it at a stated horizon, or carry a range.

## Feeds

- [Business case](../../templates/planning/business-case.md), the costs and benefits lines and the sensitivities
- [Pricing and packaging](../../templates/planning/pricing-packaging.md), section 2, the pricing model
- [Growth plan](../../templates/planning/growth-plan.md), section 2, whether the chosen channel or loop pays back
- [Assumptions register](../../templates/definition/assumptions-register.md), one row per low-confidence line
- [QBR and board update](../../templates/operate/qbr-board-update.md), the unit economics slide
- PLANNING track; the business case is read at [Gate 1](../../os/STAGE-GATES.md) and the numbers are retested at Gate 6
- Method background: [cohort retention](cohort-retention.md) for the survival curve that line E's tail hazard is measured from; the [knowledge index](../../knowledge/INDEX.md) carries no finance card, so the source above is the reference
