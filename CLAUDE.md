# CLAUDE

Read [AGENTS.md](AGENTS.md) first. It is the single source of truth for how any agent runtime, this one included, operates this repository: load order, directory map, gate rules, and tool expectations. This file adds nothing beyond the router table below.

## Router

| When the user asks for | Invoke | Backing templates |
|---|---|---|
| "start", "start a product", or any wish to be interviewed through the loop | [skills/conductor/SKILL.md](skills/conductor/SKILL.md); the full protocol is [os/CONDUCTOR.md](os/CONDUCTOR.md) | `templates/execution/state.md`, the question banks in `skills/conductor/questions/`, and the stage templates each accepted answer lands in |
| "resume", "where are we", or "continue" on a product with a workspace | The resume protocol in [os/CONDUCTOR.md](os/CONDUCTOR.md): product README, then STATE.md, then the newest gate file, verify two answers, resume at the Next question ID | `products/<name>/STATE.md` |
| Evidence gathering for DISCOVER or metric evidence for OPERATE | [skills/product-analyst/SKILL.md](skills/product-analyst/SKILL.md) | `templates/discovery/evidence-note.md`, feeding the STATE.md evidence ledger |
| A PRD for an AI-powered feature, or any spec where a model produces the output | [skills/ai-prd/SKILL.md](skills/ai-prd/SKILL.md) | `templates/definition/prd.md` plus the `templates/ai/` overlay |
| A roadmap, quarterly plan, OKR set, or a stress-test of an existing one | [skills/roadmap-builder/SKILL.md](skills/roadmap-builder/SKILL.md) | `templates/planning/roadmap.md`, `templates/planning/okrs.md` |
| Raw feedback to work through: interview transcripts, support tickets, sales notes, reviews, survey text | [skills/feedback-synthesis/SKILL.md](skills/feedback-synthesis/SKILL.md) | `templates/discovery/user-research-plan.md`, `templates/discovery/discovery-document.md` |
| "How much document does this need", or a request for a spec whose weight is unclear | No skill. Read [os/WHICH-DOCUMENT.md](os/WHICH-DOCUMENT.md) and pick the weight before drafting | `templates/definition/one-pager.md` or `templates/definition/prd.md` |
| A premortem, "what could kill this", or any risk pass before Gate 3 | [skills/program-premortem/SKILL.md](skills/program-premortem/SKILL.md) | `templates/execution/risk-register.md`, `templates/execution/dependency-register.md` |
| Anything touching a regulator, license condition, scheme rule, or compliance question | [skills/reg-gap-check/SKILL.md](skills/reg-gap-check/SKILL.md) | `modules/regulated/` (byte-exact, never edited here) |
| Evidence gathering, drafting one template, validating a draft, or attacking a draft | The matching instruction file in `agents/` per the table in AGENTS.md | Named per agent file |
| Anything else in the product loop | No skill. Offer the Conductor once, per AGENTS.md load order step 0, then follow AGENTS.md: find the stage in `os/OPERATING-LOOP.md`, fill the stage's template from `templates/`, take it to its gate in `os/STAGE-GATES.md` | Per stage |
