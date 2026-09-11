# Van Westendorp Price Sensitivity Meter: Ledgerline Expense Copilot

Fills [frameworks/pricing/van-westendorp.md](../frameworks/pricing/van-westendorp.md). Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, its accounts, its prices, its survey respondents and every result are fiction built to show the worksheet method, not to recommend a price or claim what any real product would convert at.

**Owner:** Kwame Boateng, Data Analyst, with Maya Chen, Product Manager · **Fielded:** 2027-01-05 to 2027-01-08 · **Read:** 2027-01-11 · **Evidence:** EV-S01 · **Status:** Read for the held accounts' successor price

## What it is for

This survey measures perceived price sensitivity for Ledgerline's Expense Copilot at the successor value metric, dollars per drafted report, billed monthly in arrears with no seat charge. It asks the four Van Westendorp questions and reads the cumulative curves at their crossing intervals. The method is based on the ideas of Peter van Westendorp, from the Price Sensitivity Meter presented at the ESOMAR congress (1976).

The survey sampled only the 79 active accounts; the about 2,818 to 2,821 accounts EXP-2 will expose were never contacted, so the experiment is not primed. The result is a range of roughly $1.80 to $2.60 per drafted report. The proposed $2.40 price sits inside the range, near its expensive edge.

This instrument is used because a contracted price cannot be live-tested for the held accounts. It informs the successor price for the 73 paid accounts whose current price is held for 12 months, rather than changing EXP-2's pre-declared price or success bar.

## Run it when

- A new value metric needs a perception range before a price ladder is tested.
- The existing price metric has failed, as the per-seat price did in EXP-1, and the successor metric needs a bounded range.
- A live price test is not possible for the accounts whose contracted price is held for 12 months.
- A Gabor-Granger test needs a price range and reference points.

**Skip it when:** a real price test can run on the relevant accounts. Perception from a questionnaire loses to behavior at checkout. Here, the contracted price for the 73 paid accounts cannot be live-tested, so EV-S01 is the instrument for their successor price.

The survey sampled only the 79 active accounts (N64), leaving the about 2,818 to 2,821 EXP-2 accounts untouched. EXP-2 remains a single-arm re-offer at $2.40 per drafted report, with success at 6.0% or more activated within 14 days of exposure.

## Inputs you need first

- The offer and unit: Ledgerline Expense Copilot, priced in dollars per drafted report, billed monthly in arrears, with no seat charge.
- Account admins who hold or influence the account budget. The invited population was 79 active accounts, not filers.
- One segment and a minimum n of 40 set before fielding. A size split was declined because neither half would reach 25.
- No competitor price was shown in the questionnaire.
- A reason for using a survey instead of a live price test: the 73 paid accounts have a 12-month price hold, and the survey is for their successor price.

The survey design and fielding details are recorded in [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md), LC46. The active-account and held-account facts are recorded in [ledgerline-journey.md](ledgerline-journey.md), N64, N89, N91 and N93.

## The worksheet

### 1. The four questions

Each answer was an open numeric amount in dollars per drafted report.

| # | At what price would you consider Ledgerline Expense Copilot to be... | Curve |
|---|---|---|
| Q1 | so expensive that you would not consider buying it? | Too expensive |
| Q2 | priced so low that you would doubt its quality? | Too cheap |
| Q3 | getting expensive, so that you would have to think about buying it? | Expensive |
| Q4 | a bargain, a great buy for the money? | Cheap |

**Fielding frame:** "Please answer in dollars per drafted report, billed monthly in arrears, with no seat charge."

### 2. Cleaning

| Check | Rule | EV-S01 result |
|---|---|---|
| Ordering | Drop respondents whose too-cheap answer is at or above their too-expensive answer (too-cheap >= too-expensive), or whose cheap is above their expensive (cheap > expensive); all four exclusions were the first condition, so the drop count is reproducible against LC47's grid | 4 dropped for ordering; 51 responses minus 4 dropped = 47 usable responses |
| Unit | Drop answers in the wrong unit unless the respondent stated the unit | No wrong-unit exclusions are recorded in EV-S01 |
| Segment | Tabulate segments separately; never pool company sizes | One account-admin segment, n = 47 after cleaning; a size split was declined because neither half would reach 25 |

### 3. Tabulation grid

For each price:

- TC is the count whose too-cheap answer is at or beyond the price, so it falls as price rises.
- NC is not cheap, calculated as 47 minus C.
- C is the count whose cheap answer is at or beyond the price, so it falls as price rises.
- E is the count whose expensive answer is at or below the price, so it rises as price rises.
- NE is not expensive, calculated as 47 minus E.
- TE is the count whose too-expensive answer is at or below the price, so it rises as price rises.

| Price per drafted report | TC, falls | NC, rises | C, falls | E, rises | NE, falls | TE, rises |
|---|---:|---:|---:|---:|---:|---:|
| $1.00 | 40 | 1 | 46 | 1 | 46 | 0 |
| $1.60 | 26 | 6 | 41 | 4 | 43 | 2 |
| $2.00 | 14 | 15 | 32 | 11 | 36 | 5 |
| $2.40 | 6 | 27 | 20 | 24 | 23 | 11 |
| $2.80 | 2 | 37 | 10 | 35 | 12 | 22 |
| $3.20 | 1 | 42 | 5 | 41 | 6 | 31 |
| $4.00 | 0 | 46 | 1 | 46 | 1 | 42 |

Selected arithmetic checks:

- At $2.00, NC = 47 minus C = 47 minus 32 = 15.
- At $2.40, NC = 47 minus C = 47 minus 20 = 27.
- At $2.00, NE = 47 minus E = 47 minus 11 = 36.
- At $2.40, NE = 47 minus E = 47 minus 24 = 23.

