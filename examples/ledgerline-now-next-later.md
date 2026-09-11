# Now, Next, Later roadmap

Fills [frameworks/prioritization/now-next-later.md](../frameworks/prioritization/now-next-later.md). Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, its customers, its vendor, and every count, score, price, date and dollar figure are fiction built so that the roadmap can be checked against the [journey data sheet](ledgerline-journey.md) and the [coverage sheet](ledgerline-coverage-sheet.md). No figure is a benchmark, a target to copy, or a claim about any real product.

**Owner:** Maya Chen, Product Manager · **Date:** 2027-01-04 · **Status:** Q1 2027 roadmap, sorted from WSJF and the backlog · **Product:** Ledgerline Expense Copilot · **Sources:** [ledgerline-journey.md](ledgerline-journey.md), [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md)

## What it is for

This roadmap sorts Ledgerline's Q1 2027 add-on work by confidence rather than by date. Now is committed and dated. Next is shaped and likely, with quarter-level precision. Later records a direction and its promotion signal without committing to a solution date.

The ordering starts with the WSJF ranking in LC42 and LC43:

1. BL-01, the usage meter: `(13 + 20 + 8) / 4 = 41 / 4 = 10.25`.
2. BL-03, the G-1 activation event: `(1 + 1 + 3) / 1 = 5 / 1 = 5.0`.
3. BL-04, the G-2 draft-id repair: `(3 + 1 + 5) / 3 = 9 / 3 = 3.0`.
4. BL-05 pre-submit slice: `(5 + 2 + 1) / 3 = 8 / 3 = 2.7`, using the split in LC43.
5. BL-07, migration tooling: `(5 + 1 + 3) / 4 = 9 / 4 = 2.25`.
6. BL-02, German-language extraction: `(5 + 2 + 5) / 6 = 12 / 6 = 2.0`.
7. The remainder of BL-05: `(8 + 2 + 1) / 8 = 11 / 8 = 1.4`.

BL-06 is parked, and BL-08 is not on the WSJF short list. The roadmap column is not a mechanical copy of the score: confidence, dependencies and capacity determine which score has earned Now, Next or Later.

Q1 capacity is `2 engineers x 12 weeks = 24 engineer-weeks`. The 80 percent line is `24 x 0.80 = 19.2 engineer-weeks`. The meter has a stated size of `1 person-month`, or `$10,000` at the engineering rate, and DEP4 is needed by 2027-01-08. The roadmap reserves the Now lane within the 19.2 engineer-week line. EXP-2 has a pre-declared exposure window and decision rule, but this file does not report an EXP-2 result.

## Run it when

- A ranked backlog exists, here BL-01 to BL-08 from the WSJF order in LC42 and LC43.
- The ranked items need a form that sales, support and executives can read without turning Later into a promise.
- Confidence differs by distance: the meter and EXP-2 have dated commitments, while German extraction, multi-receipt capture and the Enterprise re-offer have signals but no committed date.

**Skip it when:** every item has a hard external date. That is not the case here. DEP4 has a needed-by date, and EXP-2 has a pre-declared exposure and kill window, but the Later themes do not have committed dates.

## Inputs you need first

- **Ranked backlog:** BL-01 to BL-08, the active items on the backlog register in LC40.
- **WSJF order:** LC42 and the BL-05 split in LC43.
- **Objective linkage:** KR1, active add-on accounts, for the meter, G-1 event and EXP-2; KR2, first-submission approval on drafted reports, for the G-2 repair and pre-submit slice; KR4, add-on MRR, for migration tooling and the usage-price path.
- **Dependency status:** DEP4 is open and blocks EXP-2. DEP5 is delivered, but R3 remains open because the German-language eval result is 71% against the 90% threshold.
- **Capacity:** `2 x 12 = 24 engineer-weeks`; `24 x 0.80 = 19.2 engineer-weeks`.
- **Parked and killed list:** BL-06 is parked until 2027-02-12. BL-09 and BL-10 are killed, with their ids spent.

## The worksheet

### Step 1: the entry tests

