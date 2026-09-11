# Metrics Review: Threadmere Apparel web store

Fills [templates/operate/metrics-review.md](../templates/operate/metrics-review.md). Everything here is invented: Threadmere Apparel is a fictional direct-to-consumer apparel brand selling through its own web store, the people are roles filled by invented names, and every count, dollar figure, percentage and date is ILLUSTRATIVE, carried from this example's own working sheet so it can be checked against the arithmetic shown. See the [examples index](README.md). The domain card is [Ecommerce](../knowledge/domains/ecommerce.md); regulatory statements are described as of 2026-09-11 and are not legal advice.

**Owner:** Isabela Duarte, head of product · **Review window:** 2026-07-01 to 2026-09-30 · **Cadence:** every 13 weeks (quarterly)
**Linked OKR sheet:** okrs.md copy for the Threadmere web store, Q3 2026

## 1. Outcome vs target, per key result

<!-- Copy each key result from the OKR sheet. Do not invent new ones here; if the KRs
     were wrong, that is a finding for section 4. The italic row shows a completed entry. -->

| Key result | Baseline | Target | Actual this window | Delta | Data confidence (high / medium / low, why) |
|---|---|---|---|---|---|
| KR-1: checkout step 3 conversion, online sessions to orders | 3.02% | 3.10% | 3.42% | +0.32 pts, above target | high, storefront event pipeline, definition version v4 unchanged all window |
| KR-2: CM2 per order, whole store | $5.90 | $6.10 | $5.55 | -$0.35, short of target | medium, CM2 relies on the returns-provision assumption finance revised on 2026-08-14 |
| KR-3: free-returns-eligible SKU share, kept as a merchandising key result after it was added mid-quarter | 18% | not to exceed 24% | 31% | +13 pts, ceiling breached | high, catalogue flag, count taken 2026-09-30 |

KR-3 was not on the Q3 sheet signed on 2026-06-26. It was added on 2026-08-08 when the merchandising team widened free-returns eligibility to chase KR-1, and the OKR sheet carries the same note. Adding a key result mid-window is itself a finding; section 4 grades it.

## 2. Input metric movement

<!-- Input metrics explain the outcome row above. If an input moved and the outcome
     did not, the causal story in the strategy is wrong somewhere. Say so. -->

The two headline rows, carried unchanged from the domain card's worked example:

| Input metric | Prior window | This window | Expected to drive | Did it? |
|---|---|---|---|---|
| Conversion rate, checkout step 3 | 3.10% target against 3.42% actual | 3.42% actual | KR-1 | yes, the funnel moved exactly as scoped, but see the waterfall below before calling it a win |
| Free-returns eligible SKU share | 18% target against 31% actual | 31% actual | KR-1 | yes for conversion, no for KR-2, because the widened eligibility is where the return cost landed |

Then the contribution-margin waterfall per order, which is how [Ecommerce](../knowledge/domains/ecommerce.md) bends this template: input metrics become waterfall layers, and the layers have to be read against each other rather than in isolation.

| Waterfall layer, per order | Prior window | This window | Movement | Read |
|---|---|---|---|---|
| Revenue (AOV), CM0 | $18.40 | $18.40 | $0.00 | Held flat; the conversion gain did not come from discounting |
| minus cost of goods sold | $7.40 | $7.40 | $0.00 | Held flat; no sourcing change this window |
| CM1 after COGS | $11.00 | $11.00 | $0.00 | CM1 per order is unchanged, so the win has to be found below this line |
| minus fulfilment and shipping | $3.10 | $3.10 | $0.00 | Held flat |
| minus payment processing | $0.60 | $0.60 | $0.00 | Held flat |
| minus returns (processing plus re-shipment) | $1.40 | $1.75 | +$0.35 | The whole movement lives here; return processing and re-shipment ate two-thirds of the margin the conversion gain bought |
| CM2 after fulfilment, payment and returns | $5.90 | $5.55 | -$0.35 | Blended number moves less than either of the two rows the brief names; reading it alone would have hidden the trade |
| minus marketing (blended acquisition cost per order) | $2.40 | $2.40 | $0.00 | Held flat; paid channels were not the cause |
| CM3 after marketing | $3.50 | $3.15 | -$0.35 | The store still books a positive CM3 per order, but the trend is the wrong direction |

Arithmetic, layer by layer, so a reader can re-derive every cell: 18.40 - 7.40 = 11.00 (CM1, both windows); 11.00 - 3.10 - 0.60 - 1.40 = 5.90 (CM2 prior); 11.00 - 3.10 - 0.60 - 1.75 = 5.55 (CM2 this window); 5.90 - 2.40 = 3.50 and 5.55 - 2.40 = 3.15 (CM3). The $0.35 CM2 movement is also exactly the returns line movement, which is the point: conversion up, CM2 per order fell, because return rates rose on the widened free-returns SKUs. The two free-returns-eligible-SKU rows from the domain card's worked example, restated with targets attached so they can be read against a commitment rather than against last quarter:

