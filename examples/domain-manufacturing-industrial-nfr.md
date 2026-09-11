# NFR: Anvilworks LineGuard Controller

Fills [templates/definition/nfr.md](../templates/definition/nfr.md). Everything here is invented: Anvilworks Automation is a fictional line-controller software vendor, LineGuard is its fictional product that also performs a safety function, the people are roles filled by invented names, and every number, name and date is ILLUSTRATIVE. See the [examples index](README.md).

**Owner:** Elena Rostova, principal product manager · **Date:** 2026-09-11 · **Status:** Approved at Gate 2
**Parent PRD:** not filled for this example (ILLUSTRATIVE)

## 1. Performance and latency

| Requirement | Target (number) or owner for the number | Measured how and where | Verified by |
|---|---|---|---|
| Emergency-stop signal propagation to actuator cut-off | 50 ms at p95, ILLUSTRATIVE | Hardware-in-the-loop test rig, quarterly | IEC 61508 revalidation record, signed by functional-safety assessor |
| HMI display update of controller state | 200 ms at p95, ILLUSTRATIVE | Synthetic check on plant network simulator | Test report TR-LG-042 |
| Batch historian write cycle completes in | 1 second per cycle, ILLUSTRATIVE | Load test with 10,000 tags at 1 Hz sampling | Test report TR-LG-043 |

## 2. Availability and reliability

| Requirement | Target or owner | Measured how | Verified by |
|---|---|---|---|
| Availability of control path (no cloud dependency) | 99.99% monthly, ILLUSTRATIVE; local redundancy required, no single point of failure on plant floor | Uptime monitor on OT segment, separate from IT monitoring stack | Operational readiness review ORR-LG-01 |
| Recovery time after failure (RTO) for emergency-stop interlock path | 2 seconds, ILLUSTRATIVE: the line's documented safe-state time, not a generic RTO number | Hardware-in-the-loop test rig, quarterly | IEC 61508 revalidation record, signed by the functional-safety assessor, filed before the change goes live |
| Tolerable data loss window (RPO) for historian quality traceability | 5 minutes, ILLUSTRATIVE | Backup cadence verification on redundant storage nodes | Test report TR-LG-044 |

<!-- An availability target implies a maintenance and on-call answer; if none exists, say so here and route it to ../operate/operational-readiness-review.md. -->
Maintenance windows are tied strictly to planned shutdowns. On-call rotation covers both IT support and OT field engineers; escalation paths defined in runbook RB-LG-OT-01.

## 3. Scale and capacity

| Dimension | Launch assumption | 12-month projection | Breaks at | Source of estimate |
|---|---|---|---|---|
| Controlled axes per controller instance | 64 axes | 128 axes | 150 axes (memory buffer exhaustion on HIL rig) | Engineering estimate E-05, validated on HIL rig |
| Historian tags retained for traceability | 50,000 tags | 100,000 tags | 118,000 tags (write throughput saturation) | Capacity model CM-02 |
| Concurrent OT client connections (HMI, MES bridge) | 10 clients | 25 clients | 30 clients (network stack limit in embedded OS) | Stress test ST-07 |

<!-- "Breaks at" forces the honest conversation with engineering now instead of during the incident. -->

## 4. Security and privacy

| Requirement | Target or owner | Verified by |
|---|---|---|
| Authentication and session policy | MFA for all remote access via jump host; local console access restricted to physical key + PIN; sessions timeout after 5 minutes idle | Penetration test PT-LG-01, reviewed by OT security lead Marcus Thorne |
| Authorization model (who can do what) | Role-based access control aligned with IEC 62443 zones; safety-rated functions locked to certified engineers only | Access control matrix AC-LG-01 |
| OT network segmentation (zone and conduit model) | Two zones: Control Zone (controller instances and safety I/O) at IEC 62443 Security Level target SL2, Historian Zone (traceability and MES bridge) at SL1; one conduit between them, MES-to-controller writes disallowed on that conduit. Full zone map lives in a filled `security-architecture.md` for LineGuard (not filled for this example) | Security architecture review SA-LG-OT-01 |
| Data classes handled, and their handling rule | Process telemetry (non-PII), equipment logs (non-PII), operator IDs (PII, hashed); PII classification lives in a filled `data-model.md` for LineGuard (not filled for this example) | Data protection impact assessment DPIA-LG-01 |
| Encryption in transit and at rest | TLS 1.2+ on all conduits crossing zone boundaries (see OT network segmentation row above); AES-256 at rest on historian storage nodes | Cryptographic audit CA-LG-01 |
| Audit logging of sensitive actions | All changes to safety-rated parameters logged with user ID, timestamp, old/new value; retained for 7 years | Log integrity check LIC-LG-01 |

