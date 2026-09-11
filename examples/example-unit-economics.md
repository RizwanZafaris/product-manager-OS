# Unit Economics: RouteNest Dispatch Console

Fills [frameworks/metrics/unit-economics.md](../frameworks/metrics/unit-economics.md). Everything here is invented: RouteNest is a fictional logistics software company, Dispatch Console is its fictional product, Maya Chen and Tomas Reed are fictional people, and every figure is ILLUSTRATIVE, built to show the worksheet and arithmetic rather than to suggest a real benchmark.

**Owner:** Maya Chen (ILLUSTRATIVE) · **Date:** 2027-03-15 (ILLUSTRATIVE)

**Context, ILLUSTRATIVE:** RouteNest sells Dispatch Console to small delivery firms on a six-month agreement. Maya Chen is the product manager, Tomas Reed is the finance lead, and Nia Brooks is the growth lead. At the review date, 80 paying accounts have been billed for the current month. Product analytics has observed one cohort through month 8, with retention at 64%, 62%, 60%, and 58% in months 5, 6, 7, and 8. Those are the first four months inside the observed tail region. The observed cohort has cleared one full six-month term plus two more months of tail data, enough consecutive tail-region points to read a monthly rate, which is what makes this worksheet usable here, but the horizon remains capped at the oldest observed cohort age plus one contract term.

## What it is for

Whether one customer pays back what it cost to win and serve them, and how fast. Four numbers: contribution margin per account per period, customer acquisition cost (CAC), lifetime value (LTV), and payback period. Every growth plan, pricing change, and business case rests on these four whether or not anyone wrote them down; this sheet writes them down with the formula beside each value, so the arithmetic can be checked and the assumptions can be argued about separately from the conclusion. The method is based on the ideas of David Skok, from the "SaaS Metrics 2.0" essays on forEntrepreneurs (2013), with contribution margin taken from standard managerial accounting.

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
- The survival curve from the [cohort table](../frameworks/metrics/cohort-retention.md), not just its plateau: month-by-month retention inside the flat region is needed to get a monthly rate out of it, plus the oldest cohort age actually observed
- The contract term, from the standard agreement, because it sets how far this sheet is allowed to forecast; LTV read from a curve that has not flattened, or run past the horizon, is the sheet's oldest lie

For Dispatch Console, the billing, finance, and acquisition inputs are:

| Input | Value | Source | Confidence |
|---|---:|---|---|
| Current-month billed revenue | $24,000 | RouteNest billing system for 80 paying accounts | High |
| Paying accounts | 80 | RouteNest billing system | High |
| Hosting cost | $2,400 | Finance cost report for the month | High |
| Inference cost | $3,200 | Finance cost report for the month | High |
| Support cost | $1,600 | Finance cost report for the month | High |
| Payment fees | $800 | Finance cost report for the month | High |
| Direct sales spend | $18,000 | Growth report, one sales cycle before the accounts closed | High |
| New direct-sales accounts | 12 | CRM, matched to the same sales cycle | High |
| Partner referral spend | $6,000 | Growth report, one sales cycle before the accounts closed | High |
| New partner-referral accounts | 8 | CRM, matched to the same sales cycle | High |
| Retention at month 5 | 64% | Product analytics cohort curve | High |
| Retention at month 6 | 62% | Product analytics cohort curve | High |
| Retention at month 7 | 60% | Product analytics cohort curve | High |
| Retention at month 8 | 58% | Product analytics cohort curve | High |
| Contract term | 6 months | Standard customer agreement | High |
| Oldest cohort age observed | 8 months | Product analytics cohort curve | High |

## The worksheet

Every line carries its formula. The source and confidence rating are included for each value. High means system of record, medium means derived, and low means estimated.

The horizon cannot exceed the oldest cohort age actually observed plus one contract term:

- Oldest cohort age observed = 8 months
- Contract term = 6 months
- Horizon = 8 + 6 = **14 months**

The horizon is what makes line F an estimate rather than an extrapolation. Everything past it is a forecast, and this sheet does not price forecasts.

