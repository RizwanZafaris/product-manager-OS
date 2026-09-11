# User Stories: Sahulat Bill Pay

Fills [templates/definition/user-stories.md](../templates/definition/user-stories.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, every id, date and figure below is carried from the data sheet in [sahulat-journey.md](sahulat-journey.md), and none of it describes a real wallet, biller, bank or regulator decision. See the [examples index](README.md).

**Feature:** Sahulat Bill Pay, paying an electricity or gas bill from the wallet with cash-in through the agent network · **PRD:** [sahulat-one-pager.md](sahulat-one-pager.md), the artifact weight D2 chose over the BRD or FRD stack · **Owner:** Hira Baig, Product Manager, the only PM in the company · **Personas:** [sahulat-personas.md](sahulat-personas.md) · **First written:** 2026-03-11 · **Last refined:** 2026-05-21, the day D5 killed SAHULAT-S7, annotated through 2026-08-28 (D8) · **Status:** SIGNED at Gate 2 attempt 2, 2026-03-25; the affected criterion re-reviewed against Gate 2 on 2026-05-21 per D5, recorded in sahulat-decision-log.md

## 1. The slice this release ships

**Walking skeleton (the thinnest end-to-end path):** Shazia looks up her Ravi Power bill by the reference number printed on it, over USSD, pays it from her wallet balance, and receives an SMS with a payment reference: the thinnest working path through EP1, and the first two rows of the story register below. This skeleton assumes a standing wallet balance that P1's own evidence contradicts: six of eight customer sessions show money leaving the wallet the day it arrives (E2, T2), and a held balance is what P3, Kamran, the ASSUMPTION persona, evidences on two sessions only. See [frameworks/prioritization/user-story-map.md](../frameworks/prioritization/user-story-map.md) for the backbone this skeleton is drawn from.

| Release | What a user can do afterwards that they could not before | Stories included |
|---|---|---|
| Rel-1 | Shazia can look up and pay a Ravi Power or Chenab Gas bill, either from a wallet balance she already holds or from cash she hands an agent in the same visit, get an SMS she can show as proof, learn whether money moved if her USSD session drops mid-payment (the report half; resume-on-redial deferred to Rel-2 per the Gate 4 split, section 4), and reach a support agent who can answer "did it go through" on the first call. | SAHULAT-S1, S2, S3, S5, S6, S8, S9, S10, S11 |
| Rel-2 | Rafiq sees a confirmation on his own agent handset for a bill payment he enabled, so he can vouch for it without a call to Naveed's helpline; a Mehran Water bill can be paid the same way, once a story replaces the one D5 killed; a dropped session before the debit call resumes on the next dial rather than only reporting. | SAHULAT-S4; SAHULAT-S8 resume half (AC-8), owner Zainab Qureshi; a water story to replace SAHULAT-S7, no id assigned yet. Open: Hira Baig, gated on a validated Mehran Water reference feed |
| Later | Nothing is scheduled past Rel-2 as of this refinement. | None |

## 2. Epics

O1 names the outcome signal Gate 1 attempt 2 set on 2026-02-27, carried in unchanged: a bill due in the household is paid through Sahulat before its due date, and no late surcharge is paid that month; the record is `gates/gate-1-attempt-2.md`. This section is where the signal is defined and labelled O1; the one-pager cites this same signal in its section 4, without repeating the label, and measures it through M1 and M2. Every story below serves it; the epics just group the paths to it (EP1 to EP3 in the data sheet). EP2 answers [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md) question 1, who this is for, including an agent acting on a customer's behalf; the card's separate point about the agent's cash float being as much a part of uptime as a server log stays with risk R1, not a story here. EP1 answers the question the [payments acquiring](../knowledge/domains/payments-acquiring.md) card asks better than any other, what happens when a payment is approved and fulfilment fails afterward: SAHULAT-S2's AC-9 and risk R3.

| Epic | Objective it serves (from [sahulat-one-pager.md](sahulat-one-pager.md)) | Stories | Status |
|---|---|---|---|
| EP1: Look up and pay a bill | O1, the direct path: look up, pay, hold proof; the payments-acquiring card's fulfilment-failure question lands here too, via SAHULAT-S2's AC-9 and risk R3 | SAHULAT-S1, S2, S5, S6, S10, S11; SAHULAT-S7 killed, see section 3 | In BUILD. S1, S2, S6 are Rel-1 musts; S5, S10, S11 are Rel-1 shoulds |
| EP2: The agent counter | O1, and answers the cost of inaction the second trip prices: a customer who cashes in and pays in one visit makes no second trip (N20, N21, ILLUSTRATIVE, estimate) | SAHULAT-S3, S4 | S3 in BUILD for Rel-1; S4 not started, Rel-2 |
| EP3: Safety and support | O1, protected on the failure side: a customer who cannot trust that a dropped session did or did not move money will not pay before the due date either, and a support agent who cannot confirm a payment on the first call erodes the same trust | SAHULAT-S8, S9 | In BUILD |

## 3. The story register

| ID | Story | Persona | Priority | Acceptance criteria | Estimate | Status | Notes |
|---|---|---|---|---|---|---|---|
| SAHULAT-S1 | As Shazia, I want to look up my Ravi Power bill by the reference number printed on it over USSD, so that I know the amount and due date without the paper bill. | Shazia (P1) | must, Rel-1 | AC-1, AC-2 | Open: Zainab Qureshi | In BUILD | Walking skeleton, first half; the reference field is the one N58 later found unreliable for Mehran Water |
| SAHULAT-S2 | As Shazia, I want to pay the bill from my wallet balance and get an SMS with a reference, so that I hold proof before the due date. | Shazia (P1) | must, Rel-1 | AC-3, AC-4, AC-9, AC-10, AC-13 | Open: Zainab Qureshi | In BUILD | Walking skeleton, second half; ships only with S1, see section 4, Independent |
| SAHULAT-S3 | As Shazia, I want to cash in at an agent and pay the bill in the same visit, so that I make no second trip. | Shazia (P1) | must, Rel-1 | AC-5 | Open: Zainab Qureshi | In BUILD | Depends on Tariq Sohail's agent float at the counter (risk R1), not a story dependency |
| SAHULAT-S4 | As Rafiq, I want to see a confirmation on my agent handset when a customer I cashed in pays a bill, so that I can vouch for it when asked. | Rafiq (P2) | should, Rel-2 | None drafted, see Open questions row 5 | Open: Zainab Qureshi | Not started | No confirmation view for Rafiq today; agents field bill questions daily (T3, E3), but that a bill he enabled is invisible to him unless the customer says so is a design inference, not sourced to an evidence id |
| SAHULAT-S5 | As Shazia, I want to save a reference after paying, so that next month I do not re-enter it. | Shazia (P1) | should, Rel-1 | None drafted, see Open questions row 2 | Open: Zainab Qureshi | In BUILD | Balance-first slice with S10, S11; N54 (ILLUSTRATIVE, measured) totalled 9 of 28 engineer-weeks across the three once BUILD closed on 2026-06-05, after this section was last refined. Also serves P3, Kamran, ASSUMPTION at Gate 1, on two sessions only |
| SAHULAT-S6 | As Shazia, I want to pay a Chenab Gas bill the same way, so that both monthly bills go through one channel. | Shazia (P1) | must, Rel-1 | AC-6 | Open: Zainab Qureshi | In BUILD | Data variation split (section 5) applied once; Mehran Water was to be the second application until D5 |
| SAHULAT-S8 | As Shazia, I want a session that drops mid-payment to tell me whether money moved, so that I do not pay twice. | Shazia (P1) | must, Rel-1 | AC-7, AC-8, AC-10 (shared with S2) | Open: Zainab Qureshi | In BUILD, resume half flagged, see section 4 | From E4, the dropped-session line in INT-007; ADR-2's idempotency key is the report-half mechanism |
| SAHULAT-S9 | As a support agent on Naveed's team, I want to look up a bill payment by reference, so that I answer "did it go through" on the first call. | Naveed Akhtar's support team, not P1, P2 or P3, see the exit gate below | should, Rel-1 | AC-11 | Open: Zainab Qureshi | In BUILD | No formal persona exists for the support desk today |
| SAHULAT-S10 | As Shazia on the app, I want the same lookup and pay flow, so that I am not forced onto USSD. | Shazia (P1) | should, Rel-1 | Inherits AC-1 to AC-5 by interface parity, not independently drafted, see Open questions row 1 | Open: Zainab Qureshi | In BUILD | Balance-first slice (N54); Interface pattern (section 5), built to the same criteria after the USSD walking skeleton |
| SAHULAT-S11 | As Shazia, I want an SMS three days before a saved bill's due date, so that I cash in before the surcharge. | Shazia (P1) | should, Rel-1 | AC-12 | Open: Zainab Qureshi | In BUILD | Balance-first slice (N54); depends on S5's saved reference, a designed dependency like S2 on S1 |

Estimate: this squad does not point stories. BUILD capacity is tracked as engineer-weeks against the capacity note (N8, ILLUSTRATIVE, estimate: 4 engineers times 7 weeks equals 28 engineer-weeks), not per story, so every Estimate cell above reads Open: Zainab Qureshi, the engineering lead.

**Killed or superseded stories.** Never delete a row; move it here so the id stays spent.

| ID | Story | Why it is dead | Superseded by |
|---|---|---|---|
| SAHULAT-S7 | As Shazia, I want to pay a Mehran Water bill the same way (must at Gate 2). | Killed by D5, 2026-05-21: 3 of 10 Mehran Water test bills failed reference validation (N58, ILLUSTRATIVE, measured, 2026-05-19). Fixing the feed before the Rel-1 date would have pushed Gate 4, so the story was dropped and the date was not. No INVEST verdict for SAHULAT-S7 was ever filed, a gap already present at Gate 2 attempt 2 signing on 2026-03-25 and never closed before D5 killed the story; it is struck rather than carried forward. | Open: Hira Baig, no replacement id assigned yet; the open Rel-2 candidate named in section 1, gated on BillBridge or Mehran Water fixing the feed. The replacement takes a new id; SAHULAT-S7 is never reused |

## 4. INVEST check

| Letter | It fails when | The question to ask |
|---|---|---|
| **I**ndependent | It cannot ship unless another story ships first, and the order was not designed | What breaks if this ships alone? |
| **N**egotiable | It dictates the implementation, so there is nothing left to discuss with the team | Does this name a technology or a screen instead of a behaviour? |
| **V**aluable | Nobody outside the team is better off when it ships | Who can do something new, and what? |
| **E**stimable | The team cannot size it because something is unknown | What do we not know, and can we spike it instead? |
| **S**mall | It cannot finish inside one iteration | Which of the splitting patterns in section 5 applies? |
| **T**estable | No criterion could fail | Write the criterion that fails. If you cannot, the story is a wish |

Run on the six Rel-1 musts at Gate 2 attempt 2 (2026-03-25), when SAHULAT-S7 was still a must: no verdict was filed for SAHULAT-S7, a gap already present at that signing (see the dead table in section 3), and the story was killed by D5 before it could be closed. The table below holds only the 2026-05-21 re-run, covering the five musts that remained after D5; the original six Gate 2 verdicts are not reproduced here. Verdicts recorded, not assumed.

| Story | I | N | V | E | S | T | Verdict |
|---|---|---|---|---|---|---|---|
| SAHULAT-S1 | Pass | Pass | Pass: knows amount and due date without the paper bill | Pass: sized against N56's 8-second p95 threshold | Pass: one screen, one gateway call | Pass: AC-1, AC-2 each name a failing case | PASS |
| SAHULAT-S2 | Designed dependency on S1, ships with it in Rel-1 | Pass | Pass: holds an SMS reference before the due date; the wallet-balance half of the walking skeleton (section 1) rests on P3's ASSUMPTION persona, not P1's own evidence (E2, T2) | Pass | Pass: pay-and-confirm is one slice; drop cases live in S8 | Pass: AC-3, AC-4, AC-9, AC-10, AC-13 | PASS |
| SAHULAT-S3 | Pass | Pass | Pass: no second trip (N20, N21) | Pass | Pass | Pass: AC-5 | PASS |
| SAHULAT-S6 | Designed dependency on S1 and S2, reuses their mechanism | Pass | Pass: one channel for both monthly bills | Pass | Pass: Data variation pattern, gas after electricity | Pass: AC-6 | PASS |
| SAHULAT-S8 | Designed dependency on S2, same shape as S2 on S1 | Pass | Pass: does not pay twice | Partial: the report half is sized against ADR-2's idempotency key; the resume half, continuing the debit on the next dial after a session drops before it posts, was not separately estimated at this re-run | Split: the report-only Rel-1 slice and the resume Rel-2 slice. Annotation, 2026-06-10 (Gate 4): split decided; the report half shipped in Rel-1, the resume half deferred to Rel-2, owner Zainab Qureshi | Pass: AC-7, AC-8 each name a failing case; AC-10 (shared with S2) covers the repeat-dial case | FAIL on E at this re-run; S resolved at Gate 4, 2026-06-10, by the split above |
| ~~SAHULAT-S7~~ | n/a | n/a | n/a | n/a | n/a | n/a | Killed by D5, 2026-05-21, before this re-run; see the dead table in section 3 |

## 5. Splitting a story that is too big

| Pattern | Split it by | Use it when |
|---|---|---|
| Workflow step | The steps of the user's journey | The story spans a whole journey |
| Happy path first | The path where nothing goes wrong, then each failure | Error handling is most of the size |
| Business rule variation | One rule now, the variants later | Rules differ by market, plan or tier |
| Effort | The cheap majority of cases, then the expensive tail | A small share of cases carries most of the cost |
| Data variation | One data type, format or currency, then the rest | The work scales with the number of input shapes |
| Interface | One platform or surface first | The behaviour is the same across several surfaces |

SAHULAT-S8 is the one must in section 3 that needs a split: section 4 records its resume half, a session that drops before the debit posts, continuing on the next dial, as not yet separately estimated from its report half, a session that drops after the debit posts. Both halves are failure paths, not a happy path and a failure path, so Effort applies instead, splitting by cost rather than by sequence: the report half, the cheap majority case, sized against ADR-2's idempotency key, ships in Rel-1 now; the resume half, the expensive tail, is the Rel-2 slice. Annotation, 2026-06-10 (Gate 4): split decided; the report half shipped in Rel-1, the resume half deferred to Rel-2, owner Zainab Qureshi. Every other must in section 3 is already one vertical slice. One further split was considered and rejected: SAHULAT-S2's "pay the bill" and "get an SMS with a reference" could split along Workflow step, since both halves are happy-path steps in Shazia's journey, but pulling the SMS out ships a debit with no confirmation Shazia can see, exactly the state AC-7 exists to catch (AC-8 covers a session dropped before any debit, a different state, so it does not bear on this rejected split). SAHULAT-S6 already shows Data variation applied once, gas after electricity; SAHULAT-S7 was its second application until D5 removed it, and the water story that replaces it will reuse the pattern rather than invent one. SAHULAT-S10 shows the Interface pattern: USSD carries the walking skeleton in Rel-1, and the app flow, also a Rel-1 should, is built to the same criteria after it; the pattern was not used to split the two surfaces across releases, since both ship in Rel-1.

## 6. Traceability

"O1" below is the Gate 1 attempt 2 outcome signal named and defined in section 2 above, cited without the label in the one-pager's section 4; every criterion id is defined in [sahulat-acceptance-criteria.md](sahulat-acceptance-criteria.md).

| Story | Serves objective | Detailed by (FRD requirement) | Verified by (AC) | Covered by test |
|---|---|---|---|---|
| SAHULAT-S1 | O1 | None: D2, 2026-03-05, chose the one-pager weight over the BRD or FRD stack | AC-1, AC-2 | Open: Mariam Gill, UAT scheduled 2026-06-15 to 2026-06-24 |
| SAHULAT-S2 | O1 | None (D2) | AC-3, AC-4, AC-9, AC-10, AC-13 | Open: Mariam Gill |
| SAHULAT-S3 | O1 | None (D2) | AC-5 | Open: Mariam Gill |
| SAHULAT-S4 | O1 | None (D2) | None drafted, see Open questions row 5 | Open: Mariam Gill |
| SAHULAT-S5 | O1 | None (D2) | None drafted, see Open questions row 2 | Open: Mariam Gill |
| SAHULAT-S6 | O1 | None (D2) | AC-6 | Open: Mariam Gill |
| SAHULAT-S8 | O1 | None (D2) | AC-7, AC-8, AC-10 (shared with S2) | Open: Mariam Gill |
| SAHULAT-S9 | O1 | None (D2) | AC-11 | Open: Mariam Gill |
| SAHULAT-S10 | O1 | None (D2) | None drafted, inherits AC-1 to AC-5 by parity, see Open questions row 1 | Open: Mariam Gill |
| SAHULAT-S11 | O1 | None (D2) | AC-12 | Open: Mariam Gill |

**Orphan check.** Run both directions and record the answer, not the intention.

- Stories serving no objective: none. All ten serve O1.
- Objectives with no story: none. O1 is the Gate 1 outcome signal this journey measures at this artifact weight, defined in section 2 above and cited without the label in the one-pager's section 4, and measured through M1 and M2, and every must and should above serves it.
- FRD requirements no story delivers: none, structurally. D2 (2026-03-05) chose the one-pager weight over the BRD or FRD stack, so there is no FRD for a requirement to orphan.
- Must-priority stories with no acceptance criteria: none. The five Rel-1 musts, SAHULAT-S1, S2, S3, S6 and S8, each carry at least one AC id.

## 7. Open questions

| # | Question | Blocks which stories | Owner | Needed by |
|---|---|---|---|---|
| 1 | Does SAHULAT-S10's app flow inherit AC-1 to AC-5 by interface parity, or does the app need its own criteria for the same failure modes | SAHULAT-S10 | Hira Baig, with Mariam Gill on the test side | 2026-06-10, Gate 4 attempt 1 |
| 2 | What is the testable criterion for SAHULAT-S5's saved-reference flow, since none of AC-1 to AC-13 covers save and reuse | SAHULAT-S5, SAHULAT-S11 (depends on S5) | Hira Baig | 2026-06-10, Gate 4 attempt 1 |
| 3 | Does SAHULAT-S9 get a named persona for Naveed's support desk in sahulat-personas.md, or is it re-attributed to an existing one | SAHULAT-S9 | Hira Baig | 2026-06-10, Gate 4 attempt 1 |
| 4 | Does a Mehran Water replacement for SAHULAT-S7 land in Rel-2 as section 1 already scopes it, or slip past Rel-2, once BillBridge or Mehran Water fixes the reference feed N58 found unreliable | Rel-2 scope, section 1 | Hira Baig, with Zainab Qureshi confirming feasibility | 2026-08-28, Gate 6 |
| 5 | Does SAHULAT-S4's agent-handset confirmation need its own acceptance criteria before Rel-2 planning starts, since none of AC-1 to AC-13 covers an agent-side view | SAHULAT-S4 | Hira Baig | 2026-09-07, next DISCOVER pass |

## Exit gate (feeds Gate 2: requirements signed off)

Gate 2 was signed by Hira Baig, Zainab Qureshi, Faisal Mirza and Amna Rasheed (regulatory owner, per STAGE-GATES: regulated, no model, signed with her D2 objection noted) on 2026-03-25, attempt 2, in `gates/gate-2-attempt-2.md`. D5 on 2026-05-21 sent the affected criterion back through Gate 2 rather than absorbing the change, and the checklist below is walked again here to answer whether the amended register still meets it, not to declare the gate passed a second time; that record belongs to the gate file and the two names on it.

- [x] Every must-priority story has an acceptance criteria id that could fail
- [ ] Every story names a persona that exists in [sahulat-personas.md](sahulat-personas.md): SAHULAT-S9 names "a support agent on Naveed's team," who is not P1, P2 or P3. This gap was already present when Gate 2 attempt 2 signed on 2026-03-25: the story's text is unchanged since then. Whether it was accepted as an exception at that signing is not recorded in the data sheet. See Open questions, row 3.
- [x] Every story states an outcome, not a screen and not a technology
- [ ] INVEST has been run on every must, and the verdicts are recorded rather than assumed (section 4): true of the 2026-05-21 re-run's five musts, but the original six Gate 2 attempt 2 verdicts from 2026-03-25, the signing this checklist answers for, were never reproduced and are not known to survive anywhere, SAHULAT-S7's among them (no verdict was ever filed for it either, per section 3 and section 4)
- [ ] No story in this release is too big to finish in one iteration, or it has been split and both halves re-checked: at this 2026-05-21 re-run, SAHULAT-S8's resume half, a session that drops before the debit posts, had not been estimated separately from its report half. See section 4, Estimable and Small. Annotation, 2026-06-10 (Gate 4): the split was decided then, report half to Rel-1, resume half to Rel-2.
- [x] The walking skeleton is named and Rel-1 delivers it end to end
- [x] Traceability is filled in both directions, and every orphan list says "none" or names an owner
- [x] Killed stories are in the dead table with their ids spent, not deleted
- [x] The worked example above has been removed
