# Status Report: Expense Copilot Add-on, week of 2026-11-30

Fills [templates/execution/status-report.md](../templates/execution/status-report.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the Expense Copilot add-on is the fictional product used across this repository, the people are roles filled by invented names, and every count and dollar figure is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) so it can be checked against the documents this report feeds and follows. See the [examples index](README.md).

Stage: BUILD and DELIVER, weekly from Gate 3 onward; feeds Gate 4 and Gate 5 with the record of what slipped and what was decided.

**Owner:** Maya Chen, product manager · **Week of:** 2026-11-30 · **Overall:** AMBER (last week: GREEN) · **Distribution:** launch-team channel, copied to Isabel Ferreira

## 1. The colour rule

- **Green:** on plan, and the evidence is a linked artifact, a passed test, or a number. A feeling is not evidence.
- **Amber:** off plan with a recovery path inside the team's authority. The row must carry the date by which it is back to green or becomes red. An amber without a date is a red the author is not ready to say.
- **Red:** off plan with no recovery inside the team's authority. The row must carry the decision needed, who makes it, and by when. A red without a decision is a complaint.
- **Overall** is no better than the worst workstream unless the report says why.
- Colour improves only on evidence; it worsens on judgment.

## 2. Summary

Phase 1's exit condition was met on 2026-11-23, and EXP-1 exposure is running on schedule: 1,885 of 2,900 S-1 accounts exposed by 2026-11-29 (N81). R4 opened on 2026-11-23 and was escalated to Isabel Ferreira this week: the customer DPA does not name the model vendor as a subprocessor, which has stalled the Halvard Marine and Ostrander Group quotes since that date (R4, N79). Overall is AMBER, not RED, because the one red (R4, DPA) blocks two Enterprise prospects in S-6 and touches nothing in the S-1 launch or EXP-1; it needs Isabel Ferreira's decision by 2026-12-03.

Correction: last week's report recorded overall GREEN (N80), but seat metering was already off plan (AMBER) and the DPA gap was already RED by then (see the "last week" column below); this report corrects those last-week colours rather than carrying the earlier report's GREEN forward as evidence of anything.

## 3. Workstream status

| Workstream | Colour | Last week | What changed | Green: evidence / Amber: back-to-green date / Red: decision, decider, needed by |
|---|---|---|---|---|
| Design partners, phase 1 (N43 to N45) | GREEN | GREEN | Phase 1 window closed 2026-11-22; exit condition met on 2026-11-23: 4 of 6 partners at 70% or better first-submission approval, 224 of 412 eligible reports drafted (54%), 173 of those approved first time (77%) | Evidence: product analytics and platform approval events for the phase 1 window (N44, N45; dashboard tiles T-4 M-003 and T-2 M-006 in ledgerline-dashboard-spec.md; GTM plan phase table); LEDGERLINE-S2 and S3 live since 2026-11-10; 14 account executives briefed 2026-11-05 (N84); phase 2 entry gated on this and opened on schedule |
| EXP-1 exposure (N54 to N56, N81) | GREEN | GREEN | Exposure running since 2026-11-23; 1,885 of 2,900 S-1 accounts exposed by 2026-11-29, split across the control and anchored arms | Evidence: exposure event count from product analytics (`pricing_offer.exposure_event`, N81), reported by Kwame Boateng as a count only, since the funnel tile T-7 stays analyst-restricted until 2026-12-18; GTM plan phase table. The pre-declared sizing target of about 1,270 accounts per arm (N55) is the reference point the 2026-12-04 exposure-window close is tracked against |
| Seat metering, DEP1 (R2, ADR-007) | AMBER | AMBER (reported GREEN last week; correction, see section 2) | DEP1 and LEDGERLINE-S1 shipped 2026-11-19, but 214 legacy annual-invoice accounts cannot be billed mid-term through the seat meter; R2 gap confirmed against the 214-account legacy list (N82), manual-invoice-line procedure agreed with billing | Back to green by 2026-12-04 if billing confirms the manual-line workaround covers the remaining legacy accounts through the exposure window; red on 2026-12-04 if not, with a decision on excluding legacy annual-invoice accounts from the offer (decider Priya Nair with the billing lead) |
| German-language receipt extraction (R3) | AMBER | AMBER | Wrenfield Labs at 61% first-submission approval on 33 drafted reports, mostly German-language receipts, at the phase 1 exit reading (N45); no later reading yet. The labeled eval set (DEP5) is in progress | Back to green by 2026-12-11 if the 300-receipt eval set (DEP5) scores 90% field accuracy or better; if under 90%, becomes a decision on 2026-12-11: exclude German-language accounts from the offer or fund the extraction fix (decider Priya Nair with Maya Chen) |
| Customer DPA subprocessor terms (R4, DEP3) | RED | RED (reported GREEN last week; correction, see section 2) | The customer DPA does not name the model vendor as a subprocessor. Two Enterprise prospects, Halvard Marine and Ostrander Group, about 400 seats each and about $2,400 MRR each at the per-seat price (N79), are blocked from signing until it is resolved | Decision needed: accept the model vendor's standard subprocessor terms, with 30-day prompt retention and the existing no-training clause, or hold for bespoke terms. Decider: Isabel Ferreira, with the legal lead. Needed by 2026-12-03 so both Enterprise quotes can be countersigned before year end; each week later risks one or both slipping into 2027 |

