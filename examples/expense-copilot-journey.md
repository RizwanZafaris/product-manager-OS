# Journey: The Ledgerline Expense Copilot, from problem to development handoff

Fills no template. It is the index and data sheet for the internal-v1 chain: the fourteen artifacts in the artifact map below, from the understood problem at Gate 1 to the development-ready handoff at Gate 3, two of them the existing discovery document and PRD and twelve not yet written. Everything here is invented and ILLUSTRATIVE: the dates, the ids, the decisions and every figure are fiction, built so that twelve new artifacts can share one set of facts with each other, with the two existing artifacts, and with [ledgerline-journey.md](ledgerline-journey.md). No figure is a target to copy or a claim about any real product. See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Date:** 2026-09-11 · **Status:** Gate 3 approved 2026-09-11 (fictional), build under way

## The journey in one page

### The setting

Ledgerline is the same fictional mid-market software company as [ledgerline-journey.md](ledgerline-journey.md): about 900 employees, selling the Ledgerline platform, invoicing, bills and expenses, on three plans. This journey is that journey's prequel. It covers the internal build Ledgerline's own finance team commissioned for Ledgerline's own filers, from the trigger through a development-ready handoff, entirely before any customer-facing decision exists. [ledgerline-journey.md](ledgerline-journey.md) picks up on 2026-10-12, the day this build goes live; everything on this sheet happens before that date, inside DISCOVER, DEFINE and DESIGN.

Two documents from this window already exist: [expense-copilot-discovery.md](expense-copilot-discovery.md), closed with a GO on 2026-08-14, and [expense-copilot-prd.md](expense-copilot-prd.md), approved at Gate 2 on 2026-08-28. Both used to name the company Fernwood Software; the note at the foot of this file records the correction. Everything else in the chain, the problem framing that opens DISCOVER, the vision, strategy and roadmap that DEFINE approves alongside the PRD, the acceptance criteria signed the same sitting, and the whole DESIGN set that closes at Gate 3, is new: twelve artifacts, none yet written, each with a fixed place in the artifact map below.

### The people

Three names carry this chain, the same three the discovery document and PRD already name and [ledgerline-journey.md](ledgerline-journey.md) names in full. Maya Chen, product manager, owns every artifact here and signs Gate 1 and Gate 3 as product owner. Priya Nair, engineering lead, signs Gate 2 as engineering lead and Gate 3 as the architect or senior engineer; the internal build has no separate security lead, so she signs Gate 3's security-reviewer line as well, a fact this data sheet records rather than papers over. Daniel Okafor, finance lead, sponsors the build, signs Gate 1 as the sponsor who can stop it and Gate 2 as business sponsor, and supplies the finance-system baselines both existing documents already cite. The legal lead, who appears by role in [ledgerline-journey.md](ledgerline-journey.md), owns the two open items this chain cannot close on its own: the model vendor's training-data clause and the receipt-retention schedule, both due before Gate 5. No one else appears; this journey adds no name the cast does not already carry.

### The stages, with dates

**DISCOVER (2026-08-13 to 2026-08-14).** The problem framing is drafted 2026-08-13, the same day [ledgerline-business-case.md](ledgerline-business-case.md) is written. Discovery closes with the GO on 2026-08-14, decided by Maya Chen and Daniel Okafor; that is also Gate 1.

**DEFINE (2026-08-18 to 2026-08-28).** The vision is drafted 2026-08-18, the product strategy 2026-08-21, the roadmap 2026-08-25. Vision, strategy, roadmap, the PRD and the acceptance criteria are all approved together at Gate 2 on 2026-08-28, SIGNED by Maya Chen, Priya Nair and Daniel Okafor.

**DESIGN (2026-09-03 to 2026-09-11).** ADR-0001 is accepted 2026-09-03. The data model and the API contract are drafted together 2026-09-05. A premortem on 2026-09-08 seeds the dependency register and the risk register, drafted the same day; the decision log is read in full at the gate, carrying entries from 2026-08-14 onward. The development handoff is drafted 2026-09-10, linking all thirteen other artifacts. Gate 3 is REVIEWED AND ACCEPTED on 2026-09-11, signed by Maya Chen and Priya Nair, and this journey closes there.

**Beyond this chain.** The build runs toward Gate 5, signed 2026-10-09 per function, and go-live on 2026-10-12, where [ledgerline-journey.md](ledgerline-journey.md) begins.

