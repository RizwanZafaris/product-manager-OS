# Templates: the full catalog

Stage: every stage of the loop, plus the two tracks that run across it
Knowledge: [knowledge index](../knowledge/README.md)
Skill: [the Conductor](../skills/conductor/SKILL.md) fills these by interview; individual templates name their own driver

A template is the blank a stage produces and a gate reads. Every one opens with the same three-line header this page carries, naming the stage it serves and the gate it feeds, the knowledge card behind it, and the skill or agent that drives it, so a copy you fill in still knows where it came from and which checklist will judge it. Nothing here needs a model: the blanks are fields, the gates are checklists, and a pencil finishes the job. Before some of these blanks get filled, a worksheet in [frameworks/](../frameworks/README.md) has often done the arithmetic that lands in them, the reconciled TAM/SAM/SOM a business case argues from, the RICE score a roadmap sequences by.

Eight directories, 98 templates. Six carry stage work: `discovery` and `definition` sit under DISCOVER and DEFINE, `architecture` holds the DESIGN artifacts while `execution` holds the registers and logs that open early and stay open, `delivery` carries BUILD through DELIVER, and `operate` closes the loop at Gate 6. The last two, `planning` and `ai`, are the tracks that run across every stage rather than inside one. The stage definitions are in [os/OPERATING-LOOP.md](../os/OPERATING-LOOP.md); the checklists these feed are in [os/STAGE-GATES.md](../os/STAGE-GATES.md).

## discovery (16 templates)

DISCOVER, feeding Gate 1: problem worth solving. A no-go here is a success, because it cost a week rather than a quarter.

| Template | What it is | Reach for it when |
|---|---|---|
| [discovery-document.md](discovery/discovery-document.md) | The one-page record of why this work exists: trigger, target user, pain, hypothesis, success signal, go or no-go | A trigger arrived and nothing is written down yet. It rolls up the rest of the stage |
| [problem-framing.md](discovery/problem-framing.md) | One problem statement, its evidence, the cost of inaction, one owner | The exploration is done and a sponsor needs a single fundable statement |
| [user-research-plan.md](discovery/user-research-plan.md) | Questions, method, screener, script, notes, and synthesis themes in one file | Before you talk to anyone, so evidence never separates from method |
| [interview-guide.md](discovery/interview-guide.md) | The interviewer's question blocks, one per research question, with the rule that turns "would you" into something a real behavior can answer | Before the first session of a study, so the guide cannot drift into pitching mid-interview |
| [interview-notes.md](discovery/interview-notes.md) | One session's raw record, tagged live: facts about past behavior kept apart from compliments and hypotheticals | Every interview session, filled while the tone is still fresh, feeding the synthesis and the evidence note |
| [survey-design.md](discovery/survey-design.md) | The analysis plan written before the first response: which question answers which research question, cut how, and what result changes which decision | Interviews have already said which questions to ask, and a how-many question needs an honest count rather than a rushed poll |
| [usability-test-plan.md](discovery/usability-test-plan.md) | Tasks with a success definition, a script, a severity scale, and the findings, run against a design rather than a problem | A prototype or a live flow needs to earn its confidence from someone trying to use it, not from a walkthrough |
| [discovery-synthesis.md](discovery/discovery-synthesis.md) | Research question, themes with verbatim quotes, confidence, implications | The interview notes exist and the synthesis does not |
| [personas.md](discovery/personas.md) | Archetype fields plus a mandatory evidence section: five cited interviews, or the persona is marked assumption | Who you are building for is being asserted from memory rather than from interviews |
| [journey-map.md](discovery/journey-map.md) | One persona, one job, end to end: stages, actions, emotions, current versus future, opportunity areas | The pain is real and you need to know where in the flow it lands |
| [jtbd-spec.md](discovery/jtbd-spec.md) | Job statement, the four forces, tools hired and fired, switch barriers | The real competition is not the category you assumed, and the job has to say so |
| [opportunity-assessment.md](discovery/opportunity-assessment.md) | Cagan's ten questions as a go or no-go before an idea earns discovery time | An idea arrives with sponsorship attached and someone has to test whether it deserves a stage |
| [opportunity-solution-tree.md](discovery/opportunity-solution-tree.md) | Torres's tree as diffable tables: outcome, evidence-cited opportunity branches, solutions, assumption tests, this week's test | Discovery runs weekly and the work needs to hang off one outcome instead of a backlog |
| [competitive-analysis.md](discovery/competitive-analysis.md) | Decision-to-inform as the one mandatory field, the job and its current alternatives, dated evidence per claim | A specific decision turns on what a rival does. Never as a survey, or it becomes a scrapbook |
| [service-blueprint.md](discovery/service-blueprint.md) | One scenario across frontstage, backstage, and support systems, with line-of-visibility failure points, each owned | The product is a service and the failure happens behind the counter |
| [evidence-note.md](discovery/evidence-note.md) | One note per source: claim, verbatim load-bearing quote, source, dates, confidence | Any claim is about to enter a template and would not survive the question "says who" |

