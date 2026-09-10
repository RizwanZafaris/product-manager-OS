# OKR Sheet: Expense Copilot Add-on, 2026-11-02 to 2026-12-31

Fills [templates/planning/okrs.md](../templates/planning/okrs.md). Everything here is invented: Ledgerline is a fictional mid-market software company, and every baseline, target and score is ILLUSTRATIVE, built for this repository so the scoring can be checked, not as a benchmark or a target to copy. See the [examples index](README.md) and the [journey](ledgerline-journey.md) this sheet is one of thirteen artifacts inside.

**Owner:** Maya Chen, Product Manager (P1) · **Period:** 2026-11-02 to 2026-12-31, the add-on launch cycle (N69) · **Scoring cadence:** check-in at 2026-11-16, 2026-11-30 and 2026-12-14 (N75); final score 2026-12-21, on data to 2026-12-18 (N69) · **Status:** Signed 2026-11-03, scored 2026-12-21. Both aspirational KRs scored under the 0.7 success line: KR1 at 0.44 and KR4 at 0.53; only KR1 is under 0.5. The diagnosis and the decision it fed are in section "End-of-period scoring"
**Grading scale:** 0.0 to 1.0 at period end; around 0.7 on ambitious KRs is healthy, 1.0 across the board means the targets were sandbagged

## Objective 1: Prove the copilot add-on earns its own revenue line without weakening the approval win it already produced internally

<!-- Objective text kept unedited from signing on 2026-11-03 through scoring on 2026-12-21, per the "End-of-period scoring" section's own statement that no target in the table was edited between those two dates. -->

This objective is scored against the state before launch: zero customer accounts on the add-on, the S-1 approval baseline of 66% (N35), and zero recurring revenue from it. It is signed against D1, reuse internal evidence only where a written reason says it transfers, and D2, the add-on ships with its own revenue line rather than folded into the Business plan.

| # | Key result (an outcome, not a task) | Baseline | Target | Current | Score | Owner |
|---|---|---|---|---|---|---|
| KR1 | Business-plan accounts with the add-on active, paid or design partner (M-002) | 0 (N70) | 180 (N70) | 79 = 73 paid + 6 design partners, at 2026-12-18 (N64, N70) | 0.44 (N70) | Maya Chen (P1) |
| KR2 | First-submission approval rate on drafted reports, pooled across active add-on accounts (M-006) | 66%, S-1 median across all reports (N35, N71) | 78% (N71) | 76%, at 2026-12-18 (N65, N71) | 0.83 (N71) | Priya Nair (P2) |
| KR3 | Share of eligible reports drafted in active add-on accounts (M-003) | 0% (N72) | 50% (N72) | 47%, 555 of 1,180 reports, at 2026-12-18 (N65, N72) | 0.94 (N72) | Priya Nair (P2) |
| KR4 | Add-on monthly recurring revenue, dollars (M-011) | $0 (N73) | $30,000 (N73) | $15,900, at 2026-12-18 (N68, N73) | 0.53 (N73) | Maya Chen (P1) |

KR2's baseline is a proxy, not a like-for-like starting point: 66% is the median first-submission approval rate across all reports in all of S-1 (N35), while the KR itself is a pooled rate on drafted reports only, in active add-on accounts only, which excludes about 11% of S-1 under the metrics dictionary's G-2 gap. There was no pre-launch measurement of approval on drafted reports in this narrower population to use instead; the six design partners' own baseline, on a closer population, was 64% (N44).

