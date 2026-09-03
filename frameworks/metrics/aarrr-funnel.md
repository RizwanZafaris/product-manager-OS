# AARRR Funnel

Based on the ideas of Dave McClure, from the talk "Startup Metrics for Pirates" (2007). Explained here in this repository's own words.

## What it is for

Five stages, acquisition, activation, retention, referral, revenue, each marked by one event, with conversion measured between neighbours. The question it answers is not "how are we growing" but "where exactly does growth leak". The decision it improves is where the next experiment goes. A funnel forces the team to define activation as a moment of value rather than a page view, and it exposes the common failure of buying more acquisition to feed a funnel that loses most people two steps later.

## Run it when

- The growth plan needs a mechanism and "more marketing" is the only proposal on the table
- Sign-ups rise and revenue does not, and nobody can say which step is eating the difference
- Before a launch, to decide which events the instrumentation spec must carry
- A metrics review shows an input falling and the team cannot locate the step

**Skip it when:** every customer is closed by sales and onboarded by hand. A five-stage funnel over six enterprise deals is a table of anecdotes; run the [win-loss review](../../templates/operate/win-loss-review.md) instead.

## Inputs you need first

- The event taxonomy from the [analytics instrumentation spec](../../templates/delivery/analytics-instrumentation-spec.md), section 2
- A definition of the first moment of value, from discovery evidence or the [north star input tree](north-star-input-tree.md)
- Acquisition channel and customer segment per user, because a blended funnel hides two different funnels
- A time window long enough for the slowest stage to complete

## The worksheet

### Step 1: define the stages

One event per stage. The window says how long after the previous stage a user may still count.

| Stage | Meaning in this product | The one event that marks it | Window after the previous stage | Source |
|---|---|---|---|---|
| Acquisition | A person arrives with a trackable identity | [event] | | |
| Activation | The first moment of value; an action, never a view | [event] | | |
| Retention | The core action repeated in the next period | [event] | | |
| Referral | Another user arrives because of this one (invite sent and accepted) | [event] | | |
| Revenue | Payment, or expansion of an existing account | [event] | | |

### Step 2: measure the transitions, cut by channel and segment

| Transition | Channel or segment | Entered | Converted | Conversion (%) | Same figure last period | Change |
|---|---|---|---|---|---|---|
| Acquisition to activation | | | | | | |
| Activation to retention | | | | | | |
| Retention to referral | | | | | | |
| Retention to revenue | | | | | | |

Compare only against your own prior periods. No industry figure enters this table.

### Step 3: rank the leaks

The leak is not the lowest percentage. Weight each transition's loss by what the lost people would have been worth downstream:

leak weight = (entered minus converted) x (product of the conversion rates for every later transition) x (value per revenue-stage user)

A small loss near the bottom, where survivors are valuable, can outrank a large loss at the top.

| Transition | People lost | Downstream conversion product | Leak weight | Rank |
|---|---|---|---|---|
| | | | | |

### Step 4: one fix per leak

| Leak (rank) | Why it leaks (from evidence, not a guess) | Evidence | The one fix | Expected change in conversion | Experiment brief |
|---|---|---|---|---|---|
| | | | | | |

Rule: one fix per leak, biggest weight first. Five fixes in flight teach nothing because none can be attributed.

## Reading the result

Fix the deepest leak before buying acquisition; a funnel multiplies whatever enters it, including waste. Acquisition to activation is where most young products leak; activation to retention is where products with a sales team leak, because the sale carried people past a value moment they never had. A high activation rate paired with weak retention usually means activation was defined too early: rename the event, do not celebrate the rate. Referral near zero is normal for back-office software; it is an absence, not a leak, and a referral program will not fix it. Always report counts beside rates: a conversion that rose because the denominator shrank is not an improvement.

## ILLUSTRATIVE example

Invented figures for Ledgerline's expense-report copilot, measured per employee inside deployed customer accounts over one quarter. Revenue is accounted at the account level and kept out of the per-employee funnel.

| Transition | Entered | Converted | Conversion |
|---|---|---|---|
| Acquisition (opened the copilot from the invite) to activation (first report drafted with a matched receipt and submitted) | 5,200 | 2,340 | 45% |
| Activation to retention (second report within 60 days) | 2,340 | 1,570 | 67% |
| Retention to referral (the employee's manager enabled the copilot for the whole team) | 1,570 | 190 | 12% |

Leak weights: acquisition to activation loses 2,860 people, each with a 0.67 chance of retaining, so 1,916 retained users lost; activation to retention loses 770 directly. Activation ranks first. Cut by channel, the invite-email cohort activated at 39% and the in-app-banner cohort at 58%, so the fix targets the email path. Evidence: 61% of non-activated email-cohort users abandoned at the "connect your mailbox" step. The one fix: allow photo upload of receipts before any mailbox connection, hypothesis of 45% to 52% activation, written up as an experiment brief with the mailbox-connect rate as the guardrail.

## The trap

The average funnel. One blended set of rates across paid and organic, self-serve and sales-assisted, and the "leak" the team finds is an average of two funnels that leak in different places; the fix helps neither. In the example above the blended 45% hid a 39% path and a 58% path, and a fix aimed at the average would have been aimed at nobody. Cut by channel and segment before naming a leak, and treat a cell with fewer than a few hundred people as a rumour.

## Feeds

- [Growth plan](../../templates/planning/growth-plan.md), section 3 (the mechanism and where it leaks) and section 4 (the cheapest experiment)
- [Experiment brief](../../templates/operate/experiment-brief.md), one per fix
- [Analytics instrumentation spec](../../templates/delivery/analytics-instrumentation-spec.md), section 1, for the five stage events
- [GTM plan](../../templates/planning/gtm-plan.md), section 4, the one metric that says the launch worked
- The [growth agent](../../agents/growth-agent.md) and [analyst agent](../../agents/analyst-agent.md) read this sheet; the [metrics-tree skill](../../skills/metrics-tree/SKILL.md) fills it
- OPERATE stage, reviewed at [Gate 6: outcomes verified](../../os/STAGE-GATES.md)
- Method background: [AARRR entry in the knowledge index](../../knowledge/INDEX.md)
