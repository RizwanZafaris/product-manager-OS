# Kano Survey: Expense Copilot, seven candidate attributes

Fills [frameworks/discovery/kano-survey.md](../frameworks/discovery/kano-survey.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the copilot is the fictional product used across this repository, the respondents do not exist, and every count and coefficient is ILLUSTRATIVE, built to show the tabulation and the decision rule rather than to suggest what a real survey would find. It ran during DEFINE, between the discovery GO and the PRD, and its output is the scope table in the [PRD](expense-copilot-prd.md). Method: Kano and colleagues (1984), in this repository's own words; background in the [Kano card](../knowledge/kano-model.md). See the [examples index](README.md).

**Owner:** the PM · **Fielded:** 2026-08-18 to 2026-08-22 · **Respondents:** 41 filers who submitted at least one report last quarter, recruited from the finance mailing list

## 1. The question pair

Each attribute is asked as present and as absent, with the same five answers: I like it, I expect it, I am neutral, I can live with it, I dislike it. The pair for attribute 1, as fielded:

- Functional: "If the app pre-filled merchant, date, amount and currency from a photo of the receipt, how would you feel?"
- Dysfunctional: "If the app did not pre-fill those fields and you typed them as you do today, how would you feel?"

The two answers are looked up in the table. Classes: must-be (M), one-dimensional (O), attractive (A), indifferent (I), reverse (R), questionable (Q).

| Functional, down; dysfunctional, across | Like | Expect | Neutral | Live with | Dislike |
|---|---|---|---|---|---|
| Like | Q | A | A | A | O |
| Expect | R | I | I | I | M |
| Neutral | R | I | I | I | M |
| Live with | R | I | I | I | M |
| Dislike | R | R | R | R | Q |

## 2. Tabulation

The class is the modal column, with one rule: if the leader's margin over the runner-up is under a tenth of n (under 5 here), the tie breaks in the order M, O, A, I, because missing a must-be costs more than over-building an attractive one. Coefficients follow Berger and colleagues (1993): CS+ = (A + O) / (A + O + M + I), the satisfaction gained if present; CS- = (O + M) / (A + O + M + I), the dissatisfaction if absent, reported as a negative.

| # | Attribute | A | O | M | I | R | Q | Class | CS+ | CS- |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Fields pre-filled from a receipt photo | 9 | 24 | 5 | 2 | 0 | 1 | O | 0.83 | -0.73 |
| 2 | Policy line shown beside the suggested category | 20 | 10 | 3 | 7 | 0 | 1 | A | 0.75 | -0.33 |
| 3 | Confidence flags shown to the filer | 11 | 6 | 2 | 19 | 2 | 1 | I | 0.45 | -0.21 |
| 4 | Auto-submit without a review step | 4 | 3 | 1 | 8 | 23 | 2 | R | 0.44 | -0.25 |
| 5 | Multi-receipt capture in one photo | 15 | 12 | 4 | 8 | 0 | 2 | O, by tie-break | 0.69 | -0.41 |
| 6 | Mileage suggested from the calendar | 13 | 2 | 0 | 21 | 3 | 2 | I | 0.42 | -0.06 |
| 7 | Reminder nudges before month end | 3 | 2 | 1 | 24 | 9 | 2 | I | 0.17 | -0.10 |

Row 1, shown once: A + O + M + I = 9 + 24 + 5 + 2 = 40, with R and Q left out. CS+ = (9 + 24) / 40 = 0.83. CS- = (24 + 5) / 40 = 0.73, written as -0.73. Row 5 is the tie-break in action: A leads O by 3, under the margin of 5, so the order M, O, A, I makes it one-dimensional. Row 4's coefficients rest on the 16 respondents left after the 23 reverse and 2 questionable answers come out of the 41, which is why they look mild; the class is the finding.

## 3. Decisions

| Class | Rule | Applied here |
|---|---|---|
| M | In scope first; invest to "reliably present", no further | None found, which is suspicious this early; see Open |
| O | Compete on it; more is better | Row 1 is v1 scope. Row 5 stayed deferred at Gate 2 for an eval reason; the class says what the deferral costs, not whether the team can ship it |
| A | A small bets budget | Row 2. Cheap, so it went into v1 as the one delighter |
| I | Cut, or ship only if free | Rows 3, 6, 7. Flags go to the reviewer view instead, where the reviewer interviews asked for them; mileage and nudges leave v1 |
| R | Do not build, or make it opt-in | Row 4 backs the PRD's out-of-scope line: no auto-submission, ever |
| Q | Rewrite the question | No attribute reached 3 questionable answers; the wording held |

Row 6 splits by segment: eleven respondents claimed mileage last quarter and nine of them answered attractive. Overall it is indifferent because most filers never drive, so it is a note against the mileage row in the [RICE sheet](ledgerline-rice-scoring.md), not a v1 line. Row 7's nine reverse answers are why a nudge, if ever built, is opt-in.

## 4. What the survey cannot say

It was fielded before anyone had used a draft. Classes drift, and the card's warning lands on row 2: a policy line beside the category is a delighter today and a basic the week after every filer has seen it. The post-launch review re-runs the pair on rows 1, 2, and 5 with respondents who have used the product.

## Open

- [OPEN: no must-be surfaced, which usually means the survey listed only new things. The basics filers already have (the form saves a draft, the total adds up) were not asked. The PM owns adding three existing attributes to the next round, to check that the floor holds.]
- [OPEN: the 41 are self-selected from a mailing list, and frequent travelers answered at a higher rate than the one-trip-a-quarter filer named in discovery. The research lead owns a weighted re-cut before any class is quoted outside the team.]
- [OPEN: no finance reviewer was surveyed, so the reviewer-facing version of row 3 rests on four interviews, not a classification. The PM owns a reviewer pair if the reviewer view grows beyond flags.]

## Feeds

- [templates/definition/prd.md](../templates/definition/prd.md): the functional scope table (rows 1 and 2, and the reviewer-side flags) and the out-of-scope list (row 4).
- [templates/planning/roadmap.md](../templates/planning/roadmap.md): the O and A rows that did not fit v1, with their class as the argument.
- Gate 2 (requirements signed off) in [os/STAGE-GATES.md](../os/STAGE-GATES.md).
- Method: [knowledge/kano-model.md](../knowledge/kano-model.md), and the blank worksheet at `frameworks/discovery/kano-survey.md`.
