---
layer: os
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Stage Gates", "STAGE-GATES"]
---
# Stage Gates

Six gates, one per stage of the loop in [OPERATING-LOOP.md](OPERATING-LOOP.md). Each gate is a fill-in form: copy the gate's section into your product workspace, complete every field, tick only the boxes that are honestly true, and collect the signatures. A gate passes when the form is complete and signed, not when the meeting ends.

<!-- Conventions for every gate below:
     - Angle-bracket fields <like this> are the blanks you fill.
     - Boxes are ticked by the humans named on the sign-off lines, never by an agent.
     - "Evidence" always means a document or artifact you can point at, not a recollection.
     - A failed gate is a normal outcome. Record the misses, assign owners, re-run.       -->

## How to mark a line

Three marks, not two. **Pass** means the evidence exists and someone at the gate has seen it. **Fail** means the evidence contradicts the line. **Unknown** means nobody can produce the evidence right now, and it blocks exactly as a fail does, because the two are indistinguishable from the outside: a line nobody can evidence and a line that is false produce the same launch review. Teams that allow only pass and fail generate silent passes, and the tell is a gate form where every line is ticked and at least one has no evidence written beside it.

Write the evidence next to the mark as a path and a section, never as a name. "Marcus confirmed" is a recollection and will not survive the quarter; `definition/nfr.md` section 4, row NFR-04 will. This is the same discipline the Conductor's landing protocol enforces in [CONDUCTOR.md](CONDUCTOR.md), and it applies whether or not anyone is running the Conductor.

Each gate below closes with two things beyond its checklist: the skip warning, which is what the field has learned about skipping that gate, and **failure precedents**, which are the specific ways this gate gets failed or falsely passed, each with the tell that reveals it on the page. Read the precedents before you chair the gate, not after.

---

## Gate 1: Problem worth solving

Closes DISCOVER. Feeds DEFINE.

**Product:** <name> · **Gate run date:** <YYYY-MM-DD> · **Attempt:** <1, 2, ...>

**Inputs on the table:** completed `../templates/discovery/discovery-document.md`, plus the research artifacts it rolls up (problem framing, research plan and notes, personas, journey map).

- [ ] The problem statement is one sentence, and everyone at the gate states it the same way
- [ ] Evidence comes from at least five real user conversations or equivalent primary data, cited in the discovery document by source
- [ ] Personas built on fewer than five cited interviews are explicitly marked as assumptions
- [ ] The cost of inaction is written down: what it costs, whom, per what period, with the calculation shown
- [ ] At least one plausible reason to say no-go was seriously argued at this gate
- [ ] A domain was selected from `../knowledge/domains/README.md` or "none" was recorded, either way in STATE.md
- [ ] The success signal for a future Gate 6 is named now, before any solution exists
- [ ] Go or no-go is recorded below, with the deciding rationale in one paragraph

**Decision:** GO / NO-GO / MORE DISCOVERY, because: <one paragraph>

| Sign-off | Name | Date |
|---|---|---|
| Product owner | <name> | <date> |
| Sponsor or lead who can stop this | <name> | <date> |

> **If you skip this gate:** the field's most common postmortem finding is a team that discovers in beta that nobody has the problem, after the expensive stages are already paid for. Products regularly die of "no market need" as diagnosed after launch; this gate is where that diagnosis is cheap. A no-go here costs a week.

**Failure precedents.**