## definition (10 templates)

DEFINE, feeding Gate 2: requirements signed off. Pick the weight before you pick the template; the gate asks the same questions either way.

| Template | What it is | Reach for it when |
|---|---|---|
| [prd.md](definition/prd.md) | Background, objectives, stories, functional scope, success metrics, out of scope, launch criteria. A superset you cut, not a form you complete | Several functions, a quarter or more of work, and a sponsor who signs at Gate 2 |
| [design-brief.md](definition/design-brief.md) | The agreement between product and design on the problem, the users, the constraints, and what done looks like, before any pixels | Design work is starting on a signed PRD and the brief has to exist before the review where the designer hears the real constraint for the first time |
| [one-pager.md](definition/one-pager.md) | The light DEFINE weight: problem, proposal, scope, one metric plus a guardrail, a not-doing list, up to three acceptance criteria | One squad ships a real user-facing change over a few sprints and one or two stakeholders must not be surprised |
| [brd.md](definition/brd.md) | Business objectives, scope, stakeholders, constraints, ROI, sponsor sign-off | Money is being allocated and the reader is the sponsor, not the squad |
| [frd.md](definition/frd.md) | The PRD's functional scope decomposed into individually testable requirements, with data flows, interfaces, and traceability back to PRD items | The functional detail is load-bearing and the PRD cannot carry it without becoming unreadable |
| [nfr.md](definition/nfr.md) | Latency, availability, scale, security, accessibility, and retention targets, each with a number or a named owner for the number | Before Gate 2, because non-functional requirements are where products quietly fail |
| [business-rules.md](definition/business-rules.md) | Rule ID, statement, trigger, source of truth, exceptions, test traceability | The organization already decided something (eligibility, limits, approvals) and the product must enforce it rather than re-decide it |
| [assumptions-register.md](definition/assumptions-register.md) | Assumption, confidence, validation method, validate-by date | Always, and hardest when you feel too busy for it. It is the most skipped artifact in the field |
| [acceptance-criteria.md](definition/acceptance-criteria.md) | Given, when, then blocks with edge and negative cases and measurable thresholds | A requirement has to be able to fail before anyone builds against it |
| [prfaq.md](definition/prfaq.md) | Mock press release, customer quote, external and internal FAQ, availability | Working backwards from the launch is cheaper than arguing forward from a feature list |

## architecture (11 templates)

DESIGN, feeding Gate 3: architecture and risks reviewed. Alternatives get considered on paper here, while changing your mind is still free.

