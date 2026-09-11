# Partner Integration Brief: Kestrel

Fills [templates/planning/partner-integration-brief.md](../templates/planning/partner-integration-brief.md). Everything here is invented: Harbourgate, Kestrel and the people are fictional, and every number, date, rate and identifier is ILLUSTRATIVE, drawn from the [Harbourgate journey](harbourgate-journey.md) and [coverage sheet](harbourgate-coverage-sheet.md).

**Brief owner:** Ife Adeyemi · **Partner contact:** Dani Ferreira, Kestrel merchant success manager · **Date:** 2026-04-06
**Decision needed by:** 2026-04-09, the day ADR-0003 is accepted and one day before Gate 3

## 1. The exchange

- What the partner provides: Kestrel provides the card authorisation API, status webhooks, hosted fields for web and app payments, the terminal SDK for kiosk PIN pads, and daily settlement files. The proposal is to route every Harbourgate card payment through Kestrel from Quay, including the 61 kiosks.
- What we provide: Harbourgate provides the card payment volume currently split across Kestrel, Marlowe and Tidewater, the Quay integration, the Harbourgate checkout and kiosk operating context, and the operational ownership needed to monitor, reconcile and support the path.
- Why they want this, in their words if you have them: Kestrel's own words are not filed in this brief. The commercial rationale is that consolidation would move the full Harbourgate card path onto Kestrel, including the 61 kiosks, but the partner's motive must be confirmed with Dani Ferreira before signing.

## 2. The user problem this solves

- Problem statement: Harbourgate customers who reach the payment step cannot reliably complete an order, and support cannot consistently identify the provider or reason when payment fails. The measured entry problem is 1 order in 9, or 11.1% of orders reaching the payment step, and support receives 210 tickets per week tagged "payment failed" in March 2026. For kiosk customers, the case is operational rather than a separate filed user study: the kiosk path depends on an integration with no SLA clause, and its wrapper has an ownership and logging problem.
- Evidence: The web and app problem is filed in [harbourgate-journey.md](harbourgate-journey.md): N5 records payment-step non-completion, N13 to N15 record the provider decline baselines, and N21 records the support burden. The kiosk and boundary evidence is also filed there: R2 records that nobody owned the contractor's wrapper, N28 records that Tidewater has no SLA clause, and F1 records plain-text masked PAN and cardholder name in wrapper logs. N15 shows that Tidewater kiosk declines were already the lowest at 3.1%, so the kiosk recommendation is not based on a claim that Kestrel will improve the current decline rate.
- What users do today without this partnership: Web and app customers retry or choose another payment method after a failed payment, while Harbourgate support handles payment-failed tickets without a complete provider and reason record. Kiosk customers use the kiosk path through the Tidewater wrapper, and when the call fails the operating policy is to show "pay at the till" and hold the basket for 30 minutes. The cost is failed or delayed checkout, support investigation, and an integration boundary whose owner and service commitment are unclear.
- Why partnering beats building or buying: Building a new multi-provider wrapper would preserve three provider contracts, three settlement formats, three decline vocabularies and the contractor's ownership problem. Buying another provider would add another boundary without addressing the existing wrapper and data issues. Kestrel already carries 58% of card volume, has a committed 99.9% monthly availability SLA, and has a terminal SDK that can cover the kiosk PIN pads, so one Kestrel path removes two existing integrations and gives Harbourgate one operational surface. This is a conditional argument, not proof that kiosk declines will improve: the kiosk case rests on operations, ownership and boundary reduction, while N15 shows the existing kiosk decline rate is already the lowest.

## 3. Integration surface and owners

| Surface (API, data feed, embed, SSO) | What crosses it | Our owner | Their owner | Support expectation (response time, channel) |
|---|---|---|---|---|
| Kestrel hosted fields and authorisation API for web and app | Payment details are collected through Kestrel hosted fields; Quay sends authorisation requests and receives the result | Bea Lindqvist, payments engineer | Dani Ferreira, Kestrel merchant success manager | Harbourgate on-call and Dani Ferreira through the Kestrel merchant success channel; a response time is not specified in the filed evidence |
| Kestrel status webhooks and status handling | Signed payment status events cross into Quay; missed events use the status path rather than a second card submission | Bea Lindqvist | Dani Ferreira | Harbourgate on-call owns detection and customer handling; Kestrel escalation channel through Dani Ferreira; a response time is not specified in the filed evidence |
| Kestrel terminal SDK for the 61 kiosk PIN pads | Terminal payment requests and outcomes cross between the kiosk and Kestrel's terminal surface; DEP-1 is required before a kiosk cohort | Tomasz Wierzbicki, cutover lead, with Lena Baptiste for store scheduling | Dani Ferreira | Store and payments escalation through the Kestrel merchant success channel; response time is not specified in the filed evidence |
| Kestrel settlement file over inbound SFTP | Daily settlement data crosses into Harbourgate's reconciliation service for finance close | Bea Lindqvist, with Priya Raman accountable for reconciliation | Dani Ferreira | Finance and payments use the Kestrel merchant support channel; a response time is not specified in the filed evidence |