1. **The solution-shaped problem statement.** The statement names the absence of the planned feature: "owners lack a cash-flow forecast". Tell: delete the proposed solution from the sentence and nothing is left describing a person's day. Rewrite until the statement is true even if you build something else entirely, because a problem statement that only one solution can satisfy has already skipped DEFINE.
2. **Five conversations, one source.** The evidence line reads five interviews, and all five came from the same customer-success manager's favorite accounts. Tell: the source column has five rows and one recruiter. Independence is the property being counted, not headcount. A sixth interview from the same channel adds confidence in the channel, not in the problem.
3. **The unarguable no-go.** Someone says "we considered not doing this" and the line gets ticked. Tell: the gate attempt contains no sentence describing what the no-go option actually was. A real no-go argument names a cheaper alternative and loses on cited evidence; file the exchange, because the next person needs to see the fork, not the conclusion.
4. **The success signal chosen as usage.** "Owners open the forecast weekly" ticks the line and predicts nothing, because a product can be opened and change no behavior. Tell: the signal can be satisfied without anyone's situation improving. Push until the signal names an action, a decision, or an outcome outside the product.
5. **The cost of inaction as a single number.** A figure arrives with no arithmetic and the room either believes it or resents it. Tell: no multiplier, period, or population appears anywhere near the number. Shown arithmetic can be argued with, and an estimate nobody can argue with is an estimate nobody owns.

**Most common false pass:** a beautifully evidenced discovery document about a real problem that the company has no mandate to solve. The checklist does not ask about mandate; the planning overlay does. If no roadmap row and no key result connect to this problem, the honest outcome is MORE DISCOVERY with a different question, or a conversation with the sponsor instead of a gate.

---

## Gate 2: Requirements signed off

Closes DEFINE. Feeds DESIGN.

**Product:** <name> · **Gate run date:** <YYYY-MM-DD> · **Attempt:** <n>

**Inputs on the table:** the definition set at the weight chosen in [WHICH-DOCUMENT.md](WHICH-DOCUMENT.md). At full weight that is the completed BRD, PRD, FRD, NFR, business rules, assumptions register, and acceptance criteria from `../templates/definition/`. At the lighter weight it is a completed `../templates/definition/one-pager.md` with its acceptance criteria attached. The checklist below is the same either way: a lighter document answers these questions in fewer words, not in fewer answers.

- [ ] Every PRD objective traces to the Gate 1 problem statement, and every FRD requirement traces to a PRD item
- [ ] Every acceptance criterion can fail: it has a condition, an expected result, and a measurable threshold
- [ ] Every NFR target is a number, or names the owner who will produce the number by a dated deadline
- [ ] The assumptions register exists, and every assumption carries a confidence, a validation method, and a validate-by date
- [ ] Out-of-scope is written down and the sponsor has read it
- [ ] The sponsor named in the BRD has signed the BRD itself, not just this gate
- [ ] **AI overlay, when the product contains a model:** acceptance criteria for model behavior are eval sets with thresholds per `../templates/ai/eval-spec.md`, not prose
- [ ] **Regulated overlay, when a financial or data regulator applies:** section 0 of `../modules/regulated/templates/regulated-ai-prd-template.md` is answered per market, and its lint gate runs green on the filled document

**Decision:** SIGNED / RETURNED FOR REWORK, because: <one paragraph>

| Sign-off | Name | Date |
|---|---|---|
| Product owner | <name> | <date> |
| Engineering lead | <name> | <date> |
| Business sponsor | <name> | <date> |
| Regulatory owner (regulated products only) | <name or N/A because <reason>> | <date> |

> **If you skip this gate:** requirements defects found after build are the most expensive class of defect there is; decades of software engineering economics agree the cost multiplies with every stage a defect survives. The unsigned assumption is the one that resurfaces in the launch review, and for regulated products, a deferred precondition can resurface with a regulator's reference number attached.

**Failure precedents.**

