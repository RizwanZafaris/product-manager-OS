# Design Sprint Runbook: Sahulat Bill Pay, agent-initiated payment (pass 2)

Fills [frameworks/discovery/design-sprint-runbook.md](../frameworks/discovery/design-sprint-runbook.md). Everything here is invented: Sahulat, its people, agents and customers are fiction, and every number and quote below is ILLUSTRATIVE, chosen so this sprint week agrees with the rest of the [Sahulat journey](sahulat-journey.md) and the [coverage sheet](sahulat-coverage-sheet.md) that extends it, not to describe any real mobile-money wallet or design sprint. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager, the only PM · **Week:** 2026-09-14 to 2026-09-18 · **Status:** Complete; D9 logged 2026-09-18; proof-format re-test scheduled 2026-09-24 and 2026-09-25

## What it is for

This is the second design sprint the journey runs, and the first one this repository's examples show worked end to end. It sits inside the pass-2 DISCOVER cycle that D8 opened on 2026-09-07 after the Gate 6 pivot to agent-assisted bill pay. The assumption map opened that day scored [AS-3](sahulat-coverage-sheet.md) (customers will confirm an agent-keyed payment on their own phone without handing over their PIN) and [AS-7](sahulat-coverage-sheet.md) (the licence permits an agent to initiate a payment with the customer's confirmation, owner Amna Rasheed, open) as untested and consequential enough to send straight to a sprint rather than to a build. The mom-test sessions two days earlier gave the sprint its raw material: E6, an agent's line about being handed a PIN he did not want, and E7, an agent describing a chit and a stamp standing in for a phone screen as proof. The service blueprint's failure points (the PIN, the missing slip) are the two the sprint tests directly.

## Run it when

- A problem is framed, the stakes are high, and the team is stuck between two or three directions. Here: keep letting agents hold customers' PINs, or build a confirmation the customer gives on her own phone, with the proof question (SMS alone, or SMS plus a physical slip) undecided either way.
- Interviews confirmed the pain but nobody knows whether the proposed shape of the solution lands. INT-015 to INT-020 confirmed agents already key bills and already improvise proof; nobody had shown a customer or an agent the actual flow.

**Skipped, on purpose:** whether the agent app can render a live confirmation screen within Rel-2 (AS-4) is feasibility, not desirability, and stays with Zainab Qureshi's engineering estimate rather than entering this week.

## Inputs you need first

- Problem framing carried over from the service blueprint's frontstage failure points, not a fresh one for this week.
- Evidence: E6, E7, N60 (5 of 6 pilot agent debriefs raised the paper-slip request), and the mom-test tallies (CN15 to CN17).
- Ten Friday participants, five agent-and-customer pairs from the same counters, confirmed by Tuesday: agents A-13 to A-17, customers C-09 to C-13.
- Decider Faisal Mirza committed to Monday, Wednesday and Friday afternoon before the week was booked.

## The worksheet

### 1. Roles

| Role | Who | Attended |
|---|---|---|
| Decider | Faisal Mirza, Chief Executive | Monday, Wednesday, Friday afternoon |
| Facilitator | Mariam Gill, QA engineer | All five days |
| Interviewer | Hira Baig, Product Manager | Thursday afternoon, Friday |
| Team | Zainab Qureshi (engineering lead); Tariq Sohail; Naveed Akhtar; Bilal Hasan; Usman Javed | All five days |
| Experts | Amna Rasheed, Head of Compliance | Monday afternoon only |

Five team members plus the facilitator and the decider is the method's seven-person room, with Hira Baig as interviewer on top; the squad this small could not spare a second engineer for the week, and Usman Javed sat in for field-reality checks rather than as a maker.

### 2. Schedule

