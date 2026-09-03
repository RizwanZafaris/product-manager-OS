---
layer: frameworks
stage: PLANNING
gate: 5
feeds: ["templates/planning/pricing-packaging.md", "frameworks/pricing/packaging-good-better-best.md", "templates/operate/experiment-brief.md"]
method: "knowledge/INDEX.md"
aliases: ["Gabor-Granger price ladder", "gabor-granger"]
---
# Gabor-Granger price ladder

Based on the ideas of André Gabor and Clive Granger, from their 1966 paper in Economica on price as an indicator of quality, the origin of the purchase-intention ladder that carries their names. Explained here in this repository's own words.

## What it is for

Gabor-Granger asks each respondent, at a series of prices, whether they would buy. The shares of yes at each rung form a demand curve, and price times share forms a revenue index whose peak is the revenue-maximizing price for that sample. Where van Westendorp bounds a range from perception, this method picks a point from stated purchase intention, and it does so on a ladder you control, so the answer comes back in the units and tiers you will sell. It also gives the shape of demand between rungs, which is what tier pricing needs. The decision it improves is the list price of a tier and the volume you give up by moving one rung.

## Run it when

- A van Westendorp range exists and the pricing document needs a number for each tier.
- The offer is comparable to things buyers already price, so the ladder can be short and realistic.
- A discount policy needs to know how much volume a lower rung buys.

**Skip it when:** the category is new to buyers and no range exists. A ladder anchored on the team's guess measures the guess; run [van Westendorp](van-westendorp.md) first, or a live test.

## Inputs you need first

- The offer described with its unit, from [pricing and packaging](../../templates/planning/pricing-packaging.md) section 1.
- A ladder of five to seven prices spanning the acceptable range plus one rung beyond each end.
- Budget-holding respondents, segmented, with a minimum n each from the [survey design](../../templates/discovery/survey-design.md).
- A guardrail decided beforehand: a volume floor for adoption, or a margin floor.

## The worksheet

### 1. Design

| Field | Entry |
|---|---|
| Unit | [per active filer per month, per seat, per report] |
| Ladder | [p1 to p7, ascending] |
| Presentation | [random starting rung, then up on yes and down on no; or every rung asked in random order; state which] |
| Yes definition | [a plain yes or no; or a five-point likelihood with only "definitely would buy" counted as yes; state which] |
| Guardrail | [minimum share of buyers, or minimum margin] |

### 2. Cleaning

Drop respondents who say yes at a higher rung after no at a lower one, and report the count.

### 3. Demand and revenue table

<!-- Revenue index = price times count of yes (or times share; the ranking is the same).
     Drop = yes at the previous rung minus yes at this rung. -->

| Price | Would buy (count) | Share | Revenue index | Drop from previous rung |
|---|---|---|---|---|
| [p1] | | | | |

**Decision rule:** the candidate price is the rung with the highest revenue index. Report the plateau, every rung within a tolerance you set beforehand (one part in twenty of the maximum is a workable convention), and pick inside the plateau using the guardrail and the van Westendorp range. If the maximum sits on the top rung, the ladder was too short; extend it and re-run before believing anything.

## Reading the result

A flat plateau means price is not the lever in this range and packaging or the value metric is; a sharp peak means buyers share a reference price, and the rung above it is where you lose them. The drop column is the discount policy: it tells you what volume a rung of discount buys, which is usually less than sales expects. Read segments separately; a plateau at 8 for small firms and at 15 for large ones is two tiers, and pooling them yields a price wrong for both. Stated intention overstates purchase, so treat the count of yes as an upper bound, and treat the price choice, not the volume forecast, as the output.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot, per active filer per month, the same invented panel of 32 finance buyers as the van Westendorp sheet, plain yes or no, random starting rung.

| Price | Would buy | Revenue index | Drop |
|---|---|---|---|
| 6 | 30 | 180 | |
| 8 | 27 | 216 | 3 |
| 10 | 21 | 210 | 6 |
| 12 | 16 | 192 | 5 |
| 15 | 9 | 135 | 7 |
| 18 | 4 | 72 | 5 |

Maximum at 8; plateau 8 to 10 under the tolerance set beforehand. The van Westendorp range began near 9, so 8 sits at the cheap edge where quality doubt starts. Decision: 10 as the list price for the middle tier, with the drop from 8 to 10 (6 of 32) recorded as the volume the team accepts giving up; the discount rule caps at 8 for annual prepay. Segment note: firms above 500 staff plateaued at 12 to 15 and are priced in the top tier instead.

## The trap

The revenue peak on the top rung. The ladder stopped at the price the team could imagine, every rung said yes often enough, and the sheet crowns the last rung as optimal because there was nothing above it to lose to. The fix is mechanical: a ladder must include a rung where most say no, or it has not measured demand. The quieter failure is the ascending ladder from a low start: respondents commit at 6 and stay consistent upward, inflating yes at every rung; randomize the start, or ask each rung independently, and say which you did.

## Feeds

- [Pricing and packaging](../../templates/planning/pricing-packaging.md): section 3 (tiers), the price column; section 5 (discount rules), the drop column
- [Good-better-best packaging](packaging-good-better-best.md): one plateau per tier
- [Experiment brief](../../templates/operate/experiment-brief.md): the live price test that confirms the chosen rung
- PLANNING track, feeding [Gate 5: release readiness green](../../os/STAGE-GATES.md) through the pricing document
- Method background: [knowledge index](../../knowledge/INDEX.md); [van Westendorp](van-westendorp.md) for the range this ladder spans
