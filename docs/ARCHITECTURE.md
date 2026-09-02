# Product Manager OS: Architecture

This document is the blueprint for the whole repository. It defines the operating concept, the complete file tree, how files link to each other, and what the quality gate checks. When a file in the repo disagrees with this document, fix the file or fix this document, never leave both standing.

## 1. The OS concept

### 1.1 What this is

Product Manager OS turns any capable language model, or no model at all, into a working product management team. It is a document system first and an AI system second. Every template works with a text editor and a pencil. The AI layers (boot prompts, skills, agents, routing) are accelerants stacked on top of a document format that stands without them.

The design follows one rule proven by the regulated module that seeds this repo: graceful degradation is structural, not aspirational. If the model is free-tier, offline, or wrong, the artifacts and gates still function.

### 1.2 The operating loop

A PM runs one product through six stages. Each stage ends at a gate: a named checklist that must pass before the next stage opens. Gates are documents, not ceremonies; a gate passes when its checklist file is filled in and signed.

```
DISCOVER -> [Gate 1: problem worth solving]
DEFINE   -> [Gate 2: requirements signed off]
DESIGN   -> [Gate 3: architecture and risks reviewed]
BUILD    -> [Gate 4: acceptance criteria met]
DELIVER  -> [Gate 5: release readiness green]
OPERATE  -> [Gate 6: outcomes verified, learn or sunset]
        -> loops back to DISCOVER
```

Two tracks run across the loop rather than inside one stage: PLANNING (roadmap, OKRs) which feeds every stage, and AI OVERLAY (eval specs, guardrails, red team) which activates whenever the product itself contains a model. The regulated module is a third overlay for products under a financial or data regulator.

The loop is defined in `os/OPERATING-LOOP.md`, the gate checklists in `os/STAGE-GATES.md`, and a narrative walkthrough of a full pass in `os/HOW-TO-RUN-A-PRODUCT.md`. Since v0.2.0 the Conductor (`os/CONDUCTOR.md`, driven from `skills/conductor/`) can run the loop as a stage-gated interview whose memory is `products/<name>/STATE.md`; the loop itself, and the pencil path through it, are unchanged.

### 1.3 The five layers

| Layer | Directory | Answers | Example |
|---|---|---|---|
| Knowledge | `knowledge/` | WHY a method exists and when it misleads | RICE card explains false precision |
| Templates | `templates/` | WHAT to produce at each stage | PRD template with fill-in fields |
| Skills and agents | `skills/`, `agents/` | HOW to produce it with an AI runtime | conductor interviews the loop; ai-prd drives the PRD template |
| System prompts | `system/` | WHO the model becomes | Boot prompt installs the PM team persona |
| Routing | `routing/` | WITH WHICH model each task runs | Extraction on cheap tier, judgment on frontier tier |

Since v0.3.0 the knowledge layer carries two sub-layers, `knowledge/roles/` (WHO each product title is) and `knowledge/domains/` (WHERE the product plays, ten market cards with a fintech pointer to the regulated module), and a sixth layer sits beside the five: `learn/` (three study paths, a library, a tutor skill, and a practice workspace). `learn/` depends downward only, on `knowledge/`, `templates/`, the `os/` loop files, and the Conductor's question banks, all read-only; nothing outside `learn/` depends on it existing.

Dependencies point downward only. Templates cite knowledge cards. Skills cite templates. System prompts cite skills and templates by repo path. Routing serves all of them. Nothing in `knowledge/` or `templates/` depends on any AI layer existing.

### 1.4 What the field is missing, and what this OS does about it

A teardown of the strongest existing systems (BMAD-METHOD, github/spec-kit, buildbetter product-os, deanpeters Product-Manager-Skills, ChatPRD, the Anthropic PM plugin) shows each owns one segment: spec-kit owns spec-to-code, product-os owns discovery, BMAD owns agentic build. None chains discovery through requirements, architecture, delivery, and post-launch verification in one system. None carries a regulated overlay, a canon knowledge layer with named attribution, tiered model routing, or a whole-tree consistency gate. Those four gaps are this repo's reason to exist, and the file tree below closes each one with a named directory.

## 2. Complete file tree

