# Opportunity scoring: Sahulat Bill Pay, pass 2

Fills [frameworks/discovery/opportunity-scoring.md](../frameworks/discovery/opportunity-scoring.md). Everything here is invented: Sahulat, its people, agents, customers, billers, bank, aggregator and telco are fiction, and every number is ILLUSTRATIVE, chosen so that this worksheet agrees with the [Sahulat journey data sheet](sahulat-journey.md) and its [coverage sheet](sahulat-coverage-sheet.md).

**Owner:** Hira Baig, Product Manager, the only PM in the company · **Date:** 2026-09-28 · **Pass:** 2 · **Status:** Complete for Gate 1 of pass 2

## What it is for

This worksheet ranks the outcomes agents care about when they perform an assisted Sahulat bill payment for a customer. It uses the 734 responses to agent survey SV-1, with mean aggregation for both importance and satisfaction.

The result is one underserved outcome:

- **OUT-5, minimize the unpaid time spent on a customer's bill, score 15.8.**

Proof, OUT-4, and float, OUT-2, are solid opportunities. Dispute risk, OUT-3, is adequately served. The segment cut shows that float hurts less in the Lahore pilot district, where the hotline ran first.

The outcome statements contain no Sahulat feature. They describe progress an agent can recognize without presupposing a particular solution. The source data and outcome identifiers are in [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md).

## Run it when

- A job map has named the struggling steps in agent-assisted bill payment and the team needs to rank the outcomes inside them.
- The team needs to decide whether unpaid agent time, proof, float, dispute risk or payment confirmation deserves the next discovery slice.
- A survey is already planned and importance and satisfaction can be asked for every outcome.

**Skip it when:** there are fewer than a handful of respondents per segment. This pass has 734 SV-1 responses, including 188 from the Lahore pilot district and 546 elsewhere, so the overall mean is suitable for ranking. The segment readings remain descriptive where the data sheet provides a segment score.

## Inputs you need first

- Five outcome statements from SV-1, identified as OUT-1 to OUT-5.
- SV-1 responses from 734 agents, as recorded in CN21.
- The segment cut decided before fielding: Lahore pilot district against elsewhere.
- The importance and satisfaction means, gaps and scores recorded in CN24.
- The segment scores supplied in CN24 for OUT-2 and OUT-5.

## The worksheet

### 1. Scales

| Question | Scale | Aggregation |
|---|---|---|
| How important is it that you can [outcome]? | 1 (not important) to 10 (critical) | Mean across 734 SV-1 respondents. The mean lands in 1 to 10. |
| How satisfied are you with how you [outcome] today? | 1 (not at all) to 10 (fully) | Mean across the same 734 SV-1 respondents. The mean lands in 1 to 10. |

This sheet uses the mean path only. Every score must therefore remain within 1 to 19.

### 2. Scoring table

**Arithmetic:** gap = max(importance minus satisfaction, 0); opportunity score = importance plus gap.

| ID | Desired outcome | Job step | n | Importance (1 to 10 mean, 0 to 10 share) | Satisfaction (1 to 10 mean, 0 to 10 share) | Gap | Score | Rank |
|---|---|---|---:|---:|---:|---:|---:|---:|
| OUT-1 | Minimize the time to confirm a customer's bill posted before she leaves the counter | Confirm payment posting | 734 | 8.1 | 4.2 | 3.9 | 12.0 | 4 |
| OUT-2 | Minimize the likelihood of running out of float on a bill-peak day | Maintain float for assisted payment | 734 | 8.8 | 3.6 | 5.2 | 14.0 | 3 |
| OUT-3 | Minimize the likelihood a customer disputes a payment the agent keyed | Resolve payment confidence at the counter | 734 | 7.4 | 5.9 | 1.5 | 8.9 | 5 |
| OUT-4 | Minimize the time to hand the customer proof she accepts | Hand over accepted proof | 734 | 8.6 | 2.9 | 5.7 | 14.3 | 2 |
| OUT-5 | Minimize the unpaid time spent on a customer's bill | Perform the customer's bill payment | 734 | 9.1 | 2.4 | 6.7 | 15.8 | 1 |

Arithmetic and bound check for every row:

