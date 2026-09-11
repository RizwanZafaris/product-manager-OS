# Integrations Register: Quay Payment Service

Fills [templates/architecture/integrations.md](../templates/architecture/integrations.md). Everything here is invented: Harbourgate is a fictional mid-market retailer, Kestrel, Marlowe and Tidewater are fictional payment providers, Quay is the fictional payment service this register covers, every person is fictional, and every number, date and identifier is ILLUSTRATIVE, carried from the shared data sheet in the [Harbourgate journey](harbourgate-journey.md) rather than from any real payments stack. See the [examples index](README.md).

Stage: DESIGN, feeds Gate 3
Knowledge: [knowledge index](../knowledge/INDEX.md)
Skill: [architect agent](../agents/architect-agent.md)

**Scope:** Every boundary line Quay crosses, web, app and kiosk, across its live surface (Kestrel) and its two retiring legacy surfaces (Marlowe, Tidewater), plus the internal boundaries the payment step depends on.
**Register owner:** Bea Lindqvist, Senior Engineer, payments; caretaker of the contractor's wrapper from 2026-04-24 · **Date:** 2026-04-09, reviewed weekly through DELIVER, current as of 2026-10-16 · **Status:** Approved at Gate 3, 2026-04-10

## 1. Register

Eleven rows, I-1 to I-11. Four rows (I-5 to I-8, the two legacy providers) have carried no new authorisations since their cohorts reached 100% (Marlowe 2026-07-20, Tidewater 2026-08-17, N71); flags removed 2026-08-03 and 2026-08-31 (N49). They are scheduled for retirement on 2026-12-15 (D-024, sunset plan section 6), and as of 2026-10-16 they still carry refunds and settlement files.

