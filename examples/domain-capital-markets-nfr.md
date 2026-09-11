# Non-Functional Requirements: Pre-Trade Risk Gateway, Tallyhouse Markets

Fills [templates/definition/nfr.md](../templates/definition/nfr.md). Everything here is invented: Tallyhouse Markets is a fictional trading-venue technology vendor, the Alderbank Vale Exchange is a fictional small regional equities exchange, the people are roles filled by invented names, and every number, date and identifier is ILLUSTRATIVE, drawn from the fictional context block below rather than from any real venue, vendor or market. See the [examples index](README.md).

**Owner:** Sunniva Aas, head of product, Tallyhouse Markets · **Date:** 2026-09-11 · **Status:** In review at Gate 2, presented to the Alderbank Vale Exchange membership committee on ILLUSTRATIVE 2026-09-25
**Parent PRD:** not filled for this example (ILLUSTRATIVE)
**Domain:** [Capital markets](../knowledge/domains/capital-markets.md)

## Context (ILLUSTRATIVE)

Tallyhouse Markets is a fictional trading-venue technology vendor. Its product in this document is the pre-trade risk gateway (PTRG) for the Alderbank Vale Exchange, a fictional small regional equities exchange with ILLUSTRATIVE 22 member firms. The gateway sits between each member firm's order-entry session and the exchange's matching engine: every order is screened against that member's credit, size and price-collar limits before it is allowed to reach the match, and the gateway holds the kill switch for each member session.

The people named in this document are fictional:

- Sunniva Aas, head of product, Tallyhouse Markets (owner of this NFR set).
- D. Okafor, head of trading risk, Alderbank Vale Exchange (owns the kill-switch drill).
- Ingrid Halvorsen, chief regulatory officer, Alderbank Vale Exchange (verifier, by role).
- Marwan Aziz, member-surveillance lead, Alderbank Vale Exchange (verifier, by role).
- The engineering contact for capacity estimates is signed by role as the Tallyhouse gateway engineering lead; the person is not named here.

Regulatory statements below are dated as of 2026-09-11 and are not legal advice. Confirm every regulatory statement with counsel before relying on it.

## 1. Performance and latency

Every row is measured by replaying the prior trading day's full order flow through the gateway test harness, which runs the same binary and the same exchange connection configuration as production, on the same hardware class, with the same co-located session profile. Replay is the measurement method named by D. Okafor at the 2026-09-04 requirements review, because a synthetic benchmark with modelled order sizes would not answer the question the exchange's membership agreement actually asks: how much latency does this add to the order flow the exchange has already seen.

| Requirement | Target (number) or owner for the number | Measured how and where | Verified by |
|---|---|---|---|
| Market-access pre-trade risk control: every order is screened before it is sent (Rules 15c3-5 analogue) | 100% of orders screened pre-send; no order reaches the matching engine without a screening decision (target, ILLUSTRATIVE N-KS1) | Replay of the prior trading day's full order flow through the gateway test harness, screening decision stamped on every order | Kill-switch drill log and replay report, signed by D. Okafor, ILLUSTRATIVE dated 2026-10-02 |
| Screening adds latency to the order path, at the 99th percentile | No more than 250 microseconds added at p99 (target, ILLUSTRATIVE N-KS1) | Same replay, latency histogram captured per order at the gateway egress interface | Replay report, verified by Sunniva Aas, ILLUSTRATIVE dated 2026-10-02 |
| Screening adds latency at the median | No more than 40 microseconds at p50 (target, ILLUSTRATIVE N-KS2) | Same replay, latency histogram | Replay report, verified by Sunniva Aas, ILLUSTRATIVE dated 2026-10-02 |
| Failure of the screening path itself only fails closed | A screening error rejects the order, never passes it; measured as a counter, not a latency number | Fault injection during replay: 100% of injections end in a reject, ILLUSTRATIVE N-KS3 | Fault-injection log, verified by Marwan Aziz, ILLUSTRATIVE dated 2026-10-09 |
| Daily risk-limit recalculation completes before the pre-open session | Owner: Tallyhouse gateway engineering lead, by 2026-09-25, to produce the number | Batch job timing against the exchange's published pre-open schedule | Batch-run log, verified by D. Okafor |
| End-to-end client latency budget, including the client's distance from the venue | Owner: D. Okafor, by 2026-10-16, using the exchange's own colocation measurements, because the gateway's own number is not the number the member experiences | Member-side measurement, outside the gateway's instrumentation | Member latency report, to be agreed with the membership committee |
| Replay corpus coverage: the share of the prior day's order messages the harness processes without an unhandled message type | Owner: Tallyhouse gateway engineering lead, by 2026-09-25 | Replay harness coverage report | Replay report |

