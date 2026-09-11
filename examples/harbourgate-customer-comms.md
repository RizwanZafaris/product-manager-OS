# Customer Comms: Harbourgate checkout cutover

Fills [templates/delivery/customer-comms.md](../templates/delivery/customer-comms.md). Everything here is invented: Harbourgate is a fictional mid-market retailer, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is the journey's fictional cast, and every number, date, amount, rate and identifier is ILLUSTRATIVE, taken from [harbourgate-journey.md](harbourgate-journey.md) or its supplement [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md) and never to be quoted as a benchmark. See the [examples index](README.md).

**Owner:** Ife Adeyemi, Product Manager · **Date:** 2026-07-10 · **Status:** Approved for Marlowe cohort 1 (2026-07-13); the Marlowe email and the Marlowe status-page text are now published or spent and the shopper notice they carried stands as the record. Reusable wording for the Tidewater store cohorts and the Kestrel legacy connector cohorts is drafted here and re-approved per cohort; the HG-INC-14 rows are the incident messaging as it ran, filed after the fact.

## 1. Facts every message derives from

Two event types are in play. The cutover is a provider-by-provider traffic shift (D-021, N71), and its shoppers saw no visible change (coverage reconciliation note 7), so its customer-facing message is a quiet in-app and merchant-channel notice. HG-INC-14 is an incident with no customer impact, so its message was an internal one. The rows below are per message, and the facts block is copied from [harbourgate-journey.md](harbourgate-journey.md); nothing is retyped here.

| Field | Value |
|---|---|
| Event type | Cutover freeze / traffic shift (Marlowe cohort 1, 2026-07-13); incident (HG-INC-14, 2026-06-15) |
| What is true for the customer, in one sentence | Shoppers: nothing changes, you pay the same way you pay today. Merchants and internal teams: card payments on the web and app will move behind the scenes from one card provider to another (Kestrel), in small groups of orders, and the way a payment looks behind the scenes changes, not the way a customer pays |
| What they must do, if anything | Shoppers: nothing. Store associates: nothing during the Marlowe shift (kiosks were not touched until the Tidewater cohorts, first 2026-08-03, N71); during a store cohort, use the kiosk as normal and follow the printed "pay at the till" card only if it appears |
| When | Marlowe cohort 1 5% flagged at 10:00 Europe/London on 2026-07-13 (N71, HC25); cohort 2 50% 2026-07-16; cohort 3 100% 2026-07-20, the day BR-008 was retired (N71; BR-008 retired 2026-07-20). Kiosk fallback (BR-004): "pay at the till" shown within 10 s of a failed call, basket held 30 minutes (N31, target) |
| Who is affected | Shoppers: all, no visible change. Merchants/finance: the Marlowe cohort's orders and their settlement and refund paths. Stores: none at cohort 1 |
| Source document | [harbourgate-migration-cutover-plan.md](harbourgate-migration-cutover-plan.md) (v2, D-021) and [harbourgate-release-readiness.md](harbourgate-release-readiness.md) section 1; for the incident, [harbourgate-incident-postmortem.md](harbourgate-incident-postmortem.md) |

## 2. Approval chain

One row per message, as it actually ran. Legal or compliance is named wherever a message touched money, personal data or a settlement file.