## 4. Milestones

Baseline dates come from the GTM plan signed 2026-11-06, the experiment brief of 2026-11-05, and the dependency register (DEP3).

| Milestone | Baseline date | Current forecast | Slip (days) | Reason | Recovery, or "none, accepted by [name]" |
|---|---|---|---|---|---|
| Phase 1 live for six design partners | 2026-11-09 | 2026-11-10 | 1 | The internal metrics review that Gate 5 was held on ran on 2026-11-09, one day before phase 1 could open (N85) | None, accepted by Maya Chen |
| Phase 2 entry, EXP-1 exposure begins | 2026-11-23 | 2026-11-23 | 0 | On schedule; phase 1 exit condition met the same day | Not applicable |
| EXP-1 analysis date | 2026-12-18 | 2026-12-18 | 0 | On schedule; no change forecast this week | Not applicable |
| Metrics review and OKR scoring (Gate 6 read) | 2026-12-21 | 2026-12-21 | 0 | On schedule | Not applicable |
| Customer DPA subprocessor addendum (DEP3) | 2026-11-06 | 2026-12-03 | 27 | Legal has not closed the subprocessor language; two Enterprise deals are the visible cost | Recovery is the decision requested in section 5, needed by 2026-12-03 |

## 5. Decisions needed

| Decision | Options | Recommendation | Decider | Needed by | Cost of waiting a week |
|---|---|---|---|---|---|
| Customer DPA subprocessor terms for the model vendor, to be logged as D5 once decided | (a) accept the vendor's standard subprocessor terms, 30-day prompt retention, existing no-training clause; (b) negotiate bespoke terms first | (a), then notify Halvard Marine and Ostrander Group of the updated subprocessor list for acceptance. The standard terms already carry the no-training clause the internal build relied on, and the two blocked deals are worth about $4,800 MRR combined at the current per-seat price (N79) | Isabel Ferreira, with the legal lead | 2026-12-03 | Both Enterprise quotes, Halvard Marine and Ostrander Group, slip a further week each and risk moving past year end; no change to EXP-1 either way, since Enterprise accounts sit outside S-1 (S-6) |

## 6. Risks and dependencies that moved

