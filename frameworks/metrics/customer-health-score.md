---
layer: frameworks
stage: OPERATE
gate: 6
feeds: ["templates/operate/customer-success-handoff.md", "templates/operate/metrics-review.md", "templates/operate/metrics-dictionary.md"]
method: "knowledge/INDEX.md"
aliases: ["Customer Health Score", "customer-health-score"]
---
# Customer Health Score

No single originator for the health score: it grew up in customer success practice at subscription software companies, and no one author or paper defines it. The Net Promoter Score is Fred Reichheld's, from "The One Number You Need to Grow", Harvard Business Review (2003). The critique of it below draws on Timothy L. Keiningham, Bruce Cooil, Tor Wallin Andreassen and Lerzan Aksoy, "A Longitudinal Examination of Net Promoter and Firm Revenue Growth", Journal of Marketing (2007), and on this repository's [UX measurement card](../../knowledge/design/ux-measurement.md). CSAT has no single originator. Explained here in this repository's own words.

## What it is for

One number per account that says, early enough to act, which customers are likely to leave or not renew, so customer success spends its hours on the accounts where an hour changes the outcome. The score is a weighted sum of four to six leading signals, each put on a 0 to 100 scale, and it is banded red, amber and green. The part that makes it a measurement instead of a colour scheme is the back-test in Step 7: the score is computed as it would have read before past renewals, and it earns trust only if it would have flagged the accounts that actually left. This sheet also defines NPS and CSAT precisely, because both arrive in health scores as signals and both are misread more often than they are read.

## Run it when

- Customer success covers more accounts than its people can review one by one each month, and the order they are reviewed in is set by who shouted
- A launch changes the behaviour a health signal measures, and the bands need re-checking before the [customer success handoff](../../templates/operate/customer-success-handoff.md) names renewal-risk accounts
- A health score exists, nobody can say when it was last checked against renewals, and a forecast is being built on it
- NPS or CSAT is reported as a trend and nobody has stated the response count or the margin of error

**Skip it when:** you have fewer than about 30 churned or non-renewed accounts in your history to back-test against, or fewer than about 50 accounts in total. With that little history the weights cannot be checked, and with that few accounts the person who owns them already knows which ones are in trouble; a monthly account-by-account review in the [metrics review](../../templates/operate/metrics-review.md) beats an untestable composite.

## Inputs you need first

- The outcome the score predicts and the unit it is computed for, agreed with whoever owns renewals
- Per-account usage history from the [analytics instrumentation spec](../../templates/delivery/analytics-instrumentation-spec.md), including the activation event from [activation and churn diagnosis](activation-churn-diagnosis.md)
- Seat counts, contract dates and renewal outcomes from the billing or CRM system, for at least the last four quarters
- Support ticket history with the canonical severity from the [testing strategy](../../templates/delivery/testing-strategy.md) ladder
- Survey responses with the account each response belongs to, the date, and the question wording as asked
- The churn codes from Part 3 of the [activation and churn diagnosis](activation-churn-diagnosis.md), to read why the score missed the accounts it missed

## The worksheet

### Step 1: the outcome and the lead time

| Field | Answer |
|---|---|
| Unit scored | [account, workspace, or contract] |
| Outcome predicted | [renewed at term end / still paying 90 days later] |
| Lead time | [the score is read this many days before the outcome date, long enough for a save play to run] |
| Segments scored separately | [plan, size band, sales-led versus self-serve; a segment whose back-test differs gets its own cut points] |
| Score owner | [name; the one person who may change signals, weights or bands] |

### Step 2: pick four to six leading signals

A leading signal moves before the customer decides; a lagging one moves after. Invoice paid late, a cancellation request, and a usage collapse in the last fortnight before term end are lagging, and a score built from them reports news the account manager already has.

| # | Signal | Definition: numerator / denominator, period | Why it should lead the outcome | Source | Owner |
|---|---|---|---|---|---|
| H1 | [e.g. seat activation] | [active seats in the last 28 days / paid seats] | | | |
| H2 | [e.g. core-action trend] | [core actions per active seat per week, last 4 weeks / the prior 12 weeks] | | | |
| H3 | [e.g. support friction] | [tickets at severity S1 or S2 in the last 60 days] | | | |
| H4 | [e.g. sponsor engaged] | [a meeting or reply from the named executive sponsor in the last 90 days, yes or no] | | | |
| H5 | [e.g. sentiment] | [see Step 6] | | | |
| H6 | [optional] | | | | |

