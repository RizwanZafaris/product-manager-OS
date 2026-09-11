# Product-market fit survey: Sahulat Bill Pay

Fills [frameworks/discovery/pmf-survey.md](../frameworks/discovery/pmf-survey.md). Everything here is invented and every number is ILLUSTRATIVE: Sahulat, its people, agents, customers, billers, bank, aggregator and telco are fiction, and the values below were chosen so that this worksheet agrees with [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md), not to describe any real wallet, market or survey.

**Owner:** Sara Lodhi, Data analyst · **Date:** 2026-09-15 · **Status:** Complete through the SV-2 read toward Gate 6

## What it is for

SV-2 asks wallets that paid at least two bills through Sahulat how they would feel if they could no longer pay bills through the wallet. The survey is a stated-preference signal, not proof of behavioral fit.

The decision is whether to scale the existing positioning, or narrow the next pass around the segment that finds Sahulat hardest to give up. The bar was written before fielding:

> **At fit:** 40 percent very disappointed inside the target segment.

This bar was written before SV-2 fielding, as recorded in CN36. The survey population was 12,400 wallets that paid at least two bills between 2026-07-06 and 2026-08-31, and 386 completed the survey.

The result is below the bar overall:

- Very disappointed: 131 of 386
- Arithmetic: 131 / 386 x 100 = 33.9 percent
- Bar comparison: 33.9 percent is below 40 percent

The agent-keyed segment is above the bar:

- Agent keyed the last payment: 94 of 214 very disappointed
- Arithmetic: 94 / 214 x 100 = 43.9 percent
- Bar comparison: 43.9 percent is above 40 percent

This is the band where fit exists for a segment the positioning does not name. It supports D8, the 2026-08-28 pivot to agent-assisted bill pay, and should be read with the cohort result rather than treated as a standalone Gate 6 claim.

## Run it when

- A live product has users who completed the core action at least twice.
- A growth or positioning decision needs a stated-preference read from the same behavioral population.
- The retention or cohort read is available beside the survey.
- A bar has been written before fielding.

SV-2 was run after the product was live and after the population had paid at least two bills. Naveed Akhtar's team called 1,500 wallets drawn at random from the population between 2026-09-01 and 2026-09-10. Sara Lodhi tabulated the 386 completed responses on 2026-09-15.

**Skip it when:** the product is not in real use. This population screen avoids asking prospects to be disappointed about losing a product they have not relied on.

## Inputs you need first

| Input | Sahulat read |
|---|---|
| Population | 12,400 wallets that paid at least two bills between 2026-07-06 and 2026-08-31 |
| Sample | 1,500 wallets drawn at random; 386 completed |
| Fieldwork | Naveed Akhtar's team, 2026-09-01 to 2026-09-10 |
| Tabulation | Sara Lodhi, 2026-09-15 |
| Bar | 40 percent very disappointed inside the target segment, written before fielding |
| Cohort read | July cohort: 5,640 of 9,400 paid again in August, 60 percent; 4,890 of 9,400 paid again in September to 2026-09-20, 52 percent, September partial |
| Related funding-path read | July cohort cash-in-within-two-hours group: 4,530 of 7,300 paid in August, 62 percent; balance-held-over-48-hours group: 440 of 850, 52 percent |
| Positioning context | D8, 2026-08-28, pivot to agent-assisted bill pay; next DISCOVER pass opens 2026-09-07 |

The cohort read is not added to the survey counts. It is a behavioral check on the same product direction.

## The worksheet

### 1. Questions

| # | Question | Answers |
|---|---|---|
| Q1 | How would you feel if you could no longer pay bills through Sahulat? | Very disappointed / Somewhat disappointed / Not disappointed / I no longer use it |
| Q2 | What type of person do you think would benefit most from paying bills through Sahulat? | Open text |
| Q3 | What is the main benefit you get from paying bills through Sahulat? | Open text |
| Q4 | How can we improve Sahulat bill pay for you? | Open text |
| Q5 (optional) | What would you use instead if Sahulat bill pay were gone? | Open text, not tabulated in the supplied SV-2 result rows |

