# Opportunity Solution Tree: [outcome short name]

Stage: DISCOVER, feeds Gate 1 (problem worth solving)
Knowledge: [Continuous discovery](../../knowledge/torres-continuous-discovery.md)
Skill: manual

<!-- The structural tool of Teresa Torres's continuous discovery practice, built
     here as tables instead of a diagram so it can be diffed, cited, and kept
     honest. One outcome at the root; opportunities are needs, pains, and desires
     heard from customers, in the customer's words; solutions hang under targeted
     opportunities; assumption tests hang under solutions. The tree turns "what
     should we build?" into "which assumption do we test this week?"

     The trap the knowledge card names is the kickoff tree: built in a workshop,
     admired, never touched again. A stale tree is worse than none, because it
     wears the costume of evidence. The "last fed by" field below is the alarm:
     if you cannot name the branch that changed after last week's touchpoints,
     you have a picture of a practice, not a practice. -->

**Owner:** [name] · **Started:** [YYYY-MM-DD] · **Last fed by:** [session ID, YYYY-MM-DD]
**Trio:** [PM] · [design] · [engineering]

## 1. Outcome

**Outcome:** [one metric move: metric, from X to Y, by date]
**Traces to:** [the input metric in [north-star-metric.md](../planning/north-star-metric.md) or the key result in [okrs.md](../planning/okrs.md), named]
**Why this outcome now:** [one sentence]

## 2. Opportunity branches

<!-- Phrase each branch as the customer said it ("I never know if the payment
     went through"), never as a solution in disguise ("users need a status
     page"). Every branch cites [evidence note](evidence-note.md) IDs. A branch
     with no citation is a guess; either cut it or mark it assumption and put an
     interview slot against it. Sub-opportunities point at their parent. -->

| ID | Opportunity, in the customer's words | Parent | Evidence (note IDs) | Heard how often | Targeted now? |
|---|---|---|---|---|---|
| O1 | | root | | [n of m sessions] | yes / no |
| O2 | | | | | |

**Target selection:** [which one or two branches are targeted this cycle, and why they beat the siblings: frequency, severity, fit with the outcome]

## 3. Solutions per targeted opportunity

<!-- Minimum two per targeted opportunity, compared against each other. One
     candidate is allowed only when labeled a single-solution bet with the
     reason stated; unlabeled single solutions are how the most recent idea
     wins by default. -->

| ID | Solution sketch (one sentence) | Opportunity | Comparison status |
|---|---|---|---|
| S1 | | O1 | compared against S2 / single-solution bet because [reason] |
| S2 | | O1 | |

## 4. Assumptions per solution

<!-- "For this to work, it must be true that..." Tag each desirability,
     viability, or feasibility; add usability or ethical where they apply.
     Rank by risk-if-wrong so the tests below chase the killers first. -->

| ID | Assumption | Solution | Type | Risk if wrong (H/M/L) | Evidence today |
|---|---|---|---|---|---|
| A1 | | S1 | desirability / viability / feasibility | | [note IDs or "none"] |

## 5. Assumption tests

<!-- Smallest test that could kill the assumption: an interview prompt, a fake
     door, a spike, a data pull. Days, not sprints. Route anything that grows
     into a real experiment to [experiment-brief](../operate/experiment-brief.md). -->

| Assumption | Smallest test design | Pass / kill signal | Status | Result |
|---|---|---|---|---|
| A1 | | | planned / running / done | |

**This week's test:** [the one test running now, its owner, and the session or data slot it uses]

---

### Worked micro-example (illustrative, invented)

> **Outcome:** raise week-4 repeat usage of expense filing from the OKR key result.
> O1 "I batch receipts until they pile up" (INT-002, INT-009, 6 of 8 sessions), targeted.
> S1 capture-at-purchase prompt vs S2 weekly digest reminder, compared.
> A1 (desirability, high risk): users will act on a prompt within a day of purchase.
> This week's test: fake prompt in the follow-up interviews, kill signal is fewer than 3 of 5 saying they would act on it. Result feeds the O1 branch either way.

---

## Exit gate (feeds Gate 1: problem worth solving)

- [ ] One outcome, traced to a named north star input metric or key result
- [ ] Every opportunity branch cites at least one evidence note ID, or is marked assumption with an interview slot against it
- [ ] Targeted opportunities were selected by comparison, and the losing branches show why
- [ ] Every targeted opportunity carries at least two compared solutions, or a labeled single-solution bet
- [ ] Every solution's riskiest assumption has a test designed, and at least one test is live this week
- [ ] "Last fed by" is within two weeks; a staler tree re-earns its branches before it feeds a gate
