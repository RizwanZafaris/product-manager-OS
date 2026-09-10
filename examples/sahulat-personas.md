# Personas: Sahulat Bill Pay

Fills [templates/discovery/personas.md](../templates/discovery/personas.md). Everything here is invented: Sahulat Digital, Shazia, Rafiq, Kamran and every session, quote and count below are fiction, built so three personas can be checked against the same fourteen invented sessions by session ID. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager, the only PM in the company · **Date:** 2026-02-17 · **Status:** Final for Gate 1, unchanged through both attempts (attempt 1, 2026-02-20, MORE DISCOVERY on lines this file does not hold; attempt 2, 2026-02-27, GO) · **Source study:** [sahulat-journey.md](sahulat-journey.md)'s N17 row; `sahulat-user-research-plan.md` fills the plan itself in this same set, 14 sessions, 2026-01-26 to 2026-02-13: 8 customers (INT-001 to INT-008), 6 agents (INT-009 to INT-014)

---

## Persona: Shazia, the Household Bill-Runner

### Snapshot

- **Role and context:** Runs the household's utility bills, electricity, gas, sometimes water, on a feature phone over USSD, or at her agent's counter; not an app-first user.
- **Segment size:** 246,000 wallets, a proxy count of wallets with a cash-in on the 5th to 10th in two of the last three months (N64, estimate, query BP-01, February 2026); a behavioral proxy, not a direct count, since nothing in the ledger names "who runs the household bills" today.
- **Frequency of contact with the problem:** Close to weekly: the sample's households carry three bills a month, electricity, gas and water (N22, measured, bills shown in 8 customer sessions).

### The job

> When a utility bill in my house is due, I want to pay it without a special trip to a bank or a bill shop, so I can avoid a late surcharge and get back to the rest of my day.

### Goals and success

- **They consider the day won when:** No separate trip was made, a receipt or an SMS proves the bill is paid, and the next bill carries no surcharge line.
- **They are measured or judged by:** Her own household budget; a surcharge is money she personally has to explain, not a line item anyone else absorbs for her.

### Pains and workarounds

*Figures ILLUSTRATIVE. Source and firmness for each ID are in the data sheet at [sahulat-journey.md](sahulat-journey.md).*

| Pain | Current workaround | What the workaround costs them |
|---|---|---|
| A due date that falls on a day the bank branch is shut, or on a working day she cannot spare | Pays at a bank branch or a bill shop, whichever is open that day: 4 of 8 sampled customers used each channel (N63, measured, told) | A round trip of about 70 minutes and PKR 60 in transport (N20, estimate, told); a bill-shop visit adds a PKR 30 to 50 fee on top (N21, estimate, told) |
| The bill-shop fee is real money on a bill already due | Pays it rather than make a second trip | N21's source is agent testimony (INT-009 to INT-014), not a customer session; see the claim below |

### Behaviors that matter to design

- Holds close to no standing balance: money enters the wallet for a purpose and leaves the same day, a pattern six of the eight customer sessions describe and only two contradict (T2; N26 counts the two contradictors). "I only put money in the phone when I need to send it that day. Why would I leave it there?" (E2, INT-004, 2026-02-02, 18:35).
- Pays close to the due date rather than early, so a slow channel or a shut branch turns directly into a surcharge (T1, T5).
- When a USSD session drops mid-attempt, redials rather than waiting for a status message; INT-007 describes exactly this (T4).

### What they distrust

Leaving money sitting in a wallet she cannot picture spending that day (E2). A USSD screen that goes dark mid-transaction with no confirmation either way, which is the exact moment INT-007 describes waiting ten minutes before dialing again (T4).

### Evidence (mandatory)

| # | Session ID | What it contributed to this persona |
|---|---|---|
| 1 | INT-001 | Pilot (guide v1), 2026-01-26; the trip-and-fee pattern that became T1 |
| 2 | INT-002 | Pilot (guide v1), 2026-01-26; second confirmation of the same-day cash-in pattern, T2 |
| 3 | INT-004 | 2026-02-02; the surcharge bill and Sunday due date behind E1; source of E2 |
| 4 | INT-005 | 2026-02-03; corroborated the trip-and-fee pattern and the due-date timing |
| 5 | INT-007 | 2026-02-06; the dropped USSD session and redial behind "behaviors that matter to design" |
| 6 | INT-008 | 2026-02-09; corroborated the same-day cash-in pattern N26 later counted against |

**Claims above with no evidence row:** The PKR 30 to 50 bill-shop fee (N21) rests on agent testimony only; no session in this persona's own six names the amount she pays out of pocket, so it is listed rather than presented as customer-confirmed.

### Anti-persona note