| Column | What it means | Entry test, all must hold | Precision allowed | Q1 application |
|---|---|---|---|---|
| Now | Committed, in flight or next up | Confidence at or above 70 percent; every dependency resolved or dated; capacity reserved within the 80 percent line; outcome named | Month or sprint | BL-01, EXP-2 and the G-1 event meet the confidence and commitment tests |
| Next | Shaped, planned, not started | Problem evidenced; solution shaped enough to size; confidence 50 to 70 percent | Quarter | BL-04, the BL-05 pre-submit slice, BL-07 and phase 3 meet the evidence and confidence tests |
| Later | A direction, not a feature | Problem named, evidence that it exists, strategy bet served, no solution committed | None: theme and problem only | German extraction, multi-receipt capture and the Enterprise re-offer have signals but no committed dates |
| Parked or killed | Deliberately not doing | Written reason and a date | Not applicable | BL-06 is parked until 2027-02-12. BL-09 and BL-10 are killed |

### Step 2: sort

| Initiative | Column | Outcome it serves, objective ref | Confidence | Evidence for the confidence | Dependency status | Precision written as | Promotion or demotion signal |
|---|---|---|---|---|---|---|---|
| BL-01, usage meter and running cost, LEDGERLINE-S6 | Now | KR1, active add-on accounts; enables EXP-2 | 90 percent | LC40 marks BL-01 committed. DEP4, ADR-008 and N87 define the meter and its need | Dated, DEP4 needed by 2027-01-08 | By 2027-01-08 | Promote EXP-2 only after the meter counts drafted reports per account and bills in arrears. Demote if DEP4 slips |
| EXP-2, usage re-offer at $2.40 per drafted report | Now | KR1, active add-on accounts | 80 percent | N89 and N91 pre-declare the price, single-arm design and 6.0% success bar | Dated, DEP4 needed by 2027-01-08 | Exposure 2027-01-11 to 2027-01-29 (N91); kill or analysis date 2027-02-12 (N92) | At least 6.0% activated within 14 days of exposure keeps the bet eligible for phase 3. Under 4.0% at the analysis date or on 2027-02-12 kills it. This roadmap reports no EXP-2 result |
| BL-03, G-1 manual-invoice activation event | Now | KR1, active add-on accounts and accurate M-002 | 75 percent | G-1 is defined in the dictionary. LC40 marks BL-03 refined, and N82 records 3 legacy annual-invoice accounts activated through manual invoice lines | No blocking dependency, the billing event is the known gap | February | Promotion to completed when the manual invoice line emits the activation event. Demote if the event remains absent and M-002 is still undercounted |
| BL-04, G-2 draft-id repair | Next | KR2, first-submission approval on drafted reports | 60 percent | G-2 identifies classic-approvals events without a draft id, affecting about 11% of S-1. LC40 marks BL-04 candidate | Open, solution needs shaping | Q1 2027 | Promote when the event mapping is shaped and sized, and the affected accounts can enter M-006. Demote if the repair cannot preserve the metric definition |
| BL-05 slice, warn the filer about the single top bounce cause before submit | Next | KR2, first-submission approval on drafted reports | 55 percent | LC43 splits the item and gives it `8 / 3 = 2.7`, above BL-07. N38 and LC4 evidence support the bounce problem | Open, shaped slice required | Q1 2027 | Promote when the pre-submit slice is sized and the warning can be evaluated without changing the M-006 denominator |
| BL-07, migration tooling for the 73 held accounts | Next | KR4, add-on MRR, and the usage-price migration path | 50 percent | LC40 marks BL-07 candidate. N93 and R8 identify the 12-month hold and the migration risk. D10 keeps the two Enterprise quotes withdrawn until EXP-2 resolves | Open, migration decision memo due 2027-10-01 | Q1 2027 | Promote when the migration choice is shaped and the held-account path preserves the N48 promise. Demote if the price or migration decision remains unresolved |
| Phase 3 rollout of whichever price ships | Next | KR1 and KR4, active add-on accounts and MRR | 50 percent | LC45 names phase 3 as Next. The GTM plan held phase 3 after EXP-1 KILL, and D7 sets EXP-2 as the next bet | Open, entry test is EXP-2 at 6.0% or better | Q1 2027 | Promote only if EXP-2 reaches 6.0% or better and its counter-metrics hold: M-009 at most $1.05, M-006 at least 70% and M-010 at most 8 per week |
| BL-02, German-language extraction, R3 | Later | KR2, first-submission approval on drafted reports | Not written | N83 and LC20 record 71% field accuracy against the 90% eval threshold. LC40 marks BL-02 blocked on EVAL-3 | Open, R3 and G-3 remain open | None | Promote when EVAL-3 reaches 90% or better. No solution or date is committed here |
| BL-08, multi-receipt capture | Later | KR2, first-submission approval on drafted reports | Not written | LC40 and the PRD identify one-receipt-per-item as the current boundary. LC40 marks BL-08 candidate, but it is not on the WSJF short list | Open | None | Promote when evidence shows overlapping or multi-receipt capture is a material problem and a safe solution is shaped |
| Re-offer Halvard Marine and Ostrander Group, D10 | Later | KR4, add-on MRR | Not written | N79 records the two Enterprise prospects blocked previously. D10 keeps both quotes withdrawn until EXP-2 resolves | Open, D10 | None | Promote when EXP-2 ships and the offer can be reconsidered without re-selling the seat price killed by D6 |
| BL-06, admin view of billed seats against filers, LEDGERLINE-S4 | Parked | None assigned in this cycle | Not written | LC40 records the item as parked to 2027-02-12 | Parked | Not applicable | Revisit on 2027-02-12 |
| BL-09, revise anchored offer copy | Killed | None | Not applicable | LC40 records KILL on 2026-12-21 because both EXP-1 arms sat under the kill line. D6 records the same decision | Killed | Not applicable | Do not reopen without a changed strategy or evidence |
| BL-10, ten-report free allowance | Killed | None | Not applicable | LC40 records KILL on 2026-11-03. D2 rejected the allowance | Killed | Not applicable | Do not reopen without a changed margin case and decision |

