---
layer: os
stage: DISCOVER
gate: 1
feeds: ["os/maps/define.md", "skills/conductor/questions/discover.md"]
method: ""
aliases: ["DISCOVER"]
---
# DISCOVER: map of content

Stage 1 of the six in [OPERATING-LOOP.md](../OPERATING-LOOP.md). Find a problem worth solving and prove someone has it. The stage ends at Gate 1 in [STAGE-GATES.md](../STAGE-GATES.md).

This file is a hub node. Its job is to give the graph one place per stage to fan out from, so the vault reads as six clusters instead of one hairball. It is curated by hand, not generated: see [maps/README.md](README.md) for the maintenance rule.

## The gate this stage ends at

| Gate | Closes | What it demands, in one line |
|---|---|---|
| Gate 1: problem worth solving | DISCOVER | Evidence from five or more independent primary sources, a cost of inaction with its arithmetic shown, and the Gate 6 success signal named before any solution exists. |

## Templates this stage owns

| Template | What it is for |
|---|---|
| [discovery-document.md](../../templates/discovery/discovery-document.md) | The roll-up the gate reads: trigger, user, pain, hypothesis, success signal, go or no-go |
| [problem-framing.md](../../templates/discovery/problem-framing.md) | One problem statement, its evidence, the cost of inaction, an owner |
| [user-research-plan.md](../../templates/discovery/user-research-plan.md) | Questions, method, screener, script, synthesis plan, written before the first session |
| [interview-guide.md](../../templates/discovery/interview-guide.md) | The session guide built from the research plan |
| [interview-notes.md](../../templates/discovery/interview-notes.md) | The raw record of one session, kept apart from interpretation |
| [evidence-note.md](../../templates/discovery/evidence-note.md) | One note per source, with the load-bearing quote and its date |
| [discovery-synthesis.md](../../templates/discovery/discovery-synthesis.md) | Themes with quotes and confidence, between research and framing |
| [personas.md](../../templates/discovery/personas.md) | Archetypes with a mandatory evidence section, or marked as assumptions |
| [journey-map.md](../../templates/discovery/journey-map.md) | Current against future state, with the opportunity areas named |
| [jtbd-spec.md](../../templates/discovery/jtbd-spec.md) | Job statement, the four forces, tools hired and fired |
| [opportunity-solution-tree.md](../../templates/discovery/opportunity-solution-tree.md) | Outcome, evidenced opportunities, solutions, this week's test |
| [opportunity-assessment.md](../../templates/discovery/opportunity-assessment.md) | The ten-question go or no-go before an idea earns discovery time |
| [competitive-analysis.md](../../templates/discovery/competitive-analysis.md) | Reached for when a specific decision needs it, never as background reading |
| [survey-design.md](../../templates/discovery/survey-design.md) | Sample, question bank, bias checks, analysis plan written first |
| [usability-test-plan.md](../../templates/discovery/usability-test-plan.md) | Evaluates a solution; it never discovers a problem |
| [service-blueprint.md](../../templates/discovery/service-blueprint.md) | One scenario across frontstage, backstage, and support systems |

## Frameworks the methods come from

| Worksheet | What you run it for | Originator, in one line |
|---|---|---|
| [mom-test-interview-guide.md](../../frameworks/discovery/mom-test-interview-guide.md) | Ask about life and past behavior instead of about your idea | Rob Fitzpatrick set out these interview rules in The Mom Test (2013) |
| [jtbd-job-map.md](../../frameworks/discovery/jtbd-job-map.md) | Map the job in steps and weigh push, pull, anxiety, habit | Ulwick and Bettencourt published the job-map form (2008); the forces framing is Moesta's |
| [opportunity-scoring.md](../../frameworks/discovery/opportunity-scoring.md) | Rank outcomes by importance against satisfaction | Tony Ulwick's outcome-driven scoring, in What Customers Want (2005) |
| [assumption-mapping.md](../../frameworks/discovery/assumption-mapping.md) | Sort assumptions by importance against evidence, then test | Bland and Osterwalder, Testing Business Ideas (2019) |
| [empathy-map.md](../../frameworks/discovery/empathy-map.md) | Consolidate observed sessions into says, thinks, does, feels | Dave Gray at XPLANE, from 2005 onward |
| [kano-survey.md](../../frameworks/discovery/kano-survey.md) | Classify attributes from the standard question pair | Noriaki Kano and colleagues, in their 1984 paper on attractive quality |
| [pmf-survey.md](../../frameworks/discovery/pmf-survey.md) | Ask the disappointment question and read the bands | Sean Ellis popularized this survey in 2009 |
| [design-sprint-runbook.md](../../frameworks/discovery/design-sprint-runbook.md) | Five days from framed problem to tested prototype | Jake Knapp and colleagues, Sprint (2016) |
| [iceberg-model.md](../../frameworks/systems/iceberg-model.md) | Separate a symptom from the structure that produces it | Michael Goodman's four-level teaching form (2002), on Senge's structure-over-blame idea (1990) |
| [cynefin.md](../../frameworks/systems/cynefin.md) | Decide which method the problem can even support | Cynthia Kurtz and Dave Snowden, IBM Systems Journal (2003) |
| [market-sizing.md](../../frameworks/strategy/market-sizing.md) | Build the market twice and reconcile the two numbers | No single originator, and the worksheet says so |

