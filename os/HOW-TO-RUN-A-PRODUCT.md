# How to Run a Product

One fictional product taken through all six gates, naming every template used at each step. The product is **Ledgerline**, a cash-flow forecast feature inside a small-business bookkeeping app, with a model-generated plain-language explanation attached to each forecast. Fictional company, fictional people, invented numbers throughout. The point is the moves, not the story.

Read [OPERATING-LOOP.md](OPERATING-LOOP.md) for the stage definitions and [STAGE-GATES.md](STAGE-GATES.md) for the forms this walkthrough keeps arriving at.

## Before stage 1: planning decides this enters the loop

Ledgerline does not start because someone had an idea in a meeting. The quarterly plan in `../templates/planning/roadmap.md` carries a theme, "owners stop being surprised by cash", with a confidence level and a target period. The company OKRs in `../templates/planning/okrs.md` carry a key result about second-month retention, with a baseline and a target. The roadmap slot plus the retention KR is the mandate. The PM, Dana, opens the loop.

Because the explanation component is model-generated, Dana notes on day one that the AI overlay will apply from DEFINE onward. Ledgerline's company is not a licensed financial institution and the feature makes no decisions about anyone's access to money, so the regulated overlay does not activate; Dana records that determination and the reasoning in the decision log rather than leaving it as an assumption. Had the answer been yes, `../modules/regulated/` would have attached at Gate 2 and Gate 5, via `../skills/reg-gap-check/SKILL.md`.

## DISCOVER, ending at Gate 1

Dana copies `../templates/discovery/problem-framing.md` and writes one problem statement: small-business owners find out about cash shortfalls when payments bounce, not before. Evidence: support tickets tagged "overdraft", churn interviews from last quarter. Cost of inaction: the churn line, calculated in the template's own field.

The research plan goes into `../templates/discovery/user-research-plan.md`: eight owner interviews, a screener excluding businesses with full-time finance staff, a script that asks about the last cash surprise, never "would you use a forecast". Notes and synthesis themes accumulate in the same document.

Two archetypes come out of the interviews and go into `../templates/discovery/personas.md`. One is backed by six cited interviews. The other is backed by two, so the template's evidence rule forces it to be labeled an assumption, which later stops a design argument cold. The path from invoice sent to payment landed, with the panic points marked, goes into `../templates/discovery/journey-map.md`.

Everything rolls up into `../templates/discovery/discovery-document.md`: trigger, target user, pain, hypothesis ("a two-week forecast owners trust changes behavior before the shortfall"), success signal (owners who see a warning act on it), go or no-go.

**Gate 1.** The form from STAGE-GATES.md is filled at a one-hour review. The no-go argument is seriously made: maybe alerts, not forecasts, are the real product. It loses on the interview evidence. GO is recorded, the sponsor signs, and the success signal is written down months before launch. Attempt 1 passes.

## DEFINE, ending at Gate 2

Business case first: `../templates/definition/brd.md` names objectives, scope, stakeholders, constraints, the ROI logic, and the sponsor who will sign it.

Then the PRD in `../templates/definition/prd.md`: background, objectives traced to the Gate 1 problem statement, user stories, functional scope, success metrics, out of scope (no payment initiation, no lending referrals), launch criteria. Because the explanation text is model-generated, Dana runs the PRD through `../skills/ai-prd/SKILL.md`, which pulls in the AI overlay:

- `../templates/ai/eval-spec.md` turns "explanations should be accurate" into a labeled eval set with a numeric pass threshold and a rule for what happens below it.
- `../templates/ai/guardrails.md` gives every rail an owner and a test, including "never state a number that is not in the forecast data".
- `../templates/ai/hallucination-controls.md` pins the grounding source (the forecast table itself) and the abstain policy.
- `../templates/ai/human-approval-gates.md` is short here: no irreversible actions exist, and the template records why that is the honest answer.
- `../templates/ai/prompt-structure.md` and `../templates/ai/context-management.md` version the prompt and budget the context, so a future model change is a diff, not archaeology.

Functional detail lands in `../templates/definition/frd.md`, each requirement traced back to a PRD item. Targets that are numbers, latency, availability, accessibility, retention, go into `../templates/definition/nfr.md`; the one target nobody can state yet names an owner and a date instead. Forecast calculation rules go into `../templates/definition/business-rules.md` with rule IDs and test traceability. Every load-bearing guess, "owners check the app at least weekly", goes into `../templates/definition/assumptions-register.md` with a confidence, a validation method, and a validate-by date. Acceptance criteria that can fail go into `../templates/definition/acceptance-criteria.md` as given/when/then blocks with thresholds.