| # | Counterparty system | Direction | Protocol | Auth | Counterparty SLA (and source) | Owner (ours) | Failure behavior (one clause) |
|---|---|---|---|---|---|---|---|
| I-1 | Kestrel authorisation API | Outbound | REST over TLS | OAuth 2.0 client credentials | 99.9% monthly availability, Kestrel MSA schedule 3 (N26) | Bea Lindqvist | A network error or timeout retries once after 2 s with the same idempotency key (N61); a 5xx is not retried; either returns 503 provider_unavailable; checkout shows "unavailable, try again shortly", not a decline. A 402 card decline offers retry on a different method (BR-001) |
| I-2 | Kestrel status webhooks | Inbound | HTTPS, HMAC-signed | Shared secret, rotated per Kestrel's key policy | Not stated in the MSA as recorded (N26) | Bea Lindqvist | Quay polls status on a missed webhook rather than leaving an order stuck at "pending" |
| I-3 | Kestrel terminal SDK on kiosks | Outbound | Vendor SDK over the store LAN | Terminal keys, per-device | 99.9% monthly availability, Kestrel MSA schedule 3 (N26) | Bea Lindqvist, with Lena Baptiste on the store side | Kiosk shows "pay at the till" within 10 s and holds the basket 30 minutes (BR-004, N31) |
| I-4 | Kestrel settlement file | Inbound, SFTP | Flat file, daily 06:30 (N33) | SFTP key, held by Bea Lindqvist | 99.9% monthly availability, Kestrel MSA schedule 3 (N26) | Bea Lindqvist | Page at 07:45 if no file has landed since 06:30 (N34, AC-13) |
| I-5 | Marlowe authorisation API | Outbound, legacy, plus inbound status callbacks | REST over TLS | API key outbound; callbacks unsigned, IP allowlist from 2026-04-17 (F3, R13) | 99.5% monthly availability, Marlowe contract of 2019, schedule 1 (N27) | Bea Lindqvist | Scheduled for retirement 2026-12-15; while live, customer saw a decline with retry offered, same as I-1; until 2026-07-20 BR-008 also retried Kestrel declines on the legacy path through this API; retired 2026-07-20; a refund on a legacy-authorised order failing is R7 (open, score 9) |
| I-6 | Marlowe settlement file | Inbound, SFTP, legacy | Flat file, daily 06:30, weekend settlements on Monday's file (N33) | SFTP key, no sandbox equivalent (DEP-2) | 99.5% monthly availability, Marlowe contract of 2019, schedule 1 (N27) | Bea Lindqvist | The file HG-INC-14 happened to: no arrival, no alert, a 5 h 40 min late finance close before A3's page existed |
| I-7 | Tidewater through the contractor's wrapper | Outbound, legacy | XML over HTTPS | Client certificate, expiring 2027-02-03 (N66) | No SLA clause in the 2021 contract (N28) | Bea Lindqvist, caretaker since 2026-04-24 | Kiosk falls back to "pay at the till" the same as I-3; scheduled for retirement 2026-12-15, certificate expiry falls after retirement and is moot; a refund on a legacy-authorised order failing is R7 (open, score 9) |
| I-8 | Tidewater settlement file | Inbound, SFTP, legacy | Flat file, weekly, Mondays 06:30 (N33) | SFTP key | No SLA clause in the 2021 contract (N28) | Bea Lindqvist | Scheduled for retirement 2026-12-15; a missed weekly file would block finance close the same way I-6's did; since 2026-07-09 it pages at 07:45 (A3, N34) |
| I-9 | Fraud rules engine | Internal, inbound event stream | Event stream | Internal service auth | Internal, no external SLA | Saoirse Whelan, DEP-6 | If the event stream is unavailable, checkout requires step-up authentication on every card-not-present order rather than falling open [OPEN: this degraded-mode behavior is not yet recorded in BR-005; owner Saoirse Whelan] |
| I-10 | Order service and order-history page | Internal, bidirectional | Shared database table (legacy shape, ADR-0002); Quay API calls for capture and refund | Internal service auth | Internal, no external SLA | Bea Lindqvist for the write side; Grace Mbeki for the read side (DEP-4) | If Quay's write fails the order is not marked paid; the order-history page keeps reading the old table shape unchanged, so a schema change here is a regression, not a feature (AC-9) |
| I-11 | Finance ERP export | Outbound, nightly | File export, from the reconciliation service | Internal service auth | Internal, no external SLA | Bea Lindqvist | A failed export blocks the day's close the same as a missing settlement file; covered by DEP-3's runbook |

## 2. Detail block, one per row

### Integration I-1: Kestrel authorisation API

- Purpose: Authorises every card payment on web and app; Kestrel is the record, and Quay commits its local write on Kestrel's response, reconciling any gap by idempotency key, not a shared local transaction, since an outbound call to Kestrel cannot take part in one (NFR section 2, system design section 1).
- Data exchanged: Card details via hosted fields, so no card number reaches a Harbourgate server (AC-1); the payload carries order amount, currency and a merchant reference. PII class: cardholder billing address and email, per the retention schedule (N58).
- Environments: Sandbox available; production credentials held by Bea Lindqvist and rotated per Kestrel's key policy.
- Failure behavior, expanded: A network error or timeout retries once after 2 s with the same idempotency key (N61); a 5xx is not retried; either returns 503 provider_unavailable after that; checkout shows "card payments are temporarily unavailable, try again shortly", not a decline, and the event is not counted as a decline. BR-001 applies only to a 402 card_declined response: the customer is offered one retry on a different method and no automatic re-submission occurs. Quay never falls back to Marlowe or Tidewater for this call; that cascade behaviour was BR-008 and it is retired.
- Backoff and retry policy: Timeout 8 s; one retry after 2 s on network error only, same idempotency key; idempotency window 24 h; rate limit 50 req/s total across consumers, 429 with Retry-After (N61, the API contract).
- Monitoring: Until 2026-09-21, Kestrel 5xx rate above 2% of calls over 5 minutes and decline rate per cohort above baseline plus 2 points over 30 minutes were both rollback triggers (N17), paging on-call, who could call the rollback without discussion. With the last legacy flag removed (N49), the N17 thresholds no longer trigger a flag flip; they page as incident signals, and a restore to legacy (22 minutes, N40) remains possible until 2026-12-15 (R10), alongside the SLO 1 availability alert (N25).
- Counterparty contact: Dani Ferreira, Kestrel merchant success manager; response SLA not recorded beyond N26's monthly availability commitment.
- Contract or DPA reference: Kestrel master services agreement, schedule 3, held by Anneliese Vogt.
- Change notice: Kestrel's API versioning notice channel, watched by Bea Lindqvist; no breaking change occurred inside this journey's window.

