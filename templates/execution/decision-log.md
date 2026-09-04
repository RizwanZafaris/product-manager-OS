---
layer: templates
stage: ALL STAGES
gate: 1
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Decision Log", "decision-log"]
---
# Decision Log: [initiative name]

Stage: all stages, read at every gate in [STAGE-GATES](../../os/STAGE-GATES.md)
Knowledge: [knowledge index](../../knowledge/INDEX.md)
Skill: [decision-memo](../../skills/decision-memo/SKILL.md)

<!-- The decision log answers the most expensive recurring question on any team:
     "why did we do it this way?" Asked without a log, it costs a meeting and gets a
     guess. Asked with one, it costs thirty seconds and gets the truth, including
     the options that lost.

     Division of labor: decisions that shape system structure go in an ADR
     (../architecture/adr.md); everything else that closes a debate goes here:
     scope calls, pricing calls, sequencing, naming, a vendor shortlist, a metric
     definition. Same immutability rule as ADRs: a decision is never edited into a
     different one. Reversals get a new numbered entry that names the old one.

     This file is written continuously, which is what makes the index in
     section 1 load-bearing rather than decorative. A log of forty prose
     entries is a log nobody reads, and a log nobody reads does not answer the
     question it exists for. Scan the table, then open the one entry. -->

**Initiative:** [name] · **Log owner:** [name] · **Started:** [YYYY-MM-DD]
**Entries:** [n] · **Open reversals:** [n] · **Last entry:** [YYYY-MM-DD]

## 1. Index

<!-- Newest first, one row per decision, so a reader can find the entry in a
     glance instead of reading the file. The index is the product; the blocks
     in section 3 are the evidence behind it.

     Status is the column people skip and the one that earns the log. "Holding"
     means the decision still stands. "Reversed" means a later entry replaced
     it, and the reader must follow that link before acting on this one.
     "Superseded by circumstance" is the honest third option: nobody reversed
     it, the world moved, and it is no longer safe to rely on. A log with only
     the first value is a log nobody has revisited. -->

| ID | Decision, in one line | Date | Decider | Type | Status |
|---|---|---|---|---|---|
| D-[n] | | [YYYY-MM-DD] | | scope / pricing / sequencing / vendor / metric / naming | holding |

## 2. When to log, and when not to

<!-- The bar has to be written down, or the log fills with trivia in month one
     and with nothing in month three. Both failures come from the same cause,
     which is that nobody agreed what deserves an entry. -->

| Log it | Do not log it |
|---|---|
| Two or more people debated it for over ten minutes | It was never in question |
| Anyone could reasonably reopen it in three months | It is a task, and the tracker already holds it |
| It closed off an option that cost something to give up | It restates something already decided; link the original instead |
| A new joiner would otherwise ask "why is it like this?" | It changes system structure, which belongs in an [ADR](../architecture/adr.md) |
| It was decided under time pressure or with thin evidence | It is a preference nobody will act on |

**Log within a day of deciding.** A rationale reconstructed a week later is a rationalisation: the reasons that get written down are the ones that survived, not the ones that operated.

## 3. Decisions

<!-- Copy the block. Newest first, and add the matching row to the index above
     in the same edit; an entry with no index row will not be found, and an
     index row with no entry is worse because it looks answered. -->

### D-[n]: [the decision, stated as the decision itself]

- **Date:** [YYYY-MM-DD] · **Decider:** [the one name that made the call]
- **Type:** [scope / pricing / sequencing / vendor / metric / naming / other]
- **Context:** [what forced a decision now, two or three sentences]
- **Options considered:** [option A; option B; option C]
- **Decision and rationale:** [which option, why it won, and what was given up]
- **Evidence it rested on:** [link or "judgment under uncertainty, no data"]
- **What would change our mind:** [the observation that should trigger a revisit]
- **Reverses or is reversed by:** [D-number, or "none"]
- **Who was told:** [channel and date]

---

## 4. How this log fails

<!-- Every row below has been observed in real logs. They are listed because a
     log that fails this way still looks like a log, which is what makes the
     failure expensive: the team believes it has a record right up to the
     moment it needs one. -->

| Failure mode | What it looks like | The rule |
|---|---|---|
| Winners only | Every entry lists what was chosen and no option that lost | An entry with no losing option is a announcement, not a decision. Reject it at review |
| Committee as decider | "The team decided", or three names in the decider field | Exactly one name. A group can agree; only a person can be asked why |
| Edited history | An old entry now describes what the team currently believes | Entries are immutable. A change of mind is a new id that names the old one |
| Rationale is the outcome | "We chose A because A was better" | The rationale names the trade: what A cost, and why that cost was acceptable |
| Silent staleness | Entries from two strategies ago, all still marked holding | Review status at every gate. Mark superseded by circumstance rather than leaving it |
| Log kept by one person | Entries stop when that person is on leave | The owner is named, and the review is on a recurring agenda, not in someone's memory |
| Nobody was told | A correct decision that half the team acts against | "Who was told" is a required field, and blank means the decision has not landed yet |

## 5. Gate review

<!-- Run at every stage gate. The point is not to admire the log, it is to
     catch decisions that quietly expired: a gate is the moment the team is
     already re-examining its assumptions, and a decision resting on an
     assumption that just changed is the cheapest thing to catch there. -->

| Gate | Reviewed on | Entries still holding | Marked superseded | New reversals |
|---|---|---|---|---|
| [n] | [YYYY-MM-DD] | | | |

### Worked micro-example (ILLUSTRATIVE, invented)

<!-- Shows the expected size and, in the last two fields, the two things most
     often left out. Delete it once real entries exist. -->

**Index row:**

| ID | Decision, in one line | Date | Decider | Type | Status |
|---|---|---|---|---|---|
| *D-004* | *Launch in one market, not three* | *2026-04-02* | *R. Ali, product lead* | *scope* | *holding* |

**Entry:**

### D-004: Launch in one market, not three

- **Date:** 2026-04-02 · **Decider:** R. Ali, product lead
- **Type:** scope
- **Context:** Engineering can support one localised rollout per quarter. Sales asked for three markets at once; support has headcount for one queue.
- **Options considered:** all three markets at reduced support depth; one market fully supported; delay a quarter and do two.
- **Decision and rationale:** One market, fully supported. A weak first market costs the reference customers the other two depend on. The delay option loses a committed customer. Given up: two quarters of revenue from markets two and three, and the sales team's stated forecast.
- **Evidence it rested on:** support capacity model, and one customer commitment letter. No data on whether reduced support depth actually costs references; that is the judgment in this call.
- **What would change our mind:** support headcount funded for a second queue, or a second reference customer landing without one.
- **Reverses or is reversed by:** none
- **Who was told:** initiative channel and sales weekly, 2026-04-03

## Exit gate

<!-- Checkable by a person who was not in any of the meetings, which is the
     test of whether the log works. Each box is a fact about the file. -->

- [ ] Every entry has a matching index row, and every index row has an entry
- [ ] Every entry has exactly one decider, by name
- [ ] Every entry lists the options that lost, not only the winner
- [ ] Every rationale names what was given up, not only what was gained
- [ ] Every entry records the evidence it rested on, or says plainly that it was judgment
- [ ] Every entry names what would change our mind
- [ ] No entry has been edited into a different decision; reversals are new ids
- [ ] Entry dates are within a day or two of the decisions they record
- [ ] Status has been reviewed at the most recent gate, and stale entries are marked superseded rather than left holding
- [ ] Structural technology decisions are in [ADRs](../architecture/adr.md), linked rather than duplicated here
- [ ] The worked example above has been removed
