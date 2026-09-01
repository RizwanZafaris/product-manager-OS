# The Conductor: design for v0.2.0

This document is the blueprint for the Conductor, the v0.2.0 upgrade that turns this repository from a template library into an interactive, stage-gated product interviewer. The Conductor asks before it writes. It runs one product through the six-stage loop in [../os/OPERATING-LOOP.md](../os/OPERATING-LOOP.md) as a sequence of interviews, one question at a time, cross-examines weak answers, refuses to advance a stage until the gate in [../os/STAGE-GATES.md](../os/STAGE-GATES.md) is met on evidence, and lands every accepted answer in a filled template inside the product workspace. Nothing in v0.1.0 changes underneath it: the templates still work with a pencil, the gates are still signed by humans, and a user who never says "start" never meets the Conductor.

Builders implement from section 6. Everything before it is the reasoning they build against.

## 1. Prior art, and what this design takes from each

Four open systems were read in full, and each contributed one mechanism, restated here in this repository's own words.

- **BMAD-METHOD** (bmad-code-org/BMAD-METHOD): elicitation as an explicit checkpoint. After a draft exists, the agent offers a numbered menu of refinement methods, and nothing changes until the user applies or rejects a specific edit. The Conductor borrows the behavioral gate: an answer is accepted by an explicit user action, never inferred from a friendly reply.
- **spec-kit** (github/spec-kit): the document is the memory. Each accepted clarification is appended to the working file before the next question fires, unknowns are marked in the file rather than guessed, marked unknowns are capped, and the stage exit is a rendered checklist re-evaluated against the current draft. The Conductor borrows all four, with STATE.md as the append target.
- **gstack** (garrytan/gstack, the office-hours skill): forcing questions asked one at a time with a stop after each, a vague answer pushed at least twice before acceptance, the question subset picked by the product's stage rather than run by rote, and a bounded escape hatch, honored only after the highest-stakes remaining questions are forced. The Conductor borrows the interrogation grammar and the escape hatch shape.
- **ai-dev-tasks** (snarktank/ai-dev-tasks): lettered option lists so a user can answer a clarifying question in one line, and a hard pause between generation phases until the user explicitly says go. The Conductor borrows the option format and the pause.

Five failure modes those systems avoid, which this design treats as defects if they appear in any builder's output: question walls (everything at once), fake choices (options that do not differ in consequence), advancing on vibes (a polished first answer accepted untested), no convergence rule (interrogation without a cap or a done state), and guessing instead of marking (a gap silently filled rather than visibly parked).

## 2. The Conductor's contract

Seven rules, binding on every stage and every runtime.

1. **One question at a time.** A full interrogative sentence, then a stop. Before the options: one line naming what it costs to get this answer wrong. Then a recommended default with a one-line reason, so agreeing costs the user one word, and two to five lettered options that differ in consequence, each paired with what choosing it implies.
2. **Smart skip.** Never ask what the loaded context already answers. Before each question the Conductor checks STATE.md, the product README, and the stage's filled artifacts; a question answered there is marked accepted with its source cited, and the user sees the skip.
3. **Cross-examine, capped at two pushes.** A vague answer meets the challenge grammar in section 4, at most twice per question. After the second push the answer is either accepted as offered or parked in the assumptions register with an owner and a validate-by date, and the parked item appears in STATE.md under open challenges. No looping, no silent acceptance.
4. **The answer lands before the next question.** Every accepted answer is written into STATE.md and, where one applies, the target template field, immediately. Chat context is never the only copy of anything.
5. **The gate decides advancement, a human signs it.** Stage exit means the Conductor renders the stage's gate checklist from [../os/STAGE-GATES.md](../os/STAGE-GATES.md), marks each line pass, fail, or unknown with the evidence beside it, and refuses to open the next stage while any line is fail or unknown. When every line passes, the Conductor says so and stops: a named human ticks the boxes and signs. The Conductor records the outcome and files the attempt under `products/<name>/gates/`, failures included.
6. **The escape hatch is bounded and loud.** A user who says "advance anyway" gets the two highest-stakes unanswered questions for the stage forced first. If they still insist, the skip is recorded in STATE.md and as a risk-register row naming what was skipped and what it risks, quoting the gate's own skip warning. There is no quiet path past a gate.
7. **The WHICH-DOCUMENT tree runs before any template opens.** At DEFINE, the three questions from [../os/WHICH-DOCUMENT.md](../os/WHICH-DOCUMENT.md), stakes, audience, reversibility, are the first three questions asked, and their answers pick the artifact weight. Sometimes the right output is a decision-log entry and no document at all, and the Conductor says so instead of drafting.

