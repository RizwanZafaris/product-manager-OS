# SLA and SLO Definition: Aldergate Core, real-time posting and overnight batch

Fills [templates/delivery/sla-slo-definition.md](../templates/delivery/sla-slo-definition.md). Everything here is invented: Aldergate Core is a fictional core-banking platform run by Lyndmoor Bank, a fictional regional retail bank, the people are roles filled by invented names, and every number, date and identifier is ILLUSTRATIVE. Regulatory statements are as of 2026-09-11 and should be confirmed with counsel; this is not legal advice. Regulatory context is drawn from [the core-banking domain card](../knowledge/domains/core-banking.md). See the [examples index](README.md).

**Owner:** Priya Nandakumar, head of core platform · **Date:** 2026-09-11 · **Status:** Approved at Gate 5, 2026-09-18

## 1. Service and users

Aldergate Core is Lyndmoor Bank's ledger of record for retail and SME deposit accounts. It performs two distinct jobs that customers experience differently: real-time posting (when a payment or transfer lands, the balance must update immediately, and the customer expects to see it), and overnight batch (end-of-day processing that closes the books, runs interest accrual, statementing, and feeds every downstream reconciliation). A single blended "uptime" number measures neither, because a customer trying to pay rent at 02:00 cares only about the real-time path, and the bank's operational-resilience lead cares most about whether the batch closes before branch and app opening.

| Field | Value |
|---|---|
| Service or feature | Aldergate Core: real-time balance and posting API (surface: mobile app, internet banking, branch teller terminal, ATM network) and overnight batch (surfaces: statementing, interest accrual, reconciliation feeds, regulatory reporting extracts) |
| Who depends on it | Lyndmoor Bank's 412,000 retail deposit customers, 8,100 SME accounts, branch tellers, the bank's operations team, downstream reconciliation systems (card processing, payment schemes, regulatory reporting) |
| Criticality tier | Tier 1 (highest); per Lyndmoor Bank's internal criticality taxonomy, rev. 4, 2025-11, which classifies any service whose unavailability prevents customers from accessing or moving their money as Tier 1 |
| Contract holder for the SLA | Lyndmoor Bank, represented by Dana Okonkwo, operational-resilience lead; the SLA is Schedule 4 of the Aldergate Core managed service agreement, MC-2024-0117 |
| Measurement source of truth | Aldergate Core's own SLI computation pipeline, running in the platform's observability stack and independently reconciled against the bank's monitoring feed each month |

## 2. Service level indicators

Two SLIs are carried unchanged from [the core-banking domain card](../knowledge/domains/core-banking.md), whose worked example sets the pairing. A third is added for the batch, because the batch-completion timing is distinct from real-time availability and latency and needs its own valid-event definition.

| SLI id | What is measured, in user terms | Good event | Valid event, with exclusions | Measured where |
|---|---|---|---|---|
| SLI-1 | Real-time balance and posting API: any request from a customer-facing surface that returns within the latency threshold | A request that returns a successful response within 2 seconds at the 95th percentile | Any authenticated API request from the mobile app, internet banking, teller terminal or ATM; exclusions: health checks, requests rejected for malformed input (HTTP 4xx not caused by a core fault), and requests during a pre-announced maintenance window that the bank has accepted in writing | Aldergate Core observability stack, request-level telemetry |
| SLI-2 | Real-time availability: the API is reachable and accepting work | One minute in which at least 99.5% of requests to the real-time API either succeed or fail fast with a core-caused error (not a caller error) | Every minute in the rolling window; no exclusion for the nightly batch window, because a customer trying to pay at 02:00 does not know batch is running and the domain card is explicit that the definition deliberately does not exclude it | Aldergate Core observability stack, minute-level reachability probe plus request telemetry |
| SLI-3 | Batch completion: the end-of-day batch closes before the named cut-off | A calendar day on which the full end-of-day batch run (ledger close, interest accrual, statementing, and all downstream reconciliation feeds) completes successfully by the cut-off | Every calendar day on which a batch is scheduled; exclusions: a day when the bank has formally declared a bank holiday and no batch is due, and a day when a scheduled maintenance window was agreed in writing at least five working days in advance | Aldergate Core batch scheduler, emitting a completion timestamp per run |

## 3. Service level objectives

One SLO per SLI. The rationale column earns each row. SLI-1's and SLI-2's targets and windows are carried unchanged from [the core-banking domain card](../knowledge/domains/core-banking.md). SLI-3's target of completion by 05:00 local is set to give a two-hour buffer before branch and app opening at 07:00.

