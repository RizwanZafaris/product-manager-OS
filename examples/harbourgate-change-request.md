# Change Request: CR-1, AC-3 re-baseline after provider migration decision

Fills [templates/execution/change-request.md](../templates/execution/change-request.md). Everything here is invented: Harbourgate is a fictional retailer, every person is fictional, and every number and date is ILLUSTRATIVE, drawn from the [Harbourgate journey](harbourgate-journey.md) and [Harbourgate coverage sheet](harbourgate-coverage-sheet.md).

**Requested by:** Ife Adeyemi · **CR owner:** Ife Adeyemi · **Raised:** 2026-05-21 · **Decision needed by:** 2026-05-28 · **Status:** Approved

## 1. The change

- **From:** AC-3 compared the percentage ramp against the per-provider decline-rate baselines N13 to N15.
- **To:** AC-3 compares each migrated cohort against that provider's baseline plus 0.5 percentage points over a trailing 7 days, as N16.
- **Baseline reference:** Gate 2 attempt 2, signed 2026-04-07 against N13 to N15; D-011, dated 2026-04-14; AC-3 in HARBOURGATE-S1 and HARBOURGATE-S2.
- **Trigger:** D-017, dated 2026-05-21, reversed D-011 after the fraud team saw double authorisations on 2026-05-19 during the percentage ramp with shadow comparison. D-017 moved the migration to one provider at a time behind a per-provider flag and sent AC-3 back to Gate 2.
- **Why now, and what happens if it waits:** The acceptance criterion must describe the provider-by-provider migration before the next baseline is treated as signed. If it waits, the team has two competing definitions of success, and the re-baselined migration cannot be assessed consistently.

## 2. Options

| Option | What it means | Impact in one line |
|---|---|---|
| Accept as proposed | Re-baseline AC-3 for each migrated cohort against that provider's baseline plus 0.5 percentage points over a trailing 7 days, N16, and retain D-017's per-provider flag approach. | Moves the completion date from 2026-06-30 to 2026-07-26, with a range of 3 to 6 weeks and about 20 engineer-weeks absorbed. |
| Accept reduced: retain D-017 but do not re-baseline AC-3 | Migrate one provider at a time behind a per-provider flag, while continuing to judge AC-3 against the existing percentage-ramp comparison. | The migration shape and the signed criterion would not match, leaving the baseline ambiguous. |
| Defer to the provider-by-provider migration release | Do not re-sign AC-3 at this change request. Revisit the criterion when the provider-by-provider migration is ready for its next release decision. | Leaves the Gate 2 acceptance criterion unresolved while D-017 is in force. |
| Reject | Reject D-017's change and fix the retry logic, then continue the percentage ramp and shadow comparison from D-011. | Preserves the original comparison approach and date, but leaves the double-authorisation risk that led to D-017. |

## 3. Impact assessment

| Dimension | Baseline | After the change | Delta | Range (low / high) | Assessed by |
|---|---|---|---|---|---|
| Scope (stories, acceptance criteria) | AC-3 compared the percentage ramp against N13 to N15. | AC-3 compares each migrated cohort against its provider baseline plus 0.5 percentage points over a trailing 7 days, N16. | AC-3 re-signed; no new story. | One acceptance criterion changed; no separate numeric range supplied. | Tomasz Wierzbicki |
| Schedule (milestones, Gate 4 date) | Completion date 2026-06-30. | Completion date 2026-07-26. | About one month later, N44. | 3 to 6 weeks, HC28. | Tomasz Wierzbicki |
| Cost (build, run) | Existing plan before D-017. | About 20 engineer-weeks of squad time, calculated as 5 engineers x 4 weeks, absorbed with no new budget, HC28. | About 20 engineer-weeks absorbed; no new budget. | No separate cost range supplied. | Tomasz Wierzbicki |
| Quality and non-functional targets | AC-3 used the percentage-ramp comparison against N13 to N15. | AC-3 uses N16 for each migrated cohort. | The comparison unit changes from the percentage ramp to the migrated cohort; the 0.5 percentage point tolerance remains. | One acceptance criterion; no separate numeric range supplied. | Tomasz Wierzbicki |
| Risk (new or changed register rows) | R1, shadow-comparison retries authorise the same card twice, score 4, L2 x I2. | D-017 closes R1 by removing the shadow-comparison path and uses a per-provider flag. | R1 changes from open risk to closed on 2026-05-21. | Score remains 4 before closure; no new numeric range supplied. | Ife Adeyemi |
| Dependencies (other teams, needed-by dates) | Gate 2 acceptance was signed on 2026-04-07 against N13 to N15. | Gate 2 attempt 3 re-signs AC-3 on 2026-05-28 under D-018. | Gate 2 re-sign required before the changed baseline is used. | One Gate 2 attempt; no separate numeric range supplied. | Ife Adeyemi |
| Compliance (regulated overlay, if it applies) | Existing Harbourgate payment controls and provider obligations remain in force. | No compliance target or regulated overlay is changed by CR-1. | No compliance scope change. | Not applicable. | Hamid Qureshi |

