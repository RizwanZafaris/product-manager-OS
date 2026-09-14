# Product Vision: Expense Copilot

Fills [templates/planning/vision.md](../templates/planning/vision.md). Everything here is invented: Ledgerline is the fictional mid-market software company used across this repository, and this vision opens DEFINE in the internal-v1 chain the [Expense Copilot journey](expense-copilot-journey.md) indexes, drafted once discovery has already closed with a GO. Every number, date and id below is ILLUSTRATIVE, carried from that journey's own data sheet (V2, V3, V8) and from [ledgerline-journey.md](ledgerline-journey.md)'s N1 to N6, so it can be checked against the [problem framing](expense-copilot-problem-framing.md) and [discovery document](expense-copilot-discovery.md) it follows. See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Horizon:** past this internal release; this vision does not project a multi-year market state, and it is silent on whether the build is ever sold outside Ledgerline, the separate question [ledgerline-journey.md](ledgerline-journey.md) takes up after go-live · **Last updated:** 2026-08-18

## 1. The future state

A filer comes back from a trip and photographs each receipt on the way to their desk, or forwards the email one arrived in. By the time they sit down, a draft is waiting: merchant, date and amount read off the receipt, a suggested category next to the policy line it matched. They check what the system flagged as uncertain, fix anything that needs fixing, and press submit. Nothing leaves before they do that; the filer stays the author of their own report, the way [expense-copilot-discovery.md](expense-copilot-discovery.md)'s hypothesis already puts it, which is also what keeps accountability where Ledgerline's policy already puts it.

The report clears review the first time, because the two things that used to cause a bounce, a re-typed number with a typo in it and a guessed category, do not happen anymore: a field the system cannot read stays blank and flagged rather than filled with a guess, so what a reviewer sees is either right or honestly marked uncertain, never confidently wrong. Reviewers spend their pass on the judgment calls that need a person, not on re-checking totals and categories a machine already got right.

None of this requires a filer to trust a black box. The policy line sits next to every suggested category, so a bounce, on the rare report that still gets one, becomes a conversation with a rule the filer can read rather than a mystery. An admin who spots a wrong mapping fixes it once, and the fix is logged; the system does not quietly relearn the fix into every future suggestion on its own, because nobody has reviewed that loop yet, but the correction is never lost either.

We will know we were wrong if the numbers move the wrong way rather than this one: if first-submission approval does not climb from the 62% baseline toward the 80% the finance lead has already agreed to target (N3, N4), or if filers keep re-typing receipts by hand alongside the new flow instead of choosing it, short of the half of eligible reports the discovery document already set as the signal worth watching two months after launch. A copilot that is used but does not change the approval rate is a copilot that drafted convincingly and was wrong just as often as the form it replaced; that would mean this vision was wrong, not merely early.

## 2. Who this is for

| Field | Answer |
|---|---|
| Primary customer | Filers at Ledgerline: individual contributors who travel or spend against the company account and file their own expense reports, drawn from the roughly 900-person workforce measured at N1 |
| The progress they are trying to make | File a report that clears review the first time, without re-typing what the receipt already shows or guessing at a policy line, per [expense-copilot-discovery.md](expense-copilot-discovery.md)'s Pain section |
| Who this is explicitly NOT for yet | The three finance reviewers who approve every report (N7): a secondary audience whose relief is a consequence of this vision, not its design target; and anyone filing on another person's behalf, the executive-assistant workflow discovery deliberately parked |

## 3. Why now

| Shift that opens the window | Evidence it is real | What happens if we wait |
|---|---|---|
| Ledgerline changed its travel-agency vendor, and expense-related support tickets rose sharply in the two quarters that followed, turning a standing but tolerated process into one the finance lead asked engineering about directly | [expense-copilot-discovery.md](expense-copilot-discovery.md) Trigger section; discovery's own GO, decided 2026-08-14 by Maya Chen and Daniel Okafor (V2) | The pattern behind the request does not fix itself: reviewers keep absorbing about 30 hours, about $1,800, a month in mechanical checks (N7) while first-submission approval stays near 62% (N3) instead of moving toward the 80% the finance lead has already agreed is worth reaching (N4) |

## 4. North star tie-in

- **North star metric this vision implies:** candidate: first-submission approval rate on copilot-drafted reports, 62% baseline moving toward an 80% target (N3, N4). No separate north-star sheet exists yet for this internal build; OKR and north-star instances for the internal v1 are out of scope for this chain, so this candidate is stated here rather than in a sheet of its own.
- **How the future state moves it:** a report a filer never has to re-type and never has to guess a category on is a report finance approves without a second look. Every field the system gets right without inventing an answer converts what used to be a mechanical bounce into a clean first pass, so the metric moves directly, by removing the two causes discovery already named, not by a proxy that could move on its own.

## 5. Non-goals

| We will not | Because | Revisit when |
|---|---|---|
| Auto-submit any report on a filer's behalf | The filer stays the author; this is a load-bearing guardrail this vision treats as permanent, not a v2 candidate | Never on its own; a change here would need a new problem framing, not a roadmap slot |
| Reconcile corporate-card feeds, mileage or per-diem rules | Out of this build's scope; the receipt-reading problem this vision answers is narrower than the whole of expense management | A future discovery pass finds the card-feed or mileage problem costs Ledgerline on the same order as the one this vision answers |
| Let anyone file an expense report on another person's behalf | The parked executive-assistant workflow from discovery, a distinct workflow with its own review needs | A future discovery pass scopes the EA workflow on its own terms, with its own evidence |
| Let the model vendor train on Ledgerline's receipt data | The vendor's training-data and retention terms are still open, carried forward from discovery as a known risk | The legal lead closes the vendor clause, before Gate 5 |

## How this vision fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Indistinguishable from a competitor's | Language any vendor in the category could publish unchanged | Section 1 names Ledgerline's own policy line, matched and shown beside the draft, not a generic promise of automation |
| A roadmap in disguise | Quarters, deliverables and dates dressed as direction | Section 1 carries no date and no phase name; the roadmap that carries dates is a separate file |
| Adjectives with no picture | "Seamless," "intelligent," "delightful," and no scene | Section 1 describes one filer's afternoon, photographing a receipt and reviewing a draft, not an adjective list |
| Unfalsifiable | So abstract that no outcome could ever contradict it | Section 1's closing paragraph states the observation that would mean this vision was wrong: usage without the approval rate moving |
| Written once, never referenced | A file nobody opens between planning rounds | The product strategy and roadmap that follow this vision both cite its non-goals and its north-star candidate by name |

## Exit gate

This vision is fit to publish when:

- [x] The future state is written in the customer's terms and would not survive a competitor name swap: section 1 names Ledgerline's own policy-matching behavior, not a generic claim
- [x] Exactly one primary customer is named, and the deferred segments are listed as non-goals: filers in section 2; reviewers and the executive-assistant workflow named as not-yet in section 2 and section 5
- [x] The why-now names a real shift with linked evidence, not a trend headline: the travel-agency switch and the ticket rise it caused, linked to the discovery document and to Gate 1's own decision
- [x] The implied north star metric is stated, even if only as a candidate: first-submission approval rate, section 4
- [x] Every non-goal carries a reason and a revisit condition: four rows in section 5, each with both
- [x] A team could use this document to say no to a plausible feature request: a request to auto-submit, to reconcile card feeds, or to file on another person's behalf each has a non-goal row that answers it directly

Approved at Gate 2 by the business sponsor: Daniel Okafor, 2026-08-28