The Conductor also inherits, unchanged, the gate rules of [../AGENTS.md](../AGENTS.md): never invent a number, a name, a citation, or a quote; never sign; never edit `templates/`, `knowledge/`, `os/`, or `modules/regulated/` on a product run.

## 3. The journey map

One table row per stage. Question banks live as files under `skills/conductor/questions/`, one per stage; the core questions below are the normative content of those files, and each bank file adds, per question: the evidence class required (section 4), the cross-examination trigger, and the template field the accepted answer lands in.

| Stage | Interviewing skill or agent | Working skill or agent | Templates written on acceptance | Exit |
|---|---|---|---|---|
| DISCOVER | `skills/conductor` | `skills/product-analyst` via [../agents/research-agent.md](../agents/research-agent.md) | `templates/discovery/` set, rolled into discovery-document.md | Gate 1 |
| DEFINE | `skills/conductor` | [../agents/drafting-agent.md](../agents/drafting-agent.md); [../skills/ai-prd/SKILL.md](../skills/ai-prd/SKILL.md) when a model is inside; [../agents/validation-agent.md](../agents/validation-agent.md) before the gate | `templates/definition/` set at the chosen weight | Gate 2 |
| DESIGN | `skills/conductor` | drafting agent in the Architect role; [../skills/program-premortem/SKILL.md](../skills/program-premortem/SKILL.md) | `templates/architecture/` and `templates/execution/` sets | Gate 3 |
| BUILD | `skills/conductor` | [../agents/validation-agent.md](../agents/validation-agent.md), [../agents/red-team-agent.md](../agents/red-team-agent.md) | `templates/delivery/` testing set; decision log updates | Gate 4 |
| DELIVER | `skills/conductor` | drafting agent; [../skills/reg-gap-check/SKILL.md](../skills/reg-gap-check/SKILL.md) when regulated | `templates/delivery/` release set; `templates/planning/gtm-plan.md` | Gate 5 |
| OPERATE | `skills/conductor` | `skills/product-analyst` for metric evidence | `templates/operate/` set; `templates/planning/growth-plan.md` | Gate 6 |

### DISCOVER: seven core questions

1. Who exactly has this problem? A segment is not an answer; one title, at one named or precisely described company, with the consequence they personally eat. Evidence class: named user or cited interview.
2. What did that person do the last time the problem occurred? Behavior, not intention. Evidence class: observed behavior or an artifact of the workaround (a ticket, a spreadsheet, an export).
3. What does the current workaround cost them, per what period? Evidence class: a number with a unit, a period, and a source, or an explicit assumption-register entry.
4. What does it cost to do nothing? The cost-of-inaction calculation, shown. Evidence class: same as question 3.
5. How many real user conversations stand behind this, and where are they cited? Gate 1 requires five or more; fewer means the personas are labeled assumptions. Evidence class: cited interviews by source.
6. What would make the honest answer no-go? Gate 1 requires the no-go case seriously argued; the Conductor collects it here, in advance. Evidence class: a stated disconfirming condition someone could observe.
7. What observable signal, measurable at Gate 6, says this worked? Named before any solution exists. Evidence class: a measurable signal plus the source system that will measure it.

### DEFINE: eight core questions

1. Stakes: what does being wrong cost, an afternoon, a sprint, a quarter, a license? 2. Audience: who must read this and act? 3. Reversibility: flag-reversible in a day, or does it set contracts and data models? These three run the WHICH-DOCUMENT tree and pick the weight; the answer may be "decide and log," in which case the interview ends with one log entry.
4. For each objective: which Gate 1 problem statement does it trace to? An objective that traces to nothing is cut or the gap is named.
5. For each requirement: how does it fail? Condition, expected result, measurable threshold. Prose that cannot fail is returned, not accepted.
6. What is out of scope, and has the sponsor read the list?
7. Which assumptions is this built on? Each gets confidence, validation method, validate-by date, into the assumptions register.
8. Does a model produce any user-facing output, and does a financial or data regulator govern any target market? Yes to the first attaches the AI overlay, eval rows replacing prose criteria. Yes to the second routes through reg-gap-check before Gate 2, because the overlay's preconditions freeze here.

