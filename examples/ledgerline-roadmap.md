# Roadmap: Expense Copilot

Fills [templates/planning/roadmap.md](../templates/planning/roadmap.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the Expense Copilot add-on is the fictional product used across this repository, the people are roles filled by invented names, and every count, dollar figure and date is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) and its supplement, the [coverage sheet](ledgerline-coverage-sheet.md), so it can be checked against the documents this roadmap feeds. See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Last updated:** 2027-01-14 · **Review cadence:** monthly
**Linked OKR sheet:** [ledgerline-okrs.md](ledgerline-okrs.md) (cycle 2026-11-02 to 2026-12-31, scored 2026-12-21 on data to 2026-12-18, N69; the next cycle's objectives are set after EXP-2 resolves)

## Preamble: read this before the tables

> **This roadmap manages expectations, not delivery dates.** Only Now is a commitment, and it is a commitment to the work, not to a date. It says what we are working on now, what we expect to pick up next, and the directions we are holding open for later. It is not a delivery contract and no date on it is a promise.
>
> **Now** is committed and in flight. Confidence is high, and if something here slips you will hear it from us before you notice it yourself.
>
> **Next** is shaped and planned, not started. The order can change when evidence changes. Treat anything here as likely, not scheduled.
>
> **Later** is a set of directions, not features. Anything in Later may never ship, and the entries are deliberately imprecise: a specific feature name written a year out becomes a commitment nobody made.
>
> Things move backward as well as forward, and items get killed. The parked-and-killed table below is part of the roadmap, not an appendix to it. If a decision here affects something you are counting on, ask, and you will get the real answer rather than the reassuring one.

## Now (committed, in flight or next up)

| Theme | Initiative | Outcome it serves (objective ref) | Target period | Confidence | Dependencies | Status |
|---|---|---|---|---|---|---|
| Packaging pivot to usage billing | BL-01, the drafted-report meter (LEDGERLINE-S6, ADR-008): count drafts per account and bill in arrears | Serves the pivot D6 recorded on 2026-12-21; unblocks EXP-2, which carries KR1 (accounts with the add-on active, target 180, actual 79 at 2026-12-18, N70) and KR4 (add-on MRR, target $30,000, actual $15,906, N73); the next cycle's objective is set after EXP-2 resolves | January 2027 (needed by 2027-01-08, DEP4, N87) | 90% (LC45) | DEP4 (billing with Priya Nair, needed by 2027-01-08, open) | In progress |
| Re-offer at the usage price | EXP-2, exposure of the $2.40-per-drafted-report offer to about 2,818 to 2,821 S-1 accounts not paying (N91), single arm, success bar 6.0% or better reaching paid status within 14 days (M-007), kill under 4.0% at the analysis date or on 2027-02-12, whichever comes first (N92) | Same as above: EXP-2 is the test that decides whether the add-on earns a place in any revenue plan (D11 keeps it out of FY2027 until EXP-2 resolves, coverage sheet) | January to February 2027 (exposure 2027-01-11 to 2027-02-12, N91) | 80% (LC45) | DEP4 must land by 2027-01-08 (row above); R7, margin floor breach risk if M-009 moves (coverage sheet) | Not started |
| Billing-instrument gap | BL-03, legacy annual-invoice accounts emit no activation event (G-1, N82, 214 accounts, 3 activated through manual invoice lines in the window) | Feeds M-002 accuracy (active add-on accounts, N64), the input metric behind KR1 | February 2027 | 75% (LC45) | Kwame Boateng owns the fix; no external dependency | Not started |

## Next (planned, shaped, not yet committed)

| Theme | Initiative | Outcome it serves | Target period | Confidence | Dependencies | Status |
|---|---|---|---|---|---|---|
| Instrumentation debt | BL-04, classic-approvals events carry no draft id (G-2, about 11% of S-1 excluded from M-006) | Makes M-006 (first-submission approval on drafted reports, KR2, N71) measurable across all eligible accounts | Q1 2027 | 60% (LC45) | Kwame Boateng; platform approvals team | Shaped |
| Filer experience | BL-05 slice, warn the filer pre-submit on the single top bounce cause only (from support tickets, N38, 610 tagged category or receipt in Q3) | Attacks the bounce rate directly, feeding KR2's target of 78% (actual 76%, N71) | Q1 2027 | 55% (LC45) | None beyond capacity; WSJF split ranks it above BL-07 (LC43) | Shaping |
| Migration path | BL-07, a way to move the 73 held accounts (N93) to a successor price at term end without breaking the 12-month promise (N48) | Protects M-011 (add-on MRR, KR4, N73) during and after the pivot; R8 opened 2026-12-22 | Q1 2027 | 50% (LC45) | Decision memo owed by Isabel Ferreira, due 2027-10-01 (LC33); depends on EXP-2 outcome | Shaping |
| Rollout | Phase 3 rollout of whichever price ships after EXP-2 | Expansion of M-002 (KR1) beyond the current 79 active accounts (N64) toward the 180 target (N70) | Q2 2027 | 50% (LC45) | Entry condition: EXP-2 at 6.0% or better (N91); Halvard Marine and Ostrander Group quotes stay withdrawn until EXP-2 resolves (D10, coverage sheet) | Shaped |

## Later (directional themes only)

| Theme | Problem it addresses | Earliest it could enter Next | Signal that would promote it |
|---|---|---|---|
| Language coverage for extraction | German-language receipts fail the eval threshold (EVAL-3 at 71% field accuracy against 90%, N83, LC20; realised at Wrenfield Labs, N45; G-3 undercounts M-004) | Q2 2027 | EVAL-3 re-scored at 90% or better (LC45 promotion signal); D9 still open, owner Priya Nair with Maya Chen |
| Multi-receipt capture | Filers photograph one receipt at a time (BL-08, raised by Marcus Webb 2026-11-06, candidate) | Q3 2027 | Demand signal from support or win-loss beyond BL-08's current rank; no capacity allocated |
| Enterprise re-engagement | Two Enterprise prospects (Halvard Marine, Ostrander Group, about 400 seats each, about $2,400 MRR each at the seat price, N79) are blocked on packaging, not on the DPA (closed by D5, 2026-12-03) | Q2 2027 | EXP-2 ships at 6.0% or better (N91); D10 holds both quotes withdrawn until then |

## Parked and killed

| Initiative | Parked or Killed | Reason | Date |
|---|---|---|---|
| BL-06, admins see billed seats against filers before activating (LEDGERLINE-S4) | Parked | Superseded by BL-01 and LEDGERLINE-S6 if the usage price ships; parked to 2027-02-12 pending EXP-2 (LC40, LC45) | 2026-12-23 |
| BL-09, revise the anchored offer copy | Killed | Both arms sat under the kill line (EXP-1 control 2.4%, anchored 2.9%, N61); iterating copy does not fix a value-metric mismatch (D6) | 2026-12-21 |
| BL-10, a ten-report free allowance | Killed | The accounts that most need the product are exactly the accounts that would exhaust it (D2, rejected at pricing review) | 2026-11-03 |

## Change log

| Date | Change | Why | Who decided |
|---|---|---|---|
| 2026-12-21 | Phase 3 rollout moved from Next to held; per-seat price removed from all planning rows | D6: EXP-1 killed the per-seat price (both arms under 4.0%, N61); phase 3 entry condition unmet | Isabel Ferreira, on the metrics review |
| 2026-12-22 | BL-01 (usage meter) and EXP-2 added to Now; German-language extraction moved to Later; BL-06 parked | D7: growth plan queued EXP-2 as the next bet; DEP4 blocks EXP-2; LC45 set the horizon structure | Maya Chen with Isabel Ferreira |
| 2026-12-23 | BL-09 killed; BL-06 parked to 2027-02-12; backlog triaged with WSJF ranking | Backlog health check (LC41); median age 14.5 days, oldest BL-08 at 47 days; two dead items with ids spent | Maya Chen |
| 2027-01-14 | This roadmap published; D11 recorded: add-on kept out of the FY2027 revenue plan until EXP-2 resolves, on or before 2027-02-12 | Board meeting; the add-on has no proven conversion rate at a customer scale, and EXP-2's result is open on purpose (coverage sheet rule) | The board, on Isabel Ferreira's recommendation |

## How this roadmap fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Dates read as promises | A month appears next to an item, and a customer is told it | Say in the legend that these are targets. Outward-facing versions use Now, Next, Later with no dates |
| Features with no outcome | Rows of things to build, none tied to an objective or a metric | Every row names the outcome it serves. A row that cannot is a task, not an initiative |
| Later is a graveyard | Half the items sit in Later permanently and nobody revisits them | Items in Later expire after two cycles and are re-justified or killed |
| Nothing moves | The same items sit in Now for months while work happens elsewhere | Anything in Now for more than two cycles is flagged: kill it, or re-commit with a new target period and a change-log row |
| Killed work vanishes | An item disappears and three months later somebody asks what happened to it | Killed items move to the parked and killed table with one line of reason |
| Confidence set once | The confidence column was filled at planning and never touched again | Confidence is re-entered every cycle. A carried-over value is not a confidence |

## Exit gate

This roadmap is fit to share when:

- [x] Every Now and Next initiative names the objective it serves, and that objective exists in the OKR sheet. Each row cites KR1, KR2, KR4 or the M-id chain from the [OKR sheet](ledgerline-okrs.md); the next cycle's objective is set after EXP-2 resolves, which is stated in the Now rows rather than left implicit
- [x] Confidence is stated per row, and nothing under 70% sits in Now. Now rows: 90%, 80%, 75%. Next rows: 60%, 55%, 50%, 50%. No Next row under 70% is in Now
- [x] Later contains themes, not dated features. Three rows, each a direction with a promotion signal, no feature name precise enough to quote back
- [x] Dependencies are named, and each appears in the [dependency register](../templates/execution/dependency-register.md). DEP4 (usage meter, needed by 2027-01-08, open) is the binding constraint on EXP-2; R7 and R8 are risks tracked in the coverage sheet; the migration memo (due 2027-10-01, LC33) is owned by Isabel Ferreira
- [x] At least one thing has been parked or killed since the last review, or the owner has written why not. BL-09 killed 2026-12-21, BL-10 killed 2026-11-03, BL-06 parked 2026-12-23; three items, all with reasons and dates
- [x] The change log shows the roadmap is alive, not laminated. Four entries from 2026-12-21 to 2027-01-14, recording the pivot, the kill, the parking and the board's packaging hold

Signed: Maya Chen, Product Manager, 2027-01-14
