# Empathy Map: Sahulat Bill Pay, Shazia

Fills [frameworks/discovery/empathy-map.md](../frameworks/discovery/empathy-map.md). Everything here is invented: Sahulat, its people, customers, agents, billers, bank, aggregator and telco are fictional, and every number is ILLUSTRATIVE, chosen so that the artifacts agree with each other and not to describe any real wallet, market or regulator.

**Owner:** Hira Baig, Product Manager · **Date:** 2026-02-16 · **Status:** Synthesis draft for Gate 1 · **Product:** Sahulat bill pay · **Data sheets:** [sahulat-journey.md](sahulat-journey.md), [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md)

## What it is for

This map keeps P1 Shazia tied to what the customer sessions support before the persona is written. It maps the household bill-runner job for Sahulat, using INT-001, INT-002, INT-004, INT-005, INT-007 and INT-008.

The key contradiction is between what Shazia says after the pitch-slip, “would probably try it”, and what she does: money enters the wallet for a bill and the wallet is emptied the same day, as recorded in T2. The contradiction matters because the product opportunity is bill payment, not a general promise that Shazia will hold a balance.

## Run it when

This map is being run on the synthesis day before the personas, 2026-02-16. It uses six customer sessions, which is arithmetic of:

`INT-001 + INT-002 + INT-004 + INT-005 + INT-007 + INT-008 = 6 sessions`

It is not a map of all Sahulat customers. It is one role, one job and one participant composite, P1 Shazia.

## Inputs you need first

- Customer session IDs: INT-001, INT-002, INT-004, INT-005, INT-007 and INT-008.
- Agent session IDs: INT-009 to INT-014.
- The timestamped evidence in INT-004, including E1 at 02:10 and E2 at 18:35.
- E4 from INT-007 at 21:15.
- Themes T1, T2, T4 and T5.
- The canonical data sheets: [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md).
- No timestamp is added for INT-001, INT-002, INT-005 or INT-008 because the supplied synthesis data does not provide one.

## The worksheet

### 1. Frame

| Field | Entry |
|---|---|
| Who we are mapping | Shazia, P1, the household bill-runner; sessions INT-001, INT-002, INT-004, INT-005, INT-007 and INT-008 |
| What they need to do | Pay the household electricity, gas or water bill on or near the due date without a trip, a shop fee or a late surcharge |
| Sessions used | INT-001, INT-002, INT-004, INT-005, INT-007 and INT-008, `6 sessions = 6 distinct session IDs` |

### 2. The six cells

| Cell | Entry (verbatim or observed) | Source (session ID, timestamp) | Evidence class |
|---|---|---|---|
| Says | “The bill was due on a Sunday. The bank was shut, the shop man charged me fifty, and the office still put the fine on the next bill.” | INT-004, 02:10, E1 | said |
| Says | “I only put money in the phone when I need to send it that day. Why would I leave it there?” | INT-004, 18:35, E2 | said |
| Says | “Would probably try it”, after the pitch-slip | INT-004, timestamp not recorded in the supplied synthesis notes | said |
| Does | Pays in person on or near the due date, using a bank branch or bill shop. The sample split is `4 of 8 at a bank branch + 4 of 8 at a bill shop = 8 of 8 customers`. | INT-001, INT-002, INT-004, INT-005, INT-007 and INT-008, timestamp not recorded in the supplied synthesis notes; N63 | observed |
| Does | Puts money into the wallet for a purpose and empties the wallet the same day, rather than leaving money there. | INT-001, INT-002, INT-004, INT-005, INT-007 and INT-008, T2, timestamp not recorded in the supplied synthesis notes | observed |
| Does | When a USSD screen goes off during payment, waits for the message and then dials again. | INT-007, 21:15, E4 | observed |
| Thinks | “The due date is risky if it falls on a Sunday or outside the bank's opening time.” | Inferred from INT-004, 02:10, E1, and T5 | inferred from INT-004, 02:10 |
| Thinks | “If money is put into the wallet, it should leave for the intended payment that day.” | Inferred from INT-004, 18:35, E2, and T2 | inferred from INT-004, 18:35 |
| Feels | Concern about being charged a late surcharge when the due date falls on a weekend or the payment route is closed. | Inferred from INT-004, 02:10, E1, and T5 | inferred from INT-004, 02:10 |
| Feels | Uncertainty when a USSD session drops and the wallet movement is not yet clear. | Inferred from INT-007, 21:15, E4 | inferred from INT-007, 21:15 |
| Pains | A bill-paying trip takes a median `70 minutes` round trip and `PKR 60` transport per trip. | INT-001, INT-002, INT-004, INT-005, INT-007 and INT-008, N20; timestamps not recorded in the supplied synthesis notes | observed and told |
| Pains | A shop may charge `PKR 30 to 50` per bill. | INT-009 to INT-014, N21, timestamp not recorded in the supplied synthesis notes; agent-told, not a customer session | told |
| Pains | A surcharge may appear on the next bill. | INT-004, 02:10, E1; T5 (INT-004, 005, 008) | said and told |
| Gains | A bill paid without the bank or bill-shop trip would remove the median `70 minutes` of round-trip travel and `PKR 60` transport for that trip. | Inferred from INT-001, INT-002, INT-004, INT-005, INT-007 and INT-008, N20 and T1 | inferred from INT-001, INT-002, INT-004, INT-005, INT-007 and INT-008 |
| Gains | A clear payment reference or message would reduce the uncertainty after a dropped session. | Inferred from INT-007, 21:15, E4 | inferred from INT-007, 21:15 |

