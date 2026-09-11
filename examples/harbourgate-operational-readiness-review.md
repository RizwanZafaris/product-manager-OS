# Operational Readiness Review: Harbourgate Quay

Fills [templates/operate/operational-readiness-review.md](../templates/operate/operational-readiness-review.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and pound is ILLUSTRATIVE, drawn from the [Harbourgate journey](harbourgate-journey.md) and the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md). See the [examples index](README.md).

**Owner:** Tomasz Wierzbicki, Engineering Lead · **Date:** 2026-07-07 · **Status:** Complete with carried gaps C1 and C2; rechecked at Gate 6 on 2026-10-14 (HC16) · **Service:** Quay payment service

**Service owner:** Tomasz Wierzbicki · **On-call lead:** Bea Lindqvist · **Review date:** 2026-07-07 · **Gate 6 recheck:** 2026-10-14 (HC16)

## 1. Service overview

Quay authorises, captures, voids and refunds Harbourgate card payments through Kestrel for the web store, app and kiosks, while preserving the legacy payment table shape for downstream consumers.

- What it does, in one sentence a responder can act on: Quay is the payment path to check first when a customer cannot pay, a payment outcome is missing, or a refund follows an order authorised on the legacy path.
- Criticality tier: Tier 1, revenue-critical (HC14) · Users affected when down: every customer attempting a card payment on the web store, app or kiosk, with every card payment surface affected by a Kestrel outage (R4).
- Upstream dependencies: Kestrel authorisation API and hosted fields, Kestrel terminal SDK on kiosks, Kestrel status webhooks, the order service, the fraud rules engine and the payment routing flag.
- Downstream consumers: the checkout clients, the order service and order-history page, fraud and risk, finance reconciliation and the finance ERP export.

## 2. Runbooks

The review found that the high-risk operational paths had been exercised, with the settlement-file runbook and the support runbook carried as C1 and C2 until their stated completion dates.

| Scenario | Runbook location | Last rehearsed | Rehearsed by |
|---|---|---|---|
| Roll back a provider cohort to the legacy path | Quay operations runbook, rollback section | 2026-07-04 (N40) | Bea Lindqvist and Tomasz Wierzbicki |
| Respond to a missing settlement file | Quay operations runbook, settlement section | 2026-07-02, synthetic failure check (N72) | Bea Lindqvist |
| Restore the ledger backup into a clean environment | Quay recovery runbook, restore section | 2026-07-03 (HC17) | Bea Lindqvist |
| Respond to a payment support ticket | Support runbook | 2026-07-10, published and support briefed (HC19) | Callum Fraser and Bea Lindqvist |

C1 was the settlement-file-absent page and its production verification, owned by Bea Lindqvist, due 2026-07-09. C2 was publication of the support runbook and briefing of support, owned by Callum Fraser, due 2026-07-10. Both were closed before the Gate 6 recheck.

## 3. On-call and escalation

- Rotation: the payments squad's five engineers, one week each (HC15) · Paging tool and policy: the on-call paging tool pages the first responder for a payment-path breach; lower-severity support tickets wait for the support path.
- Escalation path: the scheduled on-call engineer, then Bea Lindqvist after 15 minutes, then Tomasz Wierzbicki after 30 minutes. A page is acknowledged within 5 minutes (HC15).
- The one person who knows this system best, and the plan for when they are away: Bea Lindqvist owns Quay's reconciliation service and the integrations register. The rotation names another engineer as the first responder each week, with escalation to Bea Lindqvist and then Tomasz Wierzbicki.

The rollback decision does not wait for discussion when the documented trigger is met: a cohort decline rate above its baseline plus 2 percentage points over 30 minutes, or Kestrel 5xx above 2% of calls over 5 minutes (N17).

## 4. Backup and recovery

- Data covered by backups: the payment ledger and its authorisation records · Backup cadence: continuous point-in-time backup with a nightly snapshot (HC17).
- Recovery point objective (max acceptable data loss): 0 minutes for authorisations, because Kestrel is the record and the local write is in the same transaction (N30) · Recovery time objective: 30 minutes during the drain, from flag flip to legacy, and 60 minutes after sunset for Kestrel region failover (N29).
- Last successful RESTORE test, not backup test: 2026-07-03, into pre-production, by Bea Lindqvist; it took 38 minutes (HC17).
- Where restore steps live: Quay recovery runbook, restore section, with the clean-environment procedure used for the 2026-07-03 test.

The restore test is evidence that the backup can be recovered, not only that backup jobs run. The 30-minute drain objective is supported by the rollback rehearsal, which took 3 minutes 50 seconds to flip to legacy and 22 minutes to restore after flag removal (N40).

## 5. Blast radius and containment