## 2. Availability and reliability

The availability target below implies a maintenance and on-call answer. The exchange's trading calendar and session hours are set by the exchange, not by Tallyhouse, and the gateway has no maintenance window inside a trading session. The operational-readiness answer for the gateway is routed separately, to [templates/operate/operational-readiness-review.md](../templates/operate/operational-readiness-review.md), and is not settled in this document.

| Requirement | Target or owner | Measured how | Verified by |
|---|---|---|---|
| Availability of the pre-trade screening path during trading hours | 99.99% per calendar month ILLUSTRATIVE (N-KS4); downtime minutes are counted only inside the exchange's published session hours | Uptime monitor on the screening path plus the exchange session clock | Monthly availability report, verified by the chief regulatory officer, Ingrid Halvorsen |
| Recovery time after failure (RTO), gateway process | 60 seconds (ILLUSTRATIVE N-KS5), measured as time from process failure to the first order accepted on the recovered process | Restore drill, run against a pre-production venue connection | Restore drill log, verified by the chief regulatory officer |
| Tolerable data loss window (RPO), risk-limit state | 0 seconds for the live limit state; the state is reconstructed from the order and audit log, not from a periodic snapshot, and reconstruction time to first order accepted is part of the 60-second RTO | Backup and reconstruction cadence of the order and audit log | Reconstruction drill, verified by Marwan Aziz |
| Kill switch: time from trigger to cancellation of a member's open orders | No more than 2 seconds at p99 (ILLUSTRATIVE N-KS6), every time, under a replayed peak-load order flow | Kill-switch drill: trigger is pulled on a live member session with the prior day's peak message rate replayed, and the cancellation receipt from the matching engine timestamps the end | Kill-switch drill log, signed by D. Okafor, ILLUSTRATIVE dated 2026-10-02 |
| Kill switch: authority to pull | Owner: Ingrid Halvorsen, by 2026-09-25, to publish the named roles and the escalation path; the mechanism is built, the authority list is a governance artifact | Written authority list, tested in the next drill by having a second named role pull it | Authority list, verified by the chief regulatory officer |
| Kill switch: behaviour on a partial pull (one member session of several) | Owner: D. Okafor, by 2026-09-25, to state whether a partial pull is permitted, because the exchange's membership agreement decides this, not the gateway team | Drill of the partial-pull path | Drill log, verified by D. Okafor |
| Availability of the surveillance and audit feed the gateway publishes | Owner: Marwan Aziz, by 2026-10-16, to state the tolerance, because the surveillance feed is an input the surveillance team depends on rather than a customer-facing surface | Monitor on the feed plus a daily completeness reconciliation | Feed reconciliation report, verified by Marwan Aziz |

## 3. Scale and capacity

All rows are ILLUSTRATIVE. The launch assumption is derived from the exchange's own prior-month peak message rate, which the exchange records as 1,200 orders per second across all member sessions, ILLUSTRATIVE (N-KS7). Twelve-month projection is the launch figure multiplied by 1.5, ILLUSTRATIVE (N-KS8). "Breaks at" is the figure the Tallyhouse gateway engineering lead gave at the 2026-09-04 requirements review, and every row's breaks-at figure is that row's launch assumption multiplied to a stated multiple, not an independently tested number, because the gateway has not yet run beyond 1.3 times the exchange's recorded peak. That gap is recorded here rather than smoothed over: the harness is the instrument, and it has only been pushed to 1,560 orders per second, ILLUSTRATIVE (N-KS9), which is the "breaks at" figure for the screening path row and is 1.3 times the launch assumption.