| Template | What it is | Reach for it when |
|---|---|---|
| [system-design.md](architecture/system-design.md) | Goals, non-goals, diagram, components, alternatives considered, tradeoffs | One system, or one major change to a system: written before code, revised in review, frozen at Gate 3 |
| [solution-architecture.md](architecture/solution-architecture.md) | Context diagram, capability map, integration points, build versus buy rationale | One initiative spans several systems and an executive or a partner team actually has to read it |
| [adr.md](architecture/adr.md) | Nygard's format: numbered title, status, context, decision, consequences. Reversals supersede, never edit | One decision is significant, contested, or expensive to reverse |
| [data-model.md](architecture/data-model.md) | Entities, relationships, keys, a data dictionary, PII classification | Before the migration, because the data model outlives the code that uses it |
| [privacy-impact-assessment.md](architecture/privacy-impact-assessment.md) | The processing description, necessity and proportionality questions, risks to the individuals whose data it is, and the mitigations, structured but never answered here | A regulator or data-protection regime is in scope, or the design profiles people or applies a model to personal data |
| [api-contract.md](architecture/api-contract.md) | Endpoint, schema, auth, errors, versioning, and a worked OpenAPI-style micro-example | Consumers you will never meet will build against exactly what is written here |
| [sequence-diagram.md](architecture/sequence-diagram.md) | A Mermaid skeleton with sync, async, and error-path conventions | A flow crosses a system boundary, or holds money, data, or a user in suspense |
| [integrations.md](architecture/integrations.md) | System, direction, protocol, auth, SLA, owner, and failure behavior for every line that crosses a boundary | The counterparty can change under you and nobody has written down who watches for it |
| [security-architecture.md](architecture/security-architecture.md) | A STRIDE walk per component: trust boundaries, risk score, mitigation owner | Before Gate 3, and again whenever a trust boundary moves |
| [accessibility-checklist.md](architecture/accessibility-checklist.md) | A component-by-component walk against the WCAG guideline families at the conformance level the NFR already set, each check carrying evidence a skeptic could open | Before Gate 3, and again at Gate 4 once the evidence column can be filled from a real keyboard and screen-reader pass |
| [observability.md](architecture/observability.md) | SLOs, logs, traces, alert thresholds, dashboard owner, a synthetic failure check | Deciding what "working" means while you can still instrument for it |

## execution (10 templates)

These open early and are never finished. The stakeholder map is first required at Gate 2, the risk and dependency registers open at DESIGN and are governed weekly through DELIVER, and the decision log and STATE.md run for the life of the product.

| Template | What it is | Reach for it when |
|---|---|---|
| [stakeholder-map.md](execution/stakeholder-map.md) | Name, interest, influence, RACI tag, cadence, concerns | Built early, revisited at every gate. The stakeholder who sinks a launch is the one nobody mapped |
| [risk-register.md](execution/risk-register.md) | Risk, likelihood, impact, score, mitigation, owner, review date | Kept live from DESIGN through DELIVER, with a premortem pass before Gate 3 |
| [decision-log.md](execution/decision-log.md) | Numbered decisions with context, options, rationale, decider | Continuously. It answers "why did we do it this way" without costing a meeting |
| [dependency-register.md](execution/dependency-register.md) | Dependency, owning team, needed-by date, status, escalation contact | Work sits on someone else's backlog under someone else's priorities. Governed weekly, not at kickoff only |
| [state.md](execution/state.md) | The STATE.md blank: position, accepted answers, open challenges, evidence ledger, journal | Any session, in any runtime, has to pick up where the last one stopped |
| [status-report.md](execution/status-report.md) | The weekly written record of where work stands against plan, colored on one rule: green needs evidence, amber needs a date, red needs a decision | Every week from Gate 3 onward, so a report is never green out of habit until the week it turns red |
| [change-request.md](execution/change-request.md) | One change to a signed baseline: what it does to scope, schedule, cost, and risk, and who approves it before the baseline moves | Scope, a committed date, budget, or a non-functional target changes after Gate 2, never before the approval is recorded |
| [tech-debt-register.md](execution/tech-debt-register.md) | A ledger with an interest rate: what each item costs the team every quarter it stands against what it costs once to remove | Debt is contested at every planning meeting and nobody can say what it actually costs to carry |
| [retrospective.md](execution/retrospective.md) | One format's worth of what happened, kept blameless, ending in two or three actions with owners | The end of a cycle or a gate, where the alternative is skipping straight to the next one and repeating the same miss |
| [hiring-scorecard.md](execution/hiring-scorecard.md) | The outcomes a seat must move, competencies with what strong and weak evidence sound like, a structured loop, and a decision made on evidence rows | A PM req opens, written before any candidate exists so the rubric cannot be built around a favorite |

## delivery (13 templates)

BUILD into DELIVER, feeding Gate 4: acceptance criteria met, and Gate 5: release readiness green.