### 2. Tabulation

The denominator is 386 completed responses.

| Answer to Q1 | Count | Share of responses | By segment: who keyed the last payment | By segment: plan or tenure |
|---|---:|---:|---|---|
| Very disappointed | 131 | 131 / 386 x 100 = **33.9 percent** | Agent keyed: 94 / 214 x 100 = **43.9 percent**; customer keyed: 37 / 172 x 100 = **21.5 percent** | Not available in CN35 to CN38 |
| Somewhat disappointed | 142 | 142 / 386 x 100 = **36.8 percent** | Agent-keyed and customer-keyed split not tabulated in the supplied result rows | Not available in CN35 to CN38 |
| Not disappointed | 88 | 88 / 386 x 100 = **22.8 percent** | Agent-keyed and customer-keyed split not tabulated in the supplied result rows | Not available in CN35 to CN38 |
| No longer use | 25 | 25 / 386 x 100 = **6.5 percent** | Agent-keyed and customer-keyed split not tabulated in the supplied result rows | Not available in CN35 to CN38 |
| **Total** | **386** | **131 + 142 + 88 + 25 = 386; 33.9 + 36.8 + 22.8 + 6.5 = 100.0 percent** | **214 + 172 = 386; 94 + 37 = 131 very disappointed** | Not available |

Segment arithmetic:

- Agent keyed: 214 respondents, 94 very disappointed, 214 minus 94 = 120 not very disappointed.
- Customer keyed: 172 respondents, 37 very disappointed, 172 minus 37 = 135 not very disappointed.
- Segment total: 214 + 172 = 386 respondents.
- Very disappointed total: 94 + 37 = 131.
- Segment very-disappointed shares: 94 / 214 x 100 = 43.9 percent; 37 / 172 x 100 = 21.5 percent.
- Overall check: 131 / 386 x 100 = 33.9 percent.

### 3. Segmentation

Q2 and Q3 were coded to identify the benefit named by the very disappointed respondents. The supplied tabulation identifies the main benefit as paying at a counter the respondent already visits, with no trip. The segment field used for the decision is who keyed the last payment.