- **OUT-1:** gap = max(8.1 minus 4.2, 0) = 3.9. Score = 8.1 + 3.9 = **12.0**, which is within 1 to 19.
- **OUT-2:** gap = max(8.8 minus 3.6, 0) = 5.2. Score = 8.8 + 5.2 = **14.0**, which is within 1 to 19.
- **OUT-3:** gap = max(7.4 minus 5.9, 0) = 1.5. Score = 7.4 + 1.5 = **8.9**, which is within 1 to 19.
- **OUT-4:** gap = max(8.6 minus 2.9, 0) = 5.7. Score = 8.6 + 5.7 = **14.3**, which is within 1 to 19.
- **OUT-5:** gap = max(9.1 minus 2.4, 0) = 6.7. Score = 9.1 + 6.7 = **15.8**, which is within 1 to 19.

The mean path's ceiling is 19, because the highest possible importance is 10 and the largest possible gap is 9. The mean path's floor is 1. All five scores pass the bound check.

### 3. Segment cut

| ID | Score, Lahore pilot district, n = 188 | Score, elsewhere, n = 546 | Difference | Hidden segment? |
|---|---:|---:|---:|---|---|
| OUT-1 | Not cut in CN24 | Not cut in CN24 | Not calculable from the supplied segment scores | Not assessed |
| OUT-2 | 12.1 | 14.6 | 14.6 minus 12.1 = 2.5 | No, both are in the solid band |
| OUT-3 | Not cut in CN24 | Not cut in CN24 | Not calculable from the supplied segment scores | Not assessed |
| OUT-4 | Not cut in CN24 | Not cut in CN24 | Not calculable from the supplied segment scores | Not assessed |
| OUT-5 | 16.2 | 15.6 | 16.2 minus 15.6 = 0.6 | No, both are in the underserved band |

The segment scores supplied by CN24 show:

- **OUT-2:** Lahore is 12.1 and elsewhere is 14.6. The difference is 2.5 points, with the score lower in Lahore. Float therefore hurts less in the Lahore pilot district, where the hotline ran first.
- **OUT-5:** Lahore is 16.2 and elsewhere is 15.6. The difference is 0.6 points, and both scores remain in the underserved band.
- No segment score is supplied for OUT-1, OUT-3 or OUT-4, so no difference or hidden-segment claim is calculated for those outcomes.

**Decision rule:** rank by score. The reading bands are:

- **15 and above:** underserved, worth building for
- **12 up to 15:** solid
- **10 up to 12:** moderate
- **Below 10:** adequately served

The bands are half-open, so a score of 15 belongs to the underserved band, while a score below 15 belongs to the solid band. No row has satisfaction above importance, so there is no overserved outcome in this cut.

## Reading the result

**OUT-5 is the release candidate for the next discovery slice.** It is the only overall score in the underserved band:

- OUT-5 score: 15.8
- Importance: 9.1
- Satisfaction: 2.4
- Gap: 6.7
- Arithmetic: 9.1 + 6.7 = 15.8

The result says that agents consider the unpaid time spent on a customer's bill highly important and poorly served today. It does not select a solution. The next pass should test how the agent's time is created, what part can be paid through the proposed PKR 5 per bill commission, and whether the agent-initiated, customer-confirmed flow changes the unpaid-time outcome.

**OUT-4 and OUT-2 are solid opportunities:**

- OUT-4, proof accepted by the customer, scores 14.3. It is important at 8.6 and poorly served at 2.9, with a 5.7 gap.
- OUT-2, float on a bill-peak day, scores 14.0. It is important at 8.8 and poorly served at 3.6, with a 5.2 gap.

Float is less painful in Lahore than elsewhere:

- Lahore: 12.1
- Elsewhere: 14.6
- Difference: 14.6 minus 12.1 = 2.5

That cut is consistent with the Lahore pilot district receiving the hotline first. Both segment scores remain solid, so the cut changes emphasis rather than the band.

**OUT-1 is also solid overall**, with a score of 12.0. It is a lower-ranked solid opportunity, not the release candidate.

**OUT-3 is adequately served**, with a score of 8.9:

- Importance: 7.4
- Satisfaction: 5.9
- Gap: 1.5
- Arithmetic: 7.4 + 1.5 = 8.9

The overall rank is therefore:

