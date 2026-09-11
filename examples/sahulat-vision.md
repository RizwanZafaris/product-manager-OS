# Product Vision: Sahulat Bill Pay

Fills [templates/planning/vision.md](../templates/planning/vision.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, the people and every figure are shared with the rest of the [Sahulat journey](sahulat-journey.md), every number and claim in this document is ILLUSTRATIVE, drawn from the journey's data sheet, and this vision was originally dated to what discovery actually knew on 2026-03-02, before the DESIGN and OPERATE stages the journey later records; it carries a 2026-08-28 amendment folding in decisions D3 and D8 and ADR-2, each of which postdates the original sign-off. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager, the only PM · **Horizon:** 3 years (2026 to 2029) · **Last updated:** 2026-08-28 · **Status:** Signed 2026-03-02 by Faisal Mirza; amended 2026-08-28 after decision D8, whose agent-assisted pivot is reflected in the funding-agnostic wording of sections 1 and 4 ("from cash just handed to Rafiq" / "funded from a balance or from cash just handed to an agent"). D3 (2026-04-03), ADR-2 (2026-04-09) and D8 (2026-08-28) postdate the original sign-off and are folded in at this amendment

## 1. The future state

It is the third week of a month in 2029, and Shazia's Ravi Power bill is due in three days. She does not go looking for the paper bill to check what she owes: a message named the reference, the amount and the due date the day it posted, the same way Chenab Gas's does the same week. She has not made a trip whose only purpose was paying a bill since the year both of them moved onto Sahulat. When she next visits Rafiq, her agent, it is because she needs cash for something else entirely; while she is at his counter, on that same visit, she settles both bills, and it costs her nothing beyond the bill itself.

That last sentence used to be false three ways at once. A trip to a bank branch or a bill shop cost a median of 70 minutes round trip and PKR 60 in fares (N20, estimate, told); four of the eight households in the discovery sample used a bill shop that agents said charged PKR 30 to 50 to carry the payment for them (N21, estimate, agent-told; N63); and five of eight had paid a late surcharge in the last three months (N18), a median of PKR 200 (N19, estimate), and three of eight most recent due dates fell on a weekend when the bank was shut, while six of eight households pay on the due date itself, leaving no slack for a closed branch (N24, N25). Shazia used to be one of them: her bank was shut on a Sunday due date, the bill shop charged PKR 50 to carry it anyway, and the biller still put a fine on the next bill (E1).

None of that arithmetic is visible to her now. She never wonders whether a session that dropped mid-payment took her money; if one does, a message tells her within two minutes whether the money moved, before she thinks to dial again (E4). She pays whichever way she has money that week, sometimes from a balance already sitting in the phone, more often from cash just handed to Rafiq (Amendment, 2026-08-28: funding-agnostic wording added per D8's agent-assisted pivot), and the bill is paid before its due date either way. The paper bill still arrives in the post and sits in a drawer with the others; nothing on it matters to her anymore, because the reference, the amount and the receipt all live in a text message she can find any time.

She is not unusual on her street. Sahulat had 1.9 million registered wallets (N1), and in December 2025 only 410,000 of them (N2) did anything in a given month; 61 percent of cash-ins were fully cashed out within 48 hours (N10). By 2029, a meaningful share of that base looks like Shazia's household: two or three bills a month, paid on the ledger because the bill itself is the reason to pay, not because a promotion once asked them to keep a balance.

We will know we were wrong if, a year after this feature ships, Shazia still keeps the paper bill to know what she owes, or still makes a trip whose only purpose is paying it. We will have been wrong in a different way if she pays only because we made her into someone she is not: six of the eight customers in the discovery sessions describe money entering the wallet for a purpose and leaving the same day (T2), and only two describe holding a balance for more than two days (N26), the only evidence under Kamran, the balance-keeping persona this vision does not build for. Whether Shazia herself will ever hold a balance is untested, not settled either way. This vision does not require Shazia to keep money in her phone. It requires the bill to get paid, whichever way the money arrives at the moment she pays it.

## 2. Who this is for

| Field | Answer |
|---|---|
| Primary customer | Shazia, the household bill-runner (persona P1): a composite of six of the fourteen discovery sessions (INT-001, 002, 004, 005, 007, 008), who already reaches Sahulat through an agent or a USSD short code, and who pays her household's electricity and gas bills, and water, three bills a month (N22) |
| The progress they are trying to make | In her own words (E1, INT-004, 2026-02-02): "The bill was due on a Sunday. The bank was shut, the shop man charged me fifty, and the office still put the fine on the next bill." She wants the month's bills paid before their due dates without a trip whose only purpose is paying them, and without handing someone else PKR 30 to 50 to carry the payment for her (RQ1; N18 to N21, N24) |
| Who this is explicitly NOT for yet | Rafiq's own retail business, if an agent wanted to accept Sahulat payments for goods sold at the counter rather than for cash-in and cash-out (see the merchant-acquiring non-goal below); households reachable only by a smartphone app, the minority channel in Sahulat's own USSD-majority market (see the app-first non-goal); and Kamran, the salaried balance-keeper persona (P3, ASSUMPTION), whose balance-holding behavior only two of eight discovery sessions support (N26; see the non-goal below) |

Kamran, a salaried balance-keeper the same research surfaced, is deliberately not this primary customer: only two of eight sessions support him holding a balance for more than two days (N26; carried in [personas](sahulat-personas.md) as an explicit ASSUMPTION), and section 1 was written so it does not depend on which of the two of them turns out to be more common.

## 3. Why now

Two shifts, ILLUSTRATIVE like every number in this document and sourced in the [journey's data sheet](sahulat-journey.md#data-sheet):

| Shift that opens the window | Evidence it is real | What happens if we wait |
|---|---|---|
| Customers are already asking for bill pay by calling the agent helpline, not being pitched it, while most cash-in still leaves the wallet again within two days, so the board's active-wallet key result has nothing organic feeding it | 412 calls in the four weeks to 2026-01-09, tagged BILL-ASK on the agent helpline (N13); 61 percent of cash-ins were fully cashed out within 48 hours in Q4 2025 (N10), against a 2026 board key result of 520,000 30-day active wallets, 110,000 above the December 2025 base of 410,000 (N4; N2) | The helpline keeps absorbing demand nobody is serving, the wallet keeps functioning as a remittance pass-through wearing an inclusion story, and the key-result gap gets no closer to year end with nothing in the pipeline to close it |
| Falak Telecom's own USSD tariff rises in October, raising the cost of every session and every retry on the channel most of Sahulat's base actually uses: a dropped session produces a blind repeat dial after a five-to-ten-minute wait for a status message that never comes (T4, E4), and that repeat happens on a new dial, never inside the dropped one, so each repeat is its own session against the same 180-second gateway ceiling (N66; AC-8, cited as part of the 2026-08-28 amendment) | Tariff notice dated 2025-12-18: PKR 0.40 rising to PKR 0.65 per session from 2026-10-01, a 62.5 percent rise (N62, quoted) | From 2026-10-01, every one of those extra sessions costs PKR 0.65 rather than PKR 0.40, so the flow's own dropped-session handling (Amendment, 2026-08-28: the ADR-2 idempotency design, folded in after ADR-2's 2026-04-09 decision, designed to resume rather than restart a session; the resume half, AC-8, is the Gate 4 miss deferred to Rel-2, owner Zainab Qureshi) is worth more after October, because every retry it prevents costs more that day than it would today |

## 4. North star tie-in

- **North star metric this vision implies:** candidate M5, wallets with at least one on-ledger payment in the trailing 30 days, 96,000 wallets in December 2025 (N14). The [north star sheet](sahulat-north-star-metric.md) that formalizes M5's guardrails was not built yet as of this vision's original 2026-03-02 signing; it follows two days later.
- **How the future state moves it:** a household not already counted in M5 joins it the month it settles a bill through Sahulat because the bill exists, not because a promotion asked it to keep a balance, and it does so whether the payment was funded from a balance or from cash just handed to an agent (Amendment, 2026-08-28: funding-agnostic wording added per D8), because M5 counts the payment landing on the ledger, not how the money arrived there.

## 5. Non-goals

| We will not | Because | Revisit when |
|---|---|---|
| Extend credit, or a loan against a bill amount | Sahulat's EMI license covers e-money issuance and payment services, not lending; underwriting credit needs different capital treatment and a risk function the nine-engineer team does not have | A licensed lending partner is willing to underwrite behind Sahulat's rail, and compliance confirms the arrangement sits inside the license's permitted activities |
| Design a flow that only pays off if customers hold a balance | Only two of eight discovery sessions support Kamran, the salaried balance-keeper persona, holding a balance for more than two days (N26), short of the research plan's bar; carried in [personas](sahulat-personas.md) as an explicit ASSUMPTION | A later DISCOVER pass finds three of eight or more customers holding a balance for more than two days |
| Build merchant acquiring, letting a shop accept a Sahulat QR code or card-present payment | This vision answers a household's outgoing bill, not a shop's incoming sale; the [payments-acquiring card](../knowledge/domains/payments-acquiring.md)'s four-party model makes merchant underwriting and chargeback liability, and PCI DSS scope for any card-present acceptance, a different business from paying a biller | The agent network itself asks to be paid as merchants for goods they sell, rather than through cash-in and cash-out commission, a distinct discovery question this pass does not own |
| Build an app-first flow that treats USSD as a fallback channel | Sahulat's own market is USSD-majority, reached through a feature-phone short code or the agent counter, with the smartphone app a minority channel (per [the journey](sahulat-journey.md)); the [mobile-money card](../knowledge/domains/mobile-money-wallets.md) is explicit that designing for the smartphone persona in a USSD-majority market builds the wrong product well | The app becomes the majority channel for active bill-pay usage, sustained across two consecutive quarters |
| Settle bills over a bank's bill-pay rail whose cut-off posts after-hours or weekend payments the next working day | A payment that posts the next working day reproduces the weekend surcharge this vision exists to remove; a licensed aggregator can post the same day, seven days a week instead (BillBridge's quoted 30-minute SLA, N36) | A bank rail posts to the biller the same day, seven days a week. (Amendment, 2026-08-28: tested and rejected as D3, 2026-04-03; D3 names the specific condition, Darya's cut-off past 20:00 seven days a week.) |
| Do national scheme interoperability work, connecting bill pay to the national instant-payment scheme or another wallet's rail | This feature pays a bill inside Sahulat's own closed loop through one aggregator; interoperability is a wallet-wide bet decided at the company level, bigger than one feature's horizon or a nine-engineer team can fund alongside it. Raast obligations SBP imposes on the wallet, such as the P2M mandate for QR scan and Request to Pay, are owned by Amna Rasheed at wallet level, and this feature adds no scheme work beyond them | The company sets a wallet-wide interoperability program, or a second product on this rail needs to reach an account outside Sahulat's own network |

## How this vision fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Indistinguishable from a competitor's | Language any vendor in the category could publish unchanged | Name one moment for one person that only you could credibly own |
| A roadmap in disguise | Quarters, deliverables and dates dressed as direction | A vision states a destination. The moment it carries a date it is a plan |
| Adjectives with no picture | "Seamless", "intelligent", "delightful", and no scene | One paragraph describing a named person doing the thing, some years out |
| Unfalsifiable | So abstract that no outcome could ever contradict it | Write the observation that would mean it had failed |
| Written once, never referenced | A file nobody opens between annual planning rounds | It is quoted in kickoffs and in PRDs, or it is not operating |

This vision answers its own "Indistinguishable" row inside section 1: no other wallet connects Ravi Power, Chenab Gas and an agent named Rafiq to one Falak Telecom short code the way this one does. Section 1 also carries no date and a named scene, answering "A roadmap in disguise" and "Adjectives with no picture". It answers "Unfalsifiable" in section 1's closing paragraph, which states the observation that would mean this document was wrong. Against "Written once, never referenced": the one-pager's app-first, bank-rail and merchant-acquiring not-doing items, and D3's "what would change our mind" field in the decision log, each quote this vision by name and link back to it.

## Exit gate

This vision is fit to publish when:

- [x] The future state is written in the customer's terms and would not survive a competitor name swap
- [x] Exactly one primary customer is named, and the deferred segments are listed as non-goals
- [x] The why-now names a real shift with linked evidence, not a trend headline
- [x] The implied north star metric is stated, even if only as a candidate
- [x] Every non-goal carries a reason and a revisit condition
- [x] A team could use this document to say no to a plausible feature request

Signed: Faisal Mirza, Chief Executive, 2026-03-02
