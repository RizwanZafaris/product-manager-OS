# Metrics Dictionary: [product name]

Stage: OPERATE, feeds [Gate 6: outcomes verified](../../os/STAGE-GATES.md); first written in DEFINE, before the instrumentation spec, and maintained for the life of the product
Knowledge: [north star input tree](../../frameworks/metrics/north-star-input-tree.md)
Skill: [metrics-tree](../../skills/metrics-tree/SKILL.md); the [analyst agent](../../agents/analyst-agent.md) keeps the definitions honest

> **Delete any section you do not need.** A single feature with two metrics fills section 2 and stops. The full form is the product-wide dictionary that every dashboard, review, and board update cites by metric id. Never leave a heading standing over white space.

<!-- One row per metric anyone reports, defined precisely enough that two people
     computing it get the same number. Every dashboard tile and every metrics
     review row cites an id from here; a number that exists without a row here is a
     number nobody can check.

     Neighbours: north-star-metric.md (../planning/north-star-metric.md) chooses the
     metric and its inputs; the analytics instrumentation spec
     (../delivery/analytics-instrumentation-spec.md) specifies the events the
     formulas read; the dashboard spec (dashboard-spec.md) lays out the tiles that
     cite these ids; the metrics review (metrics-review.md) reads the numbers.

     Fill first: the register in section 2 for the north star and its inputs, then
     the known-gaps column of every row, then the entities in section 1. -->

**Owner:** [name] · **Analytics counterpart:** [name] · **Last updated:** [YYYY-MM-DD] · **Source of truth:** [warehouse and schema] · **Status:** Draft / Agreed / In use

## 1. Conventions and entities

<!-- Definitions that every formula below assumes. Most dictionary disputes are
     entity disputes wearing a metric's name: two teams agree on "active accounts"
     and disagree on "account". -->

- **Id format:** M-[three digits]; ids are never reused, and a changed definition gets a new id or a version suffix
- **Time grain and timezone:** [daily / weekly / monthly, in [timezone]; weeks start [day]]
- **Rounding and display:** [decimals, percent versus ratio]

| Entity | Definition | Source table | Known ambiguities |
|---|---|---|---|
| User | | | [e.g. whether internal staff and test accounts are excluded, and how] |
| Account | | | |
| [Expense report, or your core object] | | | |

## 2. The register

<!-- Type: north star, input, guardrail, or diagnostic. Formula names numerator,
     denominator, and filters; "engagement" with no formula is not a metric.
     Refresh includes latency, because a daily job that lands at noon makes
     "yesterday" mean two days ago at 9 am. The italic row is ILLUSTRATIVE. -->

| Id | Metric | Type | Definition in one sentence | Formula (numerator / denominator, filters) | Grain | Source (events or tables) | Owner | Refresh and latency | Known gaps | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |
| *M-004* | *reports submitted without edit (ILLUSTRATIVE)* | *input* | *share of submitted expense reports whose extracted fields the submitter did not change* | *count(report_submitted where edit_count = 0) / count(report_submitted), excluding test accounts* | *weekly* | *report_submitted event, instrumentation spec section 2* | *[name]* | *daily job, about 24 hours behind* | *mobile client below version [n] does not send edit_count; those reports count as edited* | *agreed* |

## 3. Segments and filters

<!-- A segment is defined once here and reused by id on every dashboard. A segment
     defined per dashboard is a future argument about why two charts disagree. -->

| Segment id | Segment | Definition | Applies to metric ids |
|---|---|---|---|
| S-[n] | | | |

## 4. Lineage

<!-- The tree from the north star worksheet, as rows. Every input feeds something;
     every key result in the OKR sheet is fed by something. An orphan in either
     direction is a finding. -->

| Metric id | Feeds (metric id or key result) | Fed by (metric ids) | Lead or lag |
|---|---|---|---|
| | | | |

## 5. Known gaps and open questions

<!-- Gaps are stated per row in section 2 and collected here with a fix. Effect
     says which way the number is wrong; a gap with unknown direction is a
     confidence note on every chart that uses the metric. -->

| Gap | Metric ids affected | Effect (overcounts / undercounts / unknown) | Fix | Owner | By when |
|---|---|---|---|---|---|
| | | | | | |

## 6. Change log

<!-- A definition change is announced before it lands, with the old and new value
     side by side for one period. Silent redefinition is how a metric "improves"
     in a quarter nothing shipped. -->

| Date | Metric id | Change | Why | Old versus new value for the last period | Announced where |
|---|---|---|---|---|---|
| | | | | | |

---

## Exit gate (feeds Gate 6: outcomes verified)

Done when every box is honestly ticked. The dictionary is the reference every tile in [dashboard-spec.md](dashboard-spec.md) and every row in [metrics-review.md](metrics-review.md) cites at [Gate 6](../../os/STAGE-GATES.md).

- [ ] Every metric a dashboard, review, or update shows has a row here with an id
- [ ] Every formula names numerator, denominator, and filters, and reads events or tables that exist in the instrumentation spec
- [ ] Every row has an owner and a refresh with its latency
- [ ] Every row's known-gaps cell is filled, or says "none found on [date]"
- [ ] Entities are defined once in section 1 and every formula uses them
- [ ] The north star and its inputs are typed and connected in the lineage table
- [ ] Every definition change is in the change log and was announced before it landed
- [ ] The ILLUSTRATIVE row has been deleted
- [ ] Signed by [name], [date]
