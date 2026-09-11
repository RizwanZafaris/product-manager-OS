# Non-Functional Requirements: Fennwick Mobile Core Network Services

Fills [templates/definition/nfr.md](../templates/definition/nfr.md). Everything here is invented: Fennwick Mobile is a fictional MVNO running on a host network operator, the people are roles filled by invented names, and every number, name and date is ILLUSTRATIVE. See the [examples index](README.md).

**Owner:** Elias Thorne, Principal Product Manager · **Date:** 2026-10-24 · **Status:** Approved at Gate 2
**Parent PRD:** `prd.md` (the product workspace's own PRD; not tracked in this repository)

## 1. Performance and latency

| Requirement | Target (number) or owner for the number | Measured how and where | Verified by |
|---|---|---|---|
| Mobile number port-out completion time, donor confirms | 95% within 1 working day of donor confirmation, per PTA's portability determination (verify the current threshold before relying) | Portability gateway timestamp, from donor confirmation to first successful call on the recipient network, not from the customer's original request | Weekly cross-check against the regulator's own portability dashboard; owner: Ayesha Noor, Regulatory Affairs Lead |
| Lawful-intercept fulfilment time | 100% of valid requests actioned within the statutory window; owner: Ayesha Noor, baseline due 2026 Q4 | Intercept-request log matched to the statutory clock's start, not to internal ticket-open time | Quarterly attestation to the licensing regulator |
| Emergency-call setup with handset location (Advanced Mobile Location) | 98% of emergency calls transmit AML payload within 3 seconds of call answer | Network element logs at MSC/GMSC, correlated with PSAP receipt logs | Load test report from QA, signed off by engineering lead |

## 2. Availability and reliability

| Requirement | Target or owner | Measured how | Verified by |
|---|---|---|---|
| Availability of Voice over LTE (VoLTE) core services (dependent on Host Operator X) | 99.9% monthly ILLUSTRATIVE | Uptime monitor on IMS core, excluding planned maintenance windows agreed with Host Operator X | Monthly SLA report from Host Operator X, audited by internal SRE team |
| Recovery time after failure (RTO) for billing mediation system | 4 hours ILLUSTRATIVE | Restore drill performed quarterly in disaster recovery region | Drill report signed by Head of Infrastructure |
| Tolerable data loss window (RPO) for subscriber profile database | 15 minutes ILLUSTRATIVE | Backup cadence monitoring and transaction log replay tests | Automated alerting on backup lag exceeding threshold |
| Emergency-call availability (voice path) | 99.99% ILLUSTRATIVE, dependent on Host Operator X radio access network | End-to-end synthetic call attempts to emergency numbers every minute from distributed probes | Regulatory outage notification filed if availability drops below target for >1 hour |

<!-- An availability target implies a maintenance and on-call answer; if none exists, say so here and route it to ../operate/operational-readiness-review.md. -->
Maintenance windows are coordinated with Host Operator X via their wholesale portal. On-call rotation is managed by the Network Operations Center (NOC); details in [operational-readiness-review.md](../templates/operate/operational-readiness-review.md).

## 3. Scale and capacity

| Dimension | Launch assumption | 12-month projection | Breaks at | Source of estimate |
|---|---|---|---|---|
| Active SIM subscribers | 50,000 ILLUSTRATIVE | 250,000 ILLUSTRATIVE | 300,000 subscribers without adding a second HSS node | Capacity plan v1.2, reviewed by CTO |
| Call Detail Records (CDRs) generated per day | 2 million ILLUSTRATIVE | 10 million ILLUSTRATIVE | 15 million/day exceeds current Kafka topic partition count | Engineering load test, Q3 2026 |
| Interconnect traffic volume (minutes/month) | 5 million ILLUSTRATIVE | 25 million ILLUSTRATIVE | Depends entirely on Host Operator X trunk capacity; no internal break point defined yet | Commercial agreement with Host Operator X, Section 4.2 |

<!-- "Breaks at" forces the honest conversation with engineering now instead of during the incident. -->

## 4. Security and privacy

| Requirement | Target or owner | Verified by |
|---|---|---|
| Authentication and session policy | Mutual TLS between all core network elements; API keys rotated every 90 days for partner integrations | Penetration test report, annual review by InfoSec |
| Authorization model (who can do what) | Role-based access control (RBAC) enforced at the Mediation Platform; only Compliance Officers can trigger lawful intercept | Audit log review, quarterly compliance check |
| Data classes handled, and their handling rule | Call Detail Records (CDRs), Location Data, Subscriber Identity (IMSI/MSISDN). All classified as High Sensitivity PII under UK GDPR. Handling rules in [data-model.md](../templates/architecture/data-model.md) | Data Protection Impact Assessment (DPIA) sign-off |
| Encryption in transit and at rest | TLS 1.3 for all external interfaces; AES-256 for stored CDRs and backups | Configuration audit script run nightly |
| Audit logging of sensitive actions | All lawful-intercept activations, deactivations, and data exports logged immutably for 7 years | Log integrity verification tool, checked monthly |

<!-- If a regulator governs any data class here and the product contains an AI or machine-learning feature, the regulated overlay applies: see ../../os/STAGE-GATES.md for the rule and ../../modules/regulated/README.md for the module. A regulated data class with no model in the product does not activate it. Security architecture detail belongs in ../architecture/security-architecture.md; this table holds the product-level commitments. -->
Note: Fennwick Mobile currently has no AI/ML features in the core network stack. The regulated overlay is active due to the presence of regulated data classes (CDRs, Location) governed by the Investigatory Powers Act 2016 and UK GDPR.

## 5. Accessibility

| Requirement | Target or owner | Verified by |
|---|---|---|
| Conformance level | WCAG 2.2 AA for the self-care web portal and mobile app | External accessibility audit, scheduled Q1 2027 |
| Keyboard-only operation of core flows | Yes, for account management and bill payment flows on web | Automated axe-core scan in CI pipeline |
| Localization and language support | English only at launch. Revisit for Welsh and Urdu at 2027-06-01 based on subscriber demographic shifts | Market analysis report from Growth Team |

<!-- A buyer or agency asking for a VPAT/ACR wants the Accessibility Conformance Report per Section508.gov; that is a compliance-team output built from this table's audit artifact, not a template here. The market and locale list that drives the localization row lives in the discovery document's target market fields: ../discovery/discovery-document.md. -->

## 6. Data retention

| Data class | Retention period | Deletion behavior | Driven by (policy, regulation, choice) | Owner |
|---|---|---|---|---|
| Call Detail Records (CDRs) | 6 months ILLUSTRATIVE | Hard delete after 6 months unless subject to a live Legal Hold | Billing and dispute-management period under PECR 2003 regulation 7 and UK GDPR Article 6(1)(b)/(c) (contract necessity and accounting obligations); not a retention notice under the Investigatory Powers Act 2016, Section 87, which is a separate instrument the Secretary of State issues for investigatory purposes, not a basis Fennwick sets its own billing retention on (confirm with counsel) | Ayesha Noor, Regulatory Affairs Lead |
| Location Data (Cell ID) | 24 hours ILLUSTRATIVE | Overwritten automatically by next ping | Technical constraint of HLR/HSS update cycle; privacy-by-design choice | Elias Thorne, Product Manager |
| Customer Support Chat Logs | 2 years ILLUSTRATIVE | Anonymized user IDs retained, text deleted | Internal Policy FP-04; used for training support agents | Sarah Jenkins, Head of CX |
| Lawful Intercept Metadata | Duration of warrant + 1 year ILLUSTRATIVE | Secure destruction certificate issued to court | Court order requirements | Ayesha Noor, Regulatory Affairs Lead |

## 7. Operability

| Requirement | Target or owner | Verified by |
|---|---|---|
| Observability: logs, metrics, traces for core flows | Centralized ELK stack for application logs; Prometheus/Grafana for infrastructure metrics. Tracing limited to HTTP APIs, not SIP/RTP streams at launch. Detail in [observability.md](../templates/architecture/observability.md) | Dashboard review at operational readiness check |
| Feature kill or rollback path | Dynamic configuration flags allow disabling non-regulatory features (e.g., new USSD menus) in <5 minutes. Regulatory features cannot be killed | Chaos engineering drill, simulated flag flip |
| Support handover | Runbooks located in Confluence space "Fennwick Ops". Updated weekly. | Spot check by NOC manager |

## 8. Waivers

<!-- A target can be waived only by its owner, in writing, with a revisit date. Waivers hide here rather than in meeting minutes. -->

| Requirement waived | Waived by | Reason | Revisit date |
|---|---|---|---|
| None | | | |

---

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every row has a number or a named owner and date for the number
- [x] No adjective survives without a measurement ("fast", "secure", "scalable" all resolved)
- [x] Unagreed numbers are labeled ILLUSTRATIVE
- [x] Every row names its verification artifact
- [x] Scale table includes a "breaks at" estimate from engineering
- [x] Retention table covers every data class in the data model
- [x] All waivers are recorded here with a revisit date

Signed: Elias Thorne, Principal Product Manager, 2026-10-24
