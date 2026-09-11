# User Story Map: Sahulat Bill Pay

Fills [frameworks/prioritization/user-story-map.md](../frameworks/prioritization/user-story-map.md). Everything here is invented: Sahulat, its people, agents, customers, billers, bank, aggregator and telco are fiction, and every number is ILLUSTRATIVE, chosen so that this worksheet agrees with [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md).

**Owner:** Hira Baig, Product Manager · **Date:** 2026-03-10 · **Stage:** DEFINE

## What it is for

This map turns Shazia's bill-paying journey into a smallest usable path and then separates the later slices. The backbone is written from Shazia's side:

**know what is owed, look up, fund, pay, hold proof, recover**

The walking skeleton is SAHULAT-S1 followed by SAHULAT-S2. The fund column is deliberately narrow: the skeleton rests on an existing wallet balance, which is the Kamran assumption rather than a validated fact. SAHULAT-S3 adds cash-in and pay in one visit after the skeleton.

## Run it when

- Turning the Sahulat one-pager into stories before acceptance criteria are attached.
- Planning Rel-1 so that every part of the bill-paying journey has a usable path.
- Making the balance-first work visible instead of allowing it to hide inside the main payment column.

**Skip it when:** there is no user journey to map. Sahulat has a journey with a start, payment, proof and recovery, so the map is needed.

## Inputs you need first

- Shazia's journey and evidence in [sahulat-journey.md](sahulat-journey.md).
- The coverage and identifier supplement in [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md).
- The actors P1 Shazia, P2 Rafiq and P3 Kamran, where Kamran is labelled **ASSUMPTION**.
- The Sahulat story register identifiers SAHULAT-S1 to SAHULAT-S11.
- Capacity for BUILD: **Open: Zainab Qureshi** on 2026-03-10. N8's figure was not agreed until the capacity note of 2026-04-16, five weeks after this map and one day after Gate 3, just before BUILD starts on 2026-04-20; see the postscript under Step 3.
- Acceptance criteria references AC-1 to AC-13, added to the cards on 2026-03-13, after this map was dated.

## The worksheet

### Step 1: the backbone

| Activity (left to right) | Actor | Steps, in order |
|---|---|---|
| Know what is owed | Shazia | Have a bill to pay; know the amount and due date |
| Look up | Shazia | Enter the Ravi Power reference; receive the amount and due date |
| Fund | Shazia | Use an existing wallet balance; or cash in at an agent in the same visit |
| Pay | Shazia | Confirm payment; prevent a duplicate; handle biller posting failure |
| Hold proof | Shazia | Receive an SMS reference for the payment |
| Recover | Shazia, then support | Know what happened after a dropped session; get support lookup by reference |

The skeleton's fund step is explicitly **existing balance only**, resting on the Kamran assumption. The same-visit cash-in path is SAHULAT-S3, not a prerequisite for the walking skeleton.

### Step 2: the map

| Slice | Know what is owed | Look up | Fund | Pay | Hold proof | Recover |
|---|---|---|---|---|---|---|
| 1, walking skeleton | SAHULAT-S1 returns the amount and due date | SAHULAT-S1, Ravi Power by reference over USSD | Existing wallet balance, assumption carried by Kamran | SAHULAT-S2 pays from the existing balance | SAHULAT-S2 sends an SMS reference | SAHULAT-S2 covers the payment result and posting outcome |
| 2 | SAHULAT-S6 extends the known bill path to Chenab Gas | SAHULAT-S6, Chenab Gas lookup | SAHULAT-S3, cash in at an agent | SAHULAT-S3, same-visit cash-in and pay; SAHULAT-S6, gas payment | SAHULAT-S3 and SAHULAT-S6 use the payment proof path | SAHULAT-S8 reports whether money moved after a dropped session; SAHULAT-S9 supports lookup by reference |
| 3, balance-first plus Mehran Water | SAHULAT-S11 reminds Shazia about a saved bill's due date | SAHULAT-S5 saves the reference; SAHULAT-S10 provides the app lookup path | SAHULAT-S11 supports cash-in before a surcharge, but remains balance-first | SAHULAT-S10 provides the app pay path; SAHULAT-S7, still alive on 2026-03-10, extends the same path to Mehran Water | SAHULAT-S10 uses the same proof path | SAHULAT-S8 and SAHULAT-S9 remain the recovery path |
| Parking lot, no step | Merchant QR and bill-linked credit are outside this map | | | | | |

Within each column, the stories are ordered by necessity. The walking skeleton has no empty journey column because the existing balance is the fund mechanism, SAHULAT-S2 supplies payment and proof, and the payment result supplies the initial recovery outcome.

