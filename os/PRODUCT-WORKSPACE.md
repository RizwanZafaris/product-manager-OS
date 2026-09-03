# The Product Workspace

Templates are blanks. A product is the filled copies of them, accumulated over a year, and that pile is the only memory the next PM will have. This file defines where the pile lives and what it is called, so that "what did we decide about refunds" is a file path rather than an archaeology project.

The convention is a folder. That is the whole mechanism, and it is deliberate: the answer to a memory problem in a document system is a place to put documents, not a database.

## The layout

One folder per product, named for the product, holding one subfolder per stage of the loop:

```
products/
└── ledgerline/
    ├── README.md              what this product is, one paragraph, plus the current stage and gate
    ├── STATE.md               the Conductor's running memory: position, accepted answers, evidence ledger
    ├── discovery/             filled copies of templates/discovery/
    ├── definition/            filled copies of templates/definition/
    ├── architecture/          filled copies of templates/architecture/
    ├── execution/             decision log, risk register, stakeholder map, dependency register
    ├── delivery/              filled copies of templates/delivery/
    ├── operate/               filled copies of templates/operate/
    ├── planning/              this product's roadmap and OKR copies
    └── gates/                 one file per gate attempt, copied from os/STAGE-GATES.md
```

Where the folder sits is your choice. Three arrangements work, and only the third needs a rule:

1. **Its own repository**, with this one cloned alongside as reference. The cleanest option for a team.
2. **Inside your product's existing repository**, next to the code the documents describe.
3. **Inside a clone of this repository.** Allowed, and the reason `products/` is the reserved name: nothing in this repository will ever ship a directory by that name, so your work cannot collide with an update. Add `products/` to `.gitignore` if the contents are private and the clone is not.

## A filled workspace, month nine

The layout above is the shape. This is what it contains once one product has been through all six gates, taken from the Ledgerline walkthrough in [HOW-TO-RUN-A-PRODUCT.md](HOW-TO-RUN-A-PRODUCT.md). Nothing here is aspirational: every file is one the walkthrough names, and the absences are as instructive as the contents.

```
products/ledgerline/
├── README.md                                    updated at each gate, 6 edits
├── STATE.md                                     append-only, 61 accepted-answer rows
├── planning/
│   ├── roadmap.md                               the theme row that opened the loop
│   └── okrs.md                                  the retention key result Gate 6 scored
├── discovery/
│   ├── problem-framing.md                       problem sentence + cost-of-inaction arithmetic
│   ├── user-research-plan.md                    8 interviews, screener, script, themes in s.6
│   ├── interview-notes.md                       19 sessions, source IDs the personas cite
│   ├── personas.md                              archetype A (6 sources), archetype B (2, marked)
│   ├── journey-map.md                           invoice sent to payment landed, panic points
│   └── discovery-document.md                    the Gate 1 roll-up, success signal in s.7
├── definition/
│   ├── brd.md                                   signed by the sponsor, not just the gate
│   ├── prd.md                                   objectives traced to the Gate 1 statement
│   ├── frd.md                                   each requirement traced to a PRD item
│   ├── nfr.md                                   NFR-04 freshness rule, rewritten at attempt 2
│   ├── business-rules.md                        forecast calculation rules, rule IDs
│   ├── assumptions-register.md                  continuous; A-03 validated before Gate 3
│   ├── acceptance-criteria.md                   AC-07 and AC-11 rewritten; AC-09 re-signed
│   └── ai/
│       ├── eval-spec.md                         240 pairs, grounded-number + abstain metrics
│       ├── guardrails.md                        each rail an owner and a test
│       ├── hallucination-controls.md            grounding source + abstain policy
│       ├── human-approval-gates.md              short, with the reason it is short
│       ├── prompt-structure.md                  change log, incl. the injection fix
│       ├── context-management.md                context budget
│       ├── agent-architecture.md                read-only, one forecast at a time
│       ├── multi-agent-workflow.md              N/A because one call, no handoffs
│       └── red-team-review.md                   memo-field injection, found, fixed, re-tested
├── architecture/
│   ├── system-design.md                         pipeline, goals, non-goals
│   ├── adr-001-nightly-precompute.md            supersedes the on-demand assumption
│   ├── adr-002-build-not-buy-forecasting.md     residency constraint + reopening condition
│   ├── solution-architecture.md                 capability map
│   ├── data-model.md                            PII classes, retention per class
│   ├── api-contract.md                          forecast endpoint, worked example
│   ├── sequence-diagram.md                      async explanation call + error path
│   ├── integrations.md                          bank feed: SLA, owner, failure behavior
│   ├── security-architecture.md                 six threat categories per component
│   └── observability.md                         SLOs, the stale-forecast alert threshold
├── execution/
│   ├── decision-log.md                          continuous; row 1 = regulated determination
│   ├── risk-register.md                         continuous; 5 rows from the premortem
│   ├── stakeholder-map.md                       Tomas: high interest, low assigned power
│   └── dependency-register.md                   bank-feed team, reviewed weekly from Gate 3
├── delivery/
│   ├── analytics-instrumentation-spec.md        written before BUILD, per WHICH-DOCUMENT
│   ├── testing-strategy.md                      levels, coverage targets, entry/exit
│   ├── edge-cases.md                            9-day-old business, negative balance
│   ├── failure-scenarios.md                     feed outage: detection, recovery, data loss
│   ├── uat-plan.md                              9 owners, severities agreed before session 1
│   ├── release-readiness.md                     rollback timed, known issues, 4 signatures
│   ├── support-runbook.md                       written in the 3 days after the Gate 5 no-go
│   └── release-notes.md
├── operate/
│   ├── operational-readiness-review.md          runbooks, rotation, backup verified
│   ├── compliance-impact-assessment.md          mostly "N/A because", never blank
│   ├── incident-postmortem-2026-05-14.md        feed degradation; finding was a detection gap
│   ├── metrics-review.md                        headline + the flat input metric
│   └── post-launch-review.md                    within six weeks, once
└── gates/
    ├── gate-1-attempt-1.md                      GO; the no-go argument is in it
    ├── gate-2-attempt-1.md                      RETURNED; 3 lines failed, quoted
    ├── gate-2-attempt-2.md                      SIGNED; AC-09 re-signature appended later
    ├── gate-3-attempt-1.md                      ACCEPTED
    ├── gate-4-attempt-1.md                      MET; 2 misses carried with owners
    ├── gate-5-attempt-1.md                      NO-GO; operations line unsigned
    ├── gate-5-attempt-2.md                      GO
    └── gate-6-attempt-1.md                      PERSIST; 3 filed sentences
```

