# Integrations Register: Fernbridge Core Platform

Fills [templates/architecture/integrations.md](../templates/architecture/integrations.md). Everything here is invented: Fernbridge Finance is a fictional embedded-finance platform offering accounts and cards to software companies under a sponsor bank's licence, Petra Novak is its fictional integrations lead, and every name, number and date is ILLUSTRATIVE. See the [examples index](README.md).

**Owner:** Petra Novak, integrations lead · **Date:** 2026-08-14 · **Status:** Draft, for Gate 3 review

## 1. Register

| # | Counterparty system | Direction | Protocol | Auth | Counterparty SLA (and source) | Owner (ours) | Failure behavior (one clause) |
|---|---|---|---|---|---|---|---|
| I-3 | Fictional Sponsor Bank Co, programme ledger API | Outbound, real-time | REST over TLS | mTLS client cert, sponsor-issued | 99.9% monthly, sponsor programme agreement schedule 4 (ILLUSTRATIVE) | Programme Ops lead | A ledger-API outage freezes new account opening and card issuance immediately; existing balances stay visible read-only from the sponsor's own status feed, never inferred locally, because only the sponsor's ledger is the record of a customer's funds |
| I-4 | Fictional Sponsor Bank Co, compliance review queue (human) | Inbound | Email and secure document portal | Sponsor-issued credentials, two-factor | 10 business days for standard programme changes, 20 business days for structural changes, per sponsor programme agreement, article 9.2 (ILLUSTRATIVE) | Product counsel | The sponsor holds unilateral authority to suspend the entire programme for non-compliance or risk-appetite breaches; when the queue times out, the roadmap stops, not the platform |
| I-5 | Fictional Card Processor Inc, card issuance API | Outbound, real-time | REST over TLS | API key and HMAC signature | 99.5% monthly, processing agreement schedule B (ILLUSTRATIVE) | Payments engineer | Issuance halts and existing-card authorizations degrade to declined if the processor's authorisation endpoint is unreachable; card status is cached for 24 hours only, never longer |
| I-6 | Fictional KYC Vendor Ltd, identity verification API | Outbound, real-time | REST over TLS | API key and IP allow-list | 99.9% monthly, vendor MSA schedule 1 (ILLUSTRATIVE) | Trust and safety engineer | New account applications are queued up to 24 hours and then rejected with a generic "try again tomorrow" message; existing customer data is not verified in-flight, preventing a mass freeze on existing accounts if the vendor degrades |
| I-7 | Fictional Sponsor Bank Co, ACH origination | Outbound, batched | SFTP and REST hybrid | Sponsor-issued SFTP credentials | NACHA settlement windows enforced by sponsor; submission cutoffs at 17:00 Eastern for same-day, next-day otherwise, sponsor operational runbook v4 (ILLUSTRATIVE) | Payments engineer | Failed submissions are queued locally for retry into the next window; customers see a pending status, never an immediate failure message, because settlement timing is the sponsor's operational constraint, not ours |
| I-8 | Fictional Dispute Operations, chargeback intake | Bidirectional | REST webhook | Shared secret, verified HMAC | Resolution clock: 15 days to file a response, set by card network rules (Visa Core Rules, ILLUSTRATIVE timing example) | Trust and safety ops | If the intake endpoint fails, disputes are held in a local queue; missing the network's filing deadline due to our queue backlog is a direct financial loss to the sponsor, who then holds it against our programme volume limit |

## 2. Detail block, one per row

### Integration I-3: Fictional Sponsor Bank Co, programme ledger API

