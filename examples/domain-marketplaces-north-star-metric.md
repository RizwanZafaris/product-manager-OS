# North Star Sheet: Gatherwell

Fills [templates/planning/north-star-metric.md](../templates/planning/north-star-metric.md). Everything here is invented for this standalone example: Gatherwell is a fictional UK two-sided home-services marketplace matching households with cleaners and trades, Priya Anand its only fictional product manager, and every number, name and date is ILLUSTRATIVE, not drawn from any real platform or market. There is no external Gatherwell journey or data sheet. See the [examples index](README.md).

**Owner:** Priya Anand · **Date:** 2026-09-11 · **Vision:** not filled for this example (ILLUSTRATIVE)

## 1. The metric

| Field | Answer |
|---|---|
| North star metric | Liquidity: share of active listings that transact within 14 days (percent) |
| The customer value it expresses | A household finds a provider who actually shows up and completes the job; a provider gets paid for work they did. It measures the probability that a match becomes money changing hands on-platform, which is the only outcome both sides care about. |
| Vanity test | If providers stop getting jobs or households stop booking, this percentage falls immediately because listings sit idle and searches end without transactions. GMV can rise while this falls if subsidy inflates average order value on listings that were already transacting, without recruiting new listings into the transacting share. Subsidy can still inflate liquidity itself, by forcing a marginal booking that would not otherwise happen; that is why this metric is paired with the guardrails below, not trusted alone: a subsidized booking that fails to clear the gross-margin-per-subsidy floor, or that fails a safety review, is caught by those two guardrails directly. A forced booking that never becomes a repeat pair does not show up in a guardrail at all; it shows up as a stall in the on-platform repeat-booking input metric (section 2), which is the signal to distrust a liquidity gain that subsidy alone produced. |
| Source system | Core Transaction Ledger, query `liquidity_14d_active_listings` |
| Current value | 34% (ILLUSTRATIVE, measured as of 2026-08-31) |

## 2. Input metric tree

| Input metric | Causal claim (how it feeds the north star) | Owner (one name) | Current | Target |
|---|---|---|---|---|
| Provider response time (median minutes to first reply) | Faster replies reduce drop-off between search and booking, directly increasing the share of listings that transact within the 14-day window; slow responses are the primary leak in the supply-side funnel | Head of Supply Ops, Marcus Chen | 45 min | <15 min |
| Verified providers per category and area (count) | More verified supply in a specific geography/category increases the chance a household’s search returns a bookable option, raising transaction probability; background-check turnaround runs through the UK's DBS (Disclosure and Barring Service) flow, so verification speed is a bottleneck to expanding this input (as of 2026-09-11, confirm with counsel) | Head of Trust & Safety, Elena Rodriguez | 120 per major metro | 200 per major metro |
| Search-to-booking rate (percent) | Higher conversion from search to booking means more attempts become transactions, directly lifting the numerator of the liquidity ratio; friction in booking flow or lack of trust signals suppresses this rate | Head of Product, David Kim | 8.5% | 12% |
| On-platform repeat-booking rate (percent of bookings from returning pairs) | Repeat bookings indicate satisfied matches and reduce disintermediation risk; higher retention keeps transactions on-platform where they count toward liquidity, whereas off-platform leakage removes them from the measure entirely | Head of Growth, Sarah Jenkins | 23% | 35% |

## 3. Guardrails

| Guardrail metric | Floor or ceiling | Who calls the halt | Why it guards |
|---|---|---|---|
| Gross margin contribution per subsidy pound | Floor: £1.20 | CFO, James Wright | Prevents chasing liquidity with unprofitable subsidies that inflate GMV without sustainable unit economics; if every pound of subsidy generates less than £1.20 in gross margin contribution, growth is destroying value. Margin, not GMV, is the comparable unit against a subsidy cost |
| Provider earnings per hour | Floor: £14.50 | Head of Supply Ops, Marcus Chen | Protects the constrained side’s willingness to stay; if earnings fall below local living wage benchmarks, providers churn, collapsing liquidity even if short-term booking volumes look healthy |
| Safety incidents per 1,000 jobs | Ceiling: 0.5 | Head of Trust & Safety, Elena Rodriguez | Ensures rapid liquidity growth does not compromise vetting standards; DBS checks and UK GDPR-compliant handling of provider records must not be skipped or delayed to hit targets, as regulatory exposure and user harm outweigh metric gains (as of 2026-09-11, confirm with counsel) |

## 4. Review cadence

- **Cadence:** Monthly, plus each Gate 6 review
- **Standing questions:** Did each input move? Did the north star follow? Which causal claim looks weakest? What replaces it if it fails?
- **Last review:** 2026-08-15, metrics review not filled for this example (ILLUSTRATIVE)
- **Next review:** 2026-10-15, run by Priya Anand

## Exit gate

This sheet is fit to steer by when:

- [x] The north star passes the written vanity test and is computed by a named source system
- [x] Every input carries a causal claim and exactly one named owner
- [x] There are three to five inputs, not a dashboard's worth
- [x] At least one guardrail exists, with a numeric floor and a named halt-caller
- [x] The review cadence is scheduled with an owner, not left as an intention
- [x] OKRs and PRD success metrics in flight trace to this tree, or the mismatch is logged

Signed: Priya Anand, Product Manager, 2026-09-11