**Commitment type per KR:** KR1 (accounts active) and KR4 (MRR) are aspirational, 0.7 is success, because both depend on a price the team had not yet validated at signing (D3's own mismatch note). KR2 (approval) and KR3 (drafted share) are committed, 1.0 is expected, because they measure the same product mechanism the PRD targeted internally, 80% approval and 50% drafted share by month two (N4, N19), which is what the add-on was built to carry into the customer segment; the internal review that later retired the kill line (D4, PERSIST, N20, N19 at 74% and 38%, the latter below the internal 50% target) was still six days out at signing and is not itself the basis for the commitment call made here.

There is no Objective 2 for this cycle. One objective, judged sufficient at signing because the cycle covers a single launch with a single revenue question underneath it; per the template's own guidance this is usually the stronger choice, and nothing in the 2026-12-21 scoring session reopened that call.

## Guardrails

Table below is ILLUSTRATIVE. Floors and ceilings agreed 2026-11-03 alongside the key results (N74); none were breached across the cycle, which the metrics review confirms.

| Guardrail metric | Floor or ceiling | Watched by |
|---|---|---|
| Reviewer-caught extraction errors per 100 drafted reports (M-008) | Under 3 (N58, N74); actual 2.4 at 2026-12-18 (N67) | Priya Nair (P2) |
| Model cost per drafted report, dollars (M-009) | At most $1.05 (N74); actual $0.93 at 2026-12-18 (N67) | Daniel Okafor (P3) |
| First-submission approval rate on drafted reports (M-006) | At least 70% (N58, N74), the EXP-1 stop line, separate from the 78% target M-006 also carries as KR2; actual 76% at 2026-12-18 (N65, N71) | Priya Nair (P2) |
| Support tickets per 100 add-on accounts per week (M-010) | At most 8 (N74); actual 5.1 at 2026-12-18 (N67) | Hana Sato (P8) |
| Discounts outside the pricing doc's section 5 table | 0 (N74); actual 0, none logged as of 2026-12-21, the scoring date (N74) | Ruth Adeyemi (P6) |

## Check-in log

The section that decides whether these were OKRs or decoration. Three entries, dated per N75, none of which edited a baseline or a target.

| Date | KR movements since last check-in | Confidence change | Action taken |
|---|---|---|---|
| 2026-11-16 | KR1 at 6 of 180, the six design partners live since 2026-11-10 (N41); KR4 at about $1,026, the design-partner line, $6 per seat with the 25% partner discount across 228 seats (N41, N68 partner component); KR2 and KR3: the phase 1 window (2026-11-10 to 2026-11-22, N43) is still open, too early for a rate | Confidence on KR1 and KR4 unchanged, six design partners live is the expected phase 1 state and EXP-1 had not opened; confidence on KR2 and KR3 unchanged, no rate yet to raise or lower it against | R2 opened the same day: seat metering cannot bill the 214 legacy annual-invoice accounts mid-term; owner Priya Nair with the billing lead |
| 2026-11-30 | EXP-1 exposure at 1,885 of 2,900 accounts (N81); KR1 and KR4 not restated in this log, though T-3 and T-11 refresh daily on the dashboard; KR2 and KR3 not re-pulled either, both weekly tiles; R4 escalated, the customer DPA blocking two Enterprise deals | Confidence on KR1 and KR4 lowered; the status report for this week reads AMBER overall with one RED (R4) | R4 escalated to Isabel Ferreira; no KR target edited |
| 2026-12-14 | EXP-1 exposure complete at 2,748 of 2,900 accounts (N59); M-007 not read, the dashboard's funnel tile stays restricted to the analyst until the 2026-12-18 analysis date; KR1 and KR4 not otherwise restated in this log; KR2 and KR3 not re-pulled into this log either | Confidence on KR1 and KR4 lowered, on the advisory board signal from 2026-12-02 that seat pricing penalises low-filer accounts (N78), not on a read of the EXP-1 result, which stayed unread; confidence on KR2 and KR3 unchanged | None; the EXP-1 decision rule was already pre-declared (N57) and the analysis date, 2026-12-18, had not arrived |

## End-of-period scoring

Score against the baseline recorded at planning, not against what the number turned out to be. No target in the table above was edited between 2026-11-03 and 2026-12-21.

- Scored on: 2026-12-21 · Scored by: Maya Chen, with Isabel Ferreira present
- KRs that scored below 0.3: none. Both aspirational KRs scored under the 0.7 success line: KR1 at 0.44 and KR4 at 0.53; only KR1 is under 0.5. The diagnosis for both is one cause: EXP-1's per-seat price converted at 2.7% pooled across the plain and anchored arms (N61) against a pre-declared 6.0% ship bar (N57), because the median account's seats do not track its filers, $204 a month for a median 34-seat account against a $149 Business plan (N47), and the anchored arm quoted Ledgerline's own 30 reviewer-hours a month (N7) rather than the buyer's own reviewer cost. Four of six win-loss interviews (N77) named seats billed for people who never file, or an add-on priced above the plan, and 6 of 8 advisory board members present on 2026-12-02 said the same thing (N78); both corroborate the same cause before the kill, the board three weeks earlier and the win-loss batch the week before. KR2 and KR3, both committed, scored 0.83 and 0.94, and both missed their targets: 76% against 78% for KR2, and 47% against 50% for KR3. M-006 drifted from 77% in phase 1, on the six design partners alone (N44), to 76% as the account mix widened past them (N65); M-003 fell from 54% in phase 1 to 47% the same way. G-2's exclusion of about 11% of S-1 is a caveat on what M-006 covers, not the cause of the miss. Whether carrying KR2 and KR3's targets forward unchanged is still a committed call, or whether they become aspirational next cycle, is open for the next signing.
- What carries into next period: KR2 and KR3's committed targets and the mechanism behind them, unchanged for now, though both missed their targets this cycle and whether they stay committed is a call for the next cycle's signing, not decided here. What is dropped: the per-seat value metric and its KR1 and KR4 targets. D6 on 2026-12-21 kills the seat price and pivots packaging to a usage metric; the next cycle's KR1 and KR4 targets are left open until EXP-2 reads out. Added 2026-12-22: D7 sets the re-offer at $2.40 per drafted report (N89), and the growth plan signed that day sets EXP-2's 6.0% bar on M-007 and names M-002 as the bet; neither was in view at the 2026-12-21 scoring session, and the growth plan does not itself set targets for the next OKR cycle.
- Feed the results into the [metrics review](../templates/operate/metrics-review.md) for Gate 6. The metrics review dated 2026-12-21 carries this scoring forward and records PIVOT on packaging as D6. Added 2026-12-22: the growth plan is the resulting artifact (D7).

## How this OKR set fails

| Failure mode | What it looks like | The rule that stops it, as applied here |
|---|---|---|
| Key results are tasks | "Ship the dashboard", "run the webinar", ticked at completion | Every KR above is a measured outcome (accounts active, approval rate, drafted share, MRR), none a shipped feature; LEDGERLINE-S1 through S3 shipped inside the cycle without becoming a KR of their own |
| The objective is a metric | "Increase revenue" as the objective, with the metric repeated beneath | Objective 1 states what better looks like, earning a revenue line without weakening approval, and none of the four KRs repeats the objective's wording |
| Sandbagged | Everything scores full marks and nothing changed | Both aspirational KRs scored under 0.7 (KR1 at 0.44, KR4 at 0.53); the set was not sandbagged, and the two low scores recorded the same failure the EXP-1 kill rule had already acted on, the targets were not edited to soften it |
| Too many | Five objectives and a dozen key results nobody can recall | One objective, four key results, the number the template's own guidance treats as workable to recall |
| No baseline | "Engagement up", with no starting number, argued about at scoring | Every KR's baseline is dated to signing, 2026-11-03, and traces to N70 through N73 on the journey's data sheet; none was contested at scoring, though KR2's is a proxy on a wider population than the KR itself measures, noted under the KR table rather than hidden |

## Exit gate

This sheet is fit to run the period on when:

- [x] Every objective is qualitative and time-bound; every KR is quantitative. Objective 1 states a qualitative outcome; the time bound is the header's 2026-11-02 to 2026-12-31 cycle, not restated in the objective sentence itself. All four KRs are numbers with units.
- [x] Every KR passes the "score it without asking what the team did" test. Each of KR1 to KR4 is read straight off billing or product analytics (N64, N65, N68) with no interpretation of team activity required.
- [x] Every KR has a baseline, a target, and a named owner. All four rows carry a baseline dated to signing, a target, and an owner (Maya Chen or Priya Nair).
- [x] Each KR is marked committed or aspirational. KR1 and KR4 aspirational; KR2 and KR3 committed, with the reason for the split stated under the table.
- [x] Guardrails are listed, so the objectives cannot be gamed silently. Five guardrails, each with a floor or ceiling agreed 2026-11-03 and an owner; none breached across the cycle per the metrics review.
- [x] The scoring cadence has calendar entries, not intentions. Three check-in dates (2026-11-16, 2026-11-30, 2026-12-14) have entries in the check-in log above; the scoring date (2026-12-21) has its entry in the "End-of-period scoring" section below, not the check-in log. None of the four is just named on the header line.

Signed: Maya Chen, Product Manager, 2026-11-03. Scored: Maya Chen, Product Manager, 2026-12-21, with Isabel Ferreira, Chief Product Officer, present.
