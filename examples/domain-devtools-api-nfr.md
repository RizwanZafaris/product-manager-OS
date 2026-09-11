# Non-Functional Requirements: Lanternfish API `/v1/orders` deprecation and rate limits

Fills [templates/definition/nfr.md](../templates/definition/nfr.md). Everything here is invented: Lanternfish API is a fictional public payments API platform sold to third-party fintech integrators, the people are roles filled by invented names, and every count, rate and date is ILLUSTRATIVE, based on this example's own illustrative assumptions. See the [examples index](README.md).

**Owner:** Priya Raghunathan, API platform lead · **Date:** 2026-09-11 · **Status:** In review at Gate 2 · **Parent PRD:** the Lanternfish `/v1/orders` deprecation PRD (not included in this standalone example)

## 1. Performance and latency

| Requirement | Target (number) or owner for the number | Measured how and where | Verified by |
|---|---|---|---|
| `POST /v1/orders` write path completes in | 400 ms at p95, 900 ms at p99 (ILLUSTRATIVE) | Synthetic check from three regions, continuous; production APM sampled per key | Load test before each quarterly capacity review |
| `GET /v1/orders/{id}` read path completes in | 150 ms at p95 (ILLUSTRATIVE) | Production APM | Load test before each quarterly capacity review |
| SDK call overhead (client-side, above the wire call) | 20 ms at p95 added by the official SDKs (ILLUSTRATIVE) | SDK instrumentation harness, run per release candidate | SDK release checklist |

The card at [../knowledge/domains/devtools-api.md](../knowledge/domains/devtools-api.md) asks what the first hour looks like for someone who has never seen this: time to first successful call is the only funnel step the platform fully controls, so the read path target is set tighter than the write path because the first successful call is a read (fetch a test order, then post one).

## 2. Availability and reliability

| Requirement | Target or owner | Measured how | Verified by |
|---|---|---|---|
| Availability of the `/v1/orders` surface | 99.9% monthly (ILLUSTRATIVE) | Uptime monitor against the published status page, synthetic checks from three regions | Status page incident record reviewed monthly |
| Recovery time after failure (RTO) | 30 minutes (ILLUSTRATIVE) | Restore drill run quarterly | Drill report filed by platform engineering |
| Tolerable data loss window (RPO) | 1 minute (ILLUSTRATIVE) | Backup cadence, replicated order store | Quarterly restore drill report |
| Status page update SLA | First public update within 15 minutes of a Sev-1 detection; updates every 30 minutes until resolved (ILLUSTRATIVE) | Incident timeline compared against status page post timestamps | Incident review, every Sev-1 and Sev-2 |
| Changelog and notice lead time to registered developers | Every change to a contract-governed surface announced in the public changelog and emailed to registered developers at least 30 days before it takes effect; a deprecation announcement uses the full window in section 6 (ILLUSTRATIVE) | Changelog publish timestamp versus effective date; registration email log | Priya Raghunathan, API platform lead, spot-check before each release train |

The status page update SLA is the promise the card's "error rate" and "uptime against the service level agreement" rows warn about: a monthly average absorbs the outage on the customer's launch day, so the update SLA is what a caller actually experiences during an incident. Exclusions for scheduled maintenance are listed on the status page; anything not listed there counts against the 99.9%.

An availability target implies a maintenance and on-call answer. On-call rotation and the maintenance window policy are owned by platform engineering and route to the operational readiness review for this surface (not included in this standalone example); this file holds the product-level commitment, not the roster.

## 3. Scale and capacity

| Dimension | Launch assumption | 12-month projection | Breaks at | Source of estimate |
|---|---|---|---|---|
| Active API keys | 1,800 (ILLUSTRATIVE) | 4,500 (ILLUSTRATIVE) | n/a for key count alone; keys are not the constraint | This example's own illustrative assumptions |
| Requests per second, aggregate, `/v1/orders` write path | 900 req/s (ILLUSTRATIVE) | 2,400 req/s (ILLUSTRATIVE) | 6,000 req/s before the write path's current sharding needs redesign, per platform engineering (ILLUSTRATIVE) | Platform engineering estimate, stated at the 2026-09-04 capacity review |
| Requests per second, per key | 50 req/s (ILLUSTRATIVE) | 50 req/s, unchanged; enterprise burst allowance of 5 s at 2x limit for registered enterprise keys (ILLUSTRATIVE) | Not a system break; the per-key ceiling is a policy number, and exceeding it returns 429 with `Retry-After` rather than failing | Published rate-limit policy; enterprise key list in the capacity doc |
| Order records retained in the hot store | 40 million (ILLUSTRATIVE) | 180 million (ILLUSTRATIVE) | 250 million in the current hot store design, before the archival tier must take over reads (ILLUSTRATIVE) | Platform engineering estimate, same review |