## Data sheet (ILLUSTRATIVE)

### Conventions the artifacts share

- Dates are YYYY-MM-DD. Every value below is invented and ILLUSTRATIVE, the same convention [ledgerline-journey.md](ledgerline-journey.md) uses.
- Two data sheets hold every number, date and id this chain's twelve new artifacts may use: this one, and [ledgerline-journey.md](ledgerline-journey.md)'s own sheet, rows N1 to N25 (the internal-v1 rows; N26 onward belong to the post-launch commercial add-on and are out of scope here). An artifact that needs a figure not on either sheet is wrong, or a sheet is, and the sheet is corrected first.
- Requirement ids are REQ-1 to REQ-6, one per row of the PRD's Functional scope table, in that table's own order, never renumbered.
- Acceptance criterion ids are AC-1 onward, each verifying exactly one REQ id.
- Decision log ids are D-1 onward, this chain's own sequence. [ledgerline-journey.md](ledgerline-journey.md)'s D1 to D9 are a different document, the post-launch journey's own decision table; the two never share a number.
- Dependency ids are DEPV-1 onward and risk ids RV-1 onward; the V marks this internal-v1 chain so neither collides with [ledgerline-journey.md](ledgerline-journey.md)'s later DEP1 to DEP5 or R1 to R6.
- ADR-0001 is this product's first architecture decision record. [ledgerline-journey.md](ledgerline-journey.md)'s ADR-007 and ADR-008 are later, post-launch and unrelated.
- The development handoff carries a `Gap:` line only where one is true. This sheet exists so that it never has to.

### Numbers

| # | Name | Value, with unit | Source inside the fiction | Firmness |
|---|---|---|---|---|
| V1 | Problem framing, drafted | 2026-08-13, one day before Gate 1, the same date [ledgerline-business-case.md](ledgerline-business-case.md) was written | expense-copilot-problem-framing.md (new) | date, decided |
| V2 | Gate 1 decision | GO, 2026-08-14; product owner Maya Chen, sponsor Daniel Okafor, per the discovery document's own Go or no-go section | [expense-copilot-discovery.md](expense-copilot-discovery.md) | decided |
| V3 | Vision, drafted | 2026-08-18 | expense-copilot-vision.md (new) | date, decided |
| V4 | Product strategy, drafted | 2026-08-21 | expense-copilot-product-strategy.md (new) | date, decided |
| V5 | Roadmap, drafted | 2026-08-25 | expense-copilot-roadmap.md (new) | date, decided |
| V6 | PRD approved at Gate 2 | 2026-08-28, Version 2 | [expense-copilot-prd.md](expense-copilot-prd.md), header | date, decided; restates the PRD's own line |
| V7 | Acceptance criteria, approved | 2026-08-28, the same sitting as the PRD | expense-copilot-acceptance-criteria.md (new) | date, decided |
| V8 | Gate 2 decision | SIGNED, 2026-08-28; product owner Maya Chen, engineering lead Priya Nair, business sponsor Daniel Okafor; vision, strategy, roadmap, PRD and acceptance criteria approved together; the regulated overlay line does not fire, because no financial or data regulator applies to an internal expense tool | os/STAGE-GATES.md Gate 2; [expense-copilot-prd.md](expense-copilot-prd.md) | decided |
| V9 | ADR-0001 | Accepted 2026-09-03, deciders Priya Nair and Maya Chen. Decides: extract fields from one receipt per model call, matched to one uploaded photo or one forwarded-email attachment. Rejects: batching multiple receipts into a single extraction call, the same option the PRD's Trade-offs-accepted table already rejected for v1 (multi-receipt capture wanted, one receipt per item shipped, because the extraction eval set could not hold a threshold on overlapping receipts). Consequence: a field the model cannot read stays blank and flagged rather than guessed, per the PRD's never-invent rule | expense-copilot-adr.md (new); rejected option already fixed by [expense-copilot-prd.md](expense-copilot-prd.md), Trade-offs accepted at Gate 2, row 1 | decided |
| V10 | Data model, drafted | 2026-09-05. Entities: Receipt, DraftReport, LineItem, CategoryMapping, CorrectionLogEntry. Receipt and LineItem are flagged provisionally as carrying personal data, per the PRD's own Launch-criteria line that receipts carry personal data; formal PII classification and sign-off wait for the compliance impact assessment at Gate 5, not this document | [expense-copilot-prd.md](expense-copilot-prd.md), Launch criteria; expense-copilot-data-model.md (new) | date, decided |
| V11 | API contract, drafted | 2026-09-05, the same day as the data model. Resources: POST /receipts (ingest a photo or forwarded email, REQ-1); GET /receipts/{id} (extraction status, REQ-2); POST /reports/{id}/draft (assemble a draft report, REQ-4); PATCH /reports/{id}/line-items/{id} (filer edits a field, REQ-4); POST /reports/{id}/submit (the only action that closes a report, REQ-4); PATCH /category-mappings/{id} (admin correction loop, REQ-6) | expense-copilot-api-contract.md (new) | date, decided |
| V12 | Decision log, coverage | Entries from 2026-08-14 (D-1) to 2026-09-08 (D-6), read in full at Gate 3; the index and all six entries are in Shared identifiers below | expense-copilot-decision-log.md (new) | date, decided |
| V13 | Dependency register, drafted | 2026-09-08, from the same review that ran the premortem. DEPV-1 to DEPV-4 are in Shared identifiers below | expense-copilot-dependency-register.md (new) | date, decided |
| V14 | Risk register, drafted | 2026-09-08, from a premortem run the same day with [frameworks/execution/premortem-worksheet.md](../frameworks/execution/premortem-worksheet.md). RV-1 to RV-4 are in Shared identifiers below | expense-copilot-risk-register.md (new) | date, decided |
| V15 | Development handoff, drafted | 2026-09-10 | expense-copilot-development-handoff.md (new) | date, decided |
| V16 | Gate 3 decision | REVIEWED AND ACCEPTED, 2026-09-11; product owner Maya Chen, architect or senior engineer Priya Nair, security reviewer Priya Nair (the same person; this build has no separate security lead) | os/STAGE-GATES.md Gate 3 | decided |
| V17 | Requirement ids | REQ-1 to REQ-6 map one to one, in table order, to the six rows of the PRD's Functional scope table: receipt ingestion, field extraction, category suggestion, draft report assembly, confidence flags, admin correction loop. Full list in Shared identifiers below | [expense-copilot-prd.md](expense-copilot-prd.md), Functional scope table | decided |
| V18 | Acceptance criteria ids | AC-1 to AC-10, each verifying one REQ id. Full list in Shared identifiers below | expense-copilot-acceptance-criteria.md (new) | decided |

