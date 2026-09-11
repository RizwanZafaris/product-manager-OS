# Market sizing: Sahulat bill-pay fee revenue

Fills [frameworks/strategy/market-sizing.md](../frameworks/strategy/market-sizing.md). Everything here is invented and every number is ILLUSTRATIVE: Sahulat, its people, agents, customers, billers, bank, aggregator and telco are fiction, and the figures are taken from the Sahulat data sheets to show a defensible worksheet, not to describe a real market.

**Owner:** Hira Baig, Product Manager · **Date:** 2026-03-03 · **Stage:** PLANNING · **Position:** Between the vision and the north star sheet

## What it is for

This sheet sizes Sahulat's annual bill-pay fee revenue at PKR 7 net per bill, using both a top-down account population and a bottom-up wallet and bill count. It is a planning input for the opportunity, not the source of the one-pager's M1 target.

The source data is in [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md). The market-sizing arithmetic is recorded as CN9 in the coverage sheet.

## Run it when

- The vision needs a revenue ceiling and reachable field for Sahulat bill pay.
- The product strategy needs a countable market before the north star sheet is finalized.
- The business case needs an annual fee-revenue range.
- The pricing input is available from the BillBridge rate card.

**Skip it when:** the segment cannot be described precisely enough to count. Here, the segment is domestic electricity and gas accounts billed by Ravi Power and Chenab Gas in districts with an active Sahulat agent.

## Inputs you need first

- **Segment:** Domestic electricity and gas accounts billed by Ravi Power and Chenab Gas in districts with an active Sahulat agent, from CN5.
- **Unit:** Bills, counted as annual bill transactions. The account and wallet rows are used as population proxies, with 12 bills per account per year in the top-down calculation and 24 bills per wallet per year in the bottom-up calculation.
- **Price:** PKR 7 net per bill through BillBridge, from N32.
- **Top-down population:** 3,100,000 accounts, CN5.
- **Top-down filters:** 0.16 reachability, CN6, and 0.25 obtainability by 2026-12-31, CN7.
- **Bottom-up population:** 246,000 Shazia-type wallets, N64.
- **Bottom-up SOM capacity:** 60,000 wallets, CN8.
- **SOM horizon:** The board's 2026 year end, 2026-12-31, from N4.

## The worksheet

### Part 1: market definition

| Field | Answer |
|---|---|
| Job or category | Pay a household electricity or gas bill |
| Segment | Domestic electricity and gas accounts billed by Ravi Power and Chenab Gas in districts with an active Sahulat agent |
| Geography | Districts with an active Sahulat agent |
| Revenue period | One year, annual bill-pay fee revenue |
| SOM horizon | Through 2026-12-31, the board's year end in N4. SOM is the annual revenue run-rate reached at that date |
| Unit | Bill transaction |
| Price per unit per year | PKR 7 net per bill, annualized by the number of bills. Source: N32, BillBridge rate card, 2026-02-10 |

The revenue period is one year, while the SOM horizon ends on 2026-12-31. TAM, SAM and SOM are therefore annual revenue run-rates, not cumulative revenue through the horizon.

### Part 2: top-down

| Step | Population or filter | Value | Value is | Source (URL, date) or AS-id | Confidence |
|---|---|---:|---|---|---|
| Total population, this unit | Domestic electricity and gas accounts in the defined segment | 3,100,000 accounts | a count of units | CN5, BillBridge rate-card meeting, 2026-02-10; recorded in [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md) | Assumption |
| Price per unit per year, from Part 1 | Net Sahulat revenue per bill | PKR 7 per bill | currency per bill | N32, BillBridge rate card, 2026-02-10; recorded in [sahulat-journey.md](sahulat-journey.md) | Quoted |
| TAM (population times price) | 3,100,000 accounts x 12 bills per year x PKR 7 | **PKR 260.4 million per year** | currency per year | CN9 arithmetic, based on CN5 and N32 | Estimate |
| Filter: share reachable with our product, channel, geography | Active Sahulat wallet household share | 0.16 | a share, 0 to 1 | CN6, Hira Baig, from N2 against CN5; recorded in [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md) | Assumption |
| SAM (TAM times the reachability filter) | PKR 260.4 million x 0.16 = PKR 41.664 million, rounded to PKR 41.7 million | **PKR 41.7 million per year** | currency per year | CN9 arithmetic, based on CN5, CN6 and N32 | Estimate |
| Filter: share obtainable by the end of the SOM horizon, given capacity and competition | Obtainable share of SAM by 2026-12-31 | 0.25 | a share, 0 to 1 | CN7, Hira Baig; recorded in [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md) | Assumption |
| SOM (SAM times the obtainability filter) | PKR 41.664 million x 0.25 = PKR 10.416 million, rounded to PKR 10.4 million | **PKR 10.4 million per year, at 2026-12-31** | currency per year, at the end of the horizon | CN9 arithmetic, based on CN6, CN7 and N32 | Estimate |

