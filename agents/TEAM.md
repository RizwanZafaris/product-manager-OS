# TEAM: how the agents work together

Twelve instruction files live in `agents/`. [../AGENTS.md](../AGENTS.md) sets one role per run; this file sets the rest: which agent leads each stage, who supports, which human signs, what one agent hands the next, when an agent stops and asks a person, and how the Conductor calls agents mid-interview. The loop is [../os/OPERATING-LOOP.md](../os/OPERATING-LOOP.md), the gate forms are [../os/STAGE-GATES.md](../os/STAGE-GATES.md). The system works with no agent at all; agents are an accelerant, never a stage.

## 1. Stage table

| Stage | Lead agent | Supporting agents | Human who owns the gate | Artifacts produced |
|---|---|---|---|---|
| DISCOVER | [research-agent](research-agent.md) | [analyst-agent](analyst-agent.md) when the trigger is a metric; [drafting-agent](drafting-agent.md); [validation-agent](validation-agent.md) | Gate 1: product owner, sponsor who can stop it | Evidence notes, problem framing, personas, discovery document |
| DEFINE | drafting-agent | research-agent; [acceptance-agent](acceptance-agent.md) for criteria that can fail; [estimator-agent](estimator-agent.md) for the first sizing; validation-agent | Gate 2: product owner, engineering lead, business sponsor; regulatory owner where regulated | One-pager or BRD, PRD, FRD; NFR; acceptance criteria; assumptions register |
| DESIGN | [architect-agent](architect-agent.md) | estimator-agent for option cost; [red-team-agent](red-team-agent.md) before the gate; drafting-agent; validation-agent | Gate 3: architect or senior engineer, product owner, security reviewer | System design, ADRs, risk register, dependency register |
| BUILD | acceptance-agent | drafting-agent; validation-agent; estimator-agent to re-forecast | Gate 4: engineering lead, QA owner, product owner | Test cases, evidence ledger, testing strategy, edge-case and failure-scenario tables |
| DELIVER | [release-manager-agent](release-manager-agent.md) | [pmm-agent](pmm-agent.md) for narrative and enablement; acceptance-agent for UAT evidence; red-team-agent; validation-agent | Gate 5: release owner, product owner, operations or support lead; regulatory owner where regulated | Release readiness, UAT results, rollback record, launch comms plan, release notes, GTM plan |
| OPERATE | analyst-agent | [growth-agent](growth-agent.md); research-agent for the why behind a number; drafting-agent; validation-agent | Gate 6: product owner and sponsor | Metrics review, metrics dictionary, dashboard spec, growth plan, experiment briefs |
| PLANNING track | estimator-agent for capacity; pmm-agent for positioning | drafting-agent; validation-agent; research-agent | No gate: the product lead, on the planning cadence | Roadmap, OKRs, capacity plan, positioning, product strategy |
| AI overlay | red-team-agent | architect-agent for permissions and guardrail owners; acceptance-agent for eval evidence per version | The stage's gate owners, plus the security reviewer | The `templates/ai/` set at DEFINE and DESIGN; eval results at Gates 4 and 5 |

[hermes-agent](hermes-agent.md) is not a stage agent: it is the integration file for a Hermes deployment, whose task types route into this table.

## 2. The handoff packet

Every agent ends every run with this block, whether the next reader is an agent or a person. The artifact alone is not auditable; the packet is.

```
HANDOFF
From: <agent> · To: <agent, or human role> · Stage: <stage> · Feeds: <Gate n, or planning cadence>
Artifact: <workspace-relative path, and section if partial>
Evidence used:
- <field or claim> <- <source a reader can open, with its date>
Open fields:
- [OPEN: <what is missing>, owner-to-be: <role>]
Conflicts:
- [CONFLICT: <A says X (source)>; <B says Y (source)>]
Not checked:
- <what this run did not verify, and why>
Next action requested: <one line, one owner>
```

Four rules. Evidence lines point at things a reader can open: a workspace path and section, an evidence-ledger row, a dated export, a public URL. "Not checked" is never empty; an agent that checked everything has misread its scope. The receiving agent cannot close a conflict; a human resolves it and the resolution lands in the [decision log](../templates/execution/decision-log.md). An owner-to-be is a role until a human names a person.

## 3. Escalation to a human

An agent stops when the next step needs a decision, a number, or a name the evidence does not hold. The stop is loud: the packet's last line names the rung.

