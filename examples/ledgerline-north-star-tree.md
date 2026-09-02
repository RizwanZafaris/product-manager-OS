# North Star Input Tree: Expense Copilot

Fills [frameworks/metrics/north-star-input-tree.md](../frameworks/metrics/north-star-input-tree.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the copilot is the fictional internal product used across this repository, the owners are roles, and every current value and target is ILLUSTRATIVE, present to show how a tree is filled and checked, not to suggest what any product should measure or hit. Built after Gate 2 and before launch, which is why the current values are baselines and zeros. Method background in the [north star card](../knowledge/north-star-metric.md). See the [examples index](README.md).

**Owner:** the PM · **Date:** 2026-09-01 · **Reviewed with:** the finance lead, the engineering lead, the data analyst

## 1. The north star

| Field | Answer |
|---|---|
| Metric | Copilot-drafted expense reports approved on first submission, per month |
| Customer value it expresses | A filer got the report done in one sitting and it did not come back; a reviewer got a report that needed judgment, not arithmetic |
| Unit and period | Count of reports, calendar month |
| Source system | Finance system of record (approval event) joined to product analytics (draft id). The join does not exist yet; see Open |
| Current value | 0, pre-launch. Baseline across all reports: 62% of about 800 a month approved first time, so about 500 |
| Lead or lag | Lag: it moves after the inputs move, usually within the month |

Rejected candidates, kept so the reasoning survives: "reports drafted" (rises with usage even when the drafts are bad), "first-submission approval rate" (a rate hides adoption; ten perfect drafts is a 100% rate), and "reviewer hours saved" (real, but a benefit of the tree, not the value the filer came for).

## 2. Input metrics

| # | Input | Causal claim | Lead or lag | Owner | Current | Target (ILLUSTRATIVE) |
|---|---|---|---|---|---|---|
| 1 | Share of eligible reports started in the draft flow | More drafted reports means more that can be approved as drafted; the breadth dial | Lead | The PM | 0 | 50% by month two, 60% by month six |
| 2 | Extracted fields accepted without edit | Fields the filer did not touch are fields the reviewer rarely bounces; the quality dial | Lead | Engineering lead | eval set only | 90% of fields on the live receipt mix |
| 3 | Suggested category kept by the filer | Category mismatch is the top bounce reason; a kept suggestion that matches policy removes it | Lead | Finance admin, who owns the mapping | 0 | 85% kept |
| 4 | Median minutes from first receipt to submit | Faster than the spreadsheet on the first try or the month-end batchers do not come back; feeds input 1 | Lead | Design lead | 25, all reports, discovery timing | under 10 |
| 5 | First-submission approval rate on drafted reports | The rate the north star count is made of; the direct quality check | Lag | Finance lead | 62%, all reports | 80% |

Four leads and one lag is deliberate. The leads are dials a team can turn this sprint; input 5 is the rate that says whether turning them worked, and the north star is that rate times input 1 times report volume.

## 3. Sanity checks

| Check | Result | Reasoning |
|---|---|---|
| Value, not vanity: would it fall within the quarter if customers stopped benefiting? | Pass | If extraction degrades, reviewers bounce and the count falls that month; if filers abandon the draft flow, the count falls the next month. It cannot only go up |
| Moves within a quarter | Pass | Monthly count; the inputs are per-sprint dials |
| No single metric hides a leak | Pass, with a companion | The count rises with travel volume alone in a busy quarter. Companion on the same dashboard: the count as a share of all reports, so a seasonal rise shows as a flat share |
| Exactly one owner per input | Pass | Roles above. The finance admin owns input 3 because the mapping is theirs, not engineering's |
| Three to five inputs | Pass | Five. A sixth, "receipts forwarded by email", was cut; it is an input to input 1, not to the north star |

## 4. Guardrails

| Guardrail | Floor or ceiling | Who calls the halt | What bad win it prevents |
|---|---|---|---|
| Reviewer-caught extraction errors per 100 drafted reports | Under 3, and never rising two months running | Engineering lead | A count that rises because reviewers stopped checking |
| Reports submitted without the filer's review step | 0, always | The PM | Adoption bought by removing the accountability the expense policy requires |
| Kept category suggestions later corrected by finance | Under 5 per 100 drafted reports | Finance admin | Input 3 rising because the suggestion is easy to accept, not because it is right |

## 5. Review cadence

Monthly, at the [metrics review](../templates/operate/metrics-review.md), starting four weeks after launch, run by the PM with the data analyst. Standing questions: did each input move; did the north star follow; which causal claim looks weakest. The claim expected to fail first is input 4's: filing time may fall without adoption rising, if the batchers' habit is stronger than the interviews suggested. If it fails, input 4 becomes a guardrail and the adoption dial gets a new input.

## Open

- [OPEN: the join between finance approvals and product draft ids does not exist. Until the analytics instrumentation spec is written and shipped, the north star cannot be computed and this tree is a hypothesis. The data analyst owns the spec; the engineering lead owns shipping it before launch, because a north star named before it can be measured is a slogan.]
- [OPEN: input 2's current value comes from the labeled eval set, not live receipts. The live figure is unknown until the first month of data; the engineering lead owns replacing it.]

## Feeds

- [templates/planning/north-star-metric.md](../templates/planning/north-star-metric.md): sections 1 to 4 fill straight across.
- [templates/planning/okrs.md](../templates/planning/okrs.md): the quarter's key results are inputs 1, 2, and 5.
- [templates/delivery/analytics-instrumentation-spec.md](../templates/delivery/analytics-instrumentation-spec.md): every input and guardrail above needs an event in it.
- Method: [knowledge/north-star-metric.md](../knowledge/north-star-metric.md), and the blank worksheet at `frameworks/metrics/north-star-input-tree.md`.
