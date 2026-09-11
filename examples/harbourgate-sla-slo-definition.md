# SLA and SLO Definition: Harbourgate Quay payment service

Fills [templates/delivery/sla-slo-definition.md](../templates/delivery/sla-slo-definition.md). Everything here is invented: Harbourgate, Quay, Kestrel and every person are fictional, and every number, date, rate and pound is ILLUSTRATIVE, drawn from [harbourgate-journey.md](harbourgate-journey.md) and [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md). It is never to be quoted as a benchmark or copied as a target.

**Owner:** Bea Lindqvist · **Date:** 2026-07-08 · **Status:** Approved at Gate 5 attempt 2, GO WITH CONDITIONS; rechecked at Gate 6 on 2026-10-14

## 1. Service and users

| Field | Value |
|---|---|
| Service or feature | Quay payment service, covering the web checkout, app checkout and kiosk payment step through the Kestrel authorisation API and terminal SDK |
| Who depends on it | Harbourgate shoppers paying by card on the web, app or kiosk; checkout and order services; finance operations; fraud and risk; support; store operations |
| Criticality tier | Tier 1, revenue-critical, per Harbourgate's service catalogue v2 (HC14) |
| Contract holder for the SLA | None, there is no external SLA for Harbourgate Quay |
| Measurement source of truth | Quay operations dashboard, with the decline event stream for SLI-4 |

## 2. Service level indicators

| SLI id | What is measured, in user terms | Good event | Valid event, with exclusions | Measured where |
|---|---|---|---|---|
| SLI-1 | Whether the payment step accepts an authorisation attempt | A valid payment-step authorisation attempt completes successfully through Quay and Kestrel | Every payment-step authorisation attempt, excluding health checks and requests rejected for bad input before an authorisation attempt is made | Quay operations dashboard |
| SLI-2 | Authorise latency, end to end, at p95 | The authorisation attempt receives its outcome within the target latency | Every valid authorisation attempt from the payment step, excluding health checks and requests rejected for bad input before an authorisation attempt is made | Quay operations dashboard |
| SLI-3 | Whether a kiosk shows an outcome within 10 seconds, per shop per day | The kiosk payment attempt shows an outcome within 10 seconds | Every valid kiosk payment attempt, grouped per shop per day, excluding health checks and requests rejected for bad input before a payment attempt is made | Quay operations dashboard |
| SLI-4 | Whether a decline can be understood and traced | Every declined authorisation carries the provider, reason class and trace id | Every declined authorisation recorded in the decline event stream, excluding health checks and requests rejected for bad input before an authorisation attempt is made | Decline event stream |

## 3. Service level objectives

| SLI id | Target | Window (rolling or calendar) | Rationale and evidence | Owner |
|---|---|---|---|---|
| SLI-1 | 99.9% of minutes | Monthly | This is the availability requirement from N25 and the observability SLO. No baseline existed when the target was set. The first-month reading on Quay traffic was 99.94% for 2026-07-13 to 2026-08-11 (HC20). | Bea Lindqvist |
| SLI-2 | p95 authorise latency of 2,000 ms | Rolling 30 days | N23 set the target before production measurement. No baseline existed when the target was set. The first-month reading was 1,380 ms for 2026-07-13 to 2026-08-11 (HC20). | Bea Lindqvist |
| SLI-3 | 99.5% of kiosk payment attempts show an outcome within 10 seconds, per shop per day | Per shop per day, reviewed over the rolling 30-day window | N32 sets the store-floor target and the 10-second user outcome. No baseline existed when the target was set. In the Gate 6 window, the reading was 1,705 of 1,708 shop-days meeting the outcome measure (HC20). | Bea Lindqvist |
| SLI-4 | 100% of declines carry provider, reason class and trace id | Rolling 30 days | AC-4 requires every decline to carry these fields. No baseline existed when the target was set. The Gate 6 reading was 100% completeness (HC20 and N20). | Bea Lindqvist |

**Baseline measured before targets were set:** no. No baseline existed when the targets were set. First-month readings were collected from 2026-07-13 to 2026-08-11 in the Quay operations dashboard (HC20).

## 4. Service level agreement

No external SLA exists for Harbourgate Quay. The Harbourgate service has no customer contract commitment with a remedy attached.

| Commitment | Backed by SLO | SLA threshold | Remedy | Exclusions (maintenance, force majeure, customer-caused) | Where the contract text lives | Owner |
|---|---|---|---|---|---|---|
| No external SLA for Harbourgate Quay | None | None | None | None | No external contract text | None |

