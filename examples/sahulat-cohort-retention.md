# Cohort Retention: Sahulat Bill Pay, July and August cohorts

Fills [frameworks/metrics/cohort-retention.md](../frameworks/metrics/cohort-retention.md). Everything here is invented and every number is ILLUSTRATIVE: Sahulat, its people, agents, customers, billers, bank, aggregator and telco are fiction, and the values below were chosen to show the cohort-retention reading rather than to describe any real wallet or market.

**Owner:** Hira Baig, Product Manager · **Date:** 2026-09-18 · **Review:** 2026-09-21 · **Query:** CH-01 · **Product:** Sahulat bill pay · **Supplement:** [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md)

**Annotation, 2026-09-20:** the September partial cells below (July P2 and August P1) were pulled from CH-01 through 2026-09-20, two days after this worksheet's stated Date. The read was prepared on 2026-09-17 and 2026-09-18 for the 2026-09-21 review, and the September cutoff was extended to 2026-09-20 before that review without moving the worksheet's own Date field.

## What it is for

This read separates the wallets that first paid a bill in July or August from the calendar volume of bills. It asks whether a wallet that paid its first bill paid again in the next monthly bill cycle. The method is cohort retention, based on cohort analysis as brought into product work by Eric Ries in The Lean Startup (2011).

The active event is a bill payment, not a login, lookup or cash-in. The July cohort has one completed monthly age, with 5,640 of 9,400 wallets paying again in August. Its September cell is partial, with data through 2026-09-20. The August cohort has only a partial September follow-up.

The result is a retention read, not a plateau claim. Two observed ages do not establish a plateau, so no plateau level or plateau arrival period is called. The monthly cohort windows overlap the four-week window in N53, and their counts are never added to N53's 24,600 wallets or 31,200 bills.

## Run it when

- After the first bill-pay launch cohorts have at least one completed monthly follow-up.
- Before interpreting higher bill volume as a growing retained customer base.
- When the team needs to separate first-time bill payers from wallets that return for another bill.
- When comparing first-payment funding paths on the same cohort and age.

**Skip the plateau test when:** the current period is partial or the cohorts have fewer than the completed ages needed to show a curve. This read does not call a plateau because July has one completed follow-up and one partial follow-up, while August has one partial follow-up.

## Inputs you need first

- **Active definition:** the wallet paid at least one bill in the monthly bill cycle.
- **Cohort key:** the wallet's first bill payment, dated within the calendar month of that first payment.
- **Period:** calendar month, matching the monthly bill cycle.
- **Segments:** first-payment funding path, specifically cash-in within two hours, balance held over 48 hours, and other.
- **Denominator rule:** the number of wallets in the first-payment cohort. Accounts are not removed for a contract end because no such removal rule is present in CH-01.
- **Source queries:** CH-01 for cohort membership and repeat payment, joined to FP-01 for first-payment funding path.
- **Window note:** the monthly windows overlap N53's four-week window. The two windows are read separately and are never added together.

## The worksheet

### Step 1: definitions

| Field | Answer |
|---|---|
| Active means | The wallet paid at least one Sahulat bill in the monthly bill cycle. |
| Cohort key | The wallet's first bill payment, using the calendar month of that first payment. A lookup, cash-in or login does not create a cohort. |
| Period | Calendar month, matching the monthly bill cycle. |
| Segments to cut | First-payment funding path: cash-in within two hours, balance held over 48 hours, and other. |
| Denominator rule | Cohort size at P0. July uses 9,400 wallets and August uses 23,900 wallets. No contract-ended accounts are removed because CH-01 supplies no such exclusion rule. |
| Query and review | CH-01, prepared for the 2026-09-21 review and read on 2026-09-18. |
| Window relationship | These calendar-month cohorts overlap N53's four-week window. Their wallets and bills are never added to N53. |

### Step 2: the table

Percent of the cohort active in each period after its start. September is partial through 2026-09-20.

| Cohort (start period) | Size | P0 | P1 | P2 | P3 | P4 | P5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| July 2026 | 9,400 | 100 | 60 | 52, partial | | | |
| August 2026 | 23,900 | 100 | 54, partial | | | | |

