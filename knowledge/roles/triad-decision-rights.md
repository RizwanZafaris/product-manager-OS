---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Triad Decision Rights", "triad-decision-rights"]
---
# Triad Decision Rights

The product triad, PM, design lead, engineering lead, shares one team and splits four risks: the PM answers for value and viability, design for usability, engineering for feasibility, per [empowered product teams](../cagan-product-teams.md). [Specializations](specializations.md) states that accountability never narrows; what neither card supplies is a procedure for the day two seats disagree. This card supplies it. The premise, drawn from Marty Cagan's work and restated in this repository's own words: decision rights that live in speeches are not rights, they are moods.

## Who decides what

| Question | First voice | The other seats' part |
|---|---|---|
| Is it valuable, will they choose it | PM | Design and engineering supply evidence that tests the belief |
| Is it viable for the business | PM, with the affected stakeholders | The others flag viability costs hiding in their domains |
| Can users succeed with it | Design | PM keeps it tied to the outcome; engineering flags feasibility limits on the design |
| Can we build and run it | Engineering | PM and design state what degrades gracefully and what must not |
| Scope and sequence within the area | PM, after hearing both | Dissent recorded, then commitment |

"First voice" means the seat whose call stands when evidence runs out, not the only voice. A first voice used early and often stops being heard as judgment and starts being heard as rank.

## The partner rule: how might we, never a veto

Each seat's authority is a duty to answer, not a veto over the others. A designer who believes users will fail owes a testable statement of where and why, opened as "how might we", not a blocked ticket. An engineer who believes the design is unbuildable owes the constraint and one alternative that fits it. A PM who overrides either owes the evidence, in writing. The seat that only says no has stopped doing its job and started doing the others' badly.

## The dispute path

Three steps, and the third one always ends in the [decision log](../../templates/execution/decision-log.md):

1. **Restate the dispute as a falsifiable disagreement.** Which of the four risks is contested, and what evidence would settle it? Most disputes die here, because they turn out to be about taste, and taste disputes go to the first voice by default.
2. **Buy the evidence at the smallest price.** An interview prompt, a prototype test, a spike, a data pull, timeboxed in days. The [opportunity solution tree](../../templates/discovery/opportunity-solution-tree.md) assumption-test table is the natural home.
3. **If evidence cannot arrive in time, the first voice decides.** The decision log records the call, the dissent, and the trigger that reopens it. Disagreement is fine; relitigating without new evidence is not. A dispute that survives all three steps leaves the triad through the [escalation skill](../../skills/escalation/SKILL.md), as a brief, not a hallway campaign.

## Saying no without spending the relationship

The triad's decisions get contested from outside more often than from inside. Two moves keep the no cheap, both standard product leadership practice stated in this repo's own words:

- **Stack-rank your P0s.** When a stakeholder declares everything critical, hand them the list and ask for their own ordering. A rank is a decision they share; a label is a demand they filed.
- **Outcome-first questions.** "Which outcome does this move, by how much, and how would we know?" asked sincerely, converts a feature demand into either scoreable evidence for the [roadmap](../../templates/planning/roadmap.md) or a visible shrug, and both are progress. The roadmap's defense page is where the answer lands either way.

## The trap: rights asserted, never written

Every triad believes it has decision rights until the first expensive dispute, when it discovers it has habits. The failure is not malice; it is that nobody wrote the table above down for THIS team, so the dispute becomes a negotiation about the rules during the game. The remedy costs an hour: copy the table, adjust it, put the three names in the [stakeholder map](../../templates/execution/stakeholder-map.md), and log the adoption in the decision log. Revisit when any seat changes hands, because the split is partly a treaty between three specific people.

## Sources

- Marty Cagan, Inspired (2017) and the SVPG essays: the four risks, the empowered triad, and coaching leaders to push decisions to the team; see [empowered product teams](../cagan-product-teams.md).
- Teresa Torres, Continuous Discovery Habits (2021): the trio deciding together from weekly customer contact, which is what makes step 2 of the dispute path cheap; see [continuous discovery](../torres-continuous-discovery.md).