Five things a reader can learn from that listing without opening a file, which is the property a folder has and a database does not.

- **The gate history has failures in it.** Two returned attempts, both kept. A `gates/` directory with six files and no attempt numbers above 1 is either a very lucky product or a rewritten one, and the second is more common.
- **The AI overlay sits inside `definition/`, not beside it.** The overlay attached at DEFINE, so its artifacts live where the stage that produced them lives. An `ai/` folder at the top level would imply the model was a project rather than a component.
- **Two ADRs are named for their decisions.** Not `adr-1.md` and `adr-2.md`, and not `architecture-decisions.md` holding both. When a superseding record arrives it becomes `adr-003-...`, and ADR-001 stays exactly as written, which is the only way a decision history is worth having.
- **The incident file carries a date and the others do not.** Incidents and gate attempts are events, so they are numbered or dated. Everything else is a living document with one canonical copy, which is rule 2 below.
- **Nothing is missing from `discovery/` that DISCOVER produced, and `competitive-analysis.md` is absent.** It was never needed, so it was never copied. An empty template in a workspace reads as an unanswered question; the absence reads as a decision, and the decision-log row explains it in one line.

## What a new owner reads, in order

A new PM inheriting this folder has a reading path, and the path is the argument for the convention. Roughly ninety minutes to be useful, in this sequence:

1. **`README.md`**, two minutes. What the product is, where it is in the loop, what the next gate waits on.
2. **`execution/decision-log.md`**, twenty minutes, newest entries first. This is the most information per minute in the whole folder, because a decision log is a list of the moments the product could have gone differently. Row 1 here is the regulated-overlay determination from week one, which is exactly the row that constrains the next proposal.
3. **`execution/risk-register.md` and `definition/assumptions-register.md`**, twenty minutes. What the last owner was worried about and what they were guessing. Any assumption past its validate-by date is the new owner's first piece of work.
4. **The newest file in `gates/`**, ten minutes. The current position, stated as evidence rather than as status.
5. **`operate/metrics-review.md`**, twenty minutes, if the product has shipped. Whether the thing worked, and which driver did not move.
6. **`STATE.md`** where one exists, for the evidence ledger's verbatim quotes.

The PRD is not in the first ninety minutes, which surprises people. A PRD describes what was intended at one moment; the four continuous files describe what happened, what is still uncertain, and what was decided against. Read intentions after you know outcomes, or the intentions will read as facts. `../templates/planning/first-90-days.md` is the structured version of this handover.

## The four rules that make it memory rather than storage