| SLI id | Target | Window (rolling or calendar) | Rationale and evidence | Owner |
|---|---|---|---|---|
| SLI-1 | 2 seconds at the 95th percentile for real-time posting and balance requests | Rolling 30 days, continuous | Baseline measured 2026-05-01 to 2026-05-31: p95 latency was 1.4 seconds across 41 million requests. The 2-second target gives headroom for peak-hour load without masking degradation. Alerts fire before the SLO is breached so the team can act. | Priya Nandakumar, head of core platform |
| SLI-2 | 99.9% of minutes | Rolling 30 days, continuous | Carried unchanged from [the core-banking domain card](../knowledge/domains/core-banking.md). The definition deliberately does not exclude the nightly batch window. Baseline measured 2026-05-01 to 2026-05-31: 99.94% of minutes. | Priya Nandakumar, head of core platform |
| SLI-3 | Complete by 05:00 local every day a batch is scheduled | Rolling 90 calendar days, with a monthly reporting point | The cut-off is set two hours ahead of branch and app opening at 07:00, so a bank holiday or a slow run still closes before customers arrive. Baseline measured 2026-06-01 to 2026-08-31: median completion 03:48, 90th percentile 04:37, one run completing at 05:52 (2026-07-14), which triggered the error-budget spend in section 5. | Batch Operations Lead |

**Baseline measured before targets were set:** yes, from 2026-05-01 to 2026-08-31 across both the real-time path (31 days of request telemetry) and the batch path (92 batch runs in the 90-day window), source: Aldergate Core observability stack and batch scheduler logs.

## 4. Service level agreement

Each SLA commitment maps to an SLO tighter than the SLA threshold, so the team hears about trouble before the bank can claim a remedy. The SLA is Schedule 4 of managed service agreement MC-2024-0117. The remedies and exclusions below are contract language; the text is owned by Dana Okonkwo, operational-resilience lead for Lyndmoor Bank, and Priya Nandakumar for Aldergate, and it lives in MC-2024-0117 Schedule 4.

| Commitment | Backed by SLO | SLA threshold | Remedy | Exclusions (maintenance, force majeure, customer-caused) | Where the contract text lives | Owner |
|---|---|---|---|---|---|---|
| Monthly real-time availability | SLI-2 (99.9% of minutes) | 99.5% of minutes in any calendar month | Tier 1 credit: 5% of the month's service fee if availability falls below 99.5% but at or above 99.0%; 10% of the month's service fee if below 99.0%; a service credit rather than a refund, applied to the next invoice | Pre-announced maintenance windows accepted in writing at least five working days in advance; outages caused by the bank's own network or by customer error; force majeure | MC-2024-0117 Schedule 4, clause 4.2 | Dana Okonkwo (bank), Priya Nandakumar (Aldergate) |
| Daily batch completion before cut-off | SLI-3 (complete by 05:00 local) | Complete by 06:00 local on at least 96% of scheduled days in any calendar month | Tier 2 credit: 3% of the month's service fee for each percentage point below 96%, capped at 15% of the month's fee | Days when the bank has formally declared a bank holiday and no batch is due; a delay caused by a downstream system outside Aldergate's operational boundary and under the bank's control; force majeure | MC-2024-0117 Schedule 4, clause 4.3 | Dana Okonkwo (bank), Priya Nandakumar (Aldergate) |

Both thresholds are deliberately looser than the SLOs behind them: 99.5% SLA against 99.9% SLO gives the team a 0.4 percentage point buffer before any credit is owed, and a 06:00 SLA cut-off against a 05:00 SLO gives a one-hour buffer on the batch path.

## 5. Error budget policy

The error budget for the real-time path is the gap between 99.9% and 100% over the rolling 30-day window: 0.1% of the minutes. On a 30-day month that is 43.2 minutes of permitted unavailability. The error budget for the batch path is the gap between "every day a batch is scheduled" and "complete by 05:00 local": on a 30-day month, 3% of scheduled days (about one day in 30) is the permitted missed cut-off, so the budget is roughly one late batch per rolling 90-day window before a policy action.

The policy in section 5 is deliberately written to spend budget on a late batch even when the real-time path reads 100% available, because a batch completing after the cut-off compresses every downstream reconciliation window behind it, and the domain card is explicit that a batch that finishes late but before branch open looks fine on a blended metric while silently squeezing the reconciliation windows that follow.

