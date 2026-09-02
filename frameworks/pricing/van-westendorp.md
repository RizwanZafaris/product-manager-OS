# Van Westendorp price sensitivity meter

Based on the ideas of Peter van Westendorp, from the Price Sensitivity Meter presented at the ESOMAR congress (1976). Explained here in this repository's own words.

## What it is for

The meter asks buyers four questions about price, two on the expensive side and two on the cheap side, and tabulates the answers as cumulative curves. Where the curves cross, it reads off a range of acceptable prices and two reference points inside it. It answers "what price range would this segment consider without flinching" before you have a product to sell, which makes it the first pricing instrument for a new offer or a new value metric. It does not answer "what price maximizes revenue"; that is [Gabor-Granger](gabor-granger.md), run after this one has bounded the range. The decision it improves is the price ladder you test next, and whether the value metric itself makes sense to buyers.

## Run it when

- A new product or tier has no price history and the alternatives are priced on a different unit.
- The value metric changed (per seat to per active filer) and the old prices carry no information.
- Before a Gabor-Granger test, to choose a ladder that is not anchored on the team's hopes.

**Skip it when:** you can run a real price test. Perception from a questionnaire loses to behavior at checkout every time; if a live experiment through the [experiment brief](../../templates/operate/experiment-brief.md) is possible, run that.

## Inputs you need first

- A one-paragraph description of the offer with its unit stated (per active filer per month), from [pricing and packaging](../../templates/planning/pricing-packaging.md) section 1.
- Respondents who hold or influence the budget, screened by role; filers are not buyers.
- Segments decided before fielding, with a minimum n each, in the [survey design](../../templates/discovery/survey-design.md).
- No competitor price shown anywhere in the questionnaire.

## The worksheet

### 1. The four questions

Each answer is an open numeric amount in the stated unit.

| # | At what price would you consider [offer] to be... | Curve |
|---|---|---|
| Q1 | so expensive that you would not consider buying it? | Too expensive |
| Q2 | priced so low that you would doubt its quality? | Too cheap |
| Q3 | getting expensive, so that you would have to think about buying it? | Expensive |
| Q4 | a bargain, a great buy for the money? | Cheap |

### 2. Cleaning

| Check | Rule |
|---|---|
| Ordering | Drop respondents whose too cheap is at or above their too expensive, or whose cheap is above their expensive; report the count dropped |
| Unit | Drop answers in the wrong unit (annual where monthly was asked) unless the respondent stated the unit |
| Segment | Tabulate segments separately; never pool company sizes |

### 3. Tabulation grid

<!-- For each price on a grid: TE = count whose too-expensive answer is at or below the price
     (rises with price); E = count whose expensive answer is at or below (rises); C = count
     whose cheap answer is at or above the price (falls); TC = count whose too-cheap answer is
     at or above (falls). NC = n minus C (not cheap); NE = n minus E (not expensive). -->

| Price | TC (falls) | NC (rises) | C (falls) | E (rises) | NE (falls) | TE (rises) |
|---|---|---|---|---|---|---|
| [price 1] | | | | | | |

### 4. Reading points

| Point | Where the columns swap order | Meaning |
|---|---|---|
| Point of marginal cheapness (PMC) | TC drops below NC | Below this, doubt about quality outgrows the bargain |
| Point of marginal expensiveness (PME) | TE rises above NE | Above this, refusals outgrow acceptance |
| Optimal price point (OPP) | TC drops below TE | Fewest respondents reject on either ground |
| Indifference price point (IPP) | C drops below E | As many call it cheap as call it expensive; often near the habitual price in the category |

**Decision rule:** the acceptable range runs from PMC to PME. Read each crossing as the interval between the two grid prices where the columns swap order, and quote it as an interval. Choose the Gabor-Granger ladder to span the range plus one rung outside each end.

## Reading the result

The range is the result; the points are landmarks. A narrow range means buyers share a mental model of the unit, usually because an incumbent trained them; a wide range means the value metric is unfamiliar and packaging will do more work than price. OPP well below IPP is common and does not mean you should price at OPP: it is the price with the fewest objections, not the most revenue. Segments with non-overlapping ranges are separate tiers, not one price. Small samples give crossing intervals, never a decimal; report n per segment beside every reading, and remember that it measures perception on the day, framed by your description.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot, priced per active filer per month. 32 finance buyers at mid-market firms after cleaning (3 dropped for ordering). Counts at each grid price:

| Price | TC | NC | C | E | NE | TE |
|---|---|---|---|---|---|---|
| 4 | 30 | 0 | 32 | 0 | 32 | 0 |
| 6 | 24 | 1 | 31 | 1 | 31 | 0 |
| 8 | 15 | 5 | 27 | 4 | 28 | 2 |
| 10 | 8 | 12 | 20 | 9 | 23 | 5 |
| 12 | 3 | 20 | 12 | 19 | 13 | 11 |
| 15 | 1 | 27 | 5 | 26 | 6 | 21 |
| 20 | 0 | 31 | 1 | 31 | 1 | 29 |

PMC between 8 and 10 (TC drops below NC there); OPP between 10 and 12 (TC drops below TE); IPP between 10 and 12 (C drops below E); PME between 12 and 15 (TE rises above NE). Acceptable range: roughly 9 to 13 per active filer per month. Next step: a Gabor-Granger ladder of 6, 8, 10, 12, 15, 18.

## The trap

A pretty chart from people who will never sign the invoice. The survey goes to filers because they are easy to reach, the curves are smooth, and the range describes what employees think their employer should pay. Screen on budget authority, and if the buyer sample is thin, say so beside the chart instead of pooling. The second failure is reading OPP as the price: the team charges at the point of fewest objections and leaves the revenue-maximizing price, which usually sits higher, on the table.

## Feeds

- [Pricing and packaging](../../templates/planning/pricing-packaging.md): section 1 (value metric evidence) and section 3 (tiers), the range as the evidence column
- [Gabor-Granger](gabor-granger.md): the ladder
- [Good-better-best packaging](packaging-good-better-best.md): non-overlapping segment ranges become tier boundaries
- PLANNING track, feeding [Gate 5: release readiness green](../../os/STAGE-GATES.md) through the pricing document
- Method background: [knowledge index](../../knowledge/INDEX.md); the [pricing-packaging skill](../../skills/pricing-packaging/SKILL.md) runs the research design