1. **Filled copies, never edits to the originals.** Copy the template out, fill the copy. `templates/` stays blank so the next product starts clean. This is the same rule the agent files state and the reason for it is the same. The failure it prevents is the one that ends a template library: a repository where the blanks contain one product's answers, so the next product inherits assumptions nobody restated, and eventually a PM writes their own template rather than untangle yours.
2. **Keep the file name of the template you copied.** A filled PRD is `definition/prd.md`, not `PRD_v3_final_FINAL.md`. Versions are the file's history, not its name. When one product genuinely needs two of something, the suffix names the thing, not the version: `architecture/adr-004-precompute-explanations.md`. The tell that this rule has lapsed is a folder where two files could both plausibly be current, and the cost is paid by whoever has to guess.
3. **Four files never get archived, whatever the stage.** The decision log, the risk register, the assumptions register, and STATE.md run the length of the product. Everything else is written at a stage and read afterward; these four are written continuously and are the first things a new owner reads. STATE.md appears once a Conductor run starts (the blank ships at `templates/execution/state.md`); a product run entirely with a pencil may never have one, and loses nothing but the resume protocol.
4. **Gate attempts are kept, including the failures.** `gates/gate-2-attempt-1.md` is more useful than `gates/gate-2.md`, because the attempt that was returned records what the team did not know at the time. A gate history with no failures in it is either a very lucky product or a rewritten one. The returned Gate 2 in the listing above is the single most read file in the folder six months later, because it contains the sentence that explains why the freshness rule is worded the way it is.

## The product README is the index

One paragraph on what the product is, then a short table: current stage, last gate passed and when, next gate and what it is waiting on, and the owner. Update it at each gate, which is six edits a year, not a maintenance burden.

Filled, it is this short:

```markdown
# Ledgerline forecast

A two-week cash-flow forecast for small-business owners inside the
invoicing product, with a plain-language explanation attached to each
forecast. Owners currently discover shortfalls when a payment bounces.

| Field | Value |
|---|---|
| Current stage | OPERATE |
| Last gate passed | Gate 5 (attempt 2), 2026-04-30 |
| Next gate | Gate 6, review window closes 2026-06-11 |
| Waiting on | Six weeks of action-rate data from the warehouse |
| Owner | Dana |
| Overlays | AI overlay active. Regulated: not applicable, decision log row 1 |
```

The "waiting on" field is the one that earns the table. Current stage and last gate are status; "waiting on" is the answer to the only question anyone actually arrives with, which is whether they can help. A README whose waiting-on field has not changed in six weeks is telling you something true about the product, and it is the cheapest status report in the system.

This is what an AI runtime reads first when you point it at a product, followed by STATE.md where one exists. It is also what a new PM reads first, which is the same requirement.

## What this convention is deliberately not

It is not a knowledge graph, an index service, or a database. Those were considered and rejected for the first version, because a document system whose memory needs software has stopped working with a pencil, and because the failure mode of index infrastructure is a stale index that lies with confidence. A folder cannot go stale in a way that hides from you.

The tradeoff is real and worth stating rather than glossing: search across many products is grep, cross-product rollups are manual, and nothing enforces that the README's stage field matches the newest gate file. Those costs are paid by a person, visibly, and a mismatch is discovered by the person who cares. An index gets those things right until it silently stops, and the failure surface of a wrong index is every decision made from it.

It is also not a replacement for the canon layer. `knowledge/` holds methods that are true across products, with named attribution. `products/<name>/` holds what happened to one product. The two never merge: a lesson from one product graduates into the canon only when it stops being about that product, and it arrives with an attribution like everything else in that directory.

The graduation test, since this is where the two layers get confused: could a team at a different company, in a different domain, act on this sentence without knowing your product? "Freshness rules must be stated in the artifact the user reads" passes and belongs in the canon. "Ledgerline's explanation states data age" fails and belongs in the product folder forever. Most lessons never graduate, and a canon layer that grows every quarter is absorbing one team's history under the label of method.

## How the loop uses it

[OPERATING-LOOP.md](OPERATING-LOOP.md) says which template a stage produces. This file says where it lands. [HOW-TO-RUN-A-PRODUCT.md](HOW-TO-RUN-A-PRODUCT.md) walks one product through all six stages and every artifact it names ends up in one of the folders above. [WHICH-DOCUMENT.md](WHICH-DOCUMENT.md) decides how heavy each of those artifacts should be before you copy it out. [STAGE-GATES.md](STAGE-GATES.md) is the only file in `os/` that gets copied into the workspace, once per gate attempt, and [CONDUCTOR.md](CONDUCTOR.md) is the protocol for a runtime that fills these files by interview rather than by hand.
