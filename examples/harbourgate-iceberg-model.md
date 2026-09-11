# Harbourgate Iceberg Model

Fills [frameworks/systems/iceberg-model.md](../frameworks/systems/iceberg-model.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and identifier is ILLUSTRATIVE, chosen to show the reconstruction rather than to be quoted as a benchmark or copied as a target. See the [Harbourgate journey](harbourgate-journey.md) and [coverage sheet](harbourgate-coverage-sheet.md).

**Owner:** Ife Adeyemi, Tomasz Wierzbicki and Priya Raman · **Facilitator:** Noor Haddad · **Date:** 2026-03-16 · **Stage:** DISCOVER reconstruction · **Evidence label:** HC53

Based on the four-level diagnostic Michael Goodman set out in "The Iceberg Model" (2002); the underlying idea, that behaviour is explained by structure rather than by blaming a person, is Peter Senge's, from 1990, but the four-tier diagram itself is neither Senge's Fifth Discipline nor Donella Meadows'.

## What it is for

This worksheet separates Harbourgate's payment-step symptom from the structure producing it. The reconstruction feeds the problem framing behind the labelled Gate 1. It is not an action list and does not assign blame to a person.

The working rule for this session was: no names in any cell, at any level.

## Run it when

- A payment metric appears persistently wrong rather than being a single incident
- Several systems or providers could plausibly explain the same failure
- The first explanation is that a second acquirer can only save declines
- A planning decision needs a diagnosis before the problem statement is reconstructed

**Skip it when:** the cause is single, mechanical and undisputed. This Harbourgate symptom recurs across the twelve-month series, so the worksheet was run.

## Inputs you need first

- The event at entry: one order in nine does not complete the payment step, N5
- The recurring series: the twelve-month payment-step non-completion series, HC50
- The adjacent operating signals: 210 payment-failed tickets a week in March 2026, N21, and 11 payment-path pages in March 2026, N22
- The written rule: BR-008, the 2019 cascade rule
- The structural evidence: Marlowe logs no declines, N20 and HC51, and the wrapper has had no commit since the contractor's last commit in 2021, HC52 and R2
- The session record: Ife Adeyemi, Tomasz Wierzbicki and Priya Raman, facilitated by Noor Haddad, HC53

## The worksheet

### Step 1: the event, stripped of story

| # | Event as observed (date, number, source) | Who noticed | First explanation offered | Does that explanation name a person or a one-off? |
|---|---|---|---|---|
| 1 | At entry, one order in nine, 11.1% of orders reaching the payment step, does not complete it. Source: N5, order data for February 2026 | Product and payment operations review | “A second acquirer can only save declines.” | No |
| 2 | Support has 210 tickets a week tagged “payment failed” in March 2026. Source: N21, support tool | Support operations review | “A second acquirer can only save declines.” | No |
| 3 | The payment path has 11 on-call pages in March 2026. Source: N22, on-call tool | On-call review | “A second acquirer can only save declines.” | No |

### Step 2: the climb

| Level | The question it answers | What you write | Evidence it needs |
|---|---|---|---|
| 1. Events | What happened, once? | Payment-step non-completion is 1 order in 9, with 210 payment-failed tickets a week and 11 payment-path pages in March 2026. | N5, N21 and N22 |
| 2. Patterns and trends | How often, over what window, and moving which way? | HC50 records 12 monthly readings from March 2025 to February 2026: 11.3%, 10.9%, 11.0%, 11.4%, 11.2%, 10.8%, 11.1%, 11.5%, 11.6%, 11.2%, 10.9% and 11.1%. Arithmetic: 11.3 + 10.9 + 11.0 + 11.4 + 11.2 + 10.8 + 11.1 + 11.5 + 11.6 + 11.2 + 10.9 + 11.1 = 134.0; 134.0 / 12 = 11.166..., approximately 11.2%. The series stays near the same level across the full window, rather than showing a one-month spike. | HC50, from one order-data source, with 12 periods |
| 3. Systemic structures | What arrangement makes that pattern the normal outcome? | Three arrangements reinforce the same outcome: BR-008 says, “WHEN Kestrel declines THEN retry the authorisation through Marlowe (the 2019 cascade)”; Marlowe logs no declines, so 0% of Marlowe declines carry provider and reason class at entry, N20; and HC52 records no commit to the wrapper since the contractor's last commit in 2021, with 0 engineers able to change it safely until 2026-04-24, R2. Arithmetic for attribution: Kestrel 58% + Tidewater 15% = 73% of payment attempts attributable to a provider at entry; Marlowe carries the remaining 27% without decline attribution, HC51. | BR-008, N12, N20, HC51, HC52 and R2 |
| 4. Mental models | What belief makes that arrangement look reasonable to the people inside it? | “A second acquirer can only save declines.” This makes the cascade look like recovery, makes missing decline data look tolerable, and makes the untouched wrapper look like a contained technical concern rather than a structural ownership gap. | The explanation offered at the event level, BR-008, N20 and HC52 |

### Step 3: structure candidates

| Candidate | Ask | Present? | The rule, quoted |
|---|---|---|---|
| Policy or rule | What are people required or forbidden to do here? | y | BR-008: “WHEN Kestrel declines THEN retry the authorisation through Marlowe (the 2019 cascade).” |
| Incentive or measured target | What is the only thing measured about this work? | n | No incentive or measured target is identified in the reconstruction evidence. |
| Capacity or queue | What arrives faster than it can be worked? | n | No capacity or queue rule is identified in the reconstruction evidence. |
| Handoff or ownership | Where does the work change hands with no owner across the seam? | y | HC52: “No commit to the wrapper since the contractor's last in 2021; 0 engineers able to change it safely until 2026-04-24.” R2 records the ownership risk as “Nobody owns the contractor's wrapper when it misbehaves.” |
| Feedback delay | How long between the mistake and the person who made it learning of it? | y | N20 records that Marlowe logs no declines, so a Marlowe decline has no event at entry to feed back into diagnosis; the only evidence is the monthly Marlowe statement, N14, which stands in for a decline count. |
| Tool default | What does the software do when nobody chooses? | n | No separate software default is identified beyond the explicit BR-008 cascade rule. |

### Step 4: the readiness score

Depth reached, D, is 4 because the session has an event, a twelve-period pattern, named structures with quoted rules, and a mental-model sentence.

Evidence, C, is 2 because the diagnosis is supported by independent operational data and written system evidence, but the reconstruction does not claim two independent authors for every source.

Arithmetic:

- D = 4
- C = 2
- Readiness = D + C = 4 + 2 = 6
- Readiness band: 6 is in the Structure band, 6 to 7

| Band | Readiness | What it means | What you may do |
|---|---|---|---|
| Symptom | 2 to 3 | You have noticed something | Contain it, and keep digging. No plan, no quarter, no roadmap row |
| Pattern | 4 to 5 | You know it recurs and roughly when | Fund the investigation, and a containment with an end date |
| Structure | 6 to 7 | You can name the arrangement and quote its rule | Change the structure, and say which level you are changing |

The Harbourgate result is readiness 6, the structure band. The diagnosis therefore changes the target of the reconstructed problem framing from “recover declines with another provider” to the structure that prevents decline attribution and leaves the cascade and wrapper arrangements in place.

## ILLUSTRATIVE example

This Harbourgate reconstruction is an ILLUSTRATIVE example run on 2026-03-16 during the two-week reconstruction.

Step 1 identified three events: 1 order in 9 does not complete the payment step, 210 payment-failed tickets a week were recorded in March 2026, and 11 payment-path pages were recorded in March 2026.

Step 2 climbed those events through the HC50 series. The 12 readings sum to 134.0 percentage points, and 134.0 / 12 = 11.166..., approximately 11.2%. The stable level shows recurrence rather than a one-off event.

Step 3 identified:

1. BR-008, the cascade from Kestrel to Marlowe
2. Marlowe's missing decline logging, N20
3. The wrapper's lack of maintenance ownership since 2021, HC52 and R2
4. A feedback delay: Marlowe logs no declines at entry, so the only evidence is its monthly statement, N14 and N20

Step 4 calculated D + C = 4 + 2 = 6, the Structure band. The output feeds the reconstructed problem framing behind labelled Gate 1.

## Reading the result

The symptom is one order in nine failing to complete the payment step. The pattern is the near-flat HC50 series across 12 months, not merely the February reading in N5.

The structure is not a person. It is the combination of a cascade rule, incomplete decline attribution and an integration wrapper without an active change path. The mental model makes that combination appear reasonable because it treats a second acquirer as a recovery mechanism without requiring the system to learn which declines it is recovering.

The structure-band result does not prove that every non-completion has the same cause. It does show that the reconstructed problem statement should address attribution, feedback and integration structure rather than describe a reminder or a person-level correction.

## The decision it feeds

The reconstructed problem framing behind labelled Gate 1 should state:

- The observed symptom: one order in nine that reaches the payment step never completes it, N5
- The pattern: payment-step non-completion remained near 11.2% on average across the 12-month HC50 series
- The structural diagnosis: BR-008 cascades Kestrel declines to Marlowe, Marlowe logs no declines at entry, and the wrapper has had no commit since 2021
- The mental model to test: “A second acquirer can only save declines.”

The level chosen is Structure. The symptom-level explanation, “a second acquirer can only save declines,” is rejected as the problem framing because it describes the apparent remedy rather than the arrangement producing the recurring symptom.

## Where the output lands

- [Harbourgate journey](harbourgate-journey.md), which records the reconstructed DISCOVER stage and the labelled Gate 1
- [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), HC50 to HC53, which records the pattern, structural evidence and readiness score
- The reconstructed problem framing behind Gate 1, with the symptom, pattern and structure carried forward

## Re-run trigger

Re-run when the payment-step symptom recurs after a structural change, when the cascade or provider arrangement changes, or when the decline event stream and wrapper ownership change enough to alter the diagnosis.

## When this method misleads you

This reconstruction would mislead if the HC50 series were treated as proof that every failed payment shared one cause. It would also mislead if the mental model sentence were used to blame a team rather than to test the belief that made BR-008 and the missing logging appear reasonable.

The readiness score is deliberately coarse. Readiness 6 permits a structural diagnosis, but it does not make an implementation plan. The next document must still test the proposed change against the payment providers, the wrapper, the decline data and the customer outcome.

## Feeds

- The reconstructed problem framing behind labelled Gate 1
- [Harbourgate journey](harbourgate-journey.md), which records the reconstructed Gate 1 context
- [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), HC50 to HC53, the source rows for this worksheet
- The next diagnostic and strategy work, where the structural diagnosis is tested rather than treated as a finished solution
