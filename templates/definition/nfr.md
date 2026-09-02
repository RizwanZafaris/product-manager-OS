# Non-Functional Requirements: [feature or product name]

Stage: DEFINE, feeds Gate 2 (requirements signed off)
Knowledge: [Knowledge index](../../knowledge/INDEX.md)
Skill: [drafting-agent](../../agents/drafting-agent.md)

<!-- Non-functional requirements are where products quietly fail: nobody writes
     "must fall over at month three" but plenty of teams ship it by leaving this
     file empty.

     The one rule of this template: every row carries a NUMBER, or the NAME of
     the person who will produce the number and a date. "Fast", "secure",
     "scalable" are not requirements; they are adjectives waiting for an
     argument. A named owner for a missing number is honest; a blank is a
     decision deferred to whoever finds it blank.

     Every number is ILLUSTRATIVE until the named owner has agreed it; label
     accordingly. Verification lands later: each row names the artifact that will
     prove it at Gate 4 or 5. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved
**Parent PRD:** [prd.md](prd.md)

## 1. Performance and latency

| Requirement | Target (number) or owner for the number | Measured how and where | Verified by |
|---|---|---|---|
| [interaction] completes in | [n ms at p95, or "owner: name, by date"] | [APM, synthetic check] | [test or artifact] |
| [batch or background job] completes in | | | |

## 2. Availability and reliability

| Requirement | Target or owner | Measured how | Verified by |
|---|---|---|---|
| Availability of [surface] | [n% monthly, e.g. 99.9% ILLUSTRATIVE] | [uptime monitor] | |
| Recovery time after failure (RTO) | [n minutes] | [restore drill] | |
| Tolerable data loss window (RPO) | [n minutes] | [backup cadence] | |

<!-- An availability target implies a maintenance and on-call answer; if none
     exists, say so here and route it to ../operate/operational-readiness-review.md. -->

## 3. Scale and capacity

| Dimension | Launch assumption | 12-month projection | Breaks at | Source of estimate |
|---|---|---|---|---|
| [users, requests/s, records, storage] | | | [the number where the current design fails] | |

<!-- "Breaks at" forces the honest conversation with engineering now instead of
     during the incident. -->

## 4. Security and privacy

| Requirement | Target or owner | Verified by |
|---|---|---|
| Authentication and session policy | [statement or owner] | |
| Authorization model (who can do what) | [statement or owner] | |
| Data classes handled, and their handling rule | [list; PII classification lives in [../architecture/data-model.md](../architecture/data-model.md)] | |
| Encryption in transit and at rest | [standard, or owner] | |
| Audit logging of sensitive actions | [what is logged, retention] | |

<!-- If a regulator governs any data class here, the regulated overlay applies:
     see ../../modules/regulated/README.md. Security architecture detail belongs
     in ../architecture/security-architecture.md; this table holds the
     product-level commitments. -->

## 5. Accessibility

| Requirement | Target or owner | Verified by |
|---|---|---|
| Conformance level | [e.g. WCAG 2.2 AA, or owner and date] | [audit artifact] |
| Keyboard-only operation of core flows | [yes / no per flow] | |
| Localization and language support | [languages, or "single language, revisit at [date]"] | |

<!-- A buyer or agency asking for a VPAT/ACR wants the Accessibility Conformance
     Report per Section508.gov; that is a compliance-team output built from this
     table's audit artifact, not a template here. The market and locale list that
     drives the localization row lives in the discovery document's target market
     fields: ../discovery/discovery-document.md. -->

## 6. Data retention

| Data class | Retention period | Deletion behavior | Driven by (policy, regulation, choice) | Owner |
|---|---|---|---|---|
| | | | | |

## 7. Operability

| Requirement | Target or owner | Verified by |
|---|---|---|
| Observability: logs, metrics, traces for core flows | [what exists at launch; detail in [../architecture/observability.md](../architecture/observability.md)] | |
| Feature kill or rollback path | [mechanism, time to disable] | |
| Support handover | [runbook location, or owner and date] | |

## 8. Waivers

<!-- A target can be waived only by its owner, in writing, with a revisit date.
     Waivers hide here rather than in meeting minutes. -->

| Requirement waived | Waived by | Reason | Revisit date |
|---|---|---|---|
| | | | |

---

## Exit gate (feeds Gate 2: requirements signed off)

- [ ] Every row has a number or a named owner and date for the number
- [ ] No adjective survives without a measurement ("fast", "secure", "scalable" all resolved)
- [ ] Unagreed numbers are labeled ILLUSTRATIVE
- [ ] Every row names its verification artifact
- [ ] Scale table includes a "breaks at" estimate from engineering
- [ ] Retention table covers every data class in the data model
- [ ] All waivers are recorded here with a revisit date
