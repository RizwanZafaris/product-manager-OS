# Non-Functional Requirements: Cistern Sentry

Fills [templates/definition/nfr.md](../templates/definition/nfr.md). Everything here is invented for this standalone example: Cistern Sentry is a fictional connected leak detector, Beatriz Santos its fictional product manager, and every number, name and date is ILLUSTRATIVE, not drawn from any real device or market. There is no external hardware-IoT journey or data sheet. See the [examples index](README.md).

**Owner:** Beatriz Santos · **Date:** 2026-09-11 · **Status:** In review
**Parent PRD:** none filled for this example

## 1. Performance and latency

| Requirement | Target (number) or owner for the number | Measured how and where | Verified by |
|---|---|---|---|
| Local alarm trigger after connectivity loss (fail-loud) | 90 s at p95, measured from last successful heartbeat to local audible alarm + app push | Bench test, 40 units, connection killed at hub; p95 alarm latency logged against the 90 s target | Gate 4 bench report; current status: target met at bench (p95 = 61 s against the 90 s target); field validation pending on a unit with a battery below 20%, where the radio's transmit-power fallback has not yet been tested against the alarm's own power draw |
| Battery life at reporting interval | 18 months at 15-minute reporting interval, using two AA lithium batteries | Continuous discharge simulation in environmental chamber at 25°C; validated against field return rates | Gate 4 reliability report; owner: Marcus Chen, hardware lead, by 2026-10-15 |
| Radio certification compliance | FCC Part 15 Subpart C (intentional radiators, since the device carries active Wi-Fi/Zigbee transceivers); EU Radio Equipment Directive 2014/53/EU with delegated act (EU) 2022/30 on cybersecurity requirements, applying from 1 August 2025 | Accredited test lab reports; DoC signed by manufacturer | Certification bodies' test reports held in quality records; confirm with counsel that all harmonised standards are fully applied to avoid notified-body requirement; confirm delegated-act applicability date and FCC subpart citation with counsel as of 2026-09-11 |

## 2. Availability and reliability

| Requirement | Target or owner | Measured how | Verified by |
|---|---|---|---|
| Device uptime (connected state) | 99.5% monthly ILLUSTRATIVE, excluding scheduled maintenance windows; owner: Beatriz Santos, to validate with field telemetry by 2026-11-01 | Fleet telemetry dashboard counting heartbeats received vs expected | Gate 5 operational review; note: an offline device fails loud locally but cannot report its own downtime, so this metric is a floor, not a ceiling |
| Recovery time after failure (RTO) | 4 hours for OTA update rollback to previous stable firmware | Staged ring deployment logs; manual recovery drill on bricked test units | Gate 4 release-readiness checklist; brick recovery procedure documented in runbook |
| Tolerable data loss window (RPO) | Zero: leak detection events buffered locally until cloud sync confirmed | Event queue depth monitoring; verify no event dropped during 24-hour connectivity outage | Gate 4 integration tests with simulated network partitions |

An availability target implies a maintenance and on-call answer; if none exists, say so here and route it to ../operate/operational-readiness-review.md. *Note: Cistern Sentry's fleet support model assumes over-the-air fixes first, field replacement second. No 24/7 on-call rotation exists yet; open item owned by Beatriz Santos to define escalation path before Gate 5.*

## 3. Scale and capacity