Two header numbers sit beside the LTV-to-CAC hurdle agreed with finance:

| Header field | Value | Rule |
|---|---:|---|
| Contract term | 6 months | From the standard agreement |
| Horizon (months) | 14 months | 8 observed months + 6 month contract term = 14 months |
| LTV-to-CAC hurdle | 3 | Hurdle set with Tomas Reed, finance lead (ILLUSTRATIVE) |

| Line | Quantity | Formula | Value | Source | Confidence |
|---|---|---|---:|---|---|
| A | Revenue per account per month | billed revenue / paying accounts | $300 | $24,000 / 80 = $300, billing system | High |
| B | Variable cost to serve per account per month | (hosting + inference + support + fees) / paying accounts | $100 | ($2,400 + $3,200 + $1,600 + $800) / 80 = $8,000 / 80 = $100, finance report | High |
| C | Contribution margin per account per month | A minus B | $200 | $300 - $100 = $200, derived from A and B | Medium |
| D | Contribution margin ratio | C / A | 0.67 | $200 / $300 = 0.6667, rounded to 0.67 | Medium |
| E | Monthly logo churn, tail hazard | 1 minus (retention at month m+1 / retention at month m), read inside the flat region and averaged across it | 3.2% per month | 1 - (58 / 64)^(1 / 3) = 1 - 0.9677 = 0.0323, rounded to 3.2% | Medium |
| F | Expected lifetime (months) | the lower of 1 / E and the horizon | 14 months | 1 / 0.0323 = 31.0 months; lower of 31.0 and 14 = 14 | Medium |
| G | LTV, contribution basis | C x F | $2,800 | $200 x 14 = $2,800 | Medium |
| H | CAC, direct sales | channel spend in the period / new accounts from that channel in the period | $1,500 | $18,000 / 12 = $1,500, growth report and CRM | High |
| H | CAC, partner referrals | channel spend in the period / new accounts from that channel in the period | $750 | $6,000 / 8 = $750, growth report and CRM | High |
| H | CAC, blended | total channel spend / total new accounts | $1,200 | ($18,000 + $6,000) / (12 + 8) = $24,000 / 20 = $1,200, secondary line only | High |
| I | Payback, direct sales | H / C | 7.5 months | $1,500 / $200 = 7.5 months | Medium |
| I | Payback, partner referrals | H / C | 3.8 months | $750 / $200 = 3.75 months, rounded to 3.8 | Medium |
| I | Payback, blended | H / C | 6.0 months | $1,200 / $200 = 6 months | Medium |
| J | LTV to CAC, direct sales | G / H | 1.9 | $2,800 / $1,500 = 1.8667, rounded to 1.9 | Medium |
| J | LTV to CAC, partner referrals | G / H | 3.7 | $2,800 / $750 = 3.7333, rounded to 3.7 | Medium |
| J | LTV to CAC, blended | G / H | 2.3 | $2,800 / $1,200 = 2.3333, rounded to 2.3 | Medium |

The retention evidence is taken from consecutive months inside the observed tail region rather than from the plateau level:

- Month 5 to month 6 survival ratio = 62 / 64 = 0.96875
- Month 6 to month 7 survival ratio = 60 / 62 = 0.96774
- Month 7 to month 8 survival ratio = 58 / 60 = 0.96667
- Combined three-month survival ratio = 58 / 64 = 0.90625
- Monthly survival ratio = 0.90625^(1 / 3) = 0.9677
- Tail hazard E = 1 - 0.9677 = 0.0323, or 3.2% per month

The plateau is a level, not a monthly churn rate. The observed tail moves from 64% to 58% across three months, so the tail hazard is calculated from the consecutive-month movement. Because 1 / E is 31.0 months and the horizon is 14 months, line F is capped at 14 months.

### Sensitivity