### DESIGN: seven core questions

1. What alternative was seriously considered and rejected, and what tradeoff decided it? Lands as an ADR; a design with no rejected alternative has not been designed yet.
2. For every integration: who owns it, what SLA, what happens when it fails?
3. Where does PII live, and what is the retention per data class?
4. It is six months from now and this product failed: why? Asked twice, second answer must differ from the first. Both land in the risk register with owners. This is the premortem entry point.
5. Which teams does this wait on, by what date, and who is the escalation contact?
6. How will you see it misbehaving before users tell you: SLOs, alert thresholds, dashboard owner, before code exists?
7. AI overlay: what is the least access each agent needs, and does every guardrail have an owner and a test?

### BUILD: six core questions

1. Which acceptance criteria are demonstrated passing, and for each miss, who owns it and what was decided?
2. Which edge-case rows are still undecided? The accepted count is zero; anything else is a named miss.
3. Were the failure scenarios exercised, did detection fire, did recovery match the write-up?
4. What changed in scope since Gate 2, and where is each change in the decision log with a decider named?
5. AI overlay: did the eval sets run against the model version that ships, and what happened at each threshold?
6. What did the red team break, and was every fix re-tested?

### DELIVER: six core questions

1. Was the rollback actually performed in pre-production, and how long did it take?
2. Are UAT exit criteria met with real users or named proxies, and is every severity-1 defect closed?
3. Which known issues ship, each with a workaround or an accepted-risk signature?
4. Who is the first user cohort, through which channel, and what evidence says that channel reaches them? First of the gtm-plan questions; the bank file carries the rest (positioning against the named alternative, launch sequence, the one metric that says the launch worked, and the stop condition that pauses rollout).
5. Do support and on-call know this is coming, and does the runbook exist?
6. Regulated overlay: are the section 0 answers from Gate 2 still true of the artifact that ships?

### OPERATE: six core questions

1. Was the Gate 1 success signal measured, with the source system and the calculation stated?
2. For each key result: number versus number. Adjectives are returned unanswered.
3. Did the input metrics move, or did the headline move for an unrelated reason?
4. What does this cost to run: incident count, support volume, on-call load?
5. Which input metric is the next growth bet, and what is the cheapest experiment that would move it? First of the growth-plan questions; the bank file carries the rest (the loop or channel behind the metric, the counter-metric that catches damage, and the kill condition for the experiment).
6. Persist, pivot, or sunset, and what consequence is scheduled: the next DISCOVER pass, the pivot's Gate 1, or the sunset plan with dates and an owner?

## 4. Evidence classes and the challenge grammar

Every question in every bank names the minimum evidence class it accepts, from this ladder, strongest first:

1. **Observed behavior**: something a user did, with a date and a place it is recorded.
2. **Artifact**: a document, dataset, ticket, or export a reader could open.
3. **Named commitment**: a person with standing said yes in writing.
4. **Interview claim**: a real person said it, cited by source and date.
5. **Team belief**: goes to the assumptions register, never into a template as fact.

The challenge grammar, applied when an answer misses its class:

- **Category to name.** "Mid-market finance teams" is met with: name one title, one company, one consequence.
- **Interest to behavior.** A signup, a compliment, or "they said they would" is met with: what did someone pay, or what broke that caused a call?
- **Banned openers.** An answer leading with "everyone", "obviously", "we believe", "users want", or "growing fast" is named as the pattern it is, out loud, so the pushback reads as a standard, not skepticism, and the question is re-asked at its evidence class.
- **Naked numbers.** A number without a unit, a period, and a source is routed to the assumptions register, not accepted as fact.
- **Two pushes, then park.** Section 2, rule 3. The cap is visible to the user from the first push.

A strong answer gets one line of acknowledgment and a harder follow-up, never praise that stalls the pace.

## 5. STATE.md: the file that carries the journey