**Two-sessions rule check:**

| Cell | Distinct sessions represented | Arithmetic | Result |
|---|---:|---|---|
| Says | 1 timestamped session, with the pitch-slip statement also only attributed to INT-004 in the supplied synthesis record | `1 = INT-004` | Misses the two-sessions rule |
| Does | 6 sessions | `6 = INT-001 + INT-002 + INT-004 + INT-005 + INT-007 + INT-008` | Meets the rule |
| Thinks | 2 sessions | `2 = INT-004 + INT-007` | Meets the rule |
| Feels | 2 sessions | `2 = INT-004 + INT-007` | Meets the rule |
| Pains (trip) | 6 sessions | `6 = INT-001 + INT-002 + INT-004 + INT-005 + INT-007 + INT-008` | Meets the rule |
| Pains (shop fee) | 6 agent sessions, no customer session | `6 = INT-009 + INT-010 + INT-011 + INT-012 + INT-013 + INT-014` | Misses the two-sessions rule for a customer cell; agent-told only |
| Pains (surcharge) | 3 sessions | `3 = INT-004 + INT-005 + INT-008` | Meets the rule |
| Gains | 6 sessions for avoiding the trip, 1 session for payment proof after a drop | `6` for the trip entry; `1 = INT-007` for the proof entry | Trip entry meets the rule; proof entry misses it |

No timestamp is invented for INT-001, INT-002, INT-005 or INT-008. The cells that rely on those sessions use session IDs and the supplied themes or data-sheet rows only. The shop-fee sub-row rests on the agent sessions INT-009 to INT-014 only, and its two-sessions arithmetic is counted there separately from the customer-session count.

### 3. Contradictions

| Says | Does | What it might mean | Follow-up question |
|---|---|---|---|
| “Would probably try it”, said after the pitch-slip | The wallet is emptied the same day after money enters for a purpose, T2 | The statement is willingness to try bill pay, not evidence that Shazia wants to store a balance. The product must support a purposeful, same-day payment path rather than assume balance retention. | “Tell me about the last time money entered your wallet for a bill. What happened next, and when did the money leave?” |
| “Why would I leave it there?” | Pays on or near the due date through a bank branch or bill shop, often with a trip or fee | The constraint may be timing, proof and access, not an unwillingness to use a wallet. | “What would need to be true for you to pay the bill through Sahulat on the due date?” |
| Waits for the message, then dials again after the screen goes off | Repeats the USSD attempt rather than waiting for certainty | A dropped session is experienced as a payment-risk problem. The first requirement is status clarity and duplicate protection, not a faster pitch. | “After a dropped session, what would convince you that the first payment did or did not happen?” |