### Integration I-2: Kestrel status webhooks

- Purpose: Carries the asynchronous outcome of an authorisation or capture when it does not resolve synchronously on I-1.
- Data exchanged: Order reference, status, reason code. No card number crosses this boundary.
- Environments: Sandbox available; the signing secret is held by Bea Lindqvist.
- Failure behavior, expanded: A missing webhook leaves the order at "pending" locally; Quay polls I-1's status endpoint after a bounded wait rather than leaving the order stuck, so the customer-facing outcome never depends on webhook delivery alone.
- Backoff and retry policy: Kestrel retries delivery on its own schedule; Quay's poll fallback fires after a bounded wait once no webhook has arrived. Idempotency mechanism: every event carries an event id and the consumer dedupes on it, the same at-least-once-delivery rule the API contract states for this status event (API contract section on the status event).
- Monitoring: Webhook-to-poll fallback rate is watched on the same dashboard as I-1; a rising rate is treated as an early signal on I-1, not a separate incident class, and pages on-call through I-1's own alerts once it crosses those thresholds.
- Counterparty contact: Dani Ferreira, Kestrel merchant success manager; response SLA not recorded beyond N26's monthly availability commitment.
- Contract or DPA reference: Kestrel master services agreement, schedule 3.
- Change notice: Same channel as I-1.

### Integration I-3: Kestrel terminal SDK on kiosks

- Purpose: Runs the card-present transaction on the PIN pad at each of the 61 kiosks (N1, N2), certified against the kiosk model under DEP-1.
- Data exchanged: Card data stays on the PIN pad and Kestrel's terminal path; Quay receives only the outcome. PII class: none beyond the order reference.
- Environments: No sandbox terminal in every shop; store operations tested the certified model after certification was delivered on 2026-07-09 (DEP-1).
- Failure behavior, expanded: On a failed or timed-out call, the kiosk shows "pay at the till" within 10 s and holds the basket for 30 minutes (BR-004, N31); this is the kiosk store-floor SLO (N32), alerting when any shop is below 95% over 2 hours.
- Backoff and retry policy: One retry at the terminal layer per Kestrel's SDK default; no application-level retry, because a card-present retry at the till is the fallback, not a second SDK attempt.
- Monitoring: Kiosk store-floor SLO dashboard, per shop per day (N32), paging on-call with store operations notified when any shop is below 95% over 2 hours; weekly kiosk-use report to Lena Baptiste tracks whether associates keep using kiosks after seeing the fallback (R11).
- Counterparty contact: Dani Ferreira, Kestrel merchant success manager, for the SDK, response SLA not recorded beyond N26's monthly availability commitment; Lena Baptiste, Head of Store Operations, for kiosk firmware scheduling (DEP-5).
- Contract or DPA reference: Kestrel master services agreement, schedule 3; the terminal addendum is not itself on the data sheet, so cite schedule 3 as the recorded source (N26).
- Change notice: A firmware update was scheduled across 61 shops under DEP-5, delivered 2026-07-30, ahead of its 2026-08-01 need date.

### Integration I-4: Kestrel settlement file