- Worst credible failure and who it reaches: a Kestrel outage stops every card payment on every Harbourgate surface, because Quay routes every card payment through Kestrel after the provider migration (R4). Kiosk customers can receive the “pay at the till” fallback within 10 seconds, with the basket held for 30 minutes (N31), but web and app card payments remain unavailable until recovery or rollback.
- Kill switch or feature flag to isolate this service or feature: the per-provider routing flag isolates a provider cohort. It supports a 5% first cohort before a wider shift (N46), and the rollback rehearsal proved the flag flip to legacy in 3 minutes 50 seconds (N40). A flag change requires two named approvers and is logged with both names (AC-6, BR-007).
- Rate limits and load shedding in place: Quay observes Kestrel's 50 req/s total rate limit across consumers and handles 429 responses with `Retry-After` (N61). The Kestrel call policy uses an 8-second timeout and one retry after 2 seconds on a network error only, with the same idempotency key (N61). This prevents uncontrolled retries from increasing load on the provider and protects the checkout path from duplicate authorisations.

## 6. Checks derived from past incidents

HG-INC-14's verified corrective actions A2 to A5, together with the R1 double-authorisation failure, are now standing checks rather than one-time fixes.

| Past incident (yours or a neighboring team's) | Check added here | Evidence it holds | Verified date |
|---|---|---|---|
| HG-INC-14, a pre-production job consumed the production settlement file | Every environment has a separate SFTP drop, and pre-production credentials cannot read the production drop | A failed production-drop read attempt verified A2 | 2026-06-26 |
| HG-INC-14, no page existed when a settlement file was absent | The settlement-file-absent check pages by 07:45 when no file has landed since 06:30 | The withheld-file synthetic check fired at 07:46 and the runbook completed in 11 minutes (N72); the live page was verified after the release | 2026-07-10 |
| HG-INC-14, the ingestion job did not fail safely when no file was present | The production ingestion job exits non-zero on “no file”, so the scheduler cannot treat an absent file as success | The behaviour is covered by the CI check for A4 | 2026-06-26 |
| HG-INC-14, the abort left pre-production schedules enabled | Every abort checklist includes disabling every pre-production schedule | The checklist was used in the rehearsal 2 abort drill | 2026-06-27 |
| R1, shadow-comparison retries authorised the same card twice | No shadow authorisation runs beside the live authorisation. A decline offers one retry with a different method, and the same card is never re-submitted automatically | D-017 removed the shadow-comparison path; AC-5 and BR-001 are checked in the release and support paths | 2026-05-21 |
| HG-INC-14 and R1, operational safety depended on a single unobserved path | At every cohort change, the on-call lead checks the per-provider flag, the rollback trigger, the settlement-file alert and the idempotency behaviour before approving the change | The Gate 5 runbook and rollback evidence were rechecked with the operational readiness review at Gate 6 | 2026-10-14 |

## 7. Gaps found by this review

| Gap | Risk if unfixed | Owner | Fix by |
|---|---|---|---|
| C1: the settlement-file-absent page was not yet live in production at the review | A missing settlement file could delay finance close without paging the on-call lead, repeating HG-INC-14 | Bea Lindqvist | 2026-07-09 |
| C2: the support runbook was not yet published and support had not yet been briefed | Support could not give consistent guidance for declined payments, kiosk fallback or legacy-authorised refunds | Callum Fraser | 2026-07-10 |

C1 and C2 were carried gaps, not reasons to conceal the readiness state. C1 was verified through N72 and the live page. C2 was verified when the runbook was published and support was briefed. Both were closed by the Gate 6 recheck.

## How this review fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| A rota with no names | Slots filled with a team name or a placeholder, signed off as complete | Every slot names a primary and a backup, and both know they are on it |
| Runbooks never executed | Reviewed, tidied, and never once run end to end | At least one full execution per runbook, recently, with the elapsed time recorded |
| Alerts that page for everything or nothing | Dashboards green while the pager is silent through a real breach | Each alert links to a runbook and has a tested path to a named human |
| Backups never restored | “Backups are running” in the report, and no restore attempted | A restore into a clean environment on a stated cadence, checked against the source |
| Sign-off by a team | Several leads approve, and nobody owns it after launch | One named accountable approver per service, with a date |

## Exit gate

This review passes when:

- [x] Every runbook scenario in section 2 exists and the highest-risk one was rehearsed. The rollback, settlement-file, restore and support paths are named, and the rollback and restore paths were timed.
- [x] The escalation path is names and thresholds, not team labels. The path is the scheduled on-call engineer, Bea Lindqvist after 15 minutes, and Tomasz Wierzbicki after 30 minutes, with acknowledgement within 5 minutes.
- [x] A restore has actually been tested, not just backups taken. The 2026-07-03 restore into pre-production took 38 minutes.
- [x] A kill switch or containment mechanism exists, or its absence is a gap row with a date. The per-provider flag supports a 5% cohort and a timed rollback.
- [x] Section 6 has at least one row, because no team has zero relevant incident history. It carries checks from HG-INC-14 and R1.
- [x] Every gap has an owner and a date. C1 belongs to Bea Lindqvist and C2 belongs to Callum Fraser, with dates recorded and both closed before the Gate 6 recheck.

Signed: Tomasz Wierzbicki, Engineering Lead and service owner, 2026-10-14, Gate 6 recheck (HC16)