`products/<name>/STATE.md` is the Conductor's memory and the fourth continuously written file in the workspace, alongside the decision log, the risk register, and the assumptions register. It is append-mostly: sections 3 through 5 only grow, and corrections are new rows, not edits. The blank template ships at `templates/execution/state.md`; the format is:

```
# STATE: <product name>
Updated: <YYYY-MM-DD> by <runtime or person>

## Position
Stage: <DISCOVER | DEFINE | DESIGN | BUILD | DELIVER | OPERATE>
Gate attempts: <gate n: attempt count and outcome, one line each>
Next question: <bank ID, e.g. DEFINE-5>
Overlays active: <AI: yes/no> <regulated: yes/no> <decided at: date, logged where>

## Accepted answers
| ID | Question (short) | Answer (one line) | Evidence class | Landed in |

## Open challenges
| ID | Answer offered | Why not accepted | Pushes used (n of 2) | Parked to |

## Evidence ledger
| E# | Claim | Verbatim quote | Source | Source date | Retrieved | Confidence |

## Journal
<one line per session: date, runtime, questions covered, artifacts touched>
```

Rules: the `Landed in` column is a workspace-relative path plus a section, so every answer is auditable against the artifact it produced. The evidence ledger holds the load-bearing sentence of each source verbatim, in quotation marks, because paraphrase drifts across sessions and a quote is checkable later. Confidence is one of: verified (two or more independent sources), single-source, contested, unverified. Contested rows name what disagrees.

## 6. The resume protocol

Any model, any runtime, mid-journey:

1. Read `products/<name>/README.md`, then STATE.md, then the newest file in `gates/`.
2. **Verify before trusting.** Spot-check two accepted answers against the artifacts their `Landed in` column names. A mismatch means STATE.md is corrected, as a new row noting the correction, before any new question is asked.
3. Re-run smart skip over the remaining bank for the current stage: anything the workspace now answers is marked accepted with its source.
4. Resume at the `Next question` ID, or at the oldest open challenge with pushes remaining.
5. Never re-ask an accepted answer. Re-open one only when new evidence contradicts it, and log the re-opening in the journal.
6. Append one journal line at session end, always.

In Method 2 (chat, no file access), the user pastes STATE.md at session start and the Conductor dictates the updated sections back at each acceptance for the user to save. The file format is the protocol; the runtime is interchangeable.

## 7. Model routing per stage

Method 4 splits each stage across the three tiers from [../routing/README.md](../routing/README.md), by blast radius, never by convenience:

| Work | Tier |
|---|---|
| Transcribing accepted answers into STATE.md and template fields; formatting; smart-skip lookups | extraction, `auto/cheap` |
| Drafting a template section from a set of accepted answers; gtm-plan and growth-plan first drafts | drafting, `auto/coding` |
| Cross-examination, gate-checklist evaluation, premortem, red team, reconcile-before-handoff, persist/pivot/sunset framing | judgment, `auto/reasoning:pro` |

Queue when the judgment tier is capped; never downgrade a cross-examination to the cheap tier, because an interrogation that cannot spot a weak answer is worse than a delayed one.

## 8. The product-analyst skill

`skills/product-analyst` is the DISCOVER and OPERATE research engine, a single-analyst distillation of a staged research pipeline. Its method, in order: decompose the question into sub-claims and named entities with a coverage check against the original ask; plan searches across three lenses (breadth, canonical primary sources, adversarial, meaning a deliberate hunt for who disagrees); write one evidence note per source carrying a verbatim load-bearing quote; name cross-source tensions in writing before drafting anything; commit a position per sub-question with a confidence label and a stated "what would change my mind"; run one adversarial pass against its own draft before handoff. The evidence-note format ships as `templates/discovery/evidence-note.md` and its rows feed the STATE.md evidence ledger directly.

[../agents/research-agent.md](../agents/research-agent.md) is upgraded in place rather than duplicated, since it already owns discovery evidence and the gap is additive: it gains the decomposition step at the top of its operating rules, the three-lens search plan, a verbatim-quote field in its output shape, a committed position per question, and one new section, "Reconcile before handoff," that plays sources against each other before findings reach any template. Per-source findings, however well cited individually, do not force their tensions into the open on their own; that step exists because nothing else in the chain does it.

## 9. Build plan: four builders, zero file overlap

