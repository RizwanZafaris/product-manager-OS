# Journey Map: Shazia Paying One Ravi Power Bill

Fills [templates/discovery/journey-map.md](../templates/discovery/journey-map.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, Shazia and every session, quote and count below are fiction, and every number is ILLUSTRATIVE, drawn from the shared data sheet in [the Sahulat journey](sahulat-journey.md) so this map agrees with the other Sahulat artifacts rather than to describe any real wallet, market or biller. See the [examples index](README.md) and, for how this file sits in the Sahulat set, the [coverage sheet's](sahulat-coverage-sheet.md) artifact map.

**Owner:** Hira Baig, Product Manager, the only PM in the company · **Date:** 2026-02-18, one day after [the personas](sahulat-personas.md) · **Status:** Drafted for Gate 1; not itself a gate, and not amended after Gate 1 attempt 1 (2026-02-20, MORE DISCOVERY on lines this file does not hold) or attempt 2 (2026-02-27, GO)
**Persona:** [Shazia, the Household Bill-Runner (P1)](sahulat-personas.md) · **Scenario:** Shazia pays one Ravi Power electricity bill this month, from the bill arriving to a surcharge appearing on the next one.
**Evidence base:** INT-001, INT-002, INT-004, INT-005, INT-007, INT-008 (P1's own sessions); themes T1, T4, T5; evidence rows E1 and E4; data-sheet rows N18 to N25 and N63

## 1. Current journey

<!-- Columns are stages: name each stage as the user would, not as your system would. -->

| | Stage 1: The bill arrives | Stage 2: Reads the due date | Stage 3: Trip to a branch or bill shop | Stage 4: Pays | Stage 5: A fine on the next bill |
|---|---|---|---|---|---|
| **User actions** | Ravi Power's paper bill reaches the house; she reads the amount and the due date printed on it, one of three household bills a month (N22, measured, bills shown in 8 customer sessions) | Checks which day the due date falls on and whether she can reach a branch or shop that day; six of eight sampled customers pay on the due date itself rather than earlier (N25, measured, told) | Makes the round trip: median 70 minutes and PKR 60 in transport (N20, estimate, told) | Pays in cash at whichever venue is open: four of eight customers in the sample use a bank branch, four of eight use a bill shop (N63, measured, told) | Receives the next bill and finds a surcharge line on it |
| **Touchpoints and tools** | The paper bill | The paper bill, her own memory of which days the branch is open | Bank branch or bill shop (split evenly, N63); the wallet's existing USSD menu, unrelated to bill pay, which does not yet exist | Branch teller, or the bill-shop counter | The next paper bill |
| **Thoughts** | Reads the amount and the date, nothing quoted at this stage in the sample | "The bill was due on a Sunday" (E1, INT-004, 2026-02-02, 02:10), when the date lands badly | "The screen went off in the middle and I did not know if the money went. I waited ten minutes for the message and then dialed again." (E4, INT-007, 2026-02-06, 21:15) | "The shop man charged me fifty" (E1, INT-004) | "The office still put the fine on the next bill" (E1, INT-004) |
| **Emotion (high / neutral / low)** | Neutral | Low for the three of eight whose most recent due date fell on a Saturday or Sunday (N24, measured, shown); low, INT-004, INT-005, INT-008 (T5) | Low, INT-007 (E4, T4): a dropped session with no status message, then a blind redial | Low, INT-004 (E1): pays a fee she did not budget for | Low, INT-004 (E1); five of eight customers paid a late surcharge in the last three months, median PKR 200, four of the five bills shown, not only described (N18, N19) |
| **Pain and friction** | None recorded in the sample at this stage | A weekend or after-hours due date closes the branch before she can reach it (T5) | No confirmation a USSD attempt succeeded or failed; if the branch is shut, the shop is the only option and it charges a fee, PKR 30 to 50 (N21, estimate, told by agents) | The shop fee lands on a bill already due; paying late at a branch does not visibly register as on time | The surcharge posts even when she believes she paid before the due date, with no channel shown in the sample to dispute it |
| **Moments of truth** | None; she has not yet decided how she will pay | Decides which of the two channels to try first, bank or shop, roughly a coin flip in the sample (N63) | Decides whether to redial the dropped session or wait for a status message, which the sample shows her resolving by redialing rather than giving up on the attempt (T4) | Decides whether to pay the shop's fee to avoid a second trip, which four of eight do (N63), or hold out for the branch | Absorbs the surcharge; the sample shows no case of her disputing it |

**Backstage note:** what happens between a branch teller or a bill-shop till taking the cash and Ravi Power's billing office marking the account paid is not established in the research; E1 shows the surcharge landing on the next bill even when the customer's own account is that she paid, which means either the payment posted after Ravi Power's cutoff for that cycle or the two systems did not reconcile in time, and the sample cannot tell which. Open: Hira Baig, next DISCOVER pass, to ask Ravi Power's side of stage 5 directly rather than inferring it from the customer's account. This is the exact question the [payments acquiring](../knowledge/domains/payments-acquiring.md) sector card raises about what happens once a payment is approved and its posting to a biller fails or lags afterward, here on the branch and shop rail rather than on a digital one. When this line is worth more than one line, [service-blueprint.md](../templates/discovery/service-blueprint.md) is the template for mapping the branch's and the shop's side of stage 4 properly; that map does not exist yet.

## 2. Future journey

<!-- Same stages unless the concept removes or merges one. Only rows that CHANGE. -->

| | Stage 1: The bill arrives | Stage 2: Reads the due date | Stage 3: Trip to a branch or bill shop | Stage 4: Pays | Stage 5: A fine on the next bill |
|---|---|---|---|---|---|
| **What changes** | No change sketched here | No change sketched here | Removed as a dedicated trip: the same USSD channel that dropped the session in E4 becomes the payment channel itself, so no separate visit is needed to settle the bill | Pays from wherever she already is, and receives something in hand at the moment of paying rather than only a memory of having paid | No change sketched here as its own row; whatever follows from a changed Stage 4 is this stage's concern, not a separate change |
| **User outcome** | | | No trip, no PKR 60 transport, no median 70 minutes spent (N20); a payment attempt that fails is one she can see fail, unlike E4 | Holds proof the moment she pays, not only after the fact, which the shop or branch trip in Stage 4 today does not give her | Whether a fine still lands depends on what Stage 4's proof actually resolves at Ravi Power's end, which is the same backstage gap named above and not something this sketch can close |

**Stages removed or merged, and why:** Stage 3, the trip, is removed as a separate stage; whatever channel eventually carries the payment absorbs it into Stage 4. This is a DISCOVER-stage sketch, not a DESIGN commitment: which channel, which rail and what it costs to build are DESIGN and DEFINE questions this map does not answer, and no vendor or architecture choice is implied here.

## 3. Opportunity areas

<!-- Rank by user impact times frequency, not by ease of building. -->

Ranked by how often the sample shows the pain landing and how much it costs when it does, not by which is easiest to build.

| # | Opportunity | Journey stage | Evidence (session IDs, metrics) | Who feels it and how often | Candidate for |
|---|---|---|---|---|---|
| 1 | Remove the dedicated trip to pay a bill | Stage 3: Trip to a branch or bill shop | N20 (median 70 minutes, PKR 60 transport); T1 (INT-001, 002, 004, 005, 007, 008) | All eight customer sessions describe some version of this trip; three bills a month per household in the sample (N22), so up to three times monthly | [sahulat-problem-framing.md](sahulat-problem-framing.md) |
| 2 | Stop a weekend or after-hours due date from producing both a shop fee and a surcharge in the same cycle | Stage 2: Reads the due date, and Stage 5: A fine on the next bill | N24 (3 of 8 most recent due dates fell on a Saturday or Sunday); T5 (INT-004, 005, 008); E1 | The three of eight whose due date lands badly pay twice over, a fee and then a fine, in the same account (E1); recurs whenever a due date falls on a closed day | [sahulat-problem-framing.md](sahulat-problem-framing.md) |
| 3 | Give a status the moment a self-service payment attempt succeeds or fails | Stage 3: Trip to a branch or bill shop | E4, INT-007; T4 (INT-004, 007, 008, 012, across customers and agents) | Narrower in this sample, one customer session names it directly, but T4 spans four of fourteen sessions across both segments, and a channel a customer cannot trust is one she keeps abandoning for the trip this map is trying to remove | [sahulat-problem-framing.md](sahulat-problem-framing.md) / not now, pending a wider count |

---

## How this map fails

<!-- A journey map is the artifact most often drawn from the org chart rather
     than from a user, and it looks identical either way. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Drawn from the org chart | The stages match internal teams and handoffs | Stages are what the user is trying to do, named in their words |
| The happy path only | Every step succeeds, and nothing is confusing or abandoned | Mark where people drop out. That is where the product is |
| No evidence behind a step | Emotions and pain points asserted with nothing cited | Each stage cites an interview, a ticket or an observation, or is marked assumption |
| Ends at purchase | The map stops where the funnel does, and ignores the life after | Map through first value and renewal, because that is where retention is lost |
| A poster, not an input | Beautifully produced, never referenced again | Every pain point names the opportunity or story it produced, or is deleted |
| One map for several personas | Composite journey averaging people who behave differently | One map per persona whose journey actually differs |
| A future stage borrows a solution nobody chose yet | The Stage 3 rewrite reads as a decision when it is a sketch, and DESIGN inherits it as fact | Name the sketch as a sketch; leave the vendor and the architecture to DESIGN's own decision log |

## Exit gate (feeds Gate 1: problem worth solving)

<!-- Checkable by someone who did not write this document, which is the
     test of whether a gate is a gate. -->

- [x] One persona and one scenario, named in the header: Shazia (P1) paying one Ravi Power bill this month.
- [x] Current journey drawn from cited evidence, not memory: every cell in section 1 that states a fact carries an ID, N18 to N25, N63, E1, E4, T1, T4 or T5; the one stage-1 cell with nothing to cite says so plainly rather than inventing a quote.
- [x] Every emotion low carries a session ID or data point: Stage 2 (N24, T5), Stage 3 (E4, INT-007, T4), Stage 4 and Stage 5 (E1, INT-004, N18, N19).
- [x] Backstage note filled for each painful stage: one backstage note is written, for Stage 5, the stage the sample cannot explain from the customer's side alone; it is marked Open rather than guessed at, per this repository's no-fabrication rule.
- [x] Future journey shows only what changes: only Stage 3 and Stage 4 carry a filled row; Stages 1, 2 and 5 are left to say so explicitly rather than restating the present.
- [x] Opportunities ranked by impact and frequency, each with evidence: three rows, ordered by how often the sample shows the pain and what it costs when it lands, each citing an ID from the data sheet.

This file does not decide Gate 1 on its own: [sahulat-journey.md](sahulat-journey.md) records attempt 1's MORE DISCOVERY (2026-02-20, on the cost-of-inaction and success-signal lines in [sahulat-problem-framing.md](sahulat-problem-framing.md), neither of which lives here) and attempt 2's GO (2026-02-27), both signed in the gate file itself, by Hira Baig and Faisal Mirza, not here.

Reviewed and ready to feed Gate 1: Hira Baig, Product Manager, 2026-02-18.