- Purpose: Daily reconciliation source for what Kestrel actually settled against what Quay captured.
- Data exchanged: Settlement lines carrying amount, reference and outcome. PII class: masked PAN (first 6, last 4) and order reference; settlement files retained 7 years (N58, compliance impact assessment section 3). Previously conflicted with the security architecture's threat-model row for this component, which asserted no PII beyond the order reference; that row has since been corrected to masked PAN plus order reference, matching this entry and I-6/I-8 (harbourgate-security-architecture.md, settlement file ingestion, information disclosure row).
- Environments: Sandbox equivalent available; production SFTP key held by Bea Lindqvist.
- Failure behavior, expanded: A missing file pages on-call at 07:45 (N34, A3), verified live in production on 2026-07-10 by the same per-provider alert proven by the Marlowe synthetic failure check on 2026-07-02 (N72, 11-minute runbook; that check exercised A3 against a withheld Marlowe file, not this Kestrel one).
- Backoff and retry policy: No automatic re-request; the runbook behind the 07:45 page tells the on-call engineer to raise it with Kestrel directly. [OPEN: no idempotent-ingestion key (e.g. file name plus line reference) for a reissued settlement file is recorded on the data sheet; owner Bea Lindqvist]
- Monitoring: Settlement-file-absent alert (A3) pages on-call; reconciliation tolerance of £50 per provider per day on settled versus captured value, 0 lines on count once the straddle set is classified (N35).
- Counterparty contact: Dani Ferreira, Kestrel merchant success manager; response SLA not recorded beyond N26's monthly availability commitment.
- Contract or DPA reference: Kestrel master services agreement, schedule 3.
- Change notice: Same channel as I-1; file format changes would appear there first.

### Integration I-5: Marlowe authorisation API

- Purpose: Carried the Marlowe orders not yet shifted during the phased traffic shift (N71); no new authorisations since cohort 3 reached 100% on 2026-07-20; flag removed 2026-08-03 (N49); scheduled for retirement 2026-12-15 (D-024). Until 2026-11-15, refunds on legacy-authorised orders route here (BR-002, N50); from 2026-11-16 finance operations refunds through the provider portal (BR-009, to 2027-06-15, N52).
- Data exchanged: While live, the card number itself transited Harbourgate's own servers on this path, which is why this integration was inside PCI DSS assessment scope at entry (N55); its retirement is part of what takes PCI DSS scope from 7 at entry to 5 during the drain and a target of 3 after sunset (N55), pending assessor confirmation (DEP-7, G3).
- Environments: No sandbox for the authorisation API. (The settlement-file sandbox request, DEP-2, was against I-6, not this row; see I-6.)
- Failure behavior, expanded: While live, a decline surfaced the same as I-1: retry offered on a different method, no automatic re-submission (BR-001). BR-008's cascade, a Kestrel decline on the legacy path retried through Marlowe, ran until it was retired 2026-07-20 once the Marlowe cohort completed. A refund on a legacy-authorised order failing is R7 (open, score 9, owner Priya Raman, next review 2026-11-16).
- Backoff and retry policy: While live, no application-level retry beyond BR-001's customer-initiated one.
- Monitoring: Marlowe callbacks were unsigned at entry, a finding (F3) that became R13; an IP allowlist closed the exposure on 2026-04-17, and R13 closed fully on 2026-08-03 when the Marlowe flag was removed. No live alert remains on this boundary since the flag removed; the refund tail is watched through R7's weekly risk-register review (owner Priya Raman, next review 2026-11-16) until 2027-06-15 (N52).
- Counterparty contact: Marlowe merchant support, ticket queue only, 4-hour response commitment (N69); responded in 2 h 10 min on ticket MRL-88213 during HG-INC-14.
- Contract or DPA reference: Marlowe contract of 2019, schedule 1, held by Anneliese Vogt; termination notice sent 2026-09-14 for 2026-12-15 (D-023, DEP-8).
- Change notice: No proactive notice channel from Marlowe; changes were discovered through the ticket queue, which is one reason this integration is retired rather than kept.

### Integration I-6: Marlowe settlement file