| Change | Payback (I) | LTV to CAC (J) |
|---|---:|---:|
| Tail churn (E) one point higher | Direct: $1,500 / $200 = 7.5 months; partner: $750 / $200 = 3.8 months | Direct: $2,800 / $1,500 = 1.9; partner: $2,800 / $750 = 3.7 |
| Horizon one contract term shorter | Direct: $1,500 / $200 = 7.5 months; partner: $750 / $200 = 3.8 months | Direct: $1,600 / $1,500 = 1.1; partner: $1,600 / $750 = 2.1 |
| CAC one fifth higher | Direct: $1,800 / $200 = 9.0 months; partner: $900 / $200 = 4.5 months | Direct: $2,800 / $1,800 = 1.6; partner: $2,800 / $900 = 3.1 |
| Cost to serve one fifth higher | New B = $100 x 1.2 = $120; new C = $300 - $120 = $180. Direct: $1,500 / $180 = 8.3 months; partner: $750 / $180 = 4.2 months | New G = $180 x 14 = $2,520. Direct: $2,520 / $1,500 = 1.7; partner: $2,520 / $750 = 3.4 |

For the tail churn sensitivity:

- New E = 3.2% + 1.0% = 4.2%
- 1 / 0.042 = 23.8 months
- The lower of 23.8 and the 14-month horizon remains 14 months
- Therefore G remains $2,800, so payback and LTV to CAC do not move

For the shorter horizon sensitivity:

- One contract term shorter = 14 - 6 = 8 months
- New F = 8 months
- New G = $200 x 8 = $1,600

The horizon row is binding before the one-point churn row. With the current observed hazard, a one-point increase in churn does not change the capped lifetime, while shortening the horizon reduces LTV immediately.

## Reading the result

Payback is the number finance reads first, because it says how long cash is tied up per account; compare it with how long the company can carry that cash, which is the company's hurdle and not an industry rule. The often-quoted three-to-one LTV-to-CAC ratio is a venture rule of thumb, not a law; RouteNest's finance hurdle is 3, recorded in the header.

The partner referral channel pays back in 3.8 months, inside the six-month contract term, and its LTV-to-CAC ratio is 3.7, above the hurdle. Direct sales pays back in 7.5 months, after the six-month term, and its LTV-to-CAC ratio is 1.9, below the hurdle. Direct sales therefore depends on renewal behavior that is not yet observed through the full forecast horizon.

The 3.2% tail hazard is derived from the observed month 5 to month 8 movement. The 14-month horizon is the controlling assumption because it caps expected lifetime below the 31.0-month constant-hazard result. The result should be reported as "$2,800 contribution-basis LTV at a 14-month horizon", not as an uncapped lifetime number.

The blended CAC of $1,200 is not the decision number. It hides direct sales CAC of $1,500 and partner referral CAC of $750. The next account should not be assumed to cost $1,200 unless the channel mix is expected to remain the same.

The sensitivity rows show two decision risks:

- A one-point tail-churn increase does not change the result while the horizon remains binding.
- A horizon shortened by one contract term drops direct-sales LTV to $1,600 and its ratio to 1.1.

The assumptions register should carry the medium-confidence hazard, lifetime cap, and LTV lines with an owner and expiry. Tomas Reed owns the next finance review, and Maya Chen owns the cohort check.

## ILLUSTRATIVE example

RouteNest's Dispatch Console is sold on a six-month agreement. The observed cohort has reached month 8, so the horizon is 14 months:

- Contract term = 6 months
- Oldest observed cohort age = 8 months
- Horizon = 8 + 6 = 14 months
- Finance LTV-to-CAC hurdle = 3