**Who this persona is NOT:** Kamran, the salaried balance-keeper (P3, ASSUMPTION); both are wallet-holding household customers on the same USSD channel, which is why they get confused. The difference: Shazia spends the same day and holds close to zero balance (E2, T2); Kamran leaves a standing balance between paydays (E5). Two of the eight sessions describe his pattern (N26); six describe hers.

---

## Persona: Rafiq, the Corner-Shop Agent

### Snapshot

- **Role and context:** Runs a general store that doubles as a Sahulat cash-in and cash-out counter; deals with customers face to face, mostly on his own agent handset, sometimes helping a customer dial USSD on their own phone at the counter.
- **Segment size:** 3,200 active agents network-wide (N5, measured, agent management system, 2025-12-31); how many field bill questions as often as this sample is not measured. Open: Tariq Sohail, next agent debrief round.
- **Frequency of contact with the problem:** Daily. Six or seven customers a day ask him whether he can pay their bill (E3, INT-011, 2026-02-04, 06:50, told).

### The job

> When a customer at my counter asks if I can pay their bill, I want to say yes and keep the transaction here, so I stop handing a paying customer to the shop across the road.

### Goals and success

- **They consider the day won when:** A bill question that walks in becomes a transaction at his counter, not a referral out the door.
- **They are measured or judged by:** His daily commission, PKR 15 per cash-in and PKR 20 per cash-out today (N29, N30, commission schedule v6, measured); bill pay carries no commission line yet, the open question below.

### Pains and workarounds

*Figures ILLUSTRATIVE. Source and firmness for each ID are in the data sheet at [sahulat-journey.md](sahulat-journey.md).*

| Pain | Current workaround | What the workaround costs them |
|---|---|---|
| Six or seven bill questions a day, and no product to answer them with (E3; T3 across all six agent sessions) | Sends the customer to a rival bill shop across the road | The rival keeps the PKR 30 to 50 fee per bill that could have been his (N21, estimate, told); how many of the daily asks become a lost transaction, and what that totals monthly, was not counted. Open: Sara Lodhi, agent debrief data |
| A dropped USSD session at the counter looks the same to him whether it is his handset or the customer's | Reassures the customer and tries again (T4, INT-012) | Time at the counter with nothing to show for it; not separately measured on the agent side |

### Behaviors that matter to design

- Works mostly from his own agent handset rather than the customer's phone, which the [mobile money and wallets card](../knowledge/domains/mobile-money-wallets.md) names directly: the agent is a persona alongside the wallet holder, not a channel bolted onto one.
- Refers rather than losing the relationship outright, wanting to keep the customer's trust even when he cannot complete the job himself: "Six or seven people a day ask me if I can do their bill. I send them to the shop across the road and he keeps the fifty." (E3, INT-011, 2026-02-04, 06:50).
- Daily, face-to-face contact means any friction becomes something he has to personally explain to someone standing in front of him, not a support ticket he can defer.

### What they distrust

Open: Hira Baig, next DISCOVER pass. Whether helping a customer complete a bill payment earns him anything if the customer does not also need a fresh cash-in that visit. No session in this round asked him that directly.

### Evidence (mandatory)

| # | Session ID | What it contributed to this persona |
|---|---|---|
| 1 | INT-009 | 2026-02-04; first session to establish the daily-referral pattern, T3 |
| 2 | INT-010 | 2026-02-04; corroborated T3 and the fee range, N21 |
| 3 | INT-011 | 2026-02-04, 06:50; source of E3, the six-or-seven-a-day line and the rival shop |
| 4 | INT-012 | 2026-02-06; corroborated the dropped-session pattern from the agent's side, T4 |
| 5 | INT-013 | 2026-02-11; corroborated the referral pattern and fee range, N21 |
| 6 | INT-014 | 2026-02-13; closing session, confirmed the pattern across the full six-session set |

**Claims above with no evidence row:** The monthly value of the referrals he loses is not computed anywhere in this round; six or seven a day and a PKR 30 to 50 fee are both evidenced, their product is not, and is marked Open above rather than multiplied out here.

### Anti-persona note

**Who this persona is NOT:** The rival bill-shop proprietor across the road, the one E3 names as keeping the fifty. Both take a fee for the same errand; the difference is that Rafiq's transactions post to Sahulat's ledger under a commission it controls, while the rival's exist in no system Sahulat can see, with no float, agreement or reconciliation tying him to the network.

---

## Persona: Kamran, the Salaried Balance-Keeper (ASSUMPTION)

### Snapshot

