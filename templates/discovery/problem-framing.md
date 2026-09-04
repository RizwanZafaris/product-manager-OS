---
layer: templates
stage: DISCOVER
gate: 1
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Problem Framing", "problem-framing"]
---
# Problem Framing: [problem short name]

Stage: DISCOVER, feeds Gate 1 (problem worth solving)
Knowledge: [Knowledge index, SCR entry](../../knowledge/INDEX.md)
Skill: [persona-builder](../../skills/persona-builder/SKILL.md)

<!-- One problem, one page, one owner. The discovery document records the whole
     exploration; this file distills it into a single statement a sponsor can fund
     or kill in one reading.

     The structure follows the situation-complication-resolution pattern
     associated with Barbara Minto's work on structured writing, encoded here in
     this repo's own words: establish the stable situation, name what broke it,
     and only then propose what to do about it.

     One problem per file. If you find yourself writing "and also", split the file. -->

**Owner:** [name, the single person accountable for this problem being solved or retired]
**Date:** [YYYY-MM-DD] · **Status:** Draft / Framed / Funded / Retired

## 1. Situation

<!-- What is true today, stated so someone who works elsewhere could picture
     it. Situation and complication are separated because teams routinely
     write the complication and call it the situation. -->


[Two or three sentences of stable context that everyone already agrees on. No news here; this is the shared ground the reader stands on.]

## 2. Complication

<!-- What changed, or what makes the situation no longer acceptable. If the
     complication is that leadership asked, say so plainly rather than
     inventing a user-facing one. -->


[What changed or was discovered that makes the situation untenable. This is the news. One or two sentences.]

## 3. Problem statement

> [User or segment] needs a way to [outcome they seek] because [driver], but today [obstacle], which costs them [consequence, quantified where possible].

<!-- One sentence. No solution words allowed: if the statement contains "app",
     "dashboard", "AI", or a feature name, it is a solution in disguise. Reframe
     around the outcome the user cannot reach. -->

## 4. Evidence

| # | Evidence item | Type (interview / ticket / metric / observation) | Source or ID | Strength (strong / weak) |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

<!-- Mark strength honestly. A metric from your own warehouse is strong. A
     secondhand quote from one sales call is weak. Weak evidence is allowed at
     this stage; unlabeled weak evidence is not. -->

## 5. Cost of inaction

- **To the user:** [what they lose per week or month if nothing changes]
- **To the business:** [revenue, cost, risk, or trust impact; a number or a named owner who will produce the number by a date]
- **Trajectory:** [is this getting worse, stable, or fading on its own? Say how you know]

<!-- "Fading on its own" is a legitimate finding. Some problems retire themselves,
     and framing that honestly saves a quarter of work. -->

## 6. Who feels it and how often

<!-- Frequency and reach, with a number. This decides whether the problem is
     worth a quarter, and it is the section most often left qualitative
     because the number is uncomfortable. -->


| Segment | How many | Frequency of the pain | Severity (blocks work / slows work / annoys) |
|---|---|---|---|
| | | | |

## 7. Constraints on any resolution

[Known boundaries a solution must respect: budget ceiling, platform, regulatory regime, team capacity, deadline. If a financial or data regulator applies to the product, note it here and raise it again at Gate 2. The regulated overlay itself activates only when the product also contains an AI or machine-learning feature; see ../../os/STAGE-GATES.md for the rule and for what a regulated product with no model brings instead.]

## 8. Decision requested

- **Ask:** [fund discovery / fund definition / retire the problem]
- **From:** [sponsor name] · **By:** [date]

---

### Worked micro-example (illustrative, invented)

> **Situation:** Finance closes the books monthly, and expense reports feed the close.
> **Complication:** Failed receipt submissions tripled in March, and the close slipped four days.
> **Problem statement:** Field sales reps need a way to submit expenses that are accepted on the first pass because they file from phones in poor light, but today half of receipt photos fail validation after submission, which costs each rep about an hour a week and delays the monthly close.
> **Cost of inaction:** Close slips compound quarterly; the controller owns producing the cost figure by April 15.

---

## How this framing fails

<!-- The first row is the one that costs quarters. A solution written as a
     problem passes every later gate, because every later document takes the
     problem as given. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| A solution in disguise | "Users cannot find the documentation" names the fix in the phrasing | State what someone is trying to do and what stops them, naming no product and no feature |
| Too broad to disagree with | "Communication is hard", which rejects nothing and directs nothing | If nobody could argue with it, it is an observation rather than a problem |
| Nobody is shown to have it | A memorable anecdote, and no interview, ticket or log behind it | Cite one observed case before the document is written, or mark the framing an assumption |
| Never sized | "This happens a lot", with no count and no cost | A number: how often, to how many, costing what. Rough and sourced beats precise and invented |
| The person is not named | "Users" and "stakeholders" throughout | One role, one job they are trying to get done, one situation where it fails |

## Exit gate

<!-- Checkable by someone who did not write this document, which is the
     test of whether a gate is a gate. -->
 (feeds Gate 1: problem worth solving)

- [ ] Exactly one problem in this file
- [ ] Problem statement contains no solution words
- [ ] Every evidence row has a source ID and a strength label
- [ ] Cost of inaction carries a number or a named owner and date for the number
- [ ] A single accountable owner is named
- [ ] The decision requested names the sponsor and a date