### Step 3: the movement rules

| Move | Trigger | Who records it, where | Applied Q1 rule |
|---|---|---|---|
| Later to Next | The promotion signal in the row has been observed and a solution is shaped | Maya Chen, in the roadmap change log | EVAL-3 at 90% or better can promote German extraction. EXP-2 shipping can promote the Enterprise re-offer |
| Next to Now | Sized, dependencies dated, confidence at or above 70 percent, capacity free | Maya Chen, after the capacity check with Priya Nair | BL-04, the BL-05 slice, BL-07 and phase 3 remain Next until their evidence, sizing and entry tests are met |
| Now to Next | A dependency slipped or confidence fell below 70 percent; say so before anyone notices | Maya Chen, the same week, with a note to whoever was counting on it | If DEP4 slips, EXP-2 moves out of Now before its exposure is treated as committed |
| Anywhere to Parked or Killed | The evidence changed, or the strategy did | Maya Chen, with the reason, in the parked and killed table | BL-06 is parked to 2027-02-12. BL-09 and BL-10 remain killed |
| EXP-2 to decision | The pre-declared activation or kill rule is reached | Maya Chen, in the experiment and roadmap change log | Success is 6.0% or more activated within 14 days of exposure. Kill is under 4.0% at the analysis date or on 2027-02-12. No result is reported in this roadmap |

**Size rule:** Now holds what fits within 80 percent of the capacity for its horizon. Q1 capacity is `2 engineers x 12 weeks = 24 engineer-weeks`; the line is `24 x 0.80 = 19.2 engineer-weeks`. Next holds about the same again. Later is unbounded, but every theme traces to KR1, KR2 or KR4 and has a written promotion signal.

### Mapping to the roadmap template

| This sheet | Roadmap template section | Rows |
|---|---|---|
| Now rows | Now table: initiative, outcome, target period, confidence, dependencies, status | BL-01, EXP-2 and BL-03 |
| Next rows | Next table, with the quarter and shaping status | BL-04, BL-05 slice, BL-07 and phase 3 |
| Later rows | Later table: theme, problem, earliest entry to Next, promotion signal | BL-02, BL-08 and the D10 Enterprise re-offer |
| Parked and killed rows | Parked and killed table, with the reason | BL-06, BL-09 and BL-10 |
| Every move | Change log | DEP4 movement, EXP-2 decision, promotion signals and parking review |

