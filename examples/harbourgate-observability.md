# Observability Requirements: Quay payment service

Fills [templates/architecture/observability.md](../templates/architecture/observability.md). Everything here is invented: Harbourgate is a fictional mid-market retailer, Quay is the fictional payment service that replaces checkout-pay, Kestrel, Marlowe and Tidewater are fictional payment providers, every person is fictional, and every number, date and threshold is ILLUSTRATIVE, carried from the shared data sheet in the [Harbourgate journey](harbourgate-journey.md) rather than from any real payments stack. See the [examples index](README.md).

**Stage:** DESIGN, feeds [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md); re-checked at Gate 5
**Knowledge:** [knowledge index](../knowledge/INDEX.md)
**Skill:** [architect agent](../agents/architect-agent.md); [metrics-tree](../skills/metrics-tree/SKILL.md) for the product metrics it must emit

**System:** Quay · **Owner:** Bea Lindqvist, Senior Engineer, payments · **Date:** 2026-04-09
**Status:** Approved at Gate 3, 2026-04-10; current as of 2026-07-10 (A3 live)

## 1. Service level objectives

Four SLO targets, drafted alongside the NFR and reviewed at Gate 3 on 2026-04-10, before a line of Quay's code existed, so the design had numbers to build against rather than an adjective; two (latency, decline fields) still lack a window, see exit gate. SLO 3's target and alert thresholds were provisional at Gate 3; agreed by Lena Baptiste on 2026-06-25 (NFR section 2).

