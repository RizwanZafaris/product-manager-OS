# Changelog

Every notable change to this repository is recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this repository uses [semantic versioning](https://semver.org/spec/v2.0.0.html).

What a version number means here, since this is a document system and not a library:

- **MAJOR** changes rename or remove a template field, move or delete a file that other files link to, or change what a gate demands. These are the changes that break a fork or a half-filled document, so they only happen on a major version, and this file names the migration for each one.
- **MINOR** adds a template, a knowledge card, a skill, or a section. Nothing you filled is renamed, moved, or broken by it. Corrected 2026-09-03: this used to say existing filled documents keep working untouched, which read as a promise about the gate and is only a promise about the document. A section added in a minor version can become a section today's checks expect, so an older filled document keeps meaning what it meant and can fall short of the current bar. The two entries where that actually happened, 0.6.0 and 0.5.1, carry a dated note saying so.
- **PATCH** fixes wording, links, typos, or a lint rule that was wrong.

The stability promise is stated in [README.md](README.md) and repeated here so it survives a fork: within a major version, template field names and file paths do not change under you. That is the whole promise, and the paragraph above says what it deliberately leaves out.

## 0.7.1, 2026-09-03

An external audit reproduced six release-blocking defects in the executable
layer against ce81264. Every one of them is closed here, each with a
regression test that fails against the behaviour it replaced rather than
merely passing against the new one. Nothing in the document layers changed
shape, so a filled artifact from 0.7.0 still matches the template it came
from and every path a document links to still resolves.

### Fixed

- **The runner and the initializer placed the same template in two
  different files.** They differed on thirteen of the sixty templates the
  manifest routes to, and the initializer refused a fourteenth outright.
  The expensive one was STATE.md: the runner filed it at
  `execution/state.md` while every skill, prompt and adapter addresses it
  at the workspace root, so a run could leave a second state file and a
  later resume could read the wrong one. Every `templates/ai/` file landed
  outside the DEFINE stage that produced it. `tools/workspace.py` is now
  the single answer and both callers import it;
  `tools/check_workspace_contract.py` proves they still agree, and skips
  cleanly on a tree with no `harness/`.
- **The runner never rewrote a placed copy's links.** A template's relative
  links are computed from `templates/`; written unchanged into a workspace
  folder they point at paths that have never existed. Measured across the
  sixty templates: 391 broken links in 49 of them. The runner now calls the
  same rewriter the initializer has always used, reads the staged bytes
  back off disk, and fails the run rather than committing a document whose
  links go nowhere.
- **The Conductor could not satisfy both of its contracts.** Its skill says
  ask one question and stop; the runner demanded a fully filled STATE.md or
  its structure check rejected the answer. No reply could pass both. Routes
  now declare a `kind` and the runner branches on it: `artifact` fills a
  template, `report` judges without rewriting, `interactive` is one turn of
  a conversation, `reference` is an answer read out of the tree. Only the
  first two file a document, and the structure check runs only where there
  is a template to measure against. The kind is a required, validated key,
  and it appears on every generated command card.
- **The three-file transaction was not atomic.** Injecting a failure on the
  second of three replaces committed the first and left it: an artifact
  with no log, the exact state the docstring said could not happen. Every
  destination is now copied aside before anything is replaced and restored
  if the commit cannot finish. The one thing still not claimable without a
  write-ahead journal, that the rollback itself cannot fail, is reported by
  path instead of passed over. `SECURITY.md` says the same thing.
- **Concurrent journal writes lost rows.** Two runners read the same
  STATE.md, each appended to that copy, and the second replace overwrote
  the first: one row on disk where two runs had happened, and no error
  anywhere. The read-modify-write is serialized under an advisory lock held
  from the read to the commit, because a lock around the replace alone
  would still let two processes read the same body.
- **CI did not test the shipped runtime.** A Python syntax error introduced
  into `harness/runner.py` did not fail the build: every step read markdown
  or parsed JSON, and none imported the one file that makes a network call.
  CI now compiles every tracked `.py`, runs the harness suite, checks the
  adapter and the desktop self-test, initializes a real workspace and lints
  it, proves the workspace contract, and runs a second job that deletes
  `harness/` to keep the deletability guarantee honest.
- **The review gate checked that a checkbox existed, never that it was
  ticked.** A document could carry nine empty boxes and pass. An unticked
  box is not a defect on its own, and the worked example ships with one
  unticked and a paragraph saying why. A document whose status line says
  Approved while a box is unticked now fails; everything else is a tally
  reported as a notice, because nothing here can stop a person ticking a
  box the evidence does not support.
- **The metric check rejected truthful evidence.** A sourced churn baseline
  was refused because that exact figure appears in the worked example, which
  taught the operator that the way to pass the gate is to round the number.
  The repository tree keeps the blunt ban. A product workspace now judges
  the same literal on whether it carries provenance on its line or the
  next, and the refusal says explicitly not to round it.
- **The rewriter and the gate read different link patterns.** An
  angle-bracket destination with a space in it was a link the gate judged
  and the rewriter never saw, so a workspace could pass `init_product
  --check` and fail `lint --workspace` on the same file. The rewriter
  imports `lint.py`'s pattern rather than restating it.
- **A test asserted the interpreter, not the gate.** The line number
  CPython reports for a trailing comma in JSON changed between 3.11 and
  3.14, so `test_lint.py` failed on a Python a user actually had
  installed. CI now runs on both.

### Added

- `tools/workspace.py`, the one answer to where a filled artifact lands and
  what its links say once it lands there.
- `tools/check_workspace_contract.py`, which proves the two writers agree.
- `init_product --add-all` installs every shipped template and then settles
  the links between them; `--relink` runs that settling pass alone and is
  idempotent. Without it, installing everything left 181 links across 41
  files still aimed at the blank templates rather than at the workspace's
  own copies, because a link can only prefer a copy that already exists and
  the order of installation decided which it got.
- Deferred work writes a durable job record with an id, deduplicated by
  route and input, listable with `runner.py --list-queue`, and exits 75
  (EX_TEMPFAIL) instead of 0. It is a record, not a queue: nothing picks a
  job up, and the record says so in as many words.

### Changed

- `harness/README.md` states the harness's maturity separately from the
  document system's, in a table of what it is not: not a job queue, not a
  team system of record, not governance evidence, not a portfolio, not
  reproducible. The document layers carry none of those limits, which is
  why the two are now stated apart rather than under one version number.

### Known gaps, unchanged by this release

Named because a release note that only lists wins is marketing. STATE.md
still models one product at one stage, so it cannot carry a portfolio.
There is still no immutable audit log, no approval identity, and no hash
over the evidence a gate was passed on, so this tree still produces no
governance evidence. There is still no run id tying a document to the
commit, prompt, template and skill that produced it, so a run is not
replayable. Twenty-two routes still require `--template` when they name
more than one, which is deliberate: picking the first would turn a request
for a BRD into a PRD silently. And the repository's tags stop at v0.4.0
while this file describes releases through 0.7.1.

## 0.7.0, 2026-09-03

The graph, harness, and systems work. It is numbered 0.7.0 rather than 0.6.0 because
0.6.0 below is the depth release, which was written first and says nothing new was added
to the loop. That was true of the depth pass and is not true of this one, so these
additions get their own number instead of being folded backward into an entry that
already shipped a different claim. Both arrive in one merge, in that order.

Nothing here renames, moves, or removes a file, and no gate changed what it demands.

- **Twelve worksheets, and the frameworks layer goes from 46 in six groups to 58 in
  eight.** Two of the groups are new. `frameworks/systems/` (iceberg-model, cynefin,
  causal-loop-diagram, leverage-points) exists because every group before it is a
  planning instrument that takes the problem as given, and a planning sheet aimed at a
  symptom returns a confident quarter of work on the wrong thing with the confidence
  coming from the sheet. `frameworks/assessment/` (product-operating-model-assessment,
  team-topologies-assessment, tech-debt-assessment, westrum-culture-typology) scores the
  organization a plan lands in rather than the plan. Two landed in `metrics/`
  (dora-four-keys, space-framework) and two in `execution/` (fmea,
  theory-of-constraints). Each of the twelve is reachable from a skill or a template, so
  none is an orphan in the graph, and each is named in the stage map that owns it in
  both link forms.
- **The graph layer.** YAML declarations across the six declaring layers, with a
  `SKILL.graph.yml` sidecar wherever frontmatter is closed to them, plus
  `tools/frontmatter_init.py` to seed them and `tools/graph.py` to render
  `docs/GRAPH.md`. Beside the generated file: `os/maps/`, one hub note per stage so a
  graph view has centers instead of a hairball, and a committed core-only `.obsidian/`
  vault config that colors the graph by layer. `lint.py` grows from nine tree checks to
  eleven (10 graph declarations, 11 wikilinks) and `test_lint.py` from 25 tests to 47.
- **The harness.** `harness/` makes the router table executable: `MANIFEST.json` with one
  entry per router row in router order, `INVARIANTS.md`, `tiers.md`, `runner.py`, and
  three adapters. `tools/check_manifest.py` proves the manifest and the table agree row
  for row and CI runs it. The harness is deletable and is not a runtime dependency, and
  the deletability proof in its README now passes all four gates with no exception; the
  rule that earned that is one line long, which is that a file outside `harness/` names
  a harness path in plain text and never as a link.
- **Three router rows,** each where a trigger phrase already existed rather than one per
  new sheet: "is this a symptom or a structure", "what kind of problem is this", and
  "are we set up to ship this". Manifest entries `diagnose-symptom-or-structure`,
  `classify-problem-domain`, and `assess-delivery-readiness` match them in router order,
  taking the table and the manifest from 38 rows to 41.
- **An eleventh example,** `examples/ledgerline-harness-routing-run.md`, the only file
  under `examples/` produced by a model call rather than written by hand.
- **The faces were swept for the counts this work invalidated,** in `README.md`,
  `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/FAQ.md`, `frameworks/README.md`,
  `knowledge/README.md`, `os/README.md`, `system/BOOT-PROMPT.md`, the harness READMEs,
  and the routing-run example. `docs/ARCHITECTURE.md` also carried three counts that had
  been stale since before this branch: 73 templates where there are 98, nine skills
  where there are 28, and five agent role files where there are twelve.

### Fixed in remediation, 2026-09-03

An independent external review was run against this release before it shipped. It found
three critical defects in `harness/runner.py`, all three of which would have produced a
document that looked finished and was not, plus a set of smaller ones in the gates, the
tools, and the claims these documents make. Recording what was found matters more than
recording that it was fixed: a changelog that lists only additions is a marketing
document, and these three are the exact class of failure this repository says it exists
to prevent.

The three critical ones:

- **Truncated model output was accepted and written as a finished artifact.** A stream
  that carried text and then stopped, a `finish_reason` of `length`, a malformed frame,
  and an error object arriving after text were all treated as success. A reply is now
  usable only with text, a terminal event, and a `finish_reason` of exactly `stop`, and a
  second check that does not trust the gateway compares the produced document against its
  template: headings present and in order, table column counts held, no table returning
  as a bare header, no document ending mid-row. A committed artifact in this repository
  was carrying that defect and is caught by the new check.
- **Tier certification was a probe-time illusion.** The probe resolved a concrete model
  id, then the real call sent the tier alias again, so the gateway could answer from any
  model while the artifact carried the certified id. Every request now targets the
  concrete id, and the response header is held to it; a mismatch or a missing header
  queues the work instead of writing a document.
- **Writes were unconfined, destructive, and not atomic.** A product slug could contain
  path separators and walk out of `products/`, a rerun overwrote finished work, and the
  artifact, its log, and the journal row were written independently. The slug is now
  validated and the resolved directory has to sit directly under `products/`, an existing
  artifact or log is refused unless `--update` is passed, and the three files are staged
  and committed together.

Also fixed in the same pass: the credential redaction guarantee was unsupported and is
now enforced at one redactor with no length floor, with sanitized URLs and no raw gateway
bodies persisted; the 6000-character recovery path condensed the template as well as the
evidence, breaking the exact-input contract; the manifest checker and the desktop adapter
would read through a symlink out of the tree; the router table's Invoke and
Backing-templates columns were never checked against the manifest; the four universal
invariants bound every route in prose and were missing from the routes an adapter
actually reads, with `content-is-data` absent from 35 of the 41; the graph
tool could produce one node id for two different files; and seven worksheets and
templates carried invented arithmetic that was not labelled as invented, including one
sensitivity row whose numbers could not be reproduced. `harness/test_runner.py` is new,
with a failure-proving test per fix; `test_lint.py` goes from 47 tests to 78;
`tools/check_manifest.py` from 6 checks to 8; `harness/MANIFEST.json` and the generated
plugin move to 0.7.0.

The public claims were swept in the same pass, which is the part worth reading if you are
deciding whether to trust this repository. `SECURITY.md` described a tree of two Python
files with no service and no credentials, which stopped being true when the harness
landed; it is now a threat model with the manual path and the runtime path separated.
The AI-layer deletability claim was too strong in `README.md`, `docs/FAQ.md`, and
`docs/PHILOSOPHY.md`: the harness is deletable and a gate proves it, and deleting a
content layer leaves working documents and a lint gate failing in the hundreds, which is
now what those files say. The stability promise is corrected below. `README.md` claimed
every commit carries a Claude trailer; two merge commits do not, so it now says every
non-merge commit. And the deletability proof in `harness/README.md` no longer passes:
`AGENTS.md` names two harness paths as links, which breaks the link gate on a tree with
`harness/` deleted, and that is recorded there as an open item rather than quietly
dropped.

### Known gaps at this point

- None of the twelve new worksheets has a filled example. The layer's own bar asks for an
  invented worked example inside each sheet, which they carry, but the `examples/`
  directory illustrates six worksheets out of 58.
- The stage maps are curated by hand and no script keeps them in step with the tree, so
  the next worksheet added is invisible in the graph view until somebody remembers. The
  maintenance rule is written in `os/maps/README.md` and it is a rule, not a check.
- The three new router rows name no skill, so the sheets carry the whole procedure. That
  is correct for a worksheet and it does mean a run has no adversarial pass over it, the
  way the skills do.
- The deletability proof for `harness/` is red. Two markdown links in `AGENTS.md` name
  harness paths, so deleting the directory fails the link gate and the test that asserts
  the tree ships clean. The documents are unaffected and the fix is to backtick two
  paths. Nothing enforces the plain-text rule that would have prevented it, and attention
  has now failed it twice.
- CI runs the lint gates, the graph and manifest checks, and both `test_lint.py` copies.
  It does not run `harness/test_runner.py`, `generate.py --check`, or the desktop
  selftest, so a harness change is only as verified as the person who remembered to run
  them by hand.
- Nothing checks that a claim in `README.md`, `SECURITY.md`, or `docs/` still matches the
  code. This release found several that did not, all of them written truthfully and then
  outlived by the tree. The mechanism against that is a review, which is a person, which
  is the same class of control as a gate.

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

> **Correction added 2026-09-03, entry left as it shipped.** "Keeps working" is true of
> the document and not of the gate, the same way it is in the 0.5.1 entry below. A depth
> pass that adds a required block to a template raises what a current check expects of a
> document filled before it. The promise this repository actually keeps inside a major
> version is that field names and paths do not move under you. It does not promise that
> an older filled document still clears today's exit gate, and `README.md` now says so in
> the versioning section rather than leaving a reader to find out at a gate.

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
  averaging 35 lines against 132 for a canon card. (Count corrected 2026-09-03: the
  directory holds ten cards plus its README and index stub, which is what
  `README.md` and `docs/ARCHITECTURE.md` say. The gap itself stands.) Each names its gatekeepers and
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

> **Correction added 2026-09-03, entry left as it shipped.** The last sentence was too
> generous and is worth reading against what the tree does now. Nothing renamed, moved,
> or broke, so an older PRD still opens and still means what it meant. What did change is
> the bar: `agents/validation-agent.md` checks a draft against the current headings in
> order, and the PRD's own exit gate treats the sections this release added as required.
> So a 0.5.0 PRD does not keep working *untouched* in the sense of clearing today's
> checks; it keeps working as a document and reports the new sections as missing. If you
> hold one and it has to pass a gate again, diff it against the current template and add
> the sections rather than refilling the file.

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