Build order is B1, B2, B3, then B4, because B4's links must resolve against files the first three created. Each builder runs `python3 lint.py --os` before handing off. No file appears in two lists.

| Builder | Files (create unless marked edit) | Count |
|---|---|---|
| B1: Conductor core | `skills/conductor/SKILL.md`; `os/CONDUCTOR.md` (the full protocol: contract, challenge grammar, gate procedure, escape hatch, per-method notes); `skills/conductor/questions/README.md` (bank file format and the evidence ladder); `skills/conductor/questions/discover.md`, `define.md`, `design.md`, `build.md`, `deliver.md`, `operate.md` | 9 |
| B2: Analyst | `skills/product-analyst/SKILL.md`; `templates/discovery/evidence-note.md`; `agents/research-agent.md` (edit, per section 8) | 3 |
| B3: Workspace and planning | `templates/planning/gtm-plan.md`; `templates/planning/growth-plan.md`; `templates/execution/state.md`; `os/PRODUCT-WORKSPACE.md` (edit: STATE.md joins the layout and the never-archived list); `examples/conductor-transcript.md` (fictional, two stages, showing one full cross-examination and one refused advance); `examples/README.md` (edit: index the transcript) | 6 |
| B4: Integration | `README.md` (edit: the lead usage story becomes clone, open a runtime, say "start"); `CLAUDE.md` (edit: router rows for "start", "resume", "where are we"); `AGENTS.md` (edit: load order step 0 reads STATE.md when a product workspace exists; conductor and product-analyst rows); `system/BOOT-PROMPT.md` (edit: conductor mode and manifest additions); `system/ROLE-PROMPTS.md` (edit: Conductor role block); `routing/README.md` (edit: the stage-tier table from section 7); `routing/omniroute.config.json` (edit: taskMap entries for conductor and product-analyst); `CHANGELOG.md` (edit: 0.2.0 entry with known gaps); `docs/ARCHITECTURE.md` (edit: file tree and layer table gain the new files) | 9 |

Constraints binding all four: new templates carry the three-line Stage/Knowledge/Skill header; new SKILL.md files carry exactly `name` and `description` frontmatter with a "Use when" clause; triggering lives in CLAUDE.md and AGENTS.md, never inside a skill; nothing under `modules/regulated/` is touched; question banks cite knowledge cards by relative link when a question applies a method (the DELIVER bank cites the crossing-the-chasm index entry, the OPERATE bank cites [../knowledge/north-star-metric.md](../knowledge/north-star-metric.md), the DESIGN bank cites the premortem entry), because the Conductor names the framework it is applying and why, every time it applies one.

## 10. Anti-sloppiness rules, embedded verbatim in the Conductor prompt

These ship inside `skills/conductor/SKILL.md` and the Conductor role block, not only in this design.

1. "Everyone", "obviously", "we believe", "users want", and "growing fast" are never accepted as evidence; each triggers the challenge grammar.
2. Every question names its evidence class, and the Conductor demands that class, not a class-shaped sentence.
3. A number without a unit, a period, and a source is an assumption and is filed as one.
4. Two pushes per question, then park, visibly. An interrogation with no cap is hazing, not rigor.
5. The WHICH-DOCUMENT tree decides what gets written, and the honest output of an interview is sometimes one decision-log line and no document.
6. Model output is not evidence. The Conductor's own summaries, drafts, and inferences are labeled as such and never promoted into the evidence ledger.
7. Never ask what the loaded context already answers; cite the source of every skip.
8. Quotation marks are reserved for verbatim text. A framing phrase dressed as a quote loses the marks or gets cut.
9. The Conductor reports gate lines as pass, fail, or unknown with evidence beside each, and an unknown blocks exactly as a fail does.
10. The Conductor never signs, never invents a name or a citation to complete a field, and never advances silently. Every skip, park, and refusal is one visible line in STATE.md.

## 11. What the Conductor is deliberately not

Not a replacement for the four v0.1.0 usage methods: Method 1 users never see it, and every template remains fillable with a pencil. Not an autopilot: it produces filled artifacts and gate reports, and humans produce signatures. Not a chatbot personality layer: it has no name, no persona, and no small talk, because the interview is the product. And not a second source of truth: STATE.md points into the workspace artifacts, and where the two disagree, the artifact wins and STATE.md is corrected.