Legend: (COPY) is a verbatim copy from the source repo, the standalone regulated-ai-prd repository (pre-release), byte-exact where marked; fixes to that material land in the source repo and are re-copied here, never edited here. (EXTEND) starts as a copy of that repo's file and is then modified here. Everything else is original to this repo.

```
product-manager-OS/
├── README.md  Front door: story, loop diagram, four usage methods, quickstart, module map
├── CLAUDE.md  Thin router for Claude Code: points to AGENTS.md as single source of truth, maps triggers to skills/
├── AGENTS.md  Single source of truth for any agent runtime: load order, directory map, gate rules, tool expectations
├── CHANGELOG.md  Keep a Changelog format; what each semver level means here, the release inventory, and a stated known-gaps list
├── LICENSE  MIT, copyright Rizwan Zafar
├── lint.py  (EXTEND)  OS-wide quality gate, stdlib only; original regulated checks preserved, tree mode added (spec in section 4)
├── test_lint.py  (EXTEND)  Unit tests for every original and every added lint check
├── docs/
│   ├── ARCHITECTURE.md  (this file)  The blueprint: concept, tree, cross-link conventions, lint spec
│   └── CONDUCTOR-DESIGN.md  The v0.2.0 design: prior art, the Conductor's contract, journey map, evidence classes, STATE.md format, resume protocol, build plan
├── os/
│   ├── OPERATING-LOOP.md  The six-stage loop, the two overlays, entry and exit definition for each stage
│   ├── CONDUCTOR.md  The interview protocol: seven-rule contract, challenge grammar, gate procedure, escape hatch, per-method notes
│   ├── STAGE-GATES.md  Six gate checklists, each a fill-in form with sign-off lines and a skip-risk warning drawn from field data
│   ├── HOW-TO-RUN-A-PRODUCT.md  Narrative walkthrough: one fictional product taken through all six gates, naming every template used, plus the interview-to-backlog chain hop by hop
│   ├── WHICH-DOCUMENT.md  Picks the artifact weight (logged decision, ticket, one-pager, PRD, BRD+PRD+FRD stack) by stakes, audience, and reversibility
│   └── PRODUCT-WORKSPACE.md  The products/<name>/ folder convention: where filled artifacts accumulate as the product's memory, why it is a folder and not software, and STATE.md's place in the layout
├── knowledge/
│   ├── INDEX.md  All 11 cards plus 18 one-line index entries (Mom Test, ICE, WSJF, HEART, 7 Powers, SCR, and the rest), each with originator and year
│   ├── cagan-product-teams.md  Empowered teams, outcomes over output, four risks; attribution to Marty Cagan's Inspired and Empowered; trap: the label without the accountability
│   ├── torres-continuous-discovery.md  Weekly touchpoints and the opportunity solution tree; attribution to Teresa Torres; trap: a stale tree
│   ├── jobs-to-be-done.md  Progress-based competition framing; attribution to Ulwick, Christensen, Moesta; trap: job stories without interview evidence
│   ├── kano-model.md  Basic, performance, delighter classification; attribution to Noriaki Kano, 1984; trap: delighters decay into basics
│   ├── rice-prioritization.md  Reach x Impact x Confidence / Effort; attribution to Sean McBride at Intercom; trap: false precision
│   ├── shape-up.md  Appetite, shaping, six-week cycles; attribution to Ryan Singer at Basecamp; trap: cycles without shaping
│   ├── north-star-metric.md  One value metric plus input metrics; attribution to Sean Ellis and Amplitude; trap: vanity metrics
│   ├── okrs.md  Objectives and key results; attribution to Andy Grove via John Doerr; trap: key results that are tasks
│   ├── amazon-pr-faq.md  Working backwards from the press release; attribution to Amazon practice per Bryar and Carr; trap: selling a decision already made
│   ├── high-output-management.md  Managerial output is team output; attribution to Andrew Grove; trap: busyness mistaken for impact
│   ├── crossing-the-chasm.md  Beachhead before broadcast; attribution to Geoffrey Moore; trap: the beachhead that is secretly everyone
│   ├── roles/
│   │   ├── INDEX.md  The roles layer map: eight-rung ladder table, the IC/management fork, directional-naming caveat
│   │   ├── ladder.md  APM to CPO, each rung with owns/decides/docs-out/docs-in/success/failure-mode and stage variance
│   │   ├── specializations.md  Core, PO (with the split-is-an-anti-pattern position), TPM, Growth, Platform, Data, AI PM
│   │   ├── pmm-boundary.md  PM vs PMM decision table, frontloaded/backloaded framing, document ownership, the unwritten-boundary warning
│   │   ├── stage-shift.md  Startup vs scale-up vs enterprise per title; the title-inflation trap
│   │   ├── triad-decision-rights.md  Who decides value, usability, feasibility; the how-might-we-never-a-veto rule; the three-step dispute path ending in the decision log; the saying-no pattern
│   │   └── pm-hiring-and-growth.md  Structured hiring loop (screens, project, blind-vote debrief) and the manager 1:1 and career conversation, both calibrated against ladder.md
│   └── domains/
│       ├── INDEX.md  Pick-your-domain table, the Conductor usage note, and the card-to-template-pack graduation rule
│       ├── ecommerce.md · streaming-ott.md · gaming.md · saas-b2b.md · consumer-social.md  Digital-market cards
│       ├── healthtech.md · edtech.md · logistics.md · ai-products.md  Regulated-adjacent market cards
│       └── fintech.md  Pointer card only: routes to modules/regulated and skills/reg-gap-check, duplicates nothing
├── templates/
│   ├── discovery/
│   │   ├── discovery-document.md  Trigger, target user, pain, hypothesis, success signal, go or no-go
│   │   ├── problem-framing.md  One problem statement, evidence, cost of inaction, owner
│   │   ├── user-research-plan.md  Questions, method, screener, script, notes, synthesis themes
│   │   ├── personas.md  Archetype fields plus a mandatory evidence section: minimum five interviews cited or the persona is marked assumption
│   │   ├── journey-map.md  Stages, actions, emotions, current vs future, opportunity areas
│   │   ├── competitive-analysis.md  Decision-to-inform as the one mandatory field, job and current alternatives, dated evidence per claim, axes that can move the decision
│   │   ├── evidence-note.md  One note per source: claim, verbatim load-bearing quote, source, dates, confidence; rows feed the STATE.md evidence ledger
│   │   ├── opportunity-assessment.md  The Cagan ten-question go/no-go before an idea earns discovery time
│   │   ├── discovery-synthesis.md  Research question, themes with verbatim quotes, confidence, implications; sits between the research plan and problem framing
│   │   ├── jtbd-spec.md  Job statement, four forces, tools hired and fired, switch barriers
│   │   ├── opportunity-solution-tree.md  Torres's structural tool as diffable tables: outcome, evidence-cited opportunity branches, solutions, assumption tests with this week's test
│   │   └── service-blueprint.md  One scenario, eight to twelve actions: frontstage, backstage, support systems, line-of-visibility failure points each with an owner
│   ├── definition/
│   │   ├── brd.md  Business objectives, scope, stakeholders, constraints, ROI, sponsor sign-off
│   │   ├── prd.md  Background, objectives, stories, functional scope, success metrics, out of scope, launch criteria; opens with the delete-unused-sections rule and the weight question
│   │   ├── one-pager.md  The light DEFINE weight: problem, proposal, scope, one metric plus a guardrail, not-doing list, up to three acceptance criteria; promoted to prd.md when it stops fitting
│   │   ├── frd.md  Functional requirements list, data flows, interfaces, traceability back to PRD items
│   │   ├── nfr.md  Latency, availability, scale, security, accessibility, retention targets, each with a number or a named owner for the number
│   │   ├── business-rules.md  Rule ID, statement, trigger, source of truth, exceptions, test traceability
│   │   ├── assumptions-register.md  Assumption, confidence, validation method, validate-by date; the most skipped artifact in the field, so the template opens with the cost of skipping it
│   │   ├── acceptance-criteria.md  Given/when/then blocks, edge and negative cases, measurable thresholds
│   │   └── prfaq.md  Working backwards: mock press release, customer quote, external and internal FAQ, availability
│   ├── architecture/
│   │   ├── system-design.md  Goals, non-goals, diagram, components, alternatives considered, tradeoffs
│   │   ├── solution-architecture.md  Context diagram, capability map, integration points, build vs buy rationale
│   │   ├── adr.md  Nygard format: numbered title, status, context, decision, consequences; reversals supersede, never edit
│   │   ├── data-model.md  Entities, relationships, keys, data dictionary, PII classification
│   │   ├── api-contract.md  Endpoint, schema, auth, errors, versioning, worked OpenAPI-style micro-example
│   │   ├── sequence-diagram.md  Mermaid sequence skeleton with sync/async and error path conventions
│   │   ├── integrations.md  System, direction, protocol, auth, SLA, owner, failure behavior
│   │   ├── security-architecture.md  STRIDE walk per component, trust boundaries, risk score, mitigation owner
│   │   └── observability.md  SLOs, logs, traces, alert thresholds, dashboard owner, synthetic failure check
│   ├── execution/
│   │   ├── stakeholder-map.md  Name, interest, influence, RACI tag, cadence, concerns
│   │   ├── risk-register.md  Risk, likelihood, impact, score, mitigation, owner, review date
│   │   ├── decision-log.md  Numbered decisions with context, options, rationale, decider
│   │   ├── dependency-register.md  Dependency, owning team, needed-by, status, escalation contact; governed weekly, not kickoff-only
│   │   └── state.md  The STATE.md blank: position, accepted answers, open challenges, evidence ledger, journal; append-mostly, the Conductor's per-product memory
│   ├── delivery/
│   │   ├── testing-strategy.md  Test levels, coverage targets, environments, entry and exit criteria
│   │   ├── edge-cases.md  Case, trigger, expected behavior, linked test ID; no case left "to be decided"
│   │   ├── failure-scenarios.md  Scenario, blast radius, detection, recovery, data loss risk
│   │   ├── uat-plan.md  Scope, entry and exit criteria, testers, defect severity, sign-off form
│   │   ├── release-readiness.md  Go or no-go checklist: features, tests, known issues, rollback, comms, sign-offs per function
│   │   ├── analytics-instrumentation-spec.md  Event taxonomy, properties, owners, QA plan; filed in delivery, written during DESIGN before build starts
│   │   └── launch-comms-plan.md  Audiences, channel and timeline, messaging per audience, rollback comms
│   ├── operate/
│   │   ├── operational-readiness-review.md  Runbooks, on-call, backup and recovery, blast radius, checks derived from past incidents
│   │   ├── compliance-impact-assessment.md  Applicable regulations, data categories, DPIA flag, retention, legal sign-off
│   │   ├── metrics-review.md  Outcome vs target per KR, input metric movement, decision: persist, pivot, or sunset
│   │   ├── experiment-brief.md  Hypothesis, target metric, variants, sample size and duration, decision rule
│   │   ├── win-loss-review.md  Outcome, primary and secondary reasons, competitor, quotes, action items
│   │   ├── qbr-board-update.md  Metrics vs goal, wins, risks and asks, next-quarter roadmap, decisions needed
│   │   ├── post-launch-review.md  Goal vs actual per launch, once per launch; the recurring instrument stays metrics-review.md
│   │   ├── sunset-eol-plan.md  EOL rationale, timeline, migration path, comms cascade, decommission steps
│   │   ├── incident-postmortem.md  Blameless per-incident review: facts, severity, timeline, quantified impact, systems-language causes with no names, corrective actions with owner and verification
│   │   └── feedback-program.md  Charter for a standing feedback program (CAB, beta, panel): goal tied to a decision, recruiting, cadence, terms, intake routed to evidence notes, program exit criteria
│   ├── planning/
│   │   ├── roadmap.md  Now, Next, Later horizons with theme, initiative, target period, confidence, dependencies, status, and a pre-written expectations-not-commitments preamble to keep above the tables
│   │   ├── okrs.md  Objective, three to five key results with baseline and target, scoring cadence
│   │   ├── first-90-days.md  Mandate in the hirer's words, three learning questions, 30/60/90 blocks, one commitment that can fail, first meetings feeding the stakeholder map
│   │   ├── gtm-plan.md  Written at DELIVER: first cohort and channel with evidence the channel reaches them, positioning against the named alternative, launch sequence, the one launch metric, the stop condition
│   │   ├── growth-plan.md  Written at OPERATE: the input-metric bet, the cheapest experiment that would move it, the loop or channel behind it, the counter-metric, the kill condition
│   │   ├── vision.md  Future-state narrative, why now, who for, north-star tie-in, non-goals
│   │   ├── product-strategy.md  Strategic context, where-to-play bets, differentiation, sequencing, key risks
│   │   ├── north-star-metric.md  NSM definition, input-metric tree with owners, guardrails, review cadence
│   │   ├── positioning.md  The Dunford chain: competitive alternatives, unique attributes, value and proof, target customer, market category
│   │   ├── pricing-packaging.md  Pricing model, tiers, value metric, competitive benchmark, discount rules, owner
│   │   └── partner-integration-brief.md  One lean go/no-go file per partnership: the exchange, the evidenced user problem, the integration surface with owners on both sides, commercial shape and exit terms, dependency and data-sharing risks
│   └── ai/
│       ├── eval-spec.md  Scenario set, golden dataset, metrics, pass threshold, gate that blocks on failure
│       ├── guardrails.md  Input and output constraints, blocked behaviors, enforcement point per rail
│       ├── hallucination-controls.md  Grounding source, abstain policy, verifier step, monitored error taxonomy
│       ├── human-approval-gates.md  Trigger conditions, approver role, timeout behavior, audit log requirement
│       ├── agent-architecture.md  Agent roles, tool and permission list per agent, orchestration pattern, least-access check
│       ├── multi-agent-workflow.md  Handoff sequence, shared state, escalation, termination, cost cap
│       ├── prompt-structure.md  Versioned system prompt fields, guardrails, few-shot slots, change log
│       ├── context-management.md  Context sources, token budget, priority order, staleness policy, PII filter
│       ├── red-team-review.md  Entry points, attack scenarios (injection, jailbreak, leak, tool misuse), break-fix log, re-test sign-off
│       └── model-card.md  Intended use and out-of-scope, known limitations citing the eval spec and red-team review, performance with segment variance, data provenance, update policy and contact
├── system/
│   ├── BOOT-PROMPT.md  Master paste-anywhere prompt: installs the operating loop, gate discipline, evidence-first rules, the Conductor mode with state-in-conversation, a compact manifest of every file so the model asks by exact path, and the team of roles into any chat model with no file access assumed
│   └── ROLE-PROMPTS.md  Six labeled, individually copyable blocks: the Conductor, then Discovery Researcher, PRD Writer, Architect, Red Teamer, Program Lead; each block names the repo templates it drives so a chat user can paste file contents on request
├── knowledge, templates cross-links: see section 3
├── skills/
│   ├── conductor/
│   │   ├── SKILL.md  Entry skill for the stage-gated interviewer; the full protocol lives in os/CONDUCTOR.md, the triggering in CLAUDE.md and AGENTS.md
│   │   └── questions/
│   │       ├── README.md  Bank file format and the five-class evidence ladder
│   │       ├── discover.md  Seven core questions, each with evidence class, cross-examination trigger, and target template field
│   │       ├── define.md  Eight core questions, opening with the WHICH-DOCUMENT weight tree
│   │       ├── design.md  Seven core questions, including the twice-asked premortem entry
│   │       ├── build.md  Six core questions against acceptance criteria, edge cases, and the red team
│   │       ├── deliver.md  Six core questions, rollback proven and the gtm-plan set
│   │       └── operate.md  Six core questions, the Gate 1 signal measured and the persist-pivot-sunset decision
│   ├── product-analyst/SKILL.md  DISCOVER and OPERATE research engine: decompose, three-lens search, one evidence note per source with a verbatim quote, named tensions, committed positions, one adversarial pass before handoff
│   ├── ai-prd/SKILL.md  Drafts a PRD for an AI-powered feature using templates/definition/prd.md plus the templates/ai/ overlay; two-field frontmatter per section 3
│   ├── roadmap-builder/SKILL.md  Builds and stress-tests a roadmap from templates/planning/roadmap.md and okrs.md
│   ├── program-premortem/SKILL.md  Runs a premortem against the risk register and dependency register before Gate 3
│   ├── reg-gap-check/SKILL.md  Routes regulated questions into modules/regulated/ and refuses to invent regulator text
│   ├── feedback-synthesis/SKILL.md  Transcripts, tickets, and reviews to weighted themes with source counts and contradictions, landed in the discovery templates
│   ├── product-review/SKILL.md  The weekly WIP walk: 48-hour pre-read, per-team 20-minute walk across pre-build, in-progress, and post-build work, decisions landed in the decision log same day
│   └── escalation/SKILL.md  The stuck-decision brief (Situation, Impact, Urgency, Options, Recommendation, Ask) and the routing ladder with SLAs; outcomes feed the risk register and decision log
├── agents/
│   ├── research-agent.md  Instruction file: gathers evidence, cites sources, never asserts beyond them; feeds discovery templates
│   ├── drafting-agent.md  Instruction file: fills one named template per run, marks every unknown as an open field, never invents numbers
│   ├── validation-agent.md  Instruction file: checks a draft against its template's required fields and its stage gate; reports misses, does not rewrite
│   ├── red-team-agent.md  Instruction file: attacks a draft the way a hostile stakeholder or attacker would, using templates/ai/red-team-review.md when the product contains a model
│   └── hermes-agent.md  Hermes-compatible skill file: two-field frontmatter, request routing table, non-negotiable invariants, key facts, escalation; routes Hermes task types onto this repo's tiers and templates
├── routing/
│   ├── omniroute.config.json  Tiered config: extraction -> auto/cheap, drafting -> auto/coding, judgment -> auto/reasoning:pro; baseUrl from OMNIROUTE_BASE_URL, key from OMNIROUTE_API_KEY
│   └── README.md  OmniRoute setup (npm install -g omniroute, dashboard at localhost:20128), the OpenAI-compatible endpoint contract, tier doctrine (which pipeline work goes to which tier and why), the Conductor's per-stage tier table, fixed-fallback combo recipe, and the litellm note for Hermes users
├── modules/
│   └── regulated/
│       ├── README.md  Names the standalone regulated-ai-prd repository as the canonical source, states the byte-exact policy, explains when this overlay activates
│       ├── SKILL.md                 (COPY)  Verbatim from the source repo; its relative paths to templates/, examples/, lint.py resolve inside this directory
│       ├── lint.py                  (COPY)  Verbatim module gate, kept runnable in place
│       ├── test_lint.py             (COPY)  Verbatim module tests
│       ├── templates/
│       │   └── regulated-ai-prd-template.md   (COPY, byte-exact)  The verified regulated PRD template; never reworded here
│       └── examples/
│           └── dispute-summary/
│               └── PRD.md           (COPY, byte-exact)  The verified worked example; never reworded here
├── learn/
│   ├── INDEX.md  Path picker, step anatomy (Read/Study/Do/Done when), the checkbox-ledger convention, tutor mode entry
│   ├── library.md  Book and podcast pointers in own words with named attribution; cards and index entries linked where they exist
│   ├── path-foundations.md  Six steps plus a Gate 1 capstone on Streakline, a fictional habit tracker
│   ├── path-transitioning.md  Seven steps plus a Gate 2 capstone on Restow, a fictional returns portal
│   ├── path-senior.md  Six steps plus a Gate 6 capstone on Meterly, fictional API usage metering
│   ├── skills/tutor/SKILL.md  Tutor mode: quizzes from the Conductor's banks read-only, one push then a model answer, 0/1/2 scoring on the evidence ladder
│   └── products/README.md  Practice workspace convention mirroring os/PRODUCT-WORKSPACE.md; invented evidence labeled, real work stays in products/
└── examples/
    ├── README.md  Index of worked examples and how each was produced with the templates
    ├── expense-copilot-discovery.md  templates/discovery/discovery-document.md filled in for a fictional expense-report copilot
    ├── expense-copilot-prd.md  templates/definition/prd.md filled in for the same fictional product, cross-referencing the discovery doc, with the trade-offs accepted at Gate 2 left visible
    ├── checkout-modernization-brownfield.md  The templates attached mid-flight to a live legacy checkout: a reconstructed Gate 1 labeled as such, a coupling written into the data model, and one decision reversed with both log entries kept
    └── conductor-transcript.md  A fictional interview across two stages: one full cross-examination shown push by push, and one advance refused at a gate
```