The top-down TAM uses the CN9 convention of 12 bills per account per year. The top-down SAM arithmetic before rounding is PKR 260.4 million x 0.16 = PKR 41.664 million. The top-down SOM arithmetic before rounding is PKR 41.664 million x 0.25 = PKR 10.416 million.

### Part 3: bottom-up

| Factor | Value | Value is | Source or AS-id | Confidence |
|---|---:|---|---|---|
| Target accounts on a list we could build today | 246,000 Shazia-type wallets | a count of accounts | N64, query BP-01, February 2026; recorded in [sahulat-journey.md](sahulat-journey.md) | Estimate |
| Units per account (sample size and how it was drawn; 1 when the counting unit is the account itself) | 24 bills per wallet per year, calculated as 2 bills per month x 12 months | units per account | N65 and CN9 opportunity arithmetic; 2 bills per month is the N64 proxy convention | Estimate |
| Price per unit per year, from Part 1 | PKR 7 per bill | currency per bill | N32, BillBridge rate card, 2026-02-10 | Quoted |
| SAM (accounts times units times price) | 246,000 wallets x 2 bills per month x 12 months x PKR 7 = PKR 41,328,000, rounded to **PKR 41.3 million** | currency per year | CN9 arithmetic, based on N64 and N32 | Estimate |
| Accounts the channel can reach and the team can onboard by the end of the SOM horizon | 60,000 wallets | a count of accounts | CN8, Tariq Sohail, 2026-03-03; recorded in [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md) | Estimate |
| SOM (that count times units times price) | 60,000 wallets x 2 bills per month x 12 months x PKR 7 = PKR 10,080,000, rounded to **PKR 10.1 million** | currency per year, at the end of the horizon | CN9 arithmetic, based on CN8 and N32 | Estimate |

The bottom-up method does not compute TAM. It starts with the 246,000-wallet proxy in N64 and applies the 2-bills-per-month convention recorded in N65 and CN9.

### Part 4: reconciliation

**Stated tolerance:** the two SAM figures, and the two SOM figures, must each land within one and a half times of each other.

| Method | TAM (currency per year) | SAM (currency per year) | SOM (currency per year, end of horizon) |
|---|---:|---:|---:|
| Top-down | PKR 260.4 million | PKR 41.7 million | PKR 10.4 million |
| Bottom-up | not computed by this method | PKR 41.3 million | PKR 10.1 million |

**SAM test**

- Higher SAM divided by lower SAM: PKR 41.7 million / PKR 41.3 million = 1.0097, rounded to 1.01.
- 1.01 is inside the 1.5 tolerance.
- Difference: PKR 41.7 million - PKR 41.3 million = PKR 0.4 million.

**SOM test**

- Higher SOM divided by lower SOM: PKR 10.4 million / PKR 10.1 million = 1.0297, rounded to 1.03.
- 1.03 is inside the 1.5 tolerance.
- Difference: PKR 10.4 million - PKR 10.1 million = PKR 0.3 million.

Both tests pass. The SAM comparison is meaningful because it passes before the SOM comparison.

**Decision rule:** take the lower SOM as the base case.

- Base SOM: **PKR 10.1 million annual run-rate at 2026-12-31**.
- Top-down sensitivity: PKR 10.4 million annual run-rate at 2026-12-31.
- SAM range: PKR 41.3 million to PKR 41.7 million per year.
- SOM range: PKR 10.1 million to PKR 10.4 million per year.

The gap is not split. The lower figure is used because the bottom-up method starts from the wallet proxy and an explicit channel capacity estimate. The least certain inputs are N64, the 246,000-wallet proxy, CN6, the 0.16 reachability assumption, CN7, the 0.25 obtainability assumption, and CN8, the 60,000-wallet channel estimate. The reconciliation shares the PKR 7 price from N32, but the population and filter inputs remain distinct.

This worksheet does not set the one-pager's M1 target. M1 is the separate operational target in N42, with baseline 0, target 40,000 bills in the four weeks to 2026-08-16, and actual 31,200. The market-sizing SOM is an annual fee-revenue run-rate at 2026-12-31, not a bill-volume target for the one-pager.

