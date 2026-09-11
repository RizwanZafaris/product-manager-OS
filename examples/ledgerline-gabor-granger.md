# Gabor-Granger price ladder: Ledgerline

Fills [frameworks/pricing/gabor-granger.md](../frameworks/pricing/gabor-granger.md).

Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, its customers, its product and every count, price and date are fiction built to show how the worksheet is completed. See the [journey data sheet](ledgerline-journey.md) and [coverage sheet](ledgerline-coverage-sheet.md).

**Owner:** Kwame Boateng, Data Analyst · **With:** Maya Chen, Product Manager · **Date:** 2027-01-11

Based on the ideas of André Gabor and Clive Granger, from their 1966 paper in *Economica* on price as an indicator of quality, the origin of the purchase-intention ladder that carries their names. Explained here in this repository's own words.

## What it is for

This run asks the active Ledgerline add-on accounts whether they would keep the add-on at each price per drafted report when their current term ends. The panel is the same EV-S01 panel used by the [Van Westendorp worksheet](ledgerline-van-westendorp.md), with the unit and ladder expressed in the proposed usage metric.

The shares of definite yes responses form a demand curve. Price multiplied by the number of yes responses forms a revenue index. The revenue peak is $2.40 per drafted report. The plateau is $2.00 to $2.40, using the tolerance set before reading the result. The margin guardrail leaves $2.40 as the only plateau rung that clears the floor.

This result feeds the successor price for the 73 held accounts covered by N93 and the pricing document's re-sign. It does not change EXP-2, whose price and 6.0% success bar were pre-declared. The run also surfaces R7.

## Run it when

- A van Westendorp range exists and the pricing document needs a number for the successor price.
- The offer can be expressed in the unit that will be sold, here dollars per drafted report billed monthly in arrears with no seat charge.
- The same active-account panel can answer at every rung.
- A guardrail has been decided beforehand, here the 60% gross-margin floor on the model line.

## Inputs you need first

- The ledgerline product and its usage unit, per drafted report.
- The EV-S01 panel of active accounts: 79 active accounts were invited, 51 responded, and the Gabor-Granger tabulation retained 45 after cleaning.
- A ladder spanning the acceptable range: $1.60, $2.00, $2.40, $2.80 and $3.20.
- A van Westendorp range of roughly $1.80 to $2.60, with $2.40 inside it.
- A margin floor of 60%, with the quoted model cost of $0.92 per drafted report from N11.
- The pre-declared EXP-2 price and bar, which this worksheet does not revise: $2.40 per drafted report and 6.0% or more activated within 14 days of exposure.

## The worksheet

### 1. Design

| Field | Entry |
|---|---|
| Unit | Dollars per drafted report, billed monthly in arrears, with no seat charge |
| Ladder | $1.60, $2.00, $2.40, $2.80, $3.20, ascending |
| Panel | EV-S01, the active-account panel also used by the Van Westendorp sheet; 51 responded |
| Presentation | Every rung asked in random order |
| Question | “Would keep the add-on at this price when your current term ends” |
| Yes definition | Only “definitely” counted as yes |
| Guardrail | Minimum 60% gross margin on the model line, N49 |
| Tolerance | One part in twenty of the maximum revenue index |

### 2. Cleaning

The Van Westendorp tabulation retained 47 respondents after its ordering clean. For this ladder, 2 respondents who said yes above a no were dropped:

| Starting panel | Excluded | Arithmetic | Analysis panel |
|---|---:|---|---:|
| 47 | 2 respondents with yes above no | 47 minus 2 = 45 | 45 |

The cleaned Gabor-Granger panel is therefore n = 45.

### 3. Demand and revenue table

Revenue index equals price multiplied by the count of definite yes responses. Share equals count of yes divided by 45. Drop equals the previous rung's yes count minus the current rung's yes count.

| Price | Would buy, count | Share | Revenue index | Drop from previous rung |
|---|---:|---:|---:|---:|
| $1.60 | 41 | 41 / 45 = 91% | $1.60 x 41 = 65.6 |  |
| $2.00 | 37 | 37 / 45 = 82% | $2.00 x 37 = 74.0 | 41 - 37 = 4 |
| $2.40 | 32 | 32 / 45 = 71% | $2.40 x 32 = 76.8 | 37 - 32 = 5 |
| $2.80 | 20 | 20 / 45 = 44% | $2.80 x 20 = 56.0 | 32 - 20 = 12 |
| $3.20 | 9 | 9 / 45 = 20% | $3.20 x 9 = 28.8 | 20 - 9 = 11 |

**Decision rule:** the candidate price is the rung with the highest revenue index. The maximum is 76.8 at $2.40.

The tolerance was set beforehand at one part in twenty:

- 76.8 / 20 = 3.84
- Plateau threshold = 76.8 - 3.84 = 72.96
- $2.00 revenue index = 74.0, which is at least 72.96
- $2.40 revenue index = 76.8, which is at least 72.96
- $2.80 revenue index = 56.0, which is below 72.96

The revenue plateau is therefore $2.00 to $2.40.

The van Westendorp range is roughly $1.80 to $2.60. Both plateau rungs are inside that range, so apply the margin guardrail:

- Margin floor: 60%, from N49.
- Model cost: $0.92 per drafted report, from N11.
- Lowest price clearing the floor: $0.92 / 0.40 = $2.30.
- Margin at $2.00: ($2.00 - $0.92) / $2.00 = $1.08 / $2.00, or 54%, below the floor.
- Margin at $2.40: ($2.40 - $0.92) / $2.40 = $1.48 / $2.40, or about 62%, above the floor.