- Purpose: The reconciliation source for Marlowe-settled orders, still receiving refund settlements until the legacy refund capability ends 2026-11-15 (BR-002, N50), scheduled for retirement 2026-12-15 (D-024); the file at the centre of HG-INC-14.
- Data exchanged: Settlement lines, amount and reference; PII class: masked PAN (first 6, last 4) and order reference, retained 7 years while it rides inside the settlement file (N58, compliance impact assessment section 3), which is why the compliance impact assessment's HG-INC-14 breach assessment treats this file as a personal-data event. Weekend settlements land on Monday's file (N33), which is why the file consumed on 2026-06-15 carried the weekend's settlements (N33).
- Environments: No sandbox; DEP-2 was requested and never delivered. Rehearsal 1 read the production drop instead, because R3's mitigation said to, and pre-production shared that same production SFTP drop (F2, R14) at the time.
- Failure behavior, expanded: At entry, a missing or malformed file had no alert: this is what happened on 2026-06-15, when rehearsal 1's ingestion job, left enabled in pre-production with the only credentials Marlowe issues, consumed and deleted the production settlement file at 07:00. Finance's daily close ran 5 h 40 min late (N41, N42); no page fired because no alert existed for a missing file. The corrective actions closed the gap: A2 separated the SFTP drops by environment (verified by a failed read attempt on 2026-06-26), A3 added the 07:45 page (verified 2026-07-10), and A4 made the production ingestion job exit non-zero on "no file" (verified in CI).
- Backoff and retry policy: No automatic re-request; a missing or malformed line is manually re-requested from Marlowe support through the ticket queue, 4-hour response commitment (N69). 1,529 of the 1,742 lines in rehearsal 1's production-shaped Marlowe file (2026-06-13, N37) carried legacy references Quay's reconciliation did not recognise, because settlement lags authorisation by up to three days and refunds lag by months: there is no instant at which this integration has nothing in flight, which is what D-019's freeze-move-verify-switch hypothesis assumed and rehearsal 1 disproved. ADR-0004's dual-path ledger, matching on either reference, replaced any attempt to freeze it. [OPEN: no idempotent-ingestion key for a reissued file, as happened in HG-INC-14, is recorded on the data sheet beyond the straddle-set classification; owner Bea Lindqvist]
- Monitoring: Settlement-file-absent alert (A3, live 2026-07-09) pages on-call; reconciliation tolerance £50 per day (N35); straddle set required to reach 0 lines by T+3 days after the cohort reached 100% (N36), closed 2026-07-23.
- Counterparty contact: Marlowe merchant support, ticket queue, 4-hour response commitment (N69).
- Contract or DPA reference: Marlowe contract of 2019, schedule 1; termination notice 2026-09-14 for 2026-12-15 (D-023).
- Change notice: None; see I-5.

### Integration I-7: Tidewater through the contractor's wrapper