Knowledge behind the methods: [torres-continuous-discovery.md](../../knowledge/torres-continuous-discovery.md), [jobs-to-be-done.md](../../knowledge/jobs-to-be-done.md), [kano-model.md](../../knowledge/kano-model.md). The full index is [knowledge/README.md](../../knowledge/README.md).

## Skills that drive it

| Skill | Use when |
|---|---|
| [product-analyst](../../skills/product-analyst/SKILL.md) | A claim needs a cited source before it enters a discovery template |
| [user-interview](../../skills/user-interview/SKILL.md) | A research question needs a guide, a note sheet, and evidence notes out the other end |
| [feedback-synthesis](../../skills/feedback-synthesis/SKILL.md) | Transcripts, tickets, and reviews have to become weighted themes with source counts |
| [persona-builder](../../skills/persona-builder/SKILL.md) | Evidence exists and the who and the job still are not written down |
| [competitive-intel](../../skills/competitive-intel/SKILL.md) | A named decision needs a sourced teardown, every claim with a URL and a date |
| [market-sizing](../../skills/market-sizing/SKILL.md) | The cost of inaction or a business case needs a size someone can audit |

## Agents that lead it

Per [agents/TEAM.md](../../agents/TEAM.md), section 1.

| Role | Who |
|---|---|
| Lead | [research-agent](../../agents/research-agent.md) |
| Supporting | [analyst-agent](../../agents/analyst-agent.md) when the trigger is a metric, [drafting-agent](../../agents/drafting-agent.md), [validation-agent](../../agents/validation-agent.md) |
| Humans who sign Gate 1 | Product owner, and the sponsor who can stop this |

No agent signs a gate, and no agent invents a number or a name.

## Where this sits in the loop

Entry comes from a dated trigger or from a Gate 6 pivot. Exit feeds [define.md](define.md). The interview path through the same stage is [skills/conductor/questions/discover.md](../../skills/conductor/questions/discover.md).

## Graph links

Wikilinks below are additive: they exist so the Obsidian graph draws the edges. GitHub does not render them, and every file named here is already a normal link above.

- Loop and gates: [[os/OPERATING-LOOP.md]] · [[os/STAGE-GATES.md]] · [[os/WHICH-DOCUMENT.md]] · [[os/PRODUCT-WORKSPACE.md]]
- Neighbor hubs: [[os/maps/define.md]] · [[os/maps/operate.md]] · [[os/maps/README.md]]
- Templates: [[templates/discovery/discovery-document.md]] · [[templates/discovery/problem-framing.md]] · [[templates/discovery/user-research-plan.md]] · [[templates/discovery/interview-guide.md]] · [[templates/discovery/interview-notes.md]] · [[templates/discovery/evidence-note.md]] · [[templates/discovery/discovery-synthesis.md]] · [[templates/discovery/personas.md]] · [[templates/discovery/journey-map.md]] · [[templates/discovery/jtbd-spec.md]] · [[templates/discovery/opportunity-solution-tree.md]] · [[templates/discovery/opportunity-assessment.md]] · [[templates/discovery/competitive-analysis.md]] · [[templates/discovery/survey-design.md]] · [[templates/discovery/usability-test-plan.md]] · [[templates/discovery/service-blueprint.md]]
- Frameworks: [[frameworks/discovery/mom-test-interview-guide.md]] · [[frameworks/discovery/jtbd-job-map.md]] · [[frameworks/discovery/opportunity-scoring.md]] · [[frameworks/discovery/assumption-mapping.md]] · [[frameworks/discovery/empathy-map.md]] · [[frameworks/discovery/kano-survey.md]] · [[frameworks/discovery/pmf-survey.md]] · [[frameworks/discovery/design-sprint-runbook.md]] · [[frameworks/systems/iceberg-model.md]] · [[frameworks/systems/cynefin.md]] · [[frameworks/strategy/market-sizing.md]]
- Knowledge: [[knowledge/torres-continuous-discovery.md]] · [[knowledge/jobs-to-be-done.md]] · [[knowledge/kano-model.md]] · [[knowledge/README.md]]
- Skills: [[skills/product-analyst/SKILL.md]] · [[skills/user-interview/SKILL.md]] · [[skills/feedback-synthesis/SKILL.md]] · [[skills/persona-builder/SKILL.md]] · [[skills/competitive-intel/SKILL.md]] · [[skills/market-sizing/SKILL.md]] · [[skills/conductor/questions/discover.md]]
- Agents: [[agents/TEAM.md]] · [[agents/research-agent.md]] · [[agents/analyst-agent.md]] · [[agents/drafting-agent.md]] · [[agents/validation-agent.md]]
