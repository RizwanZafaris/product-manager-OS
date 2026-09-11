# HEART Metrics: PantryPath quick reorder

Fills [frameworks/metrics/heart-metrics.md](../frameworks/metrics/heart-metrics.md). Everything here is ILLUSTRATIVE: Cedar & Finch is a fictional company, PantryPath is a fictional wholesale ordering product, and Maya Ortiz, Leo Bennett, and Priya Shah are fictional people. Every figure is ILLUSTRATIVE, internally consistent, and included to show the worksheet method rather than to suggest a real benchmark.

**Owner:** Maya Ortiz, product manager · **Reviewed with:** Leo Bennett, product analyst, and Priya Shah, research lead · **Date:** 2026-08-22

**ILLUSTRATIVE context:** Cedar & Finch sells office supplies through PantryPath. The fictional feature is Quick Reorder, which lets a buyer review a previous basket, change quantities, and submit a new order. The team is defining the feature before implementation. Maya owns the metric definitions, Leo owns the event data, and Priya owns the post-order attitude question.

## What it is for

This worksheet chooses user-experience metrics for Quick Reorder from the user's goal first, then observable signals, then metrics. The selected categories are happiness, adoption, and task success.

The user's goal is: "I can repeat a regular order without checking every line again or fixing mistakes afterwards."

Happiness is measured by asking buyers whether they trust the reordered basket. Adoption measures new use of Quick Reorder. Task success measures whether the buyer submits the intended order without correction. Engagement and retention do not apply to this feature at this stage.

The method is HEART, based on the ideas of Kerry Rodden, Hilary Hutchinson, and Xin Fu at Google, from the paper "Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications" (CHI, 2010). This worksheet uses the method in this repository's own words.

## Run it when

- A feature's success criterion could otherwise become "usage"
- The team needs a before-and-after measure before writing the analytics instrumentation spec
- A launch could increase activity while making the user's task slower or less trustworthy
- A product change needs an attitude measure as well as behavioural measures

**Skip it when:** the feature has no human in the loop. A nightly ordering reconciliation job needs an operational SLO and belongs in the observability work instead.

For Quick Reorder, the worksheet runs before implementation so the event names, survey question, and baseline window can be confirmed before launch.

## Inputs you need first

- The user's goal in their words: "I can repeat a regular order without checking every line again or fixing mistakes afterwards."
- The event taxonomy for `quick_reorder_started`, `quick_reorder_submitted`, `quick_reorder_corrected`, and `quick_reorder_abandoned`
- The attitude question owned by the feedback program: "After using Quick Reorder, how much do you agree with this statement: I trust that the reordered basket contains what I intended to buy?" Answers are on a 1 to 5 scale.
- A baseline window before the feature ships, from 2026-07-01 to 2026-07-31
- The eligible population definition: buyers who submitted at least one PantryPath order during the baseline window and have a prior basket that can be repeated

## The worksheet

### Step 1: goals, signals, metrics

The team selected three categories. Each metric has a numerator, denominator, and period.

| Category | Goal (what the user achieves) | Signal (observable behaviour or stated attitude) | Metric (numerator / denominator, period) | Source | Owner | Applies? (yes or no, why) |
|---|---|---|---|---|---|---|
| Happiness | "I trust the reordered basket." | Buyers rate their trust in the reordered basket at 4 or 5 out of 5 after submitting it | Post-submission ratings of 4 or 5 / all valid post-submission ratings, monthly. Baseline arithmetic: 24 / 40 = 60% | Quick Reorder post-submission survey | Priya Shah | Yes, trust is an attitude and must be measured by asking |
| Engagement | The buyer completes a repeat order with less effort, rather than spending more time in the feature | Time and repeated edits are task costs, not evidence of value | Not selected. More sessions or more clicks would not show that Quick Reorder helped | Product events and task timing | Maya Ortiz | No, more use is not the goal for a utility feature |
| Adoption | A buyer who is eligible for a repeat order tries Quick Reorder for the first time | Eligible buyers submit their first Quick Reorder order during the month | Buyers with a first Quick Reorder submission / eligible buyers with a repeatable basket, monthly. Baseline arithmetic: 120 / 300 = 40% | Ordering database and Quick Reorder submission event | Leo Bennett | Yes, the team needs to know whether the feature reaches the intended buyers |
| Retention | Buyers continue to use Quick Reorder for later orders | Existing Quick Reorder adopters use it again in a later period | Not selected. The initial definition focuses on first use and task quality; a later cohort review may add retention | Product events | Maya Ortiz | No, retention is not needed to decide whether the first task works |
| Task success | The buyer submits the intended repeat order without correcting the basket afterwards | A submitted Quick Reorder order has no correction event and is not abandoned | Quick Reorder submissions with no correction event / Quick Reorder starts, monthly. Baseline arithmetic: 210 / 300 = 70% | Quick Reorder events and order records | Leo Bennett | Yes, this is the feature's core effectiveness measure; an error is a correction event or abandonment before submission |

The task-success denominator is starts rather than submissions because abandonment is part of the failure definition. A correction is any quantity, product, or basket change after the initial Quick Reorder submission and before the order is fulfilled.

### Step 2: definition card per chosen metric

