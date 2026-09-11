# Non-Functional Requirements: Palisade Detection and Response

Fills [templates/definition/nfr.md](../templates/definition/nfr.md). Everything here is invented for this standalone example: Palisade Security is a fictional detection-and-response vendor selling to regulated financial-services customers, the people are roles filled by invented names, and every number, date, name and identifier is ILLUSTRATIVE. There is no external Palisade journey or data sheet; the numbers here are internal to this file so they can be checked against each other and against the card this file bends. See the [examples index](README.md).

**Owner:** Farah Osei, product manager · **Date:** 2026-09-11 · **Status:** Draft, in review at Gate 2
**Parent PRD:** not filled for this example (ILLUSTRATIVE)

Relates to [cybersecurity-grc](../knowledge/domains/cybersecurity-grc.md). All regulatory statements below are as of 2026-09-11 and carry the instruction: confirm with counsel. This document is not legal advice.

## 1. Performance and latency

All figures ILLUSTRATIVE, agreed with the owner named in each row.

| Requirement | Target (number) or owner for the number | Measured how and where | Verified by |
|---|---|---|---|
| Detection pipeline: a raw event is enriched and available for triage within | 90 seconds at p95; owner: Priya Nandakumar, agreed 2026-09-08 | Event timestamp to enrichment timestamp in the pipeline consumer, sampled on the 24-hour window each release | Load test LT-04, artifact stored in the Gate 4 evidence bundle |
| Materiality-determination packet, US public-company customers, assembles and exports within | 4 business days of the customer's own materiality determination, to support their Form 8-K Item 1.05 filing clock. The determination itself is the customer's own obligation and runs on their timeline; the product cannot start it for them. Owner: Farah Osei, agreed 2026-09-09 | Timestamp from the customer-marked "materiality determined" event to the "packet exported" event, sampled on every confirmed incident, reviewed quarterly | Packet export test PE-11; each export carries a tamper-evident hash, verified in the audit log |
| NIS2 early-warning packet, EU essential-entity customers, assembles and exports within | 20 hours of an incident being confirmed in-product, deliberately 4 hours inside the customer's own 24-hour written deadline so the customer keeps the margin. Owner: Farah Osei, agreed 2026-09-09 | Same event pair as the Form 8-K row, this threshold set tighter | Packet export test PE-12 |
| DORA major-incident initial notification, EU financial-entity customers, assembles and exports within | Owner: Farah Osei, by 2026-10-09. The DORA Article 19 timeline in the sources this file has read is disputed between an hours-scale initial-notification window and a days-scale one, and the card names DORA's initial notification as four hours; this file does not assert which, and no number is set until counsel confirms the current text. This file is not legal advice | Once the number is agreed: same event pair as the two rows above, threshold set shorter than whatever counsel confirms | Blocked; cannot be verified until the target exists. Flagged, not hidden |

Every row in this section has a number or a named owner with a date for the number. The DORA row is the one held open, on purpose, because writing a wrong number there is worse than writing none.

## 2. Availability and reliability

All figures ILLUSTRATIVE.

| Requirement | Target or owner | Measured how | Verified by |
|---|---|---|---|
| Availability of the detection console and packet export surface | 99.9% monthly, ILLUSTRATIVE, agreed with Priya Nandakumar 2026-09-08 | Uptime monitor, monthly report routed to the reliability review | Gate 5 evidence bundle, monthly report |
| Recovery time after failure (RTO) | 60 minutes for the console; 120 minutes for the packet export service, because export is the clock-bearing surface and takes longer to bring up cleanly | Restore drill, run quarterly; first drill due 2026-11-20 | Restore drill report RD-02 |
| Tolerable data loss window (RPO) | 5 minutes for detection events; 0 minutes for a packet once the customer has exported it, meaning an exported packet must never be lost or altered | Backup cadence for detection events; immutability and hash check for exported packets | Backup audit BA-03; hash verification in the audit log |
| Degraded-mode behavior of the detection control | Fail open with a loud, customer-visible alarm, owner: Priya Nandakumar, agreed 2026-09-10 | Chaos drill, run at least once before Gate 5 | Chaos drill report CD-01. This row implements the card's question 8 directly: a control that fails open silently is a control that is absent when tested |

