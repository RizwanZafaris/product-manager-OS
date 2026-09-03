# RICE Scoring Sheet: Expense Copilot, post-launch backlog

Fills [frameworks/prioritization/rice-scoring-sheet.md](../frameworks/prioritization/rice-scoring-sheet.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the expense copilot is the fictional product used across this repository, the people are roles rather than names, and every figure is ILLUSTRATIVE, chosen to show the arithmetic and not to be copied as a target or quoted as a benchmark. The backlog is the one that formed once the [PRD](expense-copilot-prd.md) passed Gate 2 with three deliberate deferrals. See the [examples index](README.md).

**Owner:** the PM · **Scored with:** the engineering lead (effort), the finance lead (reach data) · **Date:** 2026-09-01

## Step 1: reach unit and the metric

| Field | Value |
|---|---|
| Reach unit | Expense reports per quarter. Base: 2,400 in the quarter ending 2026-06-30, finance system of record |
| Period | One quarter (Q4) |
| Metric impact is scored against | KR 1, first-submission approval rate on drafted reports (PRD objective 1) |
| Capacity | 9 person-months stated; the ranked list may fill 80 percent, 7.2, after the mandate lane takes its share |
| Scored by, on | the PM, the engineering lead, the finance lead, 2026-09-01 |

## Step 2: the scales, as used

Impact 3, 2, 1, 0.5, 0.25 against KR 1 and nothing else. Confidence 1.0 only for a result measured on Ledgerline's own reports; 0.8 for evidence with a written reason it transfers (the bounce-reason data, interview counts); 0.5 for opinion. Effort in whole person-months from the engineering lead, top of the range.

## Step 3: the scores

| # | Item | Type | Reach | Impact | Conf. | Effort | Arithmetic | RICE | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Pre-submit policy check: warn the filer about the top bounce causes | feature | 2,400 | 2 | 0.8 | 2 | 2,400 x 2 x 0.8 / 2 | 1,920 | bounce-reason data, Q2; all reports |
| 2 | Category mapping feedback loop, corrections fed back after a review step | enabler | 1,400 | 2 | 0.8 | 2 | 1,400 x 2 x 0.8 / 2 | 1,120 | reports carrying a suggestion; mismatch is the top bounce reason |
| 3 | Corporate-card feed matching | feature | 1,600 | 2 | 0.5 | 4 | 1,600 x 2 x 0.5 / 4 | 400 | reports with a card line; impact is opinion |
| 4 | Per-diem rules applied to drafts | feature | 480 | 1 | 0.8 | 1.5 | 480 x 1 x 0.8 / 1.5 | 256 | reports with a per-diem line; second bounce reason |
| 5 | Reviewer batch-approve for all-high-confidence reports | feature | 1,000 | 0.25 | 0.8 | 1 | 1,000 x 0.25 x 0.8 / 1 | 200 | saves reviewer time, moves KR 1 barely |
| 6 | Multi-receipt capture in one photo | feature | 900 | 1 | 0.5 | 3 | 900 x 1 x 0.5 / 3 | 150 | reports with three or more receipts; deferred at Gate 2 |
| 7 | Foreign-language receipt extraction | feature | 260 | 2 | 0.5 | 2 | 260 x 2 x 0.5 / 2 | 130 | foreign-currency lines as a proxy; see Open |
| 8 | Mileage capture | feature | 350 | 0.5 | 0.5 | 1 | 350 x 0.5 x 0.5 / 1 | 87.5 | reports with a mileage line; Kano indifferent overall |
| 9 | Filing on behalf of another person | discovery | 180 | 1 | 0.5 | 2 | 180 x 1 x 0.5 / 2 | 45 | assistant-filed reports; zero interviews |

Row 5 scores 0.25 on purpose. Batch approval saves reviewer hours and moves first-submission approval not at all; its case belongs in the [business case](ledgerline-business-case.md), and a sheet declared on a reviewer-hours KR would rank it near the top. Every 0.5 is an opinion and is labeled as one.

## Step 4: mandate lane, outside the ranking

| Mandate | Source | Hard date | Cost of missing it | Effort | Quarter pinned |
|---|---|---|---|---|---|
| Receipt image retention and deletion schedule | Compliance impact assessment signed at Gate 2 | 2026-11-30 | Receipts held past the retention period; a finding at the next audit | 1 | Q4 |
| Vendor clause forbidding training on Ledgerline data | Model vendor contract review | Before Gate 5 | Launch blocked; the PRD carries it as a gap | Legal time, not engineering | Q4 |

## ICE, for the intake pile

| Item | Impact | Confidence | Ease | ICE | Keep for RICE? |
|---|---|---|---|---|---|
| Personal forwarding address for emailed receipts | 6 | 8 | 9 | 432 | No: an afternoon, goes into sprint slack |
| Show last quarter's category for a repeat merchant | 5 | 6 | 8 | 240 | No: same |
| Reminder nudge three days before month end | 3 | 4 | 9 | 108 | No: Kano classed it indifferent with a reverse minority; dropped |

## Reading the result

Scores are buckets. Rows within about 20 percent of each other tie, and any row at 0.5 confidence gets a discovery task, not a build slot, however high it scores.

- **Top bucket, rows 1 and 2.** Both go to the roadmap; 4 person-months of the 6.2 available after the mandate. Row 1 first, because it needs no review step and row 2 does.
- **Middle bucket, rows 3 to 7.** Row 3 leads it but sits at opinion-level confidence with a four-month effort, so it gets a two-week count of how many bounced reports actually carry a card transaction. Row 4, at 0.8, takes 1.5 of the remaining 2.2 person-months. Rows 5 to 7 wait; row 6 was also deferred at Gate 2 for an eval reason (the receipt set could not hold a threshold on overlapping receipts), and the [Kano survey](ledgerline-kano-survey.md) classed it one-dimensional. A middling score overrules neither fact; it says KR 1 is not the argument for it.
- **Bottom bucket, rows 8 and 9.** Not this quarter. Row 9 is scored on zero interviews with its own user, so even 0.5 is generous.

The row 4 over row 3 call, with the count as the condition to reopen it, goes to the decision log.

## Open

- [OPEN: row 9 is scored on no interviews with an executive assistant. Two are owed before it is scored again; the research agent owns the interviews, the PM owns the re-score.]
- [OPEN: reach for row 7 counts foreign-currency lines, a proxy. The real unit is receipts in a language the extractor has not been evaluated on, and nobody has counted those. The engineering lead owns the count.]

## Feeds

- [templates/planning/roadmap.md](../templates/planning/roadmap.md): the top bucket fills Now; row 4 and the row 3 discovery task fill Next, each with its precondition.
- [templates/execution/decision-log.md](../templates/execution/decision-log.md): the tie-break and the row 3 deferral, with the options that lost.
- Method: [knowledge/rice-prioritization.md](../knowledge/rice-prioritization.md), and the blank worksheet at `frameworks/prioritization/rice-scoring-sheet.md`.