- Purpose: Reads the authoritative balance for every embedded customer account and writes the entry for every new account open and card issuance. Only the sponsor's ledger records the customer's funds; our system holds a projection.
- Data exchanged: Account identifier (our internal), balance in cents, ledger transaction timestamp, account status. PII class: Internal identifier linked to KYC record; no PII crosses this boundary directly.
- Environments: Sandbox available, sponsor-issued. Production credentials held by Platform Security, rotated every 90 days.
- Failure behavior, expanded: When the ledger API is unreachable or returning errors, the product immediately blocks new account opening and card issuance. The user flow for these actions returns a specific error: "We are currently unable to open new accounts. Please check back soon." Existing accounts show the last known balance with a timestamped note "Balance last updated: <time>. Live data temporarily unavailable." This state is visible; it is not hidden by a spinning loader.
- Backoff and retry policy: Exponential backoff on 5xx and timeouts, 2 seconds base, 60 seconds max, 5 retries max. Idempotency key: the internal account-open request ID, sent as a header; the sponsor deduplicates on it.
- Monitoring: PagerDuty alert "Ledger-Read-Failure-Rate > 5%" on 5-min window, fires to Programme Ops lead and SRE on-call.
- Counterparty contact: Sponsor's programme technical support channel, named contact: David Aronson, 2-hour acknowledgement SLA per schedule 4, clause 2.3.
- Contract or DPA reference: Sponsor programme agreement, schedule 4 (technical schedules); data processing addendum covers ledger data, no direct PII.
- Change notice: Sponsor announces breaking changes via secure email to integration owners, 60 days for schedule 4 changes, 30 days for non-breaking. Integration owner and Product counsel monitor.
- Sponsor authority and customer communication: The sponsor, as licence holder, may unilaterally suspend this API (and the entire programme) if risk limits are breached (e.g., outstanding balances exceed the USD 40M programme limit per programme agreement schedule 3) or if regulatory findings require it. When this API is down, it is the licence-holder's system, not Fernbridge's, that is the point of failure. The support script for end customers states verbatim: "Your funds are safe. The bank's systems are temporarily unavailable, so we cannot update your live balance or open new accounts right now. We are working with our banking partner to restore service." This text is not paraphrased, because a paraphrase could imply Fernbridge holds the funds.

### Integration I-4: Fictional Sponsor Bank Co, compliance review queue (human)

- Purpose: Submits new product features, rate changes, and partner integrations to the sponsor's compliance and risk teams for review and written approval before launch, as required by the programme agreement.
- Data exchanged: Feature specification documents, customer flow screenshots, risk assessments, updated terms and conditions. PII class: None, as submissions are sanitized to fictional test data.
- Environments: No sandbox. Production portal only, with access tied to two named individuals.
- Failure behavior, expanded: The "integration" fails if the 10-day SLA lapses without approval, or if the sponsor requests a revision and the clock resets. The consequence is a launch delay, not a runtime error. Our system does not degrade; our roadmap does.
- Backoff and retry policy: Not applicable. The escalation path is a named contact within the sponsor's programme office, followed by a call to the sponsor's relationship manager if the SLA breaches by 2 business days.
- Monitoring: A weekly report to Product counsel and the CPO lists all open requests, their age against SLA, and the last action item. Breach of SLA is logged in the partner risk register.
- Counterparty contact: Compliance review queue intake, named human contact: Elena Rodriguez, response SLA as above; escalation: Sponsor's Chief Risk Officer, via relationship manager.
- Contract or DPA reference: Sponsor programme agreement, article 9.2 (programme changes).
- Change notice: The sponsor can change its review criteria, the queue SLA, or the list of what requires pre-approval, by giving 30 days' notice in writing. Product counsel and the Head of Product monitor.
- Sponsor authority and customer communication: The sponsor's approval of a feature is a condition of the licence. The sponsor holds the unilateral right to suspend the programme for compliance reasons, irrespective of this queue's SLA. When this "system" is down (i.e., the review queue is stalled), the end customer is not told anything, because the failure is internal to the programme's development process. The risk is that the launch never happens, and the roadmap silently fails, a risk tracked internally, not exposed to the customer.

### Integration I-5: Fictional Card Processor Inc, card issuance API

