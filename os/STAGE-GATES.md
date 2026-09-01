# Stage Gates

Six gates, one per stage of the loop in [OPERATING-LOOP.md](OPERATING-LOOP.md). Each gate is a fill-in form: copy the gate's section into your product workspace, complete every field, tick only the boxes that are honestly true, and collect the signatures. A gate passes when the form is complete and signed, not when the meeting ends.

<!-- Conventions for every gate below:
     - Angle-bracket fields <like this> are the blanks you fill.
     - Boxes are ticked by the humans named on the sign-off lines, never by an agent.
     - "Evidence" always means a document or artifact you can point at, not a recollection.
     - A failed gate is a normal outcome. Record the misses, assign owners, re-run.       -->

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
- [ ] The success signal for a future Gate 6 is named now, before any solution exists
- [ ] Go or no-go is recorded below, with the deciding rationale in one paragraph

**Decision:** GO / NO-GO / MORE DISCOVERY, because: <one paragraph>

| Sign-off | Name | Date |
|---|---|---|
| Product owner | <name> | <date> |
| Sponsor or lead who can stop this | <name> | <date> |

> **If you skip this gate:** the field's most common postmortem finding is a team that discovers in beta that nobody has the problem, after the expensive stages are already paid for. Products regularly die of "no market need" as diagnosed after launch; this gate is where that diagnosis is cheap. A no-go here costs a week.

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

---

## Gate 5: Release readiness green

Closes DELIVER. Feeds OPERATE.

**Product:** <name> · **Gate run date:** <YYYY-MM-DD> · **Attempt:** <n>

**Inputs on the table:** UAT results against `../templates/delivery/uat-plan.md`, the completed `../templates/delivery/release-readiness.md`, and the rollback evidence.

- [ ] UAT exit criteria are met, with real users or their named proxies, and every severity-1 defect is closed
- [ ] The rollback was actually performed in a pre-production environment, and the time to roll back is recorded
- [ ] Known issues going out with the release are listed in the readiness doc, each with a workaround or an accepted-risk sign-off
- [ ] Comms are drafted and approved: support, sales or field teams, and customers where applicable
- [ ] On-call knows this release is coming, and the runbook for it exists
- [ ] Every function on the readiness checklist signed its own line: engineering, product, QA, support, and any others the readiness doc names
- [ ] **AI overlay:** guardrails verified live in the release candidate; the kill switch was tested, not just designed
- [ ] **Regulated overlay:** the section 0 answers from Gate 2 are still true of the artifact that ships (model version, vendor terms, data residency, disclosures); any drift is written up and re-signed by the regulatory owner

**Decision:** GO / NO-GO, because: <one paragraph>

| Sign-off | Name | Date |
|---|---|---|
| Release owner | <name> | <date> |
| Product owner | <name> | <date> |
| Operations or support lead | <name> | <date> |
| Regulatory owner (regulated products only) | <name or N/A because <reason>> | <date> |

> **If you skip this gate:** the industry's incident write-ups repeat one line: the rollback plan existed on paper and had never been run. The other repeat offender is the launch support learned about from customers. Both are cheap to prevent here and expensive to explain later.

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