1. **The adjective in the expected-result field.** "The forecast feels trustworthy", "the flow is intuitive", "performance is acceptable". Tell: read the criteria column looking only for units, and count the rows with none. The repair move that works in the room is one question: what would we see in the product if this were false? The answers are almost always testable, and the criterion becomes two of them. The walkthrough in [HOW-TO-RUN-A-PRODUCT.md](HOW-TO-RUN-A-PRODUCT.md) returns a real gate on exactly this.
2. **The criterion nobody would remove.** Some criteria cannot be made testable and are also not launch-blocking. Tell: it survives three attempts at a threshold and nobody can name what happens if it fails. The correct move is demotion, not decoration: move it to a UAT observation and record the demotion. Kept as an untestable criterion, it teaches readers that criteria are advisory.
3. **The NFR with an owner instead of a number, forever.** The line permits an owner and a date in place of a number, and teams use that as a permanent home. Tell: the same NFR row carries an owner and a date at Gate 2 and again at Gate 4, with the date moved. One deferral is a plan; two is a decision to ship without a target, and it should be made explicitly or not at all.
4. **Traceability that runs one way.** Every FRD requirement points at a PRD item, and three PRD objectives point at nothing being built. Tell: trace backward from the PRD, not forward from the FRD, and count objectives with no requirement under them. Those are either scope the team dropped silently or objectives that were decoration.
5. **The sponsor who signed the gate and not the BRD.** Tell: the BRD's signature block is empty while the gate form is fully signed. The line exists because signing a process commits nobody; signing the business case commits the person whose budget the ROI logic spends.
6. **Prose criteria on model behavior.** "Summaries should be accurate and helpful" passes a room that does not know how to write an eval row. Tell: the AI overlay line is ticked and the eval spec's dataset field is empty, or the eval spec is thorough and two model behaviors were never routed into it. The second version is more common and harder to see, because the artifact exists and looks complete.
7. **Regulated preconditions parked as risks.** A precondition is written into the risk register with an owner and treated as handled. Tell: a risk-register row whose mitigation is "confirm with legal before launch". A constraint on the solution space is not a risk to be scored; it is an answer that must exist before design starts, which is why the overlay hooks here rather than at Gate 5.

**Most common false pass:** a complete, testable, well-traced definition set for the wrong weight. Twelve filled sections on a two-week change pass every line above and cost a week nobody had. The weight question in [WHICH-DOCUMENT.md](WHICH-DOCUMENT.md) is asked before this gate precisely because this gate cannot catch it.

---

## Gate 3: Architecture and risks reviewed

Closes DESIGN. Feeds BUILD.

**Product:** <name> · **Gate run date:** <YYYY-MM-DD> · **Attempt:** <n>

**Inputs on the table:** the `../templates/architecture/` set as applicable (system design, solution architecture, ADRs, data model, API contracts, sequence diagrams, integrations, security architecture, observability), plus the full `../templates/execution/` set (stakeholder map, risk register, decision log, dependency register).

- [ ] The system design lists at least one alternative that was seriously considered and rejected, with the tradeoff recorded as an ADR
- [ ] Every integration names its owner, protocol, SLA, and failure behavior; "we will figure it out" appears nowhere
- [ ] The data model classifies PII, and retention is stated per data class
- [ ] Security architecture walked each component for spoofing, tampering, repudiation, information disclosure, denial of service, and privilege elevation, and every finding has a mitigation owner
- [ ] Observability names the SLOs, the alert thresholds, and who owns the dashboard, before any code exists
- [ ] A premortem ran (see `../skills/program-premortem/SKILL.md`): the team wrote down how this fails, and the risk register absorbed the answers
- [ ] Every risk scoring high on likelihood times impact has a named owner and a review date
- [ ] The dependency register names every team this product waits on, with needed-by dates and escalation contacts
- [ ] **AI overlay:** agent permissions follow least access per `../templates/ai/agent-architecture.md`, and guardrails each have an owner and a test per `../templates/ai/guardrails.md`

**Decision:** REVIEWED AND ACCEPTED / RETURNED, because: <one paragraph>

| Sign-off | Name | Date |
|---|---|---|
| Architect or senior engineer | <name> | <date> |
| Product owner | <name> | <date> |
| Security reviewer | <name> | <date> |

