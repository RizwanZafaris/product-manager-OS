# DELIVER bank

Stage: DELIVER, feeds Gate 5 (release readiness green) in [../../../os/STAGE-GATES.md](../../../os/STAGE-GATES.md).
Working handoffs: [../../../agents/drafting-agent.md](../../../agents/drafting-agent.md) drafts the release set and the go-to-market plan (workspace copy of [../../../templates/planning/gtm-plan.md](../../../templates/planning/gtm-plan.md)); [../../reg-gap-check/SKILL.md](../../reg-gap-check/SKILL.md) re-runs when the regulated overlay is active.
Applies: [Crossing the Chasm](../../../knowledge/crossing-the-chasm.md), Geoffrey Moore's argument that early adopters and mainstream buyers purchase for different reasons, so the first cohort is a beachhead choice, not a broadcast. The Conductor names this method aloud when DELIVER-4 runs.
Questions 4 and 7 through 10 are the go-to-market block; their accepted answers fill the gtm plan.
Format and ladder: [README.md](README.md).

### DELIVER-1: the rollback

Ask: Was the rollback actually performed in pre-production, and how long did it take?
Wrong costs: The industry's incident write-ups repeat one line: the rollback plan existed on paper and had never been run.
Evidence class: 1, the rehearsal, dated, with the time to roll back recorded.
Cross-examine when: "we have a rollback plan" arrives as a document, not a rehearsal. Move: interest to behavior, when was it run and how long did it take?
Accept when: performed, dated, timed, in a pre-production environment.
Lands in: `delivery/release-readiness.md` section 4, and STATE.md accepted answers.

### DELIVER-2: UAT and severity ones

Ask: Are the UAT exit criteria met with real users or named proxies, and is every severity-1 defect closed?
Wrong costs: UAT signed by the build team is the build team agreeing with itself.
Evidence class: 2, UAT results against the plan's exit criteria, testers named.
Cross-examine when: the testers are teammates standing in for users without being named as proxies. Move: category to name.
Accept when: exit criteria met, testers real or named proxies, severity-1 count zero.
Lands in: `delivery/uat-plan.md` section 6, and STATE.md accepted answers.

### DELIVER-3: known issues

Ask: Which known issues ship, each with a workaround or an accepted-risk signature?
Wrong costs: The unlisted known issue becomes support's discovery and the team's credibility bill.
Evidence class: 3, each accepted risk signed by someone with standing.
Cross-examine when: the list is empty on a first release. Move: banned openers; zero known issues is a claim about your testing, not your product.
Accept when: every shipping issue listed with a workaround or a signed acceptance.
Lands in: `delivery/release-readiness.md` section 3, and STATE.md accepted answers.

### DELIVER-4: the first cohort

Ask: Who is the first user cohort, through which channel, and what evidence says that channel reaches them?
Wrong costs: A launch aimed at everybody arrives for nobody; the beachhead is a choice you defend.
Evidence class: 2, evidence the channel has reached these people before.
Cross-examine when: the cohort is a segment or the channel is "marketing". Move: category to name.
Accept when: a named cohort, one channel, and prior evidence the channel reaches them.
Lands in: the workspace gtm plan, first cohort section, and STATE.md accepted answers.

### DELIVER-5: support and on-call

Ask: Do support and on-call know this release is coming, and does the runbook exist?
Wrong costs: The launch support learns about from customers is the other repeat offender in incident write-ups.
Evidence class: 3, their acknowledgment, plus the runbook as an artifact.
Cross-examine when: "they have been looped in" without a named acknowledgment. Move: interest to behavior, who confirmed, and where is the runbook?
Accept when: named acknowledgment from support and on-call, runbook path stated.
Lands in: `delivery/release-readiness.md` sections 5 and 6, and STATE.md accepted answers.

### DELIVER-6: regulated overlay drift

Ask: Are the section 0 answers from Gate 2 still true of the artifact that ships?
Wrong costs: A deferred precondition can resurface with a regulator's reference number attached.
Evidence class: 2, the answers re-checked line by line against the shipping artifact: model version, vendor terms, data residency, disclosures.
Cross-examine when: "nothing changed" without the line-by-line check. Move: interest to behavior, walk the four together.
Accept when: each answer re-verified, and any drift written up and re-signed by the regulatory owner. Skip this entry with a cited source when STATE.md says the regulated overlay is not active.
Lands in: `delivery/release-readiness.md` section 7, and STATE.md accepted answers.

### DELIVER-7: positioning

Ask: Against which named alternative is this positioned, and what is the one sentence the first cohort hears?
Wrong costs: Positioned against nothing, the product is compared to everything, on the buyer's terms.
Evidence class: 4, the alternative named from discovery evidence, not assumed.
Cross-examine when: the alternative is "doing nothing" claimed without DISCOVER-2 behavior behind it, or the sentence needs three clauses. Move: banned openers.
Accept when: one named alternative, one sentence a real cohort member would repeat.
Lands in: the workspace gtm plan, positioning section, and STATE.md accepted answers.

### DELIVER-8: launch sequence

Ask: In what order do the launch steps run, and who owns each step?
Wrong costs: A launch without a sequence is a date with hope attached.
Evidence class: 2, the sequence written with owners and dates.
Cross-examine when: steps have owners but no dates, or the sequence is a single big-bang day. Move: naked numbers.
Accept when: ordered steps, each owned and dated, with the first reversible step first.
Lands in: the workspace gtm plan, launch sequence section, and STATE.md accepted answers.

### DELIVER-9: the launch metric

Ask: What is the one metric that says the launch worked, and by when?
Wrong costs: Without one metric named in advance, the retrospective grades on a curve of whatever moved.
Evidence class: a measurable signal plus the source system that will measure it, consistent with the Gate 1 signal from DISCOVER-7.
Cross-examine when: multiple metrics arrive, or the metric contradicts DISCOVER-7 without explanation. Move: naked numbers.
Accept when: one metric, one threshold or direction, one date, one source system.
Lands in: the workspace gtm plan, success measure section, and STATE.md accepted answers.

### DELIVER-10: the stop condition

Ask: What condition pauses the rollout?
Wrong costs: A rollout with no stop condition stops only when the damage does.
Evidence class: an observable condition with a threshold and a named authority to call the stop.
Cross-examine when: the condition is "if things look bad". Move: naked numbers.
Accept when: condition, threshold, and the person with authority to pull it, named.
Lands in: the workspace gtm plan, stop condition section, and `execution/risk-register.md`, and STATE.md accepted answers.

## Forced pair

On "advance anyway": DELIVER-1, then DELIVER-10. An unrehearsed rollback and a rollout with no stop condition are the two skips that convert a bad hour into a bad quarter.

## Gate 5 rendering

| Gate 5 checklist line | Evidenced by |
|---|---|
| UAT exit criteria met, severity-1 defects closed | DELIVER-2 |
| Rollback performed in pre-production, time recorded | DELIVER-1 |
| Known issues listed with workaround or accepted-risk sign-off | DELIVER-3 |
| Comms drafted and approved | DELIVER-4, DELIVER-7, via the drafting-agent handoff against `delivery/release-readiness.md` section 6 |
| On-call informed, runbook exists | DELIVER-5 |
| Every function signed its own readiness line | Human signatures; the Conductor reports presence or absence, never supplies them |
| AI overlay: guardrails live, kill switch tested | BUILD-5 and BUILD-6 evidence re-verified against the release candidate |
| Regulated overlay: section 0 still true of what ships | DELIVER-6 |
