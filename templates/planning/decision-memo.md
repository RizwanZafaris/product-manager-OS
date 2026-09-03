---
layer: templates
stage: PLANNING
gate: 1
feeds: []
method: ""
aliases: []
---
# Decision Memo: [the decision, stated as a question]

Stage: PLANNING track, any stage; feeds the [gate the decision unblocks](../../os/STAGE-GATES.md) through the [decision log](../execution/decision-log.md)
Knowledge: [decision doors worksheet](../../frameworks/prioritization/decision-doors.md)
Skill: [decision-memo](../../skills/decision-memo/SKILL.md)

> **Delete any section you do not need.** A two-way door settled by two people in ten minutes is a decision log entry, the lightest rung in [os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md). This memo is for decisions that are costly to reverse, cross teams, or need a sponsor's name. Never leave a heading standing over white space.

<!-- One decision, one decider, one date. The memo exists to get the decision made by
     the person who can make it, with the options that lost on the record and the
     dissent captured in the dissenters' own words. The structure is Minto's
     situation, complication, resolution, indexed in the knowledge layer.

     Neighbours: the decision log (../execution/decision-log.md) stores the outcome
     in six lines; the change request (../execution/change-request.md) handles a
     change to a baseline Gate 2 already signed; the escalation skill
     (../../skills/escalation/SKILL.md) takes a decision that has already missed its
     date.

     Fill first: the question and door type in section 1, the options table in
     section 3, and the recommendation in section 4. -->

**Author:** [name] · **Decider:** [one name] · **Decision needed by:** [YYYY-MM-DD] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Decided

## 1. The decision

- **Question:** [one sentence, answerable with one of the options below]
- **Door type:** [one-way or two-way], because reversing it would cost [time, money, trust, in one line]
- **Who decides:** [the one name above, and why it is theirs to make]
- **By when, and why then:** [date, and what is lost per week after it]
- **The default if nobody decides:** [what happens by inertia; this is the real option A]

<!-- Door type sets the weight of everything below. A two-way door with a cheap
     reverse gets one page and a fast decider; a one-way door gets the evidence
     table filled and a sponsor's signature. Weighing a reversible decision like an
     irreversible one is the slow-team failure; the reverse is the reckless one. -->

## 2. Situation and complication

**Situation:** [two to four sentences everyone in the room already agrees are true]

**Complication:** [what changed, or what is now blocked, that makes a decision necessary now]

**Resolution in one sentence:** [the recommendation, so a reader who stops here still has it]

## 3. Options

<!-- Include the default from section 1 as a row. Cost includes people and time,
     not only money. "Who favors it" is there so the decider can see the room, not
     to count votes. For more than three options with competing criteria, run the
     weighted decision matrix (../../frameworks/prioritization/weighted-decision-matrix.md)
     and paste its result here. -->

| Option | What it means in practice | Cost (money, time, people) | Benefit | Main risk | Reversibility | Who favors it |
|---|---|---|---|---|---|---|
| A. [Default: do nothing or decide later] | | | | | | |
| B. | | | | | | |
| C. | | | | | | |

## 4. Recommendation

- **Option:** [letter], because [two or three sentences].
- **What it gives up:** [what the losing options offered that this one does not].
- **Conditions:** [what must be true, with an owner and date each].
- **Reversal trigger:** [the observation that would reopen this, and by when we would know].

## 5. Dissent

<!-- Written in the dissenter's words and read back to them before the decision.
     A memo with no dissent row was either not circulated or not read. Dissent
     recorded here is what lets the team commit after deciding, because nobody has
     to relitigate to be heard. -->

| Who (role) | Their position | Their strongest argument | Why the recommendation stands, or what it changed |
|---|---|---|---|
| | | | |

## 6. Evidence

| Claim the recommendation rests on | Source (evidence note, data, document) | Confidence (high / medium / low) |
|---|---|---|
| | | |

## 7. Decision record

<!-- Filled after the decision, then copied into the decision log within a day. -->

- **Decision:** [the option chosen, as a statement]
- **Decider and date:** [name, YYYY-MM-DD]
- **Options rejected:** [letters, one reason each]
- **Who is told, how, when:** [channel, date]
- **Decision log entry:** D-[n] in [decision-log.md](../execution/decision-log.md)

---

## Exit gate (feeds the decision log and the gate it unblocks)

Done when every box is honestly ticked. The decision lands as an entry in [decision-log.md](../execution/decision-log.md) and unblocks its [gate](../../os/STAGE-GATES.md).

- [ ] The question has one decider and one date, and the default outcome is written
- [ ] Door type is stated with the cost to reverse, and the memo's weight matches it
- [ ] Options include the default, each with a cost and a main risk
- [ ] The recommendation names what it gives up and the trigger that would reverse it
- [ ] Dissent is recorded in the dissenter's words and was read back to them
- [ ] Every load-bearing claim has a source and a confidence level
- [ ] After the decision: the D-number exists and the people affected have been told
- [ ] Signed by the decider, [name], [date]