A 99.9% monthly target implies a maintenance and on-call answer. Palisade has neither a published maintenance window nor a named on-call rotation as of 2026-09-11. Both are routed to [operational-readiness-review.md](../templates/operate/operational-readiness-review.md) as an open item, owned by Priya Nandakumar, needed before Gate 5; this file records the gap rather than assuming it will resolve itself.

## 3. Scale and capacity

All figures ILLUSTRATIVE. Source of every estimate: Priya Nandakumar, engineering lead, estimate dated 2026-09-08.

| Dimension | Launch assumption | 12-month projection | Breaks at | Source of estimate |
|---|---|---|---|---|
| Monitored endpoints across all customers | 40,000, ILLUSTRATIVE | 150,000 | 210,000, where the current enrichment sharding runs out of partitions and event lag exceeds 90 seconds at p95 | Priya Nandakumar, 2026-09-08 |
| Detection events ingested per second, peak | 12,000 | 40,000 | 55,000, where the pipeline consumer's single-writer commit path is the bottleneck | Priya Nandakumar, 2026-09-08 |
| Confirmed incidents per month across all customers | 30 | 120 | Not a load limit at any projected figure; incidents are rare, the queue is not | Priya Nandakumar, 2026-09-08 |
| Exported packet storage | 2 GB a month | 18 GB a month | 1 TB a year, where the tamper-evident store's current retention-by-copy rather than retention-by-delete design has to change | Priya Nandakumar, 2026-09-08 |

The 40,000 to 150,000 to 210,000 progression is what the "breaks at" column forces out into the open now rather than during an incident. The 210,000 figure is the one to watch: it sits 60,000 endpoints above the 12-month projection, which is a comfortable gap, but it is reached by adding customers at the projected rate, not by a single account, so it is a fleet-wide ceiling rather than a per-account one.

## 4. Security and privacy

This section is where the card's framing is closest to a requirement: the detection-and-response product is itself an attack surface, privileged on every customer's network. The rows below treat that as a product commitment, not only an architecture concern. Detail belongs in a filled `security-architecture.md` for Palisade (not filled for this example); this table holds the product-level promises.

All figures ILLUSTRATIVE.

| Requirement | Target or owner | Verified by |
|---|---|---|
| Agent permissions model: the endpoint agent runs least-privilege | Named permission set agreed with each customer before deployment; the agent holds no write access to customer file systems, no local-admin right where a lower-privilege mode exists, and no standing network path except the outbound telemetry channel. Owner: Marcus Ihejirika, CISO | Least-privilege audit LP-01; permission review at each customer onboarding, artifact in the security architecture file |
| Signed updates | Every agent and collector update is cryptographically signed; the agent refuses an unsigned or mis-signed update. Owner: Marcus Ihejirika | Signing verification test SV-01, run on every release |
| Staged rollout rings with a kill switch | Updates move through rings: ring 0, internal; ring 1, two named design partners; ring 2, ten percent of fleet; ring 3, general. No ring promotion without a 24-hour soak and a clean error-rate check. A kill switch can halt any ring and, once promoted past a ring, roll back. Time to roll back a fully promoted update: owner: Priya Nandakumar, by 2026-11-06 | Rollout drill RO-01; kill-switch test KS-01 |
| Data residency | Customer telemetry, packets and any derived customer data stay in the region the customer contract names (EU or US at launch). No cross-region replication of customer content; metadata-only telemetry may transit for service operation, owner: Farah Osei, boundary confirmed with counsel because the metadata carve-out is where it goes wrong | Residency test RS-01; contract-to-configuration check at onboarding |
| Authentication and session policy | Customer users authenticate through SSO with MFA; Palisade staff access to a customer's environment is just-in-time, time-boxed and logged, owner: Marcus Ihejirika | SSO and JIT access test AU-01 |
| Authorization model (who can do what) | Role-based: an analyst reads and triages; a compliance lead assembles and exports packets; a customer admin manages users and integrations; no single role both triages and certifies a packet | Authorization matrix test AZ-01 |
| Data classes handled, and their handling rule | Customer security telemetry; customer-confidential incident records; limited personal data incidentally present in logs and packets. Classification lives in [data-model.md](../templates/architecture/data-model.md). Handling rule: telemetry is customer-confidential, packets are customer-confidential and immutable once exported, personal data is minimized at enrichment and retention-bounded per section 6 | Data-class review DC-01, run at Gate 4 |
| Encryption in transit and at rest | TLS 1.3 in transit; AES-256 at rest, key management owner: Marcus Ihejirika | Encryption test EN-01; key-management review, artifact in the security architecture file |
| Audit logging of sensitive actions | Every packet assemble, export, role change, agent permission change and JIT staff access is logged; audit records are retained 13 months, tamper-evident via hash chain. Owner: Marcus Ihejirika | Audit-log test AL-01; hash-chain verification in the log store |

