# Glossary

Every term of art this repository uses in a specific way, defined once. Where a word has a general industry meaning and a narrower meaning here, the narrower one is given, because that is the one that changes what a template asks of you. Cross-links point at the file that governs the term; when a definition here and that file disagree, that file wins.

Related: [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md) for the beliefs behind these mechanisms, [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for where each layer lives, [docs/FAQ.md](docs/FAQ.md) for the questions the vocabulary provokes.

## A

- **Acceptance criteria.** Testable pass conditions for one requirement, written Given, When, Then, with edge and negative cases named. If a criterion cannot fail, it is a description. See [templates/definition/acceptance-criteria.md](templates/definition/acceptance-criteria.md).
- **ADR (architecture decision record).** A numbered record of one technical decision with its context and consequences, in Michael Nygard's format. Reversals write a new ADR and leave the original standing, because the pair is the evidence. See [templates/architecture/adr.md](templates/architecture/adr.md).
- **Affordance.** What an object's properties make possible for a user to do with it, independent of whether that possibility is signaled. See [knowledge/design/interaction-design-principles.md](knowledge/design/interaction-design-principles.md).
- **Agent.** Here, an instruction file that gives a model an identity and standing rules for a role, such as red teamer or release manager. Distinct from a skill, which is a procedure. See [agents/README.md](agents/README.md).
- **AI interaction spec.** The user-facing half of an AI feature's design: streaming, stop and regenerate, citations, confidence, ratings, and fallback and ephemeral-mode defaults, distinct from the model-facing half in the AI overlay. See [templates/ai/ai-interaction-spec.md](templates/ai/ai-interaction-spec.md).
- **AI overlay.** The extra questions that attach whenever the product itself contains a model: eval sets in place of prose criteria, guardrails with owners, red-team review. Applies at every document weight above ticket-only. See [templates/ai/eval-spec.md](templates/ai/eval-spec.md).
- **Angle-bracket field.** The one sanctioned blank in this tree, written `<like this>`. The lint gate treats other deferred markers as unanswered questions rather than placeholders.
- **APCA.** A perceptual contrast algorithm proposed for a future WCAG; not a ratified standard, and no accessibility check in this tree is named APCA. See [knowledge/design/visual-foundations.md](knowledge/design/visual-foundations.md).
- **Appetite.** From Shape Up: the time you are willing to spend on a problem, fixed before scope is designed, so scope flexes against time instead of the reverse. See [knowledge/shape-up.md](knowledge/shape-up.md).
- **Assumptions register.** The ledger where a belief goes when it is not evidence: assumption, confidence, validation method, validate-by date, owner. A belief with no date does not expire on its own. See [templates/definition/assumptions-register.md](templates/definition/assumptions-register.md).
- **Attribution line.** The opening line of every knowledge card and worksheet naming the originator and year, restated in this repository's words. Where a method has no single originator, the line says so rather than inventing one.

## B

- **Banned metric.** One of six literal number strings from the maintainer's own past drafts that no file in this tree may contain, blocked repository-wide by the [lint gate](lint.py). The list lives in the gate's own constant and is never spelled out in prose.
- **Bidi isolation.** Wrapping a span of text whose direction differs from its surroundings, such as a username inside a right-to-left sentence, so its characters do not reorder the text around it. See [knowledge/design/internationalisation-and-rtl.md](knowledge/design/internationalisation-and-rtl.md).
- **Blast radius.** How far a failure reaches before something stops it: which users, which data, which downstream systems. Asked at Gate 5 and in the [operational readiness review](templates/operate/operational-readiness-review.md).
- **Boot prompt.** The paste-anywhere prompt that installs the loop, the gate discipline, the roles, and the Conductor into any chat model with no file access assumed. See [system/BOOT-PROMPT.md](system/BOOT-PROMPT.md).
- **BRD, PRD, FRD, NFR.** The requirements stack, heaviest first: business objectives and sponsor sign-off, product intent and scope, functional detail, and non-functional targets. The heavy stack is one of five weights, not the default. See [os/WHICH-DOCUMENT.md](os/WHICH-DOCUMENT.md).
- **Brownfield.** Applying the templates to a product already live and already messy, including a Gate 1 reconstructed after the fact and labeled as reconstructed. Worked example: [examples/checkout-modernization-brownfield.md](examples/checkout-modernization-brownfield.md).

## C

- **Challenge grammar.** The named moves the Conductor uses when an answer misses its evidence class: category to name, interest to behavior, banned openers, naked numbers, then park. Naming the move makes pushback read as a standard rather than as skepticism. See [os/CONDUCTOR.md](os/CONDUCTOR.md).
- **Choice symmetry.** Whether accepting and declining an offer, or upgrading and downgrading, or subscribing and cancelling, cost the user the same number of steps and the same clarity. See [frameworks/design/choice-symmetry-audit.md](frameworks/design/choice-symmetry-audit.md).
- **Cognitive walkthrough.** A task-based inspection method that steps through one specific user goal, action by action, asking whether the interface's cues line up with what the user is trying to do next; the task-based variant of heuristic evaluation. See [frameworks/design/heuristic-evaluation.md](frameworks/design/heuristic-evaluation.md).
- **Conductor.** The interviewer that runs the loop one question at a time, asks before it writes, cross-examines twice at most, and refuses to advance a stage until its gate passes on evidence. It never signs. See [os/CONDUCTOR.md](os/CONDUCTOR.md).
- **Conformance level.** The WCAG level (A, AA, or AAA) a product commits to, set once in the NFR and inherited by the accessibility checklist rather than chosen there. See [templates/definition/nfr.md](templates/definition/nfr.md).
- **Cost of inaction.** What continuing exactly as you are costs per period, with the calculation shown. Not the value of the proposal, which is a different and friendlier number. Gate 1 refuses it as an assertion, because a problem nobody has priced cannot be compared with the other things the quarter could buy, and because the figure becomes the do-nothing row of the [business case](templates/planning/business-case.md), where it has to survive a sponsor who would rather spend the money elsewhere.
- **Counter-metric.** The number you watch to catch your own win being paid for elsewhere, such as activation rising while support contacts rise with it. Required in the [growth plan](templates/planning/growth-plan.md).
- **Cross-examination.** One push against a weak answer, capped at two per question with the cap announced, after which the answer is accepted as offered or parked. An uncapped interrogation is hazing, not rigor.

## D

- **Deceptive pattern.** An interface designed to produce a choice the user would not make with full information and equal effort, formerly called a dark pattern. See [knowledge/design/deceptive-design.md](knowledge/design/deceptive-design.md).
- **Decision log.** The numbered, append-only record of decisions with context, options, rationale, and decider. The cheapest artifact in the tree and the one that answers "why is it like this" six months later. See [templates/execution/decision-log.md](templates/execution/decision-log.md).
- **Design critique.** A facilitated review that improves the work in front of the room; it grants no approval and is distinct from the design review record, which signs. See [frameworks/design/design-critique.md](frameworks/design/design-critique.md).
- **Design review (the two-gate record).** The one signed record of an experience-design review, walked once before build and again on the live build before Gate 4. See [templates/architecture/design-review-record.md](templates/architecture/design-review-record.md).
- **Design system.** The shared components, tokens, and service-standard rules a product's UI draws on, treated as an internal product with its own maturity and adoption. See [knowledge/design/design-systems-and-tokens.md](knowledge/design/design-systems-and-tokens.md).
- **Design token.** A named, platform-independent design decision, such as a colour or a spacing step, that compiles to the values each platform actually uses, so a rebrand changes the token rather than every file that used the raw value. See [knowledge/design/design-systems-and-tokens.md](knowledge/design/design-systems-and-tokens.md).
- **DESIGN.md.** The product's own file of tokens, components, content, and accessibility rules, agent- and human-readable, landing at `products/<name>/DESIGN.md` beside STATE.md. See [templates/architecture/design-md.md](templates/architecture/design-md.md).
- **Domain card.** One market's effect on the loop: who can stop a launch there, which metrics practitioners are judged on, and how each of those metrics lies. Fintech is a pointer to the regulated module. See [knowledge/domains/README.md](knowledge/domains/README.md).
- **Door, one-way and two-way.** Whether a decision can be walked back. Two-way doors get decided fast and logged; one-way doors earn a memo and a named decider. See [templates/planning/decision-memo.md](templates/planning/decision-memo.md).

## E

- **Error budget.** The amount of unreliability an objective permits before feature work yields to reliability work. Stated as a field, never as a shipped number. See [templates/delivery/sla-slo-definition.md](templates/delivery/sla-slo-definition.md).
- **Escape hatch.** The bounded, loud path past a gate: the stage's two highest-stakes unanswered questions are forced first, then the skip is recorded in STATE.md and as a risk row quoting the gate's own warning. There is no quiet path.
- **Evaluator effect.** The finding that different evaluators running the same heuristic evaluation catch substantially different problem sets, which argues for more than one evaluator rather than for abandoning the method. See [frameworks/design/heuristic-evaluation.md](frameworks/design/heuristic-evaluation.md).
- **Evidence class.** The minimum strength of evidence a given question accepts, from the five-class ladder: observed behavior, artifact, named commitment, interview claim, team belief. Class five is a filing instruction, not a failure.
- **Evidence ladder.** The five classes above, strongest first, used by every question bank and by the gate rendering that maps checklist lines to accepted answers. See [os/CONDUCTOR.md](os/CONDUCTOR.md).
- **Evidence note.** One note per source: the claim, a verbatim load-bearing quote, the source, dates, and confidence. Rows feed the STATE.md evidence ledger. See [templates/discovery/evidence-note.md](templates/discovery/evidence-note.md).

## F

- **Forced pair.** The two questions a stage forces first when a user says "advance anyway", named in each question bank so the escape hatch cannot skip the expensive unknowns.
- **Framework worksheet.** A runnable sheet for one method: its scales, its arithmetic written out, the inputs it needs, an invented worked example, its trap, its skip line, and what it feeds. The how layer, as against the knowledge layer's why. See [frameworks/README.md](frameworks/README.md).

## G

- **Gate.** A named checklist that must pass, on evidence, before the next stage opens, closing with signature lines. Six of them, one per stage. A gate nobody can fail is a ceremony. See [os/STAGE-GATES.md](os/STAGE-GATES.md).
- **Gate attempt.** One numbered run at a gate, filed in the product workspace whether it passed or failed. A folder in which every gate passed on attempt one is the clearest tell that the gate is decorative.
- **Graceful degradation.** The design rule that the artifacts and gates keep working when the model is free-tier, offline, or wrong, because nothing in the knowledge, frameworks, template, or loop layers depends on an AI layer existing.
- **Greenfield.** A product with no existing implementation to accommodate, the case the loop reads most naturally in. Contrast brownfield.
- **Guardrail metric.** A limit set alongside a target so the target cannot be hit by damaging something else, for example latency held while conversion is pushed. Recorded in the [north star metric](templates/planning/north-star-metric.md).

## H

- **Heuristic evaluation.** An inspection method where evaluators judge an interface against a named set of usability principles, most often Nielsen's ten, rather than testing it with users. See [frameworks/design/heuristic-evaluation.md](frameworks/design/heuristic-evaluation.md).

## I

- **ILLUSTRATIVE.** The literal label an invented number carries when it sits where a measured one could be mistaken for it: on the worked case in every [knowledge card](knowledge/README.md), and inside the outputs of the agents that handle thresholds, costs and estimates. An unlabeled number in one of those places is a defect, and an ILLUSTRATIVE threshold can never reach evidenced-pass at a gate, because the test then passed against a figure nobody agreed. Elsewhere the same discipline runs under different words: `os/` and `frameworks/` say invented in prose, and the [learn paths](learn/README.md) prefix invented evidence with "invented:". Three forms, one rule.
- **Input metric.** A metric a team can move directly this week, sitting under the north star in the tree and owned by name. The north star is the outcome; input metrics are the levers. See [frameworks/metrics/north-star-input-tree.md](frameworks/metrics/north-star-input-tree.md).

## J

- **JTBD (jobs to be done).** The frame that treats the unit of demand as a job a person is trying to get done in a circumstance, rather than as a segment or a feature request. Used here in the narrow sense that makes it testable: a job statement is only usable if it still reads correctly when your company does not exist, and only load-bearing if it rules something off the roadmap. Sheet: [frameworks/discovery/jtbd-job-map.md](frameworks/discovery/jtbd-job-map.md). Why and how it fails: [knowledge/jobs-to-be-done.md](knowledge/jobs-to-be-done.md).

## K

- **Kano model.** The classification of product attributes by how satisfaction responds to their presence and absence: must-be, one-dimensional, attractive, indifferent, reverse. The classification is a reading of one population at one time, never a property of the feature, because attractive attributes decay into must-be as competitors ship them. Sheet: [frameworks/discovery/kano-survey.md](frameworks/discovery/kano-survey.md). Why and how it lies: [knowledge/kano-model.md](knowledge/kano-model.md).
- **Key result.** The measurable half of an OKR, with a baseline and a target. A key result that names a task rather than a movement is the field's most common OKR defect. See [knowledge/okrs.md](knowledge/okrs.md).
- **Kill criteria.** The conditions under which the team stops or rolls back, each with a threshold, a check point, and the person allowed to call it. Section 9 of the [PRD](templates/definition/prd.md), added because every system surveyed could start work and none could stop it.
- **Knowledge card.** One canonical method explained in this repository's words: why it exists, when to use it, its skip condition, its trap, and the templates that draw on it. The why layer. See [knowledge/README.md](knowledge/README.md).

## L

- **Ladder rung.** One step on the eight-rung product ladder from Associate PM to CPO, each with what it owns, decides, and how it fails. Rung names are marked directional, because titles are software's least standardized vocabulary. See [knowledge/roles/ladder.md](knowledge/roles/ladder.md).
- **Learn path.** One stepped curriculum over fictional products, ending at a real gate checklist as a capstone. Three exist: foundations, transitioning, senior. Practice work never lands in `products/`. See [learn/README.md](learn/README.md).
- **Lint gate, tree mode.** `python3 lint.py --os`, the eleven-check whole-tree gate: characters, banned metrics, placeholders, links, template headers, skill frontmatter, pinned-file integrity, system-prompt paths, secrets, graph declarations, wikilinks. Green means consistent, not true.
- **Loop, the operating loop.** Six stages, DISCOVER through OPERATE, each closing at a gate, with Gate 6 feeding DISCOVER again. Two tracks run across it: planning, and the AI overlay. See [os/OPERATING-LOOP.md](os/OPERATING-LOOP.md).

## M

- **Mandate lane.** The separate, unscored lane for compliance items, contract commitments, and scheme rules. They take capacity first, pinned to the quarter their date demands, because scoring a legal deadline against a revenue feature produces a number that looks like a decision and is not one. See [frameworks/prioritization/rice-scoring-sheet.md](frameworks/prioritization/rice-scoring-sheet.md).

## N

- **Never-invent rule.** The standing prohibition in [AGENTS.md](AGENTS.md) against originating a fact, a name, a number, a date, a citation, or a quote. An unknown is written as an open field with an owner, never filled with a plausible value, because a fabricated figure reads exactly like a measured one at the same font size and survives to the gate that a thin answer would have failed. The rule binds this repository's own prose as much as anything produced inside it.
- **North star metric.** The single metric expressing the value customers get, sitting above a tree of input metrics with owners and guardrails. One per product; a second one is a reorganization in disguise. See [knowledge/north-star-metric.md](knowledge/north-star-metric.md).

## O

- **One-pager.** The light DEFINE weight: problem, proposal, scope, one metric plus a guardrail, a not-doing list, up to three acceptance criteria. Promoted to a PRD when it stops fitting, and the promotion is logged. See [templates/definition/one-pager.md](templates/definition/one-pager.md).
- **Overlay.** A set of questions that attaches across stages rather than sitting inside one: planning, AI, and regulated. Overlays sit on top of the document weight, never inside it.

## P

- **Parked answer.** A weak answer that survived two pushes and went to the assumptions register with an owner and a validate-by date, visible in STATE.md under open challenges; the local PMOS runtime always takes this path on the third invalid submission, since it has no call that accepts an answer as offered. Parking is the alternative to silent acceptance.
- **Pencil path.** Running the whole system with no model at all: copy a template, fill it in any editor, work the gate checklist by hand. Method one of the five in [README.md](README.md).
- **Postmortem, blameless.** The per-incident review written in systems language with no names: facts, timeline, quantified impact, corrective actions with owners and verification. See [templates/operate/incident-postmortem.md](templates/operate/incident-postmortem.md).
- **Premortem.** The exercise of assuming the launch already failed and writing the causes, run before Gate 3, because a team that has named nine failure modes in advance recognizes the first one in week two. See [frameworks/execution/premortem-worksheet.md](frameworks/execution/premortem-worksheet.md).
- **Product workspace.** `products/<name>/`, the folder where filled artifacts, gate attempts, and STATE.md accumulate as a product's memory. Gitignored, never shipped here, so your work cannot collide with an update. See [os/PRODUCT-WORKSPACE.md](os/PRODUCT-WORKSPACE.md).

## Q

- **Question bank.** One file per stage at [skills/conductor/questions/](skills/conductor/questions/README.md), holding the questions that stage asks, the evidence class each one accepts, its Accept-when line, and the forced pair the escape hatch cannot skip. Banks are read-only in tutor mode, so the interview and the quiz grade against the same wording rather than against two drifting copies.

## R

- **Reach unit.** The single counting unit declared before a scoring sheet is filled, for one sheet only. Filers and reports are not comparable, because one filer files many reports, and unit drift decides rankings by a bookkeeping accident.
- **Reflow.** Content re-laying-out to a single column at high zoom instead of requiring two-dimensional scrolling, the WCAG 2.1 and 2.2 test (success criterion 1.4.10) for whether zoomed content stays usable. See [knowledge/design/visual-foundations.md](knowledge/design/visual-foundations.md).
- **Regulated overlay.** The byte-exact imported module for products that contain an AI or machine-learning feature **and** have a financial or data regulator applying to them: a section-0 regulatory register, eval-set criteria, guardrails with owners, its own review gate. Activates at Gate 2 and Gate 5, and only when both halves hold, because the module covers two AI-specific instruments and nothing else. A regulated product with no model in it gets no coverage here. The narrowed rule in [os/STAGE-GATES.md](os/STAGE-GATES.md) governs; the module's own README at [modules/regulated/README.md](modules/regulated/README.md) retains the broader wording, so read it against the gate file.
- **RICE.** Reach times impact times confidence, divided by effort: four beliefs written down and turned into one comparable number. Treated here as a bucketing device rather than a ranking, because two scores within about a fifth of each other sit inside the error bars of their own inputs. The number is the receipt; the argument required to produce it is the product. Sheet: [frameworks/prioritization/rice-scoring-sheet.md](frameworks/prioritization/rice-scoring-sheet.md). Why it gets gamed: [knowledge/rice-prioritization.md](knowledge/rice-prioritization.md).
- **Routing tier.** Which class of model runs a task: extraction on a cheap tier, drafting on a coding tier, judgment on a frontier reasoning tier. Paying frontier prices to reformat a table is waste; the reverse is worse. See [routing/README.md](routing/README.md).

## S

- **Signifier.** A perceivable cue that communicates where an action is possible, distinct from the affordance itself; a button still needs a signifier even where its affordance, clickability, is real. See [knowledge/design/interaction-design-principles.md](knowledge/design/interaction-design-principles.md).
- **Skill.** Here, a procedure a model executes end to end, such as writing a PRD or running the weekly product review. Distinct from an agent, which is an identity. See [skills/README.md](skills/README.md).
- **Skip line.** The line beginning "Skip it when" carried by every card and worksheet, naming the situation where running the method costs a week and returns nothing. Written as a test on the situation, so someone else in the room can check it; "we are busy" is a schedule, not a skip condition.
- **Skip-risk warning.** The sentence each gate in [os/STAGE-GATES.md](os/STAGE-GATES.md) carries naming what advancing without this evidence has historically cost, quoted verbatim into the risk register when the escape hatch is used. Distinct from a skip line, which excuses a method; this one prices a decision. It exists because a gate waved through in the abstract costs nothing to wave through, and the warning makes the person doing it wave through something specific, in writing, with their name beside it.
- **Smart skip.** The Conductor's rule against asking what the loaded context already answers: the question is marked accepted with its source cited and the skip is shown in one line. This is why a prepared user gets a short interview.
- **Snowflake component.** A one-off UI element built instead of reused from the shared library, tracked as UX or design-system debt because each one is a small maintenance cost that compounds. See [templates/execution/tech-debt-register.md](templates/execution/tech-debt-register.md).
- **Stage.** One of the six phases of the loop, each with a written entry and exit definition and exactly one gate at its end.
- **STATE.md.** One product's per-session memory: position in the loop, accepted answers, open challenges, evidence ledger, journal. Append-mostly, and the reason any later session in any runtime can resume. Blank at [templates/execution/state.md](templates/execution/state.md).
- **Sunset.** The end of the loop chosen on purpose at Gate 6: rationale, timeline, migration path, comms cascade, decommission steps. See [templates/operate/sunset-eol-plan.md](templates/operate/sunset-eol-plan.md).
- **Superset template.** Every template here, deliberately. The instruction that comes with it is to delete what does not apply, because an empty section reads as an unanswered question and teaches readers to skim.
- **SUS (System Usability Scale).** A ten-item, five-point attitude survey producing one score out of 100, the most studied usability questionnaire in use. See [frameworks/design/ux-scorecard.md](frameworks/design/ux-scorecard.md).

## T

- **Target size.** The minimum tappable or clickable area for a control, 24 by 24 CSS pixels at WCAG 2.2's 2.5.8 criterion, with named exceptions. See [templates/architecture/accessibility-checklist.md](templates/architecture/accessibility-checklist.md).
- **Tell.** The observable symptom that reveals a failure mode while it is still cheap, given alongside the failure mode itself throughout the tree, because a named defect you cannot detect is trivia.
- **Trap.** The section in every card and worksheet naming how the method fails in practice, usually by producing an output that borrows authority its inputs never earned.
- **Triad.** Product, design, and engineering deciding value, usability, and feasibility respectively, with a written dispute path ending in the decision log and no veto for any leg. See [knowledge/roles/triad-decision-rights.md](knowledge/roles/triad-decision-rights.md).
- **Tutor mode.** The learn layer's quizmaster: questions drawn read-only from the Conductor's banks, one push then a model answer, scored 0, 1, or 2 on the evidence ladder. See [learn/skills/tutor/SKILL.md](learn/skills/tutor/SKILL.md).

## U

- **UI state inventory.** The single owner of the list of states a screen or component must render, such as empty, loading, or error, referenced rather than restated by the component spec, the content audit, the review record, and the localisation checklist. See [templates/definition/ui-state-inventory.md](templates/definition/ui-state-inventory.md).
- **UMUX-LITE.** A two-item usability questionnaire that correlates closely with the full SUS at a fraction of the length. See [frameworks/design/ux-scorecard.md](frameworks/design/ux-scorecard.md).
- **UX debt.** Tech debt a user feels rather than one a compiler flags: a rework or workaround the interface forces on a user, tracked with severity, frequency, and journey location alongside technical and design-system debt. See [templates/execution/tech-debt-register.md](templates/execution/tech-debt-register.md).

## W

- **Weight.** How much document a decision deserves, chosen before a template opens by three questions, stakes, audience, reversibility, across five levels from a logged decision to the full requirements stack. Upgrading is normal, downgrading is a decision, and both get a line in the log. See [os/WHICH-DOCUMENT.md](os/WHICH-DOCUMENT.md).

## Z

- **Zombie spec.** A specification whose last edit predates the last three shipped changes and which the tracker still calls the source of truth. The remedy is to cut it to the decisions it records and mark the rest superseded, never to update it into fiction. See [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md).
