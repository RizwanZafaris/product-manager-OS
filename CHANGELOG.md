# Changelog

Every notable change to this repository is recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this repository uses [semantic versioning](https://semver.org/spec/v2.0.0.html).

What a version number means here, since this is a document system and not a library:

- **MAJOR** changes rename or remove a template field, move or delete a file that other files link to, or change what a gate demands. These are the changes that break a fork or a half-filled document, so they only happen on a major version, and this file names the migration for each one. Corrected 2026-09-23: "change what a gate demands" is scoped to the document schema, the templates together with the checks that read a filled document. Adding a section those checks require is that change, and it fails a document filled against the older shape. It does not cover the runtime bank contract in `pmos/question_banks.json`, which every product pins, so a question added there reaches no existing product until `pmos repin` is run. [README.md](README.md) states the three versioned surfaces and what each one promises.
- **MINOR** adds a template, a knowledge card, a skill, or a section. Nothing you filled is renamed, moved, or broken by it. Corrected 2026-09-03: this used to say existing filled documents keep working untouched, which read as a promise about the gate and is only a promise about the document. A section added in a minor version can become a section today's checks expect, so an older filled document keeps meaning what it meant and can fall short of the current bar. The two entries where that actually happened, 0.6.0 and 0.5.1, carry a dated note saying so. Corrected 2026-09-23: the same sentence is also narrower than it read on the runtime side. A minor release may add questions to a shipped bank, and no product already in flight adopts them: it keeps the banks it pinned, its approvals keep holding, and `pmos repin` refuses outright to add questions to a bank that product has already approved. A question reworded in an approved bank is adopted by repin and reports that gate stale until it is proved again. On the document schema it is narrower the other way: a section a minor release adds must be one no check requires. A release that makes a section required changes what the gate demands for every document already filled, which is a major change; 0.6.0 and 0.5.1 did it in minor releases, and their dated notes stand as the record of that.
- **PATCH** fixes wording, links, typos, or a lint rule that was wrong.

The stability promise is stated in [README.md](README.md) and repeated here so it survives a fork: within a major version, template field names and file paths do not change under you. That is the whole promise, and the paragraph above says what it deliberately leaves out.

## Unreleased

### Added

- A 27th release gate, `example-availability`: `python3 tools/example_availability.py --check`. The new generator `tools/example_availability.py` writes an "Example availability (generated)" paragraph into each of the 47 domain cards under `knowledge/domains/`, below the card's "Filled in this repo" paragraph. It is built only from declarations already in the tree: each file under `examples/` declares which template it fills in its first five lines, the same window `tools/template_rubric.py --backpointers` reads; an example declares it was written for a domain by being named `domain-<card>-<template>.md`; and a card declares which templates it bends in its "Templates this bends" line. The paragraph states global existence and domain applicability separately: which bent templates have a filled example anywhere, which of those examples were written for this domain, which bent templates have none anywhere, and which have examples written for other products. `--check` also fails on a repository-wide absence claim written by hand in a card outside the generated block; a claim scoped to one domain is allowed. Why: seven domain cards denied examples the tree already carried, and an eighth, `knowledge/domains/card-issuing.md`, did too, while every gate passed, because nothing read prose. Those eight sentences now name the nearest filled example and the gap that is real for that domain. A ninth, in `knowledge/domains/fintech.md`, said no filled example fills a template from inside `modules/regulated`; it now names the module's own byte-exact worked example, `modules/regulated/examples/dispute-summary/PRD.md`, which `modules/regulated/README.md` already called one, and keeps the separate and still true statement that no PRD example under `examples/` carries a run reg-gap-check output. `README.md` and `docs/FAQ.md` now say 27 gates and `docs/ARCHITECTURE.md` says twenty-seven. Review of the first version of this gate found four ways out of it, all closed. A card carrying neither the generated block nor the "Filled in this repo" line the block is placed below was left untouched and counted fresh, so deleting one line switched the gate off for that card; `--check` now names such a card and fails, and so does the write mode, which cannot place the block either. Only the first pair of markers is regenerated, so a second, hand-added pair was a place to park a false sentence that nothing rewrote and that the prose scan stripped before reading it; a card must now carry exactly one pair, and the prose scan drops only the first pair. The prose scan first suppressed a repository-wide absence claim whenever the words "for this domain" appeared within sixty characters after it, and then required those words to end the sentence; a second review broke that rule four times, because a sentence can end with a phrase without that phrase governing anything in it. One such case was "No filled failure-scenarios example exists in this repository, and none is planned for this domain.", which is false because six files under `examples/` declare they fill `templates/delivery/failure-scenarios.md`; the comma, semicolon, dash and bare "and" forms all worked. The code now allows only a connective from a closed list (yet, still, so far, to date, as yet) to stand between the claim and the scoping phrase, and the phrase has to end the sentence; anything else opens a new clause, and a repository-wide claim followed by another clause is still a claim about the whole repository. Two smaller ways out closed at the same time: a backtick or a link around the template stem used to walk a claim past the pattern, and the pattern missed both a claim with no stem at all and the wording "anywhere in this repository", which is the generator's own; all four shapes are matched now. A card whose block closer was written before its opener used to raise a ValueError out of the renderer, and is now named like the other block faults. The prose scan also reads the two files beside the cards, `knowledge/domains/INDEX.md` and `knowledge/domains/README.md`, which carry no generated paragraph of their own, so a claim moved one file out of a card is not a claim outside the gate; neither file carries one today. The pattern is a finite list of the phrasings that went wrong, not a reading of English, so a claim written in words nobody has used here yet will still pass. And `knowledge/domains/ai-products.md` declares its whole template pack by linking the directory, `[templates/ai/](templates/ai/eval-spec.md)`, of which only the file in the link's URL was counted, so the paragraph said the card bends 2 templates where it declares 12; a link whose text is a template directory now declares every template in that directory, the paragraph reads 11 of 12 with a filled example and names `assumptions-register` as the one without, and the card's hand-written sentence listing five of those examples by name is now a pointer to the generated paragraph instead of a second, unchecked copy of it.
- `tools/exec_surface.py`, a generator for the executable-surface inventory in [SECURITY.md](SECURITY.md). `python3 tools/exec_surface.py` rewrites the block between the two `executable-surface` markers from the tree, and `--check` fails when the committed block no longer matches. The block gives the number of scripts under `tools/` and names every one whose source spells an environment read or a network primitive, both read from each script's syntax with `ast` rather than searched for as text, so this generator's own detector constants do not classify it. `tools/docs_contract.py` runs the same comparison as the new `executable-surface` check, so the release gate that already runs that file fails on a stale block; a block whose markers have been deleted is reported rather than passed, because deleting it is the cheapest way to drop the claim it makes.
- Two checks in `tools/docs_contract.py` for the class of editorial defect that every structural check walked past, each one well-formed enough to parse. `duplicate-heading` reads every markdown file in the tree and reports a heading that repeats an earlier heading of the same level under the same parent; siblings, not the whole file, because a changelog writes `### Fixed` under every release on purpose and a persona sheet repeats `#### Snapshot` under every persona. Headings inside fenced code blocks are not read. `declared-path` reads every explicit relative path under `templates/`, one beginning `./` or `../` and ending in a committed suffix, wherever it appears in the file including inside an HTML comment, and resolves it from the directory of the template that wrote it; a reference that names no file, or that climbs out of the repository, is reported. A reference without a leading `./` or `../` is a stated limit and is not read, and so is every file outside `templates/`: the inherited comments in `examples/` carry relative paths that resolved from their template's directory and not from `examples/`, and those are left to the change that owns that layer. Measured with that pattern on the whole tree, 36 relative references resolve to nothing: 27 under `examples/`, 6 in `README.md` and 2 in `CHANGELOG.md` where a path is quoted on purpose, including the wrong and the corrected eval-spec path in this entry, and 1 in `docs/readiness/EXT-USER-session-script.md`. Every one of the nine outside `examples/` is prose quoting a path rather than declaring one.
- Two further checks in `tools/docs_contract.py`, each one closing a way the checks above could be walked around. `script-count` reads `SECURITY.md` outside the generated markers and compares any whole-directory claim about how many scripts `tools/` holds, in digits or in words, with the directory itself: generating the inventory closed the sentence and left the page open, and the stale sentence re-typed one line above the markers passed everything. A count of a named subset, such as this file's own "Six local scripts stay on this path", is not read, and a correct hand-typed number passes until the directory changes under it. `commitment-probe` reads every markdown file under `templates/`, `examples/` and `frameworks/`, and reports a checklist line or table row that bans asking about the future, or a question containing "would", in a guide that itself asks for a commitment in those words, unless the line names the exemption. Six lines in four files carried that contradiction.
- A wider network reading in `tools/exec_surface.py`, and the recognition list printed inside the block it writes. The first version read `urllib`, `http.client` and a socket; a script spelling `import http.server` and `asyncio.open_connection` got no row, and the generated sentence then said its source named no network primitive. The reading now covers the standard library's server, mail and remote-file modules, the common third-party HTTP and remote-access packages, the `asyncio` stream and server constructors, and a program such as `curl` handed to a subprocess as a string. The generated block ends with the whole list, in full, because "names no network primitive" is a statement about a fixed list and never about what a script can do; a name outside it, or one assembled at run time, is not seen, and the block says so.
- `SeverityCrosswalkTests` in `tests/test_contract_gates.py` adds 12 tests that read the shipped documents rather than copies of them, with `tests/fixtures/severity-crosswalk.json` as the fixture. The document sets are globs, the delivery template plus every matching file under `examples/`, for four kinds (testing strategy, UAT plan, support runbook, release-readiness), each with a floor count, so renaming a document out of the scan fails instead of shrinking it silently. The fixture holds three synthetic defects, each resolved to a severity id twice, once through the engineering definition and once through the UAT business wording, and the release outcome is then read three times: off the ladder's release rule, off the UAT crosswalk's, and off the release-readiness decision table, which is a different table in a different document with its own vocabulary (No / Only if / Yes). All three must agree with the fixture, for the templates and for every shipped example pair. Every ladder in the tree must state the same four definitions and release rules, so an example cannot drift from the template. Every column a covered document calls Severity must hold a canonical id or a classed `not a defect:` marker; the scan finds the column by its own name, so renaming a neighbouring column hides nothing, and every release-readiness record must still carry a known-issues table with a Severity column. A UAT plan may carry only one table under section 5, and no other table in the file may be keyed by the canonical ids or call a column Severity. No file under `templates/`, `examples/`, `frameworks/`, `knowledge/` or `skills/` may use a Sev 1 style scale; this file is excluded, because it names the scale it records the removal of. A known-issues row may not be S1; an S2 row must record an approver or be written as a condition; a `not a defect:` row must name one of the four gap classes and its Issue cell must carry the evidence words the fixture lists for that class, which is what stops a product defect being relabelled out of the ladder. The claims in the documents are tested too: the ladder's dictionary sentence must name the three other covered documents, and release-readiness must still state its two exit-gate lines and its failure-mode row.
- A test, `test_journey_chain.JourneyChainTests.test_the_prd_example_fills_every_section_of_the_template_spine`, reads the numbered spine out of `templates/definition/prd.md` and fails unless `examples/expense-copilot-prd.md` carries every one of those sections plus the sign-off block and the exit gate. Reverting the example alone fails it by name. Named limit, written in the test: it counts headings, not answers, so it cannot tell a filled section from a heading over one honest sentence. What is written under each heading is what review is for.

- `templates/definition/one-pager.md` gains section 8, "Cost, stop and reversal": an **Appetite:** line for the engineer-weeks or calendar weeks the business sponsor agrees to spend before the review date plus any new money, with the costing detail linked to `templates/planning/business-case.md` rather than restated; a stop table with threshold, checked-when and who-calls-it columns and two placeholder rows; and a **Reversal:** line for how this is turned off, how long that takes, who does it and what cannot be undone, with the rehearsed rollback linked to `templates/delivery/release-readiness.md`. Its section 4 metric table gains a "Review date" column, and the exit gate gains one checklist line per new field. The template's own failure table already demanded that costs, risks and a kill criterion appear on the same page and that success carry one date, and the fillable structure had nowhere to put any of them. Sections 1 to 7 keep their numbers, because `skills/conductor/questions/define.md` and several examples cite this template by section number. `examples/sahulat-one-pager.md` fills every new field: 28 engineer-weeks of appetite, stop rows S1 to S3 each with a threshold and a named caller, a review date on all four metric rows, and a reversal line naming the bill the aggregator has already posted as the part that cannot be undone. A new test class `OnePagerCostAndStopTests` in `tests/test_contract_gates.py`, registered in `docs/readiness/test-classes.json`, holds both files to it. The limit, stated plainly: nothing reads a user's filled one-pager. The test reads the shipped template and that one worked example, so an appetite with no number, a stop row with no caller or a blank review date still reaches Gate 2, where the humans who sign it are the check.
- A 26th release gate, `template-backpointers`: `python3 tools/template_rubric.py --backpointers` fails unless the templates with no verified filled-example link are exactly the exception list in that file, `BACKPOINTER_EXCEPTIONS`, each entry with a one-line reason. A link is verified the way the rubric's worked-example mark already verified one: it resolves to a file under `examples/` whose first five lines name the template. An entry fails too when its template has such a link, when it names no template in the tree, or when any file under `examples/` names its template back. The list has one entry, `templates/definition/assumptions-register.md`, which no example names back in its first five lines: nine examples mention it and `examples/example-brd.md` carries a labelled excerpt of it inside a BRD, but none is a filled copy of it. The mode also prints every template that more than one example names back, 23 today, with every candidate and a mark on each one linked, because it can verify a link and cannot judge which example is the right one. `README.md` and `docs/FAQ.md` now say 26 gates and `docs/ARCHITECTURE.md` says twenty-six, and its entry for `tools/template_rubric.py` names the mode.
- A `Filled example:` line in the 67 templates that had no verified one, 85 links in all, each after the blank line that follows the generated "What checks this" paragraph, where the existing pointers sit. 107 of the 108 templates now link a filled example that names them back. One rule chose the links: a journey file first (`expense-copilot-`, `sahulat-`, `harbourgate-`, `ledgerline-`, in that order), then `example-*`, then `domain-*`, alphabetical within a tier, at most two. `templates/planning/business-case.md` departs from it and links only `examples/domain-agritech-business-case.md`, because `examples/ledgerline-business-case.md` does not follow the template's sections. The pointers in `templates/definition/prd.md` and `templates/discovery/discovery-document.md` name the sections their only example leaves out. The 40 templates that already carried a pointer are unchanged. Scores from `python3 tools/template_rubric.py` move with the new links: 14 templates score higher, the median goes from 85.0 to 87.5, and one of the 14, `templates/architecture/adr.md`, rises only because the rubric counts the word "never" in a newly linked example's title as a failure warning.
- Requirement lineage and change impact are now readable inside `templates/definition/prd.md` itself, where the 360 audit's F09 found them spread across linked documents. Section 2 gains `Evidence` and `Metric ID`, so an objective names the evidence note it stands on and the `../operate/metrics-dictionary.md` row that fixes its formula. Section 3 gains `Verified by (test ID, filled at BUILD)`, the column that carries an acceptance criterion to the test that ran it. Section 4 gains `Objective it serves` and `Release slice`, and a `Release slices and dependencies` table beneath it says what each slice delivers, what it waits on ("none" is an answer, blank is not) and which dependency-register row holds the commitment. Section 8 gains `Covers (slice or objective)` and names a test ID beside the artifact, which is what makes a launch criterion the end of a trace rather than a separate checklist. Section 13's companion table gains `Applies (Yes / No)` and `Why`, and its guidance now says to answer every row rather than tick the true ones: a No with a reason is a claim someone can challenge at the gate, a blank is not. The sign-off block gains a `Baseline:` and `Changes since baseline:` line above it, a `Revision signed` column, and a `Change history` table whose row names the IDs that moved, the CR that carried them, the approvals re-taken and the approvals that still stand with the reason they do. Eight exit-gate lines check the new contract. Nothing existing was renamed or removed; a PRD filled against the old blank still means what it meant, and reads short in the new columns.
- `tests/test_contract_gates.py` gains `PrdLineageTraceTests`, registered in `docs/readiness/test-classes.json`. It renders one ILLUSTRATIVE filled PRD through the shipped template's own header rows and walks the audit's trace hop by hop: O1 to its evidence note and metric ID, to F1, to US1, to AC-1, to TC-101, to slice S1, to launch criterion L1. Four mutants prove the walk has teeth, each emptying one cell and asserting the trace stops there rather than passing; two more hold the change history to its own claim, that every signer is either re-taken by the change or explained, and that a signature older than the change names the older revision. Reverting the template alone fails this class. Named limit: this proves the columns exist and that a filled PRD using them resolves end to end. It does not resolve the cited IDs into `../discovery/evidence-note.md`, `../operate/metrics-dictionary.md` or `frd.md`, and no check rejects a real PRD that leaves the new cells blank; on the default path the exit gate and the humans who sign Gate 2 are what enforce them, exactly as with every other field in this template.
- Stable identifiers and verification closure in [templates/definition/nfr.md](templates/definition/nfr.md), finding F11 of the 2026-09-23 review: functional requirements and acceptance criteria carried IDs and this template identified its rows in prose, so a document with two latency rows could not say which one a waiver excused or which one a result closed. Its requirement tables gained three columns, `ID`, `Surface and workload` and `Status`. The `ID` column holds a stable identifier and a revision, written `NFR-01 r1`, and the template ships with `NFR-01` to `NFR-24` already assigned rather than bracketed, because a bracketed identifier teaches the reader that the identifier is optional. `Status` is one of Proposed, Agreed, Met, Not met, `Waived WV-nn`, or the owner and date deferral this template has always allowed for a number still to be agreed, which is preserved. The waivers table gained `Waiver ID`, `NFR ID (exactly one)` and `Gate waived at`; its four existing columns are unchanged. No existing column was renamed or removed. Four lines joined the exit gate: every row carries an ID and a revision and no ID appears twice; every row names the surface and workload its target binds; every verification result names one NFR ID and the revision it tested, and that revision is the row's current one; and every row is closed before the gate, Met against a current result, Waived under a waiver ID recorded here, or carrying the named owner and date. Per the note at the head of this file, an NFR document filled before this change keeps meaning what it meant and now falls short of four lines of the current bar.
- A seventh workspace check in [lint.py](lint.py), `NFR closure`, so the columns above are a rule rather than a suggestion. It runs under `python3 lint.py --workspace <dir>` over a filled copy of that template, found by the `template:` field the artifact block carries or by a path ending `definition/nfr.md`. It reports a filled requirement row with no ID, an ID not of the form `NFR-01 r1`, an ID used twice, a requirement table with no ID column at all, a waivers table with no `Waiver ID` and `NFR ID` columns, a waiver naming zero or more than one NFR ID, a waiver naming an NFR ID no row defines, a waiver row with no waiver ID, a row that says it is waived with no waiver recorded against it, a row waived under a different waiver than the one recorded, a row whose `Status` says Met or Not met and whose `Verified by` cell does not say which revision was tested, and a result that names another row or a revision older or newer than the row's own. A row whose `Status` claims no result is not required to name a revision: `Verified by` names the artifact that will prove the row and is a plan until a result exists, and requiring the revision there would make every planned verification read as a result. What the check cannot do, stated because the columns invite more confidence than the code earns: it reads what is typed. It cannot tell a substantive edit from a typo fix, so a revision left at `r1` through a rewritten target is a person not bumping it; `Status` is a typed word, so a row that says Met beside a current result is a claim and not a measurement; and it does not run in tree mode, so the nine filled NFR examples under `examples/` are not held to it. Those nine still identify their requirements in prose, and the template says so above its own tables rather than leaving a reader to discover it. `tests/test_lint.py` carries the checks as `NfrClosureTests`, with the two fixtures the finding's closure proof names: one conforming document that reports nothing, and the same document with one target moved to `r2` and its `r1` result left beside it.


### Changed

- **README.md's "Versioning and stability" section held two rules that could not both be true.** One said that changing what a gate demands is a breaking change and happens only on a major version; the next said a template can grow required sections in a minor release, after which a document filled against the older shape fails the current gate. The section now names the three surfaces that carry versions separately and states the promise for each: the package version, the `version` field of `pyproject.toml` and the tag cut from it; the document schema, the templates and the checks that read a filled document, chiefly `REQUIRED_SECTIONS` in `lint.py` and the nine required sections `pmos handoff` reads, which has no version of its own and checks a filled document against today's checker; and the runtime bank contract, `pmos/question_banks.json`, where each bank carries its own version and a definition hash computed from the questions it asks, a product pins the banks it started with, and a gate approval records the hash of the questions its bank asked. An added mandatory section is breaking on the document schema and is not breaking for a product already pinned, which is the whole of the contradiction. Four outcomes are stated, each read from the runtime rather than asserted: a question added to a bank the product has not approved is adopted by `pmos repin`, which keeps every answer and stales no gate; a question added to a bank it has already approved is refused, with the bank and the question ids named and nothing written, dry run included; a question reworded in an approved bank is adopted, its answer kept, and that gate reports stale until it is proved again, the earlier approval kept as a superseded record; and a gate approved before contract pinning carries no question hash and does not go stale. `tests/test_versioning_contract.py` drives an already approved fixture through an optional and a required addition on both surfaces, and fails if README.md or this file stops stating those outcomes. The MAJOR and MINOR bullets at the head of this file carry a dated correction saying the same.
- **`pmos repin --json` listed a gate to prove again for a bank the product had never approved.** `gates_to_prove_again` was every bank whose questions changed, plus every bank the shipped contract drops. A bank with no approval has nothing that can go stale: an approval records the fingerprint of the questions its bank asked, and `pmos status` reports no stale gate for a bank that was never gated, so the field named a re-proof the runtime never asks for. It is now filtered to the banks the product's stored state holds a gate record for. Nothing else about repin changes, and the field is reported the same way under `--dry-run` as without it. `tests/test_versioning_contract.py` fails on the unfiltered value.
- One severity dictionary across four DELIVER documents. The QA severity ladder in `templates/delivery/testing-strategy.md` and the UAT scale in `templates/delivery/uat-plan.md` gave the same defect different ids, so whether a release was held depended on which document the reader had open. `templates/delivery/testing-strategy.md` section 6 is now headed "Defect severity ladder (canonical)" and is the single defect-severity dictionary for exactly four documents: itself, the UAT plan, the release-readiness checklist and the support runbook. It used to claim every DELIVER document, which was false: the support runbook, in the same folder, defined its own Sev 1 / Sev 2 / Sev 3, and other DELIVER documents legitimately score other things on their own scales, such as alert routing in the SLA/SLO definition and the observability plan, usability findings in a design review, and risk in an FMEA. The claim now names its four documents and says so. `templates/delivery/uat-plan.md` section 5 is a four-column crosswalk onto the canonical ids rather than a second scale. `templates/delivery/support-runbook.md` section 4 no longer tells the reader to paste an org severity scale in; it is a crosswalk onto the same four ids with an S4 row added, and the same change lands in `examples/harbourgate-support-runbook.md` and in the escalation wording that quoted it in `examples/harbourgate-coverage-sheet.md` and `examples/harbourgate-release-notes.md`. `templates/delivery/release-readiness.md` gains a table, "What each Severity cell means for the release", which is where the release decision is now read from instead of being inferred from the ladder. The marker for a row that is a readiness gap rather than a product defect was the bare words `not a defect`; it is now `not a defect:` followed by one of four named gap classes, untested path, missing runbook, unstaffed support and external approval pending, because the bare marker was an escape hatch under which a real product defect could be relabelled with nothing failing. The same edits land in `examples/harbourgate-testing-strategy.md` and `examples/harbourgate-uat-plan.md`, and the known-issues severities in the three shipped release-readiness examples (`examples/harbourgate-release-readiness.md`, `examples/domain-gaming-release-readiness.md` and `examples/domain-public-sector-govtech-release-readiness.md`) move from low, medium and high to canonical ids or a classed `not a defect:` marker; with the template that is four release-readiness documents, not five. Reconciling the ids onto the engineering ladder loosened the UAT gate twice, and the first version of this entry wrongly called the change policy-neutral. A defect a tester could not finish at all was S1 in UAT, and the UAT exit criterion "No open S1" had no acceptance path, so it was an absolute block; it is now S2, which the sponsor may accept in writing. A job that completed only with a workaround was S2 in UAT, blocking unless the sponsor accepted it; it is now S3, which ships with a named fix owner and a fix date and never blocks. Both UAT classes moved one notch down in blocking strength. Migration: a team with a UAT plan filled from the old template should re-read any defect it logged as S1 or S2, because the same words now select a different id and a weaker rule, and should decide whether to keep the old bar by writing it into the UAT exit criteria. This is a change to what the gate demands, and it is the release owner's call, not a wording fix. The rule forbidding a second severity-definition table ran over the UAT plans alone and now runs over all four covered kinds, exempting only each document's own canonical table: the ladder, the UAT crosswalk, the support crosswalk and the release-readiness decision table. A second table is one keyed by the IDs in any letter case, one holding them in a column it does not call Severity, one pairing a severity with what it means or when it blocks, or one parked inside an HTML comment. That column rule has a disclosed limit: a column the table does not call Severity is read as a severity scale only when every filled cell in it is a canonical ID, so a second definition table that puts the IDs in a later column, adds one row that is not an ID, such as `(other)`, and calls no column Severity is not caught, and this was measured in all ten covered documents rather than in some of them. Still caught: the same table with every row canonical, the same table with the IDs in the first column and the decoy row kept, a blank cell used as the decoy, and any column the table does call Severity whatever its rows say; the shape above is what a reviewer has to carry, and closing it means widening the rule, which is a change to what the gate demands and is not made here. A covered document may also write no other severity vocabulary at all, and a new check reads its prose, comments and code blocks included, for a definition attached to an ID in either word order. Prose that defines a defect class WITHOUT naming an ID is not caught, states a rule of its own and contradicts nothing by ID; the ladder says so in its own words and review has to carry it. Two lines in examples/domain-gaming-release-readiness.md called known issue #2 Low while the table called it S4, and now say S4. Audit 2026-09-23, finding F03.
- **The flagship PRD's worked example is now a complete fill.** `templates/definition/prd.md` pointed at `examples/expense-copilot-prd.md` and said in its own pointer line that the example had no section 0, 5 or 9 to 13, no sign-off and no exit gate, while `README.md` leads with that chain as the model of a gate-surviving artifact. The example now carries the whole spine, sections 0 to 13 with the template's own numbering, plus the sign-off block and the exit gate: the one read, an objectives table with a metric, baseline, target, owner and measurement site per objective, a non-functional summary, a success-metric table with the guardrail and its instrumentation, an out-of-scope table, kill criteria with a threshold, a check point and a named caller on each row, the four risks each with counter-evidence and a confidence, an assumptions table, four open questions, and the companion table answered Yes or No with a reason on all sixteen rows. Nothing was invented to fill it: every id, figure and date traces to `examples/expense-copilot-journey.md`'s V-rows or `examples/ledgerline-journey.md`'s N-rows, the sections Gate 2 would otherwise expect from documents this fictional build never wrote (a non-functional register, an assumptions register, an FRD, a personas file) are named as gaps with an owner and a date rather than filled with fiction, and the sign-off block says outright that every approval in it is illustrative and that no real person signed anything. The template's pointer line now describes what the example is. Its headings are numbered, so three links into it moved: `examples/expense-copilot-acceptance-criteria.md` now cites `#3-users-and-stories` and `#4-functional-scope`, and `examples/expense-copilot-data-model.md` cites `#8-launch-criteria` twice.
- `tools/journey_chain.py`'s answers for DEFINE-4, DEFINE-6, DEFINE-7, DEFINE-9 and DESIGN-6 follow the example they are drawn from: the four renamed sections, and two answers that had gone out of date with the document. DEFINE-6 counts six exclusions rather than four, and DEFINE-7 no longer says the trade-off table is the nearest thing to an assumptions register, because section 11 now is one and says so. `examples/journey-chain.md` is regenerated from the generator. What the chain proves is unchanged: no answer gained a commitment its document does not record, and DEFINE-6, DESIGN-2 and DESIGN-5 are still artifact evidence.

- `tools/docs_contract.py` reads a gate count written in words as well as in digits, up to ninety-nine, with "named" as well as "release" allowed before "gates"; takes a line naming `ci_gate.py` without its `tools/` directory as naming the file; and reads `docs/ARCHITECTURE.md` as well as `README.md` and `docs/FAQ.md`.
- `README.md`'s 188-word paragraph on the example journey is now a two-sentence lead and a three-item list: what the journey indexes, that it is not a runtime record, and where the runtime records are. The list names the discovery document among the fourteen artifacts, which the paragraph had left out.
- The Conductor now checks a supplied quotation against the document it cites, and refuses the answer when it cannot. Before this, an answer citing a real workspace file with `"quote": "THIS SENTENCE IS NOWHERE IN THE FILE"` was accepted and the invented sentence was stored beside `"verification": "source_verified"`, a label that only ever meant the cited path exists; the same quote against free text was accepted too. An evidence field is an excerpt field when its key, lower-cased and with the separators `_ . : -` removed, contains `quote`, `quotation`, `excerpt` or `verbatim`, so `Quote`, `quote_text` and `verbatimQuote` are checked exactly like `quote`. Evidence keys are ASCII only, so no look-alike letter spells one of those words; a key that contains none of them, such as `said`, is still stored as supplied and nothing checks it. Every non-blank excerpt field must be at least three words and must occur in the resolved source file, compared after collapsing every run of whitespace, line breaks included, to one space and with nothing else folded, so case and punctuation must match. A match records the new label `quote_verified`, which says those words occur in that file and nothing more. Five refusals are new, each of which challenges the answer the way any invalid evidence does, writing a turn and advancing the store revision, spending one of the two challenges, and parking the question on a third: the quote is not in the file (the refusal names both); the quote is shorter than three words; the source is not a document inside the workspace (free text, an interview id, a web address), because a quotation can only be recorded against something that can be opened; the document cannot be read (a symlink, bytes that are not UTF-8, or a reader that fails); and no document reader is configured. A gate proof whose evidence carries an excerpt field is held to the same rule and blocked when the excerpt is not in the gate source. Through `pmos` that case was already unreachable: no shipped bank declares a gate prerequisite, so a gate proof with an extra field is refused as a schema mismatch; the check covers a library caller that builds a `QuestionBank` with an excerpt field among its prerequisites.
- The text comes from a new injected `document_reader` beside `source_resolver` in `pmos/product.py`, because `pmos/conductor.py` has no filesystem access by construction and the resolver answers only True, False or None. It reads under the same bounds as the gate verifier, which now shares its walk: below the workspace root and outside `.pmos`, every path component opened without following symlinks, a regular file of at most 16 MiB by its reported size and again by the bytes actually read. The final open no longer blocks, so a named pipe planted at a cited path is refused at once instead of hanging `pmos answer` or `pmos gate`, which the gate verifier did before. Both runtime shapes get it, the pinned-contract products and the legacy onboarding ones. A test parses `pmos/conductor.py` and fails if it imports `pathlib`, `os`, `io`, `shutil`, `tempfile` or `glob`, or calls `open`, `read_text` or `read_bytes`.
- `pmos status --json` reports `quote_verified` as its own figure beside `source_verified` and `supplied_unverified`, and so does each phase's `completed` block; `pmos handoff --json`, `handoff/context-index.json` and `handoff/CONTEXT.md` now carry all three. The three figures partition the accepted answers, each counted once under the strongest label it earned, so `source_verified` never includes a checked quotation and can never be read as a count of them. `development_ready` does not depend on them.
- Not changed, deliberately: an answer that supplies no excerpt field, in the sense above, is accepted and labelled exactly as before, `source_verified` when its cited file exists and `supplied_unverified` otherwise, byte for byte. Quoting is not required. So most evidence in most products still carries no checked quotation, and a `source_verified` answer says the file exists, not that it says what the answer claims. Making quotation mandatory would change what every existing product and worked example is refused, and is a separate decision.
- [docs/RUNTIME-QUICKSTART.md](docs/RUNTIME-QUICKSTART.md) states once, beside the readiness conditions, that how many answers cite a workspace document is reported and is a condition of nothing, and that a development-ready report does not certify that every answer is evidenced or that any typed actor ID is authenticated. Its account of which refusals advance the store revision is now a table, and `tests/test_pmos_conductor.py` drives every row through a real Conductor, so a row that is wrong about the revision fails a test.

### Fixed

- Four small editorial errors an external audit found, each of which parsed and none of which any check read. `templates/discovery/discovery-synthesis.md` carried its `### Theme 1` heading twice in a row, so whoever filled the form met two Theme 1 sections and one set of fields; the duplicate is gone. `templates/ai/eval-spec.md` sent a reader in a comment to `../architecture/ai-interaction-spec.md`, which is a real path from nowhere in this tree; the file it means sits beside it and the comment now says `./ai-interaction-spec.md`. `templates/discovery/interview-guide.md` told its filler that no question may ask about the future while its own Block E, which the next line requires to be present and last, asks what the participant would do next; the exit-gate line now states that exemption in the words Block E's own note uses, and the note says why a question about a next step is still a question about behaviour. And this file carried two `### Fixed` headings under `## 0.8.0, 2026-09-21`, which the new duplicate-heading check reports; the second is now `### Fixed, the development handoff's readiness report`, after the change it records. Nothing in the 0.8.0 entries was rewritten.
- The same contradiction, in the three files the first correction left behind. `templates/discovery/interview-guide.md` banned questions about the future on its exit-gate line while its own Block E, which the next line requires to be present and last, asks what the participant would do next; the template was corrected above, and the filled example it links, `examples/sahulat-interview-guide.md`, still carried the pre-fix line ticked as met. So did `frameworks/discovery/mom-test-interview-guide.md`, whose rules R1 and R2 rule out the 22-to-27-minute commitment probe R7 requires, and so did that worksheet's own filled example, `examples/sahulat-mom-test-interview-guide.md`. All three now name the exemption in the same words, "except in the closing commitment probe", and each says why it is one question wide: the probe asks for a step the participant could take this week, not an opinion about the idea, so the answer is checkable against what they afterwards do. Six lines in four files carried it, and the new `commitment-probe` check reports every one of them.
- A false positive in the `duplicate-heading` check, found before it could fail anyone's build: a heading-shaped line inside an HTML comment was read as a heading, and this tree's templates are built out of guidance comments, one of which shows the filler a repeated section by writing it twice. Comments are now skipped the way fenced blocks already were. A real duplicate after a comment is still reported.
- [SECURITY.md](SECURITY.md) said "`tools/` holds eighteen scripts in all" while the directory held 27, and named `tools/ext_ai_probe.py` as the only script that leaves the machine while `tools/model_matrix.py` had grown a `urlopen` of its own against the loopback gateway. Both sentences were true when they were typed, which is how they survived. The count and the exceptions are now the generated block described above, the prose around it names both scripts that call out and says that the other four scripts the table lists read an environment variable without leaving the machine, and the file's review-date line no longer dates the script list, because a gate now fails when it is stale.
- Three ways past the four checks above, each one found by a reviewer walking the checks rather than reading them, and each the same defect the check exists to close written one spelling to the side. `tools/exec_surface.py` recognised a module on its list only where an `import` statement spelled the dotted name, so `from http import server`, `from http import client` and `from xmlrpc import client` were read as naming nothing while `import http.server` was read: `urllib` was the only package with a case of its own. A script in that spelling dropped into `tools/` got no row and was folded into the sentence saying the rest name nothing on the list, with every gate green, while the block prints `http.server`, `http.client` and `xmlrpc.client` inside the list it claims against. A dotted name is now assembled before it is compared, and compared in one place, so `import http.server`, `from http import server`, `from http.server import HTTPServer` and `import http` used as `http.server` all name the same module; the block says so in the sentence that prints the list. A relative import such as `from . import server` names a file in this tree and is not read, and the suffix test is on a dot, so `urllib.parse` is still not `urllib.request`.
- The `duplicate-heading` check read only one of CommonMark's two heading spellings. A heading repeated as `## Zed` and `## Zed ##` was two headings to the comparison, because the closing hashes stayed in the text it compared, and a setext heading -- a line of text underlined by `=` or `-` -- was not read at all. Both are read now. A `-` underline is taken as a heading only when the line above it is ordinary paragraph text, so a table delimiter, a thematic break and a list item are left alone, and YAML front matter is skipped whole because its closing `---` underlines the last line of the block.
- Two narrow readings in the checks that close the other two. `script-count` read four wordings of a whole-directory claim and not "`tools/` contains eighteen scripts." or "There are 18 scripts under `tools/`."; it now reads "contains" beside "holds" and "all", and a count followed by the directory. A count of a named subset, such as this repository's own "Six local scripts stay on this path", is still not read. `commitment-probe` read a rule only on a table row or a checkbox item, so the same ban written as a plain bullet was not seen; it now reads a list item under any bullet or number. A rule stated in running prose is still not read, and that is a stated limit with a reason: `frameworks/discovery/mom-test-interview-guide.md` opens by summarising its own rules in a sentence, and a check that read paragraphs would demand an exemption clause from prose that is describing the rules rather than stating one.
- A sentence in `check_declared_paths`' docstring claimed coverage the tree does not have. It said a markdown link with a missing target is caught meanwhile by `lint.py`'s LINK check, two clauses after naming a reference containing a space as a stated limit; a link written with a space in its destination and no angle brackets is not reported by that check. It is not a markdown link at all -- CommonMark does not read an unbracketed destination containing a space as one -- and the spelling that is, the same destination wrapped in angle brackets, is reported. The docstring now says that, and a test pins all three cases.
- The read-only shell allowlist in `pmos/hooks.py` classified an executable's basename and ignored its options, subcommands and file operands, so three write-capable commands were returned as `allow`: `sort input -o output`, `sed -n "w written" input` and `git remote add audit <url>`. An external audit of 49ca7e8 ran all three through `decide` and then ran them for real in a disposable directory; all three mutated it. Each is now `ask`. `sort` is checked for `-o`/`--output` in every spelling, including a bundled or glued short option; `uniq` is checked for the second file operand it overwrites; `yq` for `-i`/`--inplace`/`-s`; `find` for `-fprint`, `-fprint0`, `-fprintf` and `-fls`; and a long destination spelling (`--output`, `--output-file`, `--write`, `--in-place` and four more) is refused on any allow-listed program, so a destination is protected by the shape of the argument rather than by which program carries it. `sed` is now classified by its script rather than by its name: a new scanner walks the script and reports it read-only only when it can account for every command in it, so `w`, `W`, `s///w`, `e`, `r` and `R` are refused, an unrecognised sed option or `s///` flag is refused, `-f script.sed` is refused because the script is not readable before the command runs, and `-n '1,5p'`, `s/a/b/g`, `2{p;q}` and `y/abc/xyz/` stay allowed. `git remote` still lists remotes, but `add`, `rename`, `remove`, `rm`, `set-head`, `set-branches`, `set-url`, `prune` and `update` ask, `show` asks because it contacts the remote, an unrecognised sub-subcommand asks, and a read-only Git subcommand carrying `--output`, `-o`, `-O` or `--open-files-in-pager` asks. Three wrappers stopped being treated as transparent: `time -o FILE` writes FILE, `env -S` re-splits one token into a command line this classifier never sees, and `nohup` appends to `./nohup.out`, so each is now classified itself instead of being stripped off its child. What did not change: this is a hook policy, and a host that does not consult it is unaffected either way; the audit's three probes still mutated the sandbox when run directly, because being classified `ask` is a decision for the host to enforce, not an interception.

- An independent review of that fix found nine further commands of the same class still returned `allow`, three of them observed mutating a disposable directory: `GIT_EXTERNAL_DIFF=./x git diff`, `git log` with a backticked argument, and `git grep -O./x` with the program glued to the option letter. An environment assignment written in front of a command is no longer skipped silently. It is still stripped before classification, but the variable name is now read, and a name that can name a program, a library, a configuration file or an interpreter's options - `GIT_*`, `LD_*`, `DYLD_*`, `PATH`, `HOME`, `PAGER`, `EDITOR`, `BASH_ENV` and others, matched by exact name, prefix or substring - downgrades an `allow` to `ask`; an inert name such as `MODE=safe` is still allowed. Backticks and `$` were already refused in an allow-listed program's arguments, but on the Git branch only the resolved subcommand was read; every Git argument is now checked, and so are `find`'s arguments and `sed`'s file operands - not `sed`'s script text, where `$` is a legal line address. `git --config-env` is refused like `-c`. `--exec-path`, `--git-dir`, `--work-tree`, `--namespace`, `--super-prefix` and `--attr-source` ask when they appear before the subcommand; after it the same spelling is a read-only query (`git rev-parse --git-dir`) and stays allowed. `--ext-diff`, `--textconv` and `--filters` ask wherever they appear, because each hands control to a program named by the repository's own configuration; the `--no-` spellings stay allowed. The Git output check added in the same change used an option-name test that could not see a value glued to a short letter, so `git grep -O./x` slipped past the guard added beside it; a capital-`O` letter test now covers it, and lowercase `-o` is untouched because `git status -uno` and `git ls-files -o` are ordinary usage. An option whose value names a program - `--pre`, `--pre-glob`, `--hostname-bin`, `--compress-program`, `--pager`, `--filter`, `--exec`, `--command`, `--rsh`, `--editor`, `--diff-command`, `--sh`, `--shell` - asks on every allow-listed program, so `rg --pre PROG` and `sort --compress-program=PROG` are no longer read as reads. The review also found two guards from the first round, the `env -S` and `nohup` guards, that broke no test when reverted on their own; every guard from both rounds now breaks a named test when reverted individually, checked by reverting each of the seventeen in a throwaway copy. What still does not change: as before, `ask` is a decision for the host to enforce. This entry's own disclosed limit, that `git -C <dir>` stayed allowed, was wrong to leave open and is closed by the entry below.

- A second independent review of that fix proved, by execution, that the same class was still open: `git -C <dir> diff` against a repository whose config set `diff.external`, and `git -C <dir> status` against one whose config set `core.fsmonitor`, were both classified `allow` and both ran the program the repository named. `git status` needs no options at all for this. The previous round had deliberately left `-C` out, on the grounds that it only changes directory. That was wrong: changing directory is what makes git discover and load that directory's repository configuration, which is the same mechanism as `--git-dir`, which the same change already refused. `-C` is now a member of the same set, in the global position only - after the subcommand `-C` is copy detection and stays allowed - and the comment that stated the wrong reason is gone. The check runs after the destructive-subcommand checks rather than before them, so `git -C <dir> reset --hard` is still a `deny` and not softened to an `ask`. The same redirect spelled on a wrapper is closed too: `env -C <dir>`, `env --chdir=<dir>`, `sudo -D <dir>` and `sudo --chdir=<dir>` were stripped silently, leaving no trace in the child's arguments; a wrapper that changes directory now downgrades an `allow` to `ask`. A further bypass was found while fixing that one, reported by neither review and also measured executing: every guard here matched exact option spellings, but GNU `getopt_long` and git's `parse-options` accept unambiguous abbreviations, so `git grep --open-files-in-pag=./x` started ./x on git 2.50.1 while the full `--open-files-in-pager` spelling was already refused. The program-value and write-destination sets are matched by prefix as well as exactly for the same reason, which refuses `sort --compress-prog=./x` and `sort --outp=FILE`; those two are decision-level only, because the sort on the machine this was written on is BSD sort and does not accept abbreviations. The cost, stated plainly: `git -C <dir> status` is no longer allowed, which the previous round's tests asserted, and those assertions were changed. What still does not change: `ask` is a decision for the host to enforce, not an interception.

- A third independent review found the same class still open one spelling out. The previous round added a guard for wrappers that change directory (`env -C`, `env --chdir=`, `sudo -D`, `sudo --chdir=`) and, in the same round, made other option sets tolerant of GNU long-option abbreviation, but left the wrapper chdir check an exact-spelling test, so `env --chd=evil git status`, `env --ch=evil git status` and `sudo --chd=evil git status` returned allow while the full `--chdir=` spellings correctly asked. The reviewer proved on this machine that sudo accepts the abbreviation: `sudo -n --chd=/tmp true` reaches authentication, while `sudo -n --zzz=/tmp true` is rejected as an unrecognised option. For env it is decision-level only here, because `/usr/bin/env` on this machine is BSD env with no long options at all, whereas GNU coreutils env parses `--chdir` through `getopt_long`, where `--chd` and `--ch` are unambiguous. The fix is general rather than two more strings: every long-option comparison in the file now goes through one helper, `_matches_option`, which drops a glued `=value` and matches long spellings abbreviation-tolerantly, while short spellings stay exact because short options are not abbreviated. Sweeping the rest of the file for exact-spelling comparisons found three more of the same class, reported by no review. `time --output=FILE git status` returned allow with the FULL spelling: the output option was detected, but the wrapper token and the option had already been consumed by the scan, so the code that meant to classify the wrapper classified the bare `git status` it wraps; the scan now rewinds to the wrapper, and `time --outp=FILE` and `time --app=FILE` were a second, separate miss now covered by the helper; a third, found by asking what the same option looks like written short, is `time -o/tmp/f git status` and `time -ao/tmp/f git status`, where the value is glued to or bundled with the letter and no option-name test can see it at all, so the letters of a short token are now read the way a write destination is read elsewhere. The `time` spellings are decision-level on this machine: `/usr/bin/time` here is BSD time, which has no long options, and most shells make `time` a keyword rather than running that binary; on a GNU host `time --output=FILE` truncates FILE. What is not decision-level is that the round that added the `time` guard said in this file that the wrapper was "classified itself instead of being stripped off its child", and for the glued long spelling that was not true - the wrapper and its option had been consumed, and the bare `git status` was what got classified. `git --config-en=core.pager=EVIL log` returned allow while `git --config-env=` was a deny, and both spellings now deny; that one is a refusal by shape rather than a closed exploit, because git 2.50.1 was measured rejecting it - `git --config-en=foo.bar=V rev-parse` prints `unknown option: --config-en=foo.bar=V`, since git's top-level options are parsed by a hand written parser that does not abbreviate, unlike the subcommand options `parse-options` reads, where `git grep --open-files-in-pag=./x` was measured executing. The `sudo` spellings, by contrast, are accepted by the real parser here: `sudo -n --chro=/tmp true` reaches authentication. And `sudo --chroot=evil git status` and `sudo -Revil git status` returned allow, so sudo's `-R`/`--chroot` spellings join `-D`/`--chdir`: pointing the child at a caller-chosen root directory is the same redirect as changing into one. The two guard families are now crossed by a test, which they were not before: the abbreviation test probed the prefix-matched sets and the wrapper test probed only the full `--chdir`, so no test discriminated in between. The cost, stated plainly: an abbreviation of a safe option that happens to be a prefix of a guarded one is refused too, so `env -uCFLAGS ls` asks because the bundled token carries a capital `C`; the 25 read-only positive controls are unchanged. Deliberately left as exact-spelling tests, with reasons. The git external-program options (`--ext-diff`, `--textconv`, `--filters`), because git 2.50.1 rejects `--ext-d` and `--textcon` as unrecognised arguments, so prefix-matching there would cost the read-only `git log --text` and buy nothing. And the value-consuming option lists in the wrapper parsers (`nice --adjustment`, `timeout --kill-after`, sudo's value options, uniq's field options, sed's safe long flags), where an abbreviation makes the parser stop early and the command falls out to an ask, never to an allow - each measured, not assumed. Residuals this entry does not fix and discloses rather than leaving silent: `curl --confi=FILE` is an ask where `curl --config FILE` is a deny, which changes the reason and not the outcome, because every curl command asks anyway; `git --paginate log` and `git -p log` are still allow, and in a non-tty sandbox with `core.pager` set the pager did not fire; and when the shell's own working directory is ALREADY inside a hostile repository, plain `git diff` and plain `git status` are allow and do run the program that repository's config names - that is the standing limit of any classifier that reads only the command string, it is identical on 49ca7e8, and no allowed command string reaches it, because `cd evil && git status` and `pushd evil && git status` both ask. One correction to the review that prompted this entry: `rg --file patterns.txt` is allow, not ask - `--file` is not a prefix of `--filter`, the two diverge at the sixth character - while `rg --fil patterns.txt` does ask. The previous entry's sentence saying the prefix test was applied to "the program-value and write-destination sets" was incomplete: the wrapper chdir check stayed exact, and that is the hole this entry closes. What still does not change: `ask` is a decision for the host to enforce, not an interception.

- A fourth independent review proved the same class still open, three spellings out, and all three executing. The previous round guarded the wrapper option that changes DIRECTORY and nothing else, so ``env --C<dir> git status`` and ``env --C<dir> git diff`` were allow and reached the pointed-at repository's ``core.fsmonitor`` and ``diff.external``, and ``env --P<dir> git status`` and ``env -P<dir> git status`` were allow and ran an attacker's ``./git`` outright, because ``-P`` names the directory env resolves the utility from. The guard could not see them because it read a short cluster only from a single-dash token and a long option only from a ``--`` token. macOS/BSD env has no long options at all, so its ``--`` prefix is not a long-option marker: it was measured reading ``--iP/dir`` exactly as the cluster ``-iP/dir``, and ``--Path=/tmp/bin`` as ``-P`` carrying the value ``ath=/tmp/bin``, and a planted ``./git`` was executed by both ``env -P/tmp/x/bin git status`` and ``env --P/tmp/x/bin git status``. The fix is one class rather than three strings. An option that says WHERE the child runs and an option that says WHICH binary runs are the same hole, and one helper, ``_redirects_execution``, now reads every wrapper option token for both: long spellings go through the abbreviation-tolerant matcher, a single-dash token is read as a short cluster with its value glued or bundled, and a ``--`` token that spells no guarded long option is read as a cluster too, but only against the UPPER-CASE guarded letters, because every long option name is lower case and must not be misread as a cluster. Sweeping every wrapper the policy strips for the same property found more of it. ``env``: ``-C``, ``-P``, and every spelling of ``-S``, whose glued ``env -Ssort git status`` had been an allow. ``sudo``: ``-D``/``--chdir`` and ``-R``/``--chroot`` were already guarded, ``-i``/``--login`` and ``-s``/``--shell`` run the caller's shell instead of the named program, and ``-E``/``--preserve-env`` lets the caller's own PATH and loader variables through the reset that decides which binary is found; all three were allow. sudo 1.9.17p2 was measured accepting ``-s``, ``-E`` and ``--preserve-env=PATH``, each of which reaches authentication, and rejecting ``--D/tmp`` as an unrecognised option, so that last spelling is refused by shape rather than being a closed exploit. ``command``, ``timeout``, ``nice`` and ``time`` have no option that names a program or a directory, and ``nohup``, ``xargs`` and ``busybox`` are not stripped at all and already ask or deny. The cost, stated plainly: a sudo short cluster carrying ``i`` or ``s`` asks even when that letter is part of a value, so ``sudo -uinvited git status`` asks, which is the same over-ask family as ``env -uCFLAGS ls``; the read-only positive controls are unchanged. Residuals this entry discloses rather than leaving silent. ``sudo --is git status`` is an allow, because a ``--`` token is read only against the upper-case guarded letters and sudo's lower-case ``-i``/``-s`` are not read there; sudo rejects ``--is`` outright as an unrecognised option, so nothing runs. ``env --argv0=X`` is not guarded, because it renames argv[0] and does not change which binary is executed, and this env rejects it anyway. And the largest one: this policy classifies a program by its basename, so ``./git status`` and ``/tmp/evil/bin/git status`` are allow, exactly as they are on 49ca7e8 and unchanged in either direction by any round of this work. Closing that would need the decision path to judge whether a path is trustworthy, which is a filesystem question this classifier refuses to ask, for the reason an earlier round recorded when it rejected a repository-existence check: I/O, symlink and relative-path resolution, and a time-of-check window in the decision path. What still does not change: ``ask`` is a decision for the host to enforce, not an interception.
- **A UAT plan could pass its own exit criteria with a charter that failed.** `templates/delivery/uat-plan.md` asked only that every charter had run and that none was Blocked, so a charter whose Result was Fail was closed by the others passing, with nothing tying it to a defect record or to an accepted exception; and no tester result named the build it was produced against, so a plan could accept a release nobody had tested. The template now carries a `Candidate build`, `Environment` and `Fixture set` line; a charter table with a column for the acceptance criteria, the build and the evidence as well as the defect and the exception; an accepted-exceptions register with an approver, a date and a retest result; and a sign-off bound to a named candidate build, with the rule that changing the candidate voids the verdicts. `lint.py --workspace` gains a seventh check, `UAT acceptance`, which reads a filled copy against that contract and fails it: a failed charter with no defect and no exception, an exception the register does not carry or that was approved for a different charter, an exception with no retest result, a Blocked charter, a charter run against a build that is not the candidate, and a sign-off bound to a build the charters were not run against. Stated limit: it fires only once the copy claims UAT is finished, which is a ticked exit-criteria box or a filled sign-off verdict. A blank copy and a plan still being filled in are not making that claim, and `tools/readiness_probe.py` installs every shipped template into a workspace and lints it. `tests/test_lint.py` gains `UatAcceptanceTests`, whose cases run through the real workspace gate; `docs/readiness/test-classes.json` records the class. `examples/harbourgate-uat-plan.md` is refilled against the new shape on candidate build rc-2026-07-02.3 and a test holds it to the check. `templates/delivery/release-readiness.md` and `examples/harbourgate-release-readiness.md` now ask for the UAT sign-off against the build being released. Four ways of walking past that check were found in review and are closed here. It read only the first charter table in the charter section, and a markdown table run ends at the first line that does not start with a pipe, so one blank line or one sentence above a charter row hid that row and every row below it; it now reads every complete charter table in the document, reports any run of table rows that has no header above it, and reports a table inside the charter section that does not carry the required columns, so a charter cut off from its table is a finding rather than a silence. It read only the first accepted-exceptions table, so a fully approved decoy above the real register answered for it; it now merges every register in the document and reports an exception id used by more than one row. It found the sign-off section by its number alone, so renaming or renumbering that heading turned the whole check off; it now finds that section by its number or by its words, and a plan signed only at the closing exit gate also counts as claiming completion. It read the build, environment and fixture identity out of the raw bytes, so those fields satisfied it from inside an HTML comment or a code fence; they are now read from the rendered document, every occurrence of each field is read, and two different answers to the same field are refused. The template says the first and second of those rules in prose as well: keep every charter in one table, and give each exception its own id. The template's generated "What checks this" paragraph, which says no tool checks whether what you write is right, now also names the opt-in workspace check that reads a filled copy, so the sentence does not read as a claim that nothing anywhere reads it; `tools/what_checks.py` renders that clause and the template was regenerated with it. A fifth way past the check was found in the next review: the check bound each column of the charter table to the first header cell whose name contained the column's keyword, so `Expected result` placed beside `Actual result` bound the whole result contract to the expected column and a failed charter read as a pass, and a `Build under test` column defeated the build comparison the same way. That was first fixed by refusing any column whose keyword appeared in more than one header cell, and the next review defeated the fix one spelling over: on a table headed `Expected result | Outcome` the bare word `result` appears exactly once, so the count saw no ambiguity, bound the expectation, and read a failed charter as a pass again. Columns now bind by name. A header cell binds a column when its name, normalised the way a reader reads it, is that column's name or one of a listed set of ordinary synonyms; two cells this check would accept for one column are refused as ambiguous and bind nothing, so every row reads that column as missing and the document fails closed; and a table where no cell names a column this check reads is refused with that column named, so a charter table whose results column carries a spelling this check does not know is an error rather than a document that passed because its results were unreadable. `Expected result`, `Done looks like` and the other expectation names bind nothing by design, and a second column holding nothing but Pass, Fail and Blocked that disagrees with the bound result column is reported, so parking the real results under a name this check does not know is a finding rather than a hiding place. Two limits are stated in the code and here: a build recorded in a second, unaccepted build column is not read, because build IDs are not the closed vocabulary that Pass, Fail and Blocked are; and a value written in an expectation column is read as an expectation and never as a result. The accepted-exceptions register binds by the same rule, and the completion trigger reads every verdict-shaped column rather than the first, so a blank decoy verdict column no longer means the document never claimed completion. A well-formed table whose cells hold Pass, Fail or Blocked is now read wherever it sits, not only under a heading numbered 4 or carrying the word charter, because an incomplete charter table parked under any other heading was skipped in silence. A filled copy is recognised by the sign-off binding it carries as well as by its filename and its `template:` field, so a copy renamed out of both conventions is no longer read by nothing. A sixth way past the check was found in the next review, one layer below the binder: the function that decided whether a table the binder cannot read is examined at all still picked its candidate columns with the keyword `result|outcome|status|verdict`, so a second charter table of the shipped shape, parked outside a charter-worded heading with its results column headed `Pass/Fail`, was looked at by nobody and its failed charter passed in silence. What makes a table a charter table is now the table's own shape rather than one header word or the heading above it: a table that carries four or more of the charter table's seven non-result columns under the names this check accepts, or that holds a column whose every answered cell reads as Pass, Fail or Blocked, is read as a charter table wherever it sits, and is refused with the column named when no column of it is named for the result. That detector reads a cell's first word, so `Fail (see log entry 40)` counts as a Fail, while a bound charter table is still held to the closed vocabulary exactly. The accepted-exceptions register is exempt from the value rule, because its retest column holds those same three words, and is not exempt from the column rule, so a charter table wearing a register's header is read rather than skipped. The keyword match is gone from this check. Two further limits are stated in the code and here, and the first of them is a silence rather than a refusal: a table carrying fewer than four of those columns which also records its results in some other vocabulary, a tick or `OK` or `Passed`, shares no structure with a charter table and is read by nobody; a cell written past the width its header declares is not read either, because no markdown reader renders it; and the guard that reports a second, contradicting column of Pass, Fail and Blocked matches that vocabulary exactly, so one annotated cell in the decoy column puts it past that guard, which is why the column rule and not that guard is what closes the parked-table class. The template states the column rule and the shape rule in prose beside the one-table rule. `UatAcceptanceTests` now holds forty-nine cases, and each of the check's guards fails a named case when it is reverted alone. Not changed: the severity wording in section 5, which disagrees with `templates/delivery/testing-strategy.md` and is a separate finding.

- [templates/discovery/evidence-note.md](templates/discovery/evidence-note.md) demanded a verbatim quote of every note while listing metric exports, datasets and observations among its source types, so an analyst holding a measured count had to invent a spoken sentence or fail the form. The shipped [examples/ledgerline-discovery-synthesis.md](examples/ledgerline-discovery-synthesis.md) shows what that cost: four of its themes carried the string "[No verbatim quote retained. EV-C01 to EV-C06 are paraphrased notes, not transcripts.]" inside the quotation marks the field asked for. The claim block now declares an evidence kind, one of text quotation, quantitative or observation, and offers one block per kind: text quotation keeps the verbatim quote and adds where in the source it sits; quantitative asks for the snapshot or query, the filters, the denominator, the period with its timezone, and the calculation; observation asks for the session or timecode, what was observed, and the context. Exactly one block is filled and the other two are deleted. The ledger column `Verbatim quote` is now `Evidence (quote, measure or observation)`, and changed with it in [templates/execution/state.md](templates/execution/state.md), [examples/sahulat-state.md](examples/sahulat-state.md), [examples/sahulat-evidence-note.md](examples/sahulat-evidence-note.md) and [docs/CONDUCTOR-DESIGN.md](docs/CONDUCTOR-DESIGN.md), because the note says that row is copied unchanged into the product's STATE.md. The exit gate's single quote item became four, one for the declared kind and one for each kind's own evidence. [templates/discovery/discovery-synthesis.md](templates/discovery/discovery-synthesis.md), which consumes these notes, changed its per-theme `Load-bearing quote` to `Load-bearing evidence`, naming the evidence note it comes from, and its four themes in the Ledgerline example now say plainly that no transcript was retained rather than saying it between quotation marks.
- Section 2 of [templates/discovery/discovery-synthesis.md](templates/discovery/discovery-synthesis.md) counts participants as well as sources. Themes below it are weighted by source count, and someone who filed four tickets and sat one interview was five rows and one voice. The totals cell now asks for the number of distinct participants behind the sources, the guidance says a system export is a source with no participant behind it, and the exit gate's totals item says the count is by participant rather than by artifact. The Ledgerline example states six participants behind its nine sources and names which three sources have none. Nothing checks this figure: like the rest of the form it is read by the people who sign Gate 1.
- `check_evidence_contract` in [tools/docs_contract.py](tools/docs_contract.py) holds that contract: the template must offer all three kinds and every field of each, a ledger column that accepts only a quote is reported, a theme line that demands a quote is reported, a STATE.md ledger that no longer carries the note's row is reported, and the shipped filled note is read as a filled note, where exactly one kind is declared, its own fields are answered rather than left as the bracketed instruction, a text quotation carries its quote, and a quantitative note or an observation carrying a quoted sentence is reported as quoting words nobody said. `EvidenceNoteContractTests` in [tests/test_tools_gates.py](tests/test_tools_gates.py) is the closure proof: three fixtures, one interview, one SQL metric and one watched usability session, each passing on the evidence it actually has, and mutations that put the old form back one piece at a time. What this cannot do, stated rather than hidden: it reads the contract and not the analysis, so it cannot tell whether a denominator is the right denominator, whether the query was ever run, or whether the session was ever watched, and a note that declares a kind and fills its fields with plausible invented text passes. It reads the files it names and no others, so a filled note kept in a product workspace is checked by the people who sign the gate. And it constrains quotation marks, not honesty: an invented sentence written outside them is not caught here.
- `templates/ai/multi-agent-workflow.md` told an author two different things about a reached cap. Section 4 said the run halts at any cap in section 5; the cap table's own row offered, at the same ceiling, `[halt and escalate / degrade to the cheap tier per ../../routing/README.md; state which]`, and the section's guidance said a document fails "when every ceiling escalates to a human with no cheaper degrade path". Both halves of the repository it defers to say the opposite: the `fail-closed` rule in [AGENTS.md](AGENTS.md) is halt and queue, never quietly route the work to a cheaper tier, and the runtime does exactly that (`harness/runner.py`'s `spend_gate` raises before any provider call, and `pmos/routing.py` stops admitting fallback candidates once the budget cannot reserve them). The two events are now separate rows. A pre-authorised route degradation names its trigger threshold, the cheaper route and who authorised it, and sits below the ceiling; at a ceiling the only value is halt, preserve state and queue for a named role, with a raised cap or new authorisation needed to resume. The termination section says the budget stop schedules nothing further on any model or tool, a cheaper model included, and names route degradation as not a termination path. A restart line names the step a resumed run starts from and how a replayed handoff avoids a second non-idempotent effect, which the register's own recommendation for this template also asked for. A sixth exit-gate line checks the separation, and `examples/ledgerline-multi-agent-workflow.md` fills both rows: it has no pre-authorised degradation, so every cap there is a halt. `tests/test_pmos_invariants.py`'s new `BudgetStopIsNotADowngrade` fails on any line in either document that offers a cheaper tier without refusing it, on a cap table missing either row, and on an edit that closes the gap the wrong way round by weakening the AGENTS.md rule. What this does not do: it reads these two documents, not every template, and no checker reads a filled copy of this template, so an author who writes a cheaper-tier continuation into their own filled document is caught by the Gate 3 signer, not by a test.
- A Gate 5 checklist line was reported wrongly from 0.8.0 until this change. `pmos status --json` and the desktop adapter's `pmos_status` tool, which returns the same phase report, listed "AI overlay: guardrails live, kill switch tested" as unmet on every product, including every product that had answered all three questions it cites. The report looked BUILD-5 and BUILD-6 up in DELIVER's answers only, and they are Gate 4's questions, so the line could never read met. The human `pmos status` view never showed it at all: it printed no checklist lines. The report now reads each cited question from the bank that owns it, marks each line that cites another bank's questions with `carried`, naming those banks, and lists the lines no question stands behind under `unknown_gate_lines`. This changes what the report says and nothing about what can be approved: no gate was ever refused or granted on this line, before or after.
- `docs/ARCHITECTURE.md` said "twenty-two named gates" and "Its twenty-two gates" while `tools/ci_gate.py` defined 25, and no check read either. Both now say twenty-six. The sentence listing the suite's gates now names all twenty-six, adding the journey-record, journey-chain and "What checks this" freshness gates it had left out and the new back-pointer gate. Its "Four gates sit beside `lint.py`" now says "Four checks", because on a line naming `tools/ci_gate.py` the count reader would take it for the suite's count.
- `tools/review_gate.py --record` no longer accepts evidence it cannot reproduce. Before this, an evidence item was a command and a result typed side by side, and nothing ran the command or compared the two, so a record claiming `26/26 passed` on a tree that was not 26/26 was accepted. Now the command must be, exactly, a gate's argv from `tools/ci_gate.py` or an entry of the new `EVIDENCE_COMMANDS` beside it (today the full sweep and the sweep narrowed to one gate with `--gate <id>`), and anything else is refused before it runs. It is run without a shell, in the gate's directory and environment, and refused unless it exits with the declared code (0 unless the item says `exit=N`) and prints the recorded result. An allowlist replaced a denylist of shells and command runners because every round of review found an unlisted runner (`find -exec`, a git `!` alias) that put a result beside a real tool which the tool never printed. The plain gate that `ci_gate.py` runs checks a record against itself and re-runs nothing, so it cannot tell a hand-written record whose results and outputs agree from one `--record` wrote; `python3.11 tools/review_gate.py --reexecute` re-runs every recorded command against the tree as it is now, and is opt-in because a recorded sweep takes minutes. [docs/readiness/EXT-TEAM-review-brief.md](docs/readiness/EXT-TEAM-review-brief.md#what-this-guard-cannot-do) states what the guard still cannot do: the reviewer's identity is an unauthenticated claim, the self-attestation refusal cannot match a model's name, and the interpreter and machine that run the tool are trusted.
- [examples/README.md](examples/README.md) stated three of its four journey counts wrong, and the wrong ones summed to the wrong total, so the arithmetic agreed with itself: forty-six for Ledgerline, forty for Sahulat and fifty-one for Harbourgate, one hundred and fifty-one in all, where the tree holds 58, 44, 54 and, with the expense copilot's 14, 170. It also said twenty-three standalone examples where its own table lists 16. Every count is now a digit, and `tools/docs_contract.py` holds the file to the tree rather than to itself: each journey's figure to its family's files in `examples/` and to that family's table rows, the total to their sum, the standalone and industry counts to their sections' rows, the number of journeys to the journey files present, and a row linking a file that does not exist is reported. A family is any `examples/<family>-journey.md`, and its artifacts are its other files less its two supplementary sheets, a rule read from the tree rather than a list kept beside the check, because a list of files to leave out can be edited until it reproduces whatever the index already says. Deleting the count sentence fails the check instead of passing it vacuously. A figure written in words is not read. The opening paragraph is split into a lead, a summary table and one section per group; the sentence that called the journeys' artifacts "cross-checked against each other and against their data sheet" became the artifact map's actual brief, which data-sheet rows an artifact may not contradict, followed by the artifacts that do not meet it, because nothing in this repository performs that cross-check.

### Fixed, the DEFINE interview and the two journey records

- **The DEFINE bank asks for the vision, the strategy and the roadmap.** Commit 85b0ec5 put three lines at the head of Gate 2's checklist in [os/STAGE-GATES.md](os/STAGE-GATES.md), one per planning document with its approvers, and appended "and to a roadmap phase outcome" to the line on PRD objectives. It changed nothing the Conductor reads: no DEFINE question asked for any of the three documents, `pmos status` did not list them among the documents Gate 2 expects, and the Gate 2 rendering table had eight rows for eleven lines. DEFINE-10, DEFINE-11 and DEFINE-12 now ask for them. They are appended after DEFINE-9 because a bank's IDs are never renumbered; they are three entries rather than one because each document has its own template and its own approvers; and each accepts a one-pager that carries it in a few lines, which Gate 2 allows at that weight. The Gate 2 rendering now has eleven rows in document order, the three new ones first. The appended clause is not repaired: row 4 still reads "Every objective traces to Gate 1; every requirement traces to a PRD item", and no DEFINE question asks whether an objective traces to a roadmap phase outcome. That is left for its own change.
- **`tools/question_banks.py` refuses a bank whose gate rendering table has more or fewer rows than its gate has checklist lines.** A checklist line is any box `lint.py` counts as one, `- [ ]` or `* [ ]`, ticked or not, indented or not. The check counts and does not read, because every row paraphrases its line on purpose: it catches a line added to a gate with no row added to the bank, which is what 85b0ec5 did, and it cannot catch a row paired with the wrong line or a row that drops part of its line. For this change the other five gates were read line by line against their rows. No row sits against the wrong line, but several drop a clause of theirs, among them Gate 3's dependency row (the needed-by dates), Gate 4's failure-scenario row (the data-loss check) and its AI overlay row (the escalation of a failed threshold), and Gate 5's UAT row (the real users or named proxies); like Gate 2's row 4, they are left for their own change. The check lives in the compiler because a missing row is invisible at run time: `pmos status` reports a gate's lines from these rows, so it never names a line that has none, and `pmos gate` records an approval without reading them, before and after this change.
- **Repinning.** The define bank's version moves from c5c480a5005f2332f to c81ac4afedd80cc9e, and no other bank's version moves. `pmos status` tells a product pinned to the old contract that the shipped one differs. A product that has not yet approved Gate 2 adopts it with `pmos repin`, keeps every answer, and is asked DEFINE-10 to DEFINE-12 before Gate 2 can be proved. That now includes a product holding a question it parked and then reopened, in the bank still in progress, which `pmos repin` used to strand: reopening deletes the parked answer and leaves the question behind its bank's cursor, and repin set every bank's cursor to its first question with no stored answer, which put the reopened question in front of it. Repin returned 0, the Conductor refused the product from then on ("conductor reopened questions are invalid"), and a second repin found nothing to do; this was reproduced on products the unpatched runtime made, with DEFINE-2 and with DISCOVER-2 reopened. The cursor now passes over a reopened question as it does an answered one, so the question stays reopened and is asked next; the tests reopen a question in each of those two banks and repin, and in DEFINE answer on to prove Gate 2. A product that has already approved Gate 2 cannot adopt the contract: `pmos repin` used to commit that too, and the Conductor then refused to open the product at all ("gated bank is not complete"). It is now refused before anything is written, dry run included. More generally, `pmos repin` now runs the Conductor's own validation of a stored state on the state it would write, and refuses the contract when that validation fails, so it no longer commits a state the Conductor would then refuse to open. That also refuses a contract that removes a question the product has answered, which repin used to commit, and one that puts a new question in front of answered ones. Without `--dry-run` the check runs twice, on the state repin reads first and again inside the write on the state that write replaces, so an approval another process records in between is refused as well. `pmos status` makes the same check before it advises repin, and for a product repin would refuse it names the reason instead. [docs/RUNTIME-QUICKSTART.md](docs/RUNTIME-QUICKSTART.md) says all of this, and no longer says that a reworded question is asked again, since its stored answer is kept and counts, or that moving a product to a newer contract is unsupported.
- **The chain record cites documents instead of positions.** `tools/journey_chain.py` answered every question with the next artifact in a list, one fixed sentence and one fixed person and date, so which document an answer cited depended on where a counter stood. It now answers each question from the first document its lands_in names that the workspace holds, with an answer written from a named section of that document and a `quote` that must appear in that section; pmos then checks the quote against the whole file, as it checks any quote. The run stops when a quote is not in its section, when an answer is a verbatim slice of its document, or when the document does not carry what the answer's evidence class claims. An interview claim needs its person and date named together on one line of the document. A named commitment needs its quote to hold a clause that names the person and says approved, agreed, acknowledged, committed or signed, where a clause ends at every `|`, every `;` and every full stop followed by whitespace, and the word counts as negated when any earlier word of its clause is not, never or no, in any case, or ends in n't with a straight or curly apostrophe. No other word is read as a negation, so cannot, without or refused before the assent word leave it standing. Both checks read words, not meaning. DEFINE-6, DESIGN-2 and DESIGN-5 ask for a named commitment, and no clause of the sections they cite records a yes from anyone those sections name, so each is submitted as artifact evidence, which pmos accepts as the stronger class, and its answer says what the document does not record. Seven of the 29 questions name no document the expense copilot chain ever wrote; each cites a named nearest document, its row says so, and the tests name the seven, so no other question can fall back without failing one. The ceiling is seven, where the plan for this change said two. DISCOVER-8's lands_in names only the STATE.md position block, which no document can satisfy, so it falls back whatever is written; each of the other six lands in a document no expense copilot example fills, an assumptions register, a UI state inventory, an integrations document, an observability plan, the AI overlay's agent architecture or guardrails, and a design review record. Reaching two would take five of those written as new expense copilot documents, invented for the purpose, and writing invented expense copilot documents was dropped from this round deliberately, as a task of its own, because nothing in CI can check that an invented document agrees with the fourteen already committed. An example is stamped as the file it declares in its first eight lines, in the phrasing `tools/phase_index.py` reads, under templates/ or frameworks/, rather than as the first template path anywhere in its text; one declaring nothing, one declaring a file that does not exist, and two landing on one workspace path each stop the run.
- **Both records say what was checked.** [examples/journey-chain.md](examples/journey-chain.md) replaces its one evidence column, "Evidence citing a workspace file", with the three labels pmos stores, one column each, read from each gate's row of the handoff package, and a column for the generator's own check that each quote sits in the section its answer names, which pmos does not read. Every chain answer quotes its document, pmos records all 29 as quote_verified, and the record says beside the table what that label does and does not establish. The section column equals the answered column in every record the generator writes, since a run with a failing quote stops before writing, and the record says so. It adds a table of every question with the evidence class it was submitted under, the file, the section and the first words of its answer, and its handoff line gives the package's three figures. [examples/journey-run.md](examples/journey-run.md) gains the same three label columns and a column for the artifacts each approval bound, read from the runtime's status: its answers cite an interview id, so all 57 are supplied_unverified, and its workspace holds no artifact, so no approval binds one; its Result line says so and points to the chain record. Tests run each generator on evidence and a workspace the committed records do not carry, and fail if either record writes those columns, the chain's handoff line or the run's Result line without reading them from the runtime. os/STAGE-GATES.md cited the run record for artifact-revision binding, which that record cannot show, and now cites the chain record for it.
- **`pmos handoff` reports the evidence behind each gate.** Each Gate 1 to 3 row of the package's `approvals` now carries its own bank's `evidence`, the same three labels as the package total above, counted by the same function `pmos status` uses, and `pmos handoff --json` prints them as `evidence_by_gate`. `handoff/CONTEXT.md` lists them under Evidence, one line per gate below the package's totals, and adds a line after Development-ready giving how many accepted answers cite a file pmos found inside the workspace, the quote_verified and source_verified ones together, out of all of them. The package total counts every bank, so an answer to a bank after Gate 3 counts there and on no gate's line. `development_ready` reads none of these figures. The quickstart's `pmos handoff --json` sample, which a test compares with the real output, and its description of each phase's `completed` block now carry all three labels.
- The journey counts move with the bank: 57 questions across the six banks, was 54, and 29 in Gates 1 to 3, was 26, in README.md, examples/README.md and the tests, and docs/ARCHITECTURE.md counts twelve DEFINE questions, eight of them core. The examples index also says the chain's answers cite the Ledgerline journey sheet as well as the expense copilot documents, since DISCOVER-8 falls back to it. The 0.8.0 entries below keep 54 and 26, which is what 0.8.0 shipped.

## 0.8.0, 2026-09-21

This release adds executable local engineering capability: a dependency-free `pmos` runtime, the stage-gate loop it drives, and the checks that keep the documents honest. It is a source tag and a pure-Python wheel built from that tag. It is not a provider certification, not a release attestation, and not evidence that anyone outside this repository has adopted or reviewed it: those requirements stay open in [docs/readiness/external-gates.json](docs/readiness/external-gates.json), and [docs/readiness/EXT-RELEASE-checklist.md](docs/readiness/EXT-RELEASE-checklist.md) records which of them this release carries evidence for and which it does not.

### Added

- [docs/readiness/EXT-RELEASE-checklist.md](docs/readiness/EXT-RELEASE-checklist.md), the release evidence checklist. EXT-CI's evidence exists already and is recorded there: the hosted run on the exact main commit, with all three matrix jobs successful. Of EXT-RELEASE's four items, the artifact digest and the provenance manifest can be produced by anyone and the commands are given, the wheel builds byte-identically twice from the same commit, the tag needs the owner's authorization, and there is no rollback artifact because nothing has been published yet, which the checklist says rather than leaving blank. Neither gate is marked verified: `tools/readiness.py` reports every external gate as unverified by construction.
- `pmos repin`, so a product started on older questions can adopt the shipped question bank contract. It was not possible before: a product keeps the banks it started with, which is what stops a repository update stranding it mid-interview, and which also left it on those questions for good. The command keeps every stored answer, moves each bank's recorded definition with the pin so the Conductor still opens the product, and recomputes each changed bank's cursor so questions that are new or reworded get asked again. It does not touch gates: an approval now records the fingerprint of the questions its bank asked, so a bank whose questions changed reports its gate stale on the next turn, by the same path a changed proof source takes. `--dry-run` reports what would change and writes nothing, and `pmos status` now names the command instead of saying the move is not supported.
- `pmos status` now opens, in human output only, with where the product stands, the exact next command, the document to open next and the other documents that gate expects, then one aligned line per gate. The payload already carried all of it; the `phases` list was printed as a single line of JSON that nobody could read, and it is now left out of the human view. The `--json` payload is unchanged, phases included, because it is a machine contract.
- `tools/journey_chain.py` and [examples/journey-chain.md](examples/journey-chain.md): the runtime driven from the committed expense copilot documents rather than from invented answers. The tool copies those fourteen artifacts and two data sheets into a product workspace, repoints their links, stamps each artifact, then answers all 26 questions of Gates 1, 2 and 3 with evidence citing the workspace file it came from, proves each gate, and records that the handoff reports development-ready with all nine sections linked. It then edits one cited document and records the handoff refusing, with Gates 1 and 2 stale. A `journey-chain` release gate rebuilds and compares the record, so the chain cannot rot. `tools/journey_record.py` still covers the other half: all six gates, answered generically.
- `tools/journey_record.py` and [examples/journey-run.md](examples/journey-run.md): the `pmos` command line taking a fictional product through all six question banks and gates (54 answers, six gate proofs), then a gate going stale when its proof file changes and being proved again. The record is generated, not written, and a new `journey-record` gate in `tools/ci_gate.py` regenerates and compares it, so a change that makes the record disagree with the runtime fails CI.
- `tools/what_checks.py` and a `What checks this` note in every prose skill and every template. In a skill it is the last section: which rules CI checks, which gate the skill is declared against and what the runtime refuses when that gate is proved, and which judgments rest with the people who sign it. In a template it is one paragraph under the header: a filled copy stamped with the artifact block is bound to its gate, and editing it after approval makes the approval stale. Both are generated from each file's declared gate, the conductor's question banks and the sign-off tables in `os/STAGE-GATES.md`, and a `what-checks-freshness` gate fails CI when they fall out of date.
- A dependency-free `pmos` package and CLI for deterministic local onboarding, SQLite-backed transactional snapshots, compare-and-swap commits, backup/restore, a leased at-least-once queue, scoped OS and task memory, migration/rollback, offline provenance, and verification.
- A policy-first domain model for product lifecycle, traceability, approvals that invalidate on evidence change, RBAC, collaboration, portfolio capacity/dependencies, and tamper-evident local audit export.
- A deterministic Conductor, runtime hooks, typed skill contracts, model routing with safe provenance, and adapter/outbox contracts for issue tracking, source control, analytics, research storage, and notifications.
- An optional OpenRouter adapter that discovers models at runtime, identifies free models from current pricing metadata, bounds requests/responses, and reads an environment-only credential at call time.
- Local regression, crash, migration, security, accessibility, use-case, provenance, and evaluator-integrity gates.
- A repository-local, standard-library PEP 517 backend that builds the wheel in an isolated offline environment without an undeclared setuptools installation.
- Six enterprise domain cards in `knowledge/domains/`: ERP and enterprise finance, HR technology, marketplaces, marketing and advertising technology, cybersecurity and GRC, and developer tools and APIs. They took the layer from ten cards to sixteen, before the twenty-eight sector cards below took it to forty-four, and `README.md` went on saying ten until this change set corrected it.
- The two documents the PM working set was missing: `templates/definition/user-stories.md` and `templates/execution/backlog.md`.
- Three measurement tools with a written bar behind each: `tools/pm_working_set.py` and `tools/template_rubric.py` score the templates, and `tools/skill_rubric.py` scores every prose skill against the contract the skills already use, writing `docs/readiness/skill-rubric.json`.
- `tools/ext_ai_probe.py`, an opt-in probe that drives the OpenRouter adapter for the EXT-AI evidence gate, plus the two things external evidence needs from a person: `docs/readiness/EXT-TEAM-review-brief.md` and `docs/readiness/EXT-USER-session-script.md`.
- A Claude Code hook layer, `.claude/settings.json` and `.claude/hooks/pmos_hook.py`, registered on seven session and tool events. It applies the `pmos/hooks.py` write and approval policy and runs the compile and document-tree gates when a session stops. It is the only part of this tree that runs without being invoked, which is why `SECURITY.md` now carries a section for it, and deleting `.claude/` removes it.

### Changed, repository layout

- The nineteen root unit-test modules moved from the repository root into `tests/`. `tools/ci_gate.py`, the readiness verifiers and `tools/readiness_probe.py` put `tests/` on the import path, so every test id the readiness registry pins is unchanged (`test_lint.OsTreeGateTests.<name>`); the task ledger's evidence paths, `lint.py`'s rule-bearing set, the CI workflow's two direct test steps and the documents that name a test file follow the move. No document a user fills moved. Run one suite from the root with `python3 -m unittest tests/test_lint.py -v`.

### Fixed, design layer

- `knowledge/design/visual-foundations.md`'s reflow row now states WCAG 1.4.10 as written: vertically scrolling content at 320 CSS px wide, horizontally scrolling content at 256 CSS px tall, and an exception only for content that needs a two-dimensional layout. `frameworks/design/ux-scorecard.md` names the source of its post-task ease item and no longer says its quotation allowance is spent. Both came from Codex's CI-6 review of 2026-09-12.

### Changed, role ladder

- The eight rungs in `knowledge/roles/ladder.md` and the seven specializations in
  `knowledge/roles/specializations.md` now link the artifacts each role produces and consumes to
  the template each one lands in, and name the recurring workflows that drive them: two skills per
  rung, three or four skills or framework sheets per shape, each with the trigger or cadence it
  runs on. Before this the ladder's document lines were prose with an occasional link, and two of
  the eight rungs, Group PM and CPO, linked nothing at all: a reader who wanted the group's OKRs
  or the investment thesis that closes a product line was told the document existed and not where.
  The specializations' single `Documents` line splits into `Documents out`, `Documents in`, and
  `Recurring workflows`, the ladder's three-line shape. Only the document lines moved; `Owns`,
  `Decides`, `Success`, `Failure`, and `Stage variance` are untouched on every card.
- Every role's list is distinct from its neighbours by construction. Each artifact sentence on a
  specialization says which neighbouring shape does not produce it and why: a Product Owner starts
  from the PRD and never writes the discovery document, a Platform PM's integration register faces
  inward where a Technical PM's faces the counterparties it sells to. On the ladder no two adjacent
  rungs share more than two links, and the two they share sit at the top, where Director, VP, and
  CPO each produce a product strategy and a board or quarterly update because that is the work at
  those altitudes; the workflows behind each are different.
- These are cards, not journeys. No rung and no specialization has a worked example yet; the
  journeys land separately.

### Added, sector cards

- Twenty-eight domain cards, taking the sector layer from sixteen cards to forty-four. Fourteen are
  financial services, which the layer had covered with a single pointer card: core banking,
  transaction banking, remittances, payments acquiring, card issuing, lending and credit, embedded
  finance and banking-as-a-service, wealth and investing, capital markets, insurance, crypto and
  digital assets, RegTech with AML and KYC, mobile money and wallets, and Islamic finance. Fourteen
  are general sectors the layer lacked, including the four the release contract named as the
  twenty-domain target and ten more: hardware and IoT, telecom, public sector and govtech,
  automotive and mobility, energy and utilities, manufacturing and industrial, agritech, PropTech
  and real estate, travel and hospitality, media and publishing, LegalTech, pharma and life
  sciences, retail in store, and food delivery and quick commerce. Every card carries the layer's
  five parts unchanged: the questions, the gatekeepers, the metrics with how each one lies, the
  reading, and the Conductor and template overlays.
- The index splits into a general table and a financial-services table, because the money
  sectors share one fact the others do not: the licence is held by someone with a veto and every
  rail was built by a third party with its own rulebook. The fintech card stays a pointer and now
  routes to the fourteen sector cards as well as to the regulated module.
- Written under the no-fabrication rule as it applies to a card: no statistic, market size, fine
  amount, article number or case name that the author could not vouch for. Where a specific was
  uncertain the sentence carries a parenthetical that begins with "verify", the tree's marker in
  the wording each card needed, or omits the specific; 49 such parentheticals sit across the
  twenty-eight cards, listed in the pull request. Each card names at least one non-US regime, because the maintainer's market is not
  the United States and a card that assumes it is teaches the wrong gatekeepers. These are cards,
  not journeys: the graduation rule in the index still holds, and no sector has a worked
  end-to-end example yet.
- Drafted by four Sonnet workers in one isolated worktree, seven cards each, against the exemplar
  cards and a written contract. The lead scanned every card for unmarked specifics and found none;
  the independent reviewer then read the content and found six confidently stated errors the
  scan could not see: a bank described as a fiduciary custodian of deposits, Pakistan's clearing
  company named as its depository, a FATF grey listing said to impose enhanced due diligence,
  the EU Radio Equipment Directive said always to need a notified body, Solvency II grouped with
  rate-filing regimes, and the platform-work directive described from its superseded proposal;
  plus two omissions, the causation requirement in Inclusive Communities and the reversal of
  the Tornado Cash designation. Each was checked against primary sources through a web-grounded
  search before the sentence was rewritten. A second pass found the superseded platform-work
  wording surviving in that card's reading list and the causation point missing from the
  PropTech questions, and named four unmarked claims it could not vouch for; all were checked
  the same way and reworded. The lesson is recorded because a scan for numbers
  catches invented figures and cannot catch a confident wrong sentence; only a reader can.

### Added, three worked journeys

- Three journeys in `examples/`, 46 files: three journey files, each holding the story, one data
  sheet and an artifact map, plus the 43 filled artifacts those maps index. Ledgerline has 13
  artifacts, pricing and selling the expense copilot from positioning through a killed pricing
  experiment to the post-pivot growth plan, PLANNING through OPERATE. Sahulat has 14, a fictional
  mobile-money wallet's bill-pay feature taken by one product manager from DISCOVER to a Gate 6
  PIVOT. Harbourgate has 16, completing `examples/checkout-modernization-brownfield.md` from Gate 4
  through Gate 6 PERSIST and the retirement of the legacy payment layer. The 43 artifacts fill 43
  different templates; each keeps its template's H2 structure, walks its exit gate at the bottom,
  and takes every number and id from its journey's data sheet.
- Every artifact was reviewed on its own, in batches, and each journey then had a cross-artifact
  pass that corrected figures one artifact carried differently from another or from the data
  sheet. One example: Ledgerline's add-on MRR at 2026-12-18 now reads $15,906 on the data sheet,
  the OKR sheet, the growth plan, the dashboard spec and the metrics review, where the OKR sheet and
  the growth plan had carried $15,900 and the growth plan had set it as the baseline for the next
  cycle's target. The last consistency pass on each journey was not recorded clean after those
  fixes, so where two artifacts still disagree the data sheet is the authority.
- `examples/README.md` indexes the three journeys and all 43 artifacts in its own table style, one
  table per journey. The Sahulat and Harbourgate artifact maps name each file as a relative link
  where they had named it as plain text, so the lint gate now resolves all 30 of those entries.

### Added, model compatibility matrix

- `docs/COMPATIBILITY.md` and `tools/model_matrix.py`. The document keeps three matrices apart,
  model, host and workflow, because each fails on its own, and defines its words: tested means a
  command here produced the result and a record under `docs/readiness/` holds it; untested is an
  absence, not a yes. Every model cell is graded by a predicate over the response text, never by
  another model.
- The model matrix is rendered from the recorded 2026-09-09 free-tier run, kept as recorded
  rather than re-run: 17 models, 136 calls, 72 graded and 64 with no answer, each no-answer
  cell classed from the gateway's own error text. The record came from a dirty working tree and
  the table says so. No paid call was made, so every frontier model is untested.
- `tools/model_matrix.py --check` now refuses a record whose prompt, tier or description changed
  under it, a halted record, and an answered call with no usable cost; a stale table outside the
  repository is reported as a finding instead of crashing on `relative_to`. `--render` no longer
  writes em dashes into the document.
- `--budget-usd` is a running total. It used to compare each call's own cost with the ceiling
  after every call had already been made, took an answer with no cost as free, and dropped a
  charge reported on an error response. Dispatch now stops once the total passes the ceiling or
  an answered call carries no usable cost, charges on error responses count, and a NaN, infinite
  or negative ceiling is refused. The ceiling is still checked as each call returns, so calls
  already in flight, up to one fewer than the worker count, can finish over it; that is an owner
  decision to take before any paid run.
- Readiness criterion CI-1 ("every shipped root, harness, and regulated test runs") kept its own
  list of root modules and never ran `test_pmos_probe`, `test_pmos_matrix` or
  `test_pmos_invariants`, so it counted 371 root tests while the release gate ran 516. The
  matrix branch and the tools lane below fixed this two ways, and the merge keeps both: the
  full-suite probe runs the root-tests gate's own argv, keeps a floor of named modules, and now
  fails when any `test_*.py` on disk is missing from that argv, with a regression test for the
  case neither fix covered alone.

### Fixed, audit port

The findings of the 2026-09-05 audit at `9400d0b` that still reproduced on `df0601c`, ported in
ten lanes and each lane accepted by an independent verifier before it merged. Finding ids are the
audit's own.

- **Conductor, the one P0.** `conductor-park-is-a-permanent-deadlock`: a question challenged
  twice parked and froze its whole bank, so every later answer, valid evidence included, was
  refused. A parked answer is now filed as offered and marked parked, the cursor advances, and
  only the bank's gate proof is refused while anything in it is parked. No command unparks yet,
  so a bank whose parked question is its last still stops at its gate
  (`conductor-park-no-exit-route`, open for an owner ruling). Also
  `conductor-challenge-docstring-is-wrong`.
- **Store and domain.** `lease-next-cancels-a-live-lease` (P1): a cancel request on a live lease
  is kept instead of being reaped by the next poll. `store-heartbeat-deadline-branch-unreachable`
  (P1): a heartbeat past its deadline reports the deadline and dead-letters.
  `queue-verify-loads-every-blob-body`: queue admission checks hashes without reading payloads.
  `score-initiative-ignores-period` (P1): a score is written to the allocation row of the period
  it names. `store-read-snapshot-revision-pin-untested` and
  `store-promote-to-os-cas-guard-untested` now have tests.
- **Outbox, hooks, release and routing.** `outbox-retries-an-already-delivered-event`: a send
  that completed with an unusable external id, including a sender returning `None` or an empty
  string, is dead-lettered instead of being retried, and a sender that itself raises
  `DataValidationError` is recorded under that name rather than as `invalid_external_id`.
  `hook-protected-paths-case-sensitive`: the write boundary compares case-folded paths, so a
  case variant of a protected destination is denied. `hooks-allow-reading-credential-files`:
  private key blocks are blocked like other secrets. `hookbus-emit-sorts-callables`: registering a second
  hook with the same priority and name for one event raises `ValueError`, and hooks of equal
  priority run in name order.
  `build-provenance-leaks-output-dir-fd`, `provenance-default-exclusion-breaks-verify` and
  `release-dead-digest-helpers`: a failed build closes its output descriptor and removes its
  temporary provenance file, the output path is excluded only when the call writes it so a
  manifest built without output records an existing provenance file and verifies, and three
  uncalled digest helpers are gone while the live stat-to-open guard gains a test. `routing-aggregate-budget-postcheck-unreachable`: the guard stays
  and a passing call now pins it. `hooks-wrapper-tests-cannot-fail` and
  `hooks-git-clean-deny-branch-untested` are test-only.
- **Lint and the security gates.** `secret-gate-exempts-regulated-module` and
  `lint-secret-gate-skips-regulated`: the secret gate now reads `modules/regulated/` too, reading
  only, so the pins hold. The masked-text finding, `masked-text-invisible-to-banned-...`, whose
  full id carries the very deferred marker the placeholder gate rejects: the banned-metric,
  placeholder and link gates read HTML comments, so a banned figure, a deferred marker or a dead
  link inside a guidance comment now fails where it used to pass; the link gate still skips
  fenced code.
  `workspace-containment-boundary-depends-on-cwd`: workspace mode takes its boundary from the
  repository, not the directory you run it from. `approved-status-regex-too-narrow`:
  `**Status**: Approved` and case variants are read as an approval claim.
  `system-path-gate-misses-half-the-tree`: the path gate reaches every top-level directory.
  `security-gate-skips-every-test-file`, `security-gate-misses-shell-primitives` and
  `security-gate-five-of-six-credential-detectors-untested`: test files are scanned and shell and
  process-replacement primitives rejected. `docs-contract-boundary-error-names-the-wrong-file`,
  `check-manifest-model-id-regex-misses-listed-vendors` (non-numeric ids such as `deepseek-chat`,
  `qwen-max` and `grok-beta` now fail the manifest check) and
  `workspace-contract-cannot-detect-the-drift-it-names`.
- **Harness.** `runner-follows-redirect-with-bearer-key` (P1): the runner refuses a gateway
  redirect, so the key is never carried to a second host, and a redirecting gateway queues the
  run. `runner-unbounded-sse-buffer` (P1) and its newline bypass: the stream read itself is
  bounded. `write-stories-routed-to-wrong-gate`: story writing routes to DEFINE and Gate 2.
  `fallback-route-forbids-its-own-job` and `report-routes-contradict-their-own-templates-heading`:
  the catch-all route has a kind and a gate note, and generated commands title templates by what
  a route does with them; `gate-note-exemption-unenforced` makes the gate note's shape a checked
  field. `three-versions-for-one-repo` (documented in the manifest) and
  `runner-call-cli-has-no-test`.
- **Tools and packaging.** `license-never-reaches-distribution`: the wheel declares its licence.
  `backend-missing-build-sdist`: `build_sdist` refuses by name, in a way a frontend can report.
  `gitignore-covers-wrong-build-artifacts`. `ci-gate-not-actually-canonical` and
  `root-tests-gate-is-a-hardcoded-module-allowlist`: `tools/ci_gate.py` now holds 21 gates,
  adding `regulated-template` and `skill-rubric-freshness`, and every lint the workflow runs over
  a shipped file is also a gate. `skill-rubric-json-is-a-stale-measurement`,
  `stale-tracked-skill-rubric` and `skill-rubric-docstring-states-a-closed-gap-as-open`: the
  committed rubric is regenerated and a gate fails when it goes stale.
  `readiness-documentation-claims-match-verifies-no-claims` (UX-3 is retitled for what it
  verifies), `products-readme-cannot-ship` and `pm-working-set-docstring-ninety-eight`.
- **Root documents.** `readme-harness-deletion-every-gate-passes`,
  `changelog-omits-nine-commits-of-feature-work`, `ten-market-cards-is-now-sixteen`,
  `method-numbering-four-versus-five`, `agents-md-names-insufficient-gate`,
  `security-nothing-runs-vs-committed-claude-hook` and
  `security-whole-attack-surface-omits-tools`.
- **Reference documents.** `architecture-complete-file-tree-omits-tools`,
  `architecture-complete-file-tree-is-incomplete`, `architecture-fifty-three-templates-name-the-index`,
  `architecture-three-checks-not-in-ci-is-false`, `conductor-design-discover-omits-eighth-question`,
  `faq-four-methods-readme-has-five` and `comparison-one-network-component`.
  `runtime-quickstart-rejection-leaves-state-intact` (P1): the quickstart no longer says a
  rejection leaves state intact. It names the rejections that advance the revision and the ones
  that do not, where to read the next token, and, corrected at integration for the conductor fix
  above, that a park files the answer and moves on while the bank's gate stays shut.
- **Operating layer, skills and study paths.** `boot-prompt-inventory-omits-eight-files`: the path
  gate now also fails a tracked file in a boot-prompt manifest directory that the manifest does
  not name. `products-workspace-gitignore-contradiction`, `tutor-miscites-knowledge-card`,
  `stage-hub-notes-omit-the-two-new-templates`, `user-stories-and-backlog-in-no-stage-map`,
  `launch-readiness-item-8-drops-gate-5-condition`, `domain-cards-cite-wrong-conductor-question-ids`,
  `fintech-card-states-broad-regulated-activation`,
  `reg-gap-check-points-at-superseded-activation-rule`,
  `conductor-protocol-cites-nonexistent-question-id`,
  `validation-agent-worked-run-invents-a-gate-5-line`,
  `estimator-worked-run-rollup-does-not-reconcile`, `drafting-agent-draft-status-count-wrong` and
  `team-intra-stage-order-contradicts-architect`.
- **Templates, frameworks and examples.** `template-count-98-actual-100`,
  `ninety-eight-templates-is-now-one-hundred` and `template-catalog-counts-stale`: every count of
  the templates now says 100, and `tools/docs_contract.py` counts the templates the catalog and the
  front door claim, so the next stale total fails a gate. `invest-verdict-field-missing`,
  `backlog-six-numbers-are-five`, `business-case-sensitivity-split-unreproducible`,
  `exec-update-example-fails-own-gate`, `growth-plan-kill-lever-not-in-loop`,
  `leverage-points-altitude-11-not-12`, `team-topologies-wrong-marker-named`,
  `packaging-prices-contradict-gabor-granger`, `rice-example-capacity-contradiction` and
  `north-star-example-conflates-checks`.
- **Carry-overs and coverage.** `twelve-gate-tools-at-zero-coverage`: the graph, frontmatter,
  CI-gate verdict, CI wiring, manifest and workspace-contract gate tools now have tests of their
  own. `inventory-per-section-count-unpinned`, `readiness-category-exit-code-untested`,
  `ux3-title-omits-inventory` and `manifest-tier-note-true-only-after-port-c`.
- At integration, `tools/readiness_registry.py` names the lanes' new tests under the readiness
  steps they prove: the hook, routing, operations, security, release and evaluator lists grow,
  and the os-tree, manifest-contract, workspace-contract, harness-route-behavior,
  packaging-release, secret-boundaries and ci-runtime steps each run the tests behind their gate.
  `system/BOOT-PROMPT.md` names the journey files and `docs/COMPATIBILITY.md`, which the new
  manifest check reported once the branches met.
- Still open after the port: `conductor-park-no-exit-route` (above) and
  `deliver-templates-filed-under-build-map`, where `templates/delivery/testing-strategy.md` and
  `failure-scenarios.md` still declare DELIVER and Gate 5 although Gate 4 lists them as inputs.

### Changed

- Documentation now separates the document path, the optional local runtime, and external readiness. Historical claims below describe the state at the time of those entries; where they characterize the legacy harness rather than the `pmos` runtime, they are superseded by this section and the current operator documentation.
- SQLite backup and restore now retain no-follow directory and database descriptors across connection and copy boundaries, rejecting path replacement before accepting data.
- Release and review inventories compare symlink target bytes as well as file identity, so immediate inode reuse cannot hide a replaced link on Linux.
- The reviewed tree digest no longer depends on the filesystem or the checkout shape it is computed from. macOS AppleDouble sidecars (`._name`), which appear beside every entry when the repository lives on exFAT, FAT, or SMB, are excluded the same way `.DS_Store` already was; and `.git` is excluded whether it is the directory a clone carries or the `gitdir:` pointer file `git worktree add` writes. Both were hashed before, so the same commit produced a different digest on an external drive (1075 entries against 491) and a different digest again in every task worktree, which meant a review recorded the way CONTRIBUTING asks for could never match the digest CI computes and CI-6 could not be closed honestly. Corrected 2026-09-08: that entry originally ended by claiming neither exclusion narrowed what a reviewer reads, because git could not track either file. The claim was wrong for the `._` rule. `git add -f` overrides .gitignore, so a tracked `._policy.json` was force-added, left out of the reviewed inventory, and its contents flipped from `{"approved": false}` to `{"approved": true}` without moving the digest. An independent review reproduced it. The exclusion is now tracked-aware: git decides what is reviewable, a metadata-shaped name only excuses a file that git is not carrying, and an unreadable index fails closed instead of being read as an empty tracked set. The same treatment now covers `.DS_Store` and `.pyc`/`.pyo`, which shared the defect. The `.git` half of the original claim stands: the repository's own control path is not reviewable content in either form.
- Every prose skill carries the full contract. All twenty-eight score seven of seven sections under `tools/skill_rubric.py`; ten were short of it before, most often missing the failure-modes section.
- The PM working set and the eight most-referenced documents outside it were brought to one depth bar: twenty-six templates gained fields, guidance, or exit criteria. Nothing was renamed or moved, so a filled copy still matches the template it came from and still resolves its links. The added sections are sections today's checks expect, which is the case the MINOR note above describes. `tools/template_rubric.py` also states what it must not be applied to.
- `tools/review_gate.py` is closable by the person it exists to be closed by, and the record it writes binds its findings to the exact tree that was read.
- `README.md` says plainly that nothing here is released, and that the newest tag is older than this changelog on purpose.

### Fixed

- The EXT-AI probe reported success while doing none of what it claimed. An external audit
  reproduced six defects offline against `ce81264`; every one still reproduced on `61b2036`,
  so the 0.7.1 claim that they were closed was wrong for this tool. Each is now closed with a
  regression at the CLI boundary in `test_pmos_probe.py`, which the repository previously had
  no coverage for at all. The call cap counted successes, so a failing adapter was re-entered
  once per case -- four dispatches under `--max-calls 1`; it now counts dispatch attempts. The
  probe called `provider.complete(spec, prompt)` where the adapter takes a model-ID string, so
  every real call raised `OpenRouterMalformedResponse`, and it read `.text`, `.prompt_tokens`
  and `.completion_tokens` where the response carries `output`, `input_tokens` and
  `output_tokens`, recording zero characters and null usage for a 22-character answer. A run
  that errored, breached its ceiling, or dispatched nothing returned exit 0; it now returns 1,
  and a run that generated no evidence reports itself incomplete rather than passing. Cost was
  compared only after the fact, so $3.00 was billed against a $0.01 ceiling across four calls;
  spend is now reserved against the advertised price before dispatch and reconciled after, and
  a provider that bills more than it advertised halts the run instead of repeating it. Because
  price is only known once a response arrives, that is the honest bound: the ceiling is
  enforced against advertised pricing, and a discrepancy is caught and stopped, not prevented.
  `--discover-only` still generated through OmniRoute, because the guard sat on a branch
  `main()` never reached when `--via omniroute` was set. A generation with no resolved model
  was recorded as a clean call, though resolved provenance is one of the four things the gate
  requires; it is now an error.
- The skill rubric graded autocomplete. It already computed which skills carried a required
  section that was present and empty, and printed them, but only the section count decided the
  exit code -- so a skill with all seven headings and nothing underneath scored a pass. The
  hollow list now decides the exit code too, on the same thresholds. The 50 shipped prose
  skills still pass unchanged; no threshold was lowered to keep them passing.

### Fixed, review-gate follow-up

- Two more ways tracked content could leave the reviewed tree, found by independent review of
  the fix that closed the first one. `_git()` captured output with `text=True`, and
  universal-newline translation rewrites a bare CR byte to LF -- including inside the
  NUL-delimited stream `git ls-files -z` prints. A tracked filename containing a literal CR
  therefore came back spelled differently from the real on-disk name, the tracked-set lookup
  missed, and the file was excluded. Git output is now read as bytes and path data is decoded
  with `os.fsdecode`, the same filesystem semantics `os.listdir` uses, so the two spellings
  cannot diverge. `rev-parse` text is decoded separately and never with newline translation.
- `tracked_paths()` read every nonzero `rev-parse` exit as "not a repository" and returned an
  empty tracked set, which authorises excluding every metadata-shaped file. Git also exits
  nonzero for dubious ownership, permissions, and a broken config, none of which mean nothing
  is tracked here. Only git's own positive "not a git repository" wording is now trusted;
  every other failure to inspect raises. Recognition is positive by construction, so an
  unrecognised reason -- a permission error, or git answering in another language -- fails
  closed rather than being read as an absence.
### Fixed, continued

- The EXT-AI probe reported success on five more paths, found by independent review of the
  work that closed the first six. A zero-dollar budget disabled enforcement outright, because
  the guard read `if budget`: a free-only run dispatched twice and billed $1.50 with
  `budget_breach` false and exit 0. Zero is a ceiling; it now stops after the first
  unexpected charge, and unbounded spending is an explicit `--unbounded-budget` opt-in that is
  never the default. The gateway path took `--model` on trust, built its spec with `free=True`
  regardless, and recorded cost 0.0, so an out-of-catalog paid model billing $2 was dispatched
  and reported as free; catalog membership is now the eligibility check, free-ness follows the
  discovery constraint, a resolved model other than the pinned one is an error, and a gateway
  that reports a price has that price carried and enforced. Absent authoritative cost was
  coerced to 0.0, turning "the provider told us nothing" into "the provider told us it was
  free"; it is now UNKNOWN and fails the run, alongside rejection of negative, NaN, and
  infinite values. `--max-calls 0` returned success with no dispatch on the gateway path, and
  now reports incomplete on both transports. Reaching the call cap used to abandon the
  remaining cases, so the refusal checks -- which cost nothing and are the evidence the gate
  exists for -- went unevaluated; they are now always evaluated.
- `test_pmos_probe` was not in the canonical root-test list, so none of its regressions ran in
  hosted CI. It is registered, and a regression asserts the registration so the module cannot
  drift out again. `tools/skill_rubric.py` was invoked by no gate at all; it is now a gate.
- `--env` did not reach the adapter, so a custom credential variable selected a key the
  adapter never read. The gateway subprocess had no timeout and could hang a release gate
  indefinitely; it now has a finite one. The budget reservation estimated prompt tokens as
  `len(prompt)//4`, an average rather than a bound, which under-reserves on exactly the inputs
  that tokenize badly; it now reserves against byte length, since a token never covers less
  than one byte.

### Fixed, second review round

- A repository git cannot read is not an absence of a repository. Renaming `.git/objects`,
  `.git/HEAD`, or `.git/refs` away makes `rev-parse` answer with the identical
  `fatal: not a git repository` line a plain directory produces, so matching that wording
  excluded a tracked file from a damaged repository and left its digest unmoved when the file
  was edited. Control metadata on disk now decides: a `.git` entry at the root or any ancestor,
  or `GIT_DIR`, means a repository exists and any inspection failure raises. The wording is
  only corroboration. A missing `.git/config` deliberately is not used as a damage case --
  verified that git exits 0 and carries on with defaults.
- The gateway fabricated a price. `omniroute_chat()` never returns a cost at all, so the
  free-catalog fallback meant every ordinary production response recorded $0.00 on no
  evidence, and the catalog behind it is parsed from CLI strings and a `:free` suffix, which
  is a name rather than billing evidence. Absent cost is UNKNOWN now, an unprovable remaining
  budget stops the run before a second dispatch, and the aggregate says so instead of reading
  as zero. A charge the gateway did report survives a provenance error rather than being
  discarded with the result.
- The direct transport accepted model substitution: a response naming `unapproved/model` was
  recorded as clean, because only emptiness was checked. Resolved identity is now matched
  against the authorized model on both transports.
- `--env` reached generation but not discovery, so a custom credential variable selected a key
  one half of the run never read. Gateway discovery had no timeout even after generation got
  one. Both are bounded now.

### Fixed, shared acceptance matrix

- The probe's behaviour is now stated once as a table and asserted against both transports,
  because every defect closed before this was found on one transport after the other had been
  fixed -- the tell that they were being repaired case by case rather than as a contract.
  Writing the matrix immediately found four more. An empty response body was recorded as a
  successful call on both paths, though an empty body is not evidence a model answered and the
  call may still have been billed. A missing resolved model, and an adapter exception, each
  left the run continuing on the direct path while cost failures halted it. And an exception
  from the gateway transport escaped entirely, aborting the probe and losing the evidence of
  every case already run.
- Gateway discovery trusted output it should not have. A failed `omniroute simulate` -- exit
  nonzero, gateway down -- had its stdout parsed into a catalog, and that catalog is what
  decides which models may be dispatched. Discovery failure is now distinct from an empty
  catalog and refuses the run. A discovery timeout propagated as an unhandled exception rather
  than failing safely, and a missing gateway binary did the same; both are handled. The parser
  also stripped the CLI's truncation ellipsis off elided model ids and kept the fragment, so
  `openrouter/nvidia/nemotron-3.5-lig` could enter the catalog as a real model; the marker is
  evidence the name is incomplete, so such tokens are discarded rather than repaired.
- The discovery and response parsers now have tests that drive the real functions and fake only
  the subprocess beneath them. Every previous test replaced them wholesale, which is why none
  of their failure handling was exercised.

### Added, guards against recurrence

- `test_pmos_invariants.py`, registered in the canonical gate. Three review rounds each found a
  fresh instance of a defect class the previous round had fixed one example of, and a unit
  test that pins an example does nothing for the next instance. Each guard here scans the
  code for the class and names the finding that motivated it: every `subprocess.run` under
  `tools/` carries a timeout; the cost parser is checked over its whole value domain rather
  than a sample, including the bool and numeric-string cases that `float()` would otherwise
  swallow as `$1.00` and `$0.50`; no billed cost is coerced with `or 0.0`; the review gate never
  reads git path output as text; the transport matrix stays two-sided and keeps its reviewed
  rows; and every `test_*.py` at the root is in the list CI actually runs -- which the guard
  proved on itself, failing until its own module was registered.
- An adversarial self-review of the matrix change, run before opening the PR rather than
  after, found and closed three more: `usable_cost` accepted `True` as a cost of $1.00 and
  `"0.5"` as fifty cents; the truncation guard treated a sentence-ending period as an elision
  marker and silently dropped legitimate models; and the probe's own `git()` helper had no
  timeout. Four other unbounded subprocess sites in `readiness.py`, `readiness_probe.py` and
  `security_gate.py` are now bounded.

### Fixed, gateway discovery source

- The gateway path discovered its catalog from `omniroute simulate`, on the theory that the
  router's own dry run was an inventory of what it serves. Reproduced on 2026-09-09 against
  df46608: the dry run prints the weighted fallback table of the `auto` combo whatever model
  is pinned (`simulate -m openrouter/nvidia/nemotron-3-super-120b-a12b:free` printed the same
  two rows as `simulate` with no model at all), so it could neither confirm that a pinned id
  was routable nor notice that the one id it printed, `minimax/minimax-m3:free`, had been
  withdrawn from the free tier by the provider (404, "This model is unavailable for free").
  Twenty-one models were free that day by the provider's own prices; the probe could dispatch
  to none of them and refused every one as "not in the discovered catalog", which was the
  eligibility check working correctly on a source that could not answer it. The second-review
  entry above had already said that a catalog parsed from CLI strings and a `:free` suffix is
  a name rather than billing evidence.
- Discovery on the gateway path now reads the provider's public catalog, `/api/v1/models`,
  through the same `OpenRouterProvider.discover` the direct transport already trusts, so both
  transports agree on what "free" means: prompt and completion price both zero, as stated by
  the party that bills. The request is keyless by construction -- the adapter attaches an
  Authorization header only when one is passed, and a regression asserts that discovery
  neither reads nor sends one -- and it makes no generation. An unreadable catalog (timeout,
  transport error, malformed body) is still reported as discovery failure, distinct from an
  empty catalog, and still refuses dispatch. Membership remains half of the eligibility proof;
  the post-call check that the resolved model is the pinned model remains the other half. The
  parser-boundary tests that drove the retired simulate parser are replaced by tests that
  drive the new function against a faked HTTP boundary, covering the same failure classes
  plus the one the old source could not express: a `:free` name on a priced model is filtered
  by its price.

- The gateway call shelled out to `omniroute chat` and parsed a coloured footer. That path
  could not send the three request headers routing/README.md requires (compression off, no
  cache, no memory), so every "evidence" call was made under whatever the gateway's defaults
  were; it could not see whether the answer was a semantic-cache replay of an earlier prompt;
  and it returned no cost at all, so by the rule that absent cost is UNKNOWN every gateway
  run halted after its first call and no EXT-AI evidence could be produced through the
  transport that exists to keep the credential out of this process. It now calls the
  gateway's loopback HTTP API. The doctrine headers go on every request, and a regression
  asserts each one. A base URL that is not loopback is refused before any call, because the
  evidence says the prompts stayed on this host. The resolved model is read from the body and
  cross-checked against `X-OmniRoute-Model`; a disagreement is an error. A cache hit and a
  compressed prompt are errors, since neither is evidence that this model answered this
  prompt now. Token counts come from `usage`. Cost comes from the provider's own `usage.cost`
  when the gateway forwards it, otherwise from `X-OmniRoute-Response-Cost`, and the evidence
  names which of the two it was, because the gateway's figure is its pricing table applied,
  not the provider's invoice. The same gateway answers with the provider's spelling of the
  model id, `nvidia/...`, for a call pinned as `openrouter/nvidia/...`; the strict comparison
  recorded that as a substitution, and the check now accepts exactly those two spellings and
  nothing else, so a paid twin without the `:free` suffix is still a mismatch.
- `OpenRouterProvider.discover` raised `OpenRouterMalformedResponse` on the first catalog row
  it could not price and returned nothing. OpenRouter publishes five of its own meta-routers
  priced `-1` on both sides, so on the live catalog the adapter rejected 431 models for the
  sake of five that mean "depends on what answers". Such a row is now dropped: it can never
  be selected, never be called free and never enter a budget, which is what an unpriceable
  model deserves, while the priced rows beside it are kept. A body that is not a catalog, or
  a row with no id or a non-mapping price, still raises. Discovery also gained an explicit
  `anonymous=True` mode, permitted for the catalog path only and refused for generation, so
  a caller that holds no provider credential can still learn what the provider prices at
  zero; a regression asserts at the transport that no credential is read or sent, after a
  first version of that test faked the very method that was resolving one.

### Changed, review brief

- `docs/readiness/EXT-TEAM-review-brief.md` carried a commit, a digest, a file count and an
  expected gate count typed in by hand on 2026-09-03. Seven merges later a reviewer following
  it would have checked out `ba286db`, confirmed a digest that described nothing, and expected
  `18/18` from a suite that now has nineteen gates. The brief now tells the reviewer to
  establish the head, the digest and the hosted run for themselves and to write what they saw
  into the record; the expected result is stated as "18/19 with CI-6 the only red", with any
  other red a finding. The known-limits list no longer says the AI layer has never been
  observed against a live model, because on 2026-09-09 it was, through the gateway transport
  at a $0 ceiling; it now says exactly how far that observation goes and that EXT-AI stays
  required because the evidence is not in this tree. The exFAT sidecar difference between a
  maintainer's machine and CI is named so it is not filed twice.

### Changed, everyday templates

- `templates/planning/gtm-plan.md` and `templates/operate/experiment-brief.md` each scored
  88.6 on `tools/template_rubric.py`, both held back by the same mark: `failure_aware` at
  0.429, three warnings spread across seven sections. Each of their seven `##` sections now
  carries one concrete failure mode in its existing guidance comment, naming the bad answer
  and the tell that reveals it, in the file's own voice: a cohort named by title alone is not
  a beachhead, a metric borrowed from the marketing dashboard is a bad answer, a guardrail
  with no numeric floor is not a guardrail, a gate signed by the plan's own author is a rubber
  stamp rather than a check. `templates/definition/one-pager.md` scored 89.8, held back by two
  marks: `fillable` at 0.3 (three fields) and `failure_aware` at 0.667 (six warnings over nine
  sections). Its six sections that carried no failure-mode language at all got the same
  treatment, and three places that asked for a value in prose or left a table cell bare now
  carry a fill-in field in the tree's `[field name]` convention instead: the guardrail row
  names the missing number, the scope row gets a ticket-ID field, and the acceptance row spells
  out given, when, then. No existing sentence, link, table row, or the ILLUSTRATIVE example
  moved to make room for any of this. gtm-plan.md and experiment-brief.md now score 100.0;
  one-pager.md scores 99.0 (fillable 0.8, eight fields; failure_aware 1.0, twelve warnings).
  `tools/template_rubric.py` itself was not touched: every point moved because guidance was
  written into these three files, not because the instrument changed.

### Fixed, exFAT portability

- The maintainer's checkout lives on an exFAT external drive. macOS writes an AppleDouble
  sidecar (`._<name>`) beside every file and directory there, and a clone or checkout on
  exFAT, FAT, or SMB accumulates one per tracked entry -- 654 of them in this tree, none
  tracked by git. Hosted CI runs on Linux and never sees a single one, so CI stayed green
  while the maintainer's own machine failed OM-2, WS-4, WS-5, HR-7, CO-4, and CI-1, all with
  the same root cause and all on Python 3.12.13. `tools/workspace.py`'s `read_text()`, called
  during template and workspace enumeration (`tools/init_product.py`'s `every_shipped_template`,
  `relink_workspace`, and `check_workspace`, reached from `add_every_template` and the
  `--check` route), raised `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb0 in
  position 37` the first time an `rglob("*.md")` walk handed it a `._*.md` sidecar instead of
  the document it shadows. `pmos/skills.py`'s `SkillRegistry.load()` raised
  `SkillContractError("runtime root contains unknown or unsafe entry")` the moment the
  runtime skills root held a `._<skilldir>` sidecar file, because the admission check was
  name-only (anything starting with `.` was rejected) and a sidecar is a regular file, not
  the directory every real skill is. `harness/runner.py`'s job-queue listing counted a
  `._<fingerprint>.json` sidecar as a second durable job record, because it matched the same
  `folder.glob("*.json")` a real record does -- a queued run that should leave exactly one
  record read back as two. And `test_pmos_invariants.py`'s own subprocess-timeout guard,
  which scans `tools/*.py`, choked on a `._*.py` sidecar the same way `tools/workspace.py`
  did.
- The repository had already solved this class once, for `tools/review_gate.py`'s reviewed-
  tree digest, by asking git which paths are actually tracked. That answer does not travel:
  `pmos/` is a dependency-free package by policy and cannot import from `tools/`, let alone
  shell out to git, and every site above needed an answer before any of them could know
  whether a git work tree was even in play. `pmos/sidecars.py` is the one predicate both
  `pmos/` and `tools/` can reach without a cross-import (`tools/` already imports `pmos`).
  It recognizes a sidecar positively, never by name alone: a path is an AppleDouble sidecar
  only if its name starts with `._`, it is a regular file (not a symlink, not a directory),
  its first four bytes are the AppleDouble magic `00 05 16 07`, and a sibling entry with the
  `._` prefix removed exists beside it. A directory named `._foo`, a plain dotfile with no
  magic header, and a `._`-prefixed file with the right magic but no sibling all keep
  whatever behaviour -- crash, error, or listing -- they had before this module existed.
  `tools/review_gate.py` keeps its own name-only, tracked-aware rule unchanged, because a
  tracked file force-added under a sidecar-shaped name still has to be reviewed whether or
  not it happens to carry the AppleDouble magic; a test now pins that the two never disagree
  about a name both could apply to.
- `SkillRegistry.load()`, the template and workspace enumeration in `tools/init_product.py`,
  and a new `harness/runner.py` function (`queue_records()`, now the one place both
  `list_queue()` and its tests read the job list from) all filter through this predicate.
  None of it can be exercised on hosted CI or on this task's own APFS worktree, since neither
  filesystem grows a real AppleDouble sidecar on its own, so every fix carries a synthetic
  regression: a `._x.md` or `._x.py` written with the real magic bytes beside a real sibling,
  proven to reproduce each defect above against the unmodified code before the fix and to
  pass after it.
- The first version of this fix covered the runtime root and passed every synthetic case on
  an APFS worktree. Run on the exFAT checkout itself, the very next check failed instead:
  every asset inside a skill carries its own sidecar (`._SKILL.md` beside `SKILL.md`), the
  per-skill asset walk listed it, and the shipped set "differed from the trusted manifest"
  for the first skill it reached. The walk now applies the same positive recognition. Because
  a sidecar is only recognised beside the asset it shadows, a directory can never consist of
  sidecars alone, so the empty-directory rule keeps its meaning and a sidecar-shaped file
  with no sibling is still listed and still fails the comparison. The lesson is recorded
  here because it is the general one: a portability fix is proven on the volume that
  exhibits the defect, not on the one that does not.
- Third site, found the same way after the second: `tools/readiness_probe.py` walked
  `rglob("*.md")` in the drift probe and read every hit, so the probe raised on the drive and
  the `links_green` hard gate stayed off while all three link criteria passed; the lifecycle
  probe counted the same sidecars as installed documents. Both now walk through one helper
  that applies the predicate, with a regression that also asserts the probes use it.


### Fixed, third review round

An independent reviewer (OpenAI Codex, reporting itself as GPT-5) read the exact tree at
`0384d4a`, ran every gate, and rejected it with one P0, one P1 and one P2. Each is closed here
with the regression the reviewer's own reproduction implies.

- P0. The gateway call rewritten in the previous round returned before reading the cost
  whenever it refused an answer as evidence: a cache replay, a compressed prompt, or a body
  model disagreeing with the `X-OmniRoute-Model` header. The reviewer sent a body carrying
  `usage.cost` 0.75 under each condition; each was rightly refused and each aggregated to
  $0.00 with `cost_unknown` false, against a charge the gateway had reported. Billing is now
  read before any judgement about the answer and travels with every error result, including
  an error body and an HTTP error whose headers carry a cost; the run loop carries it through
  the identity checks too, so a substituted model that was billed for is billed for. A charge
  on a refused answer breaches a zero ceiling and stops the run, as it should have.
- P1. The sidecar predicate recognised AppleDouble files by format alone. The reviewer
  force-added `._real.md` with genuine AppleDouble bytes beside `real.md`, and every loader
  excused it: git was carrying the file, and nothing had asked. `pmos/sidecars.py` now carries
  the same tracked-set logic `tools/review_gate.py` already had, as `SidecarFilter`: a file git
  tracks is content whatever its bytes look like and is never excused; only in a tree git does
  not know is the format the whole rule; a repository git cannot inspect fails closed rather
  than reading as an empty tracked set. Every call site (the skill registry's root and asset
  walk, the template and workspace enumeration, the queue listing, the probes, the invariants
  scan) constructs one filter per walk and consults git once.
- P2. A catalog price of `NaN` or `Infinity` parsed to a float that passed the none-or-negative
  test, reached `ModelSpec`, and raised for the whole catalog on account of one row. Non-finite
  is unpriceable; the row is dropped and its neighbours kept.
- Also in this round, found by the lead and not by the reviewer: commit `a92cefa` on the exFAT
  branch replaced a test by slicing from its first line to the file's `__main__` block, and
  because that block had just been moved to the end of the file the slice also removed the
  four `UnpriceableCatalogRowsTests` cases the previous round had added. They were absent from
  `main` for five merges and are restored here unchanged, with the NaN case added beside them.
  Recorded because a test that disappears without a failing build is exactly the class of
  loss the review record is meant to make visible, and it was not.

### Fixed, fourth review round

The same reviewer re-read the tree at `a17c9c1`, confirmed all three earlier findings closed,
and rejected again on one P1 and three P2s, every one of them in code written the same day.

- P1. The gateway billing helper typed the provider's `usage.cost` with the same number parser
  it uses for the response-cost header, so a body cost sent as the string `"0"` became `0.0`
  before `usable_cost` could apply its rule that a numeric string is not a cost; a value the
  contract calls INVALID passed as OK with a clean exit. The body value is now handed on
  exactly as received and typed by `usable_cost` alone, so `"0"` and `True` fail the run as
  INVALID. The header is still parsed, because a header can only ever be a string, and the
  resulting float is still judged by the same validator.
- P2. `SidecarFilter` shortcut to "excused" when there was no repository, before checking that
  the path lay under its root, so a genuine sidecar from another directory was excused by a
  filter built for this one. The root check now comes first in every case.
- P2. An errored gateway call the gateway said nothing about aggregated as `cost_usd` 0.0 with
  `cost_unknown` false. Silence about money is not $0.00: such a call is now recorded with
  cost status UNKNOWN and the aggregate says so, on both transports; the one exception is the
  refusal made before any request leaves this process. The direct transport's totals now
  carry `cost_unknown` too, which they never did.
- P2. Restoring the four deleted tests did not guard against the class of loss. Two guards
  now: the restored and new skills test methods are named in the readiness registry, so a
  deletion is a dangling id and a red verifier; and `docs/readiness/test-classes.json` is an
  inventory of every test class at the root, which `test_pmos_invariants` asserts is exactly
  what the modules define, so a class cannot be deleted, renamed or added without editing
  that file in the same change. The inventory proved itself on the way in: the first version
  was generated before the guard class existed and the guard failed on its own absence.

### Added, experience design layer (MINOR)

- A `knowledge/design/` sub-layer, sixteen files (`README.md` plus fifteen cards), answering how a PM reads and judges experience design without doing the designer's job: usability heuristics, interaction design principles, a UX-laws evidence ledger, accessibility as practice and as dated regulation, internationalisation and RTL, content design and forms, deceptive design, visual foundations, UX measurement, PM and design collaboration, design systems and tokens, component-driven development, UI dependency licensing, and AI interaction patterns. Sits beside `knowledge/roles/` and `knowledge/domains/` as a third sub-layer.
- Six `frameworks/design/` worksheets, a ninth worksheet group: heuristic evaluation, content and microcopy audit, UX scorecard, design critique, choice symmetry audit, and design system audit. Took the frameworks layer from 58 worksheets in eight groups to 64 in nine.
- Seven `templates/` additions across three directories: `definition/ui-state-inventory.md` and `definition/ux-writing-guide.md`; `architecture/component-spec.md`, `architecture/design-md.md` (the filled copy lands at `products/<name>/DESIGN.md`, beside `STATE.md`), and `architecture/design-review-record.md` (one file across the Gate 3 critique and the Gate 4 live-build check, replacing the planned separate design QA sign-off); `architecture/localisation-rtl-checklist.md`; and `ai/ai-interaction-spec.md`, the user-facing half of the AI overlay. Took the templates layer from 100 templates to 107.
- `skills/design-review/SKILL.md`, driving the review record, the heuristic evaluation, the content and microcopy audit, the design critique, the choice-symmetry audit, and the localisation and accessibility checklists.
- `docs/REFERENCES-DESIGN.md`, the single source-and-licence register for the whole design layer; every adapted, paraphrased or cited source used to build it is listed there with its reuse class, so no card or worksheet carries its own licence note.
- `learn/path-design.md`, a fourth study path, six steps plus a capstone, on Kerbline, an invented council resident portal, ending in a scored design review record at Gate 3.
- Design-layer worked examples across all three journeys: the Harbourgate guest-checkout redesign (heuristic evaluation, design review record, component spec, DESIGN.md), the Ledgerline expense copilot's add-on flows and AI surface (UX scorecard, design critique, choice-symmetry audit, design-system audit, AI interaction spec), and Sahulat's second, agent-assisted DISCOVER pass (content and microcopy audit, localisation and RTL checklist, UX writing guide, UI state inventory), each journey carrying a supplementary design sheet that extends its data sheet without contradicting it.
- Integration edits across the OS: `templates/architecture/accessibility-checklist.md`, `discovery/usability-test-plan.md`, `execution/tech-debt-register.md`, `delivery/edge-cases.md`, `definition/nfr.md`, `definition/acceptance-criteria.md`, and `delivery/release-readiness.md` link the new design layer where a field already existed for it; `frameworks/metrics/heart-metrics.md` links the UX scorecard for its Happiness rule; `knowledge/roles/triad-decision-rights.md` gains the design-critique-versus-review decision-rights row; nine `knowledge/domains/` cards link the design cards and worksheets that bend them; `os/WHICH-DOCUMENT.md`, `os/STAGE-GATES.md`, `os/maps/define.md`, `os/maps/design.md` and `os/maps/build.md` route to the new artifacts; `agents/TEAM.md` adds the design-review skill as a DEFINE, DESIGN and BUILD evaluator; and `CLAUDE.md` and `harness/MANIFEST.json` carry the new router row and task entry. None of these weaken a gate, a check, a threshold or a test.

### Added, coverage and industry examples (MINOR)

- Eighty-one further worked artifacts across the three journeys, extending Ledgerline from 13 to 46, Sahulat from 14 to 40, and Harbourgate from 16 to 51, each filling one remaining template or worksheet the journey had not yet exampled. Each journey gained a supplementary coverage sheet holding the additional figures those artifacts need, extending the journey's own data sheet without contradicting it.
- Ten further standalone examples, one small invented company apiece, filling every remaining template and worksheet that had no worked example at all: a BRD, a design brief, an FRD, HEART metrics, a lean canvas, a PR/FAQ, a privacy impact assessment, a program charter, a risk matrix, and unit economics.
- Three new `knowledge/domains/` cards, taking the domain layer from forty-four to forty-seven: aerospace and defence, construction and AEC, and sports betting and iGaming, plus a fold-in note on thirteen existing cards pointing to the adjacent industry each one now also covers (data and analytics platforms on the developer-tools card, CPG and B2B commerce on ecommerce, and so on).
- Forty-one industry examples in `examples/`, one per new or fold-in domain card, each the `**Filled in this repo:**` slice the card itself names, on its own small invented company.
- `examples/README.md` reindexed in full: the standalone table, a new "Industry examples" section, and all three journey tables, grouped by product per the update this change set makes to the indexing convention itself.

### Known external requirements

- Local checks do not verify hosted CI on the exact commit, a live provider, vendor sandboxes, a non-maintainer journey, independent human team review, organization-specific regulatory approval, or a published release artifact. No tag or published release is claimed here.

### Fixed, the development handoff's readiness report

- Two ways a development handoff could report `development_ready: true` on content that was not there. A section counted any link whose target existed, including an ordinary file carrying no artifact block; since the runtime records a revision only for artifacts, nine sections could point at one scratch file and editing it afterwards staled nothing. A section now needs at least one link to a file carrying an artifact block, and reports the new status `unbound` otherwise. Separately, a section whose only content was the words `N/A because`, with no reason after them, counted as a deliberate exemption; an exemption now needs its reason, and a section without one is empty. An unbound link also beats a reasoned exemption, because linking a file claims the section applies. Both were reproducible through `pmos handoff` and both passed the suite before this change: `test_relative_and_dotdot_links_inside_root_are_linked` asserted readiness on a link to a file with no artifact block, and now covers the path-resolution case it was written for.

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
