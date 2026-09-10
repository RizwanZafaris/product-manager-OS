# Acceptance Criteria: Sahulat Bill Pay

Fills [templates/definition/acceptance-criteria.md](../templates/definition/acceptance-criteria.md). Everything here is invented: Sahulat, BillBridge, Darya Bank and Falak Telecom are all fictional, and every threshold below is chosen so this pass-or-fail contract agrees with the rest of the Sahulat journey, not to describe any real USSD gateway or bill-pay integration. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager · **Date:** 2026-03-13 · **Status:** Returned at Gate 2 attempt 1 (2026-03-18) for an unnumbered threshold in AC-3 and a guardrail with no digit; approved at attempt 2 (2026-03-25); the clause naming Mehran Water inside AC-6 struck 2026-05-21 per D5; verified at Gate 4 on 2026-06-10 with one listed miss, AC-8's resume half, owner Zainab Qureshi
**Covers:** [Rel-1 scope, the one-pager](sahulat-one-pager.md) · story ids SAHULAT-S1 to S11 in [the journey's shared identifiers](sahulat-journey.md#shared-identifiers) · sector cards: [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md), [payments acquiring](../knowledge/domains/payments-acquiring.md)

## 1. Criteria

Thirteen criteria, AC-1 to AC-13, ids fixed by the data sheet and never renumbered. D2 set this journey's weight at one-pager plus stories plus criteria, not the BRD or FRD stack, so every criterion verifies a SAHULAT-S# story directly; no FR ids exist. Grouped under the three epics the story register uses.

**EP1: Look up and pay a bill (SAHULAT-S1, S2, S5, S6, S7, S10, S11)**

### AC-1 verifies SAHULAT-S1 (happy path)

```
GIVEN a wallet holder dialed into the USSD bill-pay menu with a Ravi Power reference in hand
WHEN  she enters the reference and confirms the lookup
THEN  the menu returns biller, amount and due date within 8 seconds at p95 (ILLUSTRATIVE, N56) on Falak Telecom's gateway
```

- **Type:** happy path
- **Measurable threshold:** 8 seconds at p95 (ILLUSTRATIVE, N56)
- **Test data needed:** a valid Ravi Power reference in BillBridge's test catalogue (DEP-1)
- **Automatable:** yes

### AC-2 verifies SAHULAT-S1 (negative)

```
GIVEN the same menu
WHEN  the customer enters a reference BillBridge does not recognize
THEN  the menu returns "reference not found, check the number on your bill"; no debit, no state-machine record
```

- **Type:** negative
- **Measurable threshold:** binary outcome, no debit and no record
- **Test data needed:** a reference absent from BillBridge's 160-biller catalogue (N37)
- **Automatable:** yes

### AC-3 verifies SAHULAT-S2 (happy path)

```
GIVEN a looked-up Ravi Power bill and a wallet balance at or above the amount due
WHEN  the customer confirms payment
THEN  the wallet debits once, BillBridge is called, and an SMS carrying the payment reference arrives within 60 seconds (ILLUSTRATIVE, N56)
```

- **Type:** happy path
- **Measurable threshold:** 60 seconds (ILLUSTRATIVE, N56)
- **Test data needed:** a wallet funded above the bill amount
- **Automatable:** yes

### AC-4 verifies SAHULAT-S2 (negative)

```
GIVEN a looked-up bill and a wallet balance below the amount due
WHEN  the customer confirms payment
THEN  the menu declines, states the shortfall to the rupee, and offers a cash-in prompt; no debit
```

- **Type:** negative
- **Measurable threshold:** binary, shortfall shown equals bill minus balance exactly
- **Test data needed:** a wallet funded below a known bill amount
- **Automatable:** yes

### AC-6 verifies SAHULAT-S6 (happy path)

```
GIVEN a valid Chenab Gas reference
WHEN  the customer looks it up and pays it through the same flow used for Ravi Power
THEN  lookup, debit and SMS each meet the AC-1 and AC-3 thresholds, proving the flow is biller-agnostic
```

- **Type:** happy path
- **Measurable threshold:** same as AC-1 and AC-3 (ILLUSTRATIVE, N56)
- **Test data needed:** a valid Chenab Gas reference in BillBridge's catalogue
- **Automatable:** yes
- **Rejected option this document records:** at Gate 2 sign-off this GIVEN also named Mehran Water (SAHULAT-S7). N58, 2026-05-19: three of ten water test bills failed validation. D5, 2026-05-21: water dropped, S7 killed, id spent; struck from this clause rather than folded in silently, the criterion the one-pager calls re-signed against this gate.

### AC-9 verifies SAHULAT-S2 (negative, the acquiring card's question)

```
GIVEN a bill payment already debited, BillBridge having accepted the request
WHEN  BillBridge's posting to the biller fails after acceptance, the post-authorization fulfilment failure the acquiring card asks every product to answer
THEN  the debit is reversed to the wallet within 24 hours (ILLUSTRATIVE, N56) of detection, with an SMS saying the payment did not go through
```

- **Type:** negative, see [payments acquiring](../knowledge/domains/payments-acquiring.md), "approved payment, fulfilment fails afterward"
- **Measurable threshold:** 24 hours (ILLUSTRATIVE, N56)
- **Test data needed:** a simulated BillBridge posting failure in the DEP-1 sandbox
- **Automatable:** partially; failure injection is manual, the reversal timing check is not
- **Risk this answers:** R3, owner Hira Baig; did not arrive in the review window (0 confirmed, 4 unverified claims)

### AC-10 verifies SAHULAT-S2 (negative)

```
GIVEN a bill successfully paid for a given wallet, reference and bill month
WHEN  the same wallet attempts the identical reference and month again, the repeat-dial behavior E4 describes
THEN  the system blocks the second attempt for 24 hours (ILLUSTRATIVE, N56) and shows "already paid on [date], reference [x]"; no second debit
```

- **Type:** negative
- **Measurable threshold:** 24-hour block window (ILLUSTRATIVE, N56)
- **Test data needed:** one completed payment, replayed inside and outside the window
- **Automatable:** yes
- **Evidence:** T4, E4 (INT-007); exercised for real in launch week, when the AC-8 resume gap produced 61 duplicate-payment tickets (N47) before the fix shipped 2026-07-14

### AC-12 verifies SAHULAT-S11 (happy path, bundled negative half)

```
GIVEN a customer who saved a bill reference under SAHULAT-S5 with a due date on file
WHEN  three days remain before that due date
THEN  the wallet sends a reminder SMS naming biller, amount and due date
```

- **Type:** happy path plus a bundled negative half: a STOP reply suppresses further reminders for that reference. The data sheet fixes AC-12 as one id for both halves; a stricter reading would split it, not done here since ids are permanent and this contract closes at AC-13.
- **Measurable threshold:** 3 days before due date, per SAHULAT-S11's own wording (decided, not from N56); opt-out is binary
- **Test data needed:** a saved reference due in 3 days; a wallet that replies STOP
- **Automatable:** yes for scheduling; STOP parsing partly manual against Falak Telecom's rules
- **Note:** balance-first scope (N54); shipped and passed, but the metric it served, M2, missed badly at review (9 percent against 50)

### AC-13 verifies SAHULAT-S2 (negative, the tier limit)

```
GIVEN a wallet on a KYC tier whose limit is below the bill amount
WHEN  the customer attempts to pay a bill exceeding that limit
THEN  the payment is refused and the decline message states the tier's limit in rupees, not a generic "payment failed"
```

- **Type:** negative, see [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md), the tiered due-diligence question
- **Measurable threshold:** Open: Amna Rasheed owns the rupee figure. DEP-3's memo confirms bill pay sits within the licence's permitted activities, but no tier-limit value exists in the data sheet, so none is invented.
- **Test data needed:** a lowest-tier wallet, a bill above that tier's limit, once the figure exists
- **Automatable:** yes once the limit is set; blocked until then

**EP2: The agent counter (SAHULAT-S3, S4)**

### AC-5 verifies SAHULAT-S3 (happy path)

```
GIVEN a customer at an agent counter with no prior balance and a bill to pay
WHEN  the agent processes a cash-in of at least the bill amount
THEN  the credit is spendable within 30 seconds (ILLUSTRATIVE, N56), so the bill payment completes in the same visit
```

- **Type:** happy path
- **Measurable threshold:** 30 seconds (ILLUSTRATIVE, N56)
- **Test data needed:** an agent account carrying float; a wallet at zero balance
- **Automatable:** yes
- **Gap:** no edge or negative case exists for this story; see section 3

**EP3: Safety and support (SAHULAT-S8, S9)**

### AC-7 verifies SAHULAT-S8 (edge)

```
GIVEN a bill payment already debited, the idempotency key (ADR-2) written
WHEN  the session drops, the way E4 describes, before the confirmation screen renders
THEN  a status SMS confirming the payment went through reaches the customer within 2 minutes (ILLUSTRATIVE, N56)
```

- **Type:** edge
- **Measurable threshold:** 2 minutes (ILLUSTRATIVE, N56)
- **Test data needed:** a session forced to drop after the debit call
- **Automatable:** yes

### AC-8 verifies SAHULAT-S8 (edge, the Gate 4 miss)

```
GIVEN a bill payment where the idempotency key (ADR-2) is written but the debit has not posted
WHEN  the session drops before the debit step, the customer's next move a repeat dial rather than a wait (T4)
THEN  a status SMS saying nothing was charged reaches the customer within 2 minutes (ILLUSTRATIVE, N56), and the pending intent stays keyed to that wallet, reference and month so dialing again resumes the same bill at the same amount; the debit still posts only once
```

- **Type:** edge
- **Measurable threshold:** status SMS at 2 minutes (N56); resume is binary, the next session shows the bill pre-populated. Falak Telecom's gateway caps one session at 180 seconds (N66), so resume happens on a new dial, never inside the dropped one.
- **Test data needed:** a session forced to drop before the debit call, then a second dial from the same MSISDN
- **Automatable:** yes, once built
- **Gate 4 status, the accepted miss:** MET on the status-SMS half only; resume-on-next-dial was not built by 2026-06-10, accepted as a listed miss, deferred to Rel-2, owner Zainab Qureshi. In launch week it fed 61 duplicate-payment tickets (N47) and the M3 breach (87 percent against 90) behind D7's four-day halt (R2), the miss the retrospective names as the one that bit.

### AC-11 verifies SAHULAT-S9 (happy path)

```
GIVEN a support agent on Naveed Akhtar's team signed into the support console
WHEN  they search a payment reference read out over the phone
THEN  the console returns the payment's status, paid, reversed or pending, within 5 seconds (ILLUSTRATIVE, N56)
```

- **Type:** happy path
- **Measurable threshold:** 5 seconds (ILLUSTRATIVE, N56)
- **Test data needed:** one reference in each of the three statuses
- **Automatable:** yes
- **Gap:** no negative case for a reference the console cannot find. Open: Naveed Akhtar.

## 2. Edge and negative case coverage

| Story / FR | Edge or negative condition | Expected behavior | Criterion ID or reason not covered |
|---|---|---|---|
| SAHULAT-S1 | Reference BillBridge does not recognize | Decline message, no debit | AC-2 |
| SAHULAT-S2 | Balance below the bill amount | Declined, shortfall shown, cash-in offered | AC-4 |
| SAHULAT-S2 | BillBridge accepts, biller posting fails after | Reversed within 24 hours (N56), SMS sent | AC-9 |
| SAHULAT-S2 | Same reference and month paid twice | Blocked 24 hours (N56) | AC-10 |
| SAHULAT-S2 | Bill exceeds the wallet's KYC tier limit | Refused, limit named | AC-13, threshold Open: Amna Rasheed |
| SAHULAT-S3 | Agent float runs out before cash-in posts | Not per-transaction; R1 answers it, owner Tariq Sohail, risk register and Gate 5's condition |
| SAHULAT-S6 | Same failures as S1/S2, gas reference | Identical, shared engine | AC-2, AC-4, AC-9, AC-10; AC-6 proves only the happy path is biller-agnostic |
| SAHULAT-S7 | Mehran Water reference validation | Was inside AC-6's GIVEN at sign-off | Killed 2026-05-21 by D5 after N58; struck from AC-6, id spent |
| SAHULAT-S8 | Session drops after the debit posts | Status SMS within 2 minutes (N56) | AC-7 |
| SAHULAT-S8 | Session drops before the debit posts | Intent preserved (ADR-2), resumes on next dial | AC-8; resume half is the Gate 4 miss, owner Zainab Qureshi |
| SAHULAT-S9 | Reference not found by support | Not covered: no criterion for an unfound reference. Open: Naveed Akhtar |
| SAHULAT-S11 | Customer replies STOP to a reminder | No further reminder for that reference | AC-12, opt-out half |
| SAHULAT-S4 | Handset shows no confirmation for a payment it did not key in | Not covered: should story, Rel-2, D8's next-pass scope |
| SAHULAT-S5 | Saved reference reused after a biller changes format | Not covered: no dedicated criterion, out of scope after D8 |
| SAHULAT-S10 | App parity with USSD edge cases | Assumed to mirror them | Not covered: never re-verified at Gate 4. Open: Hira Baig |

## 3. Coverage summary

| Story / FR | Happy path ACs | Edge ACs | Negative ACs | Gaps |
|---|---|---|---|---|
| SAHULAT-S1 (must) | AC-1 | none | AC-2 | none |
| SAHULAT-S2 (must) | AC-3 | AC-9 | AC-4, AC-10, AC-13 | AC-13's threshold is Open, owner Amna Rasheed |
| SAHULAT-S3 (must) | AC-5 | none | none | No edge or negative criterion; agent float sits in R1. Owner Tariq Sohail |
| SAHULAT-S4 (should, Rel-2) | none | none | none | Deferred to Rel-2 under D8's next-pass scope |
| SAHULAT-S5 (should, balance-first) | none | none | none | No dedicated criterion; superseded by the D8 pivot |
| SAHULAT-S6 (must) | AC-6 | none | shared: AC-2, AC-4, AC-9, AC-10 | none |
| SAHULAT-S7 (must at sign-off, killed 2026-05-21) | none | none | none | Killed by D5 after N58; the criterion once inside AC-6 struck, re-signed against Gate 2; id spent |
| SAHULAT-S8 (must) | none | AC-7, AC-8 | none | AC-8's resume half is the accepted Gate 4 miss, owner Zainab Qureshi, deferred to Rel-2 |
| SAHULAT-S9 (should) | AC-11 | none | none | No negative case for an unfound reference. Open: Naveed Akhtar |
| SAHULAT-S10 (should, balance-first) | none | none | none | Assumed to mirror USSD criteria, not independently verified. Open: Hira Baig |
| SAHULAT-S11 (should, balance-first) | AC-12 | none | AC-12 (opt-out) | none |

**Must stories with zero negative cases:** SAHULAT-S3, owner Tariq Sohail, revisit by 2026-09-07 when the next DISCOVER pass opens. Its only DESIGN-stage failure mode, agent float running out, sits in R1 (likelihood 4 of 5) rather than in this contract, since it is a network-availability condition, not a per-transaction one; the reasoning is written here rather than left silent.

## How these criteria fail

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Restates the story | An early AC-1 draft read "the bill lookup works," SAHULAT-S1 with a period after it | AC-1 names the 8-second threshold and the exact fields returned, a behavior the story title does not already state |
| Could never fail | The AC-3 draft Gate 2 attempt 1 returned on 2026-03-18 read "the SMS arrives promptly" | Rewritten to "within 60 seconds" (ILLUSTRATIVE, N56) before attempt 2 signed 2026-03-25 |
| Happy path only | SAHULAT-S3 still carries this gap: only AC-5 exists, no edge or negative case | Flagged by name with an owner in section 3, not left silent |
| Adjectives as thresholds | The same 2026-03-18 return flagged a guardrail with no digit, on the north star sheet's M3 floor | Every threshold above carries a number sourced to N56, N66 or a story's own figure, except AC-13, which carries an owner instead |
| A tester cannot run it | An early idea for AC-9 read "handle the biller-side failure gracefully" | Rewritten to name the actor, the window (24 hours, ILLUSTRATIVE) and the customer-facing message |

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every must story and must FR has at least one criterion. SAHULAT-S1, S2, S3, S6 and S8 are the current Rel-1 musts and each has one; SAHULAT-S7 had one inside AC-6 until D5 struck it and killed the story.
- [x] Every criterion has one action and one observable outcome. AC-12 bundles a reminder and an opt-out under one id because the data sheet fixes it so; every other criterion carries a single GIVEN, WHEN and THEN.
- [ ] Every threshold is a number, labeled ILLUSTRATIVE where unagreed. AC-13's tier limit is not a number; it is Open, owner Amna Rasheed, pending a figure DEP-3's memo did not itself fix.
- [x] Every story has edge and negative coverage or a written reason. Section 2 carries a row and a criterion id or a named reason for all eleven live stories plus the dead SAHULAT-S7.
- [x] "Must stories with zero negative cases" says "none" or carries an owner and date. Section 3 names SAHULAT-S3, Tariq Sohail, 2026-09-07.
- [x] Model-driven criteria are paired with an eval spec reference. Not applicable: bill pay is a deterministic USSD and ledger flow with no model in the loop.

Signed at Gate 2 attempt 2, 2026-03-25, by Hira Baig as product owner and Faisal Mirza as sponsor, per `gates/gate-2-attempt-2.md` in the product workspace; this checklist is evidence for that signature, not a signature of its own. Verified against BUILD on 2026-06-10 by Mariam Gill, QA engineer, per `gates/gate-4-attempt-1.md`, with the one miss recorded above.
