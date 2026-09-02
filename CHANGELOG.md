# Changelog

Every notable change to this repository is recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this repository uses [semantic versioning](https://semver.org/spec/v2.0.0.html).

What a version number means here, since this is a document system and not a library:

- **MAJOR** changes rename or remove a template field, move or delete a file that other files link to, or change what a gate demands. These are the changes that break a fork or a half-filled document, so they only happen on a major version, and this file names the migration for each one.
- **MINOR** adds a template, a knowledge card, a skill, or a section. Existing filled documents keep working untouched.
- **PATCH** fixes wording, links, typos, or a lint rule that was wrong.

The stability promise is stated in [README.md](README.md) and repeated here so it survives a fork: within a major version, template field names and file paths do not change under you.

## Unreleased

Nothing yet.

## 0.4.0, 2026-09-02

The gap-audit release: ten files a practitioner would actually reach for, plus four sharpened edits. A minor version because everything is added; no field renames, no file moves, and every edit is an appended section or column, so a document filled against 0.3.0 keeps working untouched.

### Added

- **Incident postmortem.** `templates/operate/incident-postmortem.md`: blameless per-incident review with facts, severity, timeline, quantified impact, systems-language cause rows that carry no names, what worked, and corrective actions with owner, due date, and verification. Verified actions feed section 6 of the operational readiness review. The discipline restates Google SRE postmortem culture and Amazon's Correction of Error practice in this repository's own words.
- **Model card.** `templates/ai/model-card.md`: intended use and explicit out-of-scope uses, known limitations citing the eval spec and red-team review by path, performance with segment variance, data provenance, and an update policy with a contact. After Mitchell and coauthors' Model Cards for Model Reporting. Feeds Gate 5; the regulated module wins on overlap, same rule as the eval spec.
- **Partner integration brief.** `templates/planning/partner-integration-brief.md`: one lean go or no-go file per partnership, at one-pager weight, with the exchange, the evidenced user problem, a Team-API surface and owner table, commercial shape and exit terms, and dependency and data-sharing risk rows. The decision lands in the decision log.
- **Opportunity solution tree.** `templates/discovery/opportunity-solution-tree.md`: Torres's structural tool as diffable tables, with evidence-cited opportunity branches, minimum two solutions per targeted opportunity or a labeled single-solution bet, tagged assumptions, and this week's test. Closes the gap where the Torres card named the tree and no template built one.
- **Service blueprint.** `templates/discovery/service-blueprint.md`: one scenario, eight to twelve actions, frontstage and backstage and support systems, line-of-visibility failure points each with an owner. Shostack's form, NN/g's scoping discipline.
- **Feedback program.** `templates/operate/feedback-program.md`: the charter for a standing CAB, beta, or panel, with the decision the program informs, recruiting and curation rules, cadence, NDA and incentive and data-handling terms, intake routed to evidence notes, and exit criteria for the program itself.
- **Two skills.** `skills/product-review/SKILL.md`, the weekly truth-seeking WIP walk with the 48-hour pre-read and same-day decision-log landings; `skills/escalation/SKILL.md`, the stuck-decision brief (Situation, Impact, Urgency, Options, Recommendation, Ask) with a routing ladder and SLAs, feeding the risk register and decision log.
- **Two role cards.** `knowledge/roles/triad-decision-rights.md`, who decides value, usability, and feasibility, the how-might-we-never-a-veto rule, a three-step dispute path ending in the decision log, and the saying-no pattern; `knowledge/roles/pm-hiring-and-growth.md`, the structured hiring loop and the manager 1:1 and career conversation, both calibrated against the ladder.
- **Wiring.** Index rows, README and AGENTS and architecture-tree entries, boot-prompt manifest lines, router rows for the two new skills, a WHICH-DOCUMENT trigger line for the partner brief, pointer-only conductor bank lines (discover, deliver, operate; `os/CONDUCTOR.md` untouched), Torres card Used-by extensions, and three pointer lines: VPAT/ACR and localization in the NFR template, pricing experiments in pricing-packaging.

### Changed

- **Eval spec** (`templates/ai/eval-spec.md`, all additive): a Trace source and error analysis block with a failure-cluster table, so scenarios map to observed clusters or are labeled synthetic; a Grader type column with the rule that model graders are validated against held-out human labels before they gate; section 3 split into a capability suite (deliberately hard) and a regression suite (CI-gated); an agentic worked micro-example grading against external state, with pass@k versus pass^k stated. Exit gate extended to match.
- **Gate 5 run of show** (`os/STAGE-GATES.md`, Gate 5 only): chair, attendees, the 48-hour pre-read SLA, demo-not-slides, and a CONDITIONAL GO outcome that requires a named owner and close-by date per condition.
- **Roadmap builder** (`skills/roadmap-builder/SKILL.md`): a stakeholder-conversations step after scoring, using the saying-no moves from the triad card, and a Planning as a process section (strategy session three weeks out, team breakouts, capacity negotiation, QBR separated from initiative review).
- **QBR board update** (`templates/operate/qbr-board-update.md`): a cadence practice note; weekly async narrative with three to five commitments, monthly exception-only live review, the document itself stays quarterly.

### Known gaps

- The postmortem's no-names rule is enforced by the exit gate checklist, not by lint; a name in a cause row passes the tree gate and fails only a human reader.
- The model card inherits eval-spec numbers by citation, not by extraction; the two can drift between updates, and the card's update policy is what catches it.
- The partner brief sizes the decision, not the integration; a yes still needs its own api-contract and integrations rows, and nothing checks that they follow.
- The escalation ladder names roles, not people; an org that never fills in the ladder gets the same governance-without-decision-rights failure the skill exists to fix.

## 0.3.0, 2026-09-02

The expansion release: who you are, where you play, and how to study. A minor version because everything is added; no field is renamed, no file moves, and every new gate line accepts "none" as an answer, so a document filled against 0.2.0 keeps working untouched.

### Added

- **The roles layer.** `knowledge/roles/`: an eight-rung ladder from Associate PM to CPO with the IC and management fork after Senior PM, the specializations card (including the product-owner split argument on both sides), the PM and PMM boundary as a decision table, and the stage-shift card on what one title means at three company sizes. Rung names are marked directional until primary ladder sources are collected.
- **The domains layer.** `knowledge/domains/`: ten market cards, each with the questions to ask before trusting a plan, the gatekeepers who can block a launch, a metrics table with a how-it-lies column, attributed readings, and the Conductor questions and templates the domain bends. Fintech is a pointer card that routes to `modules/regulated/` and duplicates nothing.
- **Sixteen templates** across the existing categories. Planning: vision, product strategy, north star sheet, positioning, pricing and packaging. Discovery: opportunity assessment, discovery synthesis, JTBD spec. Definition: PR/FAQ. Delivery: analytics instrumentation spec, launch comms plan. Operate: experiment brief, win-loss review, QBR board update, post-launch review, sunset and EOL plan. The sunset plan closes the "discovery to sunset" loop the README promises.
- **Routing notes** in `os/WHICH-DOCUMENT.md`: a trigger table placing the sixteen new documents around the weight ladder, and route-do-not-build notes for the four documents people ask for by name (MRD, business case, sales one-pager, stakeholder newsletter).
- **The learn layer.** `learn/`: three stepped paths over fictional products (foundations, transitioning, senior sharpening), each ending at a real gate checklist as its capstone; a library of attributed book and podcast pointers; a tutor skill that quizzes from the Conductor's question banks read-only and scores 0/1/2 on the evidence ladder; and a practice workspace convention that keeps invented evidence labeled and out of `products/`.
- **Conductor touch points**, all additive: DISCOVER-8 (which domain pack governs this product) at the end of the discover bank, an optional `Domain:` line in the STATE.md position block, one Gate 1 checklist line accepting a card or "none", and router rows for learn mode, domains, and roles in CLAUDE.md and AGENTS.md. `os/CONDUCTOR.md` is untouched.
- **Index entry.** April Dunford's positioning method joins the knowledge index; eighteen entries now. New templates that lean on full cards extend those cards' Used-by lists.

### Known gaps

- Ladder rung names are directional, not verbatim: no per-company leveling text is cited yet, and the cards say so in three places.
- Two legal claims in the domain cards (loot-box law by market, the drone rule's current status) are marked verify-before-relying in the card rather than cited, honoring the no-invented-citation rule.
- Domain cards are cards only. No per-domain template pack exists, by rule: a pack ships when a card proves insufficient in real use.
- The tutor scores against recorded model answers and the evidence ladder; it cannot grade taste, and a confidently wrong artifact with good structure can outscore an insightful messy one.
- The learn paths' capstones use real gate checklists but fictional evidence; passing a capstone proves format fluency, not product judgment.

## 0.2.0, 2026-09-02

The Conductor release: the repository learns to ask before it writes. A minor version because everything here is added; nothing is renamed, moved, or demanded differently, and a document filled against 0.1.0 keeps matching its template.

### Added

- **The Conductor.** A stage-gated interviewer that runs the six-stage loop as a sequence of interviews. One question at a time, each with a recommended default and lettered options; weak answers cross-examined at most twice, then parked visibly; every accepted answer written into STATE.md and its template field before the next question; stage exit only when the gate checklist passes on evidence, signed by a human, never by the Conductor. Protocol at `os/CONDUCTOR.md`, entry skill at `skills/conductor/SKILL.md`, per-stage question banks under `skills/conductor/questions/`, design rationale at `docs/CONDUCTOR-DESIGN.md`.
- **STATE.md.** `templates/execution/state.md`: the append-mostly file that carries a product's journey. Position, accepted answers, open challenges, an evidence ledger with verbatim quotes, and a session journal, plus the resume protocol that lets any runtime, including a file-less chat model, pick up mid-journey.
- **The product-analyst skill.** `skills/product-analyst/SKILL.md`, the DISCOVER and OPERATE research engine: decompose the question, search across three lenses including a deliberate hunt for who disagrees, one evidence note per source with a verbatim load-bearing quote, cross-source tensions named in writing, one adversarial pass before handoff. `agents/research-agent.md` upgraded in place with the same method. Note format at `templates/discovery/evidence-note.md`.
- **Planning templates.** `templates/planning/gtm-plan.md` (written at DELIVER) and `templates/planning/growth-plan.md` (written at OPERATE).
- **Runtime integration.** Router rows for "start", "resume", and "where are we" in CLAUDE.md; load-order step 0 in AGENTS.md reads STATE.md whenever a product workspace exists and offers the conducted path when none does; Conductor mode and manifest additions in `system/BOOT-PROMPT.md`; a Conductor block in `system/ROLE-PROMPTS.md`; the per-stage tier table in `routing/README.md` with matching taskMap entries in `routing/omniroute.config.json`.
- **Worked example.** `examples/conductor-transcript.md`: two stages of a fictional interview, including one full cross-examination and one refused advance.
- **Knowledge card.** `knowledge/crossing-the-chasm.md`, graduated from the index under its own rule because the new GTM plan template depends on it. Eleven cards now, seventeen index entries.

### Known gaps

- Smart skip matches recorded text, not meaning. A fact filed under an unexpected heading gets asked again.
- In Method 2, STATE.md persistence is manual. The Conductor dictates every update, and a user who closes the session without saving the last dictation loses that delta.
- The resume protocol spot-checks two accepted answers against their artifacts, not all of them. Drift beyond the sample survives until the stage's gate.
- Question banks are fixed files. There is no supported way yet to add organization-specific questions without editing the banks, which a product run is forbidden to do.
- `lint.py` checks this tree, not user workspaces. A malformed STATE.md under `products/` surfaces at resume time, not at lint time.

## 0.1.0, 2026-09-02

First public release. Honest inventory of what exists, rather than a list of what was done to get here.

### Added

- **The operating loop.** Six stages and six gates in `os/`: `OPERATING-LOOP.md` (stage entry and exit definitions), `STAGE-GATES.md` (six fill-in gate forms with sign-off lines and skip-risk warnings), `HOW-TO-RUN-A-PRODUCT.md` (one fictional product taken through all six gates), `WHICH-DOCUMENT.md` (how much document a decision deserves), and `PRODUCT-WORKSPACE.md` (where a product's filled artifacts live).
- **Templates**, fill-in and editor-only, across seven groups: `discovery/` (six, including competitive analysis), `definition/` (eight, including the one-pager weight), `architecture/` (nine), `execution/` (four), `delivery/` (five), `operate/` (three), `planning/` (three, including the first 90 days), and the `ai/` overlay (nine).
- **Knowledge layer.** Ten canon cards with named attribution, a stated trap, and a "skip it when" line, plus an index of eighteen more methods in one line each.
- **Skills**: `ai-prd`, `roadmap-builder`, `program-premortem`, `reg-gap-check`, `feedback-synthesis`. **Agents**: research, drafting, validation, red team, Hermes.
- **System prompts** for models with no file access: `system/BOOT-PROMPT.md` with a file manifest, and five copyable role blocks in `system/ROLE-PROMPTS.md`.
- **Routing** for API-tier use: `routing/omniroute.config.json` and its tier doctrine.
- **The regulated overlay** at `modules/regulated/`, a byte-exact import from its canonical source repository, hash-pinned by the quality gate and never edited here.
- **Worked examples** in `examples/`: a greenfield discovery document and PRD for a fictional expense copilot, and a brownfield example of a legacy checkout modernization that carries a reversed decision.
- **Quality gate.** `lint.py` in two modes: the original regulated PRD gate, and `--os` tree mode with nine whole-tree checks. `test_lint.py` covers every check.

### Known gaps

Stated rather than hidden, because a changelog that only lists wins is marketing.

- The gate does not check traceability between documents: a requirement ID that exists in a PRD and nowhere else passes.
- `knowledge/` holds canon, not per-product memory. Product memory is a folder convention in `os/PRODUCT-WORKSPACE.md`, not software.
- Install is `git clone`. There is no packaged plugin, and no plugin manifest is validated in CI.
- The banned-metric check matches literal strings, so a spelled-out variant walks through it.
