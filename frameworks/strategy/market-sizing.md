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
| Period | [one year, stated] |
| Unit | [companies / seats / transactions: one, used consistently below] |

### Part 2: top-down

<!-- Every value needs a source with a URL and date, or an assumptions-register ID; a filter with neither is a guess wearing a percentage. If no public source exists for the population row, say so and skip to Part 3. -->

| Step | Population or filter | Value | Source (URL, date) or AS-id | Confidence |
|---|---|---|---|---|
| Total population, this unit | | | | |
| TAM (population times price per unit per year) | | | | |
| Filter: share reachable with our product, channel, geography | | | | |
| SAM (TAM times the reachability filter) | | | | |
| Filter: share obtainable in the stated horizon, given capacity and competition | | | | |
| SOM (SAM times the obtainability filter) | | | | |

### Part 3: bottom-up

| Factor | Value | Source or AS-id | Confidence |
|---|---|---|---|
| Target accounts on a list we could build today | | | |
| Units per account (sample size and how it was drawn) | | | |
| Price per unit per year | | | |
| SAM (accounts times units times price) | | | |
| Accounts the channel can reach and the team can onboard in the horizon | | | |
| SOM (that count times units times price) | | | |

### Part 4: reconciliation

**Stated tolerance:** the two SOM figures must land within one and a half times of each other; neither may be more than one and a half times the other.

| Method | TAM | SAM | SOM |
|---|---|---|---|
| Top-down | | | |
| Bottom-up | | | |

**Decision rule:** inside tolerance, take the lower SOM as the base case and log the gap as a sensitivity. Outside tolerance, do not split the difference. Name the one input driving the gap, usually a segment mismatch (the public figure counts a wider population) or a price mismatch (list against invoiced), fix the weaker-sourced side, and rerun that method alone.

### Part 5: sensitivity

| SOM case | Value | Driven by (the two least certain inputs) |
|---|---|---|
| Low | | |
| Base | | |
| High | | |

## Reading the result

- **Inside tolerance, base case set.** Carry the range, not a point, into the business case benefits line, with the assumption IDs beside it.
- **Outside tolerance, gap driver named.** Fix the weaker input and rerun; a business case built on an unreconciled pair is two guesses, not a number.
- **No public source exists for a top-down anchor.** Say so and run bottom-up only, flagged as the sole method used; never invent a top-down figure just to have two numbers to compare.
- **SOM exceeds the capacity the team actually has.** A GTM problem, not a sizing problem. The [GTM plan](../../templates/planning/gtm-plan.md)'s first cohort must be a countable subset of SOM, never the whole figure.

## ILLUSTRATIVE example

Invented. Ledgerline sizes the expense copilot as a product sold to other mid-market finance teams on the same shared finance system, one year, priced per firm.

Top-down: population, 10,000 firms on that finance system (invented, no public source, logged as an assumption); reachability filter, 10 percent; SAM, 1,000 firms; obtainability filter, 15 percent, given the vendors already serving this segment; SOM, 150 firms at 24,000 per firm per year, 3,600,000.

Bottom-up: 1,800 target firms on a directory built from the finance system's own marketplace listing; onboarding capacity, 160 firms reachable and activatable in three years; SOM, 160 firms at 24,000, 3,840,000.

Reconciliation: ratio, 160 over 150, about 1.07, inside the 1.5 tolerance. Base case: 150 firms, 3,600,000 per year, close to the 140-customer count the [business model canvas](business-model-canvas.md) example assumed independently. Sensitivity: the gap tracks the obtainability filter against the onboarding capacity estimate, the two least certain inputs, both logged as assumption rows with a validate-by date.

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
