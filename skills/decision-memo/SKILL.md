---
name: decision-memo
description: Write a decision memo a decider can act on in one read: the situation, the options priced, the door type, one recommendation, and the dissent recorded. Use when a decision is stuck in threads and meetings, when a choice needs a sponsor's sign-off, when a team keeps re-deciding the same question, or when a reversible call is getting one-way-door treatment (or the reverse). Takes the question, the options, and the evidence on hand; returns the memo in the decision memo template and, once decided, the entry in the decision log.
---

# Decision Memo: one page, one decider, one recorded answer

Decisions die in two ways. The reversible ones get committee treatment and take a quarter; the irreversible ones get made in a chat thread on a Friday. Either way the rationale evaporates, and the question comes back in six months to a room that has to guess why. This skill sizes the process to the door, forces the options to be priced, and puts the answer where the next person can find it.

## Files this skill drives

- [../../templates/planning/decision-memo.md](../../templates/planning/decision-memo.md), the memo itself
- [../../templates/execution/decision-log.md](../../templates/execution/decision-log.md), where the decided outcome lands as a numbered entry
- [../../frameworks/prioritization/decision-doors.md](../../frameworks/prioritization/decision-doors.md), the reversibility sheet that sets how much process the decision gets
- [../../frameworks/prioritization/weighted-decision-matrix.md](../../frameworks/prioritization/weighted-decision-matrix.md), used only when three or more options and three or more criteria need comparing
- Reads: [../../templates/execution/stakeholder-map.md](../../templates/execution/stakeholder-map.md) for who holds the decision. Structural technology decisions go to [../../templates/architecture/adr.md](../../templates/architecture/adr.md) instead.
- Method background: one-way and two-way doors (Jeff Bezos, Amazon shareholder letter, 2015); the situation, complication, resolution spine (Barbara Minto, The Pyramid Principle, 1978), indexed in [../../knowledge/INDEX.md](../../knowledge/INDEX.md). Both explained here in this repository's own words.

## When to use

- A question has been debated for more than ten minutes twice, by the same people
- A sponsor or forum must decide, and needs something shorter than the thread
- A team is about to make a one-way-door call informally, or is treating a two-way door as one
- An earlier decision is being reopened and nobody can find the original rationale

## Inputs

The question in one sentence, the options already on the table, the evidence and the constraints (dates, budget, contracts), and the name of the person who holds the decision. Ask for these when missing: the needed-by date and what expires after it; the decider's name (if no one holds the decision, that gap is the first finding, and the [escalation skill](../escalation/SKILL.md) owns it); the "do nothing" option, priced honestly; and who disagrees and why. A memo with no dissent recorded usually means nobody was asked.

## Workflow

### 1. State the decision as a decision

One sentence, in the form "whether to X or Y by date Z". "Discuss pricing" is a topic; "whether to move the pilot cohort to usage pricing before the renewal window closes" is a decision. If the sentence needs two "whether"s, it is two memos.

### 2. Classify the door

Score reversibility on the decision doors sheet: the cost to reverse (money, time, trust), the time until reversal becomes impossible, and who is affected by a reversal. Decision rule: a two-way door (cheap to reverse, reversal possible for months) gets a one-page memo, one decider, and an answer within two business days of the memo landing. A one-way door (expensive or impossible to reverse) gets the full memo, a review by the affected owners, and an explicit "what would make us wrong" section. Most decisions are two-way doors misfiled as one-way; say which this is and why.

### 3. Write the situation and the complication

Situation: two or three sentences of facts everyone already agrees on. Complication: what changed, or what the deadline forces. No adjectives, no options yet. If the reader would dispute a sentence here, it belongs in the evidence list with a link, not in the situation.

### 4. Price the options

Two to four options, always including "do nothing" and "decide later", each priced. For each: what it costs, what it gives up, the biggest risk, and the evidence that supports it. Decision rule: use the weighted decision matrix only when there are three or more options and three or more criteria that pull in different directions; run its sensitivity check (change one weight, does the winner change) and report the result. For two options, prose beats a matrix. A single option is a demand wearing a memo's clothing.

### 5. Recommend one, and record the dissent

One option, committed, with the reason it beats the runner-up and what is being given up. Then the dissent section: who disagrees, their strongest argument stated in words they would accept, and what evidence would change the recommendation. Dissent is recorded, never resolved by the memo; the decider weighs it. For a one-way door, add the reversal plan: the signal that would show the decision was wrong, who watches it, and what the fallback costs.

### 6. Get the answer and log it

The decider writes granted, declined, or deferred on the memo, with a date. Within a day, create the decision log entry: decider, options that lost, rationale including what was given up, who was told. A deferred decision gets a new needed-by date, or becomes a risk register row with the decider recorded as accepting the risk.

## Output format

The memo, in this order and under these headings:

1. Decision: one sentence, needed by [date], decider [name]
2. Door type: one-way or two-way, with the reversal cost in one line
3. Situation, then complication
4. Options table: | Option | Cost | What it gives up | Biggest risk | Evidence |
5. Recommendation and rationale, one paragraph
6. Dissent: who, their argument, what would change the recommendation
7. For one-way doors: reversal signal, watcher, fallback cost
8. Outcome line for the decider: GRANTED / DECLINED / DEFERRED, name, date

Then the decision log entry, in that template's block.

## Failure modes this skill guards against

- **Committee treatment for a two-way door.** A reversible call that took a quarter cost more than any wrong answer would have.
- **Chat-thread treatment for a one-way door.** Irreversible, undocumented, decided by whoever was online.
- **The single option.** A recommendation with nothing to compare against is a request for a rubber stamp.
- **"Do nothing" left unpriced.** It is always an option, and it is never free.
- **Dissent smoothed away.** Memos that read as unanimous produce decisions that get relitigated.
- **The recommendation that hedges.** "Option A or B, depending" transfers the analysis to the decider.
- **Rationale reconstructed later.** Logged within a day, or it is a rationalization.

## Exit gate

The memo feeds [../../templates/execution/decision-log.md](../../templates/execution/decision-log.md), which every gate in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md) reads. The memo is not done when it is sent; it is done when the outcome line carries a name and a date and the log entry exists.