> **If you skip this gate:** the failure pattern is a dependency discovered at integration time, owned by a team that never agreed to your date. Dependency registers reviewed only at kickoff are the classic version: the register was right in January and the world changed in March. The premortem exists because teams reliably know how their project will fail and reliably are not asked.

**Failure precedents.**

1. **The straw alternative.** The rejected option is one nobody would have chosen, so the ADR records a decision that was never in doubt. Tell: the tradeoff paragraph has no cost on the chosen side. Every real architectural choice gives something up; an ADR listing only the loser's flaws is advocacy. The usable form names the condition that would reopen it, which is what lets a successor reverse it intelligently instead of relitigating it from scratch.
2. **The integration with a protocol and no failure behavior.** Tell: the failure-behavior column reads "retry" or is empty. "Retry" is not a behavior, it is a mechanism; the behavior is what the user sees while the retry runs and what the system does when retries are exhausted. Fill that column with a sentence containing a user-visible noun.
3. **The premortem that was performed.** The session happened, the notes exist, and the risk register did not change. Tell: compare the register's row count and modified dates before and after the session. Zero new rows means the room hedged or the facilitator let "might" in; the mechanics that prevent it are on the sheet at `../frameworks/execution/premortem-worksheet.md`. The register was the thing being tested, and it passed by not being touched, which is the wrong pass.
4. **The dependency the other side has not agreed to.** The register names a team, a deliverable, and a needed-by date, and nobody on that team has seen the row. Tell: ask for the thread, ticket, or meeting note where the date was accepted, and notice whether the answer is an artifact or a person's name. A remembered nod in a corridor is a plan for somebody else's quarter, written in your document. This gate is the last cheap moment to convert one, because a dependency confirmed here costs an email and the same dependency discovered at Gate 5 costs the launch date, the other team's quarter having been committed in the meantime. The sibling failure, a register that was accurate at kickoff and never revisited, sits with the stage rather than the gate and is set out under DESIGN in [OPERATING-LOOP.md](OPERATING-LOOP.md); this gate's job is to install the weekly review that catches it.
5. **The high risk owned by a team.** "Platform team" owns the top risk. Tell: an owner column containing a plural noun. A team cannot be paged and cannot be asked why the mitigation slipped; the scoring discipline in `../frameworks/execution/risk-matrix.md` is wasted the moment ownership goes plural.
6. **The stakeholder identified and never invited.** The map correctly flags someone as required at a later gate, and no calendar invitation follows. Tell: a map row naming a gate requirement with no corresponding entry in any meeting, brief, or review before that gate. This is the precedent that produces most Gate 5 no-gos, and it is a follow-through failure rather than an artifact failure, which is why no template catches it.
7. **Threshold set after the first incident.** Tell: the observability doc's alert numbers are blank at this gate with a note to tune them in production. A threshold chosen after an incident is chosen to exclude that incident. Set a wrong number now; a wrong number is revisable evidence, and a blank is not.

**Most common false pass:** an architecture that is correct for the requirements and mute about operations. Every line above can pass while nobody has said who is paged, what the runbook covers, or what support tells a customer on day one. Gate 5 will find it, three months later, at the cost of a launch date.

---

## Gate 4: Acceptance criteria met

Closes BUILD. Feeds DELIVER.

**Product:** <name> · **Gate run date:** <YYYY-MM-DD> · **Attempt:** <n>

**Inputs on the table:** the acceptance criteria from Gate 2, the testing strategy, edge-case table, and failure-scenario table from `../templates/delivery/`, and the test results themselves.

- [ ] Every acceptance criterion from Gate 2 is demonstrated passing, or listed below as a miss with an owner and a decision
- [ ] The edge-case table has no row marked "to be decided"; every case has an expected behavior and a linked test
- [ ] Failure scenarios were exercised: detection fired, recovery worked, data-loss risk matched the write-up
- [ ] Coverage meets the targets the testing strategy set, and the gaps are listed by name, not by percentage alone
- [ ] Scope changes since Gate 2 all appear in the decision log with a decider named
- [ ] **AI overlay:** the eval sets from `../templates/ai/eval-spec.md` ran against the shipping model version, every threshold passed or the miss is escalated below, and the red-team review found no unfixed break rated high