### Shared identifiers

**Requirement ids (REQ), from the PRD's functional scope.**

| Id | Requirement | PRD functional-scope row |
|---|---|---|
| REQ-1 | Receipt ingestion: photo upload and forwarded email | row 1 |
| REQ-2 | Field extraction: merchant, date, amount, currency; never guessed when unknown | row 2 |
| REQ-3 | Category suggestion with the matched policy line shown | row 3 |
| REQ-4 | Draft report assembly and edit surface; nothing submitted without the filer's review | row 4 |
| REQ-5 | Confidence flags passed through to the reviewer view | row 5 |
| REQ-6 | Admin correction loop for category mappings, logged and versioned | row 6 |

**Acceptance criteria ids (AC), each verifying one REQ id.**

| Id | Criterion, one line | Verifies | Type |
|---|---|---|---|
| AC-1 | A legible photographed receipt drafts merchant, date, amount and currency | REQ-1, REQ-2 | happy path |
| AC-2 | A forwarded email receipt drafts the same four fields | REQ-1 | happy path |
| AC-3 | A field the model cannot read stays blank and flagged, never guessed | REQ-2 | negative |
| AC-4 | A drafted line shows its suggested category and the policy line it matched | REQ-3 | happy path |
| AC-5 | The filer edits a drafted field before submit and the edit holds | REQ-4 | happy path |
| AC-6 | No report reaches finance until the filer presses submit | REQ-4 | negative, guardrail |
| AC-7 | A low-confidence field is visually distinct in the reviewer's view | REQ-5 | happy path |
| AC-8 | An admin corrects a category mapping and the correction is logged with who and when | REQ-6 | happy path |
| AC-9 | A corrected mapping does not silently rewrite a report already submitted | REQ-6 | edge |
| AC-10 | A photo with more than one receipt in frame is rejected back to the filer with a per-receipt prompt, per the PRD's one-receipt-per-item v1 scope | REQ-1 | edge |