The "breaks at" column is the conversation the card says to have now rather than during the incident. The per-key row is deliberately "not a system break": 50 req/s per key with 429 and `Retry-After` on breach is an error contract, not a capacity limit, which is why it also appears in section 7.

## 4. Security and privacy

| Requirement | Target or owner | Verified by |
|---|---|---|
| Authentication and session policy | API keys for server-to-server calls; OAuth 2.0 authorization code with PKCE for user-context calls; key rotation supported without downtime (ILLUSTRATIVE) | Security review; penetration test before general availability of any new auth surface |
| Authorization model (who can do what) | Scoped keys: an integrator's key acts only on the merchant account it was issued for; no cross-tenant read path exists at any layer | Security review; tenancy isolation test in the integration suite |
| Data classes handled, and their handling rule | Card-adjacent order data and personal data of the integrator's end customers; classification lives in the product's data model document (not included in this standalone example) | Data-model review; classification is an input to this table, not restated here |
| Encryption in transit and at rest | TLS 1.3 in transit; AES-256 at rest, key management owned by platform engineering (ILLUSTRATIVE) | Security review; configuration audit |
| Audit logging of sensitive actions | Key creation, key rotation, scope change, and every order state transition logged; retained per section 6 | Audit log review; log retention check in the quarterly access review |

Lanternfish processes payment-related data and operates under payment-card industry rules that its integrators also carry; as of 2026-09-11 the relevant obligations and which of them apply to a given integrator's flow are stated in the terms of service and must be confirmed with counsel, not inferred from this table. This section is not legal advice. If a regulator governs any data class here and the product contains an AI or machine-learning feature, the regulated overlay at [../os/STAGE-GATES.md](../os/STAGE-GATES.md) and [../modules/regulated/README.md](../modules/regulated/README.md) applies; the `/v1/orders` deprecation and rate-limit work carries no such feature. Security architecture detail belongs in the product's security architecture document (not included in this standalone example).

## 5. Accessibility

| Requirement | Target or owner | Verified by |
|---|---|---|
| Conformance level | Not applicable to the API itself; the developer portal, documentation site and status page conform to WCAG 2.2 AA (ILLUSTRATIVE) | Accessibility audit of the portal and docs, before each major portal release |
| Keyboard-only operation of core flows | Yes for every developer-portal flow: key creation, log viewing, usage charts, support ticket filing | Manual keyboard walkthrough recorded in the portal release checklist |
| Localization and language support | English only at launch; revisit at 2027-03-01 (ILLUSTRATIVE) | Portal release checklist |

The API is consumed by code, so the accessibility surface is the portal where a developer reads the docs, copies a key and checks usage. A buyer asking for a VPAT or ACR wants an Accessibility Conformance Report per Section508.gov; that is a compliance-team output built from the audit artifact in this table, not restated here.

## 6. Data retention

| Data class | Retention period | Deletion behavior | Driven by (policy, regulation, choice) | Owner |
|---|---|---|---|---|
| Idempotency keys and their stored responses | 24 hours from first use (ILLUSTRATIVE); a retry after that window with the same key is treated as a new request | Expired automatically; no manual deletion path | Choice, tied to the retry window the SDKs use | Platform engineering lead |
| Order records | 7 years (ILLUSTRATIVE) | Archived to cold storage after 13 months, deleted at the end of the period on a scheduled job | Policy, driven by the record-keeping obligations that apply to the integrators' payments; confirm the exact period with counsel as of 2026-09-11, this is not legal advice | Priya Raghunathan, API platform lead |
| API request logs | 90 days (ILLUSTRATIVE) | Rolled off automatically | Choice, sized to the incident-investigation window | Platform engineering lead |
| Audit logs of sensitive actions (key creation, rotation, scope change) | 13 months (ILLUSTRATIVE) | Deleted on a scheduled job | Policy | Priya Raghunathan, API platform lead |
| Deprecation and change notices sent to registered developers | Life of the API version plus 12 months (ILLUSTRATIVE) | Deleted with the version's documentation set | Choice, so a late migrator can find the announcement | Developer-relations lead |

## 7. Operability