**Misses carried forward:** <list each miss, its owner, and the decision: fix before Gate 5 / accept with rationale>

**Decision:** MET / NOT MET, because: <one paragraph>

| Sign-off | Name | Date |
|---|---|---|
| Engineering lead | <name> | <date> |
| QA owner | <name> | <date> |
| Product owner | <name> | <date> |

> **If you skip this gate:** "code complete" quietly replaces "criteria met", and the difference ships to customers. The edge-case rows nobody decided become production incidents decided by whoever is on call. For model features, an eval suite that was written but never run against the version that ships is the most common way a green spec produces a red launch.

**Failure precedents.**

1. **Demonstrated by the person who built it.** The criterion passes in a walkthrough narrated by its author, on data the author chose. Tell: no name in the evidence column other than the implementer's. Demonstration means someone who could be surprised watched it, which is why QA signs a line of its own rather than co-signing engineering's.
2. **The criterion that quietly stopped parsing.** Scope moved, the built thing is different, and the criterion now describes nothing. Tell: read the acceptance-criteria file against the demo and count rows whose condition cannot be produced in the product at all. Two or more means Gate 2 was amended by nobody. Send those rows back to Gate 2 for an explicit re-signature; it costs one meeting, and the alternative is losing the ability to say what was promised.
3. **The miss without an owner.** "Known limitation" appears in the miss list with no name and no date. Tell: a miss row whose owner column is a team, a quarter, or empty. A miss with an owner and a date is a plan; a miss without one is a discovery someone else makes later, usually a customer.
4. **Coverage as a single percentage.** Tell: the coverage line is one number and the gaps line is absent. The number cannot distinguish untested error paths from untested getters, and the error paths are the whole point. Name the gaps: which failure branches, which edge rows, which integration.
5. **The failure scenario that was reasoned about.** The table describes detection and recovery, and neither was run. Tell: no timestamps, no incident-like artifact, no name of who watched the alert fire. Exercised means something broke on purpose and something else noticed.
6. **The eval suite that only ever passes.** Green every run, size unchanged for months. Tell: the eval set's row count is the same as at Gate 2 and its governance field has no additions. A suite that never absorbs a real failure measures the cases you thought of before you started. Every production miss and every red-team break earns a permanent row.
7. **Eval run against the wrong version.** The suite is green against last week's model or a different prompt revision. Tell: the eval report names no model version and no prompt-change-log entry. This is the precedent the skip warning calls out because it is the most common route from a green spec to a red launch, and it is invisible unless the report carries both identifiers.
8. **Red team as a review of the design.** Someone read the architecture and found nothing. Tell: the red-team write-up cites documents rather than inputs. The breaks that matter come from attacking the built thing with user-supplied text: memo fields, names, uploaded files, anything a customer controls that reaches a prompt or a query.

**Most common false pass:** every criterion met, every test green, and the product is a worse experience than the flows the criteria decompose into. Criteria are per-behavior and cannot see a journey. If nobody at this gate has used the release candidate end to end as a customer would, the gate measured the parts.

---

## Gate 5: Release readiness green

Closes DELIVER. Feeds OPERATE.

**Product:** <name> · **Gate run date:** <YYYY-MM-DD> · **Attempt:** <n>

**Inputs on the table:** UAT results against `../templates/delivery/uat-plan.md`, the completed `../templates/delivery/release-readiness.md`, and the rollback evidence.