**Decision log (D), this chain's own sequence, all read at Gate 3.**

| Id | Decision | Decider | Date | Type |
|---|---|---|---|---|
| D-1 | GO: proceed from DISCOVER into DEFINE | Daniel Okafor | 2026-08-14 | scope |
| D-2 | Ship one receipt per item in v1, not multi-receipt capture in one photo | Maya Chen | 2026-08-28 | scope |
| D-3 | Ship a static policy mapping in v1; admin corrections are logged but not fed back into suggestions | Maya Chen | 2026-08-28 | scope |
| D-4 | Ship with an ILLUSTRATIVE accuracy threshold in the eval spec, not a finance-agreed number | Daniel Okafor | 2026-08-28 | metric |
| D-5 | Post-launch backlog: fund row 4 (per-diem rules) ahead of row 3 (corporate-card feed matching) despite row 3's higher RICE score, because row 3's confidence is opinion-level at a four-month effort; reopens on a two-week count of reports carrying a card line | Maya Chen | 2026-09-01 | sequencing |
| D-6 | Defer the AI overlay's guardrails, eval spec and red-team review to the PRD's existing Gate 5 launch criteria rather than duplicate them at Gate 3 | Maya Chen | 2026-09-08 | scope |

D-5 records the call [ledgerline-rice-scoring.md](ledgerline-rice-scoring.md) itself flags as belonging here: rows 3 and 4 of that sheet's Step 3 table, with the count that reopens it.

**Dependencies (DEPV), this chain's own sequence.**

| Id | Dependency | Owner | Needed by | Status at Gate 3 (2026-09-11) |
|---|---|---|---|---|
| DEPV-1 | Vendor clause forbidding training on Ledgerline data | the legal lead, with the model vendor | before Gate 5 | open; carried in the PRD's Out of scope list and [ledgerline-rice-scoring.md](ledgerline-rice-scoring.md)'s mandate lane |
| DEPV-2 | Receipt image retention and deletion schedule | the legal lead | before Gate 5, per the PRD's Launch criteria | open |
| DEPV-3 | Model vendor's per-receipt price contracted, not only quoted | Priya Nair, with procurement | before volume outgrows the quoted-rate assumption | open; still quoted, not contracted, even after launch, per [ledgerline-journey.md](ledgerline-journey.md) N9 |
| DEPV-4 | Finance system's approval events joined to draft ids, so objective 1 can be measured | Priya Nair, with finance | 2026-10-09 (Gate 5) | open at Gate 3; delivered on time, per [ledgerline-journey.md](ledgerline-journey.md) N20 |

**Risks (RV), from the DESIGN-stage premortem of 2026-09-08.**

| Id | Risk | Owner | Opened | Status at Gate 3 (2026-09-11) |
|---|---|---|---|---|
| RV-1 | Extraction quality on crumpled or foreign-language receipts is unproven | Priya Nair | 2026-08-14, discovery document, known risks carried forward | open; echoed by [ledgerline-rice-scoring.md](ledgerline-rice-scoring.md)'s row 7 open item |
| RV-2 | The model vendor's training-data and retention terms are unresolved | the legal lead | 2026-08-14, discovery document | open; mitigated when DEPV-1 delivers |
| RV-3 | Receipts accumulate before a retention and deletion schedule is signed | the legal lead | 2026-09-08, premortem | open; mitigated when DEPV-2 delivers |
| RV-4 | One model call per receipt (ADR-0001) raises cost or latency if monthly volume outgrows the internal baseline | Priya Nair | 2026-09-08, premortem | open; watched against [ledgerline-journey.md](ledgerline-journey.md) N2 |

**Architecture decision records.** ADR-0001 (2026-09-03): extract fields from one receipt per model call; never batch multiple receipts into one call. This product's first ADR; [ledgerline-journey.md](ledgerline-journey.md)'s ADR-007 and ADR-008 are later, post-launch and unrelated.

### Timeline

