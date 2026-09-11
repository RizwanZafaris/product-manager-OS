# Dashboard Spec: Expense Copilot Add-on Launch Dashboard

Fills [templates/operate/dashboard-spec.md](../templates/operate/dashboard-spec.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the Expense Copilot add-on is the fictional product used across this repository, the people are roles filled by invented names, and every count, dollar figure and threshold is ILLUSTRATIVE, carried unchanged from the [journey data sheet](ledgerline-journey.md) so it can be checked against the documents this spec follows. See the [examples index](README.md).

**Owner:** Maya Chen, product manager · **Builder:** Kwame Boateng, data analyst · **Audience:** the add-on launch team (product, engineering, marketing, sales and finance leads named in the journey cast) · **Tool:** [OPEN: the BI tool is not named in the data sheet; confirm with Kwame Boateng before build] · **Date:** 2026-11-06 · **Status:** Verified (verification passes 2026-11-13 and 2026-12-19, section 7)
**Last updated:** 2026-12-21, after the EXP-1 kill (2026-12-18) and the metrics dictionary's M-007 change log entry (2026-12-19); the body below is the spec as it stood at its 2026-11-06 sign-off, with later facts this update adds marked by date where that separates sign-off knowledge from hindsight
**Dictionary version:** 2026-12-19, the date of the metrics dictionary's one change log entry, on [ledgerline-metrics-dictionary.md](ledgerline-metrics-dictionary.md), agreed by Maya Chen and Kwame Boateng on 2026-11-04 and re-reviewed by the same two on 2026-12-19

## 1. Audience and questions

Every tile below traces to one of these four questions, and no tile exists that does not.

| # | Audience (role) | Question they arrive with | Decision the answer changes | How often they look |
|---|---|---|---|---|
| Q1 | Launch team | Is the copilot drafting reports and getting them approved in customer accounts, at anything close to what it did internally, and is that tracking the [OKR sheet's](ledgerline-okrs.md) KR1 (accounts active) and KR3 (share drafted) | What to report against KR1 and KR3 at the OKR check-ins (2026-11-16, 2026-11-30, 2026-12-14) | Monthly, the M-001 and M-012 rollup cadence; weekly for the KR3 input, M-003 |
| Q2 | Analyst only until 2026-12-18, then the launch team | Is the per-seat offer converting exposed accounts at 6.0% or better, per the pre-declared rule | Ship, iterate or kill EXP-1 (N57), then feed the pivot decision (D6) | One authoritative read at analysis, 2026-12-18; no earlier read, per the access decision below |
| Q3 | Launch team | Are the guardrails, extraction errors, model cost, support load and drafted-report approval, holding inside the floors and ceilings agreed at planning (N74), and is the [GTM plan's](ledgerline-gtm-plan.md) phase stop condition tripped | Escalate a status-report row to red, hold the launch at its current phase, or trigger the GTM plan's stop condition (section 5, M-008) | Weekly for M-008; monthly for M-006's rollup into M-001, weekly for the M-006 tile itself; monthly for M-009 |
| Q4 | Launch team | How many accounts are active and how much MRR is the add-on generating, against KR1 and KR4 | What to report at the OKR check-ins (2026-11-16, 2026-11-30, 2026-12-14) | Weekly, and the day before each check-in |

## 2. Layout

- **Row 1:** M-001 (north star, copilot-drafted reports approved on first submission per month across customer accounts), M-012 (its companion, per the [north star tree](ledgerline-north-star-tree.md): M-001 as a share of all eligible reports, so a rise in the count alone does not read as a rise in quality), M-006 (guardrail, first-submission approval rate on drafted reports, floor and target lines)
- **Row 2:** M-004, M-005 (the two raw signals that feed the M-006 tile above), M-002 (gates the denominators of M-003, M-006 and M-012, and feeds KR1), M-003 (feeds KR3 and M-012's denominator), following the [dictionary's lineage table](ledgerline-metrics-dictionary.md) rather than an arbitrary order
- **Row 3 and below:** M-007 (the EXP-1 funnel, access-restricted per section 3), M-008, M-009, M-010 as guardrail diagnostics, M-011 as the remaining OKR-facing diagnostic (KR4)
- **Filters available on every tile:** date range on every tile; segment filters as listed per tile in section 3

## 3. Tiles

| Tile | Question # | Metric id | Visual (number / trend / funnel / cohort table / distribution) | Grain and window | Comparison (target / prior period / segment) | Segments available | Owner |
|---|---|---|---|---|---|---|---|
| T-1 | Q1 | M-001 | trend | monthly, rolled up from the weekly M-006 numerator, per the dictionary; T-2 (M-006) is the weekly proxy read during phase 1 rather than a redefinition of M-001's own grain | prior period; M-001 itself carries no formal target, only its inputs do (row 2) | S-1, S-2 | Maya Chen |
| T-2 | Q3 | M-006 | number, with floor and target lines | weekly, trailing add-on review window | floor 70% (N58, N74) and target 78% (N71, KR2) | S-1, S-2, S-5 | Priya Nair |
| T-3 | Q1, Q4 | M-002 | number / trend | weekly, point in time at week end, per the dictionary; refreshed daily | target line 180 (N70, KR1) | S-1, S-2 | Maya Chen |
| T-4 | Q1 | M-003 | trend | weekly | target line 50% (N72, KR3) | S-1, S-2 | Kwame Boateng |
| T-5 | Q1 | M-004 | trend | weekly | prior week; internal baseline 86% (N21) | S-1 | Priya Nair |
| T-6 | Q1 | M-005 | trend | weekly | prior week; internal baseline 81% (N22) | S-1 | Priya Nair |
| T-7 | Q2 | M-007 | funnel (exposed, opened, reached price step, paid) | analyst-only throughout the exposure window, per the dictionary; not refreshed weekly; the single ratified value is read once, ad hoc, at the pre-declared analysis date (2026-12-18) | ship line 6.0%, iterate band 4.0% to 6.0%, kill line under 4.0% (N57) | S-3, S-4 | Kwame Boateng, access-restricted, see below |
| T-8 | Q3 | M-008 | number | weekly, per the dictionary's weekly job (about 24 hours behind) | ceiling 3 per 100 drafted reports (N58, N74) | S-1, S-2 | Priya Nair |
| T-9 | Q3 | M-009 | number | monthly, trued up against the vendor invoice, up to 30 days behind, per the dictionary; the weekly estimate is a same-day approximation, not itself refreshed as a tile | ceiling $1.05 per drafted report (N74) | none | Daniel Okafor |
| T-10 | Q3 | M-010 | number | weekly | ceiling 8 per 100 add-on accounts per week (N74) | none | Hana Sato |
| T-11 | Q4 | M-011 | number / trend | weekly | target $30,000 (N73, KR4) | S-1, S-2 | Daniel Okafor |
| T-12 | Q1 | M-012 | trend | monthly, same rollup schedule as M-001, per the dictionary | prior period; M-012 is a companion to the north star rather than a KR, so no formal target is set | S-1 | Maya Chen |

### The access decision on the EXP-1 funnel tile

T-7 is restricted to the analyst throughout the exposure window, per the dictionary's own grain for M-007 ("restricted to the analyst throughout the exposure window, per the dashboard spec; read once, ad hoc, at the pre-declared analysis date (2026-12-18), not refreshed weekly"). Until the 2026-12-18 analysis runs, those analyst-only reads are visible only to Kwame Boateng, the data analyst who owns M-007 and runs it against the dictionary formula. Giving the whole launch team a running read of the funnel, so that the sales lead and the product marketing lead could watch the conversion number climb or stall in real time, was raised at the same 2026-11-06 sign-off session that approved this spec and rejected. The reason: the [experiment brief](ledgerline-experiment-brief.md) fixes the sample size and the analysis date in advance (N56) and names "checking daily and calling it the first time it looks significant" as a failure mode in its own right ("Peeking and stopping early"), separate from and in addition to the ship, iterate or kill rule read once at that fixed date (N57). A team watching a partial funnel from exposure's start (2026-11-23) to the analysis date (2026-12-18), about three and a half weeks, would form exactly that opinion on incomplete data. The brief's own "Peeking and stopping early" row names this tile and restriction (dashboard spec, section 3) rather than mandating it directly; this spec is what enforces the brief's fixed-read discipline, by restricting T-7's analyst-only reads to Kwame Boateng until 2026-12-18. A tile that can be peeked at before its analysis date is not a dashboard, it is a running commentary on an experiment that has not finished.

The tile unlocks for the full launch team once the 2026-12-18 analysis is logged. The number the team sees at unlock is the ratified result: 73 of 2,748 exposed, 2.7% pooled, under the 4.0% kill line (N61). The metrics dictionary's one change log entry, posted 2026-12-19, clarified the window's precision (336 hours, 14 x 24, UTC from min(exposure_event.timestamp) per account) after this value was already computed against that same exposure-based window; it is a precision clarification, not a redefinition, and changed no ratified value (dictionary, section 6). The restriction held in practice: the OKR sheet's 2026-12-14 check-in entry records that M-007 was not read and that the funnel tile stayed restricted to the analyst until the 2026-12-18 analysis date ([ledgerline-okrs.md](ledgerline-okrs.md)).

## 4. Drill paths

| From tile | To (view or report) | What it explains | Filters carried |
|---|---|---|---|
| T-3 (M-002) | Account-level activation list, billing joined to S-1 membership | Which named accounts activated or lapsed in the window | Date range, segment |
| T-7 (M-007) | Exposure and offer-page event detail, analyst-only until 2026-12-18 | Where an account dropped, opened but did not reach the price step, or reached it but did not pay | Arm (S-3 or S-4), date range |
| T-8 (M-008) | Reviewer flag detail log | Which drafted reports were flagged, and whether a language or receipt-type pattern explains a spike (R3) | Date range, account |
| T-9 (M-009) | Vendor invoice detail, joined to drafted-report count | Whether a cost rise is volume, a per-receipt rate change, or a receipts-per-report shift (N10, DEP2) | Date range |
| T-11 (M-011) | Billing ledger by account | The MRR composition: paid accounts at N46's price, design partners at the N42 discount | Date range, segment |

## 5. Alerting

| Metric id | Condition (threshold and direction) | Window | Who is told | Channel | First action (runbook or review) | Suppressed when |
|---|---|---|---|---|---|---|
| M-006 | Below 70% (floor agreed with Priya Nair, the metric owner, 2026-11-03, N58, N74) | Weekly, trailing window | Maya Chen, Kwame Boateng and Priya Nair | Launch team channel | Pull the week's flagged reports by segment; if S-1 wide, raise at the next status report; if concentrated in S-5, hold new activations in that segment pending review | [OPEN: minimum weekly drafted-report count for a small-n suppression is not stated on the data sheet; confirm with Priya Nair]; [OPEN: staleness threshold not stated on the data sheet; confirm with Priya Nair. M-006's normal refresh lag is itself about 24 hours per the dictionary, so a same-figure suppression threshold would silence the alert on most normal loads] |
| M-008 | 3 or more per 100 drafted reports (agreed with Priya Nair, the metric owner, 2026-11-03, N58, N74; matches the GTM plan's own stop-condition wording, section 5) | Weekly, per the dictionary's grain for M-008 | Priya Nair | Launch team channel | Pull the week's flagged reports; check for a receipt-language pattern (R3) before treating it as a general regression | [OPEN: minimum weekly drafted-report count for a small-n suppression is not stated on the data sheet; confirm with Priya Nair] |
| M-009 | Above $1.05 per drafted report (agreed with Daniel Okafor, the metric owner, 2026-11-03, N74) | Weekly estimate, published same day, per the dictionary's grain for M-009; trued up monthly against the vendor invoice | Daniel Okafor | Finance email digest | Check the vendor invoice against the drafted-report count for a rate change; escalate to procurement if the quoted rate itself moved (DEP2) | [OPEN: minimum weekly drafted-report count for a small-n suppression is not stated on the data sheet; confirm with Daniel Okafor] |
| M-010 | Above 8 per 100 add-on accounts per week (agreed with Hana Sato, 2026-11-03, N74) | Weekly | Hana Sato | Launch team channel | Pull the week's tickets, tag by category, check for one shared root cause before treating it as broad dissatisfaction | [OPEN: staleness threshold not stated on the data sheet; confirm with Hana Sato, the metric owner. M-010 refreshes daily, same day, per the dictionary, so a 24-hour threshold has no source here] |

## 6. Freshness and known gaps

Refresh cadence and latency are the metrics dictionary's own "Refresh and latency" column for each metric id, carried onto the tile it appears on; the "shown on the tile" column follows the template's own convention of a literal timestamp rather than a guessed cadence.

| Tile | Source refresh and latency | Shown on the tile as | Known gaps annotated (dictionary gap ids) |
|---|---|---|---|
| T-1 (M-001) | Weekly job, about 24 hours behind; monthly rollup published the 2nd business day | as of [last completed load] | G-2: the dictionary lists G-2 directly against M-001, since M-001's numerator is M-006's; excludes about 11% of S-1 still on the pre-2026-06 classic approvals workflow, whose approval events carry no draft id |
| T-2 (M-006) | Weekly job, about 24 hours behind | as of [last completed load] | G-2: excludes about 11% of S-1 still on the pre-2026-06 classic approvals workflow, whose approval events carry no draft id |
| T-3 (M-002) | Daily job, same day | as of [last completed load] | G-1: undercounts by up to 3 while legacy annual-invoice accounts (N82) wait on a manual invoice line |
| T-4 (M-003) | Weekly job, about 24 hours behind | as of [last completed load] | none found on 2026-11-04 |
| T-5 (M-004) | Daily job, same day | as of [last completed load] | G-3: a receipt in a language the extractor abstains on stays in the denominator, undercounting accounts like Wrenfield Labs |
| T-6 (M-005) | Daily job, same day | as of [last completed load] | none found on 2026-11-04 |
| T-7 (M-007) | Analyst-only, not refreshed weekly, through the exposure window; one ad hoc ratified read at the experiment's analysis date | as of the 2026-12-18 analysis, analyst-only until then | none found on 2026-11-04; the window definition's precision was clarified 2026-12-19 (dictionary section 6 change log; no ratified value changed), so this spec's own re-verification (section 7) reconfirms T-7 against the clarified wording |
| T-8 (M-008) | Weekly job, about 24 hours behind | as of [last completed load] | none found on 2026-11-04 |
| T-9 (M-009) | Weekly estimate published same day; trued up monthly against the vendor invoice, up to 30 days behind | as of [last completed load] | The vendor bills one invoice line per period, not per account, so the monthly true-up is a fleet average across all active add-on accounts, not an account-level cost. That invoice line also carries Ledgerline's own internal filers' model usage, while the denominator counts only customer drafted reports, so the monthly true-up overcounts for that reason (dictionary, M-009 known gaps) |
| T-10 (M-010) | Daily job, same day | as of [last completed load] | none found on 2026-11-04 |
| T-11 (M-011) | Daily job, same day | as of [last completed load] | none found on 2026-11-04; Enterprise accounts (S-6) are out of scope for M-011 by definition (section 1), not a gap. The two Enterprise prospects blocked on the customer DPA (N79) cleared it by D5 (2026-12-03), and their quotes were withdrawn with the pivot (N88) |
| T-12 (M-012) | Monthly, same schedule as M-001 | as of [last completed load] | Inherits G-2 through M-001's numerator; the denominator, all eligible reports, is not affected by that exclusion, so M-012 undercounts slightly |

## 7. Verification

### Pass 1: at build, 2026-11-13

Reproduced by hand from the dictionary formulas on 2026-11-13, the date LEDGERLINE-S5 (the customer-facing approval tile) shipped, four days into phase 1 (which opened 2026-11-10, N43, N85), with the six design partners (S-2) as the only active accounts. That is a partial week against the dictionary's Monday-start weekly convention (section 1), not a full one; the tiles verified below are the ones with a meaningful hand count that early, scoped to S-2 where the tile itself is S-2-scoped.

| Tile | Dictionary value on 2026-11-13 | Dashboard value | Match (yes / no) | Explanation if no |
|---|---|---|---|---|
| T-3 (M-002) | [OPEN: 2026-11-13 hand count not on the data sheet; owner Kwame Boateng] | [OPEN: 2026-11-13 hand count not on the data sheet; owner Kwame Boateng] | Yes | |
| T-2 (M-006) | [OPEN: 2026-11-13 hand count not on the data sheet; owner Kwame Boateng] | [OPEN: 2026-11-13 hand count not on the data sheet; owner Kwame Boateng] | No | The tile's first build joined all S-1 approval events without excluding accounts still on the pre-2026-06 classic approvals workflow. Those accounts' events carry no draft id (G-2), so the hand count and the tile disagreed until Kwame Boateng added the exclusion filter the dictionary's G-2 note already specified, same day |
| T-8 (M-008) | [OPEN: 2026-11-13 hand count not on the data sheet; owner Kwame Boateng] | [OPEN: 2026-11-13 hand count not on the data sheet; owner Kwame Boateng] | Yes | |
| T-11 (M-011) | [OPEN: 2026-11-13 hand count not on the data sheet; owner Kwame Boateng] | [OPEN: 2026-11-13 hand count not on the data sheet; owner Kwame Boateng] | Yes | |

The remaining eight tiles (T-1, T-4, T-5, T-6, T-7, T-9, T-10, T-12) were not reproduced at this pass: T-7 has no data before EXP-1's exposure window opens (2026-11-23); T-1 and T-12 are monthly rollups with no month of data yet; T-4, T-5, T-6, T-9 and T-10 carry too little S-2-only volume for a hand count to mean anything at four days in. They are covered by pass 2 below, once the review window (N63) closed.

### Pass 2: after the 2026-12-19 dictionary change log entry

Reproduced by hand from the dictionary formulas on 2026-12-19, the day after the add-on review window closed (2026-11-23 to 2026-12-18, N63) and the day the metrics dictionary's one change log entry landed on M-007's window definition, triggering the template's rule to re-verify after any dictionary change log entry. This pass covers all twelve tiles, both closing the eight left open at pass 1 and reconfirming T-7 against the clarified window wording (no ratified value changed).

| Tile | Dictionary value on 2026-12-18 | Dashboard value | Match (yes / no) | Explanation if no |
|---|---|---|---|---|
| T-1 (M-001) | 422 drafted reports approved first time, window 2026-11-23 to 2026-12-18 (N65); reported under the M-001 id as a window count, not the calendar-month value M-001's own definition produces | [OPEN: December's monthly rollup, published the 2nd business day, had not yet posted on 2026-12-19; the 422 window count was read off the underlying data, not the monthly T-1 tile itself] | Not yet checkable | The monthly tile could not show this window's count on 2026-12-19 |
| T-2 (M-006) | 76% (422 of 555 drafted reports), window (N65) | 76% (read off the dashboard tile) | Yes | |
| T-3 (M-002) | 79 active accounts (73 paid plus 6 design partners) at 2026-12-18 (N64) | 79 (read off the dashboard tile) | Yes | |
| T-4 (M-003) | 47% (555 of 1,180 eligible reports drafted), window (N65) | 47% (read off the dashboard tile) | Yes | |
| T-5 (M-004) | 87% of extracted fields accepted without edit, window (N66) | 87% (read off the dashboard tile) | Yes | |
| T-6 (M-005) | 82% of suggested categories kept, window (N66) | 82% (read off the dashboard tile) | Yes | |
| T-7 (M-007) | 73 of 2,748 exposed, 2.7% pooled; 33 of 1,371, 2.4% control; 40 of 1,377, 2.9% anchored (N61). The window's precision was clarified 2026-12-19 (336 hours from min(exposure_event) per account, dictionary section 6); no value changed | 2.7% pooled (read off the dashboard tile), reconfirmed on 2026-12-19 against the clarified window wording; no value changed | Yes | |
| T-8 (M-008) | 2.4 errors per 100 drafted reports, window (N67) | 2.4 per 100 (read off the dashboard tile) | Yes | |
| T-9 (M-009) | $0.93 model cost per drafted report, vendor invoice over drafted count (N67), the monthly true-up | posted 2026-12-21, after this pass; owner Daniel Okafor | Not yet checkable | The monthly true-up tied to the vendor's billing cycle had not posted by 2026-12-19, one day after the window closed; the weekly-estimate reading is a same-day approximation, not this tile's own monthly value |
| T-10 (M-010) | 5.1 support tickets per 100 add-on accounts per week, window (N67) | 5.1 per 100 (read off the dashboard tile) | Yes | |
| T-11 (M-011) | $15,906 (73 paid accounts, 2,480 seats x $6 = $14,880, plus 6 partners, 228 seats x $6 x 0.75 = $1,026) at 2026-12-18 (N68) | $15,906 (read off the dashboard tile) | Yes | |
| T-12 (M-012) | 36% (422 of 1,180 eligible reports), window 2026-11-23 to 2026-12-18 (N65); reported under the M-012 id as a window count, not the calendar-month value M-012's own definition produces | [OPEN: December's monthly rollup, published the 2nd business day, had not yet posted on 2026-12-19; the 36% window figure was read off the underlying data, not the monthly T-12 tile itself] | Not yet checkable | The monthly tile could not show this window's figure on 2026-12-19 |

---

## Exit gate (feeds Gate 6: outcomes verified)

Done when every box is honestly ticked. The verified dashboard is the screen the [metrics review](ledgerline-metrics-review.md) reads for [Gate 6](../os/STAGE-GATES.md); its tiles cite the [metrics dictionary](ledgerline-metrics-dictionary.md) and nothing else. This spec also draws on the [experiment brief](ledgerline-experiment-brief.md) for T-7's access decision, the [GTM plan](ledgerline-gtm-plan.md) for the phase stop condition Q3 tracks, and the [OKR sheet](ledgerline-okrs.md) for the KR targets shown as comparison lines.

- [x] Every tile cites a metric id from the dictionary, and no metric is defined here. Twelve tiles, T-1 to T-12, cite M-001 to M-012 and nothing else; no tile carries its own formula.
- [x] Every tile traces to a question, and every question names a decision. Section 1's four questions each name the decision the answer changes; section 3's Question # column shows which tile answers which.
- [x] The audience is one role group; a second audience got a second spec. The add-on launch team is one group; the customer-facing approval tile is a separate story, LEDGERLINE-S5 (its acceptance criteria are the journey's story-table row for that id, not a document in this repository), shipped inside the product on 2026-11-13, not on this dashboard.
- [x] Every drill path ends in a view that exists and carries filters. Section 4's five paths each name a view built alongside the tile it drills from, with the filters the reader already set.
- [x] Every alert has a threshold agreed with the metric owner, a window, a channel, and a first action. Section 5's four alerts all cite N74, agreed 2026-11-03, before this spec's own sign-off date, attributed to the metric owner named against each id in the dictionary.
- [x] Freshness and known gaps show on the tiles that have them. Section 6 carries a row, refresh cadence and all, for every one of the twelve tiles: G-1 on T-3, G-2 on T-1 and T-2 (M-001 inherits it directly through M-006's numerator, per the dictionary's own known-gaps column), G-3 on T-5, G-2 again by inheritance on T-12, the M-009 fleet-average and internal-usage caveats on T-9, and the M-011 out-of-scope note on T-11.
- [x] Every tile's value was reproduced from the dictionary formula once, with differences explained. Section 7's pass 1 (2026-11-13, four tiles reproducible that early) found one mismatch, on M-006, explained by G-2 and corrected the same day; the other three hand counts from that pass are not on the data sheet and are marked open. Pass 2 (2026-12-19, required by the dictionary's M-007 change log entry) reproduced nine of the twelve tiles against the window that closed 2026-12-18, including T-7 reconfirmed against the clarified window wording (no ratified value changed); the two monthly tiles, T-1 and T-12, could not yet be checked against their own rollup on 2026-12-19, since December's rollup had not posted, and T-9's monthly vendor-invoice true-up had not yet posted either, so those three figures are marked not yet checkable rather than matched.
- [x] The ILLUSTRATIVE row has been deleted. The template's own italicized example row (T-3, M-004) is gone; every row above is a filled tile.
- [x] Signed by Maya Chen, product manager, 2026-11-13; re-verified and this update signed 2026-12-21

Approved 2026-11-06, the session that also approved the GTM plan and the one-pager; verified and originally signed 2026-11-13; re-verified and this update signed: Maya Chen, product manager, 2026-12-21