- Purpose: Ran kiosk card-present authorisation for the 61 kiosks before the Kestrel terminal SDK cohort replaced it (N71); the Tidewater cohort reached 100% on 2026-08-17 (N71), the flag was removed 2026-08-31 (N49), and the integration has carried no new authorisations since; scheduled for retirement 2026-12-15 (D-024). Until 2026-11-15, refunds on legacy-authorised orders route here (BR-002, N50); from 2026-11-16 finance operations refunds through the provider portal (BR-009, to 2027-06-15, N52).
- Data exchanged: Card data through the wrapper; the wrapper's log files were found at the 2026-04-08 STRIDE walk to hold the masked PAN and cardholder name in plain text (F1, became R8). A scrubbing patch on the wrapper's logging path closed the live exposure on 2026-05-08 (F1, G2), approved by Hamid Qureshi as the named exception to the out-of-scope-wrapper decision (system design section 2, non-goals). The log files themselves are scheduled for deletion by 2027-01-15 (N58), a month after the 2026-12-15 shutdown and before the portal wind-down ends 2027-06-15 (N52).
- Environments: No sandbox; the wrapper was written by a contractor who left in 2021 and had no named owner until Bea Lindqvist was made caretaker on 2026-04-24 (R2, closed).
- Failure behavior, expanded: Kiosks fell back to "pay at the till" the same as I-3 (BR-004, N31). The client certificate on this integration expires 2027-02-03 (N66), after the retirement date, so its expiry does not force an emergency renewal. A refund on a legacy-authorised order failing is R7 (open, score 9, owner Priya Raman, next review 2026-11-16).
- Backoff and retry policy: No documented retry behaviour in the wrapper; this absence of documentation is part of why the wrapper is retired rather than kept, per ADR-0003's rejected-option reasoning: a routing layer over all three providers lost on operational risk, evidenced by the wrapper itself.
- Monitoring: No monitoring existed on the wrapper at entry beyond the kiosk store-floor SLO's downstream effect; the STRIDE walk (2026-04-08) and the scrubbing patch (2026-05-08) are the closest this integration got to instrumented review. No live alert remains on this boundary since the flag removed 2026-08-31; the refund tail is watched through R7's weekly risk-register review (owner Priya Raman, next review 2026-11-16) until 2027-06-15 (N52).
- Counterparty contact: Tidewater contract notice address (cutover plan section 6); no named Tidewater contact exists in the integrations register and no response-time commitment in the 2021 contract (N28). Wrapper configuration itself is held by Bea Lindqvist as caretaker (R2).
- Contract or DPA reference: Tidewater contract of 2021, no SLA clause (N28), no data-processing clause covering the wrapper's log retention at entry (G1); closed 2026-07-31 by agreeing in writing that the logs are deleted at sunset, before the first kiosk cohort shifted. Termination notice sent 2026-09-14 for 2026-12-15 (D-023, DEP-8).
- Change notice: None; the wrapper's origin (a departed contractor) is the reason.

### Integration I-8: Tidewater settlement file

- Purpose: The weekly reconciliation source for Tidewater-settled kiosk orders; has carried no new authorisation lines since the flag was removed 2026-08-31 (N49); refund settlements continue until the legacy refund capability ends 2026-11-15 (BR-002, N50); scheduled for retirement 2026-12-15 (D-024).
- Data exchanged: Settlement lines, amount and reference, weekly on Mondays (N33); PII class: masked PAN (first 6, last 4) and order reference, retained 7 years while it rides inside the file (N58, compliance impact assessment section 3).
- Environments: No sandbox equivalent recorded.
- Failure behavior, expanded: A missed weekly file would block finance close as I-6's did; since DEP-3's dual-path runbook (delivered 2026-07-08) and A1's reconciliation service (ADR-0004), both legacy files are covered under one classified straddle set, and since 2026-07-09 a missing file pages on-call at 07:45 (A3, N34).
- Backoff and retry policy: No automatic re-request; a missing weekly file is raised through the Tidewater contract notice address (cutover plan section 6), with no response commitment (N28). Straddle set required to reach 0 lines by T+8 days after the Tidewater cohort reached 100% (N36), the longest drain of the three because the file itself only arrives weekly. [OPEN: no idempotent-ingestion key for a reissued file is recorded on the data sheet beyond the straddle-set classification; owner Bea Lindqvist]
- Monitoring: Same reconciliation tolerance and straddle-set discipline as I-6 (N35, N36); settlement-file-absent alert (A3, live 2026-07-09) pages on-call.
- Counterparty contact: Tidewater contract notice address (cutover plan section 6); no named individual and no response-time commitment in the 2021 contract (N28); see I-7.
- Contract or DPA reference: Tidewater contract of 2021; termination notice 2026-09-14 for 2026-12-15 (D-023).
- Change notice: None.

### Integration I-9: Fraud rules engine