| Date | Event | Artifact that records it |
|---|---|---|
| 2026-08-13 | Business case written, approved at Gate 1 with the GO on 2026-08-14; problem framing drafted the same day | [ledgerline-business-case.md](ledgerline-business-case.md); expense-copilot-problem-framing.md (new) |
| 2026-08-14 | Discovery closes GO; Gate 1 decision; D-1 | [expense-copilot-discovery.md](expense-copilot-discovery.md) |
| 2026-08-18 | Vision drafted | expense-copilot-vision.md (new) |
| 2026-08-18 to 2026-08-22 | Kano survey fielded (framework sheet, not part of this chain) | [ledgerline-kano-survey.md](ledgerline-kano-survey.md) |
| 2026-08-20 | Strategy kernel written (framework sheet, not part of this chain) | [ledgerline-strategy-kernel.md](ledgerline-strategy-kernel.md) |
| 2026-08-21 | Product strategy drafted | expense-copilot-product-strategy.md (new) |
| 2026-08-25 | Roadmap drafted | expense-copilot-roadmap.md (new) |
| 2026-08-28 | Gate 2 SIGNED: vision, strategy, roadmap, PRD and acceptance criteria approved together; D-2, D-3, D-4 | [expense-copilot-prd.md](expense-copilot-prd.md); expense-copilot-acceptance-criteria.md (new) |
| 2026-09-01 | RICE sheet and north star tree written (framework sheets, not part of this chain); D-5 | [ledgerline-rice-scoring.md](ledgerline-rice-scoring.md); [ledgerline-north-star-tree.md](ledgerline-north-star-tree.md) |
| 2026-09-03 | ADR-0001 accepted | expense-copilot-adr.md (new) |
| 2026-09-05 | Data model and API contract drafted | expense-copilot-data-model.md, expense-copilot-api-contract.md (new) |
| 2026-09-08 | Premortem run; dependency register and risk register drafted; D-6 | expense-copilot-dependency-register.md, expense-copilot-risk-register.md (new) |
| 2026-09-10 | Development handoff drafted | expense-copilot-development-handoff.md (new) |
| 2026-09-11 | Gate 3 REVIEWED AND ACCEPTED; this journey closed | expense-copilot-development-handoff.md (new) |
| 2026-10-09 | Internal Gate 5 signed per function | not reproduced here; see [ledgerline-journey.md](ledgerline-journey.md) N16 |
| 2026-10-12 | Copilot live for Ledgerline's own filers; [ledgerline-journey.md](ledgerline-journey.md) begins | not reproduced here; see [ledgerline-journey.md](ledgerline-journey.md) N16 |

## Artifact map

Fourteen steps. The "stage and gate" column is the template's own. The last column names what the artifact decides and which rows of this sheet, or of [ledgerline-journey.md](ledgerline-journey.md), it may not contradict. A link in the Example column means the file exists today; plain text means it does not exist yet and is not linked, so no link here goes unresolved.