The only dependency SLA is Kestrel's committed 99.9% monthly availability (N26), held by Anneliese Vogt. It equals the Quay availability SLO of 99.9% (N25), rather than being looser than it. This equality is the accepted single-provider dependency risk R4: a Kestrel outage stops every card payment on every surface. R4 was accepted by Rohan Iyer in D-022 on 2026-08-24, with the kiosk fallback, the peak freeze and quarterly review.

## 5. Error budget policy

The availability budget is derived from the 99.9% SLO over 30 days:

- 30 days × 24 hours × 60 minutes = 43,200 minutes
- 100% minus 99.9% = 0.1%
- 43,200 × 0.1% = 43.2 minutes

| Field | Value |
|---|---|
| Budget per window | 43.2 minutes per 30 days, which is 0.1% of 43,200 minutes |
| At 50% of budget consumed | Ife Adeyemi and Tomasz Wierzbicki review the burn with on-call. After the last cohort, this review is the governing policy. Before 2026-09-07, the observability rule applied: no cohort advances |
| Budget exhausted | No Quay change except a rollback ships until the budget review is complete |
| Who decides exceptions | Ife Adeyemi and Tomasz Wierzbicki |
| Who has agreed to enforce this | Tomasz Wierzbicki, 2026-07-08 |

The Gate 6 reading was about 8 minutes spent in the window, which is 0.02% of 40,320 minutes (HC21). The first-month reading was about 26 minutes spent (HC21).

## 6. Alert thresholds

| Alert | SLO | Condition (burn rate or error rate) | Lookback window | Severity (page / ticket) | Routes to | Runbook |
|---|---|---|---|---|---|---|
| Cohort rollback trigger | SLI-1 | Cohort decline rate is above the provider baseline plus 2 percentage points, or Kestrel 5xx is above 2% of calls | 30 minutes for cohort decline rate; 5 minutes for Kestrel 5xx | page | On-call engineer, with rollback called by on-call without discussion | [harbourgate-support-runbook.md](harbourgate-support-runbook.md) |
| Kiosk store-floor outcome alert | SLI-3 | Any shop is below 95% of kiosk payment attempts showing an outcome within 10 seconds | 2 hours | page | On-call engineer and store operations | [harbourgate-support-runbook.md](harbourgate-support-runbook.md) |
| Settlement-file-absent alert | SLI-1 | No settlement file has landed since 06:30, checked at 07:45 | 75 minutes | page | On-call engineer and finance operations | [harbourgate-support-runbook.md](harbourgate-support-runbook.md) |

The settlement-file-absent alert was live in production on 2026-07-09 (N34). A synthetic failure check on 2026-07-02 withheld the Marlowe file in pre-production, the page fired at 07:46, and the runbook was completed in 11 minutes (N72).

**Burn-rate gap recorded at Gate 6:** no burn-rate alert exists. The three alerts above are threshold alerts, not burn-rate alerts. Bea Lindqvist owns the gap, due 2026-11-12, before the peak freeze (HC23 and N64).

## 7. Review cadence

| Review | Cadence | Attendees | Inputs | Decisions it may take |
|---|---|---|---|---|
| SLO review | Monthly, with the Gate 6 recheck on 2026-10-14 | Bea Lindqvist, Ife Adeyemi, Tomasz Wierzbicki, on-call lead | Budget consumption, SLO readings, incidents, pages and customer complaints | Tighten, loosen or retire an SLO; change the error budget policy; prioritise the burn-rate alert gap |
| SLA review | Not applicable, there is no external SLA | Bea Lindqvist and Anneliese Vogt if the dependency contract changes | Kestrel SLA reports and the accepted R4 risk | Record a dependency change or escalate R4 for a new decision |
| Post-incident | After each budget-affecting incident | Attendees per [harbourgate-incident-postmortem.md](harbourgate-incident-postmortem.md) | Incident postmortem, SLO impact and alert performance | Add or move an alert; change a runbook; propose an SLO or policy change |

## Exit gate (feeds Gate 5: release readiness green)

Filled targets feed the observability line at Gate 5 and section 5 of [harbourgate-release-readiness.md](harbourgate-release-readiness.md); the SLO review feeds the Gate 6 metrics review.

- [x] Every SLI states good events, valid events, and the exclusions, and names one measurement source
- [x] Every SLO has a target, a window, a rationale with evidence, and an owner
- [x] A baseline was measured before targets were set, or the date one will exist is written down. No baseline existed when the targets were set; first-month readings are recorded in HC20
- [x] Every SLA threshold is looser than the SLO behind it, and its contract text has an owner and a location. No external SLA exists; the dependency SLA N26 equals the SLO and is recorded as accepted risk R4
- [x] The error budget policy names actions at each stage and the person who agreed to enforce it
- [x] Every paging alert links a runbook that exists
- [x] Signed by Bea Lindqvist, 2026-07-08; rechecked by Bea Lindqvist at Gate 6, 2026-10-14