Arithmetic:

- July P0: 9,400 / 9,400 x 100 = 100 percent.
- July P1: 5,640 / 9,400 x 100 = 60 percent.
- July P2: 4,890 / 9,400 x 100 = 52 percent, partial through 2026-09-20.
- August P0: 23,900 / 23,900 x 100 = 100 percent.
- August P1: 12,900 / 23,900 x 100 = 0.5397, or 54 percent, partial through 2026-09-20.

Flattening test: the July drop from P0 to P1 is 100 minus 60 = 40 percentage points. The apparent drop from P1 to the partial P2 is 60 minus 52 = 8 percentage points, but P2 is incomplete and cannot be used as a completed-period drop. August has no completed follow-up age. Therefore, no plateau level and no plateau arrival period are recorded.

The oldest completed age actually observed is July P1, one monthly follow-up. July P2 is partial, and August P1 is partial. The unit-economics read must not treat 52 percent or 54 percent as a stable retained core or as a monthly rate.

### Step 3: what to compare

| Comparison | What it tells you | Watch out for |
|---|---|---|
| July and August at the same age | July P1 is 60 percent; August P1 is 54 percent partial. This is an early read on whether the newer cohort returns at the same monthly age. | August P1 is partial, and the cohorts have different calendar exposure. Do not call the 6 percentage point difference a product change yet. |
| July cohort by first-payment funding path | Cash-in within two hours retains at 62 percent, other at 54 percent, and balance held over 48 hours at 52 percent at P1. | Funding-path cells are smaller than the full July cohort. The balance-funded cell is 850 wallets, so the comparison is directional. |
| Same funding path across later cohorts | Not yet available from CH-01. The next read should compare the same funding paths once an August cohort follow-up is complete. | Do not compare a July completed age with an August partial age as if both were complete. |
| Monthly cohort read against N53 | The cohort table explains repeat behaviour after first payment, while N53 measures wallets with at least one bill paid in a four-week window. | The windows overlap. Never add cohort wallets or bills to N53's wallets or bills. |
| Plateau level against the lifetime the [unit economics](../frameworks/metrics/unit-economics.md) assumed | Not assessable yet. There are not enough completed ages to support a plateau or a monthly churn rate from a flat region. | A percentage at one partial age is not a plateau and is not a monthly churn rate. |

Funding-path arithmetic for the July cohort:

| July first-payment funding path | P0 size | Paid in August | P1 arithmetic | P1 |
|---|---:|---:|---|---:|
| Cash-in within two hours | 7,300 | 4,530 | 4,530 / 7,300 x 100 = 62.05 percent | 62 percent |
| Balance held over 48 hours | 850 | 440 | 440 / 850 x 100 = 51.76 percent | 52 percent |
| Other | 1,250 | 670 | 670 / 1,250 x 100 = 53.6 percent | 54 percent |
| Total | 9,400 | 5,640 | 5,640 / 9,400 x 100 = 60 percent | 60 percent |

The July funding-path sizes reconcile to the July cohort:

7,300 + 850 + 1,250 = 9,400 wallets.

The August repeat counts also reconcile to the July P1 total:

4,530 + 440 + 670 = 5,640 wallets.

The balance-funded path retains worst at P1, 52 percent, compared with 62 percent for cash-in within two hours and 54 percent for other funding. Its July cohort share is:

850 / 9,400 x 100 = 9.04 percent, shown as 9 percent.

That is consistent with N43's measured 9 percent of bill payments funded from a balance held more than 48 hours. The cash-in-within-two-hours path is:

7,300 / 9,400 x 100 = 77.66 percent, shown as 78 percent, consistent with N44's measured 78 percent.

## Reading the result

The July cohort shows 60 percent repeat payment in the next monthly cycle. Its September value is 52 percent through 2026-09-20, but that period is partial. The August cohort shows 54 percent through 2026-09-20, also partial.

This is not enough evidence for a plateau. July has one completed age and one partial age. August has no completed follow-up age. The honest result is:

