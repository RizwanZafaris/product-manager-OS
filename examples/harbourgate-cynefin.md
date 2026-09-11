# Cynefin: Harbourgate payment-provider migration

Fills [frameworks/systems/cynefin.md](../frameworks/systems/cynefin.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and identifier is ILLUSTRATIVE, taken from the [Harbourgate journey](harbourgate-journey.md) and its [coverage sheet](harbourgate-coverage-sheet.md), never to be quoted as a benchmark or copied as a target.

**Owner:** Ife Adeyemi, Tomasz Wierzbicki and Priya Raman · **Date:** 2026-06-18 · **Status:** Scored independently; feeds D-021

Based on the sense-making framework Cynthia Kurtz and Dave Snowden set out in the IBM Systems Journal (2003), and popularized by Snowden with Mary Boone in Harvard Business Review (November 2007); the domain names used here are the later, popularized ones, not the 2003 paper's own terms.

## What it is for

This sheet decides which method Harbourgate can support for each part of the payment-provider migration before the team runs it. D-019 treated the migration as one database-like change: freeze, move, verify and switch. The independent scores show that the problem was confused as posed, because K was scored 3, 3 and 1, giving a spread of:

`3 - 1 = 2`

A spread of 2 meets the confused override. The split below separates the settlement straddle, the live cohort shift, missing-file alerting and the chaotic morning of 2026-06-15.

## Run it when

- The team has argued about whether to analyse, probe or act on the provider migration.
- A dated commitment is being requested for work whose outcome differs between live cohorts.
- A rehearsal has exposed that the migration has no instant at which nothing remains in flight.
- The problem changes after HG-INC-14, D-021 or ADR-0004.

**Skip it when:** a written rule already governs the exact situation and has held. Missing-file alerting is already in the clear domain once A3 is written and applied.

## Inputs you need first

- The problem as D-019 posed it: cut each provider over in one weekend by freezing, moving, verifying and switching.
- Independent scores from Ife Adeyemi, Tomasz Wierzbicki and Priya Raman.
- The time available before harm accrues, including the live settlement and finance-close clocks.
- The attempted action and its outcome: rehearsal 1 on 2026-06-13, followed by HG-INC-14 on 2026-06-15.
- The [Harbourgate journey](harbourgate-journey.md) and [coverage sheet](harbourgate-coverage-sheet.md), especially N16, N37, N46, A3, ADR-0004 and HC41.

## The worksheet

### Step 1: state the problem and its clock

| Field | Entry |
|---|---|
| Problem, as a symptom or a decision | D-019 proposed cutting each provider over in one weekend: freeze, move, verify and switch. Rehearsal 1 showed that settlement lags authorisation and refunds, so there is no instant with nothing in flight. |
| Who must act | Ife Adeyemi as product owner, Tomasz Wierzbicki as cutover lead, Priya Raman for finance close, Bea Lindqvist for reconciliation and the on-call role for a rollback or incident response. |
| Harm per week of study | The completion date moved by 6 weeks, from 2026-07-26 to 2026-09-07. The failed hypothesis also consumed about 4 engineer-weeks on ADR-0004, cancelled 1 cutover weekend and caused 1 late finance close. |
| Tried already, with outcome | D-019 on 2026-06-02 selected a one-weekend migration shape. Rehearsal 1 on 2026-06-13 was aborted at 9 h 10 min against a planned 6 h, with 1,529 of 1,742 Marlowe settlement lines unmatched and £111,500 in the file. On 2026-06-15, the enabled rehearsal job consumed and deleted the production file, causing HG-INC-14 and a finance close 5 h 40 min late. |

### Step 2: score the two axes, independently, then compare

Each scorer filled the K score independently before the split. The source record, HC41, records K for the problem as D-019 posed it. T was not recorded before the problem was split, because the K disagreement already selected the confused domain.

**Axis K, cause and effect:**

| Scorer | K | Meaning | Test applied |
|---|---:|---|---|
| Ife Adeyemi | 3 | Known | Read D-019 as a known migration procedure: freeze, move, verify and switch. |
| Tomasz Wierzbicki | 3 | Known | Read the proposed cutover sequence as a procedure that could be rehearsed and repeated. |
| Priya Raman | 1 | Only knowable afterwards | Read the live settlement and refund behaviour as producing different outcomes across the migration, with the pattern visible only after the rehearsal and incident. |

The result is confused because:

`max(K) - min(K) = 3 - 1 = 2`

| K | Meaning | Test |
|---:|---|---|
| 3 | Known | A written rule exists and has held every time this year. Anyone trained applies it. |
| 2 | Knowable | No rule written, but a qualified expert with data that exists or can be gathered would settle it. |
| 1 | Only knowable afterwards | The same action has produced different outcomes. The pattern makes sense in retrospect and does not predict forward. |
| 0 | Absent | Nobody can say what is driving what right now. |

**Axis T, time available before you must act:**

The initial T score was not recorded before the confused result. T was scored after the split, where the parts had different clocks.

| T | Meaning |
|---:|---|
| 3 | No clock. A quarter of study costs nothing. |
| 2 | A quarter of runway. |
| 1 | Weeks. The situation moves while you study it. |
| 0 | Now. Harm accrues hourly and the ground shifts under the analysis. |

### Step 3: the arithmetic

There is no total and no average. The initial problem is confused because two K scores differ by 2:

`3 - 1 = 2`

The team must not average:

`(3 + 3 + 1) / 3 = 7 / 3`

That average is not used. It would conceal the disagreement and send the team toward a single procedure.

| Rule | Domain | Harbourgate application |
|---|---|---|
| K = 3 | Clear | Missing-file alerting, once A3 states the written 07:45 rule. |
| K = 2 | Complicated | Settlement straddle reconciliation, requiring expert analysis and ADR-0004. |
| K = 1 | Complex | Cohort shift under live traffic, requiring safe-to-fail probes. |
| K = 0 | Chaotic | No discernible cause and effect while harm is accruing. |
| Override: T = 0 and K of 2 or below | Chaotic, until the clock is bought back and the situation is re-scored | The morning of 2026-06-15: K = 2, T = 0, so it was chaotic by override. |
| Override: two scorers differ on K by 2 or more | Confused | D-019 as posed: K scores 3, 3 and 1, with a spread of 2. |

D-019 applied a rule written for database migrations to a payment-provider problem where settlement lags authorisation by up to 3 days and refunds lag by months. The relevant finding is not an average K. It is that the problem contained several domains.

### Step 4: split the problem, because it is never one domain

| Part of the problem | K | T | Domain | Action mode | Instrument to run | Owner |
|---|---:|---:|---|---|---|---|
| Straddle reconciliation: matching legacy-authorised lines that settle after a provider shift | 2, 2, 2 | 1 | Complicated | Sense, analyze, respond | Expert analysis and ADR-0004, with reconciliation against both paths | Bea Lindqvist, with Priya Raman signing the finance reconciliation |
| Cohort shift under live traffic | 1, 1, 1 | 2 | Complex | Probe, sense, respond | Safe-to-fail 5% cohort probes, then 50% and 100%; N16 is the fixed AC-3 pass criterion and N46 supplies the cohort shape | Tomasz Wierzbicki |
| Missing-file alerting | 3, 3, 3 | 1 | Clear | Sense, categorize, respond | A3, the written settlement-file-absent rule: page at 07:45 if no file has landed since 06:30 | Bea Lindqvist |
| The morning of 2026-06-15, scored afterwards | 2, 2, 2 | 0 | Chaotic by override | Act, sense, respond | Incident response for HG-INC-14, then A2, A3, A4 and A5 to buy back the clock and prevent recurrence | Tomasz Wierzbicki as cutover lead, with Priya Raman for finance close |

Arithmetic for the split:

- Straddle reconciliation: `K = 2`, so complicated. `T = 1` does not worsen it.
- Cohort shift: `K = 1`, so complex. `T = 2` leaves it complex.
- Missing-file alerting: `K = 3`, so clear. `T = 1` does not change the domain.
- Morning of 2026-06-15: `K = 2` and `T = 0`, so the override applies and the result is chaotic.

### Step 5: the response table

| Domain | Action mode | What good looks like | Instruments that apply here | Actively harmful here |
|---|---|---|---|---|
| Clear | Sense, categorize, respond | The rule is written, delegated and audited by sample. A3 pages at 07:45 when no file has landed since 06:30, and N72 records the synthetic check: the page fired at 07:46 and the runbook completed in 11 minutes. | A3, the settlement-file-absent rule, the finance close runbook and the alert check | Reopening discovery for a rule that is already written, or treating a missing-file page as an experiment |
| Complicated | Sense, analyze, respond | One expert analysis produces a decision and a range rather than a point. ADR-0004 matches settlement for both paths using either reference and classifies the straddle set. | ADR-0004, dual-path reconciliation, AC-8 and finance reconciliation under N35 | Applying the database migration sequence, or treating an expert answer as final without checking the live settlement cycle |
| Complex | Probe, sense, respond | Several small safe-to-fail probes run with the pass criterion fixed beforehand. The first web cohort is 5%, and AC-3 passes only when the migrated cohort remains within baseline plus 0.5 percentage points over a trailing 7 days, N16. | N46 cohort sizes, N16 as the fixed criterion, per-provider flags, the rollback trigger and the cutover plan v2 | A fixed-date roadmap commitment, a single weekend cutover, or averaging predicted outcomes across cohorts |
| Chaotic | Act, sense, respond | Someone acts inside the hour to stop the bleeding, then the domain is re-scored. HG-INC-14 was detected at 08:10 and resolved at 12:40 on 2026-06-15, after the finance close was already 5 h 40 min late. | Incident response, A2, A3, A4 and A5, followed by the postmortem and re-score | Waiting for consensus, a gate review or a discovery round while a live settlement file has been consumed |
| Confused | Split and re-score | The parts are separated and each is scored on its own. D-021 replaces D-019 because the split showed that reconciliation, cohort movement, alerting and the incident needed different methods. | Step 4, followed by the response for each resulting domain | Deciding on one method for the whole migration, or averaging `3, 3 and 1` into a false K of 2 |

## Reading the result

- **Clear.** Missing-file alerting needed a written rule, not a design sprint. A3 made the rule explicit, and N72 verified that the page fired.
- **Complicated.** The settlement straddle needed analysis because settlement and authorisation could be matched using evidence that existed, but no existing rule settled the references. ADR-0004 is the recorded response.
- **Complex.** The cohort shift needed probes because live traffic could produce different outcomes between cohorts. The 5% cohort and N16 pass criterion made the first probe safe to fail without committing the entire migration.
- **Chaotic.** The morning of 2026-06-15 was scored afterwards as K = 2 and T = 0. The time override made it chaotic because the file had already been consumed and finance harm was accruing.
- **Confused.** D-019 was confused, not merely imprecise. Two scorers saw a known migration procedure, while one saw an emergent live-traffic problem. D-021 is the response to that disagreement.

The key arithmetic is:

`3 - 1 = 2`

That gap is the finding. Averaging the scores would have been:

`(3 + 3 + 1) / 3 = 7 / 3`

The average is deliberately not used.

## ILLUSTRATIVE example

All scores and figures in this example are ILLUSTRATIVE and come from the Harbourgate data sheets.

| Part | K | T | Domain | Mode | What we ran |
|---|---:|---:|---|---|---|
| Settlement straddle reconciliation | 2, 2, 2 | 1 | Complicated | Sense, analyze, respond | ADR-0004: reconcile both paths from one ledger, match on either reference and classify the straddle set. |
| Cohort shift under live traffic | 1, 1, 1 | 2 | Complex | Probe, sense, respond | D-021: use cohorts of 5%, 50% and 100%, with N16 fixed as the AC-3 pass criterion. |
| Missing-file alerting | 3, 3, 3 | 1 | Clear | Sense, categorize, respond | A3: page at 07:45 if no file has landed since 06:30. N72 verified the page and runbook. |
| The morning of 2026-06-15 | 2, 2, 2 | 0 | Chaotic by override | Act, sense, respond | HG-INC-14 response, followed by A2, A3, A4 and A5. |
| D-019 as one problem | 3, 3, 1 | Not recorded before the split | Confused | Split and re-score | The K spread is `3 - 1 = 2`, so the team rejected one method for the whole migration and recorded D-021. |

The last row is the worksheet earning its cost. The arithmetic does not choose a compromise method. It exposes that different parts of the work require analysis, probes, a written rule and immediate action.

## The decision it feeds

D-021 on 2026-06-18 replaces D-019's one-weekend cutover with a phased traffic shift and legacy drain:

- Use 5%, 50% and 100% cohorts for each provider, with 6, 30 and 61 shops for the kiosk cohorts, as specified in N46.
- Use N16 as the fixed AC-3 pass criterion for each migrated cohort.
- Use ADR-0004 for the complicated settlement straddle.
- Use A3 for the clear missing-file rule.
- Treat the morning of 2026-06-15 as a chaotic incident pattern that must be acted on first, then re-scored.
- Do not average the independent K scores.

The decision does not promise a single cutover date or a single method for the whole migration. It commits to a probe cadence and to the safeguards that make the probes reversible.

## Where the output lands

- The problem and its constraints land in the Harbourgate problem framing record, with the confused call and the four-part split attached.
- The decision log gets one entry for D-021, including D-019, the independent K scores and the reason the one-weekend shape was reversed.
- ADR-0004 records the complicated reconciliation decision.
- The cutover plan records the complex cohort method, N16, N46 and the legacy drain.
- The incident postmortem records the chaotic morning and the corrective actions A2, A3, A4 and A5.

## Re-run trigger

**Re-run when the answer to the K question changes: a probe settles what was unknowable, a clear process fails in a way its rule cannot close, an expert analysis returns without an answer, or the system changes shape.**

For Harbourgate, re-score when:

- A cohort fails or passes N16 and changes what is knowable about live traffic.
- A settlement cycle contradicts ADR-0004 or leaves the straddle set unclassified.
- A3 fails to page at 07:45 when no file has landed since 06:30.
- Another incident shows that the morning-of-2026-06-15 conditions have returned.
- A provider, contract, traffic pattern or reconciliation path changes.
- The team reaches another stage transition or planning period.

A domain call with no re-run trigger becomes a label the team defends. The 2026-06-15 incident showed why the label must move when the system moves.

## When this method misleads you

The framework can mislead Harbourgate in three ways.

First, retrospective coherence can make the migration look complicated after ADR-0004 works. The result does not prove that every future cohort can be settled by analysis. The live cohort remains complex because the same action may produce different outcomes under traffic.

Second, domain preference can appear as diagnosis. Ife Adeyemi and Tomasz Wierzbicki scored the D-019 procedure as known, while Priya Raman scored the broader payment behaviour as only knowable afterwards. The disagreement was useful because it exposed that the problem statement combined several parts.

Third, chaos can be assigned after the fact merely because the team acted quickly. The morning of 2026-06-15 qualifies for the chaotic override because `T = 0` and `K = 2`, with harm accruing while the settlement file was missing. A team must name what gets worse if it waits before assigning T = 0.

A single scorer would have returned the domain that matched that person's preferred method. Independent scoring by Ife Adeyemi, Tomasz Wierzbicki and Priya Raman made the disagreement visible.

## Feeds

- The Harbourgate decision record for D-021, with D-019 retained as the reversed decision.
- ADR-0004 for the complicated settlement straddle.
- The cutover plan v2 for the complex cohort probes, N16 and N46.
- A3 and the observability record for the clear missing-file rule.
- HG-INC-14 and its postmortem for the chaotic morning.
- The [Harbourgate journey](harbourgate-journey.md) for the canonical data sheet.
- The [Harbourgate coverage sheet](harbourgate-coverage-sheet.md) for HC41, the Cynefin scoring record.