No AI or machine-learning feature sits in this product at this scope, so the regulated overlay's AI trigger does not activate even though regulated data classes are handled here. If a future detection feature scores or classifies incidents with a model, that trigger flips, and this row is the note that says so rather than leaving the question to whoever next reads [STAGE-GATES.md](../os/STAGE-GATES.md).

Marcus Ihejirika is named by role as the CISO verifier for this section, and Farah Osei as the customer-facing compliance lead. The card's gatekeeper rows treat these as two of the four gatekeepers in this domain: the compliance lead speaks for what the auditor will accept, and the CISO speaks for blast radius.

## 5. Accessibility

All figures ILLUSTRATIVE.

| Requirement | Target or owner | Verified by |
|---|---|---|
| Conformance level | WCAG 2.2 AA for the console and packet export surfaces, owner: Priya Nandakumar, agreed 2026-09-09 | Accessibility audit AA-01, artifact due at Gate 4 |
| Keyboard-only operation of core flows | Yes for triage, packet assemble and packet export; no on the map view, where keyboard navigation is partial, owner: Priya Nandakumar, by 2026-11-06 | Keyboard test KB-01; map view carried as a known partial, not claimed as passing |
| Localization and language support | English at launch; revisit at 2027-03-31, driven by whether a second-locale customer asks | Locale review LR-01 |

The map view row is the one this section is honest about: a partial keyboard path is recorded as partial rather than rounded up, because the buyer here reads the artifact, not the claim.

## 6. Data retention

All figures ILLUSTRATIVE. Every data class in [data-model.md](../templates/architecture/data-model.md) is listed below.

| Data class | Retention period | Deletion behavior | Driven by (policy, regulation, choice) | Owner |
|---|---|---|---|---|
| Detection telemetry events | 90 days hot, 13 months cold | Automatic expiry at 13 months; customer can request earlier deletion and it completes within 30 days | Choice (cost vs investigation value), with the 13-month figure chosen to cover a plausible annual review cycle | Marcus Ihejirika |
| Confirmed incident records | 7 years | Soft-delete on customer request, hard-delete at 7 years; a legal-hold flag blocks deletion where the customer's own counsel has set one | Choice, aligned to common financial-services record-keeping practice; the customer's own regulator drives the 7-year figure, and this is a reasonable chosen default rather than a stated legal requirement | Marcus Ihejirika |
| Exported compliance packets | 7 years, immutable once exported | Never mutated; deletion only on customer request, with the hash-chain record retained | Choice, matching the 7-year incident record figure so the two lines up | Farah Osei |
| Audit logs of sensitive actions | 13 months | Automatic expiry at 13 months | Choice, aligned to the same 13-month figure as telemetry so one retention habit covers both | Marcus Ihejirika |
| Customer configuration and integration settings | Life of the contract plus 30 days | Hard-delete 30 days after contract end | Choice | Marcus Ihejirika |
| Personal data incidentally present in logs and packets | Minimized at enrichment; where present, the same retention as its containing class | Deletion follows the containing class; a subject access request is served within 30 days, owner: Farah Osei | Regulation: GDPR for EU customers, confirm which basis applies with counsel; this is a statement of intent, not legal advice | Farah Osei |