**Run of show.** Chair: <the release owner, or a delegate who can say no-go>. Attendees: the sign-off owners below, plus on-call and support leads. Pre-read: the readiness doc and UAT results circulate at least 48 hours ahead, and the gate opens with questions, not a walkthrough; unread pre-reads reschedule the gate. Demo, not slides: every readiness claim is shown in the release candidate itself. Outcomes are GO, NO-GO, or CONDITIONAL GO, and a conditional go without a named owner and close-by date per condition is a no-go wearing a smile.

- [ ] UAT exit criteria are met, with real users or their named proxies, and every severity-1 defect is closed
- [ ] The rollback was actually performed in a pre-production environment, and the time to roll back is recorded
- [ ] Known issues going out with the release are listed in the readiness doc, each with a workaround or an accepted-risk sign-off
- [ ] Comms are drafted and approved: support, sales or field teams, and customers where applicable
- [ ] On-call knows this release is coming, and the runbook for it exists
- [ ] Every function on the readiness checklist signed its own line: engineering, product, QA, support, and any others the readiness doc names
- [ ] **AI overlay:** guardrails verified live in the release candidate; the kill switch was tested, not just designed
- [ ] **Regulated overlay:** the section 0 answers from Gate 2 are still true of the artifact that ships (model version, vendor terms, data residency, disclosures); any drift is written up and re-signed by the regulatory owner

**Decision:** GO / NO-GO / CONDITIONAL GO with <each condition, its owner, and its close-by date>, because: <one paragraph>

| Sign-off | Name | Date |
|---|---|---|
| Release owner | <name> | <date> |
| Product owner | <name> | <date> |
| Operations or support lead | <name> | <date> |
| Regulatory owner (regulated products only) | <name or N/A because <reason>> | <date> |

> **If you skip this gate:** the industry's incident write-ups repeat one line: the rollback plan existed on paper and had never been run. The other repeat offender is the launch support learned about from customers. Both are cheap to prevent here and expensive to explain later.

**Failure precedents.**

1. **Severities negotiated after testing.** Every defect the team wants to ship past becomes a severity 3, and "all severity-1 defects closed" self-certifies. Tell: the severity definitions carry a later date than the first test session. Agree the definitions before the first session, in one sentence each, and the hard defect classifies itself.
2. **The rollback in the future tense.** Tell: the readiness doc's rollback section contains "we would" or "we can" and no timestamp. A rehearsed rollback reads like a log entry, with an elapsed time and a date. The rehearsal is also where the ugly states surface, the empty panel and the half-migrated row, which no amount of planning produces on paper.
3. **The kill switch that takes the product with it.** A single flag disables the feature and its host surface together, so using it is a bigger outage than the bug. Tell: one switch named in the readiness doc where the failure modes are independent. Test the granularity, not just the mechanism.
4. **Support comms written by the people who will not answer the tickets.** Approved, accurate, and useless at the desk. Tell: the comms approver and the on-call ticket queue owner are different people and the second one never commented. Have the answerer rewrite it; the rewrite is short and it is the actual test of whether the feature is explainable.
5. **The conditional go with an unbudgeted owner.** A condition is assigned to someone who has no time in the release week, which converts the condition into a formality. Tell: a condition whose owner is not in the room, or whose close-by date is the release date. If the condition genuinely gates the release, record NO-GO; a three-day delay is recoverable and a formality is not.
6. **UAT with proxies who are colleagues.** "Real users or named proxies" is read as anyone outside the team. Tell: the participant list is all internal and the proxy rationale is missing. An internal proxy is legitimate when the doc names whom they proxy for and why, and illegitimate when it is a convenience.
7. **Overlay drift nobody re-checked.** The model version changed during BUILD, or the vendor updated terms, and the Gate 2 section 0 answers now describe a different artifact. Tell: the regulated line is ticked with no diff, no date, and no regulatory signature since Gate 2. What was promised at DEFINE must be true of the thing that ships, and the only way to know is a comparison someone performed.

