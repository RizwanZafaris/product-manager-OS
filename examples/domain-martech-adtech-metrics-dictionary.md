# Metrics Dictionary: Kestrion Demand-Side Platform

Fills [templates/operate/metrics-dictionary.md](../templates/operate/metrics-dictionary.md). Everything here is invented for this standalone example: Kestrion is a fictional demand-side advertising platform, Priya N. its only fictional measurement lead, and every number, name and date is ILLUSTRATIVE, not drawn from any real company or market. There is no external martech-adtech journey or data sheet. See the [examples index](README.md).

**Owner:** Priya N., measurement lead · **Analytics counterpart:** David Chen, data engineering · **Last updated:** 2026-09-11 · **Source of truth:** Snowflake warehouse, schema `kestrion_measurement` · **Status:** In use

## 1. Conventions and entities

- **Id format:** M-[three digits]; ids are never reused, and a changed definition gets a new id or a version suffix
- **Time grain and timezone:** daily, in UTC; weeks start Monday
- **Rounding and display:** two decimal places for rates and ratios; integers for counts; percentages displayed with one decimal place (e.g., 12.4%)
- **Attribution convention:** Every metric that assigns credit to a touchpoint must explicitly record its attribution model (e.g., last-touch, linear) and its lookback window (e.g., 7-day click / 1-day view) in the definition column. Two teams reporting "conversions" without these qualifiers will report different numbers for the same word.

| Entity | Definition | Source table | Known ambiguities |
|---|---|---|---|
| User | A distinct human device/browser combination identified by a consented identifier (IDFA, GAID, or hashed email) where available, otherwise an anonymous session ID | `dim_user_identity` | Internal test accounts (flagged via IP allowlist) are excluded. Safari/Firefox users often lack persistent IDs, relying on ephemeral session IDs which may fragment a single user into multiple records. |
| Account | The advertiser entity purchasing media through Kestrion | `dim_advertiser_account` | Agencies managing multiple brands share one account login but have separate billing entities; metrics are reported at the brand level (`brand_id`) not just the account level. |
| Conversion Event | A post-click or post-view action defined by the advertiser as valuable (purchase, signup, lead) occurring within the attribution window | `fact_conversion_events` | Delayed conversions (e.g., offline sales matched later) may appear after the initial daily job runs; late arrivals are backfilled up to 30 days past the conversion timestamp. |

## 2. The register

| Id | Metric | Type | Definition in one sentence | Formula (numerator / denominator, filters) | Grain | Source (events or tables) | Owner | Refresh and latency | Known gaps | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| M-001 | Last-touch attributed conversions | diagnostic | Count of conversions credited to Kestrion by the last-touch model within a 7-day click / 1-day view window | count(conversion_event where last_touch_source = 'kestrion' AND time_diff <= 7d_click OR 1d_view) | daily | `fact_conversion_events`, joined via `device_graph_match` | Priya N. | Daily job, ~18 hours behind | Model is contractual per advertiser; M-001 for Advertiser A (last-touch) is not comparable to Advertiser B (linear). iOS ATT opt-in rate limits matchable conversions. | agreed |
| M-002 | View-through conversions | diagnostic | Count of conversions credited to Kestrion where the user saw an ad but did not click, within a 1-day view window | count(conversion_event where last_touch_type = 'view' AND time_diff <= 1d) | daily | `fact_conversion_events`, `fact_impressions` | Priya N. | Daily job, ~18 hours behind | Highly sensitive to window length; no causal link established. Often inflated by organic demand intercepting ads shown shortly before natural purchase intent. | agreed |
| M-003 | Incremental conversions (Geo Holdout) | guardrail | Lift in conversion rate in served regions compared to matched holdout regions receiving no bids | (served_rate - holdout_rate) / holdout_rate | per campaign, at close | `holdout_randomization_log`, `fact_conversion_events` | Priya N. | At campaign close only | Undercounts Safari/Firefox users due to cookie loss, biasing lift estimate toward zero for those browsers. Requires sufficient sample size; small campaigns yield wide confidence intervals. | in use |
| M-004 | Incremental ROAS | north star | Return on ad spend calculated using incremental revenue from holdout tests over total spend | (incremental_conversions * avg_order_value) / total_spend | monthly | M-003 output, `fact_billing` | Priya N. | Monthly, 5 days after month end | Depends entirely on M-003 validity. If holdout design is flawed, this number is meaningless. Not available for all campaigns due to cost. | draft |
| M-005 | Identity Match Rate | input | Share of inbound conversion events successfully joined to a known user identity | count(matched_conversions) / count(total_inbound_conversions) | daily | `fact_conversion_events`, `dim_user_identity` | David Chen | Daily, ~6 hours behind | Drops silently as platforms remove identifiers (e.g., Chrome cookie deprecation). A stable series usually means the definition changed, not that matching improved. | in use |
| M-006 | Consent Rate (TCF/GPP) | input | Share of ad requests carrying a valid Transparency and Consent Framework (TCF) string or Global Privacy Platform (GPP) signal permitting personalization | count(requests_with_valid_tcf_or_gpp) / count(total_requests) | daily | `log_bid_requests` | David Chen | Real-time dashboard, ~5 minutes lag | Banner design heavily influences this; high rates may indicate dark patterns. Regulators read easy refusal paths as mandatory. | in use |
| M-007 | Identifier Availability | diagnostic | Percentage of ad impressions served where a deterministic or probabilistic identifier was present and usable | count(impressions_with_id) / count(total_impressions) | daily | `log_impression_events` | David Chen | Daily, ~12 hours behind | Varies significantly by OS and browser. iOS App Tracking Transparency (ATT) opt-in rates are low (~20-30% industry average), capping this metric's ceiling. | in use |

