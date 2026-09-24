# UAT Plan: Harbourgate Quay payment service

Fills [templates/delivery/uat-plan.md](../templates/delivery/uat-plan.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and pound is ILLUSTRATIVE, drawn from [harbourgate-journey.md](harbourgate-journey.md) and [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md).

**Owner:** Noor Haddad · **Business sponsor:** Priya Raman · **Window:** 2026-06-29 to 2026-07-06

**Candidate build:** rc-2026-07-02.3 · **Environment:** pre-production, with production-shaped schemas, synthetic card tokens and its own settlement-file drop · **Fixture set:** harbourgate-seed-2026-07-02

## 1. Scope

- Flows under acceptance: daily finance close with the straddle set, including AC-8; refunding an order authorised on a legacy provider under BR-002 and AC-7; declining a card and offering one retry with a different method under AC-5; reading order history and reporting from unchanged Quay rows under AC-9; and invoking step-up authentication above £250 under AC-11.
- Explicitly out of scope: kiosk payment flows, because those are left to the store cohorts and their store-floor testing.
- Basis documents: [harbourgate-journey.md](harbourgate-journey.md) · [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md) · [harbourgate-testing-strategy.md](harbourgate-testing-strategy.md)

## 2. Entry criteria

UAT starts only when all of these hold:

- [x] QA exit criteria from the [testing strategy](harbourgate-testing-strategy.md) are met
- [x] No open S1 or S2 defects on the flows in scope
- [x] The UAT environment is seeded with realistic, non-production data: pre-production, with production-shaped schemas, synthetic card tokens and its own settlement-file drop under HC8 and A2
- [x] Testers below are confirmed and have access
- [x] Rehearsal 3 has passed with no issues, and the rollback timing has been rehearsed: rehearsal 3 took 4 h 45 min on 2026-07-04, with flag flip to legacy in 3 min 50 s and restore after flag removal in 22 minutes, under N39 and N40

## 3. Testers

| Name | Role | Workflow they own | Time committed | Confirmed |
|---|---|---|---|---|
| Priya Raman | Head of Finance Operations | Daily finance close, settlement reconciliation and the straddle set | 6 h across the window | yes |
| Saoirse Whelan | Fraud and Risk Lead | Decline handling, retry behaviour and step-up authentication | 3 h across the window | yes |
| Callum Fraser | Support Lead | Customer-facing refund investigation and the legacy-authorised refund path | 4 h across the window | yes |
| Grace Mbeki | Data Engineering Lead | Reporting and the order-history read from the legacy table shape | 3 h across the window | yes |

Total committed time: 6 h + 3 h + 4 h + 3 h = 16 h.

## 4. Test charters

| # | Charter (the job to attempt) | Done looks like | AC / requirement IDs | Tester | Build | Evidence | Result | Defect | Exception |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Run the daily close end to end, including the straddle set created by the provider transition | AC-8 passes, the straddle set is classified, reconciliation is within the £50 per provider per day tolerance, and there are 0 unmatched lines | AC-8 | Priya Raman | rc-2026-07-02.3 | UAT log, daily close, entry 08 | Pass | none | none |
| 2 | Request a refund against an order authorised on a legacy provider | BR-002 and AC-7 pass, the refund reaches the provider that authorised the order, and the order's refund status is clear to support | AC-7, BR-002 | Callum Fraser | rc-2026-07-02.3 | UAT log, refunds, entry 04 | Pass | none | none |
| 3 | Attempt a payment with a declined card, then retry with a different method | AC-5 passes, the declined card is not re-submitted automatically, and the customer can proceed with the different method | AC-5 | Saoirse Whelan | rc-2026-07-02.3 | UAT log, decline handling, entry 11 | Pass | none | none |
| 4 | Check an order made through Quay in order history and reporting | AC-9 passes, the order-history page and reporting read Quay's rows unchanged, with no visible change to the existing workflow | AC-9 | Grace Mbeki | rc-2026-07-02.3 | UAT log, reporting, entry 19 | Pass | none | none |
| 5 | Attempt a card-not-present order above £250 | AC-11 and BR-005 pass, step-up authentication is invoked exactly when the threshold requires it, and the payment can continue after the challenge | AC-11, BR-005 | Saoirse Whelan | rc-2026-07-02.3 | UAT log, step-up authentication, entry 22 | Pass | none | none |

Kiosk flows are not UAT charters. They remain with the store cohorts.

## 5. Defect handling during UAT

| Severity | Meaning during UAT | Action |
|---|---|---|
| S1 | Tester cannot complete a scoped job at all | UAT pauses, fix before resuming |
| S2 | Scoped job completes only with a workaround | Fix inside the window or sponsor accepts in writing |
| S3 / S4 | Friction or cosmetic | Logged, prioritized after launch |

- Defects logged in: the UAT log · Triage cadence during the window: recorded in the UAT log as issues were reviewed

The outcome was 0 S1, 0 S2, 1 S3 and 1 S4. The S3 was the known N62 issue, reason class "other" on some Kestrel declines. The S4 was an unclear column label in the reconciliation view. Neither blocked a charter.

## 6. Exit criteria and sign-off

UAT passes when:

- [x] Every charter has run against candidate build rc-2026-07-02.3, and none is Blocked: 5 of 5 ran on that build
- [x] Every charter's Result is Pass, or that charter names a defect record and an approved exception in the register below whose retest result is recorded: 5 of 5 Pass, so the register is empty
- [x] No open S1; every accepted S2 has the sponsor's written acceptance attached: 0 S1 and 0 S2
- [x] Testers answered "would you use this over the current way?" and the answers are recorded: UAT log, 4 of 4 testers answered yes

**Accepted exceptions**

| Exception ID | Charter # | Defect ID | Severity | Business impact accepted | Approved by (name, role) | Date | Retest result |
|---|---|---|---|---|---|---|---|

The register is empty because no charter failed. The two logged issues, the N62
S3 and the S4 column label, blocked no charter, so neither is an exception to
this gate: they are post-launch work, tracked in the UAT log.

**Sign-off form**

| Name | Role | Verdict (Accept / Accept with conditions / Reject) | Conditions, if any | Date |
|---|---|---|---|---|
| Priya Raman | Business sponsor | Accept with conditions | Accepts the N62 S3 known issue and the S4 unclear reconciliation column label for post-launch prioritization. UAT evidence is signed against rehearsal 3, N39, and the rollback timing, N40. | 2026-07-06 |
| Noor Haddad | QA Lead and UAT owner | Accept with conditions | Same two logged issues remain visible in the UAT log. No kiosk flows are included here; those remain with the store cohorts. | 2026-07-06 |

**Sign-off is bound to candidate build:** rc-2026-07-02.3

If the candidate changes after this date the verdicts above are void: the five
charters were run against rc-2026-07-02.3 and nothing else. Re-run them against the new
build, re-record the results, and sign again.

## Exit gate

This document passes when:

- [x] Testers are named individuals who own the workflow, with committed time
- [x] Charters describe jobs, not click scripts
- [x] Entry and exit criteria are objective enough to be applied without a meeting
- [x] Every charter names the build it ran against, its acceptance criteria and its evidence
- [x] Every failed charter has a defect record and an approved exception with a retest result: no charter failed, so the register is empty
- [x] The sign-off form is complete, including any conditions in writing, and names the candidate build it accepts

Signed: Noor Haddad, QA Lead and UAT owner, 2026-07-06