| Dimension | Launch assumption | 12-month projection | Breaks at | Source of estimate |
|---|---|---|---|---|
| Active devices in field | 5,000 units | 50,000 units | Cloud ingestion pipeline saturates at 100,000 concurrent connections without horizontal scaling; estimated break point based on illustrative estimate from this example's own load test | Engineering capacity plan, reviewed 2026-08-20 |
| Daily telemetry volume | 480,000 messages/day (5,000 × 96 intervals) | 4.8 million messages/day | Message broker disk throughput exceeds baseline provisioning at >60 million msgs/day (derived from load-test extrapolation scaling the pilot cohort's peak daily rate by the projected device growth factor); owner: Dev Patel, platform architect, to provide revised sizing by 2026-09-30 | Load-test extrapolation from pilot cohort |
| Firmware storage per device | 2 MB application image | 2 MB unchanged | Flash memory partition fixed at design; breaks if feature growth requires >2 MB, forcing hardware revision | Hardware BOM review, locked at EVT close |

"Breaks at" forces the honest conversation with engineering now instead of during the incident.

## 4. Security and privacy

| Requirement | Target or owner | Verified by |
|---|---|---|
| Authentication and session policy | Mutual TLS between device and cloud; unique per-device certificate issued at manufacture; no default passwords (UK PSTI Act); unique preprogrammed passwords or reasonable security features (California SB-327) | Penetration test report; certificate inventory audit |
| Authorization model (who can do what) | User account controls only their paired devices; admin role limited to fleet operators via separate OAuth scope | Access-control matrix reviewed at Gate 4; owner: Lena Torres, security lead, sign-off by 2026-09-25 |
| Data classes handled, and their handling rule | Device ID, timestamped leak events, battery level, signal strength. No PII collected directly from device. Location derived from user-entered home address, stored encrypted at rest. Classification lives in [../templates/architecture/data-model.md](../templates/architecture/data-model.md) | Data-flow diagram audited by compliance team |
| Encryption in transit and at rest | TLS 1.3 in transit; AES-256-GCM at rest for cloud-stored event data | Cryptographic module validation per FIPS 140-3 guidelines; confirm implementation details with counsel as of 2026-09-11 |
| Audit logging of sensitive actions | All OTA update pushes, firmware signature changes, and admin role grants logged immutably for 7 years | Log integrity verification script run quarterly; retention policy aligned with liability protection and internal policy |
| Signed OTA updates with staged rings and brick recovery | Updates signed with Ed25519 key pair; public key burned into bootloader; staged rollout rings (5% → 25% → 100%) with automatic halt on >2% failure rate; dual-bank flash allows rollback to previous version if new image fails health check within 60 seconds | Gate 4 release-readiness checklist includes staged-ring dry run; brick-recovery procedure tested on 10 units with corrupted images |
| Field temperature and humidity envelope | Operational range: -10°C to 50°C; 10% to 90% RH non-condensing | Environmental chamber testing per IEC 60068-2 series; report archived in quality system |
| UK PSTI Act security requirements | No default passwords; published vulnerability-disclosure policy and a published minimum security-update period; Cistern Sentry commits to 5 years from sale ILLUSTRATIVE (owner: legal) | Policy documents reviewed by legal; alignment with ETSI EN 303 645 baseline verified |
| EU Cyber Resilience Act vulnerability reporting | Vulnerability and incident reporting (CRA Art. 14) applies from 11 September 2026 for products placed on the market before that date; from 11 December 2027 it applies to all products, alongside the remaining obligations. VERIFY with counsel as of 2026-09-11. Incident reporting timelines and technical documentation requirements mapped to CRA Annex I | Compliance gap analysis completed by Delphine Roussel (fictional regulatory consultant), dated 2026-08-15; action items tracked in risk register |

If a regulator governs any data class here and the product contains an AI or machine-learning feature, the regulated overlay applies: see ../../os/STAGE-GATES.md for the rule and ../../modules/regulated/README.md for the module. A regulated data class with no model in the product does not activate it. Security architecture detail belongs in ../architecture/security-architecture.md; this table holds the product-level commitments. *Cistern Sentry contains no AI or ML features; the regulated overlay does not apply.*

## 5. Accessibility

| Requirement | Target or owner | Verified by |
|---|---|---|
| Conformance level | WCAG 2.2 AA for companion mobile app; device itself has no screen, so physical accessibility limited to audible alarm frequency (4 kHz ± 5%) ILLUSTRATIVE (owner: Marcus Chen, hardware lead) and visual LED indicator color contrast ratio ≥ 4.5:1 against enclosure background ILLUSTRATIVE (owner: Beatriz Santos, product manager) | App store submission review; third-party accessibility audit scheduled for Gate 4; owner: Jordan Lee, UX designer, report due 2026-10-01 |
| Keyboard-only operation of core flows | N/A for device; app supports full keyboard navigation for pairing and alert acknowledgment | Automated axe-core scan integrated into CI pipeline |
| Localization and language support | English, Spanish, French, German at launch; single language fallback behavior defined in app spec | Market entry plan in discovery document; revisit expansion at 2027-Q2 |
| Colour-scheme support | N/A for device (no screen). App follows OS setting (light/dark); user toggle persists in local storage. First-load flash is minimized via CSS variables but not eliminated. | Automated axe-core scan in CI; visual regression tests |
| Text direction | LTR only for launch languages (English, Spanish, French, German). RTL support not planned for launch; revisit at 2027-Q2 market expansion. | App spec review; discovery document market fields |
| Reduced motion honoured | N/A for device (no screen). App honours OS reduced-motion setting; non-essential animations are disabled when enabled. | Automated axe-core scan in CI; manual QA test |
| Focus visible required | Yes for app. Custom focus style meets 3:1 contrast against adjacent colors. N/A for device (no screen). | Automated axe-core scan in CI; third-party accessibility audit |
| Minimum target size | WCAG 2.5.8: 24x24 CSS px minimum for app touch targets. N/A for device (no screen). | Automated axe-core scan in CI; design review |
| Density | Comfortable density for app. No user toggle for density. N/A for device (no screen). | Design system documentation; user research notes |

A buyer or agency asking for a VPAT/ACR wants the Accessibility Conformance Report per Section508.gov; that is a compliance-team output built from this table's audit artifact, not a template here. The market and locale list that drives the localization row lives in the discovery document's target market fields: ../discovery/discovery-document.md.

## 6. Data retention

| Data class | Retention period | Deletion behavior | Driven by (policy, regulation, choice) | Owner |
|---|---|---|---|---|
| Leak event timestamps and device IDs | 2 years rolling | Anonymized after 2 years; aggregated counts retained indefinitely for trend analysis | GDPR Art. 5(1)(e) storage limitation principle; internal analytics need | Beatriz Santos |
| Battery level history | 90 days | Deleted automatically upon expiry | Predictive maintenance model retraining window | Dev Patel |
| Signal strength logs | 30 days | Deleted automatically upon expiry | Debugging tooling only; not used for customer-facing insights | Marcus Chen |
| User account data (email, hashed password) | Duration of account + 30 days grace | Hard delete after grace period; backup snapshots purged within 7 days | CCPA right to deletion; GDPR Art. 17 | Lena Torres |
| Vulnerability disclosure correspondence | 7 years | Archived read-only; accessible only to security and legal teams | Internal-policy choice, not a regulatory minimum; owner: Lena Torres, security lead, by 2026-09-25 | Delphine Roussel |

## 7. Operability

| Requirement | Target or owner | Verified by |
|---|---|---|
| Observability: logs, metrics, traces for core flows | Heartbeat success/failure, alarm trigger latency, battery voltage, RSSI. Traces propagated through MQTT broker to cloud ingestion service. Detail in [../templates/architecture/observability.md](../templates/architecture/observability.md) | Grafana dashboards reviewed at Gate 4; trace sampling rate set at 10% to balance cost vs visibility |
| Feature kill or rollback path | Remote disable of non-critical features (e.g., periodic self-test) via signed config flag; full firmware rollback available within 4 hours via staged ring reversal | Runbook step RB-07 tested during brick-recovery drill |
| Support handover | Runbooks located in Confluence space "CS-Ops"; owner: Sarah Kim, support lead, to complete final draft by 2026-09-20 | Gate 5 operational readiness review checks runbook completeness |

## 8. Waivers

<!-- A target can be waived only by its owner, in writing, with a revisit date.
     Waivers hide here rather than in meeting minutes. -->

| Requirement waived | Waived by | Reason | Revisit date |
|---|---|---|---|
| Field validation of fail-loud alarm under low-battery condition (<20% charge) | Beatriz Santos | Bench test met the 90 s p95 target (p95 = 61 s), but radio transmit-power fallback interaction with alarm buzzer current draw has not been tested at low battery. Risk accepted temporarily because: (a) low-battery condition triggers its own early-warning alarm at 25%, reducing likelihood of silent failure; (b) field deployment begins in controlled pilot cohort with manual inspection weekly. | 2026-10-15, when Marcus Chen completes low-battery bench test per section 1 row 2 owner commitment |

---

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every row has a number or a named owner and date for the number
- [x] No adjective survives without a measurement ("fast", "secure", "scalable" all resolved)
- [x] Unagreed numbers are labeled ILLUSTRATIVE
- [x] Every row names its verification artifact
- [x] Scale table includes a "breaks at" estimate from engineering
- [x] Retention table covers every data class in the data model
- [x] All waivers are recorded here with a revisit date

Signed at Gate 2 attempt 1, 2026-09-11: Beatriz Santos, product owner; Marcus Chen, hardware lead; Lena Torres, security lead; Delphine Roussel, regulatory consultant (fictional role, consulted for compliance mapping).