- Purpose: Requests physical and virtual card issuance and manages card status (block, unblock, replace). The processor holds the cardholder records and PANs.
- Data exchange: Internal account identifier, card type, PAN (last 4 only in our system), issuance status, activation status. PII class: PAN fragment and cardholder name, handled under PCI DSS scope; our integration handles PAN only in transit, never at rest.
- Environments: Sandbox available, provided by the processor. Production credentials in our secrets vault.
- Failure behavior, expanded: If the issuance API is down, new card orders fail with a user-facing error: "We cannot issue your card right now. Try again in 15 minutes." If the authorisation endpoint is unreachable, transactions on existing cards are declined by the network. Our platform cannot prevent this decline. Card status (active/blocked) is cached client-side for a maximum of 24 hours to allow continued display; stale status is labelled with a datestamp.
- Backoff and retry policy: For issuance, 3 retries with 5-second fixed delay. For status read, cache-first. Idempotency: an internal order ID sent as metadata.
- Monitoring: Alert if issuance API error rate >10% in 10-min window, or if the "last successful authorization check" heartbeat from the processor's status feed fails for >2 minutes.
- Counterparty contact: Processor's 24/7 technical support line and ticket queue. Escalation path per vendor MSA, 4-hour response for Sev-1.
- Contract or DPA reference: Processing agreement, schedule B (SLA and technical specs); DPA covers PAN as PII under GDPR/UK GDPR.
- Change notice: Processor provides 90-day notice for breaking API changes via developer portal and direct email to integration owner. Payments engineer monitors.
- Sponsor authority and customer communication: Card issuance is a regulated activity under the sponsor's licence. If the sponsor directs the processor to stop all issuance for a programme (due to fraud or compliance breach), that instruction bypasses our integration. Our platform will see issuance requests begin to fail. The customer will see the issuance failure message. The sponsor's authority is absolute; processor uptime SLAs do not protect against a sponsor-mandated stop.

### Integration I-6: Fictional KYC Vendor Ltd, identity verification API

- Purpose: Verifies the identity of a new applicant for an account or card by checking documentary and biometric data against data sources, producing a decision.
- Data exchanged: Applicant name, date of birth, address, document images, liveness selfie. PII class: Full PII, sensitive data (biometric). This integration defines our PII surface.
- Environments: Sandbox with test data only. Production credentials held by Trust and Safety, accessed via our secure gateway.
- Failure behavior, expanded: If the vendor API is unreachable, the account application flow does not proceed. Applicants see: "We are unable to verify your identity at this moment. Please try again tomorrow." Applications are held in a pending-verification queue for up to 24 hours, with a single retry, then auto-cancelled with a request to reapply. This design prioritises not mass-blocking existing customers (verification happens only at onboarding) over completing every new application.
- Backoff and retry policy: One retry after a 10-second delay. After that, the application is failed. Idempotency: an internal application ID is used; re-submission reuses that ID and skips the data re-collection steps.
- Monitoring: Alert if verification failure rate exceeds 15% in 15-min window, or if average decision latency exceeds 10 seconds.
- Counterparty contact: Vendor support, with a named technical account manager. Sev-1 escalation within 1 hour per MSA.
- Contract or DPA reference: Vendor MSA, with a DPA that covers PII processing in a jurisdiction we control.
- Change notice: Vendor notifies 45 days ahead for integration-affecting changes via email and developer portal update.
- Sponsor authority and customer communication: The sponsor bank specifies the KYC vendor and the acceptable identity verification standards (as a condition of programme compliance). If the sponsor changes vendors, or rejects the vendor's decision methodology mid-programme, the integration must be replaced. This is a programme-level risk. When the vendor is down, the customer-facing message must not say "KYC systems are down" but rather "Unable to verify identity," as the vendor's specific outage is not the customer's concern. The sponsor requires we do not disclose the vendor's identity.

### Integration I-7: Fictional Sponsor Bank Co, ACH origination

- Purpose: Submits batches of ACH transactions (debits and credits) to the sponsor's originating server for settlement within the NACHA rules.
- Data exchanged: Batch files (ACHN format) and status response files. PII class: Internal account identifiers and amounts.
- Environments: Test file submission available via SFTP. Production credentials: SFTP keys in secrets vault, with a break-glass process.
- Failure behavior, expanded: A file submission can fail on format validation, on cutoff window breach, or on connection failure. If a connection fails, the file is queued for retry. If the file is rejected, we parse the response, correct locally, and resubmit in the next window. The user sees transaction status as "Pending" until the settlement response confirms, which can be the next business day.
- Backoff and retry policy: Retry failed submissions up to 3 times in the next window. Idempotency: a unique trace ID per batch, acknowledged by the sponsor.
- Monitoring: Alert if a submission response file is not received within 2 hours of the cutoff. Alert if any transaction in a batch is returned as "Reject."
- Counterparty contact: Sponsor's operational payments support team, email, with a 4-hour acknowledgement SLA during business hours.
- Contract or DPA reference: Sponsor programme agreement, schedule 2 (operational and settlement).
- Change notice: Sponsor can change cutoffs or file formats with 60 days' notice for a major change, 10 days for minor, per schedule 2.
- Sponsor authority and customer communication: The sponsor controls ACH access and can suspend our origination privileges if volume limits or dispute ratios are breached. An ACH suspension is a programme event. When the sponsor's ACH processing is down or a window is missed, customers see their transfer as "pending" for an extra business day. The support message: "Your transfer is being processed. Bank processing can take up to two business days." This is true and does not assign blame.