1. OUT-5, unpaid time spent on a customer's bill, 15.8, underserved
2. OUT-4, proof the customer accepts, 14.3, solid
3. OUT-2, float on a bill-peak day, 14.0, solid
4. OUT-1, confirmation before the customer leaves, 12.0, solid
5. OUT-3, payment dispute risk, 8.9, adequately served

The survey had 734 responses, so these are ranking inputs rather than proof that a particular intervention will work. The next research should preserve the distinction between the outcome and the solution, and should carry the Lahore versus elsewhere float difference into the next assumption test.

## ILLUSTRATIVE example

Invented for Sahulat's agent-assisted bill pay. SV-1 had 734 agent responses, and this sheet uses the mean aggregation.

| ID | Desired outcome | Importance | Satisfaction | Gap | Score |
|---|---|---:|---:|---:|---:|
| OUT-5 | Minimize the unpaid time spent on a customer's bill | 9.1 | 2.4 | 6.7 | 15.8 |
| OUT-4 | Minimize the time to hand the customer proof she accepts | 8.6 | 2.9 | 5.7 | 14.3 |
| OUT-2 | Minimize the likelihood of running out of float on a bill-peak day | 8.8 | 3.6 | 5.2 | 14.0 |
| OUT-1 | Minimize the time to confirm a customer's bill posted before she leaves the counter | 8.1 | 4.2 | 3.9 | 12.0 |
| OUT-3 | Minimize the likelihood a customer disputes a payment the agent keyed | 7.4 | 5.9 | 1.5 | 8.9 |

The arithmetic is:

- OUT-5: 9.1 + max(9.1 minus 2.4, 0) = 9.1 + 6.7 = **15.8**
- OUT-4: 8.6 + max(8.6 minus 2.9, 0) = 8.6 + 5.7 = **14.3**
- OUT-2: 8.8 + max(8.8 minus 3.6, 0) = 8.8 + 5.2 = **14.0**
- OUT-1: 8.1 + max(8.1 minus 4.2, 0) = 8.1 + 3.9 = **12.0**
- OUT-3: 7.4 + max(7.4 minus 5.9, 0) = 7.4 + 1.5 = **8.9**

Every score is within the mean aggregation bound of 1 to 19. OUT-5 is the only underserved outcome. OUT-4 and OUT-2 are solid. OUT-3 is adequately served.

The segment arithmetic supplied for the two outcomes with a cut is:

- OUT-2: 14.6 elsewhere minus 12.1 Lahore = **2.5**
- OUT-5: 16.2 Lahore minus 15.6 elsewhere = **0.6**

The Lahore and elsewhere scores for OUT-2 both remain in the solid band. The Lahore and elsewhere scores for OUT-5 both remain in the underserved band.

## The trap

The solution smuggled into the outcome would be: "minimize the time to use the agent app to pay a customer's bill." That statement would score the proposed interface rather than the agent's progress. OUT-5 stays solution-free: it names the unpaid time spent on a customer's bill, which an agent could improve through a customer-confirmed flow, a counter process, a commission change or another approach.

A second trap is treating the overall score as the whole finding. Float scores 14.0 overall, but the Lahore score is 12.1 and the elsewhere score is 14.6. The hotline's earlier operation in Lahore may explain part of that difference, so the next pass should not assume that one float intervention has the same value in both segments.

A third trap is false precision. The scores rank the outcomes from 734 responses. They do not establish that an intervention will produce a particular operational or financial result. OUT-5 is a discovery priority, not a pre-approved feature.

## Feeds

- [templates/discovery/opportunity-assessment.md](../templates/discovery/opportunity-assessment.md): section 2, evidence behind the answers
- [templates/discovery/opportunity-solution-tree.md](../templates/discovery/opportunity-solution-tree.md): section 2, opportunity branches ordered by score
- [templates/definition/prd.md](../templates/definition/prd.md): section 2, objectives trace to the top band
- [templates/planning/roadmap.md](../templates/planning/roadmap.md): Now and Next, with OUT-5 as the stated reason
- DISCOVER, feeding Gate 1 of pass 2: problem worth solving
- Method background: [jobs to be done](../knowledge/jobs-to-be-done.md)
- Blank worksheet: [frameworks/discovery/opportunity-scoring.md](../frameworks/discovery/opportunity-scoring.md)
- Source data: [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md)
