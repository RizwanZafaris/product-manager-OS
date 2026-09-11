# Support Runbook: Harbourgate payment tickets

Fills [templates/delivery/support-runbook.md](../templates/delivery/support-runbook.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and pound is ILLUSTRATIVE, drawn from the [Harbourgate journey](harbourgate-journey.md) and the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md).

**Owner:** Callum Fraser, Support Lead · **Date:** 2026-07-10 · **Status:** Approved as condition C2; maintained through OPERATE
**Support lead who reviewed it:** Callum Fraser · **Next review:** 2026-11-16, when BR-009 begins

## 1. What this feature does, for a responder

- What it does, in one sentence: Harbourgate takes card payments on the web, in the app and at shop kiosks through Quay and Kestrel, records the payment outcome against the order, and gives support a reason class for declines.
- Surfaces it appears on: web store, app and kiosk PIN pad. The kiosk fallback is the customer message "pay at the till".
- Identifier to ask the customer for: the order id, shown on the order confirmation and available in the customer's order record.
- Where that identifier is looked up: use the order id as the lookup key in the payment record and decline event stream, following [harbourgate-observability.md](harbourgate-observability.md) section 3.
- Who has it: Harbourgate customers using the web store, app or one of the 61 shop kiosks. The payment path is revenue-critical, Tier 1, per HC14.

This runbook covers customer payment tickets. It is separate from the finance close runbook, DEP-3, which covers daily reconciliation and close.

## 2. Symptoms

| # | Symptom, as the customer reports it | Likely cause | First check | Workaround or answer | Escalate if |
|---|---|---|---|---|---|
| S-1 | "declined" | The authorisation was declined, with a provider reason class recorded in the decline event stream | Look up the order id. Confirm the payment outcome, provider and reason class. Check whether the same card was already submitted | Offer one retry with a different method. Do not re-submit the same card automatically, per BR-001 | The decline cannot be found, has no provider or reason class, the customer was charged, or the same card was submitted more than once |
| S-2 | "charged twice" | A duplicate authorisation, or an authorisation hold that has not yet been voided | Look up the order id and compare authorisation, capture and void records. Check whether an authorisation was left without dispatch for 24 h | Explain whether one entry is an authorisation hold. Under BR-006, an authorisation for an order not dispatched within 24 h is voided rather than captured. Do not promise that a bank will remove a pending hold immediately | Any duplicate capture is present, the hold is not voided after the relevant 24 h period, or the payment records disagree |
| S-3 | "pay at the till" | A kiosk payment call returned no outcome within 10 s | Look up the order id and kiosk payment outcome. Confirm the shop and whether the basket is still held | Tell the customer to pay at the till. The basket is held for 30 minutes under BR-004 | A shop reports repeated failures, the fallback does not appear within 10 s, or a group of shops is affected |
| S-4 | "asked to verify" | Step-up authentication was required because the card-not-present order exceeded £250 or a fraud rule flagged it | Look up the order id and check the step-up result and the order amount | Explain that verification is required for the payment. Ask the customer to complete the verification shown, or retry with a different method if it cannot be completed | Step-up was requested for an order that did not meet BR-005, the challenge loops, or multiple customers cannot complete it |
| S-5 | "where is my refund" | The refund is still within the applicable route or has been sent to the original provider | Look up the order id and confirm the authorising provider, refund status and refund request date | For a legacy-authorised order through 2026-11-15, explain that BR-002 routes the refund to the provider that authorised the order. From 2026-11-16, BR-009 requires Finance Operations to refund through the provider portal within 5 working days | The refund is not routed to the original provider, the 5 working day period has passed under BR-009, or the order cannot be matched |

## 3. Diagnosis steps

### Symptom class: declined

1. Ask for the order id and open the payment record and decline event for that order.
2. Confirm the provider, reason class and trace id. A decline at entry may lack a reason class only where the record is incomplete. At Gate 6, 100% of declines carried provider and reason class.
3. Check whether an authorisation or capture exists. Do not treat a decline as proof that no money movement occurred until the payment record is checked.
4. Offer one retry with a different method. Never automatically re-submit the same card, per BR-001.
5. Decision: resolve with the different-method retry, or escalate with the order id, payment outcome, provider, reason class and trace id.

### Symptom class: charged twice