| Template | What it is | Reach for it when |
|---|---|---|
| [testing-strategy.md](delivery/testing-strategy.md) | Test levels, coverage targets, environments, entry and exit criteria | BUILD is starting and "we will test it" is the whole plan so far |
| [edge-cases.md](delivery/edge-cases.md) | Case, trigger, expected behavior, linked test ID, with no case left undecided | The happy path is what the team builds by instinct. This register is where the product earns its keep |
| [failure-scenarios.md](delivery/failure-scenarios.md) | Scenario, blast radius, detection, recovery, data-loss risk | The worry is not bad input but the system around the product breaking |
| [uat-plan.md](delivery/uat-plan.md) | Scope, entry and exit criteria, testers, defect severity, a sign-off form | Real users have to confirm it works for their actual job before Gate 5 |
| [release-readiness.md](delivery/release-readiness.md) | The go or no-go checklist: features, tests, known issues, rollback, comms, sign-offs per function | Always. This file is Gate 5, and it is opened before the launch meeting, not during it |
| [release-notes.md](delivery/release-notes.md) | One set of facts about what changed, cut three ways for three readers: customers, internal teams, and support | A release ships and each audience needs a different cut of the same facts rather than three separately negotiated stories |
| [migration-cutover-plan.md](delivery/migration-cutover-plan.md) | The phased sequence, the rehearsals that prove it, the rollback and where it stops being possible, and the reconciliation that proves nothing was lost | The release moves data, traffic, or customers from one system to another and has a point of no return in it |
| [sla-slo-definition.md](delivery/sla-slo-definition.md) | The SLI measured from the user's side, the SLO the team commits to and alerts on, and the SLA promised externally, kept deliberately looser than the SLO | Before first production traffic, so an error-budget breach becomes a policy decision instead of a surprised customer credit |
| [support-runbook.md](delivery/support-runbook.md) | The symptom table, diagnosis, workaround, and escalation path, written from what the customer says rather than what the system does | A support agent is about to take a call on a new feature and needs a script that starts from the complaint, not the architecture |
| [analytics-instrumentation-spec.md](delivery/analytics-instrumentation-spec.md) | Event taxonomy, properties, owners, QA plan | During DESIGN, before build starts: the metrics a PRD names are only measurable if the events exist |
| [launch-comms-plan.md](delivery/launch-comms-plan.md) | Audiences, channel and timeline, messaging per audience, rollback comms | More than two audiences have to hear different things on launch day |
| [customer-comms.md](delivery/customer-comms.md) | The messages themselves, per channel, with the approval chain each one passed through and Minto's situation, complication, resolution spine underneath | The launch comms plan has said who hears when, and now the actual words have to exist and get approved before send |
| [sales-enablement-one-pager.md](delivery/sales-enablement-one-pager.md) | A one-page derivative of positioning, the GTM plan, and pricing, with a proof point behind every claim, sized for reading between calls | A rep needs to talk about a new release before support tickets and forum posts become the only training material |

## operate (12 templates)

OPERATE, feeding Gate 6: outcomes verified, learn or sunset. Skipping this stage is how zombie products are born.