Rules: one signal per construct, because two usage counts that rise and fall together are one signal counted twice; at least one signal that is not usage; nothing a customer success manager types in as a judgement, unless the field has a written rubric and a date stamp.

### Step 3: normalise each signal to 0 to 100

Pick one method per signal and state its anchor points.

- Linear, higher is better: s = 100 x (x minus floor) / (target minus floor), then clip to 0 and 100
- Linear, lower is better: s = 100 x (ceiling minus x) / (ceiling minus best), then clip to 0 and 100
- Binary: s = 100 when the condition holds, 0 when it does not
- Percentile within segment: s = the account's percentile rank on x among accounts in the same segment, 0 to 100

| Signal | Method | Floor or ceiling | Target or best | Why those anchor points |
|---|---|---|---|---|
| H1 | | | | |

Anchors come from the distribution, not from ambition: a floor near the value churned accounts typically showed, a target near the value renewing accounts typically showed. A target nobody reaches compresses every account into the bottom half of the scale.

### Step 4: weights that sum to 1

| Signal | Weight | Why this weight |
|---|---|---|
| H1 | | |
| Total | 1.00 | |

Rules: the weights sum to exactly 1.00; no single weight above 0.40, or the composite is that one signal with decoration; weights are set before the back-test and changed only by a back-test, never by a quarter-end conversation.

### Step 5: the score and the bands

Health = w_1 x s_1 + w_2 x s_2 + ... + w_n x s_n, which runs from 0 to 100.

When a signal is missing for an account, drop it and divide by the weight that remains: Health = (the sum of w_i x s_i over available signals) / (the sum of w_i over available signals). If the available weight is under 0.70, the account is marked partial and is not banded; a score built from half its inputs is a different score.

| Band | Starting cut point | Meaning | What happens |
|---|---|---|---|
| Green | 70 and above | on track | no action from this score |
| Amber | 40 to 69 | watch | the owner reviews the account this month |
| Red | below 40 | at risk | a named save play starts, with a date |
| Falling | a drop of 15 points or more in 30 days, any band | changing | reviewed this week, whatever the band |

The cut points above are starting values; Step 7 resets them.

### Step 6: NPS and CSAT, defined precisely

**Net Promoter Score.** One question: how likely the respondent is to recommend the product to a friend or colleague, answered on a 0 to 10 scale. Promoters answer 9 or 10, passives 7 or 8, detractors 0 to 6. NPS = percent promoters minus percent detractors, so it runs from minus 100 to plus 100. Its 95% margin of error, in points, is 100 x 1.96 x the square root of ((p_P + p_D minus (p_P minus p_D) squared) / n), where p_P and p_D are the promoter and detractor shares as fractions and n is the number of responses. Report NPS with n and that margin, every time.

**CSAT.** One question about one interaction or task: how satisfied the respondent was, on a 1 to 5 scale. CSAT = responses of 4 or 5 / all responses x 100. Report it with the response count and the response rate (responses / interactions surveyed). A CSAT on a different scale, or asked after a different touchpoint, is a different number and is not trended against this one.

**The critique, stated honestly.** NPS measures a stated intention to recommend. It is not a usability measure and not a behaviour; the [UX measurement card](../../knowledge/design/ux-measurement.md) records that it correlates with usability without measuring it, and that the two can move in opposite directions on the same release. The subtraction discards the distribution: 40 percent promoters with 40 percent detractors scores 0, and so does 100 percent passives, and those are very different customer bases. As a difference of two proportions it carries a wide sampling error, so a quarter-to-quarter move of a few points on a few hundred responses is usually inside the margin. Reichheld's article argued that this one question tracked growth better than conventional satisfaction questions; Keiningham and colleagues (2007) reported that in their data it did not outperform the other satisfaction measures they compared it with. Response bias works on it from every side: who chooses to answer, when the survey is sent, and staff who ask customers for a 10. Once NPS becomes a team's target, it moves through survey management faster than through the product.