| Step | Stage and gate | Template | Example | What it decides, and which rows it may not contradict |
|---|---|---|---|---|
| 1 | DISCOVER, Gate 1 | [templates/discovery/problem-framing.md](../templates/discovery/problem-framing.md) | expense-copilot-problem-framing.md (not yet written) | Opens the chain: the problem statement, the cost of inaction and the decision requested, already answered in prose by the discovery document. Uses V1; must not restate N1 to N6 of [ledgerline-journey.md](ledgerline-journey.md) differently. |
| 2 | DISCOVER, Gate 1 | [templates/discovery/discovery-document.md](../templates/discovery/discovery-document.md) | [expense-copilot-discovery.md](expense-copilot-discovery.md) (existing; name corrected) | The GO and its rationale. Uses V2; N1 to N6. |
| 3 | DEFINE, Gate 2 | [templates/planning/vision.md](../templates/planning/vision.md) | expense-copilot-vision.md (not yet written) | The destination and who it serves; approved by Daniel Okafor as business sponsor. Uses V3, V8. |
| 4 | DEFINE, Gate 2 | [templates/planning/product-strategy.md](../templates/planning/product-strategy.md) | expense-copilot-product-strategy.md (not yet written) | Where to play, how to win, and what v1 will not do, tracing to the PRD's own Out of scope list. Uses V4, V8, V17. |
| 5 | DEFINE, Gate 2 | [templates/planning/roadmap.md](../templates/planning/roadmap.md) | expense-copilot-roadmap.md (not yet written) | Phases ordered toward the PRD's three objectives, each with a success measure. Uses V5, V8; N16. |
| 6 | DEFINE, Gate 2 | [templates/definition/prd.md](../templates/definition/prd.md) | [expense-copilot-prd.md](expense-copilot-prd.md) (existing; name corrected) | Functional scope REQ-1 to REQ-6, the three objectives, the trade-offs behind D-2 to D-4. Uses V6, V8, V17. |
| 7 | DEFINE, Gate 2 | [templates/definition/acceptance-criteria.md](../templates/definition/acceptance-criteria.md) | expense-copilot-acceptance-criteria.md (not yet written) | AC-1 to AC-10, each verifying one REQ id, with edge and negative coverage. Uses V7, V17, V18. |
| 8 | DESIGN, Gate 3 | [templates/architecture/adr.md](../templates/architecture/adr.md) | expense-copilot-adr.md (not yet written) | ADR-0001, the receipt-pipeline decision, its rejected option and its consequence. Uses V9. |
| 9 | DESIGN, Gate 3 | [templates/architecture/data-model.md](../templates/architecture/data-model.md) | expense-copilot-data-model.md (not yet written) | The five entities, their relationships and their provisional PII flags. Uses V10. |
| 10 | DESIGN, Gate 3 | [templates/architecture/api-contract.md](../templates/architecture/api-contract.md) | expense-copilot-api-contract.md (not yet written) | The six resources, one set per REQ id that needs an endpoint, with idempotency on the submit call. Uses V11, V17. |
| 11 | all stages, read at Gate 3 | [templates/execution/decision-log.md](../templates/execution/decision-log.md) | expense-copilot-decision-log.md (not yet written) | D-1 to D-6 in full, index and entries, none reversing another. Uses V12 and the Decision log table above. |
| 12 | DESIGN, Gate 3 | [templates/execution/dependency-register.md](../templates/execution/dependency-register.md) | expense-copilot-dependency-register.md (not yet written) | DEPV-1 to DEPV-4, each with an owner, a needed-by date and an escalation path. Uses V13 and the Dependencies table above. |
| 13 | DESIGN, Gate 3 | [templates/execution/risk-register.md](../templates/execution/risk-register.md) | expense-copilot-risk-register.md (not yet written) | RV-1 to RV-4, scored from the 2026-09-08 premortem. Uses V14 and the Risks table above. |
| 14 | DESIGN exit, Gate 3 | [templates/architecture/development-handoff.md](../templates/architecture/development-handoff.md) | expense-copilot-development-handoff.md (not yet written) | Links all thirteen other artifacts across its nine sections, with no `Gap:` line, and names Gates 1 to 3 as fictional sign-offs. Uses V15, V2, V8, V16. |

## What this journey teaches

- **The two-sheet rule works before the artifacts exist, not only after.** Every one of the twelve unwritten files already has its dates, its ids and its rejected option fixed here, so a later writer contradicts this sheet by choice, not by accident.
- **A rejected option does not need a dramatic loss to be worth recording.** ADR-0001's losing option, batching multiple receipts into one call, was already rejected once, in the PRD's own trade-off table; the ADR just gives that call its architectural half.
- **A small team's honest gap is worth one sentence, not a workaround.** Priya Nair signing both of Gate 3's engineering lines is written down as a fact about the team's size, not smoothed over with an invented security lead.
- **A decision log is not only for decisions that went wrong.** D-1 to D-6 hold a GO, three accepted trade-offs, a backlog sequencing call and a scope deferral; none reverses another, and the log is still worth reading.
- **A dependency that survives the gate is one whose status can be checked later.** DEPV-3 and DEPV-4 both point at rows in [ledgerline-journey.md](ledgerline-journey.md), N9 and N20, so their Gate 3 status is not the last word on them.

## The company-name correction

The internal-v1 examples, [expense-copilot-discovery.md](expense-copilot-discovery.md) and [expense-copilot-prd.md](expense-copilot-prd.md), used to name the company Fernwood Software: "Support tickets tagged 'expenses' at Fernwood Software" in the discovery document's Trigger section, and "filers at Fernwood Software re-type receipt data" in the PRD's Background section. Both now read Ledgerline, the name [ledgerline-journey.md](ledgerline-journey.md) already used for the same fictional company, the same product and the same people. [conductor-transcript.md](conductor-transcript.md) keeps its own Fernwood Software; that transcript is about a different, unrelated company, and this correction does not touch it.