| Template | What it is | Reach for it when |
|---|---|---|
| [operational-readiness-review.md](operate/operational-readiness-review.md) | Runbooks, on-call, backup and recovery, blast radius, and checks derived from past incidents | Before first production traffic. Release readiness asks whether you can ship it; this asks whether you can run it at 3 a.m. with the author on vacation |
| [metrics-dictionary.md](operate/metrics-dictionary.md) | One row per metric anyone reports, defined precisely enough that two people computing it get the same number | A dashboard tile or a metrics review cites a number nobody can trace back to an agreed formula |
| [dashboard-spec.md](operate/dashboard-spec.md) | Who looks at it, what questions it must answer, which metric id each tile shows, and where each tile drills to. No metric is defined here | A dashboard is being built, or has decayed into a wall of tiles that answers no question anyone actually asked |
| [metrics-review.md](operate/metrics-review.md) | Outcome versus target per key result, input-metric movement, and the decision: persist, pivot, or sunset | On a fixed cadence after launch. This is the review the loop exists for |
| [post-launch-review.md](operate/post-launch-review.md) | Goal versus actual for one launch, run once per launch | A launch has landed and the question is what that launch did, not how the product is doing |
| [experiment-brief.md](operate/experiment-brief.md) | Hypothesis, target metric, variants, sample size and duration, decision rule | One experiment, with the decision rule written before it runs |
| [incident-postmortem.md](operate/incident-postmortem.md) | Facts, severity, timeline, quantified impact, systems-language causes carrying no names, corrective actions with owner and verification | Once per qualifying incident, to make the same incident impossible rather than to find someone to be disappointed in |
| [compliance-impact-assessment.md](operate/compliance-impact-assessment.md) | Applicable regulations, data categories, DPIA flag, retention, legal sign-off | A regulator or a data-protection regime is in scope. It asks the questions and never supplies the answers |
| [feedback-program.md](operate/feedback-program.md) | The charter for a standing program (advisory board, beta, panel): the decision it informs, recruiting, cadence, terms, intake, and the program's own exit criteria | Feedback should arrive on a cadence instead of by accident |
| [win-loss-review.md](operate/win-loss-review.md) | Outcome, primary and secondary reasons, competitor, quotes, action items | Per meaningful win, loss, or no-decision, because the CRM dropdown always says "price" |
| [qbr-board-update.md](operate/qbr-board-update.md) | Metrics versus goal, wins, risks and asks, next-quarter roadmap, decisions needed | Leadership has to act on the numbers, not applaud them |
| [sunset-eol-plan.md](operate/sunset-eol-plan.md) | EOL rationale, timeline, migration path, comms cascade, decommission steps | Gate 6 returned SUNSET. A shutdown is a launch in reverse and gets the same discipline |

## planning (16 templates)

The PLANNING track. Most of these feed every stage and are reviewed on their own cadence rather than at a gate. The GTM plan and the growth plan are the exceptions: they are written at DELIVER and OPERATE and feed Gate 5 and Gate 6.

| Template | What it is | Reach for it when |
|---|---|---|
| [business-case.md](planning/business-case.md) | Options compared in money over time, with sensitivities, recommending one and labeling every number ILLUSTRATIVE until finance agrees the method | Money or headcount is being allocated across years and a sponsor needs the alternatives priced, not just the winner |
| [roadmap.md](planning/roadmap.md) | Now, Next, Later horizons with theme, initiative, target period, confidence, dependencies, status, and an expectations-not-commitments preamble | Deciding which products enter the loop and roughly when |
| [okrs.md](planning/okrs.md) | An objective with three to five key results, each carrying a baseline and a target, plus a scoring cadence | The targets Gate 6 will verify have to exist before the work starts |
| [vision.md](planning/vision.md) | Future-state narrative, why now, who for, north-star tie-in, non-goals | A team needs a shared picture concrete enough to decide with when you are not in the room |
| [product-strategy.md](planning/product-strategy.md) | Strategic context, where-to-play bets, differentiation, sequencing, key risks | Choice under constraint has to be written down. A goals slide is not a strategy |
| [north-star-metric.md](planning/north-star-metric.md) | The metric definition, an input-metric tree with owners, guardrails, review cadence | Choosing and then defending the one metric that expresses delivered customer value |
| [positioning.md](planning/positioning.md) | Dunford's chain: competitive alternatives, unique attributes, value and proof, target customer, market category | Before the GTM plan, because positioning decides who the launch is aimed at |
| [pricing-packaging.md](planning/pricing-packaging.md) | Pricing model, tiers, value metric, competitive benchmark, discount rules, owner | Pricing ships like a feature and reverses like a migration, so it gets a document and a review date |
| [gtm-plan.md](planning/gtm-plan.md) | First cohort and channel with evidence the channel reaches them, positioning against the named alternative, launch sequence, the one launch metric, the stop condition | At DELIVER. The release checklist proves you can ship; this answers who meets it first, and why them |
| [growth-plan.md](planning/growth-plan.md) | The input-metric bet, the cheapest experiment that would move it, the loop or channel behind it, the counter-metric, the kill condition | At OPERATE, one bet at a time, with the evidence attached |
| [first-90-days.md](planning/first-90-days.md) | The mandate in the hirer's words, three learning questions, 30, 60, and 90 day blocks, one commitment that can fail, first meetings that feed the stakeholder map | Taking over a product, whether it is new or already in flight |
| [partner-integration-brief.md](planning/partner-integration-brief.md) | One lean go or no-go per partnership: the exchange, the evidenced user problem, the integration surface with owners on both sides, commercial shape and exit terms | Someone proposes building on a partner and the open question is yes or no, not how |
| [program-charter.md](planning/program-charter.md) | The one-page agreement on what a program exists to change, who decides what, and how it is run, signed once and re-read at every gate | Several initiatives share one outcome, one sponsor, and one cadence, and "who can change scope" would otherwise get re-argued in month three |
| [capacity-plan.md](planning/capacity-plan.md) | Supply of team time set against the roadmap's demand, so Now holds only what the team can carry and Next stays honest | A roadmap gets signed without anyone having checked whether the team sizing it can actually staff it |
| [decision-memo.md](planning/decision-memo.md) | One decision stated as a question, options priced with the door type named, one recommendation, and the dissent on the record | A question has been debated twice by the same people, or a reversible call is getting one-way-door treatment |
| [exec-update.md](planning/exec-update.md) | The one-page monthly read for whoever funds and unblocks the work, ending in asks rather than activity | A decision is needed from a room this week and the honest answer to "where are we" is longer than a sentence |