| Dimension | Launch assumption | 12-month projection | Breaks at | Source of estimate |
|---|---|---|---|---|
| Orders per second, all member sessions | 1,200 orders/s ILLUSTRATIVE (N-KS7) | 1,800 orders/s (launch x 1.5, ILLUSTRATIVE N-KS8) | 1,560 orders/s, the highest the harness has run (1.3 times launch, ILLUSTRATIVE N-KS9); the measured ceiling, not a projection | Exchange prior-month peak, recorded by the exchange; ceiling from the 2026-09-04 engineering review |
| Concurrent member order-entry sessions | 22 member firms, with ILLUSTRATIVE 3 sessions each, so 66 concurrent sessions (N-KS10) | 99 concurrent sessions (launch x 1.5, same rule) | 86 concurrent sessions, 1.3 times launch, same rule (ILLUSTRATIVE N-KS11) | Exchange membership count and session policy |
| Cancel and replace messages per second | 4,200 cancel/replace per second ILLUSTRATIVE (N-KS12), which is 3.5 times the order rate, the exchange's recorded ratio | 6,300 per second (launch x 1.5, same rule) | 5,460 per second, 1.3 times launch, same rule (ILLUSTRATIVE N-KS13) | Exchange recorded message mix, prior month |
| Order and audit records written per trading day | 340,000,000 records per day ILLUSTRATIVE (N-KS14), computed as 1,200 orders/s plus 4,200 cancel/replace/s = 5,400 messages/s, over a 6.25-hour session = 22,500 seconds; 5,400 x 22,500 = 121,500,000 messages per day, and with the ILLUSTRATIVE average record multiplier of 2.8 bytes-of-record variants per message, 121,500,000 x 2.8 = 340,200,000, rounded to 340,000,000 | 510,000,000 records per day (launch x 1.5, same rule) | Not yet measured; owner: Tallyhouse gateway engineering lead, by 2026-10-16, to run the harness to the storage-write ceiling, because this row's "breaks at" is the number nobody has | Arithmetic shown above; message mix from the exchange |
| Risk-limit records held live in memory | 22 members x an ILLUSTRATIVE 40,000 limit records each = 880,000 live records (N-KS15) | 1,320,000 live records (launch x 1.5, same rule) | 2,300,000 live records, being the number the gateway's memory budget supports at the ILLUSTRATIVE measured 2.6 times headroom, which the engineering lead states is not the same as a tested ceiling (N-KS16) | Engineering review, 2026-09-04 |

## 4. Security and privacy

The gateway handles order data, which is confidential member and client order information, and it handles no payment card data and no end-client personal data beyond the identifiers an exchange order carries. It contains no AI or machine-learning feature, so the regulated overlay in [../os/STAGE-GATES.md](../os/STAGE-GATES.md) is not activated by a model in the product; the regulated data class here is order data under the exchange's member confidentiality and market-abuse rules, and the handling rules below are the product-level commitments, with the technical detail in [templates/architecture/security-architecture.md](../templates/architecture/security-architecture.md).