- Purpose: Flags card-not-present orders for step-up authentication above the £250 threshold or on a fraud-rule match (BR-005, N57).
- Data exchanged: Order amount, risk signals, decision outcome. No card number crosses this boundary.
- Environments: Internal; no sandbox distinction beyond the usual internal test environment.
- Failure behavior, expanded: If the event stream is unavailable, checkout requires step-up authentication on every card-not-present order rather than falling open to the existing threshold alone. [OPEN: this stream-unavailable behaviour is not recorded in BR-005, which as written covers only the £250 threshold and fraud-flag trigger, both mandatory with no waivable exception; below £250 with no flag the built-in path is requesting an exemption, not step-up. Adding a degraded-mode rule is a change to that policy and routes through Saoirse Whelan together with Anneliese Vogt and Hamid Qureshi per BR-005's own change-control clause; owner Saoirse Whelan]
- Backoff and retry policy: Internal event delivery retry per the platform default; no bespoke policy recorded for this boundary.
- Monitoring: Owned by Saoirse Whelan's team; delivered against DEP-6 on 2026-07-06, ahead of its 2026-07-13 need date. [OPEN: no named alert for the event stream itself going unavailable is recorded on the data sheet; owner Saoirse Whelan]
- Counterparty contact: Saoirse Whelan, Fraud and Risk Lead.
- Contract or DPA reference: Internal; no external DPA.
- Change notice: Internal change process; no external counterparty.

### Integration I-10: Order service and order-history page

- Purpose: Reads and writes the legacy payment table shape, which the order-history page, finance reporting and reconciliation all depend on (ADR-0002).
- Data exchanged: Order and payment status rows in the legacy shape. PII class per the data model's retention schedule (N58).
- Environments: Internal; the same production database for both read and write sides.
- Failure behavior, expanded: If Quay's write to this table fails, the order is not marked paid and the customer sees the same failure outcome as the authorise call that fed it (I-1's or I-5's failure behavior, since I-10's write follows a successful or failed authorisation, not an independent path); capture and refund calls from the order service (API contract) fail the same way. The order-history page keeps reading the old table shape unchanged from Quay's writes (AC-9); a schema change to this shape without the removal-date discipline in ADR-0002 is treated as a regression, not a feature, which is the reasoning behind R5 staying open and reviewed monthly, with any pull request touching that table's columns blocked in review until Grace Mbeki signs off.
- Backoff and retry policy: Standard database transaction semantics; no separate retry layer. Capture and refund calls from the order service use Quay's own API, so they carry that API's idempotency mechanism (Idempotency-Key header, 24 h window, N61), not a separate one for this row.
- Monitoring: Reporting migration off this shape is tracked as DEP-4, committed and needed by 2027-02-27, in progress at this register's date; the table shape itself is scheduled for removal 2027-03-31 (N65, ADR-0002). No separate runtime alert applies to this row: a failed write surfaces through I-1's or I-5's own alerts, and an unreviewed schema change is caught by the PR gate above, not a page.
- Counterparty contact: Grace Mbeki, Data Engineering Lead, for the read side; Bea Lindqvist for the write side.
- Contract or DPA reference: Internal; no external DPA.
- Change notice: Internal change process, tracked through DEP-4 and R5's monthly review.

### Integration I-11: Finance ERP export

- Purpose: Nightly export of reconciled settlement and refund data from the reconciliation service to the finance ERP, feeding the daily close.
- Data exchanged: Reconciled financial line items, no card data.
- Environments: Internal; no external sandbox distinction.
- Failure behavior, expanded: A failed export blocks the day's close the same way a missing settlement file does; DEP-3's dual-path reconciliation runbook, delivered 2026-07-08, covers both failure modes under one procedure.
- Backoff and retry policy: Export re-run is manual, initiated by finance operations per the runbook.
- Monitoring: Covered by the same reconciliation tolerance discipline as I-4, I-6 and I-8 (N35). [OPEN: no named export-failed alert or recipient for this row is recorded on the data sheet; owner Priya Raman, who owns the daily close this export feeds]
- Counterparty contact: Priya Raman, Head of Finance Operations.
- Contract or DPA reference: Internal; no external DPA.
- Change notice: Internal change process.

