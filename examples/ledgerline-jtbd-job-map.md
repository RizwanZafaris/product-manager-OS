# JTBD Job Map: getting reimbursed without a bounce

Fills [frameworks/discovery/jtbd-job-map.md](../frameworks/discovery/jtbd-job-map.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the twelve interviews are the fictional ones the [discovery document](expense-copilot-discovery.md) reports, the people are roles, and every score and count is ILLUSTRATIVE, there to show what a map with evidence behind it looks like and not to describe any real expense process. The method is Tony Ulwick's eight-step job map and Bob Moesta's four forces, both in this repository's own words; background in the [JTBD card](../knowledge/jobs-to-be-done.md). See the [examples index](README.md).

**Owner:** the PM · **Date:** 2026-08-05 · **Sessions:** eight filers (F01 to F08) and four finance reviewers (R01 to R04), 2026-07-20 to 2026-08-01 · **Performer mapped:** the filer

## 1. Job statement

**Job:** get money spent on a trip reimbursed or cleared, correctly, the first time, without it coming back to me. No form, no copilot, no finance team in the sentence. The reviewer's job (approve reports I can defend at audit) is a different job and gets its own map; see Open.

## 2. Job map

Struggle: 0 none observed, 1 annoyance, 2 a workaround that costs time or money, 3 the step fails or the job is abandoned. Sessions are the filer interviews that raised the step unprompted.

| Step | What the filer does today | Where it goes wrong | Struggle | Sessions | Evidence |
|---|---|---|---|---|---|
| Define | Decides what is claimable and whether to file now or at month end | Nobody has read the policy; they guess or ask a colleague | 2 | 6 | F01, F02, F04, F05, F07, F08 |
| Locate | Gathers paper receipts, emailed receipts, card statement lines | Lost receipts; hunting email for the hotel folio | 2 | 5 | F01, F03, F04, F06, F08 |
| Prepare | Photographs or scans receipts, sorts them by date | One slip at a time is tedious | 1 | 3 | F02, F03, F06 |
| Confirm | Checks amounts, converts currency, picks a category | The category is a guess and a wrong one bounces the report; currency by hand | 3 | 7 | F01 to F05, F07, F08 |
| Execute | Types each line into the form | Re-typing what the receipt already says; some keep a spreadsheet to paste from | 2 | 8 | F01 to F08; R02 and R03 named it too |
| Monitor | Waits; checks the status page; asks finance in chat | No visibility until a bounce arrives days later | 1 | 4 | F02, F05, F06, F07 |
| Modify | Fixes the bounced report and resubmits, sometimes twice | The reason is one cryptic line; the fix is a guess | 2 | 5 | F01, F04, F05, F07, F08; all four reviewers from their side |
| Conclude | Reimbursement lands; reconciles against a personal card | Timing uncertain; some carry the cost for weeks | 1 | 2 | F03, F06 |

**Decision rule applied:** struggle times sessions. Confirm 3 x 7 = 21, Execute 2 x 8 = 16, Define 2 x 6 = 12, Locate 2 x 5 = 10, Modify 2 x 5 = 10, Monitor 1 x 4 = 4, Prepare 1 x 3 = 3, Conclude 1 x 2 = 2. Confirm and Execute are where v1 spends its scope: the category suggestion with its policy line serves Confirm, extraction serves Execute, and the metric that proves it is first-submission approval, which is the Confirm step not failing. Define is next and is served by the same policy line shown at the moment of deciding. Modify and Monitor are the case for the pre-submit check that leads the [RICE sheet](ledgerline-rice-scoring.md). Conclude is a lead with two sessions, not a result.

## 3. Four forces

The switch under study: from typing the report on the last evening of the month to letting the copilot draft it and reviewing the draft. Strength: 0 absent, 1 mentioned, 2 volunteered with a specific incident, 3 the participant acted on it. Entries are paraphrases.

| Force | What we heard | Strength | Evidence |
|---|---|---|---|
| Push of the current struggle | An evening lost and the report still comes back; three filers have stopped claiming small receipts rather than face the form again | 3 | F01, F04, F05, F07, F08 |
| Pull of the new way | If it read the receipt they would file on the train home; one sitting, with the category rule visible | 2 | F02, F03, F05, F06 |
| Anxiety about the new | If it gets a number wrong it is still their name on the report; two asked who else would see their receipts | 2 | F01, F03, F04, F06, F08 |
| Habit of the old | A spreadsheet and a month-end batch; the form is known and the workaround is comfortable | 2 | F02, F04, F07, F08 |

**Decision rule applied:** switch side = 3 + 2 = 5; stay side = 2 + 2 = 4. The margin is one point, under the two the rule demands, so adding pull will not move adoption. The work is reducing anxiety and breaking habit, which is what the PRD does: the filer stays the author, nothing is submitted without review, low-confidence fields are visible, and the draft flow has to beat the spreadsheet on the first try or the month-end batchers will not try twice. This is also why the [business case](ledgerline-business-case.md) treats adoption as its swing variable rather than assuming it.

## 4. Reading it

The map is lopsided, which is the sign of evidence rather than averaging. The previous "better form" request would have spent the budget on Execute alone; the map says Confirm fails harder, and that a form cannot fix a guess. The forces say the launch story is trust and reversibility, not automation.

## Open

- [OPEN: the reviewer's job has not been mapped. R01 to R04 were coded for pains, not steps. The PM owns re-coding them before any reviewer-facing backlog item is scored.]
- [OPEN: no session covered an executive assistant filing for someone else, so the Locate and Execute rows are wrong for that performer by construction. Two interviews are owed; the research agent owns them.]
- [OPEN: importance and satisfaction scores per step do not exist. The research lead owns deciding whether the opportunity-scoring survey runs before or after launch.]

## Feeds

- [templates/discovery/jtbd-spec.md](../templates/discovery/jtbd-spec.md): section 1 and section 3 lift straight from this map.
- [templates/discovery/discovery-document.md](../templates/discovery/discovery-document.md): the pain and hypothesis sections, taken to Gate 1 in the [discovery example](expense-copilot-discovery.md).
- Gate 1 (problem worth solving) in [os/STAGE-GATES.md](../os/STAGE-GATES.md).
- Method: [knowledge/jobs-to-be-done.md](../knowledge/jobs-to-be-done.md), and the blank worksheet at `frameworks/discovery/jtbd-job-map.md`.
