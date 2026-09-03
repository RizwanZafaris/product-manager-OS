---
layer: templates
stage: DISCOVER
gate: 1
feeds: []
method: ""
aliases: ["Survey Design", "survey-design"]
---
# Survey Design: [survey short name]

Stage: DISCOVER, feeds [Gate 1: problem worth solving](../../os/STAGE-GATES.md); also used in OPERATE for satisfaction and fit measures
Knowledge: [Kano survey worksheet](../../frameworks/discovery/kano-survey.md), [PMF survey worksheet](../../frameworks/discovery/pmf-survey.md)
Skill: [research-agent](../../agents/research-agent.md) for fielding, [analyst-agent](../../agents/analyst-agent.md) for the analysis plan

> **Delete any section you do not need.** A survey earns its cost only after interviews have told you which questions to ask and which answers to offer; if fewer than five interviews exist, go back to [user-research-plan.md](user-research-plan.md). Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- A survey counts how many, not why. Interviews (user-research-plan.md,
     interview-guide.md) own why; discovery-synthesis.md owns what it all means
     together; ../operate/experiment-brief.md owns any question that is causal.
     What makes a survey honest is the analysis plan written before the first
     response: which question answers which research question, cut how, and
     what result changes which decision. Fill the goal, the decision it informs,
     and the analysis plan first; then write questions to fit the analysis,
     never the other way round. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / Piloted / Fielding / Analyzed

## 1. Goal and decision

| Field | Value |
|---|---|
| Research question | [one; a second one is a second survey] |
| Decision this informs | [the choice, who makes it, by when] |
| Result that would change the decision | [state it before fielding: "if fewer than [share] report X, we drop Y"] |
| Why a survey and not five more interviews | [what needs counting, and in whom] |

## 2. Sample

<!-- Who you are describing, who you can reach, and how the two differ. The
     target count is a field: reason it from the smallest segment you must read
     and the precision the decision needs, and write the reasoning down. -->

| Field | Value |
|---|---|
| Population described | [who the result is a claim about] |
| Sampling frame | [the list you can actually reach, and who it leaves out] |
| Sampling method | [census of the frame / random / stratified by segment / self-selected, and the bias that implies] |
| Target responses | [count, with the reasoning] |
| Segments that must be readable on their own | [list, with the minimum per segment] |
| Incentive | [what, and the bias it introduces] |
| Field window | [dates; reminders on which days] |

## 3. Question bank

<!-- One row per question, in the order asked. Type sets the analysis: single
     choice, multiple choice, rating scale (state the points and the labels),
     ranking, open text, Kano pair (functional and dysfunctional forms from the
     worksheet), PMF question (from the worksheet). Ask about past behavior
     before attitudes; demographics last. Every question serves an RQ from
     section 1 or a segment cut from section 2; delete the rest. -->

| # | Question text, as the respondent sees it | Type | Answer options (balanced, exhaustive, one "none of these") | Serves (RQ or segment cut) | Required |
|---|---|---|---|---|---|
| Q1 | | | | | |
| Q2 | | | | | |

**Screening question and routing:** [who is screened out at Q1, and where each answer routes]
**Estimated completion time:** [minutes, from the pilot]

## 4. Bias checks

<!-- Run before the pilot, by someone who did not write the questions. Every
     row gets a pass or a fix. -->

| Check | Passes when | Result |
|---|---|---|
| Leading wording | no question suggests its answer or names the product's virtue | |
| Double-barreled | each question asks one thing | |
| Acquiescence | agree or disagree scales are balanced with reversed items, or replaced by specific choices | |
| Order effects | attitude questions come after behavior; options rotated where order could steer | |
| Recall period | every "how often" names a period the respondent can remember | |
| Social desirability | no question makes one answer the respectable one | |
| Coverage | every likely answer has an option; "other" has a text box | |
| Length | completion time from the pilot is under [agreed minutes] | |
| Frame bias | section 2 states who the frame leaves out and how that bends the result | |

## 5. Pilot

- Pilot respondents: [count, drawn from the frame]
- Watched for: completion time, the drop-off question, questions answered "other" more than expected, free text that reveals a missing option
- Changes made after the pilot: [list, with question ids]

## 6. Analysis plan

<!-- Written before fielding. Thresholds are fields: agree them with the
     decision owner, then commit. A threshold chosen after the results are in
     is a story, not a finding. -->

| RQ | Questions | Cut by (segment) | Statistic (share, mean, distribution, Kano class, PMF share) | Threshold agreed in advance | Action at each result |
|---|---|---|---|---|---|
| RQ1 | | | | [threshold] | [above: ...; below: ...] |

- Open text handling: [coded by whom, using the feedback-synthesis skill; codes agreed before reading]
- Minimum responses before any segment is reported: [count]
- Where results are filed: [discovery-synthesis.md section 2, as a source row]

## 7. Distribution, consent, and data handling

- Channel and who sends: [in-app, email, panel; owner]
- What respondents are told: [purpose, anonymity or not, retention]
- Personal data collected: [fields; if any, complete ../architecture/privacy-impact-assessment.md or cite the one that covers this]
- Raw data location, access, and deletion date: [location, who can read it, YYYY-MM-DD]

## Exit gate (feeds Gate 1: problem worth solving)

Results enter [discovery-synthesis.md](discovery-synthesis.md) as a source and, for Kano or PMF questions, the worksheet tabulation, toward [Gate 1](../../os/STAGE-GATES.md).

- [ ] One research question, one decision, and the result that would change it are written before fielding
- [ ] The frame's gaps and the sampling bias are stated, and the target count carries its reasoning
- [ ] Every question serves an RQ or a segment cut, and every bias check has a result
- [ ] The analysis plan names thresholds agreed with the decision owner before the first response
- [ ] A pilot ran and its changes are logged
- [ ] Consent wording and data handling are stated, with a deletion date
- [ ] Signed by [name], [date]