| Item (register #) | Movement (new / worse / same / retired) | Action this week | Owner |
|---|---|---|---|
| R4, customer DPA subprocessor gap | worse, escalated | Opened 2026-11-23, reported GREEN last week in error and corrected here; raised to Isabel Ferreira for D5; appears in section 5 above and in the section 8 escalation row | The legal lead, escalated to Isabel Ferreira |
| R2, seat metering cannot bill legacy annual-invoice accounts | same, partially mitigated | R2 gap confirmed against the 214-account legacy list (N82); manual-invoice-line procedure agreed with billing; coverage confirmed by 2026-12-04 | Priya Nair, with the billing lead |
| R3, foreign-language receipt extraction | same | DEP5's labeled eval set in progress, scoring due 2026-12-11 | Priya Nair |
| DEP1, seat metering for add-ons | delivered, with the R2 gap noted above | Closed as delivered on 2026-11-19; the residual gap is carried under R2, not reopened here | Priya Nair, with the billing lead |

## 7. Commitments

**Last week's, accounted for:**

| Committed last week | Done (yes / no) | If not, why, and when |
|---|---|---|
| Open R2 mitigation with the billing lead, following the 2026-11-16 risk opening | Yes | Manual-invoice-line procedure agreed with billing this week; coverage confirmed by 2026-12-04 (N82) |
| Open phase 2, EXP-1 exposure, on 2026-11-23 | Yes | Exposure began on schedule; 1,885 of 2,900 accounts exposed by 2026-11-29 (N81) |
| Escalate the DPA gap once it blocked a live deal | Yes | Raised this week as R4 and as the decision in section 5, after it blocked the Halvard Marine and Ostrander Group quotes; escalation row in section 8 |

**Next week's, three to five:**

| Commitment | Owner | Evidence that will show it happened |
|---|---|---|
| Close the DPA decision with Isabel Ferreira and the legal lead | Maya Chen | A signed decision-log entry (D5) dated on or before 2026-12-03 |
| Confirm the manual-invoice-line workaround covers the remaining legacy annual-invoice accounts through the exposure window | Priya Nair, with the billing lead | Billing confirmation against the 214-account legacy list (N82), or a decision item if it does not |
| Continue EXP-1 exposure to the 2026-12-04 close and hold the funnel tile restricted to the analyst per the dashboard spec | Kwame Boateng | Exposure event count in product analytics reaching or exceeding the sizing target of about 1,270 accounts per arm (N55) |

## 8. Escalations

R4 went red on 2026-11-23; last week's report showed it GREEN in error, corrected in this report (see section 2). It was escalated to Isabel Ferreira this week, on 2026-11-30, with a response due 2026-12-03; it also appears as the decision request in section 5.

| Item | First reported red | Escalated to | On | Response due |
|---|---|---|---|---|
| R4, customer DPA subprocessor gap (DEP3) | Went red 2026-11-23; first reported red 2026-11-30 (the 2026-11-23 report showed GREEN in error) | Isabel Ferreira | 2026-11-30 | 2026-12-03 |

---

## Exit gate (feeds Gate 4: acceptance criteria met, and Gate 5)

- [x] Every amber row carries a back-to-green date. Seat metering: 2026-12-04. German-language extraction: 2026-12-11, with a decision fallback if the eval set misses the 90% threshold
- [x] Every red row carries a decision, a decider, and a needed-by date, and appears in section 5. The DPA row: decision in section 5, decider Isabel Ferreira with the legal lead, needed by 2026-12-03
- [x] Every green row carries evidence a reader can open. Phase 1 exit cites a dashboard tile and the GTM plan phase table; EXP-1 exposure cites the exposure event count reported by Kwame Boateng, not a dashboard tile, since the funnel tile stays analyst-restricted until 2026-12-18; both cite the data sheet rows behind them (N44, N45, N81)
- [x] Overall status is no better than the worst workstream, or the report says why. Overall is AMBER, not RED, because the DPA red is isolated to the Enterprise segment (S-6), outside the S-1 launch population and EXP-1, and section 2 states that exception
- [x] Every milestone slip carries a reason and a recovery or an accepting name. The phase 1 slip: accepted by Maya Chen. The DPA slip: recovery is the section 5 decision
- [x] Every commitment from last week is accounted for. Section 7, all three marked done
- [x] Any red older than two reports has an escalation row. R4 went red 2026-11-23 and was escalated to Isabel Ferreira on 2026-11-30; the row is in section 8
- [x] The ILLUSTRATIVE row has been deleted
- [x] Signed by Maya Chen, product manager, 2026-11-30

Related: the [journey index](ledgerline-journey.md) for the full cast, data sheet and timeline; [ledgerline-gtm-plan.md](ledgerline-gtm-plan.md) for the launch phases this report tracks; [ledgerline-experiment-brief.md](ledgerline-experiment-brief.md) for the EXP-1 rule this report does not preempt; [decision-log.md](../templates/execution/decision-log.md) and the journey's Decisions table for D5, the DPA decision this report's red row requests; [ledgerline-metrics-review.md](ledgerline-metrics-review.md) for D6, the pivot decided three weeks after this report was filed.
