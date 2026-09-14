# Problem Framing: Expense Copilot

Fills [templates/discovery/problem-framing.md](../templates/discovery/problem-framing.md). Everything here is invented: Ledgerline is the fictional mid-market software company used across this repository, and this is the first artifact in the internal-v1 chain the [Expense Copilot journey](expense-copilot-journey.md) indexes, drafted the day before Gate 1. Every number, date and id below is ILLUSTRATIVE, carried from that journey's own data sheet (V1, V2) and from [ledgerline-journey.md](ledgerline-journey.md)'s N1 to N7, so it can be checked against the [discovery document](expense-copilot-discovery.md) it feeds. See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Date:** 2026-08-13 · **Status:** Framed 2026-08-13; discovery closes the next day, 2026-08-14

## 1. Situation

Ledgerline is a fictional mid-market software company of about 900 employees (N1) that runs its own expense process on its own platform's Expenses product. Every employee who travels or spends against the company account files a report; the finance system of record shows about 800 reports a month, 2,400 a quarter, 9,600 a year (N2). Three reviewers check every report before it reaches finance (N7). None of this is new: the process, the volume and the review step have been stable for as long as anyone on the team remembers.

## 2. Complication

Ledgerline changed its travel-agency vendor, and expense-related support tickets rose sharply over the two quarters that followed (per [expense-copilot-discovery.md](expense-copilot-discovery.md)'s Trigger section). The finance lead's first instinct was to ask engineering for a better form. Before spending on that, the team ran discovery: interviews with filers and reviewers found that what actually costs time is not the form itself but two things it does not prevent, re-typing data the receipt already states and guessing at a category against a policy the filer has never read, against a first-submission approval baseline of 62% (N3) that the finance lead has already agreed is too low, having set 80% as the number worth aiming for (N4). Discovery closes the day after this framing is drafted.

## 3. Problem statement

> Filers at Ledgerline need a way to submit an expense report that clears review the first time, because a bounced report costs them a second submission and costs a reviewer a second pass, but today they re-type what the receipt already shows and guess at a category against a policy they have never read, which holds first-submission approval at 62% against about 800 reports a month and costs reviewers about 30 hours, about $1,800, a month on mechanical checks a correct draft would not need (N2, N3, N7).

## 4. Evidence

| # | Evidence item | Type (interview / ticket / metric / observation) | Source or ID | Strength (strong / weak) |
|---|---|---|---|---|
| 1 | First-submission approval sits at 62% of reports | metric | finance system of record (N3) | strong |
| 2 | Reviewers spend about 30 hours, about $1,800, a month on mechanical checks: totals, categories, receipt attached | metric, estimate | business case (N7) | strong for the hours, from the finance system; estimate for the dollar conversion |
| 3 | About 800 reports move through the process a month, 9,600 a year | metric | finance system, quarter ending 2026-06-30 (N2) | strong |
| 4 | Filers re-type what the receipt already states and bounce most often on a category mismatch against a policy they have never read | interview | discovery interviews, [expense-copilot-discovery.md](expense-copilot-discovery.md) Pain section | weak, a single round of qualitative interviews, not yet a logged metric |

## 5. Cost of inaction

- **To the user:** a filer whose report bounces re-types and re-submits, then waits on a second reviewer pass; the same pattern is what the business case prices on the reviewer side, about 30 hours, about $1,800, a month spent on mechanical checks a correct draft would not need (N7), at loaded rates of $55 an hour for a filer and $60 for a reviewer (N6).
- **To the business:** at about 800 reports a month (N2) and 62% first-submission approval (N3), a real share of every month's reports cost a second pass before finance sees a clean one. The business case separately estimates about 30 minutes across filer and reviewer for a single bounce (N14), and about 15 minutes, about $13.75, of filing time recovered per report if the pattern reverses (N15); both figures are the finance lead's own estimate, not a measurement, and are marked that way on the sheet that carries them.
- **Trajectory:** worsening, tied to the vendor switch behind this quarter's ticket volume ([expense-copilot-discovery.md](expense-copilot-discovery.md) Trigger). Nothing about the current process is self-correcting: the 62% baseline (N3) is the number the finance lead agreed to watch, not a number anyone expects to improve without a change to how a report gets built.

## 6. Who feels it and how often

| Segment | How many | Frequency of the pain | Severity (blocks work / slows work / annoys) |
|---|---|---|---|
| Filers who travel or spend against the company account and file their own reports | up to about 900 employees (N1), against about 800 reports a month, 9,600 a year (N2) | as often as they file; several times a quarter for a frequent filer | slows work every time, and blocks that report specifically until it is corrected and resubmitted |
| The finance reviewers who approve every report | three reviewers (N7) | continuously; about 30 hours a month combined go to mechanical checks alone (N7) | slows work: time goes to totals and categories instead of judgment |

## 7. Constraints on any resolution

No financial or data regulator applies to this internal expense tool; the regulated overlay this repository's stage gates define does not fire here, and this line is raised again, unchanged, when Gate 2 asks the same question (the journey's own record, V8). Any resolution reads receipts, which may carry personal data about where and when someone travelled or spent, before a person reviews them; the model vendor's terms for training on that data and for how long it retains it are not yet settled and stay open into DEFINE ([expense-copilot-discovery.md](expense-copilot-discovery.md), known risks carried forward). Team capacity is narrow: this chain names three people throughout, Maya Chen as owner, Priya Nair for engineering, and Daniel Okafor as the finance sponsor, with a legal lead engaged by role rather than a dedicated headcount line, so a resolution wider than this problem cannot borrow their time without a separate conversation this document does not have. Discovery closes with a decision the day after this framing is drafted; any resolution funded at that gate inherits whatever scope and timeline Gate 2 sets, not one implied here.

