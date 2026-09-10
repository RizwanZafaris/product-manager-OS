# Acceptance Criteria: Sahulat Bill Pay

Fills [templates/definition/acceptance-criteria.md](../templates/definition/acceptance-criteria.md). Everything here is invented: Sahulat, BillBridge, Darya Bank and Falak Telecom are all fictional, and every threshold below is chosen so this pass-or-fail contract agrees with the rest of the Sahulat journey, not to describe any real USSD gateway or bill-pay integration. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager · **Date:** 2026-03-13 · **Status:** Returned at Gate 2 attempt 1 (2026-03-18) for an unnumbered threshold in AC-3 and a guardrail with no digit; approved at attempt 2 (2026-03-25); the clause naming Mehran Water inside AC-6 struck 2026-05-21 per D5; verified at Gate 4 on 2026-06-10 with one listed miss, AC-8's resume half, owner Zainab Qureshi; annotated through 2026-08-28 (D8)
**Covers:** [Rel-1 scope, the one-pager](sahulat-one-pager.md) · story ids SAHULAT-S1 to S11 in [the journey's shared identifiers](sahulat-journey.md#shared-identifiers) · [sahulat-user-stories.md](sahulat-user-stories.md) · sector cards: [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md), [payments acquiring](../knowledge/domains/payments-acquiring.md)

## 1. Criteria

Thirteen criteria, AC-1 to AC-13, ids fixed by the data sheet and never renumbered. D2 set this journey's weight at one-pager plus stories plus criteria, not the BRD or FRD stack, so every criterion verifies a SAHULAT-S# story directly; no FR ids exist. Grouped under the three epics the story register uses. Each "verifies SAHULAT-S#" below names a story defined in [sahulat-user-stories.md](sahulat-user-stories.md). AC-7, AC-8 and AC-10 all come from one interview line, E4 (INT-007); the half of AC-8 accepted as a miss at Gate 4 is the exact defect that breached guardrail M3 in launch week.

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
- **Test data needed:** a well-formed Ravi Power reference that BillBridge returns as not found
- **Automatable:** yes

### AC-3 verifies SAHULAT-S2 (happy path)

```
GIVEN a looked-up Ravi Power bill and a wallet balance at or above the amount due
WHEN  the customer confirms payment
THEN  an SMS carrying the payment reference arrives within 60 seconds (ILLUSTRATIVE, N56)
```

- **Type:** happy path
- **Supporting assertions (not separately timed):** the wallet debits exactly once; BillBridge is called with the payment
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
- **Rejected option this document records:** at Gate 2 sign-off this GIVEN also named Mehran Water (SAHULAT-S7). N58, 2026-05-19: three of ten water test bills failed validation. D5, 2026-05-21 (decider Hira Baig, recorded in sahulat-decision-log.md): water dropped, S7 killed, id spent; struck from this clause rather than folded in silently. The one-pager calls this criterion re-signed against Gate 2 as a result of that decision.

### AC-9 verifies SAHULAT-S2 (negative, the acquiring card's question)

```
GIVEN a bill payment already debited, BillBridge having accepted the request
WHEN  BillBridge's posting to the biller fails after acceptance, the post-authorization fulfilment failure the acquiring card asks every product to answer
THEN  the debit is reversed to the wallet within 24 hours (ILLUSTRATIVE, N56) of the posting failure
```

- **Type:** negative; answers the question the payments-acquiring card raises about a payment approved by the network whose fulfilment fails afterward (see [payments acquiring](../knowledge/domains/payments-acquiring.md))
- **Supporting assertion (not separately timed):** an SMS saying the payment did not go through accompanies the reversal
- **Measurable threshold:** 24 hours (ILLUSTRATIVE, N56), clocked from the posting failure, not from when anyone notices it
- **Test data needed:** a simulated BillBridge posting failure in the DEP-1 sandbox
- **Automatable:** partially; failure injection is manual, run by Mariam Gill, the reversal timing check is not
- **Risk this answers:** R3, owner Hira Baig; did not arrive in the review window (0 confirmed, 4 unverified claims). AC-9 limits R3's cost to the customer's money (the debit is reversed); it does not prevent the surcharge itself if the biller's own posting deadline passes before the reversal completes.

### AC-10 verifies SAHULAT-S2 (negative)

```
GIVEN a bill successfully paid for a given wallet, reference and bill month
WHEN  the same wallet attempts the identical reference and month again, the repeat-dial behavior E4 describes
THEN  the second attempt for that same bill month is refused; no second debit ever posts for it
```

- **Type:** negative
- **Supporting assertions:** inside the 24-hour window (ILLUSTRATIVE, N56) the refusal message reads "already paid on [date], reference [x]"; outside that window the same bill month is still refused, since the idempotency key (ADR-2) is keyed per wallet, reference and bill month, not per 24 hours: the window bounds only the message wording, not the block itself
- **Measurable threshold:** binary refusal for the bill month; the 24-hour window (ILLUSTRATIVE, N56) bounds only the "already paid" message text
- **Test data needed:** one completed payment, replayed inside the 24-hour window and again after it, for the same bill month
- **Automatable:** yes
- **Evidence:** T4, E4 (INT-007); exercised for real in launch week, when the AC-8 resume gap produced 61 duplicate-payment tickets (N47) before the fix shipped 2026-07-14

### AC-12 verifies SAHULAT-S11 (happy path, bundled negative half)

```
GIVEN a customer who saved a bill reference under SAHULAT-S5 with a due date on file
WHEN  three days remain before that due date
THEN  the wallet sends a reminder SMS naming biller, amount and due date
```

The bundled negative half, same id:

```
GIVEN a wallet that has received a reminder SMS for a saved reference
WHEN  the wallet replies STOP
THEN  no further reminder SMS is sent for that reference
```

- **Type:** happy path plus a bundled negative half: a STOP reply suppresses further reminders for that reference. The data sheet fixes AC-12 as one id for both halves; a stricter reading would split it, not done here since ids are permanent and this contract closes at AC-13.
- **Measurable threshold:** 3 days before due date (ILLUSTRATIVE, from SAHULAT-S11's own wording, not from N56); opt-out is binary
- **Test data needed:** a saved reference due in 3 days; a wallet that replies STOP
- **Automatable:** yes for scheduling; STOP parsing partly manual against Falak Telecom's rules
- **Note:** balance-first scope (N54); shipped and passed, but the metric it served, M2, missed badly at review (9 percent against 50 percent)

### AC-13 verifies SAHULAT-S2 (negative, the tier limit)

```
GIVEN a wallet on a KYC tier whose limit is below the bill amount
WHEN  the customer attempts to pay a bill exceeding that limit
THEN  the payment is refused and the decline message states the tier's limit in rupees, not a generic "payment failed"
```

- **Type:** negative, see [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md), the tiered due-diligence question
- **Measurable threshold:** binary, not a rupee figure: the decline message states the configured limit for the wallet's tier in PKR, matching the tier configuration as deployed at Gate 4, owned by Amna Rasheed. DEP-3's memo confirms bill pay sits within the licence's permitted activities, but no tier-limit value exists in the data sheet, so none is invented; the deployed tier configuration is the source of truth this criterion checks against, not a number fixed here.
- **Test data needed:** a lowest-tier wallet, a bill above that tier's configured limit, and the deployed tier configuration to check the message against
- **Automatable:** yes

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
GIVEN a bill payment where the idempotency key (ADR-2) is written but the debit call has not yet been made
WHEN  the session drops before the debit step, the customer's next move a repeat dial rather than a wait, not knowing whether the money went (T4, E4)
THEN  a status SMS saying nothing was charged reaches the customer within 2 minutes (ILLUSTRATIVE, N56), and the pending intent stays keyed to that wallet, reference and month so dialing again resumes the same bill at the same amount; the debit still posts only once
```

- **Type:** edge, bundled like AC-12: a status-SMS half and a resume half under one id, the data sheet fixing AC-8 as one id for both. Gate 4 scored the two halves separately; see below.
- **Measurable threshold:** status SMS at 2 minutes (ILLUSTRATIVE, N56); resume is binary, the next session shows the bill pre-populated. Falak Telecom's gateway caps one session at 180 seconds (quoted, N66); resume happens on a new dial, never inside the dropped one.
- **Test data needed:** a session forced to drop before the debit call, then a second dial from the same MSISDN
- **Automatable:** yes, once built
- **Gate 4 status, the accepted miss:** MET on the status-SMS half only; resume-on-next-dial was not built by 2026-06-10, accepted as a listed miss, deferred to Rel-2, owner Zainab Qureshi. In launch week it fed 61 duplicate-payment tickets (N47) and the M3 breach (87 percent against 90 percent) behind D7's four-day halt (R2), the miss the retrospective names as the one that bit.

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
| SAHULAT-S1 | Lookup session nears the 180-second USSD ceiling (quoted, N66) | Not specified | Not covered: no boundary criterion. Open: Hira Baig |
| SAHULAT-S2 | Balance below the bill amount | Declined, shortfall shown, cash-in offered | AC-4 |
| SAHULAT-S2 | BillBridge accepts, biller posting fails after | Reversed within 24 hours (N56), SMS sent | AC-9 |
| SAHULAT-S2 | Same reference and month paid twice | Refused for that bill month, inside and outside the 24-hour window (N56) | AC-10 |
| SAHULAT-S2 | Bill exceeds the wallet's KYC tier limit | Refused, limit named | AC-13, tier configuration owned by Amna Rasheed |
| SAHULAT-S3 | Agent e-float below the cash-in amount at the counter | Declined, no partial credit, message names the shortfall | Not covered: this per-transaction case is unwritten because the criteria contract closes at AC-13; it would be the first id appended if this contract reopens. The separate network-availability condition (float exhausted across many transactions on a bill-peak day) sits in R1, owner Tariq Sohail, risk register and Gate 5's condition, not in this contract |
| SAHULAT-S6 | Same failures as S1/S2, gas reference | Identical, shared engine | AC-2, AC-4, AC-9, AC-10; AC-6 proves only the happy path is biller-agnostic; no gas-specific negative test data exists, the negatives are assumed to mirror Ravi Power via the shared criteria |
| SAHULAT-S6 | Same boundary as S1, gas reference | Not specified | Not covered: no boundary criterion, shared with S1. Open: Hira Baig |
| SAHULAT-S7 | Mehran Water reference validation | Was inside AC-6's GIVEN at sign-off | Killed 2026-05-21 by D5 after N58; struck from AC-6, id spent |
| SAHULAT-S8 | Session drops after the debit posts | Status SMS within 2 minutes (N56) | AC-7 |
| SAHULAT-S8 | Session drops before the debit posts | Intent preserved (ADR-2), resumes on next dial | AC-8; resume half is the Gate 4 miss, owner Zainab Qureshi |
| SAHULAT-S8 | Session drops with the debit call already made but its outcome not yet confirmed (in flight or unknown) | Not specified | Not covered: no criterion for this state. Open: Zainab Qureshi |
| SAHULAT-S8 | Same wallet, reference and month dialed again after a drop | Refused as already paid (N56), no second debit | AC-10, shared with S2; the repeat-dial case T4 and E4 describe |
| SAHULAT-S9 | Reference not found by support | Not specified | Not covered: no criterion for an unfound reference. Open: Naveed Akhtar |
| SAHULAT-S11 | Customer replies STOP to a reminder | No further reminder for that reference | AC-12, opt-out half |
| SAHULAT-S11 | Reminder scheduled near a due date that later changes | Not specified | Not covered: no boundary criterion. Open: Hira Baig |
| SAHULAT-S4 | Handset shows no confirmation for a payment it did not key in | Not specified | Not covered: should story, Rel-2, D8's next-pass scope |
| SAHULAT-S5 | Saved reference reused after a biller changes format | Not specified | Not covered: no criterion was written for S5 by Gate 4 (2026-06-10); the gap predates D8. Open: Hira Baig, closing user-stories open question row 2 |
| SAHULAT-S10 | App parity with USSD edge cases | Assumed to mirror them | Not covered: never re-verified at Gate 4, closing user-stories open question row 1. Open: Hira Baig |

## 3. Coverage summary

| Story / FR | Happy path ACs | Edge ACs | Negative ACs | Gaps |
|---|---|---|---|---|
| SAHULAT-S1 (must) | AC-1 | none | AC-2 | No boundary case for a lookup nearing the 180-second USSD ceiling (N66). Open: Hira Baig |
| SAHULAT-S2 (must) | AC-3 | none | AC-4, AC-9, AC-10, AC-13 | No edge case: no boundary criterion for a wallet balance exactly equal to the bill amount. Open: Hira Baig |
| SAHULAT-S3 (must) | AC-5 | none | none | No edge or negative criterion of its own; a per-transaction negative (agent e-float below the cash-in amount) is unwritten because the contract closes at AC-13, see section 2; agent float running out across a bill-peak day sits in R1. Owner Tariq Sohail |
| SAHULAT-S4 (should, Rel-2) | none | none | none | Deferred to Rel-2 under D8's next-pass scope |
| SAHULAT-S5 (should, balance-first) | none | none | none | No criterion was written for S5 by Gate 4, 2026-06-10; the gap predates D8. Open: Hira Baig, closing user-stories open question row 2 |
| SAHULAT-S6 (must) | AC-6 | none | shared: AC-2, AC-4, AC-9, AC-10 | No gas-specific negative test data; negatives assumed to mirror Ravi Power via the shared criteria. Owner Mariam Gill. No boundary case, shared with S1's gap. Open: Hira Baig |
| SAHULAT-S7 (must at sign-off, killed 2026-05-21) | none | none | none | Killed by D5 after N58; the criterion once inside AC-6 struck, re-signed against Gate 2; id spent |
| SAHULAT-S8 (must) | none | AC-7, AC-8 | none | AC-8's resume half is the accepted Gate 4 miss, owner Zainab Qureshi, deferred to Rel-2. The repeat-dial case T4 and E4 describe, S8's own failure mode, is exercised by AC-10, an S2 criterion; not in S8's own traceability, so it is not credited as S8's negative case, see below |
| SAHULAT-S9 (should) | AC-11 | none | none | No negative case for an unfound reference. Open: Naveed Akhtar |
| SAHULAT-S10 (should, balance-first) | none | none | none | Assumed to mirror USSD criteria, not independently verified since DEFINE. Open: Hira Baig, closing user-stories open question row 1 |
| SAHULAT-S11 (should, balance-first) | AC-12 | none | AC-12 (opt-out) | No boundary case for a reminder scheduled near a due date that later changes. Open: Hira Baig |

**Must stories with zero negative cases:** SAHULAT-S3 and SAHULAT-S8. The data sheet does not show what this line read at the 2026-03-25 signing: R1's likelihood score comes from the 2026-04-08 premortem and the 2026-09-07 revisit date from the 2026-08-28 Gate 6 pivot, both after that signature. As annotated through Gate 6: owner Tariq Sohail, revisit by 2026-09-07 when the next DISCOVER pass opens. A per-transaction negative does exist and is unwritten (agent e-float below the cash-in amount at the counter: declined, no partial credit, message names the shortfall; see section 2); it would be the first id appended if this contract reopens, since the contract closes at AC-13. The separate network-availability condition, agent float exhausted across a bill-peak day rather than at one transaction, sits in R1 (likelihood 4 of 5, premortem 2026-04-08), owner Tariq Sohail, risk register and Gate 5's condition, not in this contract; the reasoning is written here rather than left silent. SAHULAT-S8, added here 2026-08-28 (the same annotation pass as D8): AC-7 and AC-8 are both happy-path or edge criteria, and the repeat-dial negative T4 and E4 describe for this story is exercised by AC-10, an S2 criterion, not by any criterion in S8's own traceability (see the coverage table above), so it does not count as S8's negative case. Owner Zainab Qureshi, revisit alongside AC-8's resume-half fix in Rel-2.

## How these criteria fail

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Restates the story | An early AC-1 draft read "the bill lookup works," SAHULAT-S1 with a period after it | AC-1 names the 8-second threshold and the exact fields returned, a behavior the story title does not already state |
| Could never fail | The AC-3 draft Gate 2 attempt 1 returned on 2026-03-18 read "the SMS arrives promptly" | Rewritten to "within 60 seconds" (ILLUSTRATIVE, N56) before attempt 2 signed 2026-03-25 |
| Happy path only | SAHULAT-S3 still carries this gap: only AC-5 exists, no edge or negative case | Flagged by name with an owner in section 3, not left silent |
| Adjectives as thresholds | The same 2026-03-18 return flagged a guardrail row in the one-pager's section 4 with no digit in it | Every threshold above carries a number sourced to N56, N66 or a story's own figure, except AC-13, which carries a binary check against a tier table instead |
| A tester cannot run it | An early idea for AC-9 read "handle the biller-side failure gracefully" | Rewritten to name the actor, the window (24 hours, ILLUSTRATIVE) and the customer-facing message |

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every must story and must FR has at least one criterion. SAHULAT-S1, S2, S3, S6 and S8 are the current Rel-1 musts and each has one; SAHULAT-S7 had one inside AC-6 until D5 struck it and killed the story.
- [ ] Every criterion has one action and one observable outcome. AC-12 bundles a reminder and an opt-out under one id because the data sheet fixes it so, and AC-8 bundles a status-SMS half and a resume half under one id for the same reason; each half of AC-8 carries its own Gate 4 result, and only the status-SMS half was met. AC-3, AC-9 and AC-10 have been trimmed to a single THEN outcome with supporting assertions carried separately. Left unchecked because AC-8 and AC-12 remain two-outcome criteria by the data sheet's own id allocation.
- [x] Every threshold is a number, labeled ILLUSTRATIVE where unagreed, or a binary check with a named owner where no number exists. AC-13's tier limit is not a number; it checks the decline message against a tier table Amna Rasheed owns, no figure invented.
- [x] Every story has edge and negative coverage or a written reason. Section 2 carries a row and a criterion id or a named reason for all ten live stories plus the dead SAHULAT-S7.
- [x] "Must stories with zero negative cases" says "none" or carries an owner and date. Section 3 names SAHULAT-S3, owner Tariq Sohail, as annotated through Gate 6, revisit 2026-09-07; what the line read at the original 2026-03-25 signing is not recorded here.
- [x] Model-driven criteria are paired with an eval spec reference. Not applicable: bill pay is a deterministic USSD and ledger flow with no model in the loop.

The 2026-03-25 signature by Hira Baig as product owner and Faisal Mirza as sponsor rests on `gates/gate-2-attempt-2.md` in the product workspace. This exit gate is walked again here, after Gate 6 (2026-08-28), to show the contract's current state, not as fresh evidence for that earlier signature; it cites R1's premortem likelihood (2026-04-08), the 2026-09-07 revisit date and D8's pivot, none of which existed when Gate 2 was signed. Verified against BUILD on 2026-06-10 by Mariam Gill, QA engineer, per `gates/gate-4-attempt-1.md`, with the one miss recorded above.
