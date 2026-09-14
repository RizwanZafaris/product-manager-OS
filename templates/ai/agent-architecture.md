---
layer: templates
stage: AI OVERLAY
gate: 3
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Agent Architecture", "agent-architecture"]
---
# Agent Architecture: [system name]

Stage: AI overlay, active whenever the product contains a model that takes actions; feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md)
Knowledge: [AI product design](../../knowledge/design/ai-interaction-patterns.md)
Skill: [AI PRD skill](../../skills/ai-prd/SKILL.md)

<!-- An agent is a model with tools, and tools are permissions. This document exists so
     that "what can this thing actually do?" has a written answer before the incident,
     not during it. One agent per row; if two agents share a row, they are one agent. -->

**System:** [one sentence: what the agent system accomplishes]
**Architecture owner:** [name] · **Document date:** [YYYY-MM-DD]

## 1. Agent roster

<!-- One row per agent that takes actions in this system. The tools column must be
     exhaustive: a trap is listing the common tools and leaving the rare but
     dangerous one off. This fails when the roster quietly grows a second agent that
     shares a row, because the least-access check then audits only one of them. Do
     not write "and other tools as needed"; that phrase moves the boundary out of
     this document and into whatever someone assumes later. -->

| Agent | Purpose (one sentence) | Model tier (see routing note below) | Tools allowed (exhaustive list) | Data access (systems, scope) | Can it write or only read? |
|---|---|---|---|---|---|
| [e.g. triage agent] | [classifies incoming requests] | [extraction tier] | [none] | [request text only] | read only |
| [e.g. drafting agent] | [fills one template per run] | [drafting tier] | [file read, file write to workspace] | [workspace directory] | write, scoped |
| [add] | | | | | |

## 2. Least-access check

<!-- Run this per agent, in writing. The question is never "what access would be
     convenient" but "what is the minimum that still does the job". -->

For each agent above:

<!-- The access review is per agent, not per system. A trap is inheriting the
     previous agent's answers because the two look similar; their tool lists and
     data scopes differ in ways that matter. This fails when the "broadest single
     permission" line is left as a copy of the roster's tool column, because it
     then records what the agent has, not why it must have it. Never leave a
     misuse line blank; if you cannot picture the worst case, you have not found
     the boundary yet. -->

| Agent | Unneeded tool in last review | Broadest permission and why it cannot be narrower | Worst plausible misuse | Reviewer, date, next review |
|---|---|---|---|---|
| [agent] | [tool, or "none"] | [permission, reason] | [one sentence] | [name], [date], [date] |
| [agent] | | | | |

## 3. Orchestration pattern

<!-- State the one pattern this system uses, not the pattern you wish it used. A
     trap is leaving "Who decides the next step" as "the model" when a prompt
     quietly changed it to deterministic code, or the reverse. This fails when the
     concurrency line says "no parallel agents" but two agents read and write the
     same workspace with no serializer. Do not describe handoffs here; that belongs
     in multi-agent-workflow.md, and a good entry names the file rather than
     restating its rules. -->

| Decision | This system |
|---|---|
| Pattern | [single loop / planner and workers / fixed pipeline / event-driven] |
| Who decides the next step | [the model / deterministic code / a human] |
| Where the plan lives, human-inspectable mid-run | [location, yes or no] |
| Concurrency | [max parallel agents, and what serializes conflicting writes] |
| Failure of one agent | [halts the run / degrades gracefully; state which and how] |

For handoffs, shared state, and termination rules, fill [multi-agent-workflow.md](multi-agent-workflow.md); this document owns who exists and what they may touch, that one owns how they cooperate.

## 4. Boundaries with humans

<!-- Name the specific actions, rails, and stop mechanism already filled in this
     system's guardrails and approval-gate artifacts. A trap is writing a new
     approval list here that drifts from the one in human-approval-gates.md; the
     two must mirror each other. This fails when the kill switch line points at a
     generic "section 4" without naming which guardrails file, because a reviewer
     cannot tell whether it was ever filled. Do not soften an irreversible action
     into "notifies a human"; if it needs approval, list it. -->

| Boundary | This system |
|---|---|
| Actions requiring approval before execution | [list, mirrored in human-approval-gates.md](human-approval-gates.md) |
| Rails that bound every agent in the roster | [filled guardrails.md for this system](guardrails.md) |
| How a human stops the whole system now | [kill switch, from guardrails.md section 4](guardrails.md) |

## Model routing note

Do not hard-wire one model into every agent. The roster's tier column maps each agent to a routing tier: extraction-grade work runs on the cheap tier, drafting on the coding tier, judgment calls on the reasoning tier. The tier doctrine, the config format, and the fallback recipe live in [routing/README.md](../../routing/README.md) and [routing/omniroute.config.json](../../routing/omniroute.config.json); name tiers here, bind them there.

## Exit gate

- [ ] Every agent has an exhaustive tool list; "and other tools as needed" appears nowhere
- [ ] The least-access check is filled per agent with a reviewer and dates
- [ ] Write access is scoped and justified everywhere it appears
- [ ] Every irreversible action routes through a gate in human-approval-gates.md
- [ ] Each agent names a routing tier, and the tier exists in routing/omniroute.config.json