1. Ask for the order id and open all authorisation, capture and void events for that order.
2. Distinguish a pending authorisation hold from a duplicate capture. Check whether the order was dispatched and whether the authorisation reached the 24 h void condition in BR-006.
3. If one entry is an authorisation hold and no duplicate capture exists, explain the hold and record the ticket for monitoring. If the order was not dispatched within 24 h, confirm that the authorisation was voided.
4. If two captures exist, do not promise a refund or a bank release time. Escalate with the evidence below.
5. Decision: resolve by explaining the hold, apply the BR-006 outcome, or escalate as a possible duplicate charge.

### Symptom class: pay at the till

1. Ask for the order id and the shop where the customer used the kiosk.
2. Check whether the kiosk received an outcome within 10 s and whether the basket is held.
3. If there was no outcome within 10 s, confirm that "pay at the till" was the expected BR-004 fallback and that the basket was held for 30 minutes.
4. If more than one shop reports the symptom, treat it as a service issue rather than a single-customer ticket.
5. Decision: resolve with the till instruction, or escalate with the order id, shop and kiosk outcome.

### Symptom class: asked to verify

1. Ask for the order id and open the payment record.
2. Check whether the card-not-present order exceeded £250 or whether a fraud rule flagged it, the two BR-005 triggers.
3. Confirm whether the step-up challenge was presented and whether it completed or failed.
4. Do not tell the customer that the verification was caused by a confirmed fraud finding. State only that additional verification was required for the payment.
5. Decision: resolve by completing verification or choosing a different method, or escalate with the order id and step-up result.

### Symptom class: where is my refund

1. Ask for the order id and refund request date.
2. Confirm which provider authorised the order and whether the order is inside the returns window. The returns policy is 90 days from delivery.
3. For a legacy-authorised order through 2026-11-15, confirm that BR-002 sent the refund through the original provider. From 2026-11-16, route the request to Finance Operations for the provider portal under BR-009.
4. From 2026-11-16, explain that Finance Operations processes the provider-portal refund within 5 working days. Do not describe a portal refund as an immediate card credit.
5. Decision: resolve with the current refund status, apply the BR-009 route, or escalate when the refund is beyond 5 working days or the provider route is wrong.

**Evidence to collect before escalating**

| Item | Where to find it | Why engineering needs it |
|---|---|---|
| Order id | Customer order confirmation and order record | The order id is the lookup key across the payment record and event stream |
| Payment outcome, provider and reason class | Payment record and decline event stream | Separates a decline, an authorisation hold, a capture and a missing event |
| Trace id | Decline event stream | Joins the customer report to the payment request |
| Authorisation, capture and void status | Payment record | Distinguishes a pending hold from a duplicate charge and verifies BR-006 |
| Refund request date, authorising provider and refund status | Order and refund records | Confirms BR-002 or BR-009 routing and whether 5 working days have elapsed |
| Kiosk shop and outcome timing | Kiosk payment record and the order id | Shows whether the 10 s BR-004 fallback was reached and whether one shop or a group of shops is affected |
| Step-up result and trigger | Payment record and fraud event | Shows whether BR-005 applied and whether the challenge completed |
| Customer wording and a screenshot, where available | Ticket record | Preserves the symptom as reported and helps reproduce the customer-visible result |

## 4. Escalation

Support severities are from HC18.

| Severity | Definition for this feature | Escalate to (name) | How (channel, pager) | Expected first response | What to include |
|---|---|---|---|---|---|
| Sev 1 | No customer can pay on a surface | Payment on-call, then Bea Lindqvist at 15 minutes and Tomasz Wierzbicki at 30 minutes | Page the payment on-call | 15 minutes | Section 3 evidence, affected surface, customer or shop scope, and whether the issue is web, app or kiosk |
| Sev 2 | One provider's cohort or a group of shops is affected | Bea Lindqvist, with Tomasz Wierzbicki if the issue needs a service decision | Payment on-call escalation | 1 hour | Section 3 evidence, affected provider or shops, start of impact and customer scope |
| Sev 3 | One customer is affected | Callum Fraser for support triage, Bea Lindqvist for payment investigation | Support ticket escalation to the payment on-call route | Next working day | Section 3 evidence and the customer's exact symptom |

**After hours:** Sev 1 is paged to the payment on-call. The on-call rotation is the squad's five engineers. A page is acknowledged within 5 minutes, escalates to Bea Lindqvist at 15 minutes and to Tomasz Wierzbicki at 30 minutes. Sev 2 and Sev 3 follow the same named escalation path when their response expectation falls due.