**Gate 2.** Attempt 1 is RETURNED: two acceptance criteria are prose ("forecast feels trustworthy") and one NFR has neither a number nor an owner. A week later, attempt 2 passes with the criteria rewritten as eval rows and the NFR owned. The sponsor signs the BRD itself, then the gate.

## DESIGN, ending at Gate 3

Architecture work runs through `../templates/architecture/`:

- `system-design.md`: goals, non-goals, the forecast pipeline diagram, and the alternative that was rejected (a third-party forecasting API) with the tradeoff written down.
- That rejection is frozen as a numbered record in `adr.md`; if it is ever reversed, a new ADR supersedes it rather than editing history.
- `solution-architecture.md` maps capabilities and the build-vs-buy rationale; `data-model.md` classifies which entities carry PII and sets retention per class; `api-contract.md` specifies the forecast endpoint with schema, auth, errors, and a worked micro-example; `sequence-diagram.md` covers the async explanation call and its error path; `integrations.md` rows the bank-feed provider with SLA, owner, and failure behavior; `security-architecture.md` walks each component through the six threat categories and assigns mitigation owners; `observability.md` sets SLOs and alert thresholds before any code exists.
- `../templates/ai/agent-architecture.md` records that the explanation generator gets read-only access to one forecast at a time, least access checked. `../templates/ai/multi-agent-workflow.md` is consulted and marked not applicable, in writing: there is one model call, no handoffs.