<!-- If a regulator governs any data class here and the product contains an AI or machine-learning feature, the regulated overlay applies: see ../../os/STAGE-GATES.md for the rule and ../../modules/regulated/README.md for the module. A regulated data class with no model in the product does not activate it. Security architecture detail belongs in ../architecture/security-architecture.md; this table holds the product-level commitments. -->
No AI/ML features currently in scope. EU Machinery Regulation 2023/1230 applies as of 2027-01-20 (verify exact application date with counsel; confirm with counsel, not legal advice). Product-liability exposure under updated EU regime requires full traceability of software versions deployed to each unit.

## 5. Accessibility

| Requirement | Target or owner | Verified by |
|---|---|---|
| Conformance level | Not applicable for embedded HMI interfaces used exclusively by trained operators in controlled industrial environments; accessibility requirements deferred to future consumer-facing applications | Decision log DL-LG-ACC-01 |
| Keyboard-only operation of core flows | Not applicable; interface designed for touch-screen and dedicated hardware buttons | Design spec DS-LG-HMI-01 |
| Localization and language support | English and German at launch; additional languages require safety-function re-validation per language context | Translation validation plan TVP-LG-01 |

<!-- A buyer or agency asking for a VPAT/ACR wants the Accessibility Conformance Report per Section508.gov; that is a compliance-team output built from this table's audit artifact, not a template here. The market and locale list that drives the localization row lives in the discovery document's target market fields: ../discovery/discovery-document.md. -->

## 6. Data retention

| Data class | Retention period | Deletion behavior | Driven by (policy, regulation, choice) | Owner |
|---|---|---|---|---|
| Safety-rated configuration history | 10 years | Archival cold storage, accessible only by functional-safety assessor | IEC 61508 documentation requirements | Dr. Aris Vlachos, functional-safety assessor |
| Production batch genealogy (quality traceability) | 7 years | Automated purge after 7 years, unless flagged for recall investigation | Customer contractual requirement (automotive sector standard) | Quality Director Lena Schmidt |
| Operator login records (hashed IDs) | 2 years | Automated deletion | Internal privacy policy PP-LG-01 | Data Protection Officer Kofi Mensah |
| System event logs (non-sensitive) | 90 days | Rotating overwrite | Storage capacity constraint SC-01 | DevOps Lead Keiko Tanabe |

## 7. Operability

| Requirement | Target or owner | Verified by |
|---|---|---|
| Observability: logs, metrics, traces for core flows | Local syslog server on OT segment; metrics exported via OPC-UA to plant historian; no external cloud ingestion allowed on control path | Monitoring setup MS-LG-01 |
| Feature kill or rollback path | For non-safety features: immediate disable via configuration flag (<1 minute). For safety-rated features: rollback requires documented change request and revalidation; no immediate kill permitted without safe-state transition | Change management procedure CMP-LG-01 |
| Support handover | Runbooks stored in plant-specific knowledge base KB-LG-<site>; updated quarterly | Handover checklist HC-LG-01 |

<!-- A target can be waived only by its owner, in writing, with a revisit date. Waivers hide here rather than in meeting minutes. -->

## 8. Waivers

| Requirement waived | Waived by | Reason | Revisit date |
|---|---|---|---|
| Firmware signing on third-party legacy PLC modules that LineGuard reads from and writes to over the plant network, not LineGuard's own executable image, which ships signed | Elena Rostova, principal PM, approved by CTO David Chen | Legacy hardware lacks secure boot capability; compensating control implemented via physical access controls and cryptographic checksum verification on firmware images loaded via offline media | 2027-06-30, when next-generation hardware platform enters beta testing |

---

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every row has a number or a named owner and date for the number
- [x] No adjective survives without a measurement ("fast", "secure", "scalable" all resolved)
- [x] Unagreed numbers are labeled ILLUSTRATIVE
- [x] Every row names its verification artifact
- [x] Scale table includes a "breaks at" estimate from engineering
- [x] Retention table covers every data class in the data model
- [x] All waivers are recorded here with a revisit date

Signed at Gate 2, 2026-09-11: Elena Rostova, principal product manager; Dr. Aris Vlachos, functional-safety assessor; Marcus Thorne, OT security lead
