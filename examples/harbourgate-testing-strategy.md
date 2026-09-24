# Testing Strategy: Harbourgate

Fills [templates/delivery/testing-strategy.md](../templates/delivery/testing-strategy.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date and identifier is ILLUSTRATIVE, drawn from the [Harbourgate journey](harbourgate-journey.md) and [Harbourgate coverage sheet](harbourgate-coverage-sheet.md).

**Owner:** Noor Haddad · **Engineering counterpart:** Tomasz Wierzbicki · **Status:** Agreed
**Version:** 2 · **Date:** 2026-06-26

## 1. Scope

- In scope for testing: Quay's money-moving modules, including authorise, capture, void, refund and reconciliation matching; the Kestrel integration in the Kestrel sandbox; provider and consumer contracts; end-to-end checkout and kiosk payment flows; the 2026-06-05 load test; rehearsals 1 to 3 and the rollback rehearsal; the synthetic failure check; accessibility of the payment-step components; and the pre-production settlement-file flow.
- Out of scope, and why that is safe: Model evals are not applicable because Harbourgate has no model or AI feature. The guest checkout redesign remains out of scope because it is unrelated to the payment migration. The contractor's wrapper is not modified during this migration.
- Linked requirements: N/A because the product-specific PRD and acceptance-criteria files are not named in the supplied evidence. The requirements used here are HARBOURGATE-S1 to HARBOURGATE-S12 and AC-1 to AC-13 in [harbourgate-journey.md](harbourgate-journey.md).

Two lessons are carried into this version. Gate 4 attempt 1 made “exercised, not described” a rule after FS-2 and FS-5 were described but not exercised. HG-INC-14 showed that pre-production needed its own settlement-file drop. A2 split the SFTP drops, and HC8 records the resulting no-production-data policy.

## 2. Test levels

| Level | What it proves | Owner | Where it runs | Blocks release? |
|---|---|---|---|---|
| Unit | Money-moving modules enforce authorise, capture, void, refund, idempotency and reconciliation behaviour. The coverage target is 90% of lines for the critical path modules and 80% of lines for new code in this release. | Bea Lindqvist | CI, every merge | yes, failed tests or a missed target block release |
| Integration | Quay communicates with Kestrel correctly, including successful authorisation, timeout, retry, status polling, decline handling and settlement-file processing. Marlowe has no sandbox: DEP-2, requested 2026-04-20, was never committed, so Marlowe reconciliation was instead tested by reading the production settlement drop under the keep flag (R3's mitigation), closed 2026-07-03 when ADR-0004 removed the need. | Bea Lindqvist | Kestrel sandbox and pre-production's separate settlement-file drop | yes, any failed blocking scenario blocks release |
| Contract (API) | Quay consumers and the Kestrel provider continue to agree on request, response, error, idempotency and event schemas. | Tomasz Wierzbicki | CI, every merge | yes, a provider or consumer contract failure blocks release |
| End to end | Web, app and kiosk payment journeys work through Quay and Kestrel, including decline and retry behaviour, refund routing, legacy table writes and the kiosk fallback. | Noor Haddad | Pre-production with synthetic data and production-shaped schemas | yes, a failed acceptance journey blocks release |
| Performance and load | The authorise path meets the N23 latency target and the N24 request-rate readings. The 2026-06-05 load test is the required evidence. | Tomasz Wierzbicki | Kestrel sandbox | yes, the N23 or N24 load-test evidence must pass |
| Security | Environment separation prevents pre-production credentials from reading the production settlement drop, and payment data handling follows the agreed policy. A2's failed read attempt is required evidence. | Hamid Qureshi | CI for the ingestion-job check, pre-production for the separate-drop check | yes, a production-data access path or failed security check blocks release |
| Accessibility | The accessibility checklist is completed for the Kestrel hosted card fields, decline message and retry offer, step-up challenge handoff, and kiosk “pay at the till” screen. Quay must introduce no new finding. | Noor Haddad, with Ines Castellanos | Accessibility checklist and pre-production walkthrough | yes, an unresolved finding introduced by Quay blocks release |
| Model evals (AI features, see [eval spec](../templates/ai/eval-spec.md)) | N/A because Harbourgate has no AI feature or model. | N/A because model evals do not apply | N/A because no model runs | N/A because this level does not apply |
| Rehearsals and rollback | The migration can run through settlement reconciliation, including the straddle set, and the team can flip to legacy and restore the new path within the rehearsed timings. Rehearsals 1 to 3 and the rollback rehearsal are required evidence. | Tomasz Wierzbicki | Pre-production with production-shaped schemas and synthetic data | yes, rehearsal and rollback evidence must pass |

The completed evidence includes the 2026-06-05 load test, N23 and N24, rehearsal 1 at N37, rehearsal 2 at N38, rehearsal 3 at N39, rollback rehearsal N40, and the synthetic failure check N72. The blocking rule is deliberate at every applicable level: a test level is not advisory simply because another level passes.

## 3. Coverage targets

| Area | Target | Current | Owner |
|---|---|---|---|
| Money-moving modules, authorise, capture, void, refund and reconciliation matcher | 90% of lines, target | 92% on 2026-06-26, measured | Bea Lindqvist |
| New code in this release | 80% of lines, target | 86% on 2026-06-26, measured | Tomasz Wierzbicki |

The targets and readings come from HC7 in [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md). Coverage is a smoke alarm, not proof that the journeys, failure scenarios or reconciliation behaviour are correct.

## 4. Environments

| Environment | Purpose | Data policy | Refresh cadence | Who has access |
|---|---|---|---|---|
| Dev | Local development and unit-test feedback | Synthetic only | N/A because no cadence is recorded in the supplied evidence | Payments squad |
| Staging, the pre-production environment | Integration, end-to-end, rehearsal, rollback and synthetic failure testing | No production personal data. The production-shaped copy is generated from production schemas with synthetic card tokens. Settlement files are generated from provider file specifications into pre-production's own drop. | N/A because no cadence is recorded in the supplied evidence | Payments squad, Noor Haddad, Hamid Qureshi and named test participants |
| Production | Live payment processing and monitored release operation | Real production data, monitored. Production personal data never leaves production. | N/A because no refresh is performed | On-call and production operators with approved access |

A2 is part of the environment boundary: pre-production credentials cannot read the production drop. HG-INC-14 is not repeated. The no-production-data policy is recorded in HC8 and agreed by Hamid Qureshi on 2026-06-26.

## 5. Entry and exit criteria

**Testing starts when:**
- [ ] Acceptance criteria are signed (Gate 4 input, see [../templates/definition/acceptance-criteria.md](../templates/definition/acceptance-criteria.md))
- [ ] The environment above is up and seeded
- [ ] The Kestrel sandbox is reachable and its integration fixtures are available
- [ ] Pre-production has its own settlement-file drop, and a pre-production credential fails to read the production drop
- [ ] The unit and contract suites are running in CI
- [ ] The failure scenarios are at v2 or later, with FS-2 and FS-5 exercised rather than only described

**Testing ends when:**
- [ ] Every blocking level in section 2 has run and passed
- [ ] The 2026-06-05 load test has recorded the N23 and N24 readings
- [ ] Rehearsals 1 to 3 and the rollback rehearsal have passed, with N37 to N40 recorded
- [ ] The synthetic failure check N72 has passed
- [ ] Open defects are within the ladder rules in section 6
- [ ] The edge-case register has no unresolved rows. No separate edge-case register is supplied in the evidence for this example, so its status must be confirmed before the release-readiness review
- [ ] Results are recorded where the release-readiness reviewer can find them: CI results, the Kestrel sandbox test log, the load-test record, the rehearsal log, the accessibility checklist and the synthetic failure-check record

## 6. Defect severity ladder (canonical)

This table is the single defect-severity dictionary for four documents: this testing strategy, the [UAT plan](harbourgate-uat-plan.md), the [release-readiness](harbourgate-release-readiness.md) checklist and the [support runbook](harbourgate-support-runbook.md). Those documents use their own wording only alongside one of these IDs, and the release rule attached to an ID is the one stated here and is not restated differently in any of them. Quay's other DELIVER documents score other things on their own scales, such as alert routing in the observability plan and risk in the FMEA; those are not defect severities and do not use these IDs.

A check reads these four documents and fails the build when one of them carries a second table that defines a severity, when one writes any other severity vocabulary at all, whether a Sev N style scale or a known issue labelled Low, and when one attaches a definition to an ID in prose: a sentence saying what SN means, or saying to treat some kind of defect as SN. It reads HTML comments and code blocks too, and it is strict enough that this paragraph cannot spell those IDs out. What it does not reach is prose that defines a defect class without naming an ID, such as "a job a tester cannot complete at all always blocks the release": that sentence contradicts nothing by ID, so nothing fails, and whoever reviews the document has to catch it.

| Severity | Definition | Release rule |
|---|---|---|
| S1 | Data loss, security or privacy breach, or the product unusable | Always blocks |
| S2 | The job a user is trying to do cannot be completed and there is no workaround | Blocks unless a named approver records who accepted it and why |
| S3 | The job a user is trying to do completes only with a workaround, or a non-core flow is broken | Ships with a named fix owner and a fix date |
| S4 | Cosmetic, no job affected | Ships, tracked |

A defect is classified once, against this table, and keeps that same ID in every document that mentions it.

## Exit gate

This document passes when:

- [x] Every test level has an owner and an explicit blocking rule. Model evals are marked N/A because Harbourgate has no AI feature.
- [x] Coverage targets are numbers with owners, not adjectives. HC7 records 90% and 80% targets, with current readings of 92% and 86%.
- [x] Entry and exit criteria could be applied by someone who just joined the team. They identify the CI, sandbox, pre-production, rehearsal, rollback, synthetic failure and accessibility evidence required.
- [x] The environment table states the data policy for each environment. Pre-production has its own drop and no production personal data under A2 and HC8.
- [x] The severity ladder says exactly what blocks release, and none of the other three covered documents, the UAT plan, the release-readiness checklist and the support runbook, defines a defect severity of its own. S1 and S2 block under the stated rules, while S3 and S4 require the recorded treatment; the UAT plan's section 5 and the support runbook's section 4 are crosswalks onto these IDs, not second scales.

Signed: Noor Haddad, QA Lead, 2026-06-26