### 4. Reading points

| Point | Where the columns swap order | Arithmetic and reading |
|---|---|---|
| Point of marginal cheapness, PMC | TC drops below NC | At $1.60, TC 26 is above NC 6. At $2.00, TC 14 is below NC 15. PMC is between $1.60 and $2.00. |
| Point of marginal expensiveness, PME | TE rises above NE | At $2.40, TE 11 is below NE 23. At $2.80, TE 22 is above NE 12. PME is between $2.40 and $2.80. |
| Optimal price point, OPP | TC drops below TE | At $2.00, TC 14 is above TE 5. At $2.40, TC 6 is below TE 11. OPP is between $2.00 and $2.40. |
| Indifference price point, IPP | E rises above C | At $2.00, C 32 is above E 11. At $2.40, C 20 is below E 24. IPP is between $2.00 and $2.40. |

**Decision rule applied:** the acceptable range runs from PMC to PME. The crossing intervals are:

- PMC: $1.60 to $2.00
- PME: $2.40 to $2.80

To state the result as a rough range, use the midpoint of each crossing interval:

- Lower landmark: ($1.60 + $2.00) / 2 = $1.80
- Upper landmark: ($2.40 + $2.80) / 2 = $2.60

**Acceptable range:** roughly **$1.80 to $2.60 per drafted report**, for the one account-admin segment with n = 47 after cleaning.

The $2.40 proposed usage price is inside the range:

- $1.80 < $2.40
- $2.40 < $2.60

It is near the expensive edge because:

- $2.60 minus $2.40 = $0.20
- $2.40 minus $1.80 = $0.60

The Gabor-Granger ladder was run on the same panel separately. Its result is recorded in [ledgerline-gabor-granger.md](ledgerline-gabor-granger.md). It selects $2.40 as the revenue peak and the only plateau rung that clears the margin floor.

## Reading the result

The survey gives a perception range, not a revenue-maximizing price. The usable panel is 47 account admins from the 79 active accounts, after 4 ordering exclusions. It is one segment, so this reading does not claim that company-size segments share one range.

The acceptable range is roughly $1.80 to $2.60 per drafted report. The $2.40 proposed price is inside the range, near the expensive edge. The separate Gabor-Granger result and the margin calculation provide the decision support for using $2.40 as the successor price for the held accounts.

This result applies to the successor price for the 73 paid accounts under the 12-month hold. It does not alter EXP-2:

- EXP-2 exposes about 2,818 to 2,821 accounts.
- EXP-2 uses the pre-declared $2.40 price.
- EXP-2 keeps the 6.0% activation bar.
- EXP-2's kill condition remains under 4.0% at the analysis date or on 2027-02-12, whichever comes first.

The survey does not establish a price for the about 2,818 to 2,821 EXP-2 accounts, because they were never contacted.

## ILLUSTRATIVE example

EV-S01 is the worked Ledgerline example for this worksheet. It is ILLUSTRATIVE and invented.

- **Offer:** Ledgerline Expense Copilot
- **Respondents:** account admins at 79 active accounts
- **Responses:** 51
- **Dropped:** 4 for ordering
- **Usable n:** 51 minus 4 = 47
- **Unit:** dollars per drafted report, billed monthly in arrears, with no seat charge
- **Segment:** one account-admin segment
- **Fielded:** 2027-01-05 to 2027-01-08
- **Read:** 2027-01-11
- **PMC:** between $1.60 and $2.00
- **OPP:** between $2.00 and $2.40
- **IPP:** between $2.00 and $2.40
- **PME:** between $2.40 and $2.80
- **Acceptable range:** roughly $1.80 to $2.60
- **Proposed price:** $2.40, inside the range near the expensive edge

The next pricing instrument is the Gabor-Granger ladder, which was run on the same panel. Its output is in [ledgerline-gabor-granger.md](ledgerline-gabor-granger.md).

## The trap

A smooth curve from the wrong respondents can give a false sense of precision. This survey avoids that trap by asking account admins, not filers, and by stating the one-segment limitation. It also avoids priming EXP-2: the survey sampled only the 79 active accounts, so the about 2,818 to 2,821 accounts EXP-2 will expose were never contacted.

The second trap is treating the midpoint range as a proven price. The Van Westendorp result only bounds perceived acceptability. The $2.40 decision also requires the separate Gabor-Granger result and the margin constraint. At the quoted $0.92 model cost (N11), the $2.40 price has:

`($2.40 - $0.92) / $2.40 = $1.48 / $2.40 = about 62%`

That is above the 60% margin floor; at the M-009 ceiling of $1.05 this falls to about 56%, opened as R7 in the coverage sheet. The $2.40 price remains proposed for the successor price, while EXP-2 keeps its own pre-declared test rule.

## Feeds

- [ledgerline-pricing-packaging.md](ledgerline-pricing-packaging.md): successor-price evidence for the held accounts, with the willingness-to-pay evidence stated as a survey range rather than a live-test result.
- [ledgerline-gabor-granger.md](ledgerline-gabor-granger.md): the price ladder, revenue index, plateau and margin guardrail.
- EXP-2: the survey does not change the pre-declared $2.40 price or the 6.0% activation bar for the about 2,818 to 2,821 exposed accounts.
- The 73 paid accounts: successor-price decision after their 12-month price hold, with the migration risk remaining open.
- Gate 5 pricing evidence: the reading is signed into the planning record by **Kwame Boateng** with **Maya Chen**, read on 2027-01-11.