- **Role and context:** A salaried employee whose pay lands in the Sahulat wallet directly; keeps money sitting in the wallet between paydays rather than moving it out the day it arrives.
- **Segment size:** Open: Sara Lodhi, once a salary-deposit signal exists in the ledger to query against. N64's 246,000 wallets describes Shazia's cash-in pattern, not this one; reusing it here would overstate what two sessions support.
- **Frequency of contact with the problem:** Open: Hira Baig, next DISCOVER pass. Two sessions did not establish how often this pattern recurs.

### The job

> When my salary lands in the wallet, I want to leave it there until a bill is due, so I can pay from the balance without a separate cash-in trip.

### Goals and success

- **They consider the day won when:** A bill is paid straight from the balance already sitting in the wallet, with no agent visit needed that month.
- **They are measured or judged by:** Open: Hira Baig, next DISCOVER pass. Neither session asked what "day won" means to Kamran beyond skipping a trip; two sessions did not reach this depth before the guide moved on.

### Pains and workarounds

*Figures ILLUSTRATIVE. Source and firmness for each ID are in the data sheet at [sahulat-journey.md](sahulat-journey.md).*

| Pain | Current workaround | What the workaround costs them |
|---|---|---|
| Open: Hira Baig, next DISCOVER pass. Not distinguished for these two sessions from the wider sample's trip and fee questions | Keeps a standing balance and pays directly from it when a bill is due (E5) | Open: Sara Lodhi. Not priced separately for this segment |

### Behaviors that matter to design

Holds roughly PKR 2,000 to 3,000 in the wallet at a time between paydays: "I keep two or three thousand in it because my salary comes there." (E5, INT-003, 2026-01-29, 11:40). This is the only quantified, design-relevant fact this persona rests on, and it comes from two sessions.

### What they distrust

Open: Hira Baig, next DISCOVER pass. Neither session was asked, and nothing in either transcript volunteers it.

### Evidence (mandatory)

| # | Session ID | What it contributed to this persona |
|---|---|---|
| 1 | INT-003 | 2026-01-29, 11:40; the source of E5 and the first session to describe a standing balance rather than same-day spend |
| 2 | INT-006 | 2026-02-05; the second and only other session describing the same pattern, giving N26 its count of two |

**Claims above with no evidence row:** "They are measured or judged by," "What they distrust," and the segment size are all open; two sessions established only that a standing balance exists and roughly how large it is. Everything else about this persona is inferred, not evidenced, and is written above as Open rather than filled in from the same imagination the ASSUMPTION label exists to catch.

### Anti-persona note

**Who this persona is NOT:** Shazia, the household bill-runner (P1), the six-session pattern of cashing in only when a payment is imminent (E2). The difference: Kamran leaves money in the wallet between paydays; Shazia moves it out the same day. Six of the eight sessions describe her pattern; two, both his own, describe this one (N26). A saved-balance feature built around this persona is built for the two, not the six.

---

## How these personas fail

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Invented | Polished profiles, no interview behind any of them, everyone agrees | Each persona cites a source interview, or is labelled an assumption |
| Used to win arguments | "Our persona would not want that", with nothing behind it | If it cannot be traced to evidence, it cannot settle the argument |
| Labelled but not reread | Kamran carries ASSUMPTION from the day this file was written, on two sessions. That label is legal; the failure is what happens after it, when a later stage scores the risk of building for him as low and spends real engineering time without ever reopening the label | A validate-by date on the label, checked at the next gate before budget is spent against it, not filed once and trusted forever |

## Exit gate (feeds Gate 1: problem worth solving)

- [x] Two or three personas, no more: exactly three, Shazia, Rafiq and Kamran.
- [x] Every persona has five or more evidence rows, or " (ASSUMPTION)" in its title: Shazia and Rafiq each cite six sessions; Kamran cites two and carries the label.
- [x] Every persona has exactly one primary job statement: one "When... I want... so I can" line each.
- [x] No two personas share the same job with only demographic differences: paying without a trip, keeping a transaction at the counter, and paying from a standing balance are three different behaviors, not three names for one.
- [x] Each persona names its anti-persona and the behavioral difference: Shazia names Kamran, Kamran names Shazia, Rafiq names the rival bill-shop proprietor his referrals currently enrich.
- [x] Unevidenced claims are listed, not hidden: Kamran's "measured or judged by" and "what they distrust" fields, and Rafiq's uncounted lost-referral total, are marked Open rather than guessed at.

This file does not decide Gate 1 on its own: [sahulat-journey.md](sahulat-journey.md) records attempt 1's MORE DISCOVERY (2026-02-20, on the cost-of-inaction and success-signal lines, neither of which lives here) and attempt 2's GO (2026-02-27), both signed in the gate file itself, by Hira Baig and Faisal Mirza, not here.