### 4. Unsourced (assumptions)

These entries are kept out of the six cells. They are the claims the later P1 persona must not present as evidence without a cited session.

| Entry | Who believes it | Register ID |
|---|---|---|
| Shazia will keep a balance in Sahulat for more than two days so that she can pay a later bill. | The product team, inferred from the pitch-slip and the balance-first product idea | Open: Hira Baig owns the assumptions-register entry; no register ID is present in the supplied data |
| Shazia prefers paying from an existing wallet balance over cashing in and paying in the same visit. | The product team | Open: Hira Baig owns the assumptions-register entry; no register ID is present in the supplied data |
| Shazia will use Sahulat regularly once bill pay exists. | The product team | Open: Hira Baig owns the assumptions-register entry; no register ID is present in the supplied data |
| Shazia will accept an SMS reference as sufficient proof without asking for a paper slip. | The product team | Open: Hira Baig owns the assumptions-register entry; no register ID is present in the supplied data |
| Shazia has a smartphone and will use an app-first bill-pay flow. | The product team | Open: Hira Baig owns the assumptions-register entry; no register ID is present in the supplied data |

## Reading the result

The strongest result is the contradiction, not the pitch-slip response. Shazia says she would probably try Sahulat, but the observed pattern in T2 is that money enters for a purpose and leaves the same day. The evidence supports a bill-payment job with a same-day funding path. It does not support a balance-retention persona.

The clearest pains are:

- a median `70 minutes` round trip and `PKR 60` transport per bill-paying trip;
- a shop fee of `PKR 30 to 50` per bill;
- a late surcharge when the payment route is closed or the due date falls on a weekend;
- uncertainty after a dropped USSD session.

The trip avoidance gain is supported across all six mapped sessions. The proof gain is supported directly in INT-007 only, so it needs another session before it is treated as a stable persona claim.

The map therefore feeds P1 Shazia with:

- a household bill-runner role;
- a due-date and access problem;
- a same-day payment behavior;
- a dropped-session trust problem;
- an explicit warning not to turn the balance-keeper hypothesis into a fact.

## ILLUSTRATIVE example

This worksheet has no separate unrelated example. The Shazia map above, the six cells, the two-sessions rule check and the unsourced list, is the filled example, and every quote, number and session reference in it is fictional and ILLUSTRATIVE.

## The trap

The tempting mistake is to convert “would probably try it” into “will keep money in the wallet”. That would erase the contradiction with T2 and make the failed balance hypothesis look evidenced.

A second mistake is to label Shazia “frustrated” or “overwhelmed” without a quote or observed behavior. This map uses the evidence instead: a surcharge appears on the next bill, money leaves the wallet the same day, and a dropped session leads to a repeat dial.

A third mistake is to present the proof preference as established. INT-007 shows uncertainty after a dropped session, but the two-sessions rule is not met for that specific gain. It remains a follow-up question until another session supports it.

## Feeds

- [sahulat-personas.md](sahulat-personas.md): P1's role, pains, workarounds, contradiction and evidence limits.
- [sahulat-journey.md](sahulat-journey.md): canonical sessions, themes T1, T2, T4 and T5, evidence E1, E2 and E4, and data-sheet rows N18 to N25.
- [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md): coverage timeline entry for the 2026-02-16 empathy map.
- [templates/discovery/journey-map.md](../templates/discovery/journey-map.md): current journey, especially the trip, surcharge and dropped-session moments.
- [templates/discovery/problem-framing.md](../templates/discovery/problem-framing.md): evidence for the problem and the cost of inaction.
- [knowledge/jobs-to-be-done.md](../knowledge/jobs-to-be-done.md): method background.
- Gate 1: the map is usable as a synthesis input, with the says cell and the payment-proof gain explicitly marked as misses against the two-sessions rule. The unsourced claims remain open for the persona review.

**Exit-gate walk:** Hira Baig, Product Manager, signed 2026-02-16.