| Metric | Formula | Included | Excluded | Period | Segments to cut | Baseline (date) | Target (date) | Guardrail it needs |
|---|---|---|---|---|---|---|---|---|
| Quick Reorder trust | Valid post-submission ratings of 4 or 5 / all valid post-submission ratings | Buyers who submit Quick Reorder and answer the trust question within the same month; valid answers are 1 to 5 | Blank answers, duplicate responses from the same submission, and responses outside the submission month | Monthly | Buyer size, buyer tenure, basket size, and new order versus repeat order | 24 / 40 = 60%, 2026-07-01 to 2026-07-31 | 32 / 40 = 80%, 2026-08-01 to 2026-08-31 | Quick Reorder task success, because trust can rise if the question is shown only to easy orders |
| First Quick Reorder adoption | Buyers with a first Quick Reorder submission in the month / eligible buyers with a repeatable basket in the month | Buyers who have not previously submitted with Quick Reorder and submit at least one Quick Reorder order during the period | Buyers without a repeatable prior basket, internal test accounts, and buyers whose first submission is cancelled by the system | Monthly | Buyer size, buyer tenure, basket size, and ordering frequency | 120 / 300 = 40%, 2026-07-01 to 2026-07-31 | 180 / 300 = 60%, 2026-08-01 to 2026-08-31 | Task success, because adoption can rise when the feature attracts buyers who cannot complete the task |
| Quick Reorder task success | Quick Reorder starts that produce a submission with no correction event / all Quick Reorder starts | A start followed by a submitted order and no correction event before fulfilment | Abandoned starts, system test events, duplicate starts within one minute, and orders cancelled by the system rather than the buyer | Monthly | Buyer size, basket size, product category, and whether the basket contains substitutions | 210 / 300 = 70%, 2026-07-01 to 2026-07-31 | 255 / 300 = 85%, 2026-08-01 to 2026-08-31 | Trust rating, because task success can rise while buyers feel less confident or less in control |

## Reading the result

Read the three selected measures together:

- Adoption rising from 120 / 300 = 40% to 180 / 300 = 60% while task success stays at 210 / 300 = 70% would mean more buyers are trying Quick Reorder without evidence that the task is working better.
- Task success rising from 210 / 300 = 70% to 255 / 300 = 85% while trust stays at 24 / 40 = 60% would mean the flow may be faster or more effective while still making buyers uneasy. Priya should review the verbatims before the result is treated as a win.
- Trust rising from 24 / 40 = 60% to 32 / 40 = 80% while adoption remains at 120 / 300 = 40% would mean the experience is credible for the buyers who try it, but the team has not yet reached enough eligible buyers.
- Adoption and task success use different denominators. Adoption is 120 / 300 at baseline, while task success is 210 / 300. The shared denominator size is illustrative only, and the definitions must remain distinct in the metrics dictionary.
- The target arithmetic is explicit: adoption requires 180 first adopters out of 300 eligible buyers, task success requires 255 successful starts out of 300 starts, and trust requires 32 high ratings out of 40 valid responses.

The baseline window is 2026-07-01 to 2026-07-31. If that window is not confirmed as comparable to the launch month, the target comparison is not valid. The analytics instrumentation spec must preserve the event distinctions between a start, a submission, a correction, and an abandonment.

## ILLUSTRATIVE example

Cedar & Finch's Quick Reorder feature uses three HEART categories.

| Category | Goal | Signal | Metric | Baseline |
|---|---|---|---|---|
| Happiness | "I trust the reordered basket." | Buyers rate trust at 4 or 5 out of 5 after submitting | High post-submission ratings / valid post-submission ratings, monthly | 24 / 40 = 60% |
| Engagement | Does not apply: Quick Reorder should reduce effort, not create more activity | Repeated sessions and clicks are treated as possible friction | Not selected | Not applicable |
| Adoption | Eligible buyers try Quick Reorder for the first time | A first Quick Reorder submission occurs during the month | First Quick Reorder submissions / eligible buyers with a repeatable basket, monthly | 120 / 300 = 40% |
| Retention | Does not apply to this first-pass definition | Later repeat use is not yet needed to assess the initial task | Not selected | Not applicable |
| Task success | The buyer submits the intended repeat order without correction | A Quick Reorder start ends in a submission with no correction event | Successful Quick Reorder starts / all Quick Reorder starts, monthly | 210 / 300 = 70% |

Definition card for Quick Reorder task success: Quick Reorder starts that produce a submitted order with no correction event / all Quick Reorder starts, monthly. Baseline arithmetic: 210 / 300 = 70% for 2026-07-01 to 2026-07-31. The target arithmetic is 255 / 300 = 85% for 2026-08-01 to 2026-08-31. It excludes abandoned starts, system test events, duplicate starts within one minute, and system-cancelled orders. It is cut by buyer size, basket size, product category, and whether the basket contains substitutions. Its guardrail is the trust rating, because a successful submission can still feel unsafe to the buyer.

## The trap

The trap is choosing engagement because the dashboard already has session counts. If the team celebrated Quick Reorder sessions, buyers could appear highly engaged because they repeatedly opened the flow to repair quantities or replace unavailable products. That would reward friction.

The goal must come first: the buyer wants to repeat an order with less checking and fewer corrections. Adoption answers whether eligible buyers try the feature. Task success answers whether the task ends correctly. Happiness answers whether the buyer trusts the result. None of those questions is answered by a session count.

A second trap is treating a submission as success. A buyer can submit an order and then correct it because the basket was wrong. The task-success metric therefore uses a start denominator and names correction and abandonment as errors.

## Feeds

- [PRD](../templates/definition/prd.md), section 6, success metrics and instrumentation
- [Analytics instrumentation spec](../templates/delivery/analytics-instrumentation-spec.md), section 1, the events and metrics this worksheet serves
- [Metrics dictionary](../templates/operate/metrics-dictionary.md), one row for each definition card
- [Feedback program](../templates/operate/feedback-program.md), which owns the trust question and response handling
- [HEART Metrics blank worksheet](../frameworks/metrics/heart-metrics.md)
- Method background: [knowledge/INDEX.md](../knowledge/INDEX.md)
