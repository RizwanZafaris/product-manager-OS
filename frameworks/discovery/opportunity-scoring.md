---
layer: frameworks
stage: DISCOVER
gate: 1
feeds: ["templates/discovery/opportunity-assessment.md", "templates/discovery/opportunity-solution-tree.md", "templates/definition/prd.md"]
method: "knowledge/jobs-to-be-done.md"
aliases: ["Opportunity scoring", "opportunity-scoring"]
---
# Opportunity scoring

Based on the ideas of Tony Ulwick, from What Customers Want (2005) and the Outcome-Driven Innovation method behind it. Explained here in this repository's own words.

## What it is for

Customers can rate how important an outcome is and how satisfied they are with it today, even when they cannot tell you what to build. Opportunity scoring uses those two ratings per desired outcome to rank where the market is underserved. The score rewards outcomes that matter and are poorly served, and it refuses to punish outcomes that are already well served, which is why it is one sum rather than a ratio. The output is a ranked list of outcomes with a stated gap, which is what a roadmap or a PRD's objectives section should start from. It answers "which outcome, for which segment, is worth the next release".

## Run it when

- A job map has named the struggling steps and you need to rank the outcomes inside them.
- Stakeholders disagree about which of a dozen requests matters, and the argument is opinion against opinion.
- A survey is already planned and two extra questions per outcome are cheap.

**Skip it when:** you have fewer than a handful of respondents per segment. Decimals from nine people look like science and rank noise; run interviews and the job map instead until a survey is affordable.

## Inputs you need first

- Outcome statements, one per line, in the form direction + measure + object + context ("minimize the time it takes to find the receipt for a posted charge"). No solutions inside the statement.
- A respondent sample of job performers, screened on behavior, sized per segment in the [survey design](../../templates/discovery/survey-design.md).
- The segments you will cut by (role, company size, filing frequency), decided before fielding.

## The worksheet

### 1. Scales

<!-- Both questions are asked per outcome. Use the same scale for both so the gap means
     something. State which aggregation you use and never mix them within one sheet. -->

| Question | Scale | Aggregation |
|---|---|---|
| How important is it that you can [outcome]? | 1 (not important) to 10 (critical) | Mean across respondents, or the share rating 8 or above times ten; state which |
| How satisfied are you with how you [outcome] today? | 1 (not at all) to 10 (fully) | Same as importance |

### 2. Scoring table

**Arithmetic:** gap = max(importance minus satisfaction, 0); opportunity score = importance + gap. Range 1 to 20.

| ID | Desired outcome | Job step | n | Importance (1 to 10) | Satisfaction (1 to 10) | Gap | Score | Rank |
|---|---|---|---|---|---|---|---|---|
| O1 | | | | | | | | |
| O2 | | | | | | | | |

### 3. Segment cut

| ID | Score, segment A | Score, segment B | Difference | Hidden segment? |
|---|---|---|---|---|
| | | | | [yes if one segment sits in a higher band] |

**Decision rule:** rank by score. Ulwick's own reading bands, adopted here as a convention rather than a benchmark: above 15, an underserved outcome worth building for; 12 to 15, solid; 10 to 12, moderate; below 10, adequately served. Satisfaction above importance marks an overserved outcome, a candidate for simplification or cost removal.

## Reading the result

The top band is the release candidate list; the PRD's objectives should trace to it. The overserved rows are as valuable: they name what the incumbent spends on that customers no longer notice, which is where a cheaper offer can come from. Compare bands across segments before you believe an average; an outcome scoring 11 overall may score 17 for frequent travelers and 6 for occasional filers, and the average describes nobody. Report n per segment next to every score. Where a top-band outcome rests on thin n, treat it as a hypothesis for the [assumptions register](../../templates/definition/assumptions-register.md), not a ranking.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. An invented survey of 41 filers, mean aggregation.

| ID | Desired outcome | Importance | Satisfaction | Gap | Score |
|---|---|---|---|---|---|
| O1 | Minimize the time to find the receipt for a posted charge | 9.2 | 3.1 | 6.1 | 15.3 |
| O2 | Minimize the likelihood a report is rejected for a policy breach | 8.6 | 5.0 | 3.6 | 12.2 |
| O3 | Minimize the time to learn the approval status of a report | 6.8 | 4.9 | 1.9 | 8.7 |
| O4 | Minimize the time to categorize each line | 7.2 | 6.1 | 1.1 | 8.3 |
| O5 | Minimize the effort to convert a foreign-currency amount | 4.0 | 7.5 | 0 | 4.0 |

Reading: O1 is the release; O2 is the second slice; O5 is overserved, and the currency converter the previous tool advertised can leave the marketing page. The segment cut put O3 at 12.9 for approvers and 6.4 for filers, so status visibility is an approver feature, not a filer one.

## The trap

The solution smuggled into the outcome. "Minimize the effort to have the copilot read my receipts" scores high because respondents rate the thing they were just shown, and the sheet then proves the roadmap the team already had. An outcome statement names a measure of progress the customer would recognize without your product existing; if you cannot imagine a competitor serving it another way, it is a feature. The quieter version is false precision: a score of 15.3 from 41 people is a rank, not a measurement, and the second decimal decides nothing.

## Feeds

- [Opportunity assessment](../../templates/discovery/opportunity-assessment.md): section 2 (evidence behind the answers)
- [Opportunity solution tree](../../templates/discovery/opportunity-solution-tree.md): section 2 (opportunity branches), ordered by score
- [PRD](../../templates/definition/prd.md): section 2 (objectives) traces to the top band
- [Roadmap](../../templates/planning/roadmap.md): Now and Next, with the score as the stated reason
- DISCOVER, feeding [Gate 1: problem worth solving](../../os/STAGE-GATES.md)
- Method background: [jobs to be done](../../knowledge/jobs-to-be-done.md); [JTBD job map](jtbd-job-map.md) for the steps the outcomes belong to