| Requirement | Target or owner | Verified by |
|---|---|---|
| Observability: logs, metrics, traces for core flows | Requests, error rate split by status class, per-key usage, latency percentiles in production at launch; detail in the product's observability document (not included in this standalone example) | Observability review before each release train |
| Feature kill or rollback path | Per-route flag; disable time under 5 minutes for a new route, under 30 minutes for a rate-limit or validation change (ILLUSTRATIVE) | Rollback drill, quarterly |
| Support handover | Runbook for the `/v1/orders` deprecation and the 429 path in the support knowledge base; owned by developer relations | Runbook review 2026-10-02 (ILLUSTRATIVE) |
| Error contract for rate limiting | Breach of the 50 req/s per-key limit returns HTTP 429 with a `Retry-After` header, not a hard failure; enterprise keys registered by key ID get a 5 s burst allowance at 2x limit per the capacity doc (ILLUSTRATIVE) | Load test before each quarterly capacity review; production p99 sampled continuously |
| Deprecation visibility | Usage by API version, readable per key, so the share of active keys still on a deprecated version is queryable at any time, not only at the 90-day mark | Usage query in the platform console; verified by the platform PM |
| Notice reachability | Registered developers receive changelog and deprecation notices by email; the contact list is maintained at registration and re-confirmed annually | Email log; annual re-confirmation run |
| SDK support window | Each official SDK version is supported for 12 months from its release, or until its matching API version is decommissioned, whichever is later; an SDK release cadence of at least one per quarter (ILLUSTRATIVE) | SDK release calendar; support-window check at each release |
| Sandbox parity | The sandbox environment runs the same behaviour as production for validation, error codes and rate-limit responses; a parity test runs before each production release, and any intentional difference is listed in the docs (ILLUSTRATIVE) | Sandbox parity test in the release checklist |

The deprecation itself is a delivery programme, not an announcement: the card's question 7 asks whether you can see who is still calling the old path and can reach them. The `Deprecation visibility` and `Notice reachability` rows are the two mechanisms that answer it, and the adoption measure below is how the programme is judged.

### Adoption measure

The share of active keys still on `/v1/orders` at 90 days after the deprecation announcement is the adoption measure for this change (ILLUSTRATIVE). Target: at or below 40% of active keys at day 90 (ILLUSTRATIVE). This is read per key, not as an aggregate percentage alone, because the card warns that aggregates hide the tail and the tail is where the outage will be; every key above the target is named and contacted by developer relations.

## 8. Waivers

| Requirement waived | Waived by | Reason | Revisit date |
|---|---|---|---|
| None | n/a | No waiver recorded at this revision. The deprecation window, the per-key rate limit and the sandbox parity rule below are all in force. | n/a |

### Rule carried in this section: lowering a limit is itself a breaking change

Lowering a per-key rate limit, or shortening the deprecation window once announced, is a breaking change under this NFR set even though no field name, status code or response shape moves. A client written against the documented contract can stop working because a change of this kind ships, which is the definition the domain card uses. Any such change therefore follows the same path as a schema change: a changelog entry, notice to registered developers, and the full deprecation window where one applies. The card's question 1 lists "a rate limit lowered" among the things that count as breaking; this section is that rule written where the limits live.

---

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every row has a number or a named owner and date for the number. Every row in sections 1 to 7 carries a number marked ILLUSTRATIVE.
- [x] No adjective survives without a measurement ("fast", "secure", "scalable" all resolved). Availability is 99.9% monthly, the write path is 400 ms at p95, and capacity has a "breaks at" number rather than the word "scalable".
- [x] Unagreed numbers are labeled ILLUSTRATIVE. Every figure in this file is labeled ILLUSTRATIVE, since none is yet agreed with its owner.
- [x] Every row names its verification artifact. Load tests, drill reports, audits, parity tests, the status page record and the runbook review.
- [x] Scale table includes a "breaks at" estimate from engineering. Section 3 carries platform engineering's estimates: 6,000 req/s aggregate for the write path and 250 million order records in the hot store.
- [x] Retention table covers every data class in the data model. Section 6 covers idempotency keys, order records, request logs, audit logs and deprecation notices; the classification of these classes lives in the product's data model document (not included in this standalone example).
- [x] All waivers are recorded here with a revisit date. Section 8 records no waivers.

Signed at Gate 2, 2026-09-11: Priya Raghunathan, API platform lead (owner and first verifier). Co-verifier: Marcus Oyelaran, developer-relations lead, who owns the adoption measure in section 7 and the notice reachability row, since a deprecation promise that cannot be delivered to a named developer is not a promise.