## Reading the result

There are 3 Now initiatives, 4 Next initiatives, 3 Later themes, 1 Parked item and 2 Killed items.

Now is within the capacity boundary: the available line is 19.2 engineer-weeks, and the meter has a stated size of 1 person-month. EXP-2 is a dated operating bet, not a reported result. The G-1 event is included because its absence makes M-002 undercount by up to 3 in the window.

Next is shaped but not yet committed. BL-04 has a 3.0 WSJF score, the pre-submit slice has `8 / 3 = 2.7`, and BL-07 has `9 / 4 = 2.25`. Phase 3 remains behind its entry test, EXP-2 at 6.0% or better.

Later is deliberately date-free. German extraction has an evidence-based signal, EVAL-3 at 90% or better, but the current result is 71% against the 90% threshold. Multi-receipt capture has a named problem but no committed solution. The D10 Enterprise re-offer has a strategy signal, EXP-2 ships, but no date.

## ILLUSTRATIVE example

This completed roadmap is the Ledgerline example. The Q1 2027 sort places BL-01, EXP-2 and BL-03 in Now; BL-04, the BL-05 slice, BL-07 and phase 3 in Next; BL-02, BL-08 and the D10 Enterprise re-offer in Later; BL-06 parked; BL-09 and BL-10 killed: 3 Now, 4 Next, 3 Later, 1 Parked, 2 Killed.

The WSJF order from LC42 and LC43 sets the starting queue:

1. BL-01, 10.25
2. BL-03, 5.0
3. BL-04, 3.0
4. BL-05 slice, 2.7
5. BL-07, 2.25
6. BL-02, 2.0
7. The rest of BL-05, 1.4

The roadmap columns do not copy this order directly. BL-01 and BL-03 lead the queue and sit in Now because both meet the 70 percent confidence line and carry a resolved or dated dependency. BL-02 outranks BL-04 and the BL-05 slice on WSJF but sits in Later, not Next, because R3 is open and its 71% EVAL-3 result is below the 90% threshold: a high score does not buy a column on its own.

Capacity check: Q1 capacity is `2 engineers x 12 weeks = 24 engineer-weeks`, and the 80 percent line is `24 x 0.80 = 19.2 engineer-weeks`. The Now lane holds BL-01's 1 person-month and BL-03's scoped work, with EXP-2 run as a dated operating bet rather than a build item charged against the lane; the lane fits inside the 19.2 engineer-week line.

## The trap

A confidence roadmap becomes a contract when a Later theme receives a helpful date. German extraction is therefore written as a problem and an eval signal, not as a quarter. Multi-receipt capture is written as a theme, not as a release commitment. The Enterprise re-offer names D10 and its promotion signal, EXP-2 ships, without promising when it will happen.

A second trap is treating the WSJF order as sufficient evidence for Now. BL-02 has a WSJF score of 2.0, but its 71% EVAL-3 result is below the 90% threshold and R3 remains open. Its score informs the queue, while its confidence and dependency state place it in Later.

## Feeds

- [Roadmap template](../templates/planning/roadmap.md): the Now, Next, Later and Parked and killed tables, using the mapping above.
- [OKRs](../templates/planning/okrs.md): KR1, KR2 and KR4 provide the outcome references.
- [Dependency register](../templates/execution/dependency-register.md): DEP4 is the dated dependency that lets EXP-2 enter Now.
- [ledgerline-journey.md](ledgerline-journey.md): N89 to N93, DEP4, R3 and the shared identifiers.
- [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md): LC40 to LC45, D10, including the backlog, WSJF order, capacity and Q1 roadmap confidence.
- [WSJF cost of delay worksheet](../frameworks/prioritization/wsjf-cost-of-delay.md): the ranking arithmetic and the BL-05 split.
- Method background: based on the ideas of Janna Bastow, from her roadmapping work at ProdPad (2012 onward), with [Shape Up](../knowledge/shape-up.md) added here for appetite over estimate and confidence decaying with distance.
