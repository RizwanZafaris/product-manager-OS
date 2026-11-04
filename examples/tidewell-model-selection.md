# Model Selection: Tidewell Helpdesk suggested replies

Fills [templates/ai/model-selection.md](../templates/ai/model-selection.md). Everything here is invented for this standalone example: Tidewell Helpdesk is a fictional help-desk product for small online shops, Vendor North, Vendor East and Vendor West are fictional model vendors, Model A, Model B and Model C are placeholders rather than real models, and every price, score, latency, date and name is ILLUSTRATIVE, not drawn from any real vendor's price list or benchmark. See the [examples index](README.md).

**Feature:** Suggested Reply drafts an answer to a customer's ticket inside the support agent's composer. The agent edits and sends it; nothing reaches a customer until an agent presses send.
**Decision owner:** Odile Fennimore, Product Lead, Suggested Reply · **Document date:** 2026-10-20
**Eval set used for every candidate:** `evals/reply-drafts-v3`, 220 labelled tickets, SHA-256 beginning 4c1e9a07 (ILLUSTRATIVE), from the Suggested Reply eval spec section 2
**Forecast volume:** 85,000 drafts per month by the end of Q1 2027 (ILLUSTRATIVE), from forecast row F3 of the Suggested Reply business case

## 1. Budgets, then candidates

All five budgets were written between 2026-09-02 and 2026-09-12, before the first candidate run on 2026-10-06.

| Budget | Value | Set by, and from what | Date set |
|---|---|---|---|
| Quality floor | "Sendable after light edits" rate at least 0.80, and policy-violation rate at most 0.02 (ILLUSTRATIVE), the two regression rows of the eval spec | Hana Strand, Support Operations Lead, in the eval spec agreement | 2026-09-02 |
| Model cost ceiling per successful task | $0.020 (ILLUSTRATIVE) | Odile Fennimore, from the add-on's seat price and the gross-margin target in the business case | 2026-09-10 |
| Latency budget | p50 at most 3.0 s and p95 at most 6.0 s, from the agent opening a ticket to the draft appearing in the composer (ILLUSTRATIVE) | Hana Strand: in the August shadowing sessions, agents began typing their own reply after about six seconds | 2026-09-10 |
| Context need | p50 3,100 and p99 14,500 input tokens, retrieved help articles included, measured on 2,000 production tickets (ILLUSTRATIVE) | Tomasz Ekwueme, ML Engineer | 2026-09-12 |
| Data-terms floor | Vendor retention of 30 days at most; no training use of customer content; EU processing for EU tenants | Mette Arnfield, Legal Counsel, from the privacy impact assessment and the customer data processing agreement | 2026-09-12 |

| Candidate | Vendor or host | Exact version string | Prompt version used here | Prompt iterations spent | Why it is on the list |
|---|---|---|---|---|---|
| Model A | Vendor North, hosted API | `model-a-2026-08-20` | reply-prompt v9 | 9 | Runs the closed beta today |
| Model B | Vendor East, hosting an open-weight model | `model-b-instruct-v2` | reply-prompt v9b | 4, then 6 | Lowest price per token, and a different vendor, so a fallback candidate |
| Model C | Vendor West, hosted API | `model-c-2026-07` | reply-prompt v9c | 4, then 6 | Best drafts in the team's spot checks |

The first run on 2026-10-06 compared Model A's nine prompt iterations with four each for B and C. The team gave B and C two more iterations each and re-ran on 2026-10-13: B moved from 0.70 to 0.72 and C from 0.88 to 0.89. Every number below is from the second run. A still had three more iterations than either challenger, and section 6 records that.

## 2. Quality on the team's own eval set

- Run date: 2026-10-13 · Runs per candidate: 3 · Grader: human for the primary metric (two senior agents scoring against the rubric, disagreements adjudicated by Hana Strand); code for policy violations (each refund amount in a draft checked against the refund policy table)