## ai (10 templates)

The AI OVERLAY, active whenever the product itself contains a model. It attaches to DEFINE and DESIGN, and its thresholds become blocking checks at Gate 4 and Gate 5.

| Template | What it is | Reach for it when |
|---|---|---|
| [eval-spec.md](ai/eval-spec.md) | Scenario set, golden dataset, metrics, pass threshold, and the gate that blocks on failure | The product contains a model. This is what turns "it should work well" into something that can stop a release |
| [guardrails.md](ai/guardrails.md) | Input and output constraints, blocked behaviors, an enforcement point and an owner per rail | "Human in the loop for sensitive cases" needs a trigger, a test, and a name attached |
| [hallucination-controls.md](ai/hallucination-controls.md) | Grounding source, abstain policy, verifier step, monitored error taxonomy | The model asserts with equal confidence whether it knows or not |
| [human-approval-gates.md](ai/human-approval-gates.md) | Trigger conditions, approver role, timeout behavior, audit-log requirement | An action must wait for a named human, and the gate must not quietly approve on silence |
| [prompt-structure.md](ai/prompt-structure.md) | Versioned system-prompt fields, guardrails, few-shot slots, a change log | The system prompt is production code that happens to be prose |
| [context-management.md](ai/context-management.md) | Context sources, token budget, priority order, staleness policy, PII filter | Deciding on purpose what the model sees at inference time, instead of leaving it to nobody |
| [agent-architecture.md](ai/agent-architecture.md) | Agent roles, a tool and permission list per agent, orchestration pattern, least-access check | The model takes actions, and tools are permissions |
| [multi-agent-workflow.md](ai/multi-agent-workflow.md) | Handoff sequence, shared state, escalation, termination, cost cap | Two or more agents cooperate on one task |
| [red-team-review.md](ai/red-team-review.md) | Entry points, attack scenarios (injection, jailbreak, leak, tool misuse), a break-fix log, re-test sign-off | Before Gate 5, or whenever the feature has only been read by people who want it to succeed |
| [model-card.md](ai/model-card.md) | Intended use and explicit out-of-scope uses, known limitations citing the eval spec and red-team review, performance with segment variance, data provenance, update policy and contact | Someone outside the building team needs to know what this is, what it is for, and where it breaks |

## Which of these do you actually need

Most teams own one PRD template and use it for everything, so a two-day change gets twelve sections and a two-quarter bet gets the same twelve. The weight is a choice, and [os/WHICH-DOCUMENT.md](../os/WHICH-DOCUMENT.md) makes it an explicit one: three questions (stakes, audience, reversibility) pick one of five weights, from a logged decision through a ticket, a one-pager, a full PRD, and the BRD, PRD, FRD stack. Read that file before copying anything out of this directory. Then delete every section of the copy you do not need: an empty section is worse than no section, because it reads as an unanswered question and it teaches the next reader to skim.

Where the filled copies live is a separate question with its own answer, in [os/PRODUCT-WORKSPACE.md](../os/PRODUCT-WORKSPACE.md). Filled artifacts never live in this tree.