| Requirement | Target or owner | Verified by |
|---|---|---|
| Authentication and session policy | Every member order-entry session authenticates with a member-issued credential and a gateway-issued session key, no shared credentials, and a session key expires at end of trading day; owner: the Tallyhouse gateway engineering lead, by 2026-09-25, to specify the credential rotation interval | Session-authentication test at the pre-production venue connection, verified by Marwan Aziz |
| Authorization model (who can do what) | A member session may see and act on its own orders and limits only; a gateway operator role may read all sessions and may pull a kill switch; the gateway operator role cannot submit orders; owner: Ingrid Halvorsen, by 2026-10-02, to confirm the operator-role split against the exchange's membership agreement | Authorization test matrix, verified by the chief regulatory officer |
| Data classes handled, and their handling rule | Order data (member-confidential, held and transmitted under the member's own confidentiality obligations), audit records (retained per section 6), and operational telemetry (aggregated, no order contents); no payment card data; no end-client special-category data; the full classification lives in [templates/architecture/data-model.md](../templates/architecture/data-model.md) | Data-class review against the data model, verified by Marwan Aziz |
| Encryption in transit and at rest | In transit: member sessions over mutually authenticated TLS 1.3 or the exchange's own session encryption, whichever the exchange requires; at rest: audit records encrypted, with the key custody question open and owned by Ingrid Halvorsen, by 2026-10-16 | Configuration review and key-custody statement, verified by the chief regulatory officer |
| Audit logging of sensitive actions | Every screening decision, every limit change and every kill-switch pull is logged with actor, timestamp and reason; retention as section 6; the audit record is the artifact the exchange's surveillance function reads | Log-completeness reconciliation across the replay corpus, verified by Marwan Aziz |
| Operator access to order content | Owner: Ingrid Halvorsen, by 2026-10-16, to state whether gateway operators may read order contents in incident response, or only metadata, because the member confidentiality rule is the exchange's to state | Written access rule plus an access test, verified by the chief regulatory officer |

## 5. Accessibility

The gateway has two surfaces: a member-facing order-entry session (the member's own software, whose accessibility is the member's responsibility, not Tallyhouse's) and a Tallyhouse-operated gateway console that a small number of named operators use. The console is the surface this table covers. There is no public-facing surface and no end-investor surface.

| Requirement | Target or owner | Verified by |
|---|---|---|
| Conformance level, gateway operator console | WCAG 2.2 AA, ILLUSTRATIVE target (N-KS17); owner: Sunniva Aas, by 2026-11-06, to confirm the level with the exchange's procurement, since the exchange rather than Tallyhouse sets the procurement bar | Audit artifact on the console, a WCAG 2.2 AA audit report |
| Keyboard-only operation of core flows | Yes for the two core console flows, pull the kill switch and read the screening decision for an order; owner: the Tallyhouse gateway engineering lead, by 2026-10-09, to test both flows with keyboard only | Keyboard-only test log, verified by Sunniva Aas |
| Localization and language support | Single language, English, revisit at 2027-03-31; the exchange operates in one language and no member has asked for a second | Statement of no localization, reviewed at the 2027-03-31 review |

## 6. Data retention

All rows are ILLUSTRATIVE. Retention periods below are stated against real rules as of 2026-09-11; confirm with counsel before relying on them.

The two rules that drive the order-record and clock rows: MiFID II's regulatory technical standard on clock synchronisation is Commission Delegated Regulation (EU) 2017/574 (RTS 25), which sets the clock-synchronisation and timestamping obligations for trading venues and investment firms, with the exact accuracy tier depending on the venue's type and on the activity, and its application in a non-EU venue is a question for the exchange's own regulator. The US record-retention rule for broker-dealers is SEC Rule 17a-4 under the Securities Exchange Act of 1934, which sets retention periods for specified records and the conditions for electronic storage; it applies to broker-dealers subject to US jurisdiction, and whether it binds the exchange's members here is a question for counsel. Neither of those statements is legal advice.

| Data class | Retention period | Deletion behavior | Driven by (policy, regulation, choice) | Owner |
|---|---|---|---|---|
| Order messages as received from a member session | 5 years from the order's date, ILLUSTRATIVE period (N-KS18) pending counsel's confirmation of the period the exchange's own regulator requires, since SEC Rule 17a-4's period and MiFID II's are separately stated rules and this venue is neither US nor EU by default | Not deleted before the period; on expiry, archived to offline storage and excluded from live queries, not destroyed on a rolling basis | Regulation (to be confirmed with counsel) plus the exchange's own member agreement | Ingrid Halvorsen |
| Screening decisions (accept, reject and the reason) | 5 years from the decision's date, ILLUSTRATIVE period (N-KS18) | Same archive-and-exclude behavior | Regulation (to be confirmed with counsel) | Ingrid Halvorsen |
| Kill-switch activation records (who pulled it, when, which sessions) | 5 years from the activation's date, ILLUSTRATIVE period (N-KS18) | Same archive-and-exclude behavior | Regulation (to be confirmed with counsel) plus choice, because the drill log is also a product artifact | D. Okafor |
| Risk-limit state and limit-change records | 5 years from the change's date, ILLUSTRATIVE period (N-KS18) | Same archive-and-exclude behavior, keeping the change history readable for the whole period | Regulation (to be confirmed with counsel) | Ingrid Halvorsen |
| Clock-synchronization records: the gateway's timed offsets against its traceable reference clock | 5 years from the record's date, ILLUSTRATIVE period (N-KS18), because the timestamp's accuracy claim is only defensible if the offset record survives as long as the order | Same archive-and-exclude behavior | Regulation: MiFID II RTS 25 (Commission Delegated Regulation (EU) 2017/574) as the model for the obligation, with the venue's own regulator's rule to be confirmed with counsel | Ingrid Halvorsen |
| Operational telemetry (counters, latency histograms, no order contents) | 90 days rolling, ILLUSTRATIVE period (N-KS19), a choice not a regulation, because the telemetry is not a record of a trading event | Deleted on a rolling basis after 90 days | Choice, with the retention decision made jointly by Sunniva Aas and D. Okafor | Sunniva Aas |
| Support and incident tickets naming an order | 5 years from the ticket's close, ILLUSTRATIVE period (N-KS18), because a ticket naming an order is an order-derived record | Same archive-and-exclude behavior | Regulation (to be confirmed with counsel) plus choice | Sunniva Aas |

Clock synchronisation is a row in the table above because under RTS 25 the timestamp accuracy claim and the order record stand or fall together; the gateway's clock-synchronisation requirement is to remain within the tolerance the exchange's own regulator sets, and the offset record is the evidence. The exact tolerance figure is not stated here because it is tier-dependent and counsel has not yet confirmed which tier applies to this venue as of 2026-09-11.

## 7. Operability

| Requirement | Target or owner | Verified by |
|---|---|---|
| Observability: logs, metrics, traces for core flows | At launch, the gateway publishes: a screening-decision record per order, a latency histogram per session, a message-rate counter per session, kill-switch state, and clock-offset records; the surveillance feed is the same screening-decision stream and is treated as an observability surface with a regulator as stakeholder, per the domain card; detail in [templates/architecture/observability.md](../templates/architecture/observability.md) | Observability review against the listed signals, verified by Marwan Aziz, ILLUSTRATIVE dated 2026-10-09 |
| Feature kill or rollback path | Kill switch per member session, pull time 2 seconds at p99 per section 2; gateway release rollback on the pre-production venue connection, timed as a measured number, owner: the Tallyhouse gateway engineering lead, by 2026-10-02, because a bad deploy at a matching engine is the reason this row exists rather than tests alone | Rollback rehearsal log against the pre-production venue connection, verified by the chief regulatory officer |
| Support handover | Runbook location or owner: Sunniva Aas, by 2026-10-16, to name the runbook and the on-call rotation, since a gateway with no in-session maintenance window needs a stated answer before it goes live | Runbook plus the on-call roster, verified by Sunniva Aas |
| Alerting threshold and owner on the screening path | Owner: D. Okafor, by 2026-10-02, to set the threshold at which an operator is paged and who is paged, because the exchange's trading hours decide what counts as urgent | Alerting configuration review, verified by D. Okafor |
| Incident escalation path for a kill-switch pull | Owner: Ingrid Halvorsen, by 2026-09-25, to name the roles notified on a pull and the notification order | Written escalation path, tested in the next drill | Escalation test log, verified by the chief regulatory officer |

## 8. Waivers

| Requirement waived | Waived by | Reason | Revisit date |
|---|---|---|---|
| The keyboard-only operation test on the gateway operator console (section 5, row 2) | Sunniva Aas, owner of the accessibility row, in writing on 2026-09-11 | The console's keyboard-only path exists but the test was not run before the membership committee session, because the console changed after the test was scheduled; the customer-facing gateway has no accessibility surface, so the exposure is confined to a small number of named operators | Revisit 2026-11-20, one week before the 2026-11-27 committee review, with the result reported to Ingrid Halvorsen |

No other rows are waived as of 2026-09-11.

---

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every row has a number or a named owner and date for the number. Rows carrying the numbers N-KS1 to N-KS19 are ILLUSTRATIVE; the remaining rows name an owner and a date by which the number is produced, and none are blank.
- [x] No adjective survives without a measurement ("fast", "secure", "scalable" all resolved). "Fast" is the 250-microsecond p99 row and the 40-microsecond p50 row in section 1. "Secure" is the authentication, authorization and encryption rows in section 4. "Scalable" is the launch, projection and breaks-at columns in section 3.
- [x] Unagreed numbers are labeled ILLUSTRATIVE. Every number in this document carries the ILLUSTRATIVE label with the identifier it belongs to, and the regulatory statements carry the as-of date 2026-09-11 and the direction to confirm with counsel.
- [x] Every row names its verification artifact. The artifacts are the replay report, the kill-switch drill log, the fault-injection log, the reconstruction drill, the feed reconciliation report, the authorization test matrix, the access test, the WCAG 2.2 AA audit report, the keyboard-only test log, the observability review, the rollback rehearsal log, the runbook and on-call roster, the alerting configuration review and the escalation test log, each with the role that verifies it.
- [x] Scale table includes a "breaks at" estimate from engineering. Four of the five rows carry a breaks-at figure derived from the engineering review of 2026-09-04 at the stated multiple of 1.3 times launch, and the fifth row (order and audit records per trading day) carries an owner and a date rather than a guessed number, because the engineering lead's measured ceiling does not cover the storage path.
- [x] Retention table covers every data class in the data model. The data classes in [templates/architecture/data-model.md](../templates/architecture/data-model.md) are order data, screening decisions, kill-switch records, risk-limit state, audit records, clock-offset records and operational telemetry; the retention table covers all of those, with support tickets naming an order added as a derived record class.
- [x] All waivers are recorded here with a revisit date. One waiver, the console keyboard-only test, waived by Sunniva Aas on 2026-09-11, revisit 2026-11-20.

### Exit-gate walk

Walked on 2026-09-11 by Sunniva Aas, head of product, Tallyhouse Markets, in review with Ingrid Halvorsen, chief regulatory officer, Alderbank Vale Exchange, and Marwan Aziz, member-surveillance lead, Alderbank Vale Exchange. Each box above was checked against the row or rows that carry it, named in the box, rather than against the document as a whole.

Three things are open and are stated here rather than left to the reader. First, the end-to-end client latency budget in section 1 is not yet a number, because it is the exchange's measurement to make at member sites rather than the gateway's to make at its own egress, and D. Okafor owns it by 2026-10-16. Second, the regulatory retention periods in section 6 and the clock-synchronisation accuracy tier are stated against real rules as of 2026-09-11 and marked for confirmation with counsel; none of the regulatory statements in this document is legal advice, and the venue's own regulator decides which rule binds it. Where MiFID II and SEC Rule 17a-4 are named, they are named as the rules that shape the obligation, and whether either binds this venue or its members is for counsel, not for this document, to say. Third, one waiver is live: the console keyboard-only test, waived by Sunniva Aas on 2026-09-11 with a revisit date of 2026-11-20, at which point the result goes to Ingrid Halvorsen before the committee review on 2026-11-27.

The verifiers on this document are the exchange's chief regulatory officer and the exchange's member-surveillance lead, by role and not by name, because the point of the verification is that it is the exchange that accepts the risk picture, not the vendor that produces it.

Signed at the exit-gate walk, 2026-09-11: Sunniva Aas, head of product, Tallyhouse Markets (owner); Ingrid Halvorsen, chief regulatory officer, Alderbank Vale Exchange (verifier, by role); Marwan Aziz, member-surveillance lead, Alderbank Vale Exchange (verifier, by role); D. Okafor, head of trading risk, Alderbank Vale Exchange, named for the kill-switch drill log and the end-to-end latency budget, with the drill log itself due ILLUSTRATIVE 2026-10-02.