| Metric (from eval-spec.md) | Threshold | Model A | Model B | Model C |
|---|---|---|---|---|
| Sendable after light edits | at least 0.80 | 0.86 (0.85 to 0.87) | 0.72 (0.70 to 0.74) | 0.89 (0.88 to 0.90) |
| Policy-violation rate | at most 0.02 | 0.014 (mean 3.0 of 220) | 0.027 (mean 6.0 of 220) | 0.009 (mean 2.0 of 220) |
| Smallest segment: Spanish-language tickets, sendable | at least 0.80 | 20 of 24 (0.83) | 13 of 24 (0.54) | 21 of 24 (0.88) |
| Passes the quality floor | | yes | no | yes |

## 3. Fully loaded cost per successful task

All prices are ILLUSTRATIVE and stand for each fictional vendor's price page as read on 2026-10-01. The knowledge-base search costs $0.0004 per call (ILLUSTRATIVE internal unit cost), one call per attempt for every candidate. Review minutes come from a timed sample of 40 tickets per candidate, timed by two agents on 2026-10-14 and 2026-10-15, at a loaded agent cost of $0.60 per minute (ILLUSTRATIVE).

| Line | Model A | Model B | Model C | Source |
|---|---|---|---|---|
| Input tokens per attempt (mean, measured) | 3,420 | 3,610 | 3,380 | eval run log, 2026-10-13 |
| Output tokens per attempt (mean, measured) | 310 | 365 | 402 | eval run log, 2026-10-13 |
| Input price per million tokens | $2.20 | $0.35 | $5.50 | vendor price pages, 2026-10-01 |
| Output price per million tokens | $8.80 | $1.40 | $22.00 | vendor price pages, 2026-10-01 |
| Tool calls per attempt x cost per call | 1 x $0.0004 | 1 x $0.0004 | 1 x $0.0004 | internal unit cost |
| Retries per task | 0.05 | 0.12 | 0.03 | eval run log: schema or length failures re-run |
| Task success rate | 0.86 | 0.72 | 0.89 | section 2 |
| Cost per attempt | $0.01065 | $0.00217 | $0.02783 | arithmetic |
| Model cost per task | $0.01118 | $0.00244 | $0.02867 | arithmetic |
| Model cost per successful task, against the $0.020 ceiling | $0.0130, under | $0.0034, under | $0.0322, over | arithmetic |
| Cost per attempt at the p95 input length | $0.0247 at 9,800 tokens | $0.0045 at 10,300 tokens | $0.0626 at 9,700 tokens | arithmetic |
| Review minutes per successful task | 1.5 | 2.6 | 1.3 | timed sample, 40 tickets each |
| Fully loaded cost per successful task | $0.913 | $1.563 | $0.812 | arithmetic |
| Monthly model spend at 85,000 drafts | $951 | $207 | $2,437 | arithmetic |

Model A's row, worked through: cost per attempt = (3,420 x $2.20 / 1,000,000) + (310 x $8.80 / 1,000,000) + $0.0004 = $0.00752 + $0.00273 + $0.0004 = $0.01065. Model cost per task = $0.01065 x 1.05 = $0.01118. Model cost per successful task = $0.01118 / 0.86 = $0.0130. Review cost = 1.5 x $0.60 = $0.90, so fully loaded = $0.913. Monthly spend = 85,000 x $0.01118 = $951.

Whose money each line is: model cost is Tidewell's cost of goods; review minutes are the customers' agents' time. Fully loaded, Model C is the cheapest line, because its drafts save customers about $0.10 of agent time per successful draft against Model A. On Tidewell's own cost, Model C breaks the ceiling by 61 percent ($0.0322 against $0.020). The two measures point at different winners, and section 6 says which one this decision serves.

## 4. Latency against the budget

- Measured: 500 requests per candidate, from the EU serving region, at 40 concurrent requests, on 2026-10-14 between 09:00 and 11:00 UTC, the forecast peak

