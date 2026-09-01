# DISCOVER bank

Stage: DISCOVER, feeds Gate 1 (problem worth solving) in [../../../os/STAGE-GATES.md](../../../os/STAGE-GATES.md).
Working handoffs: research via [../../../agents/research-agent.md](../../../agents/research-agent.md); the accepted answers roll into the filled `templates/discovery/` set, headed by the discovery document.
Applies: [Jobs to Be Done](../../../knowledge/jobs-to-be-done.md), the Christensen, Ulwick, and Moesta framing that people hire products to make progress in a circumstance, and doing nothing is a competing hire. The Conductor names this method aloud when DISCOVER-2 and DISCOVER-4 run.
Applies: [Continuous Discovery](../../../knowledge/torres-continuous-discovery.md), Teresa Torres's argument that a weekly interview habit beats commissioned research phases because evidence arrives before the decision, not after. The Conductor names this method aloud when DISCOVER-5 runs.
Format and ladder: [README.md](README.md).

### DISCOVER-1: name the person

Ask: Who exactly has this problem?
Wrong costs: Every later stage is built for a composite nobody, and the beta is where you find out.
Evidence class: 4, interview claim, or better; a named user beats a cited quote.
Cross-examine when: the answer is a segment, a market, or a persona label. Move: category to name, one title, one named or precisely described company, one consequence that person personally eats.
Accept when: one title, one company, one consequence, one citation.
Lands in: `discovery/problem-framing.md` section 6 and `discovery/personas.md` evidence block, and STATE.md accepted answers.
Follow-up on strength: would that person take a call about this next week, and how do you know?

### DISCOVER-2: last occurrence

Ask: What did that person do the last time the problem occurred?
Wrong costs: Intentions poll well and predict nothing; you scope against behavior or against air.
Evidence class: 1 or 2, observed behavior or an artifact of the workaround: a ticket, a spreadsheet, an export.
Cross-examine when: the answer describes what they want, plan, or would do. Move: interest to behavior, what did someone pay, or what broke that caused a call?
Accept when: a dated action with a place it is recorded, or the workaround artifact named.
Lands in: `discovery/problem-framing.md` section 4 and `discovery/journey-map.md`, and STATE.md accepted answers.

### DISCOVER-3: workaround cost

Ask: What does the current workaround cost them, per what period?
Wrong costs: A problem with no priced pain loses every roadmap argument it enters.
Evidence class: 2, artifact, or an explicit assumptions-register entry.
Cross-examine when: the number arrives without a unit, a period, and a source. Move: naked numbers, route to the assumptions register unless all three arrive.
Accept when: number, unit, period, source, or a register row owning the guess.
Lands in: `discovery/problem-framing.md` section 5, and STATE.md accepted answers.

### DISCOVER-4: cost of nothing

Ask: What does it cost to do nothing?
Wrong costs: Without this line the honest default is to do nothing, and the gate should say so.
Evidence class: 2, artifact, or an explicit assumptions-register entry; the calculation shown either way.
Cross-examine when: the answer is a fear, not a figure. Move: naked numbers.
Accept when: what it costs, whom, per what period, with the arithmetic visible.
Lands in: `discovery/problem-framing.md` section 5 and `discovery/discovery-document.md` section 3, and STATE.md accepted answers.

### DISCOVER-5: conversation count

Ask: How many real user conversations stand behind this, and where are they cited?
Wrong costs: Gate 1 requires five or more; fewer, undisclosed, turns personas into fiction the whole system then trusts.
Evidence class: 4, interview claims cited by source.
Cross-examine when: the count includes teammates, secondhand summaries, or "lots". Move: banned openers, then re-ask at class.
Accept when: a count, with each conversation cited by source; below five, every persona is marked as an assumption before this answer is accepted.
Lands in: `discovery/discovery-document.md` section 2 citations and `discovery/personas.md` evidence blocks, and STATE.md accepted answers and evidence ledger.

### DISCOVER-6: the no-go case

Ask: What would make the honest answer no-go?
Wrong costs: A gate that cannot fail is a ceremony, and Gate 1 requires the no-go case seriously argued.
Evidence class: a stated disconfirming condition someone could observe; class 5 filed openly is acceptable here, because the condition, not its truth, is the deliverable.
Cross-examine when: the answer is "nothing realistic" or restates the pitch. Move: banned openers, then ask what observation this month would kill it.
Accept when: one observable condition that, if seen, ends the initiative.
Lands in: `discovery/discovery-document.md` section 7, and STATE.md accepted answers.

### DISCOVER-7: the Gate 6 signal

Ask: What observable signal, measurable at Gate 6, says this worked?
Wrong costs: Named after launch, the signal becomes whatever the launch produced.
Evidence class: a measurable signal plus the source system that will measure it.
Cross-examine when: the signal is an adjective or has no source system. Move: naked numbers.
Accept when: signal, threshold or direction, source system, all named before any solution exists.
Lands in: `discovery/discovery-document.md` section 5, and STATE.md accepted answers.

## Forced pair

On "advance anyway": DISCOVER-1, then DISCOVER-5. A team that cannot name one person or count its conversations is the gate's own skip warning in progress.

## Gate 1 rendering

| Gate 1 checklist line | Evidenced by |
|---|---|
| Problem statement one sentence, stated the same way | DISCOVER-1, DISCOVER-2, rolled into `discovery/problem-framing.md` section 3 |
| Five or more real conversations, cited by source | DISCOVER-5 |
| Personas under five cited interviews marked as assumptions | DISCOVER-5 |
| Cost of inaction written down, calculation shown | DISCOVER-3, DISCOVER-4 |
| A plausible no-go seriously argued | DISCOVER-6 |
| Gate 6 success signal named now | DISCOVER-7 |
| Go or no-go recorded with rationale | The signed gate attempt itself; the Conductor never records this line as pass on its own authority |
