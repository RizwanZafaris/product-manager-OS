---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["templates/planning/business-case.md", "templates/planning/product-strategy.md", "templates/planning/gtm-plan.md"]
method: "knowledge/crossing-the-chasm.md"
aliases: ["Market sizing", "market-sizing"]
---
# Market sizing

Based on the TAM, SAM, SOM breakdown standard in venture capital and corporate strategic planning since the 1980s; no single originator or founding text is recorded, unlike most worksheets in this file. Explained here in this repository's own words.

## What it is for

A market number is either a headline copied from a report or a count you can defend. TAM is the total spend on the job if every possible buyer paid for it: the ceiling. SAM is the slice you could actually reach with this product, channel, and geography: the real field. SOM is what you could capture in a stated horizon, given your capacity and the competition already there: the number a business case can spend. Sizing only one way hides its own error, so this worksheet runs both a top-down estimate (a population narrowed by filters) and a bottom-up count (built from an account list and a price), and forces the two to land within a stated tolerance before either leaves the page. It improves one decision: whether the opportunity is worth funding, at the scale the strategy assumes.

## Run it when

- A business case needs a market number in its benefits section
- A where-to-play choice between segments in the product strategy needs a size, not a hunch
- Leadership asks how big the opportunity is and the honest answer is not yet written down
- Pricing or packaging work needs a volume estimate per tier

**Skip it when:** the segment cannot yet be described precisely enough that two people would count the same population. An undefined segment produces two confident numbers measuring different things. Finish naming the best-fit segment in [positioning](positioning-canvas.md), or the market definition field below, first.

## Inputs you need first

- The segment, precise enough to count, from positioning's best-fit segment or the discovery document
- The unit the market is counted in (companies, seats, transactions) and the unit the product charges by
- A price or price range with its source: a price list, pilot invoices, or a labeled assumption
- Count sources: public statistics with a URL and date, internal data (CRM, billing, analytics), or a directory a list could be built from
- For SOM: channel reach from the [GTM plan](../../templates/planning/gtm-plan.md) and onboarding or sales capacity from the team that owns it

## The worksheet

### Part 1: market definition

| Field | Answer |
|---|---|
| Job or category | [one sentence, no product name] |
| Segment | [who, precisely enough to count] |
| Geography | [where] |
| Revenue period | [one year, stated. Every currency figure below is revenue for one year, never a multi-year total] |
| SOM horizon | [how many years of selling the SOM assumes, stated. SOM is the annual revenue run-rate reached at the end of it, so it stays comparable with TAM and SAM] |
| Unit | [companies / seats / transactions: one, used consistently below] |
| Price per unit per year | [the one price both methods below are built from, with its source] |

The revenue period and the SOM horizon are two different things and the sheet fails quietly when they are conflated. The period keeps every currency figure annual so TAM, SAM and SOM can sit in one table. The horizon says how long you get to accumulate accounts before that annual figure is read. A one-year top-down SOM compared against a three-year capacity count is not a reconciliation; it is two different questions with one tolerance test stretched across them.

### Part 2: top-down

<!-- Every value needs a source with a URL and date, or an assumptions-register ID; a filter with neither is a guess wearing a percentage. If no public source exists for the population row, say so and skip to Part 3. -->

| Step | Population or filter | Value | Value is | Source (URL, date) or AS-id | Confidence |
|---|---|---|---|---|---|
| Total population, this unit | | | a count of units | | |
| Price per unit per year, from Part 1 | | | currency per year | | |
| TAM (population times price) | | | currency per year | | |
| Filter: share reachable with our product, channel, geography | | | a share, 0 to 1 | | |
| SAM (TAM times the reachability filter) | | | currency per year | | |
| Filter: share obtainable by the end of the SOM horizon, given capacity and competition | | | a share, 0 to 1 | | |
| SOM (SAM times the obtainability filter) | | | currency per year, at the end of the horizon | | |

The "Value is" column is not decoration. A population is a count, a filter is a share, and only the three named lines are money; a sheet that lets a count sit in the same column as a revenue figure with nothing to tell them apart is how a firm count ends up multiplied by another firm count.

### Part 3: bottom-up

| Factor | Value | Value is | Source or AS-id | Confidence |
|---|---|---|---|---|
| Target accounts on a list we could build today | | a count of accounts | | |
| Units per account (sample size and how it was drawn; 1 when the counting unit is the account itself) | | units per account | | |
| Price per unit per year, from Part 1 | | currency per year | | |
| SAM (accounts times units times price) | | currency per year | | |
| Accounts the channel can reach and the team can onboard by the end of the SOM horizon | | a count of accounts | | |
| SOM (that count times units times price) | | currency per year, at the end of the horizon | | |

### Part 4: reconciliation

**Stated tolerance:** the two SAM figures, and the two SOM figures, must each land within one and a half times of each other; neither may be more than one and a half times the other. Test SAM first. A SAM gap outside tolerance makes the SOM agreement meaningless, because the two SOMs are then filtered slices of two different fields.

Every cell in this table is annual revenue for the same period, in the same currency, built from the same unit and the same price, and both SOM cells are read at the end of the same horizon. Bottom-up usually has no TAM; write "not computed by this method" rather than borrowing the top-down figure, which would make the row agree with itself.

| Method | TAM (currency per year) | SAM (currency per year) | SOM (currency per year, end of horizon) |
|---|---|---|---|
| Top-down | | | |
| Bottom-up | not computed by this method | | |

