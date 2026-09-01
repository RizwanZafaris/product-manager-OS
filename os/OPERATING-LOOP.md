# The Operating Loop

One product, six stages, six gates. A stage opens when the previous gate is signed and closes when its own gate is signed. Gates are documents, not ceremonies: the checklists live in [STAGE-GATES.md](STAGE-GATES.md), and a full narrative pass is in [HOW-TO-RUN-A-PRODUCT.md](HOW-TO-RUN-A-PRODUCT.md).

Two decisions come before any template gets filled. How heavy should the artifact be: [WHICH-DOCUMENT.md](WHICH-DOCUMENT.md) answers that in three questions. Where does the filled copy live: [PRODUCT-WORKSPACE.md](PRODUCT-WORKSPACE.md) defines the folder convention that becomes the product's memory.

The loop is a loop. Gate 6 does not end the product; it decides whether the next pass through DISCOVER is a deepening, a pivot, or a sunset.

```
DISCOVER -> [Gate 1] -> DEFINE -> [Gate 2] -> DESIGN -> [Gate 3]
        -> BUILD    -> [Gate 4] -> DELIVER -> [Gate 5] -> OPERATE -> [Gate 6] -> loop
```

## The six stages

### 1. DISCOVER

Find a problem worth solving and prove someone has it.

- **Entry:** a trigger worth investigating: a metric moved, a customer pattern repeated, a strategic bet was named. Or Gate 6 from a previous pass sent you back here.
- **Work:** frame the problem, plan and run research, meet users, map their journey. Templates: `../templates/discovery/problem-framing.md`, `../templates/discovery/user-research-plan.md`, `../templates/discovery/personas.md`, `../templates/discovery/journey-map.md`, and `../templates/discovery/competitive-analysis.md` when a specific decision needs it, all rolled up into `../templates/discovery/discovery-document.md`. Raw feedback becomes weighted themes through `../skills/feedback-synthesis/SKILL.md` before it enters any of them.
- **Exit:** Gate 1, problem worth solving. Evidence from real users, a cost of inaction, and an explicit go or no-go. A no-go here is a success: it cost a week, not a quarter.

### 2. DEFINE

Turn the validated problem into requirements someone can build, test, and sign.

- **Entry:** Gate 1 signed.
- **Work:** business case (`../templates/definition/brd.md`), product requirements (`../templates/definition/prd.md`, or `../templates/definition/one-pager.md` at the lighter weight), functional detail (`../templates/definition/frd.md`), non-functional targets (`../templates/definition/nfr.md`), business rules, the assumptions register, and acceptance criteria that can actually fail. Pick the weight first with `WHICH-DOCUMENT.md`; the gate asks the same questions either way.
- **Exit:** Gate 2, requirements signed off. Every requirement testable, every assumption registered, sponsor named. Regulated products answer the regulated overlay's precondition questions here, before design starts, because a license condition beats a sprint plan every time.

### 3. DESIGN

Decide how it will be built and what could go wrong, before anything is built.

- **Entry:** Gate 2 signed.
- **Work:** system and solution architecture, decision records, data model, API contracts, sequence diagrams, integrations, security architecture, observability plan (all under `../templates/architecture/`). In parallel, the execution set: stakeholder map, risk register, decision log, dependency register (`../templates/execution/`).
- **Exit:** Gate 3, architecture and risks reviewed. Alternatives were considered on paper, the premortem ran, and every high risk has an owner.

### 4. BUILD

Build to the spec, and keep the spec honest as reality pushes back.

- **Entry:** Gate 3 signed.
- **Work:** the testing strategy, edge-case and failure-scenario tables (`../templates/delivery/`), acceptance criteria verified case by case, scope changes written into the decision log rather than absorbed silently.
- **Exit:** Gate 4, acceptance criteria met. Not "code complete": criteria demonstrated, edge cases covered by tests, known misses documented with owners.

### 5. DELIVER

Ship it on purpose, with a way back.

- **Entry:** Gate 4 signed.
- **Work:** UAT with real users against entry and exit criteria (`../templates/delivery/uat-plan.md`), release readiness (`../templates/delivery/release-readiness.md`), rollback rehearsed, comms drafted.
- **Exit:** Gate 5, release readiness green. Go or no-go signed per function, rollback tested, known issues listed rather than hoped away. Regulated products re-check their overlay here: what was promised in section 0 at DEFINE must be true in the thing that ships.

### 6. OPERATE

Run it, measure it, and let the numbers decide what happens next.

- **Entry:** Gate 5 signed and the release is live.
- **Work:** operational readiness (`../templates/operate/operational-readiness-review.md`), compliance impact where applicable, and the metrics review (`../templates/operate/metrics-review.md`) against the targets set back in DEFINE.
- **Exit:** Gate 6, outcomes verified. The explicit decision: persist, pivot, or sunset. Each of the three loops back to DISCOVER with what was learned. Skipping this gate is how zombie products are born.

## The overlays

Three tracks run across the loop rather than inside one stage.

**PLANNING** feeds every stage. The roadmap (`../templates/planning/roadmap.md`) says which products enter the loop and when; OKRs (`../templates/planning/okrs.md`) supply the targets that Gate 6 verifies. A new owner taking over a product in flight starts at `../templates/planning/first-90-days.md`. Planning artifacts are reviewed on their own cadence, not at a gate.

**AI OVERLAY** activates whenever the product itself contains a model. The `../templates/ai/` set (eval spec, guardrails, hallucination controls, human approval gates, prompt structure, context management, agent architecture, multi-agent workflow, red-team review) attaches to DEFINE and DESIGN, and its eval thresholds become blocking checks at Gate 4 and Gate 5. A model feature with prose acceptance criteria cannot pass Gate 2: a requirement that cannot fail is not a requirement.

**REGULATED OVERLAY** activates when the product operates under a financial or data regulator. It lives in `../modules/regulated/` as a byte-exact import, is routed through `../skills/reg-gap-check/SKILL.md`, and hooks into the loop at Gate 2 (preconditions answered before requirements freeze) and Gate 5 (overlay re-verified before release). Files under the module are never edited in this repository.

## Rules of the loop

1. **No stage without its gate.** Work that skips a gate is inventory, not progress.
2. **Gates fail.** A gate that cannot fail is a ceremony. Expect some no-gos; they are the system working.
3. **Backward is allowed, silent backward is not.** Discovering at BUILD that a requirement was wrong sends you to Gate 2 explicitly, with the decision log updated.
4. **Evidence over confidence.** Every gate asks where a claim came from. "The model said so" is not a source.
5. **The loop ends on purpose.** Sunset is a Gate 6 outcome with its own checklist, not an abandonment.
6. **Filled artifacts accumulate in one place.** One folder per product, one subfolder per stage, per [PRODUCT-WORKSPACE.md](PRODUCT-WORKSPACE.md). A decision recorded where nobody will find it was recorded for nobody.