**In a health score.** An account rarely has enough responses for its own NPS. Use the sentiment signal only when the account has at least 3 recommend answers in the last 180 days, and score it as the mean answer x 10, which is a normalised average, not an NPS. Below 3 responses, the signal is missing and Step 5's missing-signal rule applies.

### Step 7: back-test before anyone trusts it

1. Take every account whose outcome date fell inside a closed past window, for example the last four quarters
2. Compute each account's score as of the lead time before its outcome date, using only data that existed on that date. Exclude anything recorded after the customer gave notice, and any field edited after the outcome
3. Tabulate the outcome per band, and run the same tabulation for the best single signal on its own
4. Write the result into the table below. If a different split separates the outcomes better, propose new cut points, and check them on the next closed window before they replace the old ones; cut points tuned and judged on the same accounts always look right

| Band (as of lead time) | Accounts | Renewed | Churned | Renewal rate | Share of all churned accounts |
|---|---|---|---|---|---|
| Green | | | | | |
| Amber | | | | | |
| Red | | | | | |
| Total | | | | | 100% |

Arithmetic:

- Renewal rate per band = renewed in the band / accounts in the band
- Capture = churned accounts that were red or amber at lead time / all churned accounts
- Red precision = churned red accounts / red accounts
- False-alarm share = renewed accounts that were red or amber / all renewed accounts, which is the customer success time the score spends on accounts that were going to stay
- Single-signal comparison: flag the same number of accounts, lowest first, using the best single signal alone, and compute its capture

**The score is validated only when all four hold:** at least 30 churned accounts in the window; renewal rate falls from green to amber to red; capture meets the target the renewals owner set before the back-test, written here: [target]; and the composite's capture beats the best single signal's at the same number of flagged accounts. A score that fails any of the four is labelled unvalidated on every dashboard that shows it, and work assigned from it is labelled a hypothesis. Re-run the back-test every two quarters, and whenever a signal, a weight, the packaging or the product's core action changes.

## Reading the result

The band is a triage order, not a forecast. Red means look now; it does not mean the account will leave. Judge red precision against the base rate, not against 100 percent: in the example below, red accounts churned at 52.8 percent against 18.3 percent across all accounts, and that concentration is what triage needs. Read movement beside level: the Falling flag catches a green account sliding quickly, which is the case a monthly band review sees too late.

Read the churned accounts the score called green. They are what the signals cannot see: an acquisition, a champion who left, a budget decision made above the user base. Code them with the [activation and churn diagnosis](activation-churn-diagnosis.md) taxonomy; a cluster under one code is a candidate signal for the next back-test, not a reason to override the score by feel.

Read the false-alarm share as a cost. A score that captures nearly all churn by flagging most accounts has moved the triage problem rather than solved it.

Never show the score to the customer, and never make it a customer success manager's target. A score that decides someone's bonus gets managed through the inputs people can type into.

## ILLUSTRATIVE example

Invented. Fieldmark is a fictional inspection-checklist product sold to property management firms on annual contracts. All figures are ILLUSTRATIVE.

**One account, scored.** Corbel Lettings, a fictional customer with 40 paid seats. Weights: H1 seat activation 0.30, H2 core-action trend 0.25, H3 support friction 0.15, H4 sponsor engaged 0.15, H5 sentiment 0.15, total 1.00.

| Signal | Raw value | Normalisation | Score | Weight | Weighted |
|---|---|---|---|---|---|
| H1 seat activation | 25 of 40 = 0.625 | linear, floor 0.2, target 0.8: 100 x (0.625 minus 0.2) / 0.6 | 71 | 0.30 | 21.3 |
| H2 core-action trend | 3.4 inspections per seat per week against 4.0 before = 0.85 | linear, floor 0.5, target 1.1: 100 x 0.35 / 0.6 | 58 | 0.25 | 14.5 |
| H3 support friction | 2 tickets at severity S2 in 60 days | inverse, ceiling 4, best 0: 100 x (4 minus 2) / 4 | 50 | 0.15 | 7.5 |
| H4 sponsor engaged | no contact in 90 days | binary | 0 | 0.15 | 0 |
| H5 sentiment | recommend answers 9, 7, 4: mean 6.67 | mean x 10, at least 3 responses | 67 | 0.15 | 10.05 |
| Health | | | | 1.00 | 53.35, amber |