| Message | Drafted by | Reviewed by (support, product, legal or compliance where needed) | Approved by | Approved on |
|---|---|---|---|---|
| In-app (web/app checkout) | Ife Adeyemi with Ines Castellanos (design line) | Callum Fraser (support) | Ife Adeyemi | 2026-07-08 |
| Email (merchant-facing) | Ife Adeyemi | Priya Raman (finance operations, reconciliation impact), Anneliese Vogt (legal, data-processing on Marlowe's in-transit card number, I-5), Callum Fraser (support), Hamid Qureshi (compliance, PCI scope during the drain, N55) | Anneliese Vogt | 2026-07-08 |
| Status page (maintenance) | Bea Lindqvist (on-call lead, owner of the integrations register) | Callum Fraser (support), Tomasz Wierzbicki (service owner, abort authority) | Ife Adeyemi | 2026-07-08 |
| Status page (HG-INC-14, 2026-06-15) | Callum Fraser (support), drafted from the finance analyst's report | Bea Lindqvist (incident owner, N41), Hamid Qureshi (compliance, card data in transit) | Anneliese Vogt | 2026-06-16 (post-event, severity 3) |
| Internal announcement (2026-10-19) | Ife Adeyemi | Priya Raman, Callum Fraser | Rohan Iyer (sponsor) | 2026-10-16 |

## 3. In-app message

- Trigger and placement: a banner on the web checkout payment step and the app payment step, shown only for orders routed on the Marlowe path before the shift (the pre-shift cohort), so a shopper who saw it is one whose order is about to move. The app banner and the web banner render from the same component.
- Audience rule: the per-provider routing flag (D-017), Marlowe, on the pre-shift order-id hash bucket; NOT shown once that order is authorised through Quay/Kestrel, and never shown at the kiosk, since kiosks were not shifted at this cohort (N71).
- Shows from: 2026-07-13 (the cohort 1 flag flip, 10:00 Europe/London, HC25) · Stops: 2026-07-20, the day Marlowe reached 100% and BR-008 was retired (N71)
- Text: "We're updating how we process your card payment. Your card, your basket and the price you see are unchanged. If your card is declined you will be asked to try a different card; the same card is never charged twice. [Learn what is changing](../templates/delivery/customer-comms.md)"
- Dismissal and frequency: dismissible, once per session, and it stops showing at cohort 3 regardless. Decline messaging follows BR-001 (offer one retry with a different method, never re-submit the same card automatically) and AC-5; the kiosk "pay at the till" screen is a separate component and is governed by BR-004, not by this banner.

## 4. Email

Merchant-facing, because a traffic shift changes how a payment looks behind the scenes (settlement reference, refund rail) without changing how a shopper pays. It was approved on 2026-07-08 (Gate 5 attempt 2) and sent ahead of the first send window.

- Segment and list source: the merchant operations contact list and the finance weekly distribution, pulled by Priya Raman's finance operations team, checked against unsubscribes and against the store operations register for the 61 shop contacts (N1) before send.
- Send time: 2026-07-11, 09:00 Europe/London, after the support runbook, FAQ and macros were published 2026-07-10 with C2 (HC19) and support was briefed that day
- Subject: How card payments are handled behind the scenes this month
- Body:

> Situation. Today Harbourgate processes your card payments through three card providers, and the payment step's screens are what they have been. Complication. Between 2026-07-13 and 2026-07-20 we will move card payments on the web and app from the Marlowe provider to our single provider, Kestrel, in small groups of orders, with no downtime and no change to what a shopper does. Refunds on orders that were authorised on the old provider keep going back to that provider while its path is being drained (BR-002), so a refund can look slower than usual for a short time. Resolution. There is nothing for you to do. Your checkout, your prices and your card numbers are untouched; if a payment or a refund looks different to you, or a refund is slow, write to us using your order id and we will trace it, and our support team will have the answer by hand from the first working day. [See what is changing](../templates/delivery/customer-comms.md)

- Reply-to and where replies are triaged: support@harbourgate.example, triaged by Callum Fraser's team against the support runbook severities (HC18), with the order id as the join key.

## 5. Status page

Written before the event (the template's own rule: not after). The cutover rows are the maintenance wording for a cohort window; the four stage texts below also stand as the drafted wording for a cutover window that runs long or is aborted. The cadence promise is kept or the reason is said.

| Stage | Text (drafted now) | Posted by | Update cadence |
|---|---|---|---|
| Scheduled or investigating | Scheduled maintenance: card payments are being moved between card providers in stages. There is no downtime and shoppers pay normally; a small group of orders is affected. Updates every 30 minutes until the window closes. | Bea Lindqvist (on-call lead) | Every 30 minutes until resolved |
| Identified or in progress | The shift for this group of orders has begun and is being watched against a decline-rate and provider-error trigger (N17); if it crosses the trigger we roll the group back. Shoppers pay normally. Updates every 15 minutes. | Bea Lindqvist | Every 15 minutes |
| Monitoring | This group has moved; we are watching the decline rate against the agreed tolerance for the dwell period. No shopper action is needed. Updates every 60 minutes. | Bea Lindqvist | Every 60 minutes |
| Resolved | This group of orders now runs on the new provider and the decline rate is inside tolerance. No customer action is needed. If this shift had a customer impact we would publish a postmortem; this one did not. | Ife Adeyemi | Once, at close |

For HG-INC-14 (2026-06-15) the incident stage texts ran as follows, in severity terms (HC18): at 08:10 the finance analyst's finding was investigated as "we are investigating a delay in reconciling settled payments; shoppers pay normally"; the 5 h 40 min impact (N41) was one internal close, not one payment path, so the page never reached "in progress" against a shopper-facing surface and closed to "resolved" once the file was restored and the daily close completed; a postmortem was published (corrective actions A1 to A6) and the one customer-recognisable consequence was that refunds and settled-value reporting for Marlowe lines arrived late, with no shopper unable to pay.

## 6. Holding statement and rollback wording

The rollback trigger is written and dashboarded (N17): a cohort's decline rate above its baseline + 2 percentage points over 30 minutes, or Kestrel 5xx above 2% of calls over 5 minutes, called by on-call without discussion (release readiness section 4). The flag flip to legacy was rehearsed at 3 min 50 s (N40). If it fires, this goes out within the agreed window, with names on it and no root-cause claim before the postmortem.

- Holding statement: "A small group of card payments is being moved back to the previous provider while we check something. You will not be charged twice, and the same card is never charged automatically. If a payment looks wrong, please write to us using your order id."
- Approved by: Anneliese Vogt (legal, data protection officer) · Sent by: Callum Fraser (support lead) · Sendable within: 15 minutes of the on-call trigger being called (one escalation step, HC15, from acknowledgement at 5 minutes to Tomasz Wierzbicki at 30)
- If customer data was affected: Marlowe's path carries the card number through Harbourgate's own servers (I-5), which is why legal is the approver. Confirm with Anneliese Vogt whether any personal data or card data was exposed; PCI DSS scope during the drain is 5 of 7 systems (N55), and a data event reopens the scope register with Hamid Qureshi. Where a regulator is in scope, route to [harbourgate-compliance-impact-assessment.md](harbourgate-compliance-impact-assessment.md) (where a data event occurs, PCI DSS, the card scheme rules, strong customer authentication for card-not-present orders above £250, or any fraud-rule flag (N57), and UK GDPR are the regimes the compliance impact assessment covers) and, for any incident, [templates/operate/incident-postmortem.md](../templates/operate/incident-postmortem.md).

## 7. Support brief

- Support has the messages, the FAQ and the macro ids before any send: yes. The support runbook, the FAQ and the macros were published on 2026-07-10 with condition C2 (HC19), and support was briefed the same week, with the internal announcement of 2026-10-19 repeating it; Callum Fraser's Gate 5 support signature carried a written condition, which C2 closed.
- Expected inbound and the answer (top three, from the runbook, N21 shows 210 tickets/week tagged "payment failed" in March 2026 falling to 140 in September 2026): (1) "I was charged twice" (a rare duplicate, R1 history): answer is that the same card is never re-submitted automatically (BR-001, AC-5), and the order id is the join key for finance to reverse; (2) "my refund has not arrived": answer is that a refund on a legacy-authorised order goes back to that provider and the drain makes it look slow (BR-002), and from 2026-11-16 finance operations refund it through the provider portal within 5 working days (BR-009, KI-4); (3) at a kiosk, "pay at the till" appeared (BR-004): the kiosk showed the fallback within 10 s and holds the basket 30 minutes (N31), and the shopper pays at the till.
- Feedback route: in-app dismissals and reactions, email replies triaged by Callum Fraser's team, and store-floor notes from the 61 shop contacts; all feed the post-launch review (Gate 6, N67), which measured 7.4% payment-step non-completion (N19) and a 100% decline-attribute rate (N20) against March's 11.1% (N5).

## Exit gate (feeds Gate 5: release readiness green)

Approved messages satisfy the "comms are drafted and approved" line at [Gate 5](../os/STAGE-GATES.md) and fill section 3 of [launch-comms-plan.md](../templates/delivery/launch-comms-plan.md) with linked drafts.

- [x] Section 1 is filled and every message can be traced to it line by line. Each message draws from the facts block; dates come from N71 and HC25, the kiosk fallback from BR-004 and N31, the refund path from BR-002 and BR-009
- [x] Every message has a named approver and a date, with legal or compliance named where data, money, or a regulator is touched. Section 2 names Anneliese Vogt for legal on the merchant email, the status-page incident row and the holding statement; Hamid Qureshi for compliance on the merchant email and the incident row
- [x] Every message states what the customer must do, or says plainly that nothing is required. The shopper in-app banner and the merchant email both open with "nothing you must do"; the decline retry and the kiosk fallback are the only actions, and they are named
- [x] The status page texts and the holding statement exist before the event, not after. Section 5's four stage texts and section 6's holding statement were drafted ahead of the first send on 2026-07-13
- [x] Support is briefed before any external send is scheduled. The runbook, FAQ and macros were published 2026-07-10 under C2 (HC19), before the first cohort send of 2026-07-13, and the merchant email was held to 2026-07-11 with support briefed on 2026-07-10
- [x] Signed by Ife Adeyemi, Product Manager, owner of the product and of every artifact in the journey, 2026-07-10