### Integration I-8: Fictional Dispute Operations, chargeback intake

- Purpose: Receives chargeback notifications from the card network via our dispute operations partner, who then feeds them to our case management; also submits representment responses.
- Data exchanged: Dispute case ID, account identifier, amount, reason code, submission documents. PII class: Customer name, transaction details, PII contained in evidence documents.
- Environments: Test notifications available in sandbox. Production API in our trust and safety platform.
- Failure behavior, expanded: If the inbound webhook fails, we miss the network's dispute notification. This risks missing the response deadline, causing an automatic financial loss. We poll for disputes every 4 hours as a fallback. If the outbound representment API is down, evidence is queued locally and a "manual submission required" flag is set for the case manager, who uses a portal.
- Backoff and retry policy: For inbound, no retry (we poll). For outbound, 5 retries over 1 hour. Idempotency: dispute case ID.
- Monitoring: Alert on any webhook error or if polling reveals a dispute not captured by webhook. Alert on outbound queue backlog >30 minutes.
- Counterparty contact: Dispute operations partner, named account manager, and shared Slack channel for real-time escalations.
- Contract or DPA reference: Service agreement, with a DPA covering customer PII in dispute evidence.
- Change notice: Partner notifies 30 days ahead of breaking changes or new card network rule deadlines, per card network rules (Visa Core Rules, Mastercard Operating Rules as of 2026-09-11, ILLUSTRATIVE reference to the current rulebook cycle, confirm with counsel).
- Sponsor authority and customer communication: The sponsor bank, as the issuing bank, is the party ultimately responsible for the dispute resolution process under the card network rules. If the dispute ratio becomes too high, the sponsor can suspend new card issuance or close the programme. When the dispute intake is down, no direct customer communication occurs; the internal risk is missing the network deadline, which harms the sponsor's compliance record, not the customer's experience directly.

## 3. Failure drill

- If every outbound integration failed at once, the user could still: see a last-known cached balance (I-3 read, with a timestamp and "data unavailable" note), view their existing card's details (I-5 cached status), and contact support through Fernbridge's own website. New account opening, card issuance, and identity verification for new users would all fail.
- The integration whose failure hurts most is I-4 because its failure is silent and total. A human compliance queue outage does not show up in an uptime dashboard, does not trigger a technical incident, but halts all product changes indefinitely. Its risk mitigation is the weekly compliance queue report and an accepted risk register row for sponsor-approval delay risk, tracked in Fernbridge's risk register (not included in this standalone example).

## Exit gate

- [x] Every boundary line in the solution architecture one-pager has a register row. Verified against architecture diagram v2 (not linked), which shows Sponsor Ledger, Compliance, Processor, KYC, ACH, Dispute.
- [x] Every row has a named owner on our side. Yes: Programme Ops lead, Product counsel, Payments engineer, Trust and safety engineer, Payments engineer, Trust and safety ops.
- [x] Every SLA cites its source document, not a recollection. All rows cite the sponsor agreement, vendor MSA, or processing agreement schedules.
- [x] Every detail block states failure behavior a user would recognize. The "Purpose" and "Failure behavior" in each detail block describe user-visible states: balance view blocked, new applications stopped, transactions declined, status "pending".
- [x] Retry policies name their idempotency mechanism. Yes: account-open request ID, order ID, internal application ID, trace ID per batch, dispute case ID.
- [x] Every integration with no contract or DPA reference has a risk register row. All rows have a contract reference; this check passes vacuously.
- [x] The worst-single-failure answer in section 3 is written and its mitigation linked. Section 3 names I-4 and links to the accepted risk in the risk register.

Signed by Petra Novak, integrations lead, on 2026-08-14, for Gate 3 review.
