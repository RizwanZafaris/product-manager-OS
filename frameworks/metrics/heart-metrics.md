# HEART Metrics

Based on the ideas of Kerry Rodden, Hilary Hutchinson, and Xin Fu at Google, from the paper "Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications" (CHI, 2010). Explained here in this repository's own words.

## What it is for

A way to choose user-experience metrics that match a goal, instead of adopting whatever the dashboard already shows. Five categories: happiness (attitude, measured by asking), engagement (voluntary frequency and depth of use), adoption (new users of the thing in a period), retention (existing users still using it a period later), task success (effectiveness, efficiency, error rate). For each category that applies, you write the goal first, then the signals that would show the goal is met, then the metrics that quantify the signals. The order is the method. Teams that start from metrics end up with goals reverse-engineered to fit a chart.

## Run it when

- Writing section 6 of a PRD and the success metric so far is "usage"
- A launch is "successful" by activity while support tickets and survey verbatims say otherwise
- Deciding what to instrument, before the analytics spec is written
- A redesign needs a before-and-after measure that is not a page-view count

**Skip it when:** the feature has no human in the loop. A nightly reconciliation job has no happiness or engagement; its task success is an SLO, and it belongs in the observability template.

## Inputs you need first

- The user's goal in their words, from the [JTBD spec](../../templates/discovery/jtbd-spec.md) or PRD section 3
- The event taxonomy in the [analytics instrumentation spec](../../templates/delivery/analytics-instrumentation-spec.md)
- An attitude instrument, from the [feedback program](../../templates/operate/feedback-program.md); happiness cannot be inferred from clicks
- A baseline window before the change ships

## The worksheet

### Step 1: goals, signals, metrics

Pick two or three categories for a feature, up to five for a product. A metric needs a numerator, a denominator, and a period; missing any one, it is a mood.

| Category | Goal (what the user achieves) | Signal (observable behaviour or stated attitude) | Metric (numerator / denominator, period) | Source | Owner | Applies? (yes or no, why) |
|---|---|---|---|---|---|---|
| Happiness | | | | | | |
| Engagement | | | | | | |
| Adoption | | | | | | |
| Retention | | | | | | |
| Task success | | | | | | |

Rules: happiness comes from an attitude measure (survey, rating), never from behaviour. Task success names the task's end state and its error definition. Engagement is a goal only when more use means more value; for a tool meant to disappear, more use is a cost. A category with a goal and no observable signal gets a research task, not an invented metric.

### Step 2: definition card per chosen metric

This card is what the metrics dictionary stores.

| Metric | Formula | Included | Excluded | Period | Segments to cut | Baseline (date) | Target (date) | Guardrail it needs |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## Reading the result

Read the categories against each other. Adoption up and retention flat is curiosity, not value. Task success up and happiness down means the task got faster and more annoying; read the verbatims before celebrating. Engagement up on a utility product may mean the product got harder. Retention that holds while happiness falls is usually a mandate: people who must use the tool are not people who like it, and the day the mandate lifts the retention goes with it. A metric with no baseline cannot show a change, so a launch that ships before step 2 is filled has no success criterion, whatever the PRD says.

## ILLUSTRATIVE example

Invented figures for Ledgerline's expense-report copilot, for the receipt auto-match feature.

| Category | Goal | Signal | Metric | Baseline |
|---|---|---|---|---|
| Happiness | "I trust the draft" | Submitters rate draft accuracy after submitting | Share of post-submission ratings at 4 or 5 of 5, monthly | 58% |
| Engagement | Does not apply: a report tool should take less of the user's time, not more; time per report sits under task success | | | |
| Adoption | New employees use the copilot for their first report | First report of the month drafted via copilot rather than the manual form | Copilot first reports / all first reports, monthly | 41% |
| Retention | They keep using it | Second and third reports also via copilot | Month-1 copilot adopters still using it in month 3 / month-1 adopters | 71% |
| Task success | Report approved without rework | Submitted report approved first time; lines edited after submission | First-submission approval rate, monthly; edited lines per report | 62%; 1.8 |

Definition card for first-submission approval rate: approved with zero manager or accounts-payable edits / submitted, monthly; excludes reports withdrawn by the submitter within a day; cut by department and by copilot versus manual; guardrail: post-approval corrections found by accounts payable, because a rate can rise when managers stop reading.

## The trap

Engagement on a tool that should be invisible. The copilot team celebrated daily active use because sessions were already on the dashboard, then discovered from the verbatims that people were opening the copilot several times per report to fix categorizations it kept getting wrong. The category was chosen for the chart it could produce, and the goal was written afterwards to match. The order in step 1 exists to prevent exactly this; if a goal cannot be written before the metric, the metric is decoration.

## Feeds

- [PRD](../../templates/definition/prd.md), section 6, success metrics and instrumentation
- [Analytics instrumentation spec](../../templates/delivery/analytics-instrumentation-spec.md), section 1, the metrics the spec serves
- [Metrics dictionary](../../templates/operate/metrics-dictionary.md) (one row per definition card) and [dashboard spec](../../templates/operate/dashboard-spec.md), both driven by the [metrics-tree skill](../../skills/metrics-tree/SKILL.md)
- [Feedback program](../../templates/operate/feedback-program.md), which owns the happiness instrument
- DEFINE, checked at [Gate 2: requirements signed off](../../os/STAGE-GATES.md), and OPERATE at Gate 6
- Method background: [HEART entry in the knowledge index](../../knowledge/INDEX.md)