This worksheet's recommended input to the successor-price decision memo (owed by 2027-10-01 per LC33) is $2.40 per drafted report, subject to the pricing document's re-sign. The $2.40 rung is the revenue peak, sits inside the van Westendorp range, and is the only plateau rung that clears the margin floor.

The guardrail also exposes R7:

- Highest model cost at which $2.40 still clears a 60% margin = $2.40 x 0.40 = $0.96.
- The M-009 ceiling is $1.05.
- Margin at the M-009 ceiling = ($2.40 - $1.05) / $2.40 = $1.35 / $2.40, or about 56%.
- Therefore M-009 can breach the 60% margin floor without breaching its own $1.05 ceiling.

## Reading the result

The ladder has a revenue peak at $2.40 and a short plateau from $2.00 to $2.40. The sharpest demand loss occurs after the plateau:

- From $2.40 to $2.80, definite yes responses fall from 32 to 20.
- Drop = 32 - 20 = 12 respondents.
- Share change = 71% - 44% = 27 percentage points.

The lower rung is not selected because its 54% margin is below the 60% floor. The upper rung is not selected because its revenue index is outside the plateau and its demand drop is larger. The choice is therefore $2.40, not because stated intention forecasts 32 purchases, but because it is the highest-revenue rung and survives the pre-declared margin test.

The result informs the successor price for the 73 paid accounts held at $6 per seat for 12 months under N93. It does not report or alter an EXP-2 result. EXP-2 remains the pre-declared single-arm re-offer to about 2,818 to 2,821 S-1 accounts not paying, with success at 6.0% or more activated within 14 days and a kill condition under 4.0%.

Stated intention is an upper bound on actual purchase. The output of this worksheet is the price choice, not a forecast that 71% of held accounts will renew.

R7 remains open with Daniel Okafor as owner. The $0.93 measured M-009 cost is below both the $0.96 cost boundary for the selected price and the $1.05 M-009 ceiling, but the two guardrails do not protect the same margin threshold.

## ILLUSTRATIVE example

This filled worksheet is the ILLUSTRATIVE Ledgerline example. The fictional EV-S01 panel contained 51 respondents, and the cleaned Gabor-Granger panel contained 45.

| Price | Would buy | Share arithmetic | Revenue arithmetic | Drop |
|---|---:|---|---|---:|
| $1.60 | 41 | 41 / 45 = 91% | $1.60 x 41 = 65.6 |  |
| $2.00 | 37 | 37 / 45 = 82% | $2.00 x 37 = 74.0 | 41 - 37 = 4 |
| $2.40 | 32 | 32 / 45 = 71% | $2.40 x 32 = 76.8 | 37 - 32 = 5 |
| $2.80 | 20 | 20 / 45 = 44% | $2.80 x 20 = 56.0 | 32 - 20 = 12 |
| $3.20 | 9 | 9 / 45 = 20% | $3.20 x 9 = 28.8 | 20 - 9 = 11 |

Maximum: $2.40 at 76.8. Plateau tolerance: 76.8 / 20 = 3.84. Plateau threshold: 76.8 - 3.84 = 72.96. Plateau: $2.00 to $2.40.

The margin test selects $2.40:

- $2.00 margin = ($2.00 - $0.92) / $2.00 = 54%, below 60%.
- $2.40 margin = ($2.40 - $0.92) / $2.40 = about 62%, above 60%.

Recommended input to the successor-price decision memo (LC33): $2.40 per drafted report, with R7 carried into the pricing re-sign.

## The trap

The trap is treating the revenue peak as sufficient while ignoring the margin boundary. In this run, the $2.00 rung is inside the revenue plateau, but:

- Revenue index at $2.00 = $2.00 x 37 = 74.0.
- Margin at $2.00 = ($2.00 - $0.92) / $2.00 = 54%.
- The 54% result is below the 60% floor.

The other trap is confusing this successor-price study with EXP-2. The active-account panel was deliberately used to inform the 73 held accounts and the pricing document's re-sign. It was not used to estimate EXP-2's conversion result, change EXP-2's $2.40 price, or change its pre-declared 6.0% bar.

The final trap is accepting M-009's ceiling as if it were the margin floor. At the $1.05 ceiling:

- Margin = ($2.40 - $1.05) / $2.40 = about 56%.
- The result is below 60%, although $1.05 does not breach the M-009 guardrail.

R7 is the named risk created by that gap.

## Feeds

- [ledgerline-pricing-packaging.md](ledgerline-pricing-packaging.md): successor price for the 73 held accounts and the pricing document's re-sign; the $2.40 recommendation, once the decision memo (LC33) resolves it, replaces the killed seat-price choice for future terms.
- [ledgerline-growth-plan.md](ledgerline-growth-plan.md): EXP-2 remains pre-declared at $2.40 per drafted report with the 6.0% activation bar. This worksheet does not change EXP-2.
- [ledgerline-van-westendorp.md](ledgerline-van-westendorp.md): the same EV-S01 panel's acceptable range, roughly $1.80 to $2.60.
- [ledgerline-journey.md](ledgerline-journey.md): N11, N49, N89, N91, N92 and N93.
- [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md): LC46, LC49, LC50 and LC51, including EV-S01 and R7.
- [frameworks/pricing/packaging-good-better-best.md](../frameworks/pricing/packaging-good-better-best.md): use the selected price as the usage-metric input for packaging review.
- [templates/planning/pricing-packaging.md](../templates/planning/pricing-packaging.md): section 3, the successor price; section 5, the hold and re-sign terms.
- [templates/operate/experiment-brief.md](../templates/operate/experiment-brief.md): the pre-declared EXP-2 confirmation test, without changing its price or bar.
- [knowledge/INDEX.md](../knowledge/INDEX.md): method background and the related van Westendorp method.
