# NFR: Northbank Digital Custody and Withdrawal Platform

Fills [templates/definition/nfr.md](../templates/definition/nfr.md). Everything here is invented for this standalone example: Northbank Digital is a fictional retail crypto exchange, Priya Anand its only fictional product manager, and every number, name and date is ILLUSTRATIVE, not drawn from any real exchange or market. There is no external Northbank journey or data sheet. See the [examples index](README.md).

**Owner:** Priya Anand · **Date:** 2026-09-11 · **Status:** Draft
**Parent PRD:** [prd.md](../knowledge/domains/crypto-digital-assets.md)

## 1. Performance and latency

| Requirement | Target (number) or owner for the number | Measured how and where | Verified by |
|---|---|---|---|
| Standard withdrawal confirmation completes in | 95% of withdrawals confirmed on-chain within 4 hours; anything held past 24 hours auto-escalates to a named compliance reviewer instead of sitting in the queue | Withdrawal-request timestamp to on-chain broadcast timestamp, per request | Withdrawal-latency dashboard, owner Head of Treasury |
| Batch reconciliation job completes in | Owner: Jai Kaur, Head of Treasury, by 2026-10-01 | Internal batch monitor | Reconciliation log |

## 2. Availability and reliability

| Requirement | Target or owner | Measured how | Verified by |
|---|---|---|---|
| Availability of customer-facing trading surface | 99.9% monthly ILLUSTRATIVE | Uptime monitor | SLA report |
| Recovery time after failure (RTO) | 30 minutes ILLUSTRATIVE | Restore drill | DR test report |
| Tolerable data loss window (RPO) | 5 minutes ILLUSTRATIVE | Backup cadence | Backup verification log |

An availability target implies a maintenance and on-call answer; if none exists, say so here and route it to ../operate/operational-readiness-review.md.

## 3. Scale and capacity

| Dimension | Launch assumption | 12-month projection | Breaks at | Source of estimate |
|---|---|---|---|---|
| Daily active users | 50,000 ILLUSTRATIVE | 150,000 ILLUSTRATIVE | 200,000 concurrent sessions | Engineering load test |
| Requests per second | 1,000 ILLUSTRATIVE | 3,000 ILLUSTRATIVE | 5,000 rps | Infrastructure capacity plan |
| Customer assets under management | $500 million ILLUSTRATIVE | $1.5 billion ILLUSTRATIVE | $2 billion hot wallet limit | Treasury forecast |

"Breaks at" forces the honest conversation with engineering now instead of during the incident.

## 4. Security and privacy

| Requirement | Target or owner | Verified by |
|---|---|---|
| Authentication and session policy | MFA required for all withdrawals; session timeout 15 minutes | Penetration test |
| Authorization model (who can do what) | Role-based access control; withdrawal approvals require dual sign-off for amounts over $10,000 | Access review log |
| Data classes handled, and their handling rule | PII, transaction history, wallet addresses; PII classification lives in [../templates/architecture/data-model.md](../templates/architecture/data-model.md) | Data inventory audit |
| Encryption in transit and at rest | TLS 1.3 in transit; AES-256 at rest | Cryptographic review |
| Audit logging of sensitive actions | All key operations, withdrawals, and compliance overrides logged; retention 7 years | Log integrity check |
| Hot-wallet share cap | No less than 95% of customer asset value in cold storage at every daily snapshot; any breach pages the CISO within 15 minutes | Custody attestation log |
| Signing-quorum requirement | Key operations require 3-of-5 quorum signatures from hardware security modules | Quorum enforcement test |
| Travel-rule data sent before settlement | EU Transfer of Funds Regulation (EU) 2023/1113: originator and beneficiary information must accompany every transfer of crypto-assets between crypto-asset service providers, whatever the amount, applying from 30 December 2024; for transfers above EUR 1,000 to or from a self-hosted address the provider must also assess whether that address is owned or controlled by its own customer. FATF Recommendation 16: originator and beneficiary information should accompany a transfer, with a de minimis threshold of USD or EUR 1,000 below which fewer data may be required. United States: Bank Secrecy Act travel rule, 31 CFR 1010.410(f), applies to transmittals of USD 3,000 or more. | Compliance screening report |

If a regulator governs any data class here and the product contains an AI or machine-learning feature, the regulated overlay applies: see ../../os/STAGE-GATES.md for the rule and ../../modules/regulated/README.md for the module. A regulated data class with no model in the product does not activate it. Security architecture detail belongs in ../templates/architecture/security-architecture.md; this table holds the product-level commitments. Regulatory statements are as of 2026-09-11; confirm with counsel; not legal advice.

## 5. Accessibility

| Requirement | Target or owner | Verified by |
|---|---|---|
| Conformance level | WCAG 2.2 AA ILLUSTRATIVE | Accessibility audit |
| Keyboard-only operation of core flows | Yes for login, trade, withdraw | Manual test script |
| Localization and language support | English, Spanish, German ILLUSTRATIVE | Translation QA |

A buyer or agency asking for a VPAT/ACR wants the Accessibility Conformance Report per Section508.gov; that is a compliance-team output built from this table's audit artifact, not a template here. The market and locale list that drives the localization row lives in the discovery document's target market fields: ../discovery/discovery-document.md.

## 6. Data retention

| Data class | Retention period | Deletion behavior | Driven by (policy, regulation, choice) | Owner |
|---|---|---|---|---|
| KYC documents | 5 years post-account closure | Secure destruction | AML regulations | Amara Singh, Compliance Lead |
| Transaction logs | 7 years | Archive then delete | Tax and regulatory requirements | Jai Kaur, Head of Treasury |
| Support tickets | 2 years | Delete | Internal policy | Leo Martinez, Support Manager |

## 7. Operability

| Requirement | Target or owner | Verified by |
|---|---|---|
| Observability: logs, metrics, traces for core flows | Centralized logging for withdrawals, custody movements, and API errors; detail in [../templates/architecture/observability.md](../templates/architecture/observability.md) | Monitoring dashboard review |
| Feature kill or rollback path | Kill switch for new listings and withdrawal processing; disable within 5 minutes | Incident runbook |
| Support handover | Runbook location: internal wiki page "Northbank Withdrawal Ops"; owner: Leo Martinez, Support Manager, by 2026-10-15 | Handover checklist |

## 8. Waivers

| Requirement waived | Waived by | Reason | Revisit date |
|---|---|---|---|
| Cold storage share minimum of 95% | Priya Anand, Product Manager | Temporary allowance of up to 10% hot-wallet share (cold storage minimum relaxed to 90%, versus the standard 95% floor) during initial liquidity seeding phase to ensure market depth for major pairs | 2026-12-01 |

A target can be waived only by its owner, in writing, with a revisit date. Waivers hide here rather than in meeting minutes.

---

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every row has a number or a named owner and date for the number
- [x] No adjective survives without a measurement ("fast", "secure", "scalable" all resolved)
- [x] Unagreed numbers are labeled ILLUSTRATIVE
- [x] Every row names its verification artifact
- [x] Scale table includes a "breaks at" estimate from engineering
- [x] Retention table covers every data class in the data model
- [x] All waivers are recorded here with a revisit date

Signed at Gate 2 attempt 1, 2026-09-11: Priya Anand, product owner; Jai Kaur, head of treasury; Amara Singh, compliance lead; David Chen, CISO.
