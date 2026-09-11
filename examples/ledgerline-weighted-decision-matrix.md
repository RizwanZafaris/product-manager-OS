# Weighted Decision Matrix: Ledgerline Value Metric

Fills [frameworks/prioritization/weighted-decision-matrix.md](../frameworks/prioritization/weighted-decision-matrix.md).

Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, its customers, its vendor, every score and every decision are fictional and are included to demonstrate the worksheet.

**Owner:** Isabel Ferreira, Chief Product Officer · **Date:** 2026-11-03 · **Decision:** D3

Based on the ideas of Stuart Pugh, from his concept selection method (1981) and *Total Design* (1991), with criteria weights in the manner of multi-attribute decision analysis, Keeney and Raiffa (1976). Explained here in this repository's own words. The data comes from the [ledgerline journey](ledgerline-journey.md) and the [ledgerline coverage sheet](ledgerline-coverage-sheet.md).

## What it is for

This matrix chooses the value metric for Ledgerline's Expense Copilot add-on:

- **Seats:** plan seats at $6 per seat per month.
- **Per drafted report:** a charge for each report drafted by the Copilot.
- **Per active filer:** a charge for each filer who uses the Copilot.

The matrix makes Isabel Ferreira's weights explicit before scoring. It produces a weighted total, a margin, and a sensitivity check. The result records D3: seats win, but the sensitivity rows show that the result depends on the billability weight, specifically what billing could meter by phase 1.

The options and source facts are in N13, N40, N49, DEP4, ADR-007, D3, LC11 and LC12 of the [ledgerline journey](ledgerline-journey.md) and [ledgerline coverage sheet](ledgerline-coverage-sheet.md).

## Run it when

- There are three mutually exclusive value metrics.
- The disagreement is about priorities, not about the available options.
- The decision is important enough to record as D3.
- The facts are available per option, with the unsupported per drafted report and per active filer meters recorded as gaps or dependencies.
- A single decider can set the weights before scoring. Isabel Ferreira set and dated the weights on 2026-11-03.

**Skip it when:** one criterion decides it. That was not the case here. Billability mattered, but the team also considered delivered value, sales forecasting, buyer comparability and margin safety.

## Inputs you need first

