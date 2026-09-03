# MoSCoW prioritization

Based on the ideas of Dai Clegg, from his rapid application development work at Oracle, published in Case Method Fast-Track (1994) and later adopted by the DSDM method. Explained here in this repository's own words.

## What it is for

When the date is fixed, scope is the only variable left, and MoSCoW is the language for negotiating it before the date does it for you. Every item gets one of four labels: Must, Should, Could, or Won't (this time). The labels are only useful with two disciplines attached: a test question that decides the label, and a cap on how much of the capacity Musts may consume. The cap is what makes the plan survive a bad week; without it, everything is a Must and the first slip is a failed release.

## Run it when

- A release date is fixed by a contract, a regulator, an event, or a public commitment, and the candidate list is bigger than the timebox.
- Every stakeholder calls every requirement critical and the PRD's scope section reads as a wish list.
- You need a written "not this time" that stops an item being re-raised every week.

**Skip it when:** the date is not fixed. MoSCoW without a deadline is a backlog with adjectives; the labels never bite because nothing forces a cut. Use the [RICE sheet](rice-scoring-sheet.md) instead and let capacity draw the line.

## Inputs you need first

- The date, and what makes it fixed (the contract clause, the regulation, the event).
- Capacity inside the timebox, in person-weeks, from the team.
- The candidate list with an effort estimate per item, in the same unit.
- What "the release fails" means: the legal, contractual, and operational conditions, from the [BRD](../../templates/definition/brd.md) or the [one-pager](../../templates/definition/one-pager.md).
- Who negotiates for whom, from the [stakeholder map](../../templates/execution/stakeholder-map.md), and who decides, from the [triad decision rights](../../knowledge/roles/triad-decision-rights.md).

## The worksheet

### Step 1: the tests

| Label | Test question | Passes when |
|---|---|---|
| Must | If this is missing on the date, do we ship? | The answer is no: it is required by law or contract, the product is unusable without it, or there is no workaround at all |
| Should | What is the workaround for the first six weeks? | A workaround exists and is painful; dropping it costs something measurable but not the release |
| Could | What do we lose if this never ships? | Nothing we can measure; it is wanted, and it is the first cut |
| Won't (this time) | Has the owner agreed in writing? | It is out of this release, recorded with a revisit date, so it stops being re-raised |

### Step 2: classify

| Item | Label | Test answer (why this label) | Effort (person-weeks) | Requested by | Agreed by |
|---|---|---|---|---|---|
| [item] | [M / S / C / W] | [one sentence] | [n] | [role] | [role] |

### Step 3: the cap check

Share = effort in the label / timebox capacity. Default cap: Musts at or under 60 percent of capacity. The remaining 40 is where Shoulds and Coulds live, and it is the contingency: when the timebox goes wrong, Coulds are dropped first, then Shoulds, and the Musts still ship. Set your own cap if 60 is wrong for your risk, and write it on the sheet.

| Label | Effort sum | Share of capacity | Cap | Pass? |
|---|---|---|---|---|
| Must | [n] | [n / capacity] | [60 percent] | [yes / no] |
| Should | [n] | | | |
| Could | [n] | | | |
| Total | [n] | [at or under 100 percent] | | |

If Musts exceed the cap there are exactly three moves: demote a Must, move the date, or add capacity that exists today. A fourth move, hoping, is not on the sheet.

### Step 4: the negotiation script

<!-- Run these in order with the stakeholder who wants an item promoted. Only the deciding owner changes a label; seniority moves nothing, evidence does. -->

1. "What happens on the date if this is missing?" An answer of "it will be embarrassing" is a Should. An answer that names a contract clause or a legal duty is a Must.
2. "Which current Must comes out to make room?" Whoever promotes an item names the demotion, so the cap holds.
3. "What is the workaround for six weeks?" If one exists, the item is a Should, and the workaround is written next to it.
4. "Shall we write it as a Won't for this release, with a revisit on [date]?" The graceful exit, on paper, that stops the weekly re-raise.

## Reading the result

Musts under the cap and the total under capacity: the plan holds, and the Should and Could rows are the published order of what gets cut. Musts over the cap: the release is already late; go back to step 3 today. A Must at risk during the timebox is an escalation, never a quiet reclassification. A Won't list that is empty means the negotiation did not happen.

## ILLUSTRATIVE example

Ledgerline's expense-report copilot, first release pinned to the finance team's policy refresh date, invented as 2027-01-15. Timebox capacity: 30 person-weeks.

| Item | Label | Why | Effort |
|---|---|---|---|
| Receipt extraction for photographed receipts | Must | The release is the draft; without it there is nothing to review | 10 |
| Filer review-before-submit screen | Must | Policy makes the filer accountable; no draft may submit unseen | 4 |
| Audit trail of drafted versus edited fields | Must | Finance's audit firm requires it under the contract | 3 |
| Policy category suggestion | Should | Workaround: the category dropdown already exists | 6 |
| Reviewer bulk approve | Should | Workaround: reviewers approve one by one, as today | 3 |
| Mileage from calendar entries | Could | No measurable loss; first cut | 3 |
| Filing on behalf of another employee | Won't | Parked; revisit after launch once the assistant workflow is researched | 0 |

Cap check: Musts 17 of 30, about 57 percent, under the 60 cap. Shoulds 9 (30 percent), Coulds 3 (10 percent). Total 29 of 30. When extraction ran long in week seven, mileage was cut first, by the published order, and nobody had to meet about it.

## The trap

Keeping the labels and dropping the cap. Stakeholders learn within one release that Should means "did not ship," so by the next release everything arrives as a Must, and a team without the cap rule accepts a sheet that is 95 percent Must and 5 percent contingency. The first bad week then forces a cut from the Must row, which by definition fails the release, and the meeting that follows is the one MoSCoW was meant to prevent. The cap is not decoration; it is the whole method. A sheet with the share column blank has not been run.

## Feeds

- [One-pager](../../templates/definition/one-pager.md): section 3 scope and section 5 not doing
- [PRD](../../templates/definition/prd.md): section 4 functional scope and section 7 out of scope
- [Gate 2: requirements signed off](../../os/STAGE-GATES.md), where out-of-scope must be written and read by the sponsor
- [Decision log](../../templates/execution/decision-log.md): every label change and its evidence
- [Roadmap](../../templates/planning/roadmap.md): the Musts become the Now row's commitment
- Method background: the MoSCoW entry in the [knowledge index](../../knowledge/INDEX.md)
