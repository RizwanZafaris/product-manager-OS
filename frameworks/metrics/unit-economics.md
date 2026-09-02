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
- The retention plateau from the [cohort table](cohort-retention.md); LTV read from a curve that has not flattened is the sheet's oldest lie

## The worksheet

Every line carries its formula. Fill the source and a confidence rating (high: system of record; medium: derived; low: estimate).

| Line | Quantity | Formula | Value | Source | Confidence |
|---|---|---|---|---|---|
| A | Revenue per account per month | billed revenue / paying accounts | | | |
| B | Variable cost to serve per account per month | (hosting + inference + support + fees) / paying accounts | | | |
| C | Contribution margin per account per month | A minus B | | | |
| D | Contribution margin ratio | C / A | | | |
| E | Monthly logo churn | 1 minus the cohort plateau, converted to a monthly rate; valid only once the curve has flattened | | | |
| F | Expected lifetime (months) | 1 / E | | | |
| G | LTV, contribution basis | C x F | | | |
| H | CAC, per channel | channel spend in the period / new accounts from that channel in the period, with the lag matching the sales cycle | | | |
| I | Payback (months) | H / C | | | |
| J | LTV to CAC | G / H | | | |

Rules: G is built on C, never on A; revenue-based LTV ignores the cost of serving the customer for the whole lifetime. H is computed per channel first; a blended H is allowed only as a second line labelled blended. Expansion revenue goes on a separate line, not folded into A, until it has its own cohort evidence.

### Sensitivity

| Change | Payback (I) | LTV to CAC (J) |
|---|---|---|
| Churn one point higher | | |
| CAC one fifth higher | | |
| Cost to serve one fifth higher | | |

## Reading the result

Payback is the number finance reads first, because it says how long cash is tied up per account; compare it with how long the company can carry that cash, which is the company's hurdle and not an industry rule. The often-quoted three-to-one LTV-to-CAC ratio is a venture rule of thumb, not a law; set your own hurdle with finance and record it in the sheet's header. A channel whose payback exceeds the contract length is paying to lose money. A sensitivity row that flips the decision means the decision rests on an assumption, and that assumption goes into the assumptions register with an owner and an expiry.

## ILLUSTRATIVE example

Invented figures for Ledgerline's expense-report copilot, sold per seat to mid-market accounts.

| Line | Value | Working |
|---|---|---|
| A | $1,150 | monthly billing across paying accounts |
| B | $445 | inference $210, hosting $60, support $140, fees $35 |
| C | $705 | 1,150 minus 445 |
| D | 0.61 | 705 / 1,150 |
| E | 2.0% per month | from a flattened cohort plateau |
| F | 50 months | 1 / 0.02 |
| G | $35,250 | 705 x 50 |
| H, outbound sales | $9,500 | $190,000 in the quarter / 20 new accounts, lagged one quarter |
| H, accounting-firm partners | $4,000 | $48,000 / 12 new accounts |
| H, blended | $7,438 | $238,000 / 32 |
| I, outbound | 13.5 months | 9,500 / 705 |
| I, partners | 5.7 months | 4,000 / 705 |
| J, outbound | 3.7 | 35,250 / 9,500 |
| J, partners | 8.8 | 35,250 / 4,000 |

Sensitivity: churn at 3.0% per month cuts F to 33 months, G to $23,265, and outbound J to 2.4. The partner channel looks better on every line but produced 12 accounts and cannot be scaled by spending more; outbound can. The decision the sheet supports is to fund outbound while it pays back inside the contract term, and to log the churn assumption as the one that decides it.

## The trap

Blended CAC. The blended $7,438 above hides a $9,500 channel that scales and a $4,000 channel that does not. Plans built on the blended number promise that the next hundred accounts cost what the last thirty-two did, and the next hundred come almost entirely from the expensive channel. The companion trap is LTV read from a young curve: at month three, the copilot's cohorts were still losing several points a month, and a lifetime computed from that rate would have been a third of the eventual one, while a lifetime computed from an assumed plateau would have been fiction in the other direction. Wait for the flattening, or carry a range.

## Feeds

- [Business case](../../templates/planning/business-case.md), the costs and benefits lines and the sensitivities
- [Pricing and packaging](../../templates/planning/pricing-packaging.md), section 2, the pricing model
- [Growth plan](../../templates/planning/growth-plan.md), section 2, whether the chosen channel or loop pays back
- [Assumptions register](../../templates/definition/assumptions-register.md), one row per low-confidence line
- [QBR and board update](../../templates/operate/qbr-board-update.md), the unit economics slide
- PLANNING track; the business case is read at [Gate 1](../../os/STAGE-GATES.md) and the numbers are retested at Gate 6
- Method background: [cohort retention](cohort-retention.md) for the churn input; the [knowledge index](../../knowledge/INDEX.md) carries no finance card, so the source above is the reference