## 3. Cross-link conventions

1. All links are relative repo paths (`../knowledge/rice-prioritization.md`), never absolute, never external for internal content. Lint resolves every one.
2. Every template opens with a three-line header block: `Stage:` (the loop stage and gate it feeds), `Knowledge:` (link to the card or index entry behind it), `Skill:` (link to the skill or agent that drives it, or "manual" where none applies).
3. Every method card in `knowledge/` carries a `Skip it when` line between its uses and its trap, and ends with a `Used by:` list linking the templates that draw on it. The consolidated cards under `knowledge/roles/` and `knowledge/domains/` are a different genre and use their own field lists, stated in their INDEX files; the domain cards state their skip condition once, in `knowledge/domains/INDEX.md`.
4. Every SKILL.md uses exactly two frontmatter fields, `name` and `description`, where the description contains an explicit "Use when" clause; triggering is external (CLAUDE.md and AGENTS.md map triggers to skills).
5. `system/` prompts cannot assume file access, so they reference repo paths as things the human pastes on request: "ask the user to paste templates/definition/prd.md". Every path named in a system prompt must exist; lint checks this.
6. CLAUDE.md contains no content of its own beyond the router table; AGENTS.md is the single source of truth for agent behavior, mirroring the pattern OmniRoute itself uses at its root.
7. The regulated module is linked into the loop at Gate 2 and Gate 5 via `os/STAGE-GATES.md`, but files under `modules/regulated/` are never linked as editable; the module README states the byte-exact policy.
8. The delete-unused-sections rule and the fill-these-fields-first guidance are stated once for the whole tree in `os/WHICH-DOCUMENT.md`, and repeated inside the guidance comment of the templates where the pull to fill every field is strongest: `templates/definition/prd.md`, `templates/definition/one-pager.md`, `templates/discovery/competitive-analysis.md`, and `templates/planning/first-90-days.md`. A superset template with no instruction to cut becomes a form nobody trims.
9. Filled artifacts never live in this tree. `products/` is the reserved name for the per-product workspace defined in `os/PRODUCT-WORKSPACE.md`, and no directory by that name will ever ship here, so a user's work inside a clone cannot collide with an update.