| Day | Goal | Key exercises | Output |
|---|---|---|---|
| Monday, 2026-09-14 | Map | Long-term goal restated from the vision (a month's bills settled without a trip); two sprint questions drafted from AS-3 and the proof gap; the map from agent to customer to posted bill; Amna Rasheed asked about AS-7 in the afternoon and could not confirm it on the spot, so it stayed open rather than blocking the week; target moment picked | The map with the target moment circled: a customer hands cash to the agent for a bill. SQ1 and SQ2 set (below) |
| Tuesday, 2026-09-15 | Sketch | Lightning demo from the existing USSD flow; four-step solo sketch from each of the five room members | Five anonymous solution sketches, three converging on an agent-side confirm-and-print step |
| Wednesday, 2026-09-16 | Decide | Silent review; heat-map dots landed on the converged sketch; speed critique; Faisal Mirza's supervote; storyboard of fourteen panels | Storyboard: agent enters the bill and amount on the agent app, the app sends a confirmation to the customer's own phone, the customer confirms with no PIN entry, the agent's screen shows posted, and the agent hands over a counter slip printed from the agent app alongside the SMS reference |
| Thursday, 2026-09-17 | Prototype | Facade only: a paper-and-click-through mockup of the agent app confirm screen, the customer's phone confirmation screen, and a pre-printed sample counter slip; roles split maker (Zainab Qureshi, the engineer), stitcher and writer (Naveed Akhtar and Hira Baig), asset collector (Usman Javed), interviewer (Hira Baig); trial run at day's end caught one panel where the customer's confirmation screen on A-15's prototype showed the amount in English m-d-y format rather than the Urdu d-m-y format the design sheet's CLDR rule requires | A prototype that survived the trial run; the Friday interview script |
| Friday, 2026-09-18 | Test | Five one-on-one sessions, each an agent-and-customer pair from the same counter, watched from another room; Hira Baig interviewed; notes on the grid | The pattern grid (below); D9 |

### 3. Friday grid

Participant codes, not P1 to P5, per the coverage sheet's convention that P1 to P5 are reserved for personas.

| Sprint question | A-13 / C-09 | A-14 / C-10 | A-15 / C-11 | A-16 / C-12 | A-17 / C-13 | Pattern |
|---|---|---|---|---|---|---|
| SQ1: will an agent key a customer's bill on the agent app with the customer confirming on her own phone, no PIN shared | Positive: confirmed on her own phone without being asked for a PIN | Positive: same, noted the confirmation felt slower than just handing over the phone but preferred it | Positive: confirmed without hesitation | Positive: confirmed, asked the agent to read the amount aloud first | Negative: the customer's phone had no signal at the counter and the agent fell back to asking for the PIN, which the prototype was not built to handle | 4 of 5 positive, 1 negative |
| SQ2: will the customer leave with proof she accepts, the SMS reference plus a stamped counter slip | Positive: took both, said the slip was "the one my husband will believe" | Positive: took both without comment | Negative: said a slip from an agent's own printer was less convincing than the one from the biller's office, asked how she would dispute it | Neutral: took the slip, did not react to it either way, cared only about the SMS | Positive: took both, asked if the slip could carry the biller's logo | 3 of 5 positive, 1 negative, 1 neutral |

Row totals match the coverage sheet's tally (CN19: SQ1 4 positive, 1 negative; SQ2 3 positive, 1 negative, 1 neutral). The one SQ1 negative and the signal outage that caused it went straight into Friday's prototype-vs-network note for AS-4, not into the desirability reading.

**Decision rule applied:** a sprint question is answered when four or five of five sessions point the same way. SQ1 at 4 of 5 is answered. SQ2 at 3 of 5, with the fourth cell neutral rather than positive, is unclear: the C-11 objection is about the slip's *source* (agent printer versus biller), not about proof as a concept, so the fix is a format change, not a redesign of the confirmation step. Faisal Mirza made the call Friday afternoon, in the room, and D9 went into the decision log the same day.

## Reading the result

Two questions, two different outcomes, decided together as one call because they describe one flow. SQ1: proceed. The storyboard's confirmation step becomes the pass-2 hypothesis; agent-initiated, customer-confirmed payment into the customer's own wallet replaces PIN-sharing as the assumption AS-3 stood in for. SQ2: iterate. The pattern is mixed on a question that matters (what a customer will treat as proof at a counter she does not fully trust), so the fix is narrow, keep the SMS reference, change the slip's format to carry the biller's name rather than the agent's, and re-test within a week rather than arguing about it in the room. That re-test is dated 2026-09-24 and 2026-09-25, inside the runbook's own two-day re-test window. Drop was not on the table this week: no cell across either row came back negative from more than one pair, so nothing here reproduces the flinch the runbook's drop case describes. AS-7's licence question did not move, and stays open with Amna Rasheed regardless of the sprint's result, since a desirability test cannot answer a viability question.

D9, as logged: 2026-09-18, proceed with agent-initiated, customer-confirmed payment into the customer's own wallet as the pass-2 hypothesis; re-test the proof format on 2026-09-24 and 2026-09-25; decider Faisal Mirza; sequencing. D9 postdates the decision log's 2026-08-28 revision and does not reverse D8; it commits pass 2 to a shape, not to a launch.

## ILLUSTRATIVE example

This worksheet has no separate unrelated example. The Sahulat week above, Monday's map through Friday's grid, is the filled example, and every person, date, quote and count in it is fictional and ILLUSTRATIVE.

## The trap

As it showed up here: the Thursday trial run's wrong-amount-format panel on A-15's prototype was the near miss: a five-person room fixed it in ten minutes because the trial run happened before Friday rather than being skipped for time. Had it shipped uncaught, A-15's confirmed cell would likely have read negative for the wrong reason, format confusion standing in for the trust question the sprint actually needed to answer, and the SQ1 read would have been contaminated rather than clean.

## Feeds

- [Assumption map](sahulat-coverage-sheet.md): AS-3 moves from untested to supported; AS-7 stays open, unaffected by a desirability result.
- [Decision log](../templates/execution/decision-log.md): D9 as an entry, with the two-day re-test as its follow-up condition.
- [Service blueprint](sahulat-service-blueprint.md): the PIN and missing-slip failure points, this week's evidence for each.
- [Value proposition canvas](sahulat-coverage-sheet.md): E6, E7 and this week's grid feed Rafiq's gain creators for the proof format.
- DISCOVER, pass 2, feeding Gate 1 of that pass (not yet scheduled; owner Hira Baig, per the coverage sheet's summary).
- Method background: [knowledge index, Design Sprint entry](../knowledge/INDEX.md); [assumption mapping](../frameworks/discovery/assumption-mapping.md) for what the sprint could not settle (AS-7).
- Data and identifiers: [Sahulat journey](sahulat-journey.md) and its [coverage sheet](sahulat-coverage-sheet.md), rows CN18, CN19, N60, identifiers SQ1, SQ2, D9, AS-3, AS-7, E6, E7.
