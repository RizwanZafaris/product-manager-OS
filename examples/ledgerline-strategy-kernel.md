# Strategy Kernel: Expense Copilot

Fills [frameworks/strategy/strategy-kernel.md](../frameworks/strategy/strategy-kernel.md). Everything here is invented: Ledgerline is a fictional mid-market software company of about 900 people, the copilot is the fictional internal product used across this repository, the people are roles, and every figure is ILLUSTRATIVE, carried over from the [discovery document](expense-copilot-discovery.md) to show what a kernel looks like when it is filled, not to describe any real company. The method is Richard Rumelt's kernel from Good Strategy Bad Strategy (2011), restated in this repository's own words. See the [examples index](README.md).

**Owner:** the PM · **Date:** 2026-08-20 · **Period:** the two quarters after Gate 2 · **Reviewed with:** the finance lead (sponsor) and the engineering lead

## 1. Diagnosis

**The situation.** Expense tickets tripled over two quarters after Ledgerline changed travel agencies. Reports bounce at review about a third of the time; first-submission approval sits at 62% (finance system, quarter ending 2026-06-30). Three reviewers spend about 30 hours a month on mechanical checks: totals, categories, receipt attached. Filers re-type what the receipt already says, and ten of twelve interviewees named that as the worst part without being asked.

**The crux.** Two people are doing clerical work that neither is good at, in sequence. The filer transcribes and guesses at a policy they have not read; the reviewer re-checks the transcription and applies the policy by hand. Every bounce is that pair failing once. The obstacle is not the form (the finance lead's first request) and not filer discipline (the reviewers' first theory). It is that policy knowledge and receipt data sit on the wrong side of the submit button.

**What changed.** The agency switch put more receipts, in more formats, in front of more first-time travelers. The policy did not change, which is why "train the filers" keeps failing: they file too rarely to remember it.

**What the diagnosis excludes.** It does not say expense volume is the problem (it is normal for the headcount), and it does not say the reviewers are slow (their pass is mostly mechanical, which is the point).

## 2. Guiding policy

**Move the clerical work to the machine and keep the judgment with the people, on both sides of the submit button.** The copilot drafts from the receipt and shows the policy line behind every suggestion; the filer stays the author and submits; the reviewer sees the machine's confidence and spends attention only where it is low. The system learns policy through reviewer and admin corrections, never by training filers.

What this policy refuses, which is how you know it is a policy and not a goal:

- No auto-submission, even when confidence is high. Accountability stays where the expense policy puts it.
- No card-feed reconciliation, mileage, or per-diem work until first-submission approval has moved on the drafted reports. Scope grows only on evidence that the core claim holds.
- No vendor whose terms allow training on Ledgerline data, whatever its extraction quality.
- No "better form" project in parallel. It would compete for the same two engineers and attack the symptom.

## 3. Coherent actions

Each action follows from the policy and leans on the others; that is the coherence test.

| # | Action | Why it follows from the policy | Leans on |
|---|---|---|---|
| 1 | Ship v1: extraction of four fields, category suggestion with policy line, filer edit-and-submit | The clerical half of the filer's job moves to the machine; the judgment half stays | 3, for the reviewer to trust it |
| 2 | Confidence flags in the reviewer view | The reviewer's mechanical pass shrinks to the flagged fields | 1, and the eval spec's threshold |
| 3 | Admin correction loop for category mappings, logged and versioned, fed back only after a review step | The system converges on policy without a filer ever reading it | 1; grows into the Q4 loop item on the [RICE sheet](ledgerline-rice-scoring.md) |
| 4 | Measure first-submission approval on drafted reports from week one, against the 62% baseline | The scope rule in the policy needs a number to fire on | The [north star tree](ledgerline-north-star-tree.md) |
| 5 | Close the vendor-terms clause before Gate 5 | The policy's third refusal is a contract term, not a feature | Legal; blocks launch if unmet |

## 4. The kernel test

| Question | Answer |
|---|---|
| Does the diagnosis name a crux, not a list of problems? | Yes: clerical work on the wrong side of submit. The tripled tickets are the symptom |
| Would a reasonable rival state the policy differently? | Yes. "Buy a vendor tool and mandate it" is a coherent rival policy; the sponsor argued it at the [business case](ledgerline-business-case.md) and it lost on licence cost and vendor terms |
| Does every action follow from the policy? | Actions 1 to 5 do. A proposed sixth, a month-end reminder nudge, did not, and was cut |
| Is anything here a goal wearing a strategy costume? | "Raise approval toward 80%" is the goal. It appears once, as the number action 4 watches, not as the policy |
| Is anything a slogan? | "Delight filers" was in the first draft and was removed; it excludes nothing |

Two signs of bad strategy were checked and cleared: no fluff (every sentence in the policy can be argued with), and no failure to face the challenge (the crux names something uncomfortable for both the finance lead and the reviewers).

## Open

- [OPEN: the diagnosis assumes the agency switch caused the ticket spike. Nobody has checked whether the policy's category list also changed in the same quarter, which would make "train the filers" less wrong than the crux claims. The finance lead owns the check before the next strategy review.]
- [OPEN: the policy has not been tested against the reviewer-side job map, which does not exist yet. If reviewers need something the flags cannot give them, action 2 is under-specified. The PM owns it, tied to the open item in the [job map](ledgerline-jtbd-job-map.md).]

## Feeds

- [templates/planning/product-strategy.md](../templates/planning/product-strategy.md): section 1 is the diagnosis, sections 2 and 3 carry the bets and the edge, and section 4 is the sequencing rule in the policy's second refusal.
- [templates/planning/roadmap.md](../templates/planning/roadmap.md): the scope rule decides what may enter Next.
- Method: the strategy kernel entry in [knowledge/INDEX.md](../knowledge/INDEX.md), and the blank worksheet at `frameworks/strategy/strategy-kernel.md`.