## 4. lint.py extension spec

Root `lint.py` keeps every original check (heading structure, dash bans, banned metric literals, TBD/TODO bans, as-of date freshness, review-gate boxes, section-0 and eval-table completeness in PRD mode) and adds an OS tree mode, still Python stdlib only, runnable as `python3 lint.py --os` from the repo root. Tree mode checks, over every tracked `.md` and `.json` file outside `modules/regulated/`:

1. Character gate: no em dash, en dash, horizontal bar, or minus sign codepoints anywhere.
2. Metric gate: none of the six banned metric literals in any file; the authoritative list lives inside lint.py's BANNED_METRICS constant, inherited unchanged from the source repo's lint, and is never written out in prose anywhere in this repo.
3. Placeholder gate: no TBD, TODO, FIXME, XXX outside a template's explicitly marked fill-in fields (angle-bracket fields are the sanctioned placeholder form).
4. Link gate: every relative link resolves to a file that exists; no absolute local paths anywhere.
5. Header gate: every file under `templates/` carries the three-line Stage/Knowledge/Skill header from section 3.
6. Frontmatter gate: every SKILL.md has exactly `name` and `description` and nothing else.
7. Integrity gate: sha256 of the two byte-exact files matches the pinned hashes recorded at copy time; any drift fails the build.
8. Path gate: every repo path named inside `system/` prompt files exists in the tree.
9. Secret gate: no strings matching common key patterns (AKIA, sk-, ghp_, BEGIN PRIVATE KEY).

`modules/regulated/` is exempt from tree mode (its own verbatim lint.py governs it) except for check 7, which is the whole point. `test_lint.py` gains a unit test per added check, including one fixture that must fail per gate. CI or a pre-push hook runs `python3 -m unittest test_lint` then `python3 lint.py --os`; both must pass before the repo is pushed.