**Decision rule:** inside tolerance, take the lower SOM as the base case and log the gap as a sensitivity. Outside tolerance, do not split the difference. Name the one input driving the gap, usually a segment mismatch (the public figure counts a wider population) or a price mismatch (list against invoiced), fix the weaker-sourced side, and rerun that method alone. When the fix imports a number from the other method, the two are no longer independent; say so, and log the shared input as the single assumption the reconciliation now rests on.

**If the business case needs a multi-year total,** build it from a ramp of accounts per year and bill each year at the annual price. Never multiply the end-of-horizon run-rate by the number of years: that charges every account for every year of the horizon, including the years before it was won. On a three-year horizon with an even ramp, that mistake lands exactly half again as large as the true total.

### Part 5: sensitivity

| SOM case | Value (currency per year, end of horizon) | Driven by (the two least certain inputs) |
|---|---|---|
| Low | | |
| Base | | |
| High | | |

## Reading the result

- **Inside tolerance, base case set.** Carry the range, not a point, into the business case benefits line, with the assumption IDs beside it, and with the horizon and the words "annual run-rate" attached to the figure. A SOM that travels without them arrives in the next deck as this year's revenue.
- **Outside tolerance, gap driver named.** Fix the weaker input and rerun; a business case built on an unreconciled pair is two guesses, not a number.
- **No public source exists for a top-down anchor.** Say so and run bottom-up only, flagged as the sole method used; never invent a top-down figure just to have two numbers to compare.
- **SOM exceeds the capacity the team actually has.** A GTM problem, not a sizing problem. The [GTM plan](../../templates/planning/gtm-plan.md)'s first cohort must be a countable subset of SOM, never the whole figure.

## ILLUSTRATIVE example

Invented. Ledgerline sizes the expense copilot as a product sold to other mid-market finance teams on the same shared finance system.

Part 1: unit, firms. Revenue period, one year. SOM horizon, three years. Price, 24,000 per firm per year, from the pilot invoices. Units per account is 1, because the counting unit is the account itself: one firm-wide subscription per firm.

Top-down: population, 10,000 firms on that finance system (invented, no public source, logged as an assumption). TAM, 10,000 x 24,000 = 240,000,000 per year. Reachability filter, 10 percent, an unsourced judgement; SAM, 1,000 firms, 24,000,000 per year.

Bottom-up: 1,800 target firms on a directory built from the finance system's own marketplace listing. SAM, 1,800 x 1 x 24,000 = 43,200,000 per year.

First reconciliation, at SAM: 43,200,000 over 24,000,000 is 1.8, outside the 1.5 tolerance, so the sizing stops here rather than proceeding to compare SOMs. The driver is the reachability filter: 10 percent was a judgement with no source, against a directory whose listings can be counted one by one. The weaker-sourced side is the top-down, so it is rerun alone with the filter set at 18 percent (1,800 of 10,000), giving SAM 43,200,000 per year on both rows. The two methods now share the directory, so they are no longer independent at SAM; the directory count is logged as the single assumption the rest of the sheet rests on.

SOM, both read as the annual run-rate at the end of year three: top-down obtainability, 8 percent of the reachable field given the vendors already serving it, so 144 firms, 3,456,000 per year. Bottom-up, onboarding capacity of 160 firms over the same three years, so 3,840,000 per year.

| Method | TAM | SAM | SOM at end of year 3 |
|---|---|---|---|
| Top-down | 240,000,000 | 43,200,000 | 3,456,000 |
| Bottom-up | not computed by this method | 43,200,000 | 3,840,000 |

Second reconciliation: 3,840,000 over 3,456,000 is 1.11, inside the 1.5 tolerance. Base case, the lower figure: 144 firms, 3,456,000 per year, reached at the end of year three, close to the 140-customer count the [business model canvas](business-model-canvas.md) example assumed independently. The 384,000 per year gap is logged as a sensitivity tracking the obtainability filter against the onboarding capacity estimate, the two least certain inputs, both with a validate-by date.

The three-year figure the business case wants is not 3,456,000 times three. On an even ramp of 48, 96 and 144 firms live at the end of years one, two and three, billed at 24,000, the total is 24,000 x (48 + 96 + 144) = 6,912,000 across the horizon, against the 10,368,000 that multiplying the run-rate would have produced: exactly half again too much. The 3,456,000 is a run-rate at one date, and the benefits line has to say which.

## The trap

SOM stated as a small slice of a large TAM with no bottom-up check: "even a sliver of this market and we win," where the sliver was sized to produce a number the room already liked, not counted from an account list. The tell: a SOM with no accounts column behind it, and a bottom-up sizing never run because the top-down figure already satisfied the room. A reconciliation that only runs in one direction is not a reconciliation; run both, every time, even when the top-down number feels sufficient alone.

## Feeds

- [Business case](../../templates/planning/business-case.md): SOM as a range with its assumption IDs, in the benefits section
- [Product strategy](../../templates/planning/product-strategy.md): section 2, SAM per segment informs where to play
- [GTM plan](../../templates/planning/gtm-plan.md): the first cohort as a countable subset of SOM
- [Assumptions register](../../templates/definition/assumptions-register.md): every input without a public source
- [Evidence note](../../templates/discovery/evidence-note.md): one per external figure, with its URL and the definition the source used
- PLANNING track, ahead of Gate 1
- Method background: [Crossing the Chasm](../../knowledge/crossing-the-chasm.md) (Moore, 1991), on why the beachhead, not the whole market, is the number that matters first