In parallel the execution set opens: `../templates/execution/stakeholder-map.md` (who cares, how much, RACI), `../templates/execution/risk-register.md`, `../templates/execution/decision-log.md` (the regulated-overlay determination from week one already lives here), and `../templates/execution/dependency-register.md` (the bank-feed team's needed-by date, with an escalation contact, reviewed weekly from now on, not just today).

Before the gate, the team runs `../skills/program-premortem/SKILL.md`: "it is six months from now and Ledgerline failed, why?" The top answer, stale bank-feed data producing confident wrong forecasts, becomes a risk-register row with an owner and drives a new guardrail: the explanation must state data freshness.

**Gate 3.** The security reviewer, the architect, and Dana sign. Attempt 1 passes because the premortem already forced the hard conversation.

## BUILD, ending at Gate 4

The testing strategy in `../templates/delivery/testing-strategy.md` sets levels, coverage targets, environments, and entry and exit criteria. The boundary work happens in `../templates/delivery/edge-cases.md`, no row may say "to be decided": what does the forecast show for a nine-day-old business, a negative balance, a currency the feed cannot classify? Blast-radius thinking goes into `../templates/delivery/failure-scenarios.md`: feed outage, detection, recovery, data-loss risk.

Mid-build, reality pushes back: the explanation model cannot meet the latency budget from the NFR doc. The change, precompute explanations nightly instead of on demand, is written into `../templates/execution/decision-log.md` with options and a decider, and the affected acceptance criterion is re-signed against Gate 2 explicitly. Backward is allowed; silent backward is not.

The eval set from DEFINE runs in CI against the pinned model version. One threshold fails; the failing cases are added back into the eval set per its governance field, the prompt is revised through `../templates/ai/prompt-structure.md`'s change log, and the suite goes green.

**Gate 4.** Every acceptance criterion demonstrated, two misses carried forward with owners and an accept-with-rationale decision, the red-team pass from `../templates/ai/red-team-review.md` run against the built feature (prompt injection through invoice memo fields was found, fixed, and re-tested). Engineering, QA, and Dana sign.

## DELIVER, ending at Gate 5

UAT runs against `../templates/delivery/uat-plan.md`: nine real business owners, entry and exit criteria, defect severities agreed before testing starts, sign-off form at the bottom. The go/no-go evidence accumulates in `../templates/delivery/release-readiness.md`: feature checklist, test summary, known issues (two, each with a workaround), rollback plan, comms drafts, one signature line per function.

The rollback is not a paragraph; it is performed in staging and timed. The kill switch for the explanation component is flipped, verified, and flipped back.

**Gate 5.** Attempt 1 is NO-GO: support had never seen the release. Comms and a runbook session fix it in three days; attempt 2 is GO. Release owner, product, and operations sign.

## OPERATE, ending at Gate 6, and the loop

The first weeks run against `../templates/operate/operational-readiness-review.md`: runbooks live, on-call rotation set, backup and recovery verified, checks derived from the failure-scenarios table. `../templates/operate/compliance-impact-assessment.md` is completed and mostly reads "N/A because", which is an answer; a blank is not.

Six weeks after launch, the metrics review in `../templates/operate/metrics-review.md` scores the number against the target: the Gate 1 success signal (owners act on warnings) is measured from the source system named back at DEFINE. Headline is positive; one input metric is flat, and the review says so instead of rounding up.

**Gate 6.** Decision: PERSIST, with a scheduled next DISCOVER pass aimed at the flat input metric. Three sentences of what this pass taught are filed. The sponsor signs, and the loop closes where it started: a new trigger, back into `../templates/discovery/problem-framing.md`.

## The interview-to-backlog chain, hop by hop

The walkthrough above is the whole loop. This section zooms in on the stretch people most often try to automate end to end: raw interview recordings at one end, stories a team can pick up at the other. It runs on Method 3, an agent CLI with file access. Each hop names the file that drives it, so nothing here is a black box.

| Hop | From | Runs on | Produces |
|---|---|---|---|
| 1 | Transcripts, tickets, sales notes | `../skills/feedback-synthesis/SKILL.md` | Weighted themes with source counts and contradictions, written into section 6 of `../templates/discovery/user-research-plan.md` |
| 2 | Themes | `../agents/research-agent.md` | Evidence rows with source IDs in `../templates/discovery/discovery-document.md`, sections 3 to 5 |
| 3 | Discovery document | Gate 1 in `STAGE-GATES.md`, signed by a human | GO, NO-GO, or MORE DISCOVERY, with the success signal named |
| 4 | Signed Gate 1 | `WHICH-DOCUMENT.md` | The weight of the next artifact: a ticket, `../templates/definition/one-pager.md`, or the full PRD |
| 5 | The chosen weight | `../agents/drafting-agent.md`, or `../skills/ai-prd/SKILL.md` when the product contains a model | A filled PRD or one-pager, every unknown marked as an open field |
| 6 | Draft requirements | `../templates/definition/acceptance-criteria.md`, and `../templates/ai/eval-spec.md` for model behavior | Given, when, then blocks with thresholds; eval rows where prose will not do |
| 7 | The full definition set | `../agents/validation-agent.md` | A miss list against the template's own fields and the Gate 2 checklist. It reports; it does not rewrite |
| 8 | The same set | `../agents/red-team-agent.md` | Attacks on the draft, written into the risk register and, for model features, `../templates/ai/red-team-review.md` |
| 9 | Signed Gate 2 | The PRD's own story table and `../templates/definition/frd.md` | Epics and stories, each carrying its acceptance criteria ID into whatever tracker you use |

Four things this chain does not do, on purpose.

1. **It never crosses a gate.** Hop 3 and hop 9 both stop at a signature. An agent can fill the gate form and report which boxes fail; a named human ticks them.
2. **It never promotes model output to evidence.** A theme from hop 1 carries the source IDs it was built from, and a theme that cannot name three independent sources arrives labeled as an anecdote. Rule 4 of the loop applies at every hop.
3. **It does not write into this repository.** Filled artifacts land in the product workspace described below, never in `../templates/`.
4. **It has no ticket-system integration.** Hop 9 ends at stories with IDs in a markdown file. Getting them into a tracker is a copy and paste, which is a deliberate choice: an integration is a permanent maintenance cost paid for a saved minute.

Running the chain with no AI at all is the same nine hops with a person at each one. That is Method 1, and the hops are what the walkthrough above describes Dana doing by hand.

## Where all of this lives

Every artifact named in this walkthrough is a filled copy, and the copies belong together. The convention is one folder per product with a subfolder per stage, defined in [PRODUCT-WORKSPACE.md](PRODUCT-WORKSPACE.md). Dana's Ledgerline files live at `products/ledgerline/`, its gate attempts including the two that failed live in `products/ledgerline/gates/`, and the decision log that carried the regulated-overlay determination from week one is still the first file a new owner opens a year later. That accumulated folder is the product's memory. There is no other memory, and no software is needed to keep it.

## What to copy from this walkthrough

1. Gates failed twice (Gate 2 attempt 1, Gate 5 attempt 1) and the product was better for it. Expect that.
2. Every unknown became a named owner and a date, never a blank.
3. Overlay decisions were made explicitly and recorded, including the overlays that did not apply.
4. The templates did the remembering. The team did the judging.