## 3. Segments and filters

| Segment id | Segment | Definition | Applies to metric ids |
|---|---|---|---|
| S-01 | iOS Users | Users on devices running iOS 14.5+ with App Tracking Transparency framework active | M-001, M-002, M-005, M-007 |
| S-02 | EU Traffic | Requests originating from IP addresses in European Economic Area countries | M-006, M-005 |
| S-03 | High-Intent Categories | Campaigns targeting shopping or travel verticals where organic demand interception risk is highest | M-001, M-002, M-003 |

## 4. Lineage

| Metric id | Feeds (metric id or key result) | Fed by (metric ids) | Lead or lag |
|---|---|---|---|
| M-004 | KR: Achieve 3.5x Incremental ROAS | M-003, Total Spend | Lag |
| M-003 | M-004 | M-001 (baseline), Holdout Data | Lag |
| M-001 | M-003 (comparison baseline) | Conversion Events, Attribution Model | Lead |
| M-005 | M-001, M-002, M-003 (data quality gate) | Identity Graph, Device Signals | Lead |
| M-006 | M-005, M-007 (eligibility filter) | CMP Logs, TCF Strings | Lead |

## 5. Known gaps and open questions

| Gap | Metric ids affected | Effect (overcounts / undercounts / unknown) | Fix | Owner | By when |
|---|---|---|---|---|---|
| iOS App Tracking Transparency opt-in rates remain low (approx. 25%), limiting deterministic matching | M-001, M-002, M-005, M-007 | Undercounts true conversions on iOS; biases performance metrics toward Android/Web | Adopt Privacy Sandbox APIs for aggregated measurement; rely more on M-003 geo-holdouts for iOS campaigns | Priya N. | Ongoing |
| Google abandoned Chrome-wide third-party cookie deprecation and wound down Privacy Sandbox in 2026; cookie-based matching is not going away on the timeline this dictionary was built against, but the reversal itself could be revisited under regulatory pressure | M-005, M-007 | Overstates the urgency baked into current fallback plans; the M-005/M-007 gap driven by iOS ATT opt-in (see the row above) is now the larger and more durable driver of match-rate decline than Chrome cookies | Retire the Privacy Sandbox contingency plan as the primary mitigation; keep server-side tracking work for the iOS gap instead; re-open this row if Chrome policy changes again | David Chen | 2026-10-01 |
| Last-touch model flatters channels that intercept existing demand | M-001, M-002 | Overcounts contribution of retargeting/search; understates upper-funnel awareness | Mandate M-003 (Incremental Conversions) review for all budget allocation decisions >$50k/month | Priya N. | 2026-11-01 |

## 6. Change log

| Date | Metric id | Change | Why | Old versus new value for the last period | Announced where |
|---|---|---|---|---|---|
| 2026-08-15 | M-001 | Lookback window changed from 14-day click / 1-day view to 7-day click / 1-day view | Align with industry standard for short-cycle e-commerce; previous window captured too much organic noise | Old: 12,400 conv; New: 11,850 conv (-4.4%) | Weekly Measurement Review meeting, Slack #kestrion-metrics |
| 2026-07-01 | M-005 | Added exclusion for Safari Private Relay traffic | Private Relay masks IPs, making probabilistic matching unreliable and potentially non-compliant with some interpretations of consent | Old: 82.0% match rate; New: 79.0% match rate (-3.0 pts) | Engineering changelog, Client Success update |

---

## Exit gate (feeds Gate 6: outcomes verified)

Done when every box is honestly ticked. The dictionary is the reference every tile in [dashboard-spec.md](../templates/operate/dashboard-spec.md) and every row in [metrics-review.md](../templates/operate/metrics-review.md) cites at [Gate 6](../os/STAGE-GATES.md).

- [x] Every metric a dashboard, review, or update shows has a row here with an id
- [x] Every formula names numerator, denominator, and filters, and reads events or tables that exist in the instrumentation spec
- [x] Every row has an owner and a refresh with its latency
- [x] Every row's known-gaps cell is filled, or says "none found on [date]"
- [x] Entities are defined once in section 1 and every formula uses them
- [x] The north star and its inputs are typed and connected in the lineage table
- [x] Every definition change is in the change log and was announced before it landed
- [x] The ILLUSTRATIVE row has been deleted
- [x] Signed by Priya N., 2026-09-11
