---
layer: frameworks
stage: DEFINE
gate: 2
feeds: ["templates/definition/prd.md", "templates/planning/roadmap.md", "templates/discovery/survey-design.md"]
method: "knowledge/kano-model.md"
aliases: ["Kano survey", "kano-survey"]
---
# Kano survey

Based on the ideas of Noriaki Kano, Nobuhiko Seraku, Fumio Takahashi, and Shinichi Tsuji, from the paper Attractive Quality and Must-Be Quality (1984). Explained here in this repository's own words.

## What it is for

A Kano survey asks two questions per attribute, how would you feel if it were present and how would you feel if it were absent, and uses the pair of answers to classify the attribute: must-be, one-dimensional, attractive, indifferent, reverse, or questionable. The classes have different satisfaction curves, so they deserve different budgets: cover every must-be to the reliably-present bar, compete on chosen one-dimensional attributes, hold a small bet budget for the attractive ones, cut the indifferent ones. The survey replaces the argument in which every stakeholder's favorite requirement is critical with a tabulation of what job performers said. It improves the scope decision at Gate 2 and the sequencing decision on the roadmap.

## Run it when

- A PRD's functional scope has more candidate attributes than the release can hold.
- A stakeholder insists every requirement is critical and the roadmap needs a tie-breaker in the customer's voice.
- Before a packaging decision, to learn which attributes can fence a tier.

**Skip it when:** a basic is visibly broken. The survey will tell you what the support queue already says, and the week is better spent fixing it.

## Inputs you need first

- Five to fifteen attributes, each phrased as a capability the respondent can picture inside a scenario, not a feature name.
- A respondent sample of job performers, screened on behavior, with a minimum n per segment decided in the [survey design](../../templates/discovery/survey-design.md) before fielding.
- The segments you will tabulate separately: filer against approver, frequent against occasional.

## The worksheet

### 1. The question pair

For each attribute, ask both:

| Question | Answer options |
|---|---|
| Functional: "If [attribute] were present, how would you feel?" | I like it / I expect it / I am neutral / I can tolerate it / I dislike it |
| Dysfunctional: "If [attribute] were absent, how would you feel?" | The same five options |

### 2. Classification table

<!-- Rows are the functional answer; columns are the dysfunctional answer.
     A = attractive, O = one-dimensional, M = must-be, I = indifferent, R = reverse,
     Q = questionable (a contradictory pair: the respondent misread, or the attribute is unclear). -->

| Functional answer, down; dysfunctional answer, across | Like | Expect | Neutral | Tolerate | Dislike |
|---|---|---|---|---|---|
| Like | Q | A | A | A | O |
| Expect | R | I | I | I | M |
| Neutral | R | I | I | I | M |
| Tolerate | R | I | I | I | M |
| Dislike | R | R | R | R | Q |

### 3. Tabulation

<!-- One row per attribute per segment. Class = the category with the most respondents. -->

| Attribute | Segment | n | A | O | M | I | R | Q | Class | Margin (top minus second) |
|---|---|---|---|---|---|---|---|---|---|---|
| K1 | | | | | | | | | | |

**Decision rule:** the class is the mode. When the top two categories fall within a margin you set before fielding (three respondents is a workable convention on a sample of a few dozen), apply the tie-break order M, then O, then A, then I, which favors the class whose absence hurts most. Q above a share you set beforehand (one respondent in ten is a workable convention) means the attribute was unclear: rewrite and re-ask. R concentrated in one segment means the attribute must be optional for that segment, not removed.

### 4. Action per class

| Class | What it earns |
|---|---|
| Must-be | In scope before anything else, built to reliably present, no investment past that |
| One-dimensional | Compete here; size by importance; the roadmap's performance line |
| Attractive | A small budget, sized as a bet; the differentiation line |
| Indifferent | Cut, or ship only if it is free |
| Reverse | Segment it or make it optional |
| Questionable | Rewrite the question |

## Reading the result

The tabulation is a scope map. Every M goes into the PRD's functional scope for the first release, whatever the team's enthusiasm for the As. The Os get ranked with [opportunity scoring](opportunity-scoring.md) if you asked importance as well. An attribute that reads A for filers and M for approvers is two attributes with one name; split it. Reclassify on a cadence, because attractive decays into must-be and a competitor's delighter becomes your missing basic.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. 36 respondents, filers and approvers mixed for this table, then split.

| Attribute | A | O | M | I | R | Q | Class | Note |
|---|---|---|---|---|---|---|---|---|
| K1 Card charges matched to receipts automatically | 6 | 19 | 8 | 3 | 0 | 0 | O | clear |
| K2 Policy check before submit | 5 | 9 | 17 | 4 | 0 | 1 | M | clear |
| K3 Mileage computed from the calendar | 15 | 6 | 2 | 12 | 1 | 0 | A | margin 3; tie-break order confirms A |
| K4 Copilot drafts the business-purpose text | 9 | 4 | 1 | 13 | 8 | 1 | I | R sits with approvers: audit worry |
| K5 Reimbursement status notification | 7 | 12 | 11 | 6 | 0 | 0 | M | margin 1; tie-break M over O |

Decision: K2 and K5 are the floor of release one; K1 is the competitive line; K3 is the one bet; K4 is cut for filers and revisited as an approver-controlled option.

## The trap

Everything comes back attractive. When attributes are phrased as your feature names ("Smart Match"), respondents answer like on the functional side and neutral on the dysfunctional side for all of them, because nobody can miss what they have never had, and the survey certifies a roadmap of delighters with no floor. Phrase each attribute as a capability inside a concrete scenario the respondent has lived through, and include two attributes you already know are must-be as calibration rows; if those do not come back M, the instrument is broken, not the customers.

## Feeds

- [PRD](../../templates/definition/prd.md): section 4 (functional scope), must-be rows first
- [Roadmap](../../templates/planning/roadmap.md): Now for must-be, Next for one-dimensional, Later for the attractive bets
- [Survey design](../../templates/discovery/survey-design.md): the question bank and the sample plan
- DEFINE, feeding [Gate 2: requirements signed off](../../os/STAGE-GATES.md); the tabulation itself is Gate 1 evidence
- Worked fill: [Ledgerline Kano survey example](../../examples/ledgerline-kano-survey.md)
- Method background: [Kano model](../../knowledge/kano-model.md)