**Most common false pass:** a fully signed readiness doc for a release nobody can observe. Every function signs, the rollback is timed, comms are out, and the dashboards and alerts arrive next sprint. That release is live and unmeasurable, which means Gate 6 will compare a number to nothing and OPERATE will be a stage in name only.

---

## Gate 6: Outcomes verified

Closes OPERATE. Loops back to DISCOVER.

**Product:** <name> · **Gate run date:** <YYYY-MM-DD> · **Review window:** <launch date + n weeks>

**Inputs on the table:** the completed `../templates/operate/metrics-review.md` against the Gate 1 success signal and the DEFINE-stage targets, the operational readiness review, and the compliance impact assessment where applicable.

- [ ] The success signal named at Gate 1 was measured, with the source system and calculation stated
- [ ] Every key result target from planning is scored: number vs number, no adjectives
- [ ] Input metrics are examined, not just the headline: did the drivers move, or did the headline move for an unrelated reason
- [ ] Operational load is reviewed: incident count, on-call pain, support volume, cost to serve
- [ ] The decision below is one of exactly three: persist, pivot, or sunset
- [ ] The decision's consequence is scheduled: the next DISCOVER pass, the pivot's Gate 1, or the sunset plan with dates and owner
- [ ] What this pass taught us is written in three sentences or fewer and filed where the next team will find it

**Decision:** PERSIST / PIVOT / SUNSET, because: <one paragraph>

| Sign-off | Name | Date |
|---|---|---|
| Product owner | <name> | <date> |
| Sponsor | <name> | <date> |

> **If you skip this gate:** you get the zombie portfolio: features nobody measures, maintained forever because nobody decided anything. The field's experience with launch retrospectives is blunt: teams that never verify outcomes keep shipping outputs, and output was never the point. This gate is one meeting; a zombie product is a permanent tax.

**Failure precedents.**

1. **The signal swapped for a metric that moved.** The Gate 1 signal is quietly replaced by whatever the product turned out to be good at. Tell: the metric named in the review does not appear in the Gate 1 attempt. Score the original, then report the substitute separately if it is interesting. A signal chosen after the fact is chosen to be met.
2. **The headline that moved for someone else's reason.** Retention improved during a quarter that also carried a pricing change and a seasonal peak. Tell: the review has a headline number and no input tree. Put the drivers on the same page, using `../frameworks/metrics/north-star-input-tree.md`, and the confound becomes visible instead of arguable.
3. **The flat driver described with an adverb.** "Action rate is holding steady" for a number that has not moved since week two. Tell: an adverb sits where a delta belongs. Report the number and the date it stopped moving; that pair is what makes the next DISCOVER pass sharper than the last one.
4. **Persist by default.** Nobody argues for pivot or sunset, so persist is recorded. Tell: the decision paragraph contains no comparison and no cost. Persist is a choice to keep spending; it has to beat the alternatives on the page, including the cost to serve and the on-call load this gate just reviewed.
5. **The decision with no scheduled consequence.** PERSIST recorded, next pass unscheduled; SUNSET recorded, no plan and no owner. Tell: no date anywhere after the decision line. An unscheduled consequence is how a decided product becomes a zombie anyway, and the gate that produced it will look, in the file, exactly like one that worked.
6. **Operational load skipped because it is not a product number.** Tell: the operational-load line is ticked and the review contains no incident count, no support volume, and no cost to serve. A feature that met its target and doubled on-call pages has a result the product owner does not feel and the on-call rotation does. That asymmetry is what this line exists to surface.
7. **Three sentences nobody will find.** The lesson is written into the gate attempt only, which no future team reads. Tell: nothing in the product README or the decision log points at it. File it where a new owner lands, per [PRODUCT-WORKSPACE.md](PRODUCT-WORKSPACE.md).

**Most common false pass:** an honest, well-instrumented review of a product whose review window was chosen after the numbers were visible. Every line passes and the window was selected to flatter the result. Choose the window at Gate 5, before the data exists, and write it into the readiness doc.