- **Observed July P1:** 60 percent.
- **Observed July P2:** 52 percent, partial through 2026-09-20.
- **Observed August P1:** 54 percent, partial through 2026-09-20.
- **Plateau:** not called.
- **Plateau level:** not available.
- **Plateau arrival period:** not available.
- **Oldest completed age:** July P1, one monthly follow-up.

The funding-path cut is the stronger current finding. Balance-funded first payers retain worst at 52 percent in the July P1 read. This is consistent with the measured 9 percent balance-funded share in N43 and the measured 78 percent cash-in-within-two-hours share in N44. It does not establish causation. Funding path may also reflect different customer intent or bill-paying situations.

N57 says the 5th to the 10th of the month carry 44 percent of monthly bill payments. That bill-peak pattern is a calendar effect to monitor when the September cells complete. It is not a reason to fill a missing cohort cell or to treat a partial September as a completed monthly period.

The next read should complete September before using it as a period-to-period comparison, then add a completed follow-up for the August cohort. It should preserve the same monthly definition and keep the cohort table separate from N53's four-week window.

## ILLUSTRATIVE example

This Sahulat read is the worked example. CH-01 groups wallets by their first bill payment, then checks whether each wallet paid again in a later calendar month.

The main table shows an early curve, not a plateau:

| Cohort | Size | P0 | P1 | P2 |
|---|---:|---:|---:|---:|
| July 2026 | 9,400 | 100 | 60 | 52, partial |
| August 2026 | 23,900 | 100 | 54, partial | |

The July cohort's P1 result is:

5,640 repeat payers / 9,400 first payers = 60 percent.

The July cohort's partial September result is:

4,890 repeat payers / 9,400 first payers = 52 percent.

The August cohort's partial September result is:

12,900 repeat payers / 23,900 first payers = 54 percent.

The funding-path cut shows why the aggregate July P1 should not be treated as one homogeneous customer group:

| First-payment path | July cohort share | August repeat rate |
|---|---:|---:|
| Cash-in within two hours | 7,300 / 9,400 = 78 percent | 4,530 / 7,300 = 62 percent |
| Balance held over 48 hours | 850 / 9,400 = 9 percent | 440 / 850 = 52 percent |
| Other | 1,250 / 9,400 = 13 percent | 670 / 1,250 = 54 percent |

The path shares reconcile:

78 percent + 9 percent + 13 percent = 100 percent, subject to displayed rounding.

The repeat counts reconcile:

4,530 + 440 + 670 = 5,640.

This read therefore reports the observed rates and the partial-period status, but does not claim that the curve has flattened.

## The trap

Calling a plateau from two ages, especially when one of the ages is partial. The July P2 value of 52 percent is not a stable retained core, and the August P1 value of 54 percent is not a completed monthly comparison.

A second trap is adding the cohort table to N53. N53 uses the four weeks to 2026-08-16 and reports 24,600 wallets and 31,200 bills. CH-01 uses calendar-month first-payment cohorts, including July and August, and the windows overlap. They answer different questions and are never added together.

A third trap is reading the July aggregate without its funding-path cut. The balance-funded group is 850 of 9,400 July first payers:

850 / 9,400 x 100 = 9 percent, rounded.

Its P1 repeat rate is:

440 / 850 x 100 = 52 percent.

That is below the 62 percent cash-in-within-two-hours rate and the 54 percent other-path rate. It is a useful segmentation finding, not proof that balance funding causes lower retention.

## Feeds

- The 2026-09-21 recurring metrics review, where the July and August cohort movement is read alongside the funnel.
- The [unit economics worksheet](../frameworks/metrics/unit-economics.md), which must wait for completed period-to-period cells before deriving a monthly rate.
- [sahulat-journey.md](sahulat-journey.md), the canonical Sahulat data sheet for N43, N44, N57 and the product context.
- [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md), the supplement for CN32, CN33, CN34 and CH-01.
- The [AARRR funnel worksheet](../frameworks/metrics/aarrr-funnel.md), which uses four-week windows. Its window and this monthly cohort read overlap and must remain separate.
- The [metrics review template](../templates/operate/metrics-review.md), for the review on 2026-09-21.
- Method background: [Lean Startup entry in the knowledge index](../knowledge/INDEX.md).