The balance-first slice is intentionally inside Rel-1. It contains SAHULAT-S5, SAHULAT-S10 and SAHULAT-S11, and depends on the assumption that customers will hold a balance. SAHULAT-S7 rides in the same slice for capacity reasons only; it is not itself balance-first, it is the Mehran Water lookup-and-pay path, still alive on this map's date. SAHULAT-S4 is not in this map's Rel-1 slice. It belongs in Rel-2.

### Step 3: the release line

| Release | Slices included | Outcome it must produce | Test that it walked | Capacity used |
|---|---|---|---|---|
| Rel-1 | Slice 1, slice 2 and the balance-first slice in slice 3 | A bill due in the household is paid through Sahulat before its due date, and no late surcharge is paid that month | Shazia looks up one Ravi Power bill by reference over USSD, pays it from an existing wallet balance, receives the SMS reference, and can establish the payment result | Open: Zainab Qureshi owns capacity sizing; no capacity figure is agreed as of 2026-03-10 (N8 settles it only on 2026-04-16, see the postscript below) |
| Rel-2 | SAHULAT-S4, the agent-handset confirmation path | Rafiq can vouch for a bill payment when asked | Rafiq sees the confirmation on his handset after a real same-visit payment and can repeat back the reference when asked | Open: Zainab Qureshi owns capacity sizing |

Capacity is **Open: Zainab Qureshi** as of this map's date, 2026-03-10.

**Postscript, dated 2026-04-16 (after Gate 3, accepted 2026-04-15, and just before BUILD starts on 2026-04-20):** N8 settles the figure as **4 engineers x 7 weeks = 28 engineer-weeks**, plus 1 QA and the PM. This is recorded here as a dated later annotation, the same way the AC-13 references and the S7 status are handled elsewhere in this map, not as a fact known when the map was drawn.

No story-size allocation is asserted in this map. Sizes remain **Open: Zainab Qureshi**, and the release capacity decision remains **Open: Zainab Qureshi**.

### Story cards

Acceptance-criteria references were added to the cards on 2026-03-13. The map itself is dated 2026-03-10, so the references are recorded as a later traceability update.

| ID | Story (as a [actor], I need [step] so that [outcome]) | Step | Slice | Acceptance criteria ref | Size |
|---|---|---|---|---|---|
| SAHULAT-S1 | As Shazia, I want to look up my Ravi Power bill by the reference number printed on it over USSD, so that I know the amount and due date without the paper bill | Look up; know what is owed | 1, walking skeleton | AC-1, AC-2 | Open: Zainab Qureshi |
| SAHULAT-S2 | As Shazia, I want to pay the bill from my wallet balance and get an SMS with a reference, so that I hold proof before the due date | Fund; pay; hold proof; recover | 1, walking skeleton | AC-3, AC-4, AC-9, AC-10, AC-13 | Open: Zainab Qureshi |
| SAHULAT-S3 | As Shazia, I want to cash in at an agent and pay the bill in the same visit, so that I make no second trip | Fund; pay; hold proof | 2 | AC-5 | Open: Zainab Qureshi |
| SAHULAT-S4 | As Rafiq, I want to see a confirmation on my agent handset when a customer I cashed in pays a bill, so that I can vouch for it when asked | Recover | Rel-2 | D8, next pass | Open: Zainab Qureshi |
| SAHULAT-S5 | As Shazia, I want to save a reference after paying, so that next month I do not re-enter it | Look up | 3, balance-first, Rel-1 | N54 | Open: Zainab Qureshi |
| SAHULAT-S6 | As Shazia, I want to pay a Chenab Gas bill the same way, so that both monthly bills go through one channel | Know what is owed; look up; pay | 2 | AC-6 | Open: Zainab Qureshi |
| SAHULAT-S7 | As Shazia, I want to pay a Mehran Water bill the same way, so that the same channel covers another household bill | Pay | 3, alive on 2026-03-10 | Open on 2026-03-10; later reference was N58 and D5 | Open: Zainab Qureshi |
| SAHULAT-S8 | As Shazia, I want a session that drops mid-payment to tell me whether money moved, so that I do not pay twice | Recover | 2 | AC-7, AC-8, AC-10 | Open: Zainab Qureshi |
| SAHULAT-S9 | As a support agent on Naveed's team, I want to look up a bill payment by reference, so that I answer "did it go through" on the first call | Recover | 2 | AC-11 | Open: Zainab Qureshi |
| SAHULAT-S10 | As Shazia on the app, I want the same lookup and pay flow, so that I am not forced onto USSD | Look up; pay | 3, balance-first, Rel-1 | N54 | Open: Zainab Qureshi |
| SAHULAT-S11 | As Shazia, I want an SMS three days before a saved bill's due date, so that I cash in before the surcharge | Know what is owed; fund | 3, balance-first, Rel-1 | AC-12, N54 | Open: Zainab Qureshi |