| Measure | Budget | Model A | Model B | Model C |
|---|---|---|---|---|
| p50 end to end, ticket opened to draft in composer | 3.0 s | 2.3 s | 1.4 s | 4.1 s |
| p95 end to end | 6.0 s | 5.1 s | 3.2 s | 8.9 s |
| p95 time to first token, the draft streams in | not budgeted separately | 0.9 s | 0.5 s | 1.6 s |
| Within budget | | yes | yes | no |

## 5. Context, vendor terms, and deprecation risk

| Item | Requirement (from section 1) | Model A | Model B | Model C | Source and date |
|---|---|---|---|---|---|
| Context limit, against the p99 need | 14,500 tokens | 200,000 | 32,000 | 200,000 | vendor model documentation, 2026-10-01 |
| Vendor retention of inputs and outputs | 30 days at most | None, under the signed agreement | Request logs, 7 days | 30 days, for abuse monitoring | Vendor North contract clause 7.2, 2026-07-01; Vendor East terms, 2026-09-15; Vendor West terms, 2026-08-30 |
| Use of our inputs or outputs for training | None | None | None | None, under business terms | same documents |
| Processing regions available | EU for EU tenants | EU and US | EU only | US only, fails the floor | vendor region pages, 2026-10-01 |
| Rate limit at our tier, against a forecast peak of 90 requests per minute | 90 per minute | 600 per minute | 300 per minute, provisioned | 200 per minute | vendor tier pages, 2026-10-01 |
| Published deprecation notice period | | At least 6 months | 90 days before the host withdraws it; the weights can be self-hosted | 3 months | Vendor North deprecation policy, 2026-05-12; Vendor East terms, 2026-09-15; Vendor West terms, 2026-08-30 |
| Announced end-of-life date for this version | | None announced | None announced | 2027-03-31 | vendor notices checked 2026-10-15 |
| Exit cost: what switching away from it would take | | Prompt rework and a full eval re-run, 2 to 3 weeks (ILLUSTRATIVE estimate, Tomasz Ekwueme) | 1 to 2 weeks, prompt v9b exists | Not estimated, not chosen | estimator notes, 2026-10-16 |

## 6. Decision and fallback

- **Chosen:** Model A, `model-a-2026-08-20`. Copied into the "Model and version pinned" line of the Suggested Reply eval spec and model card on 2026-10-20.
- **Why, and what it gives up:** Model A is the only candidate that clears all five budgets. The decision optimises Tidewell's model cost under the ceiling first and customers' agent time second. It gives up Model C's higher sendable rate (0.89 against 0.86) and about $0.10 of customers' agent time per successful draft, which makes C the cheaper fully loaded line. It also gives up Model B's model cost, about a quarter of Model A's ($0.0034 against $0.0130). Model A also had three more prompt iterations than either challenger. The bias is small against B's eight-point quality gap and does not explain C's failures, which are latency, cost, region and end of life rather than quality, but it is recorded here, and the calendar re-run in section 7 gives every candidate equal prompt work.
- **Why each other candidate lost:** Model B is below the quality floor (0.72 against 0.80) and over the policy-violation limit (0.027 against 0.02). Model C misses the p95 latency budget (8.9 s against 6.0 s) and the model cost ceiling ($0.0322 against $0.020). It also processes only in the US, and this version has an announced end of life on 2027-03-31.
- **Fallback model:** Model B, `model-b-instruct-v2` on Vendor East · **Its section 2 result:** 0.72 sendable, 0.027 policy violations; fails the floor
- **Degraded mode, accepted as a waiver:** Hana Strand accepted on 2026-10-20 (decision-log D-14) that in fallback the drafts are labelled "Rough draft: check refund amounts". The refund-amount guardrail blocks any draft naming an amount outside the policy table, and after 24 hours in fallback Suggested Reply switches off until Model A is back.
- **What users see in fallback:** a composer banner reading "Drafts are using a backup model and may need more editing", per the Suggested Reply interaction spec section 5a · **Switch trigger and who flips it:** Vendor North error rate above 5 percent for 5 minutes, or p95 above 12 s for 10 minutes; switched automatically, confirmed by the on-call platform engineer · **Longest time allowed in fallback:** 24 hours, then Suggested Reply is off
- [OPEN: the automatic switch to Model B has been tested once in staging at 5 concurrent requests, not at the 40-request peak; owner Tomasz Ekwueme, load test due 2026-11-12, before the general-availability rollout]
- **Recorded as:** ADR-0011 for the choice; decision-log D-14 for the degraded-mode waiver

