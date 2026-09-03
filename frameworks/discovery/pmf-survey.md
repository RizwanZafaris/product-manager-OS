---
layer: frameworks
stage: OPERATE
gate: 6
feeds: ["templates/discovery/discovery-synthesis.md", "templates/planning/positioning.md", "templates/planning/growth-plan.md"]
method: "knowledge/INDEX.md"
aliases: ["Product-market fit survey", "pmf-survey"]
---
# Product-market fit survey

Based on the ideas of Sean Ellis, from the product/market fit survey he introduced in 2009; the segmentation steps follow a later adaptation by Rahul Vohra (2019). Explained here in this repository's own words.

## What it is for

The survey asks users of a live product one load-bearing question: how would you feel if you could no longer use it? The share answering "very disappointed" is a signal of whether the product has become hard to give up for some group of people, which is what product-market fit means in practice. The follow-up questions turn the signal into a map: who the very disappointed users are, what benefit they get, and what the "somewhat disappointed" users who want the same benefit would need. The decision it improves is the one teams get wrong most often: whether to narrow and deepen, or to scale.

## Run it when

- A product or a major feature has been live long enough that users have had several chances to return.
- Growth spend is proposed and nobody can name the segment the product is loved by.
- Before Gate 6, to pair the retention curve with a stated-preference read of the same users.

**Skip it when:** the product is not in real use yet. Prospects and pilot visitors cannot be disappointed to lose what they have not relied on; run interviews and a design sprint instead.

## Inputs you need first

- The population: users who completed the core action at least twice in a stated window, exported with role and plan.
- A sample plan with a minimum n per segment, from the [survey design](../../templates/discovery/survey-design.md).
- The retention curve for the same cohorts, from [metrics review](../../templates/operate/metrics-review.md), so the survey never stands alone.
- The bar you will treat as "at fit", written down before fielding, with the reason you chose it.

## The worksheet

### 1. Questions

| # | Question | Answers |
|---|---|---|
| Q1 | How would you feel if you could no longer use [product]? | Very disappointed / Somewhat disappointed / Not disappointed / I no longer use it |
| Q2 | What type of person do you think would benefit most from [product]? | Open text |
| Q3 | What is the main benefit you get from [product]? | Open text |
| Q4 | How can we improve [product] for you? | Open text |
| Q5 (optional) | What would you use instead if [product] were gone? | Open text |

### 2. Tabulation

| Answer to Q1 | Count | Share of responses | By segment: [role] | By segment: [plan or tenure] |
|---|---|---|---|---|
| Very disappointed | | | | |
| Somewhat disappointed | | | | |
| Not disappointed | | | | |
| No longer use | | | | |

### 3. Segmentation

<!-- Code the Q2 and Q3 answers into a handful of labels before counting. The label with the
     most very-disappointed users is the segment; their most common Q3 answer is the benefit. -->

| Step | Result |
|---|---|
| Who the very disappointed are (Q2 coded, plus the export's role field) | |
| The main benefit they name (Q3 coded) | |
| Very-disappointed share inside that segment alone | |
| Somewhat-disappointed users who name the same benefit | [count; their Q4 answers are the roadmap] |
| Somewhat-disappointed users who name a different benefit | [count; set aside, they want a different product] |
| Not-disappointed users' Q5 alternatives | [the competition, in their words] |

**Decision rule:** compare the very-disappointed share inside the best segment, not the overall share, against the bar you wrote down. Then act by band, below.

## Reading the result

The widely quoted threshold is a heuristic, not a law. Ellis drew his rule of thumb (he put it at about 40 percent of respondents answering very disappointed) from his own work with a set of companies; it is one practitioner's sample, it moves with who you surveyed and how you screened, and it has never been a measurement of anything in your market. Use it as a prompt for the bands, and write your own bar down with its reason.

| Band | What it says | What to do |
|---|---|---|
| Well below your bar in every segment | Nobody yet finds the product hard to give up | Stop scaling; interview the very disappointed few; narrow scope to the benefit they name |
| Below overall, at or above in one segment | Fit exists for a segment the positioning does not name | Narrow onboarding and messaging to that segment; build from the Q4 answers of the same-benefit somewhat group |
| At or above your bar in the target segment | The product is hard to give up for that segment | Track by cohort; move to growth; confirm with the retention curve before anyone calls it fit in a board deck |

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot pilot. 48 responses from filers active in the last 30 days: 19 very disappointed, 21 somewhat, 8 not. Overall, the share sat below the bar the team had written down. Segmenting: 15 of the 19 very disappointed were frequent travelers (five or more reports a quarter), and 12 of them named the same benefit, "I stop losing receipts". Inside the traveler segment (15 of 23 respondents) the share was above the bar. Of the 21 somewhat, 9 named the same benefit and asked in Q4 for card feed matching; 12 named "drafting the business-purpose text", a different product, set aside. Decision: reposition the pilot to frequent travelers, build card feed matching, re-survey after that release, and check the traveler retention curve before the quarterly update claims anything.

## The trap

Chasing the number. The overall share disappoints, so the team re-surveys a friendlier population, drops the users who only tried it once, hits the bar, and declares fit. The retention curve keeps decaying, because a survey answer is a stated preference and the curve is behavior. When the two disagree, believe the curve, and report the survey population beside every share so a reader can see who was asked. The mirror failure: surveying everyone with a login, including people who never completed the core action, and concluding there is no fit for anyone.

## Feeds

- [Discovery synthesis](../../templates/discovery/discovery-synthesis.md): sections 3 and 5, the coded Q2 to Q4 answers as themes
- [Positioning](../../templates/planning/positioning.md): section 4 (customers who care most), from the best segment
- [Growth plan](../../templates/planning/growth-plan.md): section 1 (where the metric tree stands) and section 2 (the next growth bet)
- [Metrics review](../../templates/operate/metrics-review.md): section 3, as a guardrail read beside retention
- OPERATE, feeding [Gate 6: outcomes verified](../../os/STAGE-GATES.md); for a new product, Gate 1 evidence
- Method background: [knowledge index, Sean Ellis PMF survey entry](../../knowledge/INDEX.md); [north star metric](../../knowledge/north-star-metric.md)
