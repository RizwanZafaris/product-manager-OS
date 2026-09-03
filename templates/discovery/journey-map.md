---
layer: templates
stage: DISCOVER
gate: 1
feeds: []
method: "knowledge/torres-continuous-discovery.md"
aliases: ["Journey Map", "journey-map"]
---
# Journey Map: [persona] doing [job or scenario]

Stage: DISCOVER, feeds Gate 1 (problem worth solving)
Knowledge: [Continuous discovery](../../knowledge/torres-continuous-discovery.md)
Skill: [persona-builder](../../skills/persona-builder/SKILL.md)

<!-- One persona, one job, end to end. A journey map that tries to cover every
     user and every path becomes a mural: impressive on a wall, useless in a
     decision. Map the CURRENT journey from evidence first; only then sketch the
     future journey. Teams that draw the future state first are illustrating a
     pitch, not mapping reality.

     Every low point in the emotion row must trace to a session ID or data point.
     A frown with no source is fiction.

     Markdown tables read best at five to seven stages. If the journey genuinely
     has more, split it into two maps at a natural handoff. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD]
**Persona:** [link to the persona block in personas.md] · **Scenario:** [one sentence]
**Evidence base:** [session IDs and data sources this map is drawn from]

## 1. Current journey

<!-- Columns are stages: name each stage as the user would ("get the receipts
     together"), not as your system would ("ingestion"). -->

| | Stage 1: [name] | Stage 2: [name] | Stage 3: [name] | Stage 4: [name] | Stage 5: [name] |
|---|---|---|---|---|---|
| **User actions** | [what they do, observed] | | | | |
| **Touchpoints and tools** | [what they touch: your product, competitor, spreadsheet, phone call] | | | | |
| **Thoughts** | [what they say they are thinking, quoted or paraphrased from sessions] | | | | |
| **Emotion (high / neutral / low)** | [level plus session ID for every low] | | | | |
| **Pain and friction** | [what breaks, slows, or worries] | | | | |
| **Moments of truth** | [where the user decides to continue, abandon, or work around] | | | | |

**Backstage note:** [what happens out of the user's sight at each painful stage: systems, teams, approvals. Often the fix lives backstage.] When one line stops being enough, map the worst scenario properly in a [service blueprint](service-blueprint.md).

## 2. Future journey

<!-- Same stages unless the concept removes or merges one. Only rows that CHANGE:
     do not restate the present. Every claimed improvement should trace to an
     opportunity below. -->

| | Stage 1: [name] | Stage 2: [name] | Stage 3: [name] | Stage 4: [name] | Stage 5: [name] |
|---|---|---|---|---|---|
| **What changes** | | | | | |
| **User outcome** | | | | | |

**Stages removed or merged, and why:** [or "none"]

## 3. Opportunity areas

<!-- Rank by user impact times frequency, not by ease of building. These rows are
     candidate inputs to problem-framing.md and, later, prioritization. -->

| # | Opportunity | Journey stage | Evidence (session IDs, metrics) | Who feels it and how often | Candidate for |
|---|---|---|---|---|---|
| 1 | | | | | [problem-framing.md](problem-framing.md) / backlog / not now |
| 2 | | | | | |

---

### Worked micro-example (illustrative, invented)

> **Scenario:** Roadside Riya files a week of expenses from her car.
> Stages: gather receipts, photograph, submit, wait for validation, resubmit failures.
> Low point: "wait for validation" (emotion: low, INT-003, INT-007), because failures surface two days later when the context is gone.
> Backstage note: validation runs as a nightly batch, which is why feedback arrives late.
> Opportunity 1: move validation feedback to the moment of capture; stage "photograph"; feeds problem-framing.md.

---

## Exit gate (feeds Gate 1: problem worth solving)

- [ ] One persona and one scenario, named in the header
- [ ] Current journey drawn from cited evidence, not memory
- [ ] Every emotion low carries a session ID or data point
- [ ] Backstage note filled for each painful stage
- [ ] Future journey shows only what changes
- [ ] Opportunities ranked by impact and frequency, each with evidence