Had Corbel's sentiment signal been missing, the available weight would be 0.85, above the 0.70 floor, and Health = (21.3 + 14.5 + 7.5 + 0) / 0.85 = 43.3 / 0.85 = 50.9, still amber.

**Back-test.** 240 accounts had a renewal date in the last four quarters; each was scored as of 90 days before that date.

| Band | Accounts | Renewed | Churned | Renewal rate | Share of all churned |
|---|---|---|---|---|---|
| Green | 130 | 121 | 9 | 93.1% | 20.5% |
| Amber | 74 | 58 | 16 | 78.4% | 36.4% |
| Red | 36 | 17 | 19 | 47.2% | 43.2% |
| Total | 240 | 196 | 44 | 81.7% | 100% |

Capture = (16 + 19) / 44 = 79.5 percent, against a target of 70 percent the renewals owner set beforehand. Red precision = 19 / 36 = 52.8 percent. False-alarm share = (58 + 17) / 196 = 38.3 percent. The best single signal, seat activation, flagging the same 110 lowest accounts, captured 28 of 44, 63.6 percent. With 44 churned accounts, a falling renewal rate across the bands, capture above target and a composite that beats the single signal, the score is validated for Fieldmark's annual-contract accounts. Of the nine green accounts that churned, six were coded V8 organisational change (an acquisition or a departed champion), so "named champion still in role" goes into the next back-test as a candidate H6.

**NPS and CSAT for the same quarter.** 120 recommend responses: 54 promoters (45 percent), 42 passives, 24 detractors (20 percent). NPS = 45 minus 20 = 25. Margin = 100 x 1.96 x the square root of ((0.45 + 0.20 minus 0.25 squared) / 120) = 100 x 1.96 x the square root of (0.5875 / 120) = 13.7 points, so the honest statement is 25, plus or minus 13.7, from 120 responses. The previous quarter's 31 from 110 responses is inside that margin, and the quarterly update reports no change rather than a fall. After-ticket CSAT: 336 of 410 responses were 4 or 5, CSAT 82.0 percent, at a response rate of 410 of 2,280 closed tickets, 18.0 percent. [OPEN: whether the 1,870 closed tickets with no response differ from those that answered; owner, support operations lead.]

## The trap

The score trusted because it looks reasonable. Four sensible signals, round-number weights, a red-amber-green column on the account list, and nobody ever computed what the score would have said 90 days before last year's renewals. The tell: no back-test table exists, or the dashboard shows bands and no capture figure. The quieter version is a back-test that passes because it read the future: capture near 100 percent usually means the inputs included usage that collapsed after the customer had already given notice, or a sentiment field someone updated after the churn. Freeze every input as of the lead date, and distrust a back-test that looks better than the customer success team's own memory.

## Feeds

- [Customer success handoff](../../templates/operate/customer-success-handoff.md), section 3, which names the signals a launch moves, and section 4, which lists renewal-risk accounts by band
- [Metrics review](../../templates/operate/metrics-review.md), section 2, where the share of accounts in red and the Falling count are read, and section 3, where NPS and CSAT sit as guardrails with their response counts
- [Metrics dictionary](../../templates/operate/metrics-dictionary.md): one row per signal, plus NPS and CSAT exactly as Step 6 defines them
- [Dashboard spec](../../templates/operate/dashboard-spec.md): the health tile states whether the score is validated and the date of its last back-test
- [Activation and churn diagnosis](activation-churn-diagnosis.md), which supplies the activation event as a candidate signal and the codes used to read the score's misses
- [HEART metrics](heart-metrics.md), whose happiness category may use CSAT as defined here, never NPS as a usability stand-in
- The [analyst agent](../../agents/analyst-agent.md) runs the back-test; the [metrics-tree skill](../../skills/metrics-tree/SKILL.md) writes the signal definitions
- OPERATE stage, reviewed at [Gate 6: outcomes verified](../../os/STAGE-GATES.md)
- Method background: [UX measurement](../../knowledge/design/ux-measurement.md) for what NPS is and is not; otherwise the [knowledge index](../../knowledge/INDEX.md)