The "driven by" column separates the rows a regulator actually drives (personal data) from the rows where the number is a chosen default aligned to common practice (telemetry, incidents, packets, audit, settings). Writing the difference down is the point: a retention period read as a legal mandate when it is a convenience is a period nobody revisits.

## 7. Operability

All figures ILLUSTRATIVE.

| Requirement | Target or owner | Verified by |
|---|---|---|
| Observability: logs, metrics, traces for core flows | At launch: pipeline and console metrics, structured logs for packet assemble and export, and traces on the triage path. Detail in [observability.md](../templates/architecture/observability.md) | Observability review OB-01; runs at Gate 4 |
| Feature kill or rollback path | The update rollout kill switch (section 4) is the primary mechanism; a feature-flag kill path exists for the packet export and triage surfaces, time to disable: 15 minutes for a flag, owner: Priya Nandakumar, by 2026-11-06 | Kill-switch test KS-01; feature-flag drill FD-01 |
| Support handover | Runbook at the location named in the operational-readiness review; owner: Priya Nandakumar, by 2026-11-20 | Runbook review RB-01 |
| Customer-visible incident response (Palisade's own incidents) | The card's fourth requirement in this area: Palisade publishes its own coordinated vulnerability disclosure policy and its own incident response policy before launch, because customers will read Palisade's postmortem the way Palisade's customers read theirs. Owner: Marcus Ihejirika, policy published by 2026-12-04 | Policy publication record; referenced in [incident-postmortem.md](../templates/operate/incident-postmortem.md) as the customer-facing artifact |

The last row is the one this section would omit if it were written for a product that is not itself an attack surface. It is not omitted here.

## 8. Waivers

No waivers are recorded as of 2026-09-11. The DORA numeric target in section 1 is flagged open, not waived: a waiver would be a number declined by its owner, and no number has been proposed yet. If counsel confirms a figure this file disagrees with, that disagreement is recorded here rather than absorbed.

| Requirement waived | Waived by | Reason | Revisit date |
|---|---|---|---|
| None as of 2026-09-11 | Not applicable | Not applicable | Not applicable |

---

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every row has a number or a named owner and date for the number. The DORA initial-notification row (section 1) carries "owner: Farah Osei, by 2026-10-09" for the number, with the number itself held open on purpose rather than guessed.
- [x] No adjective survives without a measurement ("fast", "secure", "scalable" all resolved). Every number here is a rate, a percentile, a duration or a count; "tamper-evident" is resolved as a hash chain and a verification test, and "least-privilege" is resolved as a named permission set with an audit.
- [x] Unagreed numbers are labeled ILLUSTRATIVE. Every figure in sections 1 through 7 carries the label, and the one figure held open (DORA) is labeled as held open rather than as ILLUSTRATIVE, because a number held open is a different thing from a number assumed.
- [x] Every row names its verification artifact. Sections 1 to 7 each name a test, a drill, an audit or a review; the DORA row names its blocking status as the reason it has no artifact yet.
- [x] Scale table includes a "breaks at" estimate from engineering. Section 3's fourth column carries four of them, each sourced to Priya Nandakumar, dated 2026-09-08.
- [x] Retention table covers every data class in the data model. Section 6 lists six classes, matching [data-model.md](../templates/architecture/data-model.md) as of 2026-09-11.
- [x] All waivers are recorded here with a revisit date. Section 8 records none, and says why the DORA flag is a flag rather than a waiver.

Signed at Gate 2, 2026-09-11: Farah Osei, product manager and customer-facing compliance lead (per the card's gatekeeper row, she carries the customer's own clock into the requirement); with Marcus Ihejirika, CISO (the card's second named verifier, speaking to blast radius and least-privilege). The DORA numeric target in section 1 is signed off as an open item, not as a requirement, and its resolution is owned by Farah Osei with a due date of 2026-10-09.
