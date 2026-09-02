---
name: experiment-designer
description: Turn an assumption or a growth bet into an experiment brief with a mechanism-stated hypothesis, one primary metric, guardrails with floors, an exposure design, a sample size reasoned from the minimum detectable effect, and stop rules written before launch. Use when a growth plan bet needs a test, when an assumption register row is low confidence and high impact, when a price change should be tried on a slice first, or when someone says "let us just A/B it". Takes the assumption, the metric candidate with its baseline, the eligible traffic, and the guardrail candidates; returns the test card, the filled brief, the sizing record with its calculator inputs, and the pre-committed decision rule.
---

# Experiment Designer: a test that can fail, sized before it runs

Experiments fail before they start. The hypothesis has a direction and no mechanism, the metric is chosen after the data arrives, the sample size is a guess, someone peeks on day three, and a "win" ships that quietly hurt retention. This skill writes the decision rule while everyone is still ignorant of the result, and sizes the test from the effect that would change the decision rather than the effect the team hopes for.

## Files this skill drives

- [../../templates/operate/experiment-brief.md](../../templates/operate/experiment-brief.md), every section
- [../../frameworks/discovery/assumption-mapping.md](../../frameworks/discovery/assumption-mapping.md), the test card before and the learning card after (Bland and Osterwalder, Testing Business Ideas, 2019)
- [../../templates/definition/assumptions-register.md](../../templates/definition/assumptions-register.md), the row under test, moved to TESTING
- [../../templates/planning/growth-plan.md](../../templates/planning/growth-plan.md), the bet it serves and the ledger row it ends in
- [../../templates/planning/north-star-metric.md](../../templates/planning/north-star-metric.md), the tree link and the guardrails
- [../../templates/delivery/analytics-instrumentation-spec.md](../../templates/delivery/analytics-instrumentation-spec.md), the events the metric is computed from
- [../../templates/operate/metrics-review.md](../../templates/operate/metrics-review.md) and [../../templates/execution/decision-log.md](../../templates/execution/decision-log.md), where the result and the decision land
- Method background: the Lean Startup entry in [../../knowledge/INDEX.md](../../knowledge/INDEX.md) (Ries, 2011); for a feature with a model inside, [../../templates/ai/eval-spec.md](../../templates/ai/eval-spec.md) still applies and this brief does not replace it
- [../../agents/growth-agent.md](../../agents/growth-agent.md) hands ranked experiments here

## When to use

- The growth plan's next bet needs a test design
- An assumption register row is low confidence, high impact, and testable by exposing a slice of users
- A price or packaging change can be tried on new customers before it reaches everyone
- A feature could roll out to everyone, but a phased exposure would tell you whether it works
- Anyone proposes an A/B test without a written decision rule

## Inputs

The assumption or bet, by register ID or growth plan section. The target metric candidate, its tree link, and its baseline with a date and a source system. The eligible population or traffic per period, from the analytics platform. Guardrail candidates: the north star sheet's guardrails, support volume, latency, error rate, revenue per account. What can actually be built as a variant. The calculator the team uses for sample size: the analytics platform's built-in one or a standard sample size calculator, named in the brief.

Ask for what is missing, and ask one question first: what decision changes if the result is positive, and what changes if it is negative. If the answer is "nothing either way", there is no experiment to design.

## Workflow

### 1. Map the assumption and write the test card

Place the belief on the importance-versus-evidence grid from the assumption mapping worksheet. Test the important, unevidenced belief; skip beliefs with strong evidence and beliefs that do not matter. Write the test card: we believe, to verify we will, we will measure, we are right if. Reserve the learning card for the end. Choose the cheapest test that could prove the belief false; a full A/B test is not always it, and a fake door, a concierge run, or a pilot cohort may answer first.

### 2. State the hypothesis with its mechanism

"We believe [change] will move [metric] because [the reason a customer behaves differently]." One target metric, tied to the north star tree, with a dated baseline from the source system. A hypothesis without a "because" cannot be examined in the retro, so it is returned.

### 3. Name every metric that is allowed to decide

Primary: exactly one. Guardrails: what must not degrade, each with a floor and a stop behavior. Diagnostic metrics: labeled as such, useful for explaining the result and forbidden from deciding it. Decision rule: a metric not named before launch cannot decide the outcome, however interesting it looks afterwards.

### 4. Design the exposure

Unit of assignment: user, account, or session, chosen to match where the effect lives and to avoid contamination; in a product sold to teams, assign by account, because two colleagues in different variants talk. Allocation, eligibility, and ramp. Run across whole cycles of the behavior's natural period, so a weekly behavior is read over whole weeks. Decide how a novelty effect will be told apart from a lift: a longer read, a holdout, or a returning-user cut. Check that variants cannot interfere through shared inventory, queues, or notifications.

### 5. Reason about the minimum detectable effect, then use a calculator

The minimum detectable effect is the smallest lift that would change the decision, derived from the decision rule, the cost of building and maintaining the change, and the metric's place in the tree. It is not the lift you expect. The reasoning is qualitative on purpose. The smaller the effect you need to detect, the larger the sample per variant, and the growth is steep, not linear. A rare baseline event needs more sample than a common one; a noisy continuous metric needs more than a clean rate; every extra variant divides the traffic. Duration is sample per variant, times variants, divided by eligible traffic per period. Put the inputs into the named calculator (baseline, minimum detectable effect, the significance and power settings the team has agreed as its standard, the number of variants) and record every input beside the result. Decision rule: if the duration exceeds an honest ceiling, choose among a larger minimum detectable effect (only big wins will be detected; say so), broader exposure, a more sensitive proxy metric higher in the funnel, or not running the test. Never shrink the sample to fit the calendar.

### 6. Write the stop rules and the decision rule

Three outcomes, pre-committed with owners: ship, iterate, kill. The read happens at the planned end, or under a sequential method declared before launch; an early look on a Tuesday is peeking, and peeking turns noise into a decision. The only early stop is a guardrail breach. Kill ends in a written learning card, a ledger row, a metrics review entry, and a decision log entry; the register row moves to VALIDATED or BUSTED.

## Output format

1. Test card: we believe, to verify we will, we will measure, we are right if
2. Experiment brief sections 1 to 5, filled
3. Sizing record: | Input | Value | Source |, covering baseline (source system, date), minimum detectable effect with its one-line reasoning, significance and power settings as used, variants, sample per variant (from the named calculator), eligible traffic per period (source), duration
4. Stop rules: | Trigger | Who checks | When | Action |
5. The learning card, blank until the read, and the entries to write on the read

## Failure modes this skill guards against

- A hypothesis with a direction and no mechanism
- The primary metric chosen after the data arrives
- The minimum detectable effect set to the lift someone hopes for
- A sample size guessed, or "run it until it looks done"
- Peeking, and stopping on the first good day
- No guardrail, so a win that raised churn ships
- Assigning by user in a product where accounts talk to each other
- A novelty bump read as a lift
- More variants than the traffic can carry
- A test whose result changes no decision
- A kill outcome buried without a learning card

## Exit gate

The brief feeds Gate 6 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md) through the metrics review. Do not report it done until the brief's exit gate passes, the sizing record shows every calculator input with its source, the stop rules name who checks and when, and all three decision outcomes have owners.