| SLI (what is measured, from the user's view) | Target | Window | Measured where |
|---|---|---|---|
| Payment step accepts an authorisation attempt | 99.9% of minutes (target, N25) | monthly (N25) | Uptime monitor on the authorise call, per the NFR (N25) |
| Authorise latency, end to end, p95 | 2,000 ms (target; 1,350 ms measured, N23) | no window specified in N23; target only | Quay application metrics; measured 1,350 ms in the Kestrel sandbox load test, 2026-06-05 (N23) |
| Kiosk shows a payment outcome within 10 s | 99.5% of attempts, per shop per day (target, N32) | daily, per shop | Kestrel terminal SDK response, per shop, aggregated daily, per the NFR (N32) |
| Decline carries provider, reason class and trace id | 100% of decline events (target, AC-4) | no window specified in AC-4; target only | Decline event stream (AC-4, N20) |

The product metric Quay answers to, payment-step non-completion (11.1% at entry, N5), is emitted and shown on the dashboard in section 5.

- Error budget policy, availability SLO: during the drain, spending the monthly availability budget for the payment step pauses further per-provider cohort advances (a cohort already at 100% is not rolled back for this alone). Once the last legacy flag is removed (planned 2026-09-21, N49), spending the budget means only rollbacks and reliability changes ship until Ife Adeyemi and Tomasz Wierzbicki review the burn with on-call, the same shape as the N64 freeze.
- The latency, kiosk and decline-field SLOs carry no separate budget consequence recorded on this data sheet; their breach is a page (section 4) or a dashboard read (section 5), not a policy trigger.
- The fourth SLO is the one that could not have existed on the old path: Marlowe logged no declines at all before Quay, so "at least as good as the old path", the test Gate 2 set, had nothing to compare against on this measure until Quay produced its own event stream.

## 2. Logs

| Event class | Fields required (minimum) | Retention | PII handling |
|---|---|---|---|
| Request logs | timestamp, route, status, latency, caller id, trace id | 13 months, assumption: aligned to decline event retention, owner Anneliese Vogt (no request-log class on the retention schedule, N58) | No card number logged; truncated PAN only (first 6, last 4 retained; the full PAN never reaches the log, AC-1) |
| Business events | event name, entity id, actor, outcome, trace id, including every decline (AC-4) | 13 months (N58) | Truncated PAN and expiry only, 13 months (N58); no cardholder name in this stream |
| Security events | per [security-architecture.md](harbourgate-security-architecture.md) section 3 | assumption: no security-event class on the retention schedule, owner Anneliese Vogt | No PAN, no cardholder name in this stream; approver names kept per AC-6. Card token and wrapper-log retention are governed by N58, not by this stream |

Settlement files sit outside this table's event classes: they are provider files ingested, matched and reconciled, not application log lines, and Quay retains them 7 years (N58).

## 3. Traces and correlation

- Trace propagation: a trace id generated at the first Quay call, web, app or kiosk terminal SDK, carried in a traceparent header on every outbound call to Kestrel (I-1), Marlowe (I-5) and Tidewater (I-7), and on every inbound event from the fraud rules stream (I-9). Kestrel status webhooks (I-2) and inbound provider settlement files (I-4, I-6, I-8) cannot carry Quay's trace id; those lines are joined to the trace by order id instead.
- One id joins user report to logs to trace: the order id. A support agent enters it in the support tool and gets the decline event, the Kestrel call, and, for a legacy-authorised order still inside the reconciliation drain, the matching settlement line from ADR-0004's classified straddle set.

## 4. Alerts

The three alerts below were written at different times. The rollback trigger's decline-rate and Kestrel 5xx thresholds (N17) existed at Gate 3, before Quay carried live traffic; the kiosk floor alert existed at Gate 3 with provisional thresholds, agreed 2026-06-25. The rollback trigger's cohort wording and its plan v2 runbook link did not: no cutover plan existed yet at Gate 3 (D-019's plan v1 followed on 2026-06-02), and the cohort wording and the plan v2 runbook link below were only added once D-021 reshaped the plan (2026-06-18 to 2026-06-25), so "every paging alert links a runbook that exists" could not have been true for this row at Gate 3, only from 2026-06-25 on. The third alert exists because the first two did not catch what happened on 2026-06-15.

| Alert | Condition and threshold | Severity (page / ticket) | Routes to | Runbook |
|---|---|---|---|---|
| Rollback trigger | Cohort decline rate above baseline plus 2 percentage points over a rolling 30 minutes, or Kestrel 5xx above 2% of calls over 5 minutes; on-call may call it without discussion (N17) | page | on-call engineer | cutover plan v2 rollback runbook, `runbooks/quay/rollback.md` (added with cutover plan v2, 2026-06-25, under D-021) |
| Kiosk floor degraded | Any shop below 95% of attempts showing an outcome within 10 s, over 2 hours (N32) | page | on-call engineer, with store operations notified | kiosk fallback runbook, `runbooks/quay/kiosk-fallback.md` |
| Settlement file absent | No file has landed by 07:45 for a provider whose file was due at 06:30; added 2026-06-19 as AC-13, live in production 2026-07-09 (N34, A3) | page | on-call engineer | finance daily-close runbook, `runbooks/quay/settlement-file-absent.md` |

The settlement-file-absent alert is the one this document exists to explain. It did not exist on 2026-06-15, when the pre-production rehearsal's ingestion job consumed and deleted the Marlowe production settlement file at 07:00: nothing paged, because nothing watched for a file's absence, only for its content once it arrived. A finance analyst noticed the empty reconciliation view by hand at 08:10, 70 minutes after the file vanished; the close finished 5 hours 40 minutes late (N41, N42). Corrective action A3 closed that gap, owned by Bea Lindqvist, verified twice: first by the synthetic check below, then by the alert's first live production page on 2026-07-10 (A3).

This gap traces back to D-019's rejected shape: a one-weekend freeze-move-switch cutover needed a verify phase run against a real Marlowe file, and with no Marlowe sandbox (DEP-2, R3) and a shared pre-production SFTP drop (F2), rehearsal 1 reached for the live one, which is how HG-INC-14 happened. The alternative considered and rejected was relying only on corrective action A4 (the ingestion job exiting non-zero on "no file") with no page: a failed job that alerts nobody watching the close does not close the gap that mattered, which is why AC-13 added a page on top of A4 rather than replacing it.

Against these pre-set thresholds, HG-INC-14 itself breached nothing: payment-step availability, latency, the kiosk floor and decline-field completeness all held on 2026-06-15, because the only user harmed was finance, whose daily-close timeliness this table did not yet cover. The settlement-file-absent alert is a deliberate cause-based exception to alerting only on symptoms users feel: finance's close has no SLO in section 1, so the alert is the only signal for a harm this document otherwise does not measure.

## 5. Dashboard

- Dashboard location: Quay operations dashboard, internal, `dashboards/quay-ops` · Dashboard owner: Bea Lindqvist
- Shows, at minimum: each of the four SLOs above with budget remaining, traffic and error rate per provider connector, authorise latency p95, decline rate per cohort against its baseline (N13 to N15) and the N16 tolerance (the readable form of N17's decline-rate leg; N17's Kestrel 5xx leg has no tile here and is watched only in the on-call rollback trigger itself), payment-step non-completion (the core product metric, N5/N19), and the health of every row in the integrations register: I-1 (Kestrel authorisation API), I-2 (Kestrel status webhooks; its fallback-rate watch is the same one named on this dashboard in the integrations register), I-3 (Kestrel terminal SDK on kiosks), I-4 (Kestrel settlement file), I-5 (Marlowe authorisation API, legacy), I-6 (Marlowe settlement file) and I-7 (Tidewater through the wrapper, legacy) and I-8 (Tidewater settlement file), each row showing time since last successful call or file. I-9 to I-11 are internal feeds watched on the fraud and finance dashboards rather than repeated here.
- I-6 carries a standing note on the dashboard: no sandbox exists for Marlowe settlement files, so this row's health has only ever been provable against production data, which is what made a rehearsal reach for the live drop in the first place.

## 6. Synthetic failure check

- Check performed: Marlowe's settlement file withheld deliberately in pre-production, the same absence HG-INC-14 had caused for real seventeen days earlier, this time on purpose and watched for.
- Date and operator: 2026-07-02, Bea Lindqvist (N72).
- Result: the page fired at 07:46, one minute past the 07:45 threshold. That is one minute outside AC-13's "a page fires by 07:45"; the one-minute evaluation lag was accepted by Tomasz Wierzbicki as within tolerance, and AC-13 was not reworded to match. The runbook ran as written and was completed in 11 minutes (N72); the check exists to prove A3 before production depended on it. The alert went live in production on 2026-07-09 (N34, C1), and its first live page on 2026-07-10 (A3) is the second verification.
- Fixes filed from the check: none against the alert itself. The one-minute miss against AC-13 was accepted as within tolerance by Tomasz Wierzbicki, not by Bea Lindqvist, who ran the check and owns A3. The check is the verification record A3 names against its own due date of 2026-07-09.

## Exit gate

- [ ] Every SLO has a target, a window, and a measurement location: four rows, sourced to N25, N23, N32 and AC-4, but N23 (latency) and AC-4 (decline fields) carry no sourced window on the data sheet; open, owner Bea Lindqvist, to add a window to N23 and AC-4 or record one as a target with an owner
- [x] The error budget policy names what changes when the budget is spent, and who decides: during the drain, spend pauses per-provider cohort advances; once the last legacy flag is removed (planned 2026-09-21, N49), spend means only rollbacks and reliability changes ship until review, the same shape as the N64 freeze; decided by Ife Adeyemi, with Tomasz Wierzbicki reviewing the burn with on-call
- [x] Log fields, retention, and PII handling are stated per event class: three rows plus the settlement-file note; request-log and security-event retention are recorded as an assumption owned by Anneliese Vogt, since the retention schedule (N58) has no request-log or security-event class of its own
- [x] Every paging alert links a runbook that exists: the cutover plan's rollback runbook, the kiosk fallback runbook, and the finance daily-close runbook
- [x] The dashboard exists at the linked location and has a named owner: Bea Lindqvist
- [x] A synthetic failure check has been run and its result recorded: 2026-07-02, page at 07:46, runbook completed in 11 minutes (N72)
- [x] The example SLO row has been replaced with real ones: the template's placeholder "requests answered successfully, non-5xx" row is gone; all four rows above are Quay's own

Reviewed at [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md), accepted 2026-04-10 alongside the rest of the design set with the first two alerts and all four SLO targets in place (two without a window, see exit gate; SLO 3's target and alert thresholds were provisional at Gate 3, agreed by Lena Baptiste on 2026-06-25); the settlement-file-absent alert was added afterward under AC-13 and re-checked at [Gate 5](../os/STAGE-GATES.md) attempt 2 on 2026-07-08, where its delivery was recorded as condition C1, met 2026-07-09. Signed off by Bea Lindqvist, Senior Engineer, payments, as owner of the dashboard and of the alerts this document defines. See the [Harbourgate journey](harbourgate-journey.md) for the incident that produced the fourth alert and for the wider narrative around the synthetic check that proved it.