- **Options:** seats, per drafted report and per active filer.
- **Criteria:** billability inside the launch cycle, delivered value, sales forecasting and quoting, buyer comparability with Cinderwick, and margin safety on the model line.
- **Facts and gaps:** seats were supported by ADR-007 (the billing system's existing plan seat count), with the add-on seat meter still to be built (DEP1, N86). A per drafted report meter did not exist and required DEP4. Per active filer had no agreed definition.
- **Decider:** Isabel Ferreira, the pricing owner and D3 decider.
- **Decision context:** the seats option was quoted at $6 per plan seat per month, while Cinderwick's quoted price was $8 per seat per month. The model-line margin floor was 60%.

## The worksheet

### Step 1: criteria and weights, before any option is scored

Isabel Ferreira set the weights before any option was scored on 2026-11-03.

| Criterion | What a 5 looks like | What a 1 looks like | Weight (1 to 5) | Why this weight |
|---|---|---|---:|---|
| Billable inside the launch cycle | Billing can meter and charge the option by phase 1 without DEP4 | The option cannot be metered by phase 1 | 5 | The pricing review needed a value metric billing could support in the launch cycle |
| Tracks delivered value, M-001 | The charge closely follows Copilot-drafted reports approved on first submission | The charge has no clear relationship to M-001 | 4 | M-001 is the north star, so the value metric should reflect it where possible |
| Sales can forecast and quote it | Sales can forecast and quote the option from an existing account fact | Sales cannot quote it without a new definition or data source | 3 | Forecastability matters, but it does not outweigh the ability to bill |
| Buyer can compare it with Cinderwick's per-seat price | The buyer can compare the unit directly with $8 per seat per month | The buyer cannot compare the unit with Cinderwick's quoted unit | 2 | The competitor comparison is useful, but it is not the primary value test |
| Margin safety on the model line, N49 | The option supports the 60% gross-margin floor with the quoted model cost | The option makes the 60% floor difficult to protect | 3 | Margin safety is a finance constraint, not the sole definition of customer value |

The weights sum to:

`5 + 4 + 3 + 2 + 3 = 17`

The score anchors and option scores are from LC11. The buyer-comparability score for seats is the least evidenced because no buyer was asked a price, N40.

### Step 2: score and multiply

Weighted score equals weight multiplied by score. Total equals the sum of weighted scores.

| Criterion | Weight | Seats score | Seats weighted | Per drafted report score | Per drafted report weighted | Per active filer score | Per active filer weighted |
|---|---:|---:|---:|---:|---:|---:|---:|
| Billable inside the launch cycle | 5 | 5 | 5 x 5 = 25 | 1 | 5 x 1 = 5 | 2 | 5 x 2 = 10 |
| Tracks delivered value, M-001 | 4 | 1 | 4 x 1 = 4 | 5 | 4 x 5 = 20 | 3 | 4 x 3 = 12 |
| Sales can forecast and quote it | 3 | 5 | 3 x 5 = 15 | 2 | 3 x 2 = 6 | 3 | 3 x 3 = 9 |
| Buyer can compare it with Cinderwick's per-seat price | 2 | 5 | 2 x 5 = 10 | 2 | 2 x 2 = 4 | 3 | 2 x 3 = 6 |
| Margin safety on the model line, N49 | 3 | 3 | 3 x 3 = 9 | 5 | 3 x 5 = 15 | 4 | 3 x 4 = 12 |
| **Total** | | | **25 + 4 + 15 + 10 + 9 = 63** | | **5 + 20 + 6 + 4 + 15 = 50** | | **10 + 12 + 9 + 6 + 12 = 49** |

Seats wins with 63.

The runner-up is per drafted report at 50. The margin is:

`(63 - 50) / 63 = 13 / 63 = 20.634...%`, about **21%**

The margin is above the worksheet's 10% tie threshold. Seats therefore wins the base matrix, but the sensitivity check is required because the per drafted report option scores better on delivered value and margin safety.

### Step 3: sensitivity check

The rows below reproduce LC12. Each change is made one at a time.

| Change | New totals | Winner changes? | What it tells you |
|---|---|---|---|
| Swap the two highest weights | Seats = 59; per drafted report = 54; per active filer = 50 | No, seats holds | The ordering of the two highest priorities does not change the winner |
| Set the most contested weight, billability, to 1 | Per drafted report = 46; seats = 43; per active filer = 41 | Yes, per drafted report wins | The decision depends on the billability weight |
| Drop the criterion the winner scores best on, billability | Per drafted report = 45; per active filer = 39; seats = 38 | Yes, per drafted report wins | Seats is not robust when its strongest criterion is removed |
| Lower the least-evidenced score by 1, seats' Cinderwick comparability score | Seats = 61; the other totals remain 50 and 49 | No, seats holds | The least-evidenced buyer-comparability score is not the deciding hinge |

The contested-weight arithmetic is recorded as the sensitivity result from LC12:

- Billability weight set to 1: per drafted report = 46, seats = 43, per active filer = 41.
- Billability dropped: per drafted report = 45, per active filer = 39, seats = 38.
- Seats' least-evidenced comparability score lowered by 1: seats = 61, so seats still leads 50.

The decision hinges on one weight: **what billing could meter by phase 1**. DEP4 is the dependency for a usage meter, and ADR-007 records the existing seat-based entitlement and charge.

### The two-minute version: impact versus effort

This shortcut was not used for D3. No impact and effort set for the three value metrics is recorded in the [ledgerline journey](ledgerline-journey.md) or [ledgerline coverage sheet](ledgerline-coverage-sheet.md), so assigning quadrants would invent scores.

| | Effort below the median | Effort above the median |
|---|---|---|
| Impact above the median, against the period's metric | Not run: no impact and effort set is available | Not run: no impact and effort set is available |
| Impact below the median | Not run: no impact and effort set is available | Not run: no impact and effort set is available |

The weighted matrix was appropriate because the decision was about unequal priorities and the available evidence was expressed as criterion scores, not as an impact and effort backlog.

## Reading the result

The base result is:

- **Winner:** seats, plan seats at $6 per seat per month.
- **Margin:** 13 / 63, about 21% over per drafted report.
- **Hinge:** the weight assigned to billability inside the launch cycle.

The matrix supports D3, but it does not show a robust preference for seats independent of the weighting. When billability is set to 1 or removed, per drafted report wins. That means the decision is not simply "seats have more customer value." It is "seats win when phase 1 billability receives the highest weight."

The pricing document accepted this mismatch in writing: seats did not rhyme with the north star, M-001, but billing could meter seats through ADR-007 and sales could forecast seats. D3 therefore selected seats and stated that the decision would reopen on the EXP-1 kill rule or on a win-loss pattern naming seats.

EXP-1 later exposed the mismatch. The experiment result was 2.4% in the control arm and 2.9% in the anchored arm, both below the 4.0% kill threshold. EXP-1's kill rule fired on 2026-12-18, and D6 formally killed the per-seat price on 2026-12-21, and the next proposed value metric became $2.40 per drafted report through ADR-008 and DEP4.

## ILLUSTRATIVE example

Ledgerline chooses a value metric for the Expense Copilot add-on. The options are plan seats, per drafted report and per active filer. Isabel Ferreira sets the weights before scoring on 2026-11-03.

The base matrix gives:

| Option | Total |
|---|---:|
| Seats | 63 |
| Per drafted report | 50 |
| Per active filer | 49 |

The arithmetic for seats is:

`(5 x 5) + (4 x 1) + (3 x 5) + (2 x 5) + (3 x 3) = 25 + 4 + 15 + 10 + 9 = 63`

The arithmetic for per drafted report is:

`(5 x 1) + (4 x 5) + (3 x 2) + (2 x 2) + (3 x 5) = 5 + 20 + 6 + 4 + 15 = 50`

The arithmetic for per active filer is:

`(5 x 2) + (4 x 3) + (3 x 3) + (2 x 3) + (3 x 4) = 10 + 12 + 9 + 6 + 12 = 49`

Seats leads per drafted report by:

`63 - 50 = 13 points`

The relative margin is:

`13 / 63 = about 21%`

The sensitivity check changes the interpretation. Setting billability to 1 changes the order to per drafted report at 46, seats at 43 and per active filer at 41. Dropping billability changes the order to per drafted report at 45, per active filer at 39 and seats at 38.

The finding is therefore:

> Seats is the selected metric for D3 because phase 1 billing could meter it, not because it best tracks delivered value. The choice is sensitive to that billability weight.

The pricing document accepted the mismatch. DEP4 and ADR-008 later supplied the missing path to a drafted-report meter, and EXP-1 provided the evidence that reopened D3.

## The trap

Reverse engineering would have produced a seat total first and then adjusted the weights until seats won. This sheet avoids that by recording that Isabel Ferreira set the weights before scoring.

The more subtle trap is treating a 21% margin as proof that the choice is robust. The margin is calculated against the base weighting, but two sensitivity rows change the winner. The honest result is not "seats wins without qualification." It is "seats wins under the billability priority, and the decision hinges on what billing could meter by phase 1."

A second trap is hiding the evidence gap in the buyer-comparability score. N40 records that 0 of 6 design-partner interviews asked a price. Lowering that least-evidenced seats score by 1 still leaves seats ahead at 61, but that does not turn the evidence into buyer willingness to pay.

## Feeds

- [Decision log](../templates/execution/decision-log.md): D3, the options that lost, and the billability weight the decision hinged on
- [Decision memo](../templates/planning/decision-memo.md): for a one-way or heavy two-way choice when the matrix result needs a written case
- [ADR](../templates/architecture/adr.md): ADR-007 records seat-based entitlement and charge; ADR-008 proposes the drafted-report meter without editing ADR-007
- [Assumptions register](../templates/definition/assumptions-register.md): the margin-floor assumption, N49, and the least-evidenced score
- [Decision doors](../frameworks/prioritization/decision-doors.md): the later re-score of D3 and the decision to introduce ADR-008
- Method background: the attribution line above names Stuart Pugh, Keeney and Raiffa; the [knowledge index](../knowledge/INDEX.md) holds the neighbouring methods
