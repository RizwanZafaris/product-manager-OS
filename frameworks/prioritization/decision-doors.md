# Decision doors

Based on the ideas of Jeff Bezos, from the Amazon shareholder letter for 2015: one-way doors and two-way doors. Explained here in this repository's own words.

## What it is for

Deciding how much process a decision deserves, before deciding the decision. A two-way door can be walked back cheaply, so it should be taken fast, by the person closest to it, with a light record. A one-way door cannot be walked back, or only at great cost, so it earns options, evidence, dissent, and time. Teams fail in both directions: the committee that spends a week on a button default, and the single engineer who signs a two-year data contract on a Friday. This sheet scores reversibility so the process matches the door, and it writes the door type into the decision log so a later reversal reads as a planned move.

## Run it when

- Two people have debated something for more than ten minutes, the decision log's threshold for logging.
- Someone wants to escalate, or wants to decide alone, and it is not obvious which is right.
- At the top of a decision memo, before the options are written.

**Skip it when:** the decision has to be made in the next hour and both outcomes are cheap. Classifying it is more process than it deserves; decide, write one line in the log, move on.

## Inputs you need first

- The decision stated as a decision, not a topic: "store receipt images with the vendor," not "vendor storage."
- The options, at least two, one of which may be "do nothing yet."
- Who decides, per [triad decision rights](../../knowledge/roles/triad-decision-rights.md).
- What reversal would cost, asked of engineering, legal, finance, and whoever faces the customer.
- Who is affected, from the [stakeholder map](../../templates/execution/stakeholder-map.md).

## The worksheet

### Step 1: score reversibility

| Question | 0 | 1 | 2 | Score |
|---|---|---|---|---|
| Can it be undone? | Fully, by us | Partly, or with a workaround | No, or only by starting over | |
| Cost to reverse | Under a team-week and no money | A few team-weeks, or a modest sum | A quarter of a team, or a sum the sponsor would have to approve | |
| Time to learn it was wrong | Days | A quarter | A year or more, or never with certainty | |
| Who bears the reversal cost | Us | Us and a partner | Customers, a regulator, or the public record | |
| Does it foreclose options? | No | Narrows some | Locks in a contract, a public commitment, or a data model others build on | |
| Blast radius | One team or a pilot group | A product line | Every customer, or the company's name | |
| **Total** | | | | [0 to 12] |

### Step 2: read the door

| Total | Door | Who decides | Before deciding | Record | Time budget |
|---|---|---|---|---|---|
| 0 to 4 | Two-way | The single closest owner | Name the reversal trigger | One line in the [decision log](../../templates/execution/decision-log.md) with the door type | Same day |
| 5 to 8 | Heavy two-way | The owner, with whoever bears the reversal cost | Options, a trial period, a reversal trigger, and a revisit date | Decision log entry with the trigger and the date | One week |
| 9 to 12 | One-way | The accountable lead, with dissent captured | Decision memo: options, evidence per option, the weighted matrix if criteria compete, a premortem if large | Decision memo, decision log, and an [ADR](../../templates/architecture/adr.md) if structural | As long as the evidence takes, with a date the decision will be made regardless |

### Step 3: try to make it a two-way door

Before running one-way process, ask what would convert the door. Conversion is often cheaper than the process.

| Conversion move | What it costs | Converts it? |
|---|---|---|
| Feature flag or staged rollout | [engineering days] | [yes / no] |
| Pilot with a stated end date | [weeks, one segment] | |
| Contract clause: exit terms, data return, shorter term | [negotiation time, price] | |
| Reversible migration: keep the old path alive for a period | [dual running cost] | |
| Announce internally first, publicly later | [delay] | |

## Reading the result

The score sets the process, never the answer. Most decisions in a healthy team score low; a sheet where everything scores high is padding, and a team that runs one-way process on everything gets the real one-way door wrong anyway, because the vendor contract received the same attention as the button color. A high score with a cheap conversion move means convert first, then decide as a two-way door with a trigger. Write the door type and the trigger into the log entry: when the trigger fires and the decision is reversed, the record shows a plan working, not a failure.

## ILLUSTRATIVE example

Three decisions on Ledgerline's expense-report copilot, all scores invented.

| Decision | Undo | Cost | Detect | Who bears | Forecloses | Radius | Total | Door |
|---|---|---|---|---|---|---|---|---|
| Sign a two-year contract with the extraction vendor, receipt images stored on their side | 2 | 2 | 1 | 2 | 2 | 1 | 10 | One-way |
| Store extracted fields in the existing report schema rather than a new table | 1 | 1 | 1 | 1 | 2 | 0 | 6 | Heavy two-way |
| Turn category suggestion on by default for the pilot group | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Two-way |

The contract gets a decision memo, both vendors' data terms in writing, the security lead's dissent recorded, and a conversion attempt: a one-year term with a data-return clause, which would drop the score to 7. The schema choice gets an ADR, a migration script kept runnable, and a revisit date one quarter out. The default gets a feature flag, one line in the log, and a reversal trigger: the pilot's correction rate on suggested categories exceeds the rate for typed ones.

## The trap

Counting the reversal cost only when it falls on you. A team scores "delete the original receipt image after extraction" as a two-way door because the code change is an hour either way, and misses that the cost of being wrong lands on a filer facing an audit with no receipt. Question four exists for exactly this: when someone else bears the reversal, the door is heavier than it feels. The mirror failure is the team burned by one bad reversal that now scores every decision a nine; its cycle time doubles, and the true one-way door, buried in a queue of false ones, gets no more scrutiny than the rest.

## Feeds

- [Decision log](../../templates/execution/decision-log.md): every entry carries its door type and, for two-way doors, the reversal trigger
- [Decision memo](../../templates/planning/decision-memo.md), driven by the [decision-memo skill](../../skills/decision-memo/SKILL.md), for one-way doors
- [ADR](../../templates/architecture/adr.md) for structural one-way doors, feeding [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md)
- [Weighted decision matrix](weighted-decision-matrix.md) when a one-way door has competing criteria; [program premortem](../../skills/program-premortem/SKILL.md) when it is large
- [Escalation](../../skills/escalation/SKILL.md) when a one-way door is stuck past its date
- Method background: the attribution above; decision rights in [triad decision rights](../../knowledge/roles/triad-decision-rights.md)