## 4. What we give up

The team gives up the same-day side-by-side comparison data that D-011 was designed to produce, and the original completion date of 2026-06-30. It accepts a completion date of 2026-07-26, with a range of 3 to 6 weeks, and absorbs about 20 engineer-weeks with no new budget. In return, the team stops the shadow-comparison retry path that produced the double-authorisation risk and measures each migrated cohort against a criterion that matches the approved migration shape.

## 5. Recommendation

- **Option:** Accept as proposed, because D-017 has already changed the migration from a percentage ramp to one provider at a time behind a per-provider flag. N16 makes AC-3 measurable against the unit actually being migrated, while preserving the 0.5 percentage point tolerance and the trailing 7-day comparison.
- **Conditions:** Gate 2 attempt 3 must re-sign AC-3 on 2026-05-28 under D-018, with Ife Adeyemi as decision owner and Priya Raman as the finance co-signer.

## 6. Approvals

| Role | Name | Decision (approve / approve with conditions / reject) | Conditions | Date |
|---|---|---|---|---|
| Accountable for scope changes | Ife Adeyemi | Approve | AC-3 re-signed under D-018 at Gate 2 attempt 3. | 2026-05-28 |
| Engineering lead | Tomasz Wierzbicki | Approve | About 20 engineer-weeks absorbed; completion moves to 2026-07-26, with a range of 3 to 6 weeks. | 2026-05-27 |
| Sponsor (when budget or a committed date moves) | Rohan Iyer | Approve | Sponsor approval required because the committed date moves from 2026-06-30 to 2026-07-26. | 2026-05-27 |
| Regulatory owner (regulated products only) | Hamid Qureshi | Not applicable | CR-1 changes AC-3 and the migration comparison unit, not the compliance overlay. | 2026-05-28 |

Priya Raman co-signed AC-3 on 2026-05-28 under D-018.

## 7. After approval

- [x] Decision log entry D-018 created, naming CR-1
- [x] PRD or one-pager version bumped, with the change noted in its change history
- [x] Acceptance criterion AC-3 changed and re-signed
- [x] Roadmap row and capacity plan updated for the move from 2026-06-30 to 2026-07-26
- [x] Risk and dependency register rows updated, including R1's closure after D-017
- [x] Status report carries the new baseline from the next issue
- [x] Teams affected told, through the payments channel and finance weekly, of CR-1's approval on 2026-05-28 (the underlying D-017 operational decision was communicated on the same channel earlier, on 2026-05-21)

---

## Exit gate (feeds Gate 4: acceptance criteria met)

Done when every box is honestly ticked. The approved request travels with its decision log entry to Gate 4, which asks that every scope change since Gate 2 has a decider.

- [x] The change is stated as from and to, with the baseline version it changes
- [x] Reject and defer were assessed as options, not listed for form
- [x] Every impact row carries a delta with a range and the name that assessed it
- [x] What we give up is written
- [x] Approvers are the accountable names from the RACI; the sponsor signed if money or a date moved
- [x] The decision log entry exists and names this CR, D-018
- [x] Baseline documents were updated after approval, not before
- [x] Signed by the CR owner, Ife Adeyemi, 2026-05-28
