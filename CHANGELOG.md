# Changelog

Every notable change to this repository is recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this repository uses [semantic versioning](https://semver.org/spec/v2.0.0.html).

What a version number means here, since this is a document system and not a library:

- **MAJOR** changes rename or remove a template field, move or delete a file that other files link to, or change what a gate demands. These are the changes that break a fork or a half-filled document, so they only happen on a major version, and this file names the migration for each one.
- **MINOR** adds a template, a knowledge card, a skill, or a section. Existing filled documents keep working untouched.
- **PATCH** fixes wording, links, typos, or a lint rule that was wrong.

The stability promise is stated in [README.md](README.md) and repeated here so it survives a fork: within a major version, template field names and file paths do not change under you.

## Unreleased

Nothing yet.

## 0.6.0, 2026-09-03

The depth release. Nothing new was added to the loop; the existing files were made
worth reading. The trigger was a blunt review: a lot is missing to be called a
product OS. The diagnosis behind that verdict was uneven depth rather than missing
coverage. The frameworks layer averaged 87 lines a worksheet and carried its
arithmetic, its scales, its trap and its skip line, while the knowledge cards next
to it averaged 34 lines and mostly restated what the worksheet already said. A
reader who opened a card after opening a worksheet learned nothing from the second
file, which is the same defect as a missing file with an extra maintenance cost
attached.

Four layers were rewritten inside their existing skeletons: every heading, header
block, exit gate, attribution line, skip line and cross-link that was there before
is still there, and every addition is a new block within the same shape. So a
document filled against 0.5.1 keeps working, and a link written into your own notes
keeps resolving. That makes this a minor version even though it is the largest diff
in the repository's history: 22,341 lines of markdown to 25,961, with four files
added and none moved, renamed, or deleted.

The rule that governed the rewrite is worth stating, because it is what stops a
depth pass from becoming a padding pass. `frameworks/` files are the working
sheets: how to run a method, fill it, and score it. `knowledge/` cards are the why
layer: why the method exists, the mechanism that makes it work, when it fails, and
how it lies. Every deepened card was written with its paired worksheet open, and
the rule held everywhere except one block, which a review caught: the
What-good-looks-like table added to eleven cards. On the four cards that have a
paired worksheet, that table had turned the sheet's own steps into virtues, so a
declared reach unit and a class-per-action rule were being read twice. Those four
tables were rewritten to test what a worksheet cannot check, which is the
organizational evidence that the instrument has authority: whether the sheet ever
reversed an announced decision, whether an input owner changed their week,
whether a losing sponsor can name the cell rather than the score. The other seven
cards have no paired worksheet to duplicate. The same line separates `skills/`,
which hold procedures, from `agents/`, which hold identities; the one pre-existing
sentence that appeared in both `agents/research-agent.md` and
`skills/product-analyst/SKILL.md` was cut down to the standing rule and now points
at the skill for the procedure.

### Added

- **[docs/PHILOSOPHY.md](docs/PHILOSOPHY.md)**, 151 lines. Nine beliefs, each with
  the strongest counter-argument that could be built against it, the mechanism in
  the tree that makes the belief operational, a named failure mode with the tell
  that reveals it, and a decision rule or a worked micro-example. It closes with a
  belief-to-enforcement table, on the rule that a belief with no mechanism behind
  it is a mood and a mood cannot fail a gate. The counter-arguments are real: the
  gate section concedes that stage gates are the artifact of the era product
  management spent a decade escaping, and answers that rather than dodging it.
- **[docs/COMPARISON.md](docs/COMPARISON.md)**, 124 lines, dated 2026-09-03. A
  five-column table on spec-kit, BMAD-METHOD, a hosted commercial product, and
  ordinary template packs, with one column for what each does better than this
  repository. No scoring total, because a total lets a reader skip the only rows
  worth reading. It adds a picker keyed to your binding constraint rather than to
  feature lists, a per-system "pick that one when", a handoff table for running two
  of these systems together and what to strip in each direction, all seven of this
  repository's own losses collected in one list and each marked fixable or
  structural, three worked choosing scenarios on fictional products, the four gap
  claims rewritten as falsifiable statements with what would disprove each, and a
  one-afternoon evaluation protocol that beats a week of comparison reading.
- **[docs/FAQ.md](docs/FAQ.md)**, 121 lines. Sixteen questions in four sections,
  answered with the weaknesses written as weaknesses. Is this AI-generated, answered
  with how to check the claim rather than take it. Why trust a solo maintainer,
  answered as three checkable mechanisms instead of a reassurance. What happens when
  maintenance stops. Is this waterfall. Will the gates become theater. How it fits a
  tracker, an in-house PRD template, a two-person startup, and non-software work.
  Most answers carry a second paragraph that is a decision rule or a tell.
- **[GLOSSARY.md](GLOSSARY.md)**, 141 lines, 73 terms. Every word this tree uses in
  a narrower sense than the industry does, defined once, alphabetical, each with a
  because-clause where the clause teaches and a cross-link to the file that governs
  the term. Reach unit, mandate lane, evidence class, escape hatch, forced pair,
  smart skip against the skip line, weight, pencil path, tell, trap, zombie spec.
  Where this file and the governing file disagree, the governing file wins.

### Changed

- **The eleven knowledge canon cards, 443 lines to 1,453.** Each card kept its
  original heading set, attribution line, skip line, trap, Used-by list and Run-it
  block verbatim, and gained seven sections inside that skeleton: where the method
  came from and how its origin explains its blind spots, what it assumes as numbered
  claims each with a because-clause, a worked illustrative micro-case on a fictional
  product with invented numbers, the other ways it fails with the tell for each, how
  it lies or gets gamed, a what-good-looks-like against anti-pattern contrast, and
  where it sits in the loop with its upstream, downstream and gate links. Worksheet
  mechanics were kept out of the cards, with the one exception a review found and
  the Fixed section below records. Cards ran 31 to 43 lines before and 129 to 135
  after.
- **The six `os/` spine files, 674 lines to 1,319.** `OPERATING-LOOP.md` gained
  per-stage entry and exit tests, a named failure per stage with its tell, a worked
  micro-example per stage, and a backward-transition table for the moves the loop
  diagram cannot draw. `HOW-TO-RUN-A-PRODUCT.md` gained a cast table with signature
  authority, elapsed-time calibration, two gate attempts rendered as marked
  checklists with evidence beside each line, a latency trade-off with three logged
  options, and one requirement traced across nine documents. `STAGE-GATES.md` gained
  five to eight named failure precedents per gate, each with its on-page tell, plus
  the most common false pass for each gate. `CONDUCTOR.md` gained a worked
  four-part question, a five-answer evidence-ladder classification table, and
  rendered exchanges for the two-push park, the smart skip, the escape hatch and a
  failing gate. `WHICH-DOCUMENT.md` gained seven worked routing cases and four
  misreadings of the tree with their tells. `PRODUCT-WORKSPACE.md` gained an
  annotated month-nine directory listing and a ninety-minute new-owner reading path.
- **The twelve agent identity files, 595 lines to 1,315.** Each gained a yours
  against not-yours table that names the other role holding each refusal, six or
  seven judgment rules with because-clauses covering exactly what the paired skill
  procedure cannot settle, a voice section, a worked run from input to output on
  fictional products, an escalation section keyed to the ladder in
  [agents/TEAM.md](agents/TEAM.md), and failure modes of using that agent wrong with
  the tell for each. The fictional products recur across files, so the handoffs
  chain the way the team protocol says they should. Files ran 29 to 52 lines before
  and 93 to 113 after.
- **The learn layer, 416 lines to 776.** Each of the three paths now carries a
  standing invented brief with fixed numbers that every step inherits, and each step
  carries why it comes now, a run line into the paired worksheet, pass criteria at
  two, one and zero, a named trap with its tell, and a time expectation. The library
  gained per-book annotations naming what the card omits, the signal that you should
  go to the source, and the standard misapplication, plus a rule for when buying the
  book is worth it. The tutor skill gained two full worked critiques and a
  calibration rule set for the one-against-two boundary, which is where a scoring
  rubric actually breaks.
- **Wiring for the four new files.** `README.md` gains two module-map rows and links
  the reference files where each is the natural next question; `docs/ARCHITECTURE.md`
  carries them in the file tree and states why nothing links up to them;
  `AGENTS.md` and `CLAUDE.md` gain the two reference routes, with the instruction to
  give the counter-argument alongside the belief; `system/BOOT-PROMPT.md` adds them
  to its manifest marked reference-only, since none of them produces an artifact;
  `CONTRIBUTING.md` states that a failure mode needs its tell and a skip condition
  needs to be a test on the situation.

### Fixed

- `routing/README.md`: the install command is `omniroute serve` (there is no `start`); added the provider-connection commands, a tier probe that shows which concrete model answers each tier, and the request headers that stop OmniRoute's compression, semantic cache and memory injection from altering prompts that must be quoted verbatim. Found by running the config against a live OmniRoute: on a keyless install `auto/reasoning:pro` returns `404 Combo has no executable targets`, which the doctrine expects but the manual never said.
- `routing/omniroute.config.json`: the judgment tier now states what it requires and carries an explicit, off-by-default `keylessFallback` instead of leaving a fresh install to fail silently; `endpoint.requestHeaders` and `endpoint.verify` record the headers and the probe. No tier model changed.
- `system/BOOT-PROMPT.md`: the file manifest now carries `frameworks/` as six folders and 46 worksheets, `agents/` as twelve identities, all 98 templates (34 were missing, including every business case, decision memo, interview guide and survey design), 28 skills where nine were listed, and ten examples where four were. The manifest header no longer claims to be the whole repository, because it is not and does not need to be; it claims to be every file a pasted session can ask for, which is checkable. Step 2 of HOW TO WORK now routes a produced number to its worksheet before the template opens, since filling the template first inverts the work: the number gets chosen to fit the sentence already written.
- The `What good looks like` tables on the four knowledge cards that have a paired worksheet (RICE, Kano, north star, jobs to be done) restated the sheet's steps as virtues. Rewritten to the card's own side of the line, with the mechanism that unites each table's failures stated underneath it. The other seven tables have no paired worksheet and were left alone.
- `os/STAGE-GATES.md`: Gate 3's fourth failure precedent duplicated the DESIGN stage's characteristic failure in `os/OPERATING-LOOP.md`, tell included. Replaced with the gate-specific failure it was crowding out, the dependency date the other team has never seen, and a cross-link for the stale-register case.
- `os/WHICH-DOCUMENT.md`: deleted a paragraph that announced it was restating an earlier bullet, and folded its one load-bearing example, the three-line disclosure edit, into the bullet itself.
- `GLOSSARY.md`: added the J section, which did not exist, plus JTBD, Kano, RICE, cost of inaction, never-invent rule, question bank and skip-risk warning. All seven are load-bearing in `os/` and `docs/` and none was defined.
- `learn/`: the two capstones in `path-transitioning.md` and `path-senior.md` had a Done-when line and no pass bar, and three earlier steps carried theirs under a second name. One label across all three paths, and the capstone bars name the score to distrust rather than only the score to reach.
- `agents/research-agent.md`: the reconcile-before-handoff section repeated the procedure held by `skills/product-analyst/SKILL.md` pass 4, one sentence of it verbatim. Cut to the standing rule the identity owes the next reader, pointing at the skill for the mechanics.

### Known gaps

The point of a depth release is that the thin files become obvious once the deep
ones are next to them. These are the ones this version did not reach, in the order
the unevenness now shows.

- **`knowledge/domains/` is the thinnest layer in the tree**, twelve market cards
  averaging 35 lines against 132 for a canon card. Each names its gatekeepers and
  how its metrics lie, and none carries a worked example, a named failure mode with
  a tell, or the origin of the metric conventions it teaches. A reader coming from a
  deepened canon card will feel the drop immediately.
- **`knowledge/roles/` is next**, eight files averaging 46 lines. The ladder and the
  triad decision rights are the two most-cited files in the sub-layer and neither
  carries a worked dispute, which is the only thing that makes a decision-rights
  table usable under pressure.
- **`examples/` averages 67 lines** and is the layer that would benefit most from
  the same treatment, because a worked example is depth by definition. Six of the 46
  worksheets have a filled example; forty do not, unchanged from 0.5.0.
- **The 28 skills average 78 lines** and were deliberately left alone this pass to
  keep the procedure and identity layers from drifting into each other while both
  were being edited. They are the next candidate, and the anti-duplication line has
  to be redrawn before that starts.
- **`system/BOOT-PROMPT.md`'s manifest is now complete and nothing keeps it that
  way.** Every markdown file in the eight layers a pasted session can ask for is
  named in it as of this release, verified once by script and not since. The next
  file added to `frameworks/` or `templates/` will make the prompt wrong in the one
  way that matters, because the prompt also forbids asking for a path that is not on
  the list. A lint check comparing the manifest against the tree is a dozen lines and
  is not written.
- **No lint check enforces depth**, and none should on a line count. What is
  genuinely unchecked is the anti-duplication rule: nothing verifies that a
  deepened card avoided restating its worksheet, which was enforced by reading and
  therefore by attention rather than by a script.
- **The worked micro-cases are invented, and labeled so throughout.** They
  demonstrate a method's shape and failure mode; they are not evidence that the
  method works, and no release note here should imply otherwise.
- **`docs/COMPARISON.md` starts aging the day it ships.** It carries its comparison
  date and names the two rows most likely to flip, and it will need a re-read of the
  four primary sources on a cadence nothing in the repository enforces.

## 0.5.1, 2026-09-03

A research release. Before writing anything, this version studied the systems doing
adjacent work: the BMAD-METHOD, GitHub's spec-kit, BuildBetter's product-os, the
Anthropic product-management plugin, deanpeters' Product-Manager-Skills, and the
published PRD literature from Cagan through the current argument about what a spec
becomes when a model reads it. Two findings drove the release. The first was
uncomfortable and useful: nine of the twelve things none of those systems do, this
one already did. The second was the defect: there was no procedure here for writing
an ordinary PRD, because `ai-prd` scopes itself to features a model implements, so a
plain PRD fell through the router to "no skill".

A minor version because everything is added or rewired. No template field is
renamed, no file is moved, no gate changes what it demands. A PRD filled against
0.5.0 keeps working; its new sections are additions to the same document.

### Added

- **Four skills.** `write-prd` writes the general PRD and the requirements stack
  around it (one-pager, BRD, FRD, NFR, business rules, PR FAQ), picking the weight
  from `os/WHICH-DOCUMENT.md` before drafting and routing to `ai-prd` the moment the
  implementer turns out to be a model. `spec-review` reads a written spec the way a
  test reads code and reports where the prose is not testable, never rewriting.
  `persona-builder` turns discovery evidence into personas, job stories, journey maps
  and the opportunity tree, with the rule that every persona attribute traces to an
  evidence note or is flagged as a dated assumption. `write-vision-strategy` writes
  the two documents `strategy-critic` was already built to attack. The skill count
  goes from twenty-four to twenty-eight.
- **Kill criteria in the PRD.** Section 9 of `templates/definition/prd.md` names the
  conditions under which the team stops or rolls back, each with a threshold, a check
  point, and the person allowed to call it. No product operating system surveyed for
  this release has this section, ours included until now. Every one of them can start
  work; none could stop it.
- **A one-read summary.** Section 0 of the PRD, written last and placed first, under
  150 words, on the premise that most readers of most PRDs read exactly this much.
- **Counter-evidence per risk.** The four risks table gains a column for the single
  strongest fact arguing against your own answer. "None found, and here is where I
  looked" is a legal entry; an empty cell is not.
- **A dated assumptions index** in the PRD, pointing at row IDs in
  `assumptions-register.md`, on the rule that an assumption with no validate-by date
  is a belief and beliefs do not expire on their own.
- **A companion document table** (PRD section 13). Sixteen triggers, each naming the
  template this product type pulls in: failure scenarios, edge cases, instrumentation,
  support runbook, migration, sunset, launch comms, pricing, privacy, the regulated
  module, accessibility, SLOs, dependencies, the AI overlay, the business case, the
  program charter. The pattern of a short mandatory spine plus a menu pulled in by
  product type is borrowed from the BMAD-METHOD project's PRD template, applied to the
  templates this repository already ships.
- **A sign-off block** on the PRD with four named roles, and the rule stated in the
  file: the Gate 2 approver is a person, is not the author, and is not an agent.
- **A reader declaration** in the PRD header. A human reader resolves an ambiguous
  sentence with judgment and asks you at standup; a model resolves it with a guess you
  never see.

### Changed

- **Fifty-one templates had their `Skill:` header rewired.** v0.5.0 added fifteen
  skills and left the templates those skills drive still naming a generic drafting or
  research agent. Personas now name `persona-builder`, OKRs name `okr-critic`, the GTM
  plan names `gtm-launch-planner`, release readiness names `launch-readiness`, the
  architecture set names the architect agent rather than the drafting agent, and so on
  through the tree. The reverse link (each skill's "files this skill drives") and the
  forward link (each template's `Skill:` header) now agree.
- **The router gains four rows** in `CLAUDE.md`: the general PRD, the spec review, the
  persona and job set, and the vision and strategy pair. The document-weight row now
  hands off to `write-prd` after `os/WHICH-DOCUMENT.md` picks the weight, rather than
  ending at "no skill".
- **`AGENTS.md` adds one gate rule**: run `spec-review` over any spec before its gate.
  A filled field is not a written requirement. "The system should be fast" passes a
  completeness check and fails a testability one, and only the second check is worth
  running.
- **`templates/planning/product-strategy.md` gains the missing third of the kernel.**
  The file's own header cited Rumelt's diagnosis, guiding policy and coherent actions,
  then shipped sections for only two of the three, so `strategy-critic` was grading a
  policy the template had nowhere to hold. The new section is numbered 1b, not 2, so
  that every section number below it, and the nine files across `frameworks/strategy/`
  and `examples/` that cite those numbers, keep meaning what they meant before.
- The three directory faces carry the new work: `skills/README.md` catalogs
  twenty-eight skills, `templates/README.md` describes the PRD by its new spine.

## 0.5.0, 2026-09-03

The running release. Four versions in, the OS could tell you why a method exists and what artifact a stage owes its gate, and it still could not hand you the sheet when someone said "let's do a Kano". This version closes that gap and the two beside it: the procedures a PM runs weekly that had no skill, and the stages of the loop that had no agent. A minor version because everything is added: no field renamed, no file moved, no gate changed, so a document filled against 0.4.1 keeps working untouched.

### Added

- **The frameworks layer, 46 runnable worksheets in six groups** (`frameworks/`, faced by [frameworks/README.md](frameworks/README.md)). Strategy holds the kernel test, the Playing to Win cascade, a Seven Powers audit, Wardley mapping, SWOT into TOWS, five forces, PESTLE, Ansoff, the business model and lean canvases, the value proposition canvas, market sizing, build against buy against partner, and the positioning canvas. Discovery holds the Mom Test guide, the JTBD job map with the four forces, opportunity scoring, assumption mapping, the empathy map, the Kano survey with its full classification table, the product-market fit survey, and a design sprint runbook. Prioritization holds RICE with ICE beside it, WSJF, MoSCoW, a weighted decision matrix, Now-Next-Later, story mapping, impact mapping, and the one-way against two-way door test. Metrics holds the north star input tree, AARRR, HEART, growth loops, cohort retention, and unit economics. Pricing holds van Westendorp, Gabor-Granger, and good-better-best packaging. Execution holds RACI, the power-interest grid, five whys with the fishbone, four retrospective formats, an estimation sheet with reference classes, a risk matrix, and the premortem worksheet the existing skill drives. Every worksheet states its scales and its arithmetic, names its originator, carries an invented worked example, a trap drawn from practice, a line beginning "Skip it when", and the templates and gates it feeds.
- **Fifteen skills** covering the procedures a PM runs weekly that previously had none: `user-interview`, `competitive-intel`, `market-sizing`, `pricing-packaging`, `gtm-launch-planner`, `experiment-designer`, `metrics-tree`, `stakeholder-update`, `story-writer`, `okr-critic`, `strategy-critic`, `decision-memo`, `postmortem-facilitator`, `launch-readiness`, `pm-hiring`. The skill count goes from nine to twenty-four.
- **Seven agents and a team protocol.** `architect-agent` gives DESIGN an owner, `acceptance-agent` gives Gate 4 a runner, `release-manager-agent` gives Gate 5 one, and `analyst-agent`, `growth-agent`, `pmm-agent`, and `estimator-agent` fill the OPERATE and planning seats. [agents/TEAM.md](agents/TEAM.md) is the part that makes them a team rather than twelve files: who leads each stage, the handoff packet every agent emits (artifact path, evidence with sources, open fields with owners-to-be, conflicts, what was not checked), the escalation ladder, and the rule that no agent signs a gate.
- **Twenty-five templates** on the business and program side the loop had thin: business case, program charter, capacity plan, decision memo, exec update, status report, change request, tech debt register, retrospective, hiring scorecard, release notes, migration cutover plan, SLA and SLO definition, support runbook, customer comms, sales enablement one-pager, interview guide, interview notes, survey design, usability test plan, privacy impact assessment, accessibility checklist, metrics dictionary, dashboard spec, and design brief. Template count goes from 73 to 98.
- **Six worked examples** on the fictional Ledgerline expense copilot already used in `examples/`: RICE scoring, the Kano survey, the JTBD job map, the strategy kernel, the business case, and the north star tree, each showing the arithmetic and at least one honest open field.

### Changed

- `knowledge/README.md` and eleven method cards now point at the worksheet that runs the method; the card keeps the reasoning, the worksheet holds the form.
- The three directory faces added in 0.4.1 carry the new work: `skills/README.md` catalogs twenty-four skills, `agents/README.md` twelve role files plus the team protocol, and `templates/README.md` all 98 blanks with its per-directory counts corrected.
- `README.md`, `docs/ARCHITECTURE.md`, `AGENTS.md`, and `CLAUDE.md` carry the new layer, the expanded rosters, and seventeen new router rows.
- `learn/README.md` sends each step through the matching worksheet between reading the card and filling the template.

### Known gaps

- The worksheets are forms, not calculators. Nothing computes a RICE score or a payback period for you, and no lint check verifies that the arithmetic in a filled copy was done correctly.
- Attribution for TAM/SAM/SOM, RACI, and the risk matrix names a lineage rather than an originator, because no single founding source exists; those three files say so instead of inventing one.
- The pricing sheets describe research designs; sample size, screening, and fielding are named as requirements and left to the reader, since a survey run on the wrong sample fails no gate here.
- Twelve agents now exist and only the five originals have been exercised end to end in a real product pass. The new seven are specified against the loop, not proven against it.
- Six of the 46 worksheets have a filled example; the other forty are specified and unillustrated, which is the same gap the template layer carried at 0.1.0.
- Nothing checks that a worksheet's Feeds list stays true when a template it names is restructured; lint proves the link resolves, not that the claim behind it still holds.
- `frameworks/` follows the 0.4.1 README convention, so a directory face exists, but nothing in `lint.py` enforces that convention for the next directory either.

## 0.4.1, 2026-09-02

The directory-rendering fix. A code host renders `README.md` in a directory listing and nothing else, so a visitor who clicked into `templates/`, `skills/`, or `agents/` on the web met a bare file list with no framework around it, and the indexes that did exist were named `INDEX.md`, which nothing renders. A patch version: no field renamed, no file moved or deleted, and every link that resolved before still resolves.

### Added

- **Five directory faces.** `templates/README.md` catalogs all 73 templates, one table per stage directory, each row saying what the template is and when to reach for it, closing on the document-weight question. `skills/README.md` defines what a skill is here, lists the nine with a use-when and an entry point, and says how they load in an agent CLI versus a pasted chat session. `agents/README.md` separates identities from procedures and names who invokes each of the five role files. `system/README.md` and `os/README.md` do the same for the boot prompts and for the loop, the second with a read order for a first-timer.

### Changed

- **Four indexes became READMEs.** The content of `knowledge/INDEX.md`, `knowledge/roles/INDEX.md`, `knowledge/domains/INDEX.md`, and `learn/INDEX.md` moved into the `README.md` beside it, unchanged apart from links that pointed at a sibling index. Each `INDEX.md` stays behind as a two-line pointer, so a link written against the old name still lands somewhere useful.
- **Prose links across the tree** now point at the README: the module map in `README.md`, which also links `templates/`, `skills/`, `agents/`, `system/`, `routing/`, and `os/` for the first time; the router rows in `CLAUDE.md` and `AGENTS.md`; the four manifest lines in `system/BOOT-PROMPT.md`; the domain line in the Gate 1 checklist; two conductor question banks; and the learn layer's own cross-links. The `Knowledge:` header field in the 47 templates that name the knowledge index still points at `knowledge/INDEX.md` on purpose, because that field has been copied into filled documents outside this repository and the pointer costs one line to follow.
- **`docs/ARCHITECTURE.md`**: the file tree carries the nine new files, and cross-link convention 10 states the rule (every browsable directory carries a README, which is its rendered face) along with both exceptions above.

### Known gaps

- Nothing enforces the new convention. A directory added tomorrow with no README passes the gate; the rule lives in the architecture document and in review, not in `lint.py`.
- `templates/README.md` carries a Stage/Knowledge/Skill header because the header gate applies to every file under `templates/`. A catalog wearing a template's header is slightly odd; the alternative was carving an exception into the detector, and a detector with exceptions is the start of a detector nobody trusts.
- The catalog now describes the template set in a second place, alongside the tree in `docs/ARCHITECTURE.md`. Two descriptions of the same 73 files can drift, and only a human reading both will catch it.

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