### Part 5: sensitivity

| SOM case | Value (currency per year, end of horizon) | Driven by (the two least certain inputs) |
|---|---:|---|
| Low | PKR 10.1 million | CN8, 60,000-wallet channel estimate; N64, 246,000-wallet proxy |
| Base | PKR 10.1 million | Bottom-up lower-SOM rule, using CN8 and N64 |
| High | PKR 10.4 million | CN6, 0.16 reachability assumption; CN7, 0.25 obtainability assumption |

Arithmetic for the sensitivity range:

- Low and base: 60,000 wallets x 2 bills per month x 12 months x PKR 7 = PKR 10,080,000, rounded to PKR 10.1 million.
- High: 3,100,000 accounts x 12 bills per year x PKR 7 x 0.16 x 0.25 = PKR 10,416,000, rounded to PKR 10.4 million.
- Range width: PKR 10.4 million - PKR 10.1 million = PKR 0.3 million.

## Reading the result

- **Inside tolerance, base case set.** The reconciled annual SOM range is PKR 10.1 million to PKR 10.4 million at 2026-12-31. The base case is the lower figure, PKR 10.1 million annual run-rate, with the CN8 and N64 inputs beside it.
- **Outside tolerance, gap driver named.** Not applicable. SAM is 1.01 times between the methods, and SOM is 1.03 times between the methods, both inside the one-and-a-half-times tolerance.
- **No public source exists for a top-down anchor.** The top-down anchor is not presented as a public statistic. CN5 is an assumption told by BillBridge at the 2026-02-10 rate-card meeting and is labelled accordingly. The bottom-up method is retained as an independent check.
- **SOM exceeds the capacity the team actually has.** The bottom-up SOM uses Tariq Sohail's CN8 estimate of 60,000 wallets the agent channel could bring to paying two bills a month by 2026-12-31. The operational plan must treat that as a capacity estimate, not as proof that the team can onboard the whole segment.

Later reading, dated 2026-08-21: N42 recorded 31,200 bills against the one-pager's 40,000 target for the four weeks to 2026-08-16, while N53 recorded 24,600 wallets paying at least one bill, so this sizing remains a revenue opportunity estimate rather than the source of M1.

## ILLUSTRATIVE example

This Sahulat worksheet is an ILLUSTRATIVE example of the TAM, SAM and SOM method. It uses:

- **TAM:** 3,100,000 accounts x 12 bills x PKR 7 = PKR 260.4 million per year.
- **Top-down SAM:** PKR 260.4 million x 0.16 = PKR 41.664 million, rounded to PKR 41.7 million.
- **Bottom-up SAM:** 246,000 wallets x 2 bills x 12 months x PKR 7 = PKR 41.328 million, rounded to PKR 41.3 million.
- **Top-down SOM:** PKR 41.664 million x 0.25 = PKR 10.416 million, rounded to PKR 10.4 million.
- **Bottom-up SOM:** 60,000 wallets x 2 bills x 12 months x PKR 7 = PKR 10.08 million, rounded to PKR 10.1 million.

The SAM ratio is 41.7 / 41.3 = 1.01. The SOM ratio is 10.4 / 10.1 = 1.03. Both are inside the one-and-a-half-times tolerance. The lower SOM, PKR 10.1 million annual run-rate at 2026-12-31, is the base case.

## The trap

The trap would be to use the 3,100,000-account top-down population as though it were already a Sahulat revenue forecast, or to present PKR 10.4 million as the one-pager's M1 target. The top-down population is an assumption, CN6 and CN7 are assumptions, and CN8 is an estimate. The market-sizing result is a reconciled planning range for annual fee revenue, while M1 is a separate operational bill-volume metric in N42.

## Feeds

- [sahulat-journey.md](sahulat-journey.md): canonical Sahulat data sheet, including N4, N32, N42, N53, N64 and N65
- [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md): supplement, including CN5 to CN9
- [templates/planning/business-case.md](../templates/planning/business-case.md): annual SOM range with the horizon and source inputs
- [templates/planning/product-strategy.md](../templates/planning/product-strategy.md): SAM and segment sizing for where to play
- [templates/planning/gtm-plan.md](../templates/planning/gtm-plan.md): a countable first cohort within the SOM capacity estimate
- PLANNING track, ahead of Gate 1
- Method background: [knowledge/crossing-the-chasm.md](../knowledge/crossing-the-chasm.md), Moore, 1991, on why the beachhead matters before the whole market