| Field | Value |
|---|---|
| Budget per window | Real-time path: 43.2 minutes per rolling 30-day month (0.1% of minutes). Batch path: approximately one late batch per rolling 90-day window before a policy action is triggered. |
| At 50% of budget consumed (real-time path) | Review with the on-call lead; slow rollouts of non-critical changes; add capacity ahead of forecast peak. No freeze. |
| At 50% of budget consumed (batch path, meaning a second late batch within the window) | Batch Operations Lead and Priya Nandakumar review the scheduler's critical path; non-essential batch jobs are deprioritised behind ledger close, interest accrual and reconciliation feeds. No freeze on real-time changes. |
| Budget exhausted (real-time path, meaning availability has fallen below 99.9% for the month) | Feature freeze on the real-time path; reliability work takes priority; exceptions granted only by Priya Nandakumar, head of core platform. |
| Budget exhausted (batch path, meaning two or more late batches in the 90-day window) | The next real-time feature release is delayed to free capacity for batch-path reliability work, even if real-time availability reads 100% for the month. A late batch is a budget spend whether or not the real-time path is affected, because the reconciliation window compression is a downstream risk the bank bears. Exceptions granted only by Priya Nandakumar. |
| Who decides exceptions | Priya Nandakumar, head of core platform |
| Who has agreed to enforce this | Priya Nandakumar agreed on 2026-09-11, and Dana Okonkwo accepted the policy on behalf of Lyndmoor Bank on 2026-09-18 |

## 6. Alert thresholds

Two alerts per SLO: a fast burn that pages and a slow burn that files a ticket. For SLI-3, the alert is not only at failure, because a batch failing at 05:01 is already a breach; the alerts fire at batch-progress checkpoints, so the team can act on a slow run before the cut-off is missed.

| Alert | SLO | Condition (burn rate or error rate) | Lookback window | Severity (page / ticket) | Routes to | Runbook |
|---|---|---|---|---|---|---|
| Real-time API fast burn | SLI-2 | Burn rate above 14.4x (would exhaust a 30-day budget in 2 days) | 1 hour | page | Core Platform on-call | [support-runbook.md](../templates/delivery/support-runbook.md) |
| Real-time API slow burn | SLI-2 | Burn rate above 6x (would exhaust a 30-day budget in 5 days) | 6 hours | ticket | Core Platform team queue | [support-runbook.md](../templates/delivery/support-runbook.md) |
| Real-time latency breach | SLI-1 | p95 latency above 2 seconds for 10 continuous minutes | 15 minutes | page | Core Platform on-call | [support-runbook.md](../templates/delivery/support-runbook.md) |
| Batch progress checkpoint 1 | SLI-3 | Ledger close not complete by 01:00 local (expected 00:15, 45-minute early warning) | Per-run | ticket | Batch Operations Lead | [support-runbook.md](../templates/delivery/support-runbook.md) |
| Batch progress checkpoint 2 | SLI-3 | Interest accrual and statementing not complete by 03:30 local (expected 02:45, 45-minute early warning) | Per-run | page | Batch Operations on-call | [support-runbook.md](../templates/delivery/support-runbook.md) |
| Batch cut-off at risk | SLI-3 | Projected completion from current run rate is after 05:00 local, while the run is still in progress | Per-run | page | Batch Operations on-call and Priya Nandakumar | [support-runbook.md](../templates/delivery/support-runbook.md) |

Every paging alert above links a runbook that exists: [support-runbook.md](../templates/delivery/support-runbook.md) is the operational runbook Aldergate and Lyndmoor maintain jointly, and the batch checkpoint runbooks are its section 6.4.

## 7. Review cadence

| Review | Cadence | Attendees | Inputs | Decisions it may take |
|---|---|---|---|---|
| SLO review | Monthly | Priya Nandakumar (owner), Core Platform on-call lead, Aldergate product, Dana Okonkwo (bank operational-resilience lead, for the batch and resilience view) | Error-budget consumption on both paths, incidents, customer complaints, downstream reconciliation breaks | Tighten, loosen or retire an SLO; change the error-budget policy; adjust the batch cut-off |
| SLA review | Per contract cycle (annually, plus any month in which a remedy is paid) | Priya Nandakumar, Dana Okonkwo, Lyndmoor Bank procurement, Aldergate commercial | SLA reports sent, remedies paid, exclusions claimed | Renegotiate thresholds or exclusions; adjust the credit caps |
| Post-incident | After each budget-affecting incident | Per [incident-postmortem.md](../templates/operate/incident-postmortem.md) | Postmortem, timeline, contributing factors | Add or move an alert; adjust a response procedure |