## 3. Failure drill

- If every outbound integration failed at once, the user could still: reach the storefront and app, browse and build a basket, and pay at the till on any kiosk (BR-004, N31); web and app card checkout is unavailable (customers see a provider-unavailable message, not a decline, per I-1's failure behavior), which is not a completed payment but is an honest outcome rather than a silent hang.
- The failure that hurts most is Kestrel as a counterparty (I-1 for web and app together with I-3 for kiosks; I-2 and I-4 also depend on it), because after the sunset it is the counterparty behind every card-authorisation surface; its mitigation is R4, accepted by name in D-022 (2026-08-24) alongside the kiosk fallback (N31), the peak change freeze (N64), a quarterly review next due 2027-01-31, and region failover within 60 minutes after sunset (N29).

The integration that actually failed inside this journey was I-6, Marlowe's settlement file, on 2026-06-15: not Kestrel, and not an authorisation path at all, but an inbound reconciliation file with no alert behind it. That gap between the register's worst-single-failure answer and the one HG-INC-14 recorded is deliberate to state, not to paper over: the failure drill answers "which failure would hurt the customer most", and Kestrel as a counterparty still holds that answer after the sunset; HG-INC-14 answers "which failure actually happened", and it was a file with no page behind it, closed by A2 to A4 rather than by anything in section 3.

## Exit gate

- [x] Every boundary line in the solution architecture one-pager has a register row. All eleven rows I-1 to I-11 in the system design's integrations list appear here.
- [x] Every row has a named owner on our side. Ten rows carry Bea Lindqvist; I-9 carries Saoirse Whelan and I-10 splits Grace Mbeki (read) from Bea Lindqvist (write).
- [x] Every SLA cites its source document, not a recollection. Kestrel and Marlowe cite their MSA and contract schedules (N26, N27); Tidewater states plainly that its 2021 contract carries no SLA clause (N28), which is itself a cited fact, not an omission.
- [x] Every detail block states failure behavior a user would recognize. "Shows a card-payments-unavailable message", "pay at the till within 10 seconds", "the file the finance close was late because of", not "the call fails".
- [ ] Retry policies name their idempotency mechanism. I-1 names the 24-hour idempotency window and the same-key retry (N61); I-2 names event-id dedupe on the status event; I-10's capture and refund calls inherit I-1's mechanism. I-4, I-6 and I-8 (the settlement files) name none, flagged [OPEN] against Bea Lindqvist rather than asserted; this box is not met.
- [x] Every integration with no contract or DPA reference has a risk register row. I-9, I-10 and I-11 are internal with no external DPA and carry no external counterparty risk row for that reason; every externally facing row without an SLA clause (I-7, I-8) points to its contract instead.
- [x] The worst-single-failure answer in section 3 is written and its mitigation linked. Kestrel as a counterparty is named, with R4 and D-022 as the mitigation; the drill also states, separately, which integration actually failed and why that is not a contradiction.

Reviewed at [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md), accepted 2026-04-10 with the wrapper-owner miss recorded in this register: at that date I-7's owner cell read "none; Tomasz Wierzbicki to name an owner by 2026-04-24 (R2)", so this exit gate's named-owner box was not met at Gate 3 and closed 2026-04-24 when Bea Lindqvist was named caretaker. Signed off by Bea Lindqvist, register owner, and Tomasz Wierzbicki, Engineering Lead, as the design owner accountable for the boundaries the register describes. See the [Harbourgate journey](harbourgate-journey.md) for how this register reached Gate 3 and stayed current through the drain. The rejected option, a routing layer over all three providers (ADR-0003), lost on operational risk: three settlement file formats, three decline vocabularies, three on-call surfaces and three contracts forever, for a routing flexibility that the 2019 cascade rule (BR-008) had shown produces double authorisations rather than approvals; that is why I-5 to I-8 are retired rather than kept.