## 7. Revisit trigger

| Trigger | Threshold | Watched by | What happens when it fires |
|---|---|---|---|
| Vendor announces deprecation of the pinned version | Any notice for `model-a-2026-08-20` | Tomasz Ekwueme | Re-run sections 2 to 5 within 4 weeks |
| Price change on the pinned model | 20 percent either way | Odile Fennimore | Recompute section 3; a ceiling breach opens a full re-run |
| Production p95 latency above budget | Above 6.0 s on 3 consecutive weekdays, from the suggested-reply latency dashboard | On-call platform engineer | Page Tomasz Ekwueme; a vendor-side cause opens a re-run |
| Production-sampled quality below the floor | Sendable below 0.80 for 2 consecutive weeks, per the eval spec section 4 | Hana Strand | Hold the rollout and re-run |
| A new candidate clears the floor at lower fully loaded cost | 30 percent lower, on `reply-drafts-v3` or a later version | Tomasz Ekwueme | Full comparison through this file |
| Calendar | 2027-02-15 | Odile Fennimore | Full re-run, equal prompt iterations for every candidate |

## 8. How this choice goes wrong

Three of the template's failure rows were live in this comparison. Each is recorded here with what was done about it.

| Failure | The tell | What to do |
|---|---|---|
| The incumbent was tuned and the challengers were not | Nine iterations against four in the first run | Two more iterations each for B and C, re-run on 2026-10-13; the residual gap of three is written into section 6 |
| A fallback nobody evaluated | Model B was named as fallback before it had a section 2 result | Evaluated on the same set; it fails the floor, so the degraded mode is a written waiver with a 24-hour limit and an owner |
| Price per token read as cost | The first draft of section 3 ranked Model B cheapest and stopped there | The success-rate divisor and the review minutes were added; on Tidewell's cost B is still cheapest, but it fails quality, and fully loaded it is the most expensive line |

## Exit gate

This document passes when:

- [x] Every budget in section 1 has a value, a setter and a date earlier than the section 2 run (all dated 2026-09-02 to 2026-09-12; first run 2026-10-06)
- [x] Every candidate was scored on the same eval set version and hash, with the run count and spread stated (`reply-drafts-v3`, 3 runs each, ranges shown)
- [x] Prompt iterations per candidate are recorded, and any large difference is either closed or written beside the decision (narrowed from five to three, and written into section 6)
- [x] Section 3 shows every arithmetic row for every candidate, and each price row cites a dated vendor document
- [x] Latency is reported as p50 and p95 against a budget written before measurement, with how it was measured
- [x] Every vendor-terms cell cites a document and a date, or is an open field with an owner
- [x] The chosen version string is copied, character for character, into eval-spec.md and model-card.md (both on 2026-10-20)
- [x] The fallback ran the same eval set, and if it fails the floor, its degraded mode has an owner and a time limit (D-14, Hana Strand, 24 hours; the load test of the switch is the open field in section 6)
- [x] Every revisit trigger has a threshold and a named watcher, and the calendar row has a date
- [x] The decision is recorded as an ADR or decision-log row, with what it gave up (ADR-0011 and D-14)

Signed: Odile Fennimore, Product Lead, Suggested Reply, 2026-10-20