| Line | Value | Working |
|---|---:|---|
| A | $300 | $24,000 billed revenue / 80 paying accounts = $300 |
| B | $100 | ($2,400 hosting + $3,200 inference + $1,600 support + $800 fees) / 80 = $8,000 / 80 = $100 |
| C | $200 | $300 - $100 = $200 |
| D | 0.67 | $200 / $300 = 0.6667, rounded to 0.67 |
| E | 3.2% per month | 1 - (58 / 64)^(1 / 3) = 1 - 0.9677 = 0.0323 |
| F | 14 months | 1 / 0.0323 = 31.0 months; lower of 31.0 and 14 = 14 |
| G | $2,800 | $200 x 14 = $2,800 |
| H, direct sales | $1,500 | $18,000 / 12 = $1,500 |
| H, partner referrals | $750 | $6,000 / 8 = $750 |
| H, blended | $1,200 | ($18,000 + $6,000) / (12 + 8) = $24,000 / 20 = $1,200 |
| I, direct sales | 7.5 months | $1,500 / $200 = 7.5 |
| I, partner referrals | 3.8 months | $750 / $200 = 3.75, rounded to 3.8 |
| I, blended | 6.0 months | $1,200 / $200 = 6 |
| J, direct sales | 1.9 | $2,800 / $1,500 = 1.8667, rounded to 1.9 |
| J, partner referrals | 3.7 | $2,800 / $750 = 3.7333, rounded to 3.7 |
| J, blended | 2.3 | $2,800 / $1,200 = 2.3333, rounded to 2.3 |

The partner referral channel meets the finance hurdle:

- Partner LTV to CAC = $2,800 / $750 = 3.7
- Partner payback = $750 / $200 = 3.8 months
- 3.8 months is inside the six-month contract term

The direct-sales channel does not meet the hurdle:

- Direct-sales LTV to CAC = $2,800 / $1,500 = 1.9
- Direct-sales payback = $1,500 / $200 = 7.5 months
- 7.5 months is longer than the six-month contract term

The direct-sales case depends on renewal:

- Payback beyond the first term = 7.5 - 6 = 1.5 months
- The first 6 months recover $200 x 6 = $1,200 of the $1,500 CAC
- Remaining CAC after the first term = $1,500 - $1,200 = $300
- Additional contribution needed after the first term = $300
- Additional time needed = $300 / $200 = 1.5 months

The sheet supports scaling partner referrals before direct sales. Direct sales may still be tested, but its renewal dependency and 1.9 LTV-to-CAC result must be explicit in the business case.

## The trap

Blended CAC. The blended $1,200 hides a $1,500 direct-sales channel and a $750 partner-referral channel. A plan built on the blended number promises that the next accounts cost what the last 20 did, even if most next accounts come from direct sales.

The companion trap is a lifetime read from the wrong part of the curve. The observed cohort is at 64% in month 5 and 58% in month 8. Treating the month 8 level as monthly churn would produce:

- 1 - 0.58 = 0.42, or 42% monthly churn
- 1 / 0.42 = 2.4 months

That is not the tail hazard. It compresses the full decay represented by the retention level into one month.

Using the month 5 to month 8 movement gives the tail hazard instead:

- Three-month survival ratio = 58 / 64 = 0.90625
- Monthly survival ratio = 0.90625^(1 / 3) = 0.9677
- Monthly tail hazard = 1 - 0.9677 = 3.2%
- Uncapped constant-hazard lifetime = 1 / 0.0323 = 31.0 months
- Horizon-capped lifetime = lower of 31.0 and 14 = 14 months

Read the rate between consecutive months inside the observed tail region, cap it at a stated horizon, or carry a range. Do not use the plateau level as if it were a monthly churn rate.

## Feeds

- [Business case](../templates/planning/business-case.md), the costs and benefits lines and the sensitivities
- [Pricing and packaging](../templates/planning/pricing-packaging.md), section 2, the pricing model
- [Growth plan](../templates/planning/growth-plan.md), section 2, whether the chosen channel or loop pays back
- [Assumptions register](../templates/definition/assumptions-register.md), one row per medium-confidence line
- [QBR and board update](../templates/operate/qbr-board-update.md), the unit economics slide
- PLANNING track; the business case is read at [Gate 1](../os/STAGE-GATES.md) and the numbers are retested at Gate 6
- Method background: [cohort retention](../frameworks/metrics/cohort-retention.md) for the survival curve that line E's tail hazard is measured from; the [knowledge index](../knowledge/INDEX.md) carries no finance card, so the source above is the reference