## 8. Decision requested

- **Ask:** fund definition; carry this problem from DISCOVER into DEFINE rather than returning to more discovery or retiring it.
- **From:** Daniel Okafor · **By:** 2026-08-14

---

### Worked micro-example (illustrative, invented)

> **Situation:** Ledgerline's own finance team reviews about 800 expense reports a month.
> **Complication:** A travel-agency switch pushed expense support tickets up for two quarters running.
> **Problem statement:** Filers need a way to submit a report that clears review the first time because a bounce costs them a second submission, but today they re-type receipt data and guess at policy, holding first-submission approval at 62%.
> **Cost of inaction:** Reviewers alone spend about 30 hours, about $1,800, a month on mechanical checks; the finance lead owns that figure and confirms it stands.

---

## How this framing fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| A solution in disguise | "Filers need a copilot" names the fix in the phrasing | Section 3 names only what a filer is trying to do and what stops them; no product, feature or model is named there |
| Too broad to disagree with | "Filing expenses is annoying," which rejects nothing and directs nothing | Section 3 names the re-typing, the category guess and the 62% baseline, particulars a sponsor could argue with one at a time |
| Nobody is shown to have it | A memorable anecdote, and no interview, ticket or log behind it | Every evidence row in section 4 carries a source and a strength label; row 4 is marked weak rather than presented as settled |
| Never sized | "This happens a lot," with no count and no cost | Section 5 carries the reviewer-hours and dollar figures the business case already priced (N7), not an invented number |
| The person is not named | "Users" and "stakeholders" throughout | Section 3 names filers specifically, and section 6 splits them from the three reviewers rather than merging the two |

## Exit gate

(feeds Gate 1: problem worth solving)

- [x] Exactly one problem in this file: a filer's report failing to clear review the first time, nothing else.
- [x] Problem statement contains no solution words: no product, feature or model appears in section 3.
- [x] Every evidence row has a source ID and a strength label: rows 1 to 4 above.
- [x] Cost of inaction carries a number or a named owner and date for the number: section 5 carries N2, N3, N6, N7, N14 and N15.
- [x] A single accountable owner is named: Maya Chen, in the header.
- [x] The decision requested names the sponsor and a date: Daniel Okafor, by 2026-08-14, in section 8.

This checklist is the author's own read of the file, not a gate result. Gate 1 itself was walked and signed the next day, 2026-08-14: GO, decided by Maya Chen (product) and Daniel Okafor (finance lead, sponsor), per [expense-copilot-discovery.md](expense-copilot-discovery.md)'s own Go or no-go section (V2). Discovery's own trigger, target user and hypothesis, drafted across the same window, are the fuller record this framing distills; see that document for the interview synthesis this file does not reproduce in numbers.