| Rung | When | Who | Form |
|---|---|---|---|
| 0 | An input is missing and another agent owns it | That agent (evidence: research; a value: analyst; a size: estimator) | The packet, with the open field |
| 1 | A conflict between sources, a scope question, or a request to skip work | The product owner running the loop | The packet's conflicts section, both sources shown |
| 2 | A gate line cannot be evidenced, or a condition has no owner or date | The gate's sign-off owners in [../os/STAGE-GATES.md](../os/STAGE-GATES.md) | The gate form, with the line marked unknown |
| 3 | A decision has missed its needed-by date, or two owners deadlock | The ladder in [../skills/escalation/SKILL.md](../skills/escalation/SKILL.md) | The six-part brief; the outcome in the decision log |

Two rules sit above every rung, the gate rules of AGENTS.md restated for a team.

1. **No agent signs a gate.** An agent renders the checklist, marks each line pass, fail, or unknown with evidence beside it, and stops; an unknown blocks as a fail does. Signatures belong to the humans on the sign-off lines; a recommendation is a line in a packet, never a tick in a box.
2. **No agent invents a number or a name.** Not a baseline, an estimate, an owner, a customer, or a citation. The open-field marker is the only legitimate blank, and it names an owner-to-be as a role. A plausible fabrication is the one output this system exists to prevent.

A request to advance past a gate goes through the Conductor's escape hatch in [../os/CONDUCTOR.md](../os/CONDUCTOR.md), never through an agent quietly drafting the next stage's artifact.

## 4. Router

| Request | Agent |
|---|---|
| Facts behind a discovery template; "what do we know about"; competitor behavior; prior art | [research-agent](research-agent.md) |
| Fill one named template from supplied evidence | [drafting-agent](drafting-agent.md) |
| Check a draft against its template and gate before a human reads it | [validation-agent](validation-agent.md) |
| Attack a draft, design, or plan; a hostile read before Gate 3 or Gate 5; red-team a model feature | [red-team-agent](red-team-agent.md) |
| A Hermes deployment routing its PM tasks and model calls through this repository | [hermes-agent](hermes-agent.md) |
| Architecture options with trade-offs; an ADR; NFRs challenged; coupling and dependency risks; build, buy, or partner | [architect-agent](architect-agent.md) |
| Acceptance criteria into test cases; "is Gate 4 actually met"; evidence gaps by criterion | [acceptance-agent](acceptance-agent.md) |
| Readiness walk; rollback record; comms and release notes; the go or no-go packet | [release-manager-agent](release-manager-agent.md) |
| Define a metric; read a cohort or funnel; trace a metrics review to its sources; "why did the number move" | [analyst-agent](analyst-agent.md) |
| Find the growth mechanism and its leak; rank an experiment backlog; "how do we grow this" | [growth-agent](growth-agent.md) |
| Positioning from alternatives forward; messaging; launch narrative; sales one-pager | [pmm-agent](pmm-agent.md) |
| Size work in ranges; check a plan for optimism and missing work; demand against supply | [estimator-agent](estimator-agent.md) |
| Anything else | No agent. The Conductor if a journey is in progress; otherwise the load order in AGENTS.md |

## 5. How the Conductor calls agents

The Conductor interviews; agents work between questions. Its skill file says it in one line: spawn with the accepted answers as input, treat the output as a draft, never as evidence. In full:

1. **One agent per spawn, three inputs.** The accepted-answer rows from STATE.md that bear on the task, the target template path, and the evidence-ledger rows those answers cite. Not the transcript.
2. **The packet is read first.** It says what the output cannot be trusted for.
3. **Output is a draft.** It becomes the recommended default for the next question covering the same field; the user's acceptance is what lands it. Nothing an agent wrote enters the evidence ledger. The sources it cites can, once opened.
4. **Packet fields become interview moves.** Open fields are parked with an owner-to-be and a validate-by date. Conflicts become the next question's options, one letter per side. "Not checked" lines become unknowns on the gate form until evidenced.
5. **Order inside a stage.** Research, then drafting, then validation, then red team, then the stage's lead agent for the synthesis. Never two agents on one field at once.
6. **No agent touches the gate.** Gate rendering is the Conductor's own step, on artifacts, and signing is human.
7. **Method 4.** Agents run on the tier the protocol's per-method notes assign. A capped judgment tier queues red team and cross-examination; it never downgrades them.

This file feeds the gate forms in [../os/STAGE-GATES.md](../os/STAGE-GATES.md), through the humans who sign them.