Story arithmetic by map slice is:

- Walking skeleton: SAHULAT-S1 + SAHULAT-S2 = the minimum lookup-to-payment path.
- Rel-1 balance-first slice: SAHULAT-S5 + SAHULAT-S10 + SAHULAT-S11 = the three balance-first stories.
- Rel-2 addition: SAHULAT-S4 = the agent confirmation story.
- The full register remains SAHULAT-S1 to SAHULAT-S11. SAHULAT-S7 is alive on 2026-03-10 and is not treated as killed in this worksheet.

## Reading the result

The smallest useful path is deliberately narrow:

1. Shazia knows the amount and due date from SAHULAT-S1.
2. Shazia uses an existing wallet balance in the fund column.
3. Shazia pays through SAHULAT-S2.
4. Shazia receives proof through the SMS reference.
5. Shazia can establish the result if the session or biller posting fails.

The map does not pretend that cash-in is unnecessary. It marks the fund column as resting on an existing balance because that is the Kamran assumption. SAHULAT-S3 is therefore a necessary second slice for a more representative journey, not a hidden prerequisite for the skeleton.

The balance-first work is visible as a separate slice inside Rel-1:

- SAHULAT-S5 saves the reference.
- SAHULAT-S10 adds the app path.
- SAHULAT-S11 adds the due-date reminder.

SAHULAT-S4 is held for Rel-2 because it serves the agent confirmation path. SAHULAT-S7 remains alive on 2026-03-10, with its later fate not backdated into this map.

Capacity and story sizes are not guessed at. As of 2026-03-10, capacity remains **Open: Zainab Qureshi**, same as card sizes; N8's figure, 4 engineers x 7 weeks = 28 engineer-weeks, was only agreed on 2026-04-16 (see the postscript under Step 3) and is not treated as known at this map's date.

## ILLUSTRATIVE example

Sahulat's bill-paying journey is the worked example. Shazia's backbone is:

**know what is owed, look up, fund, pay, hold proof, recover**

The walking skeleton is:

**SAHULAT-S1, look up a Ravi Power bill by reference, then SAHULAT-S2, pay from an existing wallet balance and receive an SMS reference.**

The map's release arithmetic is:

- Rel-1 includes slices 1, 2 and 3.
- The balance-first slice contains SAHULAT-S5, SAHULAT-S10 and SAHULAT-S11.
- Rel-2 contains SAHULAT-S4.
- Capacity is **Open: Zainab Qureshi** on the map's date; N8 later settles it at 4 engineers x 7 weeks = 28 engineer-weeks, plus 1 QA and the PM, via the 2026-04-16 postscript.
- Size allocation is **Open: Zainab Qureshi**.

## The trap

The trap is building the balance-first or payment column downward while leaving the journey incomplete. For Sahulat, that would mean spending effort on saved references, the app flow and reminder SMS while failing to preserve the end-to-end path from lookup to payment proof and recovery.

The mechanical rule is:

**No balance-first story starts until the walking skeleton is complete and observed end to end.**

A second trap is silently replacing the existing-balance assumption with a cash-in story. The map keeps them separate. Existing balance is the skeleton's fund mechanism. SAHULAT-S3 is the same-visit cash-in slice. The assumption is visible so that the team can test it rather than mistake it for evidence.

A third trap is backdating later knowledge. On 2026-03-10, SAHULAT-S7 was alive. The acceptance-criteria references were added on 2026-03-13. Later BUILD evidence and D5 are not used to rewrite this DEFINE map.

## Feeds

- [sahulat-journey.md](sahulat-journey.md): canonical Sahulat journey, data sheet, story identifiers, actors and timeline.
- [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md): supplement confirming the 2026-03-10 map date, the later 2026-03-13 acceptance-criteria update, N8 capacity and the open sizing convention.
- [templates/definition/acceptance-criteria.md](../templates/definition/acceptance-criteria.md): one acceptance-criteria set per story card, feeding Gate 2.
- [templates/definition/prd.md](../templates/definition/prd.md): story and functional scope inputs.
- [templates/planning/roadmap.md](../templates/planning/roadmap.md): Rel-1 and Rel-2 release rows.
- [knowledge/INDEX.md](../knowledge/INDEX.md): method background for user story mapping, based on Jeff Patton's story mapping practice (2005) and the book *User Story Mapping* (2014).