| Step | Result |
|---|---|
| Who the very disappointed are (Q2 coded, plus the export's role field) | The strongest segment is the **agent-keyed** segment: 94 very disappointed respondents out of 214 agent-keyed respondents. The survey result does not supply a separate Q2 count for each coded person type. |
| The main benefit they name (Q3 coded) | **Paid at a counter they already visit, no trip.** This is the benefit used to code the same-benefit somewhat group. |
| Very-disappointed share inside that segment alone | **94 / 214 x 100 = 43.9 percent.** This is above the pre-fielding bar of 40 percent by 43.9 minus 40 = **3.9 percentage points**. |
| Somewhat-disappointed users who name the same benefit | **61**. Their Q4 answers are the roadmap for the counter-based experience. |
| Somewhat-disappointed users who name a different benefit | **81**. Arithmetic: 142 total somewhat disappointed minus 61 same-benefit = 81 different-benefit. Set aside for this positioning decision because they want a different benefit. |
| Not-disappointed users' Q5 alternatives | Not tabulated in CN35 to CN38. No competition-in-their-words conclusion is made from the supplied read. |

The segment comparison is:

| Segment | Respondents | Very disappointed | Arithmetic | Bar comparison |
|---|---:|---:|---|---|
| Overall | 386 | 131 | 131 / 386 x 100 = 33.9 percent | Below 40 percent by 6.1 percentage points |
| Agent keyed last payment | 214 | 94 | 94 / 214 x 100 = 43.9 percent | Above 40 percent by 3.9 percentage points |
| Customer keyed last payment | 172 | 37 | 37 / 172 x 100 = 21.5 percent | Below 40 percent by 18.5 percentage points |

The cohort check is:

| Cohort or funding path | Starting wallets | Returned wallets | Arithmetic | Reading |
|---|---:|---:|---|---|
| July cohort, paid again in August | 9,400 | 5,640 | 5,640 / 9,400 x 100 = 60 percent | Behavioral repeat use exists |
| July cohort, paid again in September to 2026-09-20 | 9,400 | 4,890 | 4,890 / 9,400 x 100 = 52 percent | September is partial, so it is not a final cohort age |
| July cohort, cash-in within two hours of first payment, paid again in August | 7,300 | 4,530 | 4,530 / 7,300 x 100 = 62 percent | Repeat behavior in the cash-in path |
| July cohort, balance held over 48 hours for first payment, paid again in August | 850 | 440 | 440 / 850 x 100 = 52 percent | Balance-first behavior is weaker than the cash-in path |

The survey and cohort reads point in the same direction for the pivot, but they answer different questions:

- SV-2 says the agent-keyed segment reports stronger loss aversion, 43.9 percent very disappointed.
- The cohort read shows repeat payment behavior, including 60 percent of the July cohort paying again in August.
- The balance-held-over-48-hours path retained at 52 percent in August, below the 62 percent for the cash-in-within-two-hours path.
- Therefore, the evidence supports narrowing toward agent-assisted bill pay, not returning to the balance-first positioning.

**Decision rule:** compare the very-disappointed share inside the best segment, not only the overall share, against the bar written before fielding. Then act by band below.

## Reading the result

The 40 percent threshold is being used as a heuristic bar for this survey, not as a law or market measurement. The population, screening rule and segment must travel with every share.

| Band | What it says | What to do |
|---|---|---|
| Well below your bar in every segment | Nobody yet finds the product hard to give up | Not the result here. The customer-keyed segment is below the bar, but the agent-keyed segment is above it. |
| Below overall, at or above in one segment | Fit exists for a segment the positioning does not name | **This is the result.** Overall is 33.9 percent, below 40 percent, while the agent-keyed segment is 43.9 percent, above 40 percent. Narrow onboarding and messaging toward agent-assisted bill pay, and build from the 61 somewhat-disappointed users who name the same benefit. |
| At or above your bar in the target segment | The product is hard to give up for that segment | Do not call overall product-market fit. Track the agent-assisted cohort, confirm the next read with retention, and take the narrowed positioning toward the next Gate 6 decision. |

The operating decision is:

1. Keep the 40 percent bar and report the population beside every share.
2. Treat agent-keyed bill pay as the target segment for the next pass.
3. Use the same-benefit somewhat group, 61 respondents, as the Q4 roadmap input.
4. Set aside the 81 somewhat-disappointed respondents naming a different benefit for this positioning decision.
5. Pair future survey reads with cohort retention, because the survey is stated preference and the cohort read is behavior.
6. Do not reposition around customers who key their own payments, whose very-disappointed share was 21.5 percent.
7. Continue the D8 pivot toward agent-assisted bill pay rather than the failed balance-first hypothesis.

## ILLUSTRATIVE example

This is an ILLUSTRATIVE Sahulat read, not a real survey or market result. SV-2 called 1,500 randomly drawn wallets from the 12,400-wallet population that paid at least two bills between 2026-07-06 and 2026-08-31. Naveed Akhtar's team completed 386 calls between 2026-09-01 and 2026-09-10, and Sara Lodhi tabulated them on 2026-09-15.

The team wrote the 40 percent very-disappointed bar before fielding. Overall, 131 of 386 respondents were very disappointed:

> 131 / 386 x 100 = 33.9 percent

That result was below the bar. The agent-keyed segment contained 214 respondents, of whom 94 were very disappointed:

> 94 / 214 x 100 = 43.9 percent

The customer-keyed segment contained 172 respondents, of whom 37 were very disappointed:

> 37 / 172 x 100 = 21.5 percent

The result therefore falls in the band where fit exists for a segment the positioning does not name. Of the 142 somewhat-disappointed respondents, 61 named the same benefit as the very disappointed group, paying at a counter they already visit with no trip:

> 142 - 61 = 81 respondents naming a different benefit

The cohort read provides a behavioral check. Of the 9,400 wallets in the July cohort, 5,640 paid again in August:

> 5,640 / 9,400 x 100 = 60 percent

By September 20, 4,890 had paid again:

> 4,890 / 9,400 x 100 = 52 percent

September is partial. The read also shows that 4,530 of 7,300 July wallets whose first payment was funded by a cash-in within two hours paid again in August, or 62 percent, while 440 of 850 wallets whose first payment used a balance held over 48 hours paid again, or 52 percent.

Decision: keep the overall result below the bar, reposition the next pass around agent-assisted bill pay, use the 61 same-benefit somewhat-disappointed respondents for Q4 themes, and confirm the narrowed segment with cohort behavior before describing fit beyond this Gate 6 read.

## The trap

Chasing the number would mean changing the survey population until the overall share clears 40 percent. SV-2 avoids that by naming the population, retaining the overall denominator of 386, and showing the segment denominator of 214.

The opposite trap would be declaring product-market fit from 43.9 percent in the agent-keyed segment while hiding the 33.9 percent overall result. The correct statement is narrower:

> The overall share is below the bar, and the agent-keyed segment is above it.

The cohort read is the guardrail against treating the survey as behavior. The July cohort's August repeat rate is 60 percent, while the September read is 52 percent and partial. The funding-path split also does not support returning to balance-first: the balance-held-over-48-hours group repeated at 52 percent in August, compared with 62 percent for the cash-in-within-two-hours group.

Report these together:

- Population: 12,400 wallets that paid at least two bills.
- Completed responses: 386.
- Overall very disappointed: 131 / 386 = 33.9 percent.
- Agent-keyed very disappointed: 94 / 214 = 43.9 percent.
- Customer-keyed very disappointed: 37 / 172 = 21.5 percent.
- Same-benefit somewhat disappointed: 61.
- Different-benefit somewhat disappointed: 81.
- July cohort repeat in August: 5,640 / 9,400 = 60 percent.
- July cohort repeat by September 20: 4,890 / 9,400 = 52 percent, September partial.

## Feeds

- [templates/discovery/discovery-synthesis.md](../templates/discovery/discovery-synthesis.md): sections 3 and 5, the coded Q2 to Q4 answers as themes. The supplied SV-2 result provides 61 same-benefit somewhat-disappointed answers and 81 different-benefit answers; Q5 alternatives were not tabulated here.
- [templates/planning/positioning.md](../templates/planning/positioning.md): section 4, customers who care most. Use the agent-keyed segment and the benefit, paying at a counter already visited with no trip.
- [templates/planning/growth-plan.md](../templates/planning/growth-plan.md): section 1, where the metric tree stands, and section 2, the next growth bet. Do not use the overall 33.9 percent result as a scale signal.
- [templates/operate/metrics-review.md](../templates/operate/metrics-review.md): section 3, the cohort read as a guardrail beside the survey.
- OPERATE, feeding [Gate 6: outcomes verified](../os/STAGE-GATES.md). The result supports D8's narrowed direction, not an overall fit declaration.
- Method background: [knowledge index, Sean Ellis PMF survey entry](../knowledge/INDEX.md); [north star metric](../knowledge/north-star-metric.md).

**Exit-gate walk:** Sara Lodhi, Data analyst, signed 2026-09-15: **SV-2 is complete for the Gate 6 read.** The overall share, segment denominator, pre-fielding bar, coding result, cohort comparison, population and limitations are recorded. Open: Faisal Mirza owns the next Gate 6 decision on the narrowed agent-assisted positioning.