**Product owner for "bug or design choice" questions:** Ife Adeyemi, Product Manager, through the product decision path. Support should not decide whether a new customer-facing rule is a bug fix or a design choice.

## 5. Known issues

| Id | Issue | Who is affected | Workaround | Approved wording (macro id or customer-comms.md link) | Fix owner | Fix date | Source |
|---|---|---|---|---|---|---|---|
| KI-1 | Reason class "other" appeared on 6% of Kestrel declines. The mapping fix reduced this to 1.5% on 2026-08-14; the remainder is triaged by hand | Customers whose decline is classified as "other" | Offer one retry with a different method. Do not re-submit the same card automatically | "Your payment was not approved. Please try a different payment method. We can investigate the order if you share the order id." | Bea Lindqvist | 2026-08-14 for the mapping fix; the remaining 1.5% is tracked as TD-3 | [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md), KI-1 and N62 |
| KI-2 | The straddle set had not yet met a live settlement cycle at release | Support and finance investigating a payment that crossed the provider transition | Do not infer a missing payment from one provider view. Use the order id and payment record, then keep the ticket open for reconciliation | "We are checking the payment across the records that processed it. We will update you when the payment status is confirmed." | Bea Lindqvist | Closed 2026-07-16 | [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md), KI-2 and ADR-0004 |
| KI-3 | Marlowe support is a ticket queue only, with a 4 hour committed response | Tickets requiring the legacy Marlowe provider before its contract ends | Record the Marlowe ticket reference and do not promise an immediate provider response | "We have sent the payment query to the provider's support queue. We will update you when they respond." | Bea Lindqvist | 2026-12-15, when the contract ends | [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md), KI-3 and N69 |
| KI-4 | Legacy-authorised refunds are manual through provider portals, within 5 working days | Customers requesting a refund for a legacy-authorised order from 2026-11-16 to 2027-06-15 | Route the request to Finance Operations under BR-009. Use the order id and confirm the 5 working day expectation | "Your order was authorised on a legacy provider. Finance Operations will process the refund through the provider portal within 5 working days." | Priya Raman | From 2026-11-16 to 2027-06-15 | [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md), KI-4 and BR-009 |

## 6. What support may and may not say

- May confirm: the payment status shown in the payment record, the provider and reason class when recorded, whether a payment was captured or voided, and whether a refund has been routed or completed.
- May offer: one retry with a different payment method under BR-001, the "pay at the till" workaround under BR-004, investigation using the order id, and escalation with the evidence in section 3.
- May not promise: that a pending authorisation hold will disappear immediately, a fix date not stated in section 5, a refund above the support authority, a successful refund before Finance Operations confirms it, or a root cause that has not been confirmed.
- Anything involving personal data or a regulator: route to Anneliese Vogt, Legal Counsel and Data Protection Officer, through the compliance path. Share only the information needed to investigate the order.

Support must not describe an authorisation hold as a captured duplicate without checking the payment record. Support must not send a customer to finance close for a payment-ticket investigation. DEP-3 is the separate finance close runbook.

## 7. Maintenance

- Reviewed after every incident touching this feature: yes, by Callum Fraser with Bea Lindqvist.
- Rows added from postmortems since launch: 0; HG-INC-14 is covered by the existing payment diagnosis and escalation paths.
- Retired rows: none. KI-1 remains visible after the 2026-08-14 mapping fix, KI-2 remains as historical evidence of the live-cycle limitation, KI-3 remains until 2026-12-15, and KI-4 becomes active on 2026-11-16.

## Exit gate (feeds Gate 5: release readiness green)

A reviewed runbook satisfies the "runbook for it exists" line at Gate 5 and the support row in section 6 of [harbourgate-release-readiness.md](harbourgate-release-readiness.md).

- [x] Every symptom row is written in the customer's words and ends in a workaround or an escalation rule
- [x] Every diagnosis path ends in a decision, and the evidence list exists
- [x] Every escalation row names a person, a channel, and an agreed response expectation
- [x] Every known issue from the readiness document is here with a workaround and approved wording
- [x] The support lead has read it and is named above
- [x] A next review date is set
- [x] Signed by Callum Fraser, 2026-10-16
