---
layer: templates
stage: AI OVERLAY
gate: 3
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Agent Architecture", "agent-architecture"]
---
# Agent Architecture: [system name]

Stage: AI overlay, active whenever the product contains a model that takes actions; feeds Gate 3 (architecture and risks reviewed)
Knowledge: ../../knowledge/INDEX.md
Skill: ../../skills/ai-prd/SKILL.md

<!-- An agent is a model with tools, and tools are permissions. This document exists so
     that "what can this thing actually do?" has a written answer before the incident,
     not during it. One agent per row; if two agents share a row, they are one agent. -->

**System:** [one sentence: what the agent system accomplishes]
**Architecture owner:** [name] · **Document date:** [YYYY-MM-DD]

## 1. Agent roster

| Agent | Purpose (one sentence) | Model tier (see routing note below) | Tools allowed (exhaustive list) | Data access (systems, scope) | Can it write or only read? |
|---|---|---|---|---|---|
| [e.g. triage agent] | [classifies incoming requests] | [extraction tier] | [none] | [request text only] | read only |
| [e.g. drafting agent] | [fills one template per run] | [drafting tier] | [file read, file write to workspace] | [workspace directory] | write, scoped |
| [add] | | | | | |

## 2. Least-access check

<!-- Run this per agent, in writing. The question is never "what access would be
     convenient" but "what is the minimum that still does the job". -->

For each agent above:

- Tool it has but did not need in the last review period: [tool, or "none"]
- Broadest single permission, and why it cannot be narrower: [permission, reason]
- What the worst plausible misuse of its access looks like: [one sentence]
- Reviewed by [name] on [date], next review [date]

## 3. Orchestration pattern

- Pattern: [single loop / planner and workers / fixed pipeline / event-driven]
- Who decides the next step: [the model / deterministic code / a human]
- Where the plan lives and whether a human can inspect it mid-run: [location, yes or no]
- Concurrency: [max parallel agents, and what serializes conflicting writes]
- Failure of one agent: [halts the run / degrades gracefully; state which and how]
- For handoffs, shared state, and termination rules, fill multi-agent-workflow.md; this document owns who exists and what they may touch, that one owns how they cooperate

## 4. Boundaries with humans

- Actions requiring approval before execution: [list, mirrored in human-approval-gates.md]
- Rails that bound every agent in the roster: [link the filled guardrails.md for this system]
- How a human stops the whole system now: [kill switch, from guardrails.md section 4]

## Model routing note

Do not hard-wire one model into every agent. The roster's tier column maps each agent to a routing tier: extraction-grade work runs on the cheap tier, drafting on the coding tier, judgment calls on the reasoning tier. The tier doctrine, the config format, and the fallback recipe live in ../../routing/README.md and ../../routing/omniroute.config.json; name tiers here, bind them there.

## Exit gate

- [ ] Every agent has an exhaustive tool list; "and other tools as needed" appears nowhere
- [ ] The least-access check is filled per agent with a reviewer and dates
- [ ] Write access is scoped and justified everywhere it appears
- [ ] Every irreversible action routes through a gate in human-approval-gates.md
- [ ] Each agent names a routing tier, and the tier exists in routing/omniroute.config.json
