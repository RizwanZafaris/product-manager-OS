# Metrics Dictionary: Pitchline Sports

Fills [templates/operate/metrics-dictionary.md](../templates/operate/metrics-dictionary.md). Everything here is invented: Pitchline Sports is a fictional online sportsbook and casino, Priya Osei its only fictional trading analytics lead, Marcus Deane its fictional compliance officer, and every number, name, date and regulatory citation used for illustration is ILLUSTRATIVE; the regulatory statements reflect positions as of 2026-09-11, are confirm-with-counsel items, not legal advice, and are not attributed to any real operator or regulator acting improperly. See the [examples index](README.md).

**Owner:** Priya Osei, Trading Analytics Lead · **Analytics counterpart:** Dana Whitlock, VP Engineering · **Last updated:** 2026-10-08 · **Source of truth:** pitchline_dw warehouse, schema `metrics_v3` · **Status:** In use

## 1. Conventions and entities

This section sets the two conventions every formula below assumes. Most disputes in this dictionary are convention disputes wearing a metric's name, so they are settled once, here, before any row is written.

- **Jurisdiction on every money metric.** An operator sells wagers in several places and pays a different tax, with a different taxable definition, in each: New Jersey, Pennsylvania and Ontario each have their own regulator, and what counts as taxable differs between them (the [sports betting and iGaming card](../knowledge/domains/sports-betting-igaming.md) names AGCO, iGaming Ontario, New Jersey's regulator and the other state gaming commissions as gatekeepers). So every money metric states its jurisdiction in its name, and a figure quoted without one is incomplete, not merely informal.
- **Promotional deduction, stated on every money metric.** A bonus sits between handle and NGR, not on top of it (the [domain card](../knowledge/domains/sports-betting-igaming.md), metric "Handle", how it lies). Whether a money metric has redeemed promotional credits deducted changes its value, so each metric says so in its definition: GGR is always gross, with no promo deduction (section 5); NGR is always net of redeemed promotional credits (M-014, M-015, M-016); every other money metric states its own choice. Section 6 logs the one case where that choice changed, after a change in Ontario's revenue-share treatment.
- **Id format:** M-[three digits]; ids are never reused, and a changed definition gets a new id or a version suffix
- **Time grain and timezone:** daily at close of each jurisdiction's own day, in the jurisdiction's local timezone (ET for NJ and PA, ET for Ontario); weeks start Monday; weekly and monthly rows sum daily grain and inherit its timezone rule
- **Rounding and display:** currency to whole dollars; percentages to one decimal place; ratios to three decimal places

| Entity | Definition | Source table | Known ambiguities |
|---|---|---|---|
| Account | A verified customer account holding one KYC identity, after age and identity verification and a self-exclusion check against the active jurisdiction's register cleared | `accounts` | Two accounts sharing one verified identity ("multi-accounting") count as two here but one in the anti-bonus-abuse view; test and staff accounts are excluded via the `is_internal` flag set at account creation |
| Active account | An account funding at least one accepted bet in the period; the denominator for all per-1,000 rates | `accounts_active` | A bet accepted then voided before settlement does not make the account active that period |
| Bet (wager) | One accepted stake on a priced market, the atomic unit of handle | `bets` | In-play wagers placed after an event ends but before the market closed are counted as placed in-play and reconciled against the settlement file later |
| Handle | Total stake accepted on all bets placed | sum of `bets.stake` | Whether voided-bet stakes are included or netted; here voided stakes are netted out |

## 2. The register

| Id | Metric | Type | Definition in one sentence | Formula (numerator / denominator, filters) | Grain | Source (events or tables) | Owner | Refresh and latency | Known gaps | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| M-001 | Handle, NJ online sportsbook | diagnostic | Total stake accepted on New Jersey-licensed sportsbook wagers | sum(bets.stake), filtered to market_id NJ, geolocate_passed = true, is_void = false | daily | bet_settled, NJ market only | Priya Osei | daily job at 06:00 ET, about 6 hours behind close of the previous NJ day | in-play bets placed after event end but before market close counted as placed; reconciled T+1 | agreed |
| M-002 | Gross gaming revenue, NJ online sportsbook | diagnostic | NJ handle minus winnings paid, with no promotional deduction at any stage (section 5) | sum(bets.stake) minus sum(bets.payout), filtered to market_id NJ, geolocate_passed = true, is_void = false; no promo deduction | daily | bet_settled, NJ market only | Priya Osei | daily, about 6 hours behind close | none found on 2026-10-08 | agreed |
| M-003 | Gross gaming revenue, PA online sportsbook | diagnostic | PA handle minus winnings paid, with no promotional deduction at any stage (section 5) | sum(bets.stake) minus sum(bets.payout), filtered to market_id PA, geolocate_passed = true, is_void = false; no promo deduction | daily | bet_settled, PA market only | Priya Osei | daily, about 6 hours behind close | none found on 2026-10-08 | agreed |
| M-004 | Gross gaming revenue, Ontario iGaming | diagnostic | Ontario handle minus winnings paid, with no promotional deduction at any stage (section 5) | sum(bets.stake) minus sum(bets.payout), filtered to market_id ON, geolocate_passed = true, is_void = false; no promo deduction | daily | bet_settled, ON market only | Priya Osei | daily, about 6 hours behind close | none found on 2026-10-08 | agreed |
| M-005 | Redeemed promotional credits, NJ online sportsbook | input | Face value of promotional credits actually redeemed against NJ wagers | sum(promo_credit_redeemed.value), filtered to market_id NJ, is_void = false | daily | promo_credit_redeemed, NJ market only | Dana Whitlock | daily, about 6 hours behind close | expired-unused credits are excluded here and tracked separately as M-006 | agreed |
| M-006 | Expired-unused promotional credits, NJ online sportsbook | diagnostic | Face value of promotional credits issued but never redeemed before expiry | sum(promo_credit_issued.value) minus sum(promo_credit_redeemed.value), filtered to market_id NJ and expiry_date before period end | daily | promo_credit_issued and promo_credit_redeemed, NJ market only | Dana Whitlock | daily, about 30 hours behind close of the credit's own expiry date, since a credit can redeem after its scheduled expiry | late redemptions after expiry are counted as expired here and reversed in reconciliation | agreed |
| M-014 | Net gaming revenue, NJ online sportsbook | input | GGR from New Jersey-licensed sportsbook wagers, after deducting redeemed promotional credits, before state gaming tax | stakes accepted minus winnings paid minus redeemed promotional-credit value, filtered to accounts geolocated in NJ at placement | daily | bet_settled and promo_credit_redeemed events, NJ market only | Priya Osei, Trading Analytics Lead | daily, about 6 hours behind close | deducts redeemed credits only; NJ's tax base (N.J.S.A. 5:12A-16, confirm with counsel) allows no promotional deduction at all, so this NGR runs below the taxable figure; reconciled monthly | agreed |
| M-015 | Net gaming revenue, PA online sportsbook | input | PA GGR after deducting redeemed promotional credits, before state gaming tax | (sum(bets.stake) minus sum(bets.payout)) minus sum(promo_credit_redeemed.value), filtered to market_id PA, geolocate_passed = true, is_void = false | daily | bet_settled and promo_credit_redeemed, PA market only | Priya Osei | daily, about 6 hours behind close | none found on 2026-10-08 | agreed |
| M-016 | Net gaming revenue, Ontario iGaming | input | Ontario GGR after deducting redeemed promotional credits, before provincial and federal tax | (sum(bets.stake) minus sum(bets.payout)) minus sum(promo_credit_redeemed.value), filtered to market_id ON, geolocate_passed = true, is_void = false | daily | bet_settled and promo_credit_redeemed, ON market only | Priya Osei | daily, about 6 hours behind close | Ontario's tax treatment of promotional deductions differs from NJ's (see section 6); confirm with counsel | agreed |
| M-020 | Hold percentage, per jurisdiction | diagnostic | Trading margin: GGR divided by handle, for one jurisdiction's market | M-002 or M-003 or M-004 divided by M-001 (matching jurisdiction), per jurisdiction and market_type | weekly | bet_settled, all markets | Priya Osei | weekly on Monday, about 2 days behind the period end it reports | swings with sporting results week to week; trend it over a season, not a week, or it lies | agreed |
| M-021 | Promotions as a share of GGR | input | Redeemed promotional credits divided by GGR, per jurisdiction, the real acquisition and retention cost of the promo programme | M-005 divided by M-002 (per jurisdiction, matched market filter) | weekly | promo_credit_redeemed and bet_settled | Priya Osei | weekly on Monday, about 2 days behind period end | a falling ratio can mean promo discipline or bonus abuse finally written off; read it against M-006, not alone | agreed |
| M-030 | Geolocation check failure rate, per jurisdiction | guardrail | Share of geolocation checks that return no verdict at all, so fail-closed applies and play is blocked | count(geolocate_check where outcome = fail_or_no_verdict) divided by count(geolocate_check), per jurisdiction | daily | geolocate_check events | Dana Whitlock | daily, about 2 hours behind close | a low failure rate can also mean an over-permissive check waving borderline signals through; read it paired with M-031, never alone | agreed |
| M-031 | Geolocation false-block rate, per jurisdiction | guardrail | Share of checks that blocked a real-money bet later shown, on appeal, to have been placed inside the licensed footprint | count(bet_blocked where outcome = false_block_upon_appeal) divided by count(geolocate_check where outcome = block), per jurisdiction | weekly | geolocate_check and bet_blocked events, plus the appeal table | Dana Whitlock | weekly, appeal-lagged, about 5 days behind period end | a bet blocked and never appealed does not surface here at all, so this is a floor, not the true rate | agreed |
| M-040 | RG interventions per 1,000 active accounts, per jurisdiction | guardrail | Responsible-gambling interventions triggered (deposit limit set, reality check, financial vulnerability check) per 1,000 active accounts, for one jurisdiction | count(rg_intervention) divided by count(distinct active account) times 1000, per jurisdiction | daily | rg_intervention and accounts_active | Marcus Deane | daily, about 24 hours behind close | a rise can mean better detection or more harm occurring; read it against player-outcome follow-up, never alone | agreed |
| M-041 | Self-exclusions per 1,000 active accounts, per jurisdiction | guardrail | New self-exclusions registered in the period per 1,000 active accounts, for one jurisdiction | count(self_exclusion_new) divided by count(distinct active account) times 1000, per jurisdiction | weekly | self_exclusion and accounts_active | Marcus Deane | weekly, about 24 hours behind period end | a self-exclusion that lapses and re-registers in the same period counts once, not twice | agreed |
| M-050 | Deposit success by method, per jurisdiction | input | Share of deposit attempts completed successfully, split by payment method, for one jurisdiction | count(deposit_completed) divided by count(deposit_attempt), grouped by method and jurisdiction | daily | deposit_attempt and deposit_completed events | Dana Whitlock | daily, about 12 hours behind close | a failed method can be a risk or fraud decision, not a technical failure; split by failure reason code before reading it | agreed |

## 3. Segments and filters

A segment is defined once here and reused by id on every dashboard and review row; a segment defined per dashboard is a future argument about why two charts disagree.

| Segment id | Segment | Definition | Applies to metric ids |
|---|---|---|---|
| S-1 | NJ market | market_id = NJ, geolocate_passed = true | M-001, M-002, M-005, M-006, M-014, M-020, M-030, M-031, M-040, M-041, M-050 |
| S-2 | PA market | market_id = PA, geolocate_passed = true | M-003, M-015, M-020, M-021, M-030, M-031, M-040, M-041, M-050 |
| S-3 | ON market | market_id = ON, geolocate_passed = true | M-004, M-016, M-020, M-021, M-030, M-031, M-040, M-041, M-050 |
| S-4 | First-90-day accounts | account age at period date under 90 days | M-001, M-014, M-015, M-016, M-021 |
| S-5 | High-risk deposit accounts | account flagged high-risk by the AML source-of-funds flow before funding | M-050 |

## 4. Lineage

| Metric id | Feeds (metric id or key result) | Fed by (metric ids) | Lead or lag |
|---|---|---|---|
| M-002 | M-014, M-020, M-021 | M-001 (via the NJ branch of M-002's own handle term) | lag |
| M-014 | KR-1 (net gaming revenue, all jurisdictions) | M-002, M-005 | lag |
| M-015 | KR-1 | M-003 | lag |
| M-016 | KR-1 | M-004 | lag |
| M-020 | KR-2 (trading margin) | M-001, M-002, M-003, M-004 | lag |
| M-021 | KR-2 (promo efficiency guardrail) | M-002, M-005 | lag |
| M-030 | KR-3 (geolocation control effectiveness) | none | lead |
| M-040 | KR-4 (player-harm guardrail) | none | lead |
| M-041 | KR-4 | none | lead |
| M-050 | KR-3, and the payments-availability review row | none | lead |

## 5. Known gaps and open questions

| Gap | Metric ids affected | Effect (overcounts / undercounts / unknown) | Fix | Owner | By when |
|---|---|---|---|---|---|
| Trading and Finance compute GGR on different scopes | M-002, M-003, M-004, M-020 | unknown, until a jurisdiction-month is reconciled side by side; the two can differ by the settlement-window and void-treatment rule each applies, and neither scope is "wrong", they answer different questions | Finance's scope (settled-only, tax-window aligned) becomes its own dictionary row, M-023, rather than a second, unwritten number with the same name; first reconciliation run before the next quarter close, ILLUSTRATIVE target 2026-12-15 | Priya Osei (trading scope) and Elena Marsh (Finance controller, Finance scope) | 2026-12-15 |
| M-005 excludes expired-unused credits, so M-021 can fall as bonus abuse is written off rather than as spend tightens | M-021 | overstates how well promo spend is controlled (a falling ratio can read as discipline when it is a write-off) | pair M-021 with M-006 on every promo-efficiency chart tile until the promo team's write-off convention is set | Dana Whitlock | 2026-11-30 |
| M-031 counts only appealed false blocks | M-031 | undercounts the true false-block rate | add an unappealed-block sampling audit, one jurisdiction per month | Dana Whitlock | 2026-11-30 |
| The NJ tax base treats promotional deductions differently from the trading-desk convention behind M-014 (N.J.S.A. 5:12A-16, as of 2026-09-11; confirm with counsel) | M-014 | this NGR undercounts the figure on NJ's tax return by the redeemed-promotion amount, a named, reconciled gap, not an error | keep M-014 as the trading-desk convention; publish the reconciled taxable figure as its own row, M-014-TX, alongside it, and stop using the bare label "NGR, NJ" in board material | Marcus Deane | 2026-12-15 |

## 6. Change log

| Date | Metric id | Change | Why | Old versus new value for the last period | Announced where |
|---|---|---|---|---|---|
| 2026-07-01 | M-016 | Definition changed: before the change, "NGR, Ontario" followed the same redeemed-credits-only deduction rule as the trading desk; after the change it follows Ontario's taxable base, which, per counsel's advice, differs from the NJ rule and from the prior Ontario convention in how certain promo types are treated at the taxable line (illustrative; confirm with counsel) | A change in Ontario's revenue-share treatment altered how certain promotional deductions are treated at the taxable line, so the old convention no longer matches what is reported | Old convention would have reported ON NGR at $2.4M for August 2026 (ILLUSTRATIVE); the new convention reports $2.15M, about $250K below it (ILLUSTRATIVE) | Announced in the 2026-06-24 operating review, one month before it landed, old and new side by side |

---

## Exit gate (feeds Gate 6: outcomes verified)

Done when every box is honestly ticked. The dictionary is the reference every tile in [dashboard-spec.md](../templates/operate/dashboard-spec.md) and every row in [metrics-review.md](../templates/operate/metrics-review.md) cites at [Gate 6](../os/STAGE-GATES.md).

- [x] Every metric a dashboard, review, or update shows has a row here with an id
- [x] Every formula names numerator, denominator, and filters, and reads events or tables that exist in the instrumentation spec
- [x] Every row has an owner and a refresh with its latency
- [x] Every row's known-gaps cell is filled, or says "none found on [date]"
- [x] Entities are defined once in section 1 and every formula uses them
- [ ] The north star and its inputs are typed and connected in the lineage table
- [x] Every definition change is in the change log and was announced before it landed
- [x] The ILLUSTRATIVE row has been deleted
- [x] Signed by Marcus Deane, Compliance Officer, 2026-10-08