## 4. Commercial shape and exit terms

- Commercial shape: Consolidate Harbourgate's card processing through Kestrel. The measured blended card processing cost at entry is 1.38% of card value, and the estimate after consolidation is 1.29%. The 1.29% figure is an estimate from N56, not an agreed commercial term. Revenue share, referral fees and any paid integration fee are not filed and must not be treated as agreed.
- Term and renewal: The Kestrel MSA is a rolling 12-month term with 180 days' termination notice, as recorded in HC27.
- Exit terms, written before signing: The Kestrel MSA records that card tokens are exportable to a successor processor on exit. The 180-day notice period gives Harbourgate a defined termination window. The filed MSA extract does not state the treatment of users, data other than card tokens, or in-flight transactions, so Legal must confirm those points with Anneliese Vogt before signing. Harbourgate must not remove the integration or stop supporting refunds and settlement obligations until those exit details are written down.

## 5. Risks

| Risk | Likelihood | Impact if it lands | Mitigation or accepted |
|---|---|---|---|
| R2, nobody owns the contractor's wrapper when it misbehaves | 3, score 6 at entry | 2, the payment path can fail without a clear technical owner or response path | Name Bea Lindqvist as caretaker for the existing wrapper and make the Kestrel boundary owned in the integrations register. R2 was closed on 2026-04-24 when Bea Lindqvist was named caretaker. |
| R4, a Kestrel outage stops every card payment on every surface | 1, score 3 at entry | 3, web, app and kiosk card payments would stop together | Conditional go only. Retain the kiosk fallback, "pay at the till" within 10 s with the basket held 30 minutes, and require Rohan Iyer, the sponsor, to accept R4 in writing before the last provider leaves. The later written acceptance is D-022 on 2026-08-24, with review 2027-01-31. |
| R12, the Kestrel terminal SDK needs a kiosk firmware update that shops must schedule | 2, score 4 at entry | 2, kiosk rollout could be delayed or a shop cohort could fail to move safely | DEP-1, Kestrel terminal SDK certification for the kiosk PIN pad model, is a condition before any kiosk cohort. Store operations must schedule the firmware work across the 61 shops. |
| PCI data crosses the partner boundary, including the wrapper's logged data and Harbourgate's PCI scope | 3, score 6 for the related wrapper-log risk R8 | 2, regulatory, contract and assessment exposure, with 7 systems in PCI DSS assessment scope at entry | Keep the card boundary explicit, confirm the Kestrel data and token handling with InfoSec and Legal, and record the scope effect before signing. N55 records 7 systems at entry, 5 during the drain and 3 after sunset. The wrapper-log finding F1 is tracked as R8, with scrubbing and deletion controls. |

## 6. Recommendation

Go with conditions: build on Kestrel as the single card partner for web, app and the 61 kiosks, and log the decision as D-010 on 2026-04-09 alongside ADR-0003. The strongest reason is that Kestrel already carries 58% of card volume, has a 99.9% committed monthly availability SLA, and offers the terminal surface needed to replace the operationally weak Tidewater boundary without claiming that kiosk declines need improvement. The recommendation reverses to no-go for the kiosk scope if DEP-1 certification is not complete before a kiosk cohort, or if Rohan Iyer does not accept R4 in writing, and Legal has not confirmed the PCI and exit terms before signing.

## Exit gate

- [x] Both sides of the exchange are stated in concrete terms, including the partner's motive. Kestrel's capability and Harbourgate's volume and operating context are stated; the partner's own words are not filed, so that gap is explicit.
- [x] The user problem cites filed evidence, not strategy language. The web evidence cites N5, N13 to N15 and N21; the kiosk and boundary evidence cites R2, N28 and F1, with N15 showing the kiosk decline rate was already the lowest.
- [x] Every integration surface has a named owner on each side. Harbourgate owners are named, Dani Ferreira is the Kestrel contact, and the missing response time is not invented.
- [x] Exit terms are written down before anything is signed. HC27 records the rolling 12-month term, 180 days' notice and token export to a successor processor; the unrecorded treatment of other data and in-flight transactions is assigned to Legal before signing.
- [x] Dependency and data-sharing risks have rows, and material ones are in the risk register. R2, R4, R12 and the PCI boundary are recorded; the related wrapper-log risk is R8 and the required kiosk dependency is DEP-1.
- [x] The recommendation is one of go, no-go, or conditional go, and is logged in the decision log. This is conditional go, logged as D-010 on 2026-04-09; the sponsor's written acceptance of R4 was later met by D-022.

Signed at the PLANNING decision point, 2026-04-09: Ife Adeyemi, Product Manager.