| Input metric | Target (signed) | Actual | Read |
|---|---|---|---|
| CM2 per order, free-returns-eligible SKUs | $6.40 | $2.15 | Return processing and re-shipment ate two-thirds of the margin the conversion gain bought; this line is why the free-returns share row is on this review at all |
| CM2 per order, whole store | $5.90 | $5.55 | Blended number moves less than either row above; reading it alone would have hidden the trade entirely |

Note in the review: the conversion win is real and the waterfall says it is not yet worth its return cost on this SKU set; owner to bring a category-level cap or a restocking fee to next cycle's review rather than rolling the eligibility change back blind.

## 3. Counter-metrics and guardrails

<!-- What we refuse to sacrifice for the headline. A win that trashed a guardrail is
     not a win. -->

Threadmere is the merchant of record, so inventory risk, returns, tax collection and consumer-protection liability all sit on the brand, not a marketplace. The guardrails below are the ones that can fail quietly between quarters.

| Guardrail metric | Threshold | This window | Breached? |
|---|---|---|---|
| Return rate overall | Must not rise above 23% | 26% | yes |
| Return rate by size band, fit counter-metric (the rows that matter, because overall averages hide the band the eligibility change touched) | Each band must not rise above 30% | see band table below | yes, bands 3 and 4 |
| CM2 per order, whole store | Must not fall below $5.50 | $5.55 | no, close |
| Chargeback ratio, both card schemes | Must not rise above 0.90% of transactions in a rolling 120-day window | 0.62% | no |
| Checkout session completion at peak hour | Must not fall below 90% | 94% | no |
| Economic-nexus threshold headroom, per state | Must not be crossed without a registered collection path in place | see nexus note below | needs verify |

Return rate by band, ILLUSTRATIVE, drawn from the returns engine and cross-checked against order and return records for the window. Bands follow Threadmere's size curve (1, 2, 3, 4, 5+), not one band per SKU, because SKUs multiply past usefulness.

| Size band | Return rate, prior window | Return rate, this window | Movement | Share of orders returned on free-returns SKUs this window | Read |
|---|---|---|---|---|---|
| Band 1 (fits stable) | 13% | 15% | +2 pts | 45% | Noise; band 1 was barely touched by the eligibility change |
| Band 2 (fits stable) | 18% | 19% | +1 pt | 51% | Noise |
| Band 3 (fit-sensitive) | 27% | 33% | +6 pts | 63% | The eligibility change widened into a fit-sensitive band, which is the fold-in |
| Band 4 (fit-sensitive) | 29% | 34% | +5 pts | 61% | Same pattern as band 3, on the other fit-sensitive band |
| Band 5+ (fit-sensitive) | 31% | 34% | +3 pts | 58% | Smallest order count, so read this row as direction only |

Read the band table the way the [Ecommerce](../knowledge/domains/ecommerce.md) card warns: an average hides two trends, and here the average (26%) masks the fact that bands 1 and 2 moved a point while bands 3 and 4 moved five and six points. The eligibility change did not break returns everywhere; it broke returns where fit is unstable, which is exactly the fold-in the fashion side of this domain forces on the waterfall.

Nexus guardrail, regulatory statement as of 2026-09-11, not legal advice, confirm with counsel before Threadmere acts on this row. Since South Dakota v. Wayfair (2018), US states can require sales tax collection on volume alone, with no physical presence in the state, and the obligation arrives silently. Threadmere added a new state to the shipping footprint on 2026-08-02, and the guardrail row above is marked needs verify because the cumulative-order-count measurement for that state sits between the registrations meeting on 2026-09-04 and the next one; the review records the flag rather than a conclusion. Threadmere's position in that state is being confirmed with counsel; the review does not state whether the threshold has or has not been crossed. This row is a guardrail, not a finding, and it carries no dollar figure because the state's economic-nexus threshold is not one of the numbers the working sheet fixed.

## 4. What we predicted vs what happened

<!-- The retro section. Pull the load-bearing assumptions from
     ../definition/assumptions-register.md and grade them. This table is where the
     team actually learns; skipping it turns the review into a scoreboard. -->

The load-bearing assumptions, drawn from the assumptions register for the free-returns widening decision (2026-08-08) and the Q3 sheet signed 2026-06-26:

| Assumption or prediction at launch | What actually happened | Held / Broke | What we change because of it |
|---|---|---|---|
| Widening free-returns eligibility raises checkout step 3 conversion above 3.10% | Conversion hit 3.42%, above the 3.10% target | Held | Keep the conversion mechanism, narrow the eligibility set rather than the mechanism |
| The widened SKU set would not move return rate above 23% | Return rate rose to 26% overall, and 33% to 34% on the fit-sensitive bands | Broke | Narrow free returns to fit-stable categories (section 5) |
| CM2 per order would hold above $5.50 while the eligibility widened | CM2 landed at $5.55, above the floor but short of the $6.10 target | Broke against target, held against the guardrail | Treat $6.10 as the Q4 target rather than a Q3 miss to forgive |
| Adding a key result mid-window (KR-3, 2026-08-08) would not distort the sheet | KR-3 was added, its ceiling was breached, and the sheet's Q3 comparison now has a row the Q3 sign-off never saw | Broke | Next sheet carries the eligible-SKU share as a standing key result from the start, not as a mid-quarter addition |

- The most surprising thing in the data this window: the whole CM2 movement sat in the returns line and not in fulfilment, payment processing, marketing or COGS, over a quarter in which the customer-facing conversion story looked like a clean win.
- What we will stop doing, based on the above: widening free-returns eligibility by SKU share. The eligibility rule moves to fit-stable categories only, decided in section 5, and no further eligibility widening runs before the next review.

## 5. Decision

<!-- One of three words, with a named decider. "Keep watching" is only legal with a
     date on it, otherwise it is sunset denial. -->

- **Decision:** PIVOT, on the free-returns widening only. The conversion work itself stays.
  - Persist: outcomes are moving toward target; continue and set the next review date
  - Pivot: the problem is real but this approach is not working; name what changes and take it back to DISCOVER. Here the problem (low step 3 conversion) is real and the approach (wide-by-SKU free returns) is not working on the margin it was supposed to protect, so the approach changes and the conversion mechanism is kept.
  - Sunset: the outcome is not worth the ongoing cost; name the wind-down owner and date
- Decider: Isabela Duarte, head of product · Date: 2026-10-07
- If persist: next review date: not applicable, this is a pivot on the free-returns scope and the next scheduled review is 2026-01-06
- If pivot: what changes, and the new discovery document: free-returns eligibility narrows to fit-stable categories (bands 1 and 2, which moved a point each while bands 3 and 4 moved five and six), and a category-level cap replaces the SKU-share ceiling, with a restocking fee on fit-sensitive returns carried to the next cycle's review as a candidate rather than a decision. The narrowed scope reopens the fit-sensitive bands to a DISCOVER pass, documented in a discovery document for the free-returns scope, to be opened by Isabela Duarte before the next review date.
- If sunset: not applicable this review.

The narrowed scope is the fashion fold-in the brief calls for: return rate by size band is what makes fit-stable categories the right cut, because the bands that moved were the fit-sensitive ones and the bands that did not move were the fit-stable ones.

## How this review fails

<!-- A metrics review that reports movement and decides nothing is the most
     expensive recurring meeting a product team holds, because it feels like
     governance. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Movement without cause | An arrow moved, and nobody says why or admits they do not know | Each change carries one sentence of cause, or is explicitly marked unexplained. Here the CM2 movement is attributed to the returns line, and the band table is attributed to the eligibility change |
| Compared to last period, not to target | The table shows this month against last, and no target column | Every row carries the target it was committed against. The waterfall rows in section 2 carry prior and this window, and the free-returns rows carry a signed target |
| Averages that hide two trends | One number improves while two segments move in opposite directions | Split by the segments that behave differently, not by the ones that are easy. Section 3 splits return rate by size band, which is the split that behaves differently, not by SKU |
| Definitions changed quietly | A metric halves because it is now counted differently, with no note | Version the definition and flag any change at the top of the review. CM2's returns provision was revised on 2026-08-14; the change is flagged in KR-2's confidence note, not left silent |
| No decision | It ends with a recap and the next invitation | It ends with act, watch or stop, recorded against a name. Section 5 records PIVOT against Isabela Duarte's name with a date |

## Exit gate

<!-- Checkable by someone who did not write this document, which is the
     test of whether a gate is a gate. -->


Gate 6 is satisfied when:

- [x] Every KR row has an actual and a data-confidence note. Three rows, three confidence notes, including the medium note on KR-2's revised returns provision
- [x] Input metrics are mapped to the KRs they were supposed to drive, with an honest "did it?". Section 2 maps the two headline inputs to KR-1 and carries the waterfall layers as the input metrics that explain KR-2
- [x] Guardrail metrics are reported, including breaches. Section 3 reports the return-rate breach and the return-rate-by-band breach, plus the nexus row marked needs verify rather than resolved
- [x] Section 4 grades real launch assumptions, not retrofitted ones. All four rows come from the assumptions register entries dated 2026-06-26 and 2026-08-08, before the window closed
- [x] The decision is one of the three words, with a named decider and the follow-through fields filled. PIVOT, Isabela Duarte, 2026-10-07, with the narrowed scope and the discovery document named

Signed: Isabela Duarte, head of product, 2026-10-07
