# Changelog

Every notable change to this repository is recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this repository uses [semantic versioning](https://semver.org/spec/v2.0.0.html).

What a version number means here, since this is a document system and not a library:

- **MAJOR** changes rename or remove a template field, move or delete a file that other files link to, or change what a gate demands. These are the changes that break a fork or a half-filled document, so they only happen on a major version, and this file names the migration for each one.
- **MINOR** adds a template, a knowledge card, a skill, or a section. Existing filled documents keep working untouched.
- **PATCH** fixes wording, links, typos, or a lint rule that was wrong.

The stability promise is stated in [README.md](README.md) and repeated here so it survives a fork: within a major version, template field names and file paths do not change under you.

## Unreleased

Nothing yet.

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