The monthly SLO review is timed to a governance rhythm Lyndmoor Bank already runs. UK operational-resilience rules for banks and their critical service providers, under the PRA and FCA operational resilience framework (which requires firms to set impact tolerances for important business services), make this a natural home for the batch-completion discussion: a batch that completes late but before opening is not just an IT event for the bank, it is a pressure on the impact tolerance for the deposit and payment services the bank has mapped as important business services. That framing is as of 2026-09-11 and should be confirmed with counsel; the specifics of how Lyndmoor's own impact tolerances are expressed are the bank's responsibility, not Aldergate's. The SLO review therefore includes Dana Okonkwo in her operational-resilience role, so a batch-completion trend is seen against the bank's own tolerances while there is still budget left to act on it.

## Exit gate (feeds Gate 5: release readiness green)

Filled targets feed the observability line at [Gate 5](../os/STAGE-GATES.md) and section 5 of [release-readiness.md](../templates/delivery/release-readiness.md); the SLO review feeds [metrics-review.md](../templates/operate/metrics-review.md) at Gate 6.

- [x] Every SLI states good events, valid events, and the exclusions, and names one measurement source. SLI-1, SLI-2 and SLI-3 each do so in section 2.
- [x] Every SLO has a target, a window, a rationale with evidence, and an owner. Section 3 covers all three SLIs, with Priya Nandakumar as owner for SLI-1 and SLI-2, and the Batch Operations Lead for SLI-3.
- [x] A baseline was measured before targets were set, or the date one will exist is written down. Baselines measured 2026-05-01 to 2026-08-31; stated in section 3.
- [x] Every SLA threshold is looser than the SLO behind it, and its contract text has an owner and a location. Section 4: SLI-2's 99.9% SLO backs a 99.5% SLA; SLI-3's 05:00 cut-off backs a 06:00 SLA; text owned by Dana Okonkwo and Priya Nandakumar, located at MC-2024-0117 Schedule 4.
- [x] The error budget policy names actions at each stage and the person who agreed to enforce it. Section 5: Priya Nandakumar agreed to enforce on 2026-09-11; Dana Okonkwo accepted on behalf of the bank on 2026-09-18.
- [x] Every paging alert links a runbook that exists. Section 6: [support-runbook.md](../templates/delivery/support-runbook.md).
- [x] Signed by Priya Nandakumar, 2026-09-18.

---

## Exit-gate walk

I have walked the Gate 5 exit gate above and ticked each box against this document.

The SLI and SLO pair for real-time posting is carried unchanged from [the core-banking domain card](../knowledge/domains/core-banking.md): SLI-1 (p95 latency at 2 seconds) and SLI-2 (99.9% of minutes) with their windows, exclusions and owner kept as the card sets them. The batch path's SLI-3 is a distinct definition, measured against the 05:00 cut-off before branch and app opening at 07:00, and it does not share the real-time path's exclusions, because a batch that runs early and a batch that runs late are different failures for the customer. Section 4 sets the SLA to the bank with service credits at thresholds looser than the SLOs behind them. Section 5 spends error budget on a late batch even when the real-time path reads 100% available, because every downstream reconciliation window shrinks. Section 6 alerts at batch-progress checkpoints at 01:00, 03:30 and at the point the projected completion crosses the cut-off, not only at failure. Section 7 is a monthly review that includes Dana Okonkwo, Lyndmoor Bank's operational-resilience lead, so the batch trend is seen against the bank's own impact tolerances, with the UK operational-resilience framing as of 2026-09-11 and to be confirmed with counsel.

One item is flagged rather than ticked clean. The batch path's SLO window is stated as a rolling 90 calendar days, while the error-budget action in section 5 is expressed per 90-day window rather than per month. That is intentional (a single late batch is not a monthly problem) but the monthly SLO review reports on a 30-day slice of the window, so a review may see no budget consumption in a month that is carrying a late batch from earlier in the window. That reporting mismatch is noted here, owned by Priya Nandakumar, and to be resolved at the first monthly review on 2026-10-09.

Signed: Priya Nandakumar, head of core platform, 2026-09-18.
