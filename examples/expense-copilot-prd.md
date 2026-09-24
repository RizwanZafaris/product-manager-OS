# PRD: Expense Copilot

Produced with [templates/definition/prd.md](../templates/definition/prd.md). Fictional product, fictional company, every number invented for illustration; thresholds are shown to demonstrate the format, not to recommend values. Every approval recorded below, including the Gate 2 sign-off block, is an ILLUSTRATIVE sign-off by this chain's fictional cast: no real person signed anything here, and nothing below is evidence that any review took place. Figures, ids and dates are carried from [expense-copilot-journey.md](expense-copilot-journey.md)'s data sheet (its V-rows) and [ledgerline-journey.md](ledgerline-journey.md)'s (its N-rows), so this document agrees with the rest of the internal-v1 chain rather than inventing its own facts. See the [examples index](README.md).

This is a complete fill: every section of the template's spine, 0 to 13, plus sign-off and the exit gate, is answered here or carries an explicit reason why it is not. Where this internal build genuinely has no companion document, the gap is named with an owner and a date instead of being left blank.

**Owner:** Maya Chen, Product Manager · **Engineering lead:** Priya Nair · **Design lead:** none; this build carries no separate design lead, and the line is named rather than left blank (see [Sign-off](#sign-off))
**Date:** 2026-08-28 · **Status:** Approved at Gate 2, SIGNED (V6, V8) · **Version:** 2
**Who implements this:** a human engineering team, Priya Nair's. The product contains a model, so the AI overlay governs what that team builds; it does not change who builds it.
**Links:** [problem framing](expense-copilot-problem-framing.md) · [discovery document](expense-copilot-discovery.md) · [vision](expense-copilot-vision.md) · [product strategy](expense-copilot-product-strategy.md) · [roadmap](expense-copilot-roadmap.md) · [acceptance criteria](expense-copilot-acceptance-criteria.md). No BRD, no FRD, and no separate non-functional or assumptions register is filled for this build; sections 5 and 11 carry what those documents would have carried, and say so.

## 0. The one read

**Problem:** Ledgerline's own filers re-type receipt data and bounce on category rules they have never read, and about a third of reports come back; the three finance reviewers spend roughly 30 hours a month on mechanical checks.
**What ships:** The copilot reads a photographed or forwarded receipt and drafts the line, merchant, date, amount, currency and a suggested category with the policy line it matched, which the filer edits and submits.
**Success looks like:** First-submission approval on drafted reports rises from 62% to 80% (objective 1).
**Deliberately not doing:** Nothing is ever submitted without the filer pressing submit; there is no auto-submission path, in v1 or later.
**We stop if:** Under 30% of eligible reports use the draft flow, the business case's own tripwire, called by Daniel Okafor at the first metrics review.

## 1. Background

Discovery ran 2026-07-20 to 2026-08-14 and closed with a GO: see [expense-copilot-discovery.md](expense-copilot-discovery.md), and the [problem framing](expense-copilot-problem-framing.md) that opened it. Short version: filers at Ledgerline re-type receipt data and bounce on category rules they have never read; reviewers burn their time on mechanical checks. Twelve interviews, eight filers and four finance reviewers, held 2026-07-20 to 2026-08-01, and ten of the twelve named re-typing as the worst part, unprompted. This PRD defines the first shippable slice. Because the product contains a model, the AI overlay applies: the eval, guardrail, and approval-gate documents named under Launch criteria are part of this spec, not attachments to it.

The hypothesis, copied from the discovery document rather than restated: if the system reads the receipt and drafts the report, filers will submit in one sitting and bounce rates will fall, because the two main bounce causes, typos and category mismatches, are exactly what a draft can get right. The filer stays the author: nothing is submitted without their review, which also keeps accountability where the policy puts it.

## 2. Objectives

| # | Objective | Metric | Baseline | Target | Metric owner | Measured where |
|---|---|---|---|---|---|---|
| O1 | A drafted report is approved the first time it is filed | First-submission approval rate, drafted reports | 62% (N3) | 80% (N4) | Daniel Okafor | finance system of record, joined to draft ids (Q1) |
| O2 | Filing a report stops taking an evening | Median filing time, five-receipt report | 25 minutes (N5) | under 10 minutes (N5) | Maya Chen | in-product timing |
| O3 | Filers choose it without being made to | Share of eligible reports through the draft flow at month two | 0%, the flow does not exist yet | 50% (N19's target line) | Maya Chen | product analytics |

O1 and O3 are discovery's two success signals, agreed with Daniel Okafor on 2026-08-12, and O1's baseline and method come from the finance system of record. O2's baseline comes from timed sessions in discovery, n=8, so it is directional rather than measured, and its target is its own metric owner's, set from that baseline rather than committed to finance. No target above is ILLUSTRATIVE in the sense Gate 2 blocks on: each is agreed with the person who owns the metric. The one unagreed number in this product is the eval spec's extraction threshold, which is not an objective and is handled in section 12, Q3. O1 and O2 trace to the Gate 1 problem statement; O3 traces to discovery's second success signal, adoption without a mandate, rather than to that statement, and the difference is written here rather than blurred. All three trace forward to a [roadmap](expense-copilot-roadmap.md) row, which names objectives 1 to 3 by number.

## 3. Users and stories

**Primary persona:** the filer, an individual contributor who travels one to four times a quarter and files their own reports. Secondary: the three finance reviewers who approve every report. Defined in the discovery document's [target user](expense-copilot-discovery.md#target-user) section; no personas.md is filled for this chain, and that section is the whole definition rather than a summary of one.

| # | Story | Persona | Priority | Acceptance criteria ID |
|---|---|---|---|---|
| REQ-1, REQ-2 | As a filer, I photograph or forward a receipt and get a drafted line item (merchant, date, amount, currency, suggested category) that I can accept, edit, or reject, so filing happens in one sitting. | filer | must | AC-1, AC-2, AC-3, AC-10 |
| REQ-3 | As a filer, I see the policy line behind every suggested category, so a bounce becomes a conversation with a rule, not a mystery. | filer | must | AC-4 |
| REQ-4 | As a filer, nothing is submitted until I review the full report and press submit, so I stay accountable for what goes to finance. | filer | must | AC-5, AC-6 |
| REQ-5 | As a reviewer, machine-drafted fields arrive flagged with the model's confidence, so I spend judgment where it is needed instead of re-checking arithmetic. | finance reviewer | must | AC-7 |
| REQ-6 | As a finance admin, I can correct a category mapping once and have future drafts follow it, so the system converges on our policy instead of fighting it. | finance admin | must | AC-8, AC-9 |

The `#` column carries REQ ids, not story ids, and that is deliberate. This chain fills no user-stories.md and no FRD, so the [acceptance criteria](expense-copilot-acceptance-criteria.md) bind to REQ ids and nothing else; inventing a parallel US namespace here would give every requirement two names and let them drift. REQ-1 to REQ-6 are fixed by the journey's data sheet (V17) in the order of section 4's table and are never renumbered. All ten criteria, AC-1 to AC-10, appear above, so no criterion is orphaned and no must story is uncovered.

## 4. Functional scope

| # | Capability | What it does, in one sentence | Story it serves | Detail |
|---|---|---|---|---|
| REQ-1 | Receipt ingestion: photo upload and forwarded email | Accepts an image or a PDF, one receipt per item in v1 | the one-sitting story | AC-1, AC-2, AC-10 |
| REQ-2 | Field extraction: merchant, date, amount, currency | Reads the four fields and leaves any field it cannot read blank and flagged, never guessed; the never-invent rule follows [templates/ai/hallucination-controls.md](../templates/ai/hallucination-controls.md) | the one-sitting story | AC-1, AC-3 |
| REQ-3 | Category suggestion with the matched policy line shown | Suggests one category and shows the policy line behind it; the filer confirms | the policy-line story | AC-4 |
| REQ-4 | Draft report assembly and edit surface | Assembles the draft, lets the filer edit every field, and sends nothing to finance until the filer presses submit | the accountability story | AC-5, AC-6 |
| REQ-5 | Confidence flags passed through to the reviewer view | Marks low-confidence fields visually distinct in the reviewer's view | the reviewer's judgment story | AC-7 |
| REQ-6 | Admin correction loop for category mappings | Lets a finance admin correct a mapping, logged and versioned; corrections are not fed back into suggestions in v1 (D-3) | the convergence story | AC-8, AC-9 |

This table is the contract of record for what ships. With no FRD in this chain, the Detail column names the acceptance criteria that bind each row rather than FR ids, and those criteria, not this table's prose, are what a tester runs.

## 5. Non-functional summary

Five constraints shape scope rather than merely describe quality. Receipts carry personal data, so how long an image may be kept decides what the storage design may assume. The volume is small and known, which is the only reason one model call per receipt is affordable. The run cost has a ceiling the business case set. The reviewer view has to be readable by people who do not see colour differences, because the confidence flag is the whole point of REQ-5. And nobody outside the team is promised an availability or latency number, which is itself a constraint worth writing down.

| Constraint | Target, or the owner who will produce the number and by when | Why it shapes scope |
|---|---|---|
| Retention and deletion of receipt images | No number yet: the legal lead, by Gate 5 on 2026-10-09 | The schedule decides how long an image may be held, and therefore whether the design stores images at all or only extracted fields |
| Volume the extraction path carries | 9,600 reports a year at about 4.2 receipts a report, roughly the 40,000 receipts the vendor priced against (N2, N9, N10) | Sizes the per-receipt design; one model call per receipt is affordable at this volume and would not be at ten times it |
| Run cost ceiling | $2,500 a month, of which model API $733 (N8) | An extraction design that calls the model more than once per receipt breaks the business case before it breaks anything technical |
| Accessibility of the confidence flag | No number yet: Priya Nair with Maya Chen, by Gate 5 on 2026-10-09 | AC-7 requires a low-confidence field to be visually distinct; distinct by colour alone would fail the reviewers who cannot use it, so the checklist has to run before the reviewer view is final |
| Availability and latency | No number: Priya Nair, by Gate 5 on 2026-10-09. No availability or latency promise is made to anyone outside the team, because there is nobody outside the team | Named so the absence is visible rather than assumed |

Full register: none. No nfr.md is filled for this internal build, and no accessibility checklist either. Gate 2 permits a non-functional target to name the owner who will produce the number by a dated deadline instead of carrying the number, and three rows above use that permission. [os/STAGE-GATES.md](../os/STAGE-GATES.md) names the permanent version of this as its third Gate 2 failure mode: one deferral is a plan, two is a decision to ship without a target. These are the first deferral, and Gate 4 reads this table again.

## 6. Success metrics and instrumentation

| Metric | Type | Instrumented where | Owner | Reviewed when |
|---|---|---|---|---|
| First-submission approval rate, drafted reports | lagging | finance system of record, approval events joined to draft ids; the join does not exist yet (Q1) | Daniel Okafor | first metrics review, four weeks after launch |
| Median filing time, five-receipt report | leading | in-product timing | Maya Chen | first metrics review |
| Share of eligible reports through the draft flow | leading | product analytics | Maya Chen | first metrics review, against the 30% tripwire in section 9 |
| Reviewer-caught extraction errors per 100 drafted reports | guardrail | reviewer flag button | Priya Nair | first metrics review, and watched continuously: under 3, and never silently rising |

Extraction accuracy itself is specified in the eval spec, with a labeled receipt set and a numeric pass threshold; that document, not this table, is what blocks release on model quality.

One row here is not instrumented, and it is the row objective 1 depends on. Finance's approval events carry no draft id today, so first-submission approval on drafted reports cannot be separated from the rest. Building that join is not one of the six functional-scope rows: it is a change inside the finance system, owned by Priya Nair with finance, and it is Q1 in section 12 with a needed-by of Gate 5. Until it lands, objective 1 cannot be read at all, which is why it is an open question with a date rather than a footnote.

## 7. Out of scope

| # | Excluded | Why | Where it went |
|---|---|---|---|
| X1 | Auto-submission of any report | The filer submits, always; this is a load-bearing guardrail, not a v2 candidate. The accountability the expense policy assigns is the reason | Never |
| X2 | Corporate-card feed reconciliation | v1 answers the filing problem, not the matching problem | Backlog |
| X3 | Mileage and per-diem rules | Different rule sets, no interview evidence behind them | Backlog |
| X4 | Filing on behalf of another person, the executive-assistant workflow | A distinct workflow discovery deliberately parked | Backlog, parked in discovery |
| X5 | Any use of expense data to train vendor models | The contract must forbid it; the open vendor-terms gap stays in this PRD until legal confirms the clause | Never. Tracked as A2 and K3 |
| X6 | Multi-receipt capture in one photo | The extraction eval set could not hold a threshold on overlapping receipts (D-2) | Parked on the [roadmap](expense-copilot-roadmap.md), 2026-08-25, with AC-10 defining what happens when a filer tries it anyway |

Exclusions a reader would otherwise assume in are here on purpose: nobody asked for auto-submission, and X1 is the most important row in the document.

## Trade-offs accepted at Gate 2

Not part of the template's numbered spine; kept because the three companion decisions this sitting made, D-2, D-3 and D-4 in the decision log, were taken here and a filled PRD where nothing was given up is not a worked example.

| What we wanted | What we shipped instead | Who paid for it | Why we accepted it |
|---|---|---|---|
| Multi-receipt capture in one photo | One receipt per item | Filers with a stack of restaurant slips, who keep photographing one at a time | The extraction eval set could not hold a threshold on overlapping receipts, and shipping a feature that fails on the messiest real case would have cost trust we need for the rest of it |
| Category suggestion trained on our own corrected mappings from day one | Static policy mapping in v1, admin corrections logged but not fed back | The finance admin, who corrects the same mapping more than once this quarter | The feedback loop needs a review step nobody had capacity to design before the launch window, and an unreviewed loop is how a wrong mapping becomes policy |
| An accuracy target agreed with finance | An ILLUSTRATIVE threshold in the eval spec, revisited after four weeks of live data | The team, who cannot yet say the number is a commitment | We had no baseline for machine extraction on our own receipt mix. Agreeing a number we invented would have made the eval gate look rigorous while measuring nothing |

The third row is the uncomfortable one and it is here on purpose: the honest state at Gate 2 was that one of this document's headline quality bars had no agreed number behind it, and the gate passed anyway, with the gap named, owned, and dated rather than dressed up.

## 8. Launch criteria

Launch is Gate 5, signed per function on 2026-10-09 (N16), and it runs on the delivery and overlay documents, filled for this product.

| # | Criterion | Verified by | Owner |
|---|---|---|---|
| L1 | Every must story passes its acceptance criteria | [acceptance-criteria.md](expense-copilot-acceptance-criteria.md), AC-1 to AC-10 | Maya Chen |
| L2 | Every non-functional row in section 5 carries a number, or a waiver its owner signed | section 5, re-read at Gate 4 | Priya Nair |
| L3 | [Testing strategy](../templates/delivery/testing-strategy.md), [edge-case register](../templates/delivery/edge-cases.md) and [failure scenarios](../templates/delivery/failure-scenarios.md) complete, with the receipt-storage outage rehearsed | the three filled documents | Priya Nair |
| L4 | [UAT](../templates/delivery/uat-plan.md) with named filers and one finance reviewer, exit criteria met | the filled UAT plan | Maya Chen |
| L5 | AI overlay: [eval spec](../templates/ai/eval-spec.md) thresholds met on the labeled receipt set, [guardrails](../templates/ai/guardrails.md) each with an owner and a test, [human approval gates](../templates/ai/human-approval-gates.md) confirming no submission path bypasses the filer, and the [red-team review](../templates/ai/red-team-review.md) closed, including the receipt-as-prompt-injection case | the four filled overlay documents | Priya Nair |
| L6 | [Compliance impact assessment](../templates/operate/compliance-impact-assessment.md) signed: receipts carry personal data, and the vendor-terms answer gates launch | the signed assessment | the legal lead |
| L7 | [Release readiness](../templates/delivery/release-readiness.md) signed per function, with rollback owner and trigger named | the signed pack | Maya Chen |

None of the seven documents above is filled in this chain, which ends at Gate 3; they are named here as the Gate 5 work, not claimed as done. The first [metrics review](../templates/operate/metrics-review.md) is calendared for four weeks after launch, where objective 1 is graded against the finance system and the persist, pivot, or sunset decision is made in writing.

## 9. Kill criteria

| # | We stop or roll back if | Threshold | Checked when | Who calls it | What happens |
|---|---|---|---|---|---|
| K1 | Voluntary adoption does not reach the business case's tripwire | Under 30% of eligible reports through the draft flow | First metrics review, four weeks after launch | Daniel Okafor | Scope growth stops and the persist, pivot or sunset decision is taken in writing, the business case's own wording |
| K2 | The guardrail metric degrades | Reviewer-caught extraction errors at 3 or more per 100 drafted reports | First metrics review, and on any week the reviewer flag rate rises | Priya Nair | The draft flow is turned off for new reports while the extraction path is fixed: a rollback, not a stop |
| K3 | The enabling assumption behind A2 busts | The model vendor will not contract a clause forbidding training on Ledgerline data | Before Gate 5 on 2026-10-09 | Daniel Okafor, on the legal lead's finding | The build does not launch on this vendor. The business case's option 3, a seat-priced capture vendor, is the only alternative on file, and it was put there for a different reason, v1 extraction failing its eval threshold, so reopening it here would be a new decision rather than a plan already made |

K1 and K2 are read at the same review, and they can disagree: high adoption with a rising guardrail is the case the review has to argue about rather than average away. If a criterion fires and the team continues anyway, that decision goes in the decision log with its reasoning; what is not available is having no criterion to fire.

## 10. Four risks, answered

| Risk | Answer, with evidence | Strongest evidence against | Confidence |
|---|---|---|---|
| Value: will they use it | Ten of twelve interviewees named re-typing receipt data as the worst part of filing, unprompted, and about a third of reports bounce on a category rule the filer has never read. Both are exactly what a draft addresses | Nobody in those twelve interviews has used a draft. Wanting a pain removed is not evidence of voluntary adoption, and objective 3 carries no mandate to fall back on | medium |
| Usability: can they use it | The filer keeps the job they already know, reviewing and submitting; the copilot changes what is on the screen when they start, not what they are accountable for | The 25-minute baseline is eight timed sessions, directional at best, and not one of them used a draft. The under-10-minute target has no usability evidence behind it yet | medium |
| Feasibility: can we build it | One receipt per item, four extracted fields, and a never-invent rule keep the model's job narrow enough for Priya Nair's team to build inside the window | Extraction quality on crumpled or foreign-language receipts is unproven, and the eval set could not hold a threshold on overlapping receipts at all. That is why v1 is one receipt per item, and it is a narrowing of the problem, not an answer to it | low; routed to A3 with a validation method and a date |
| Viability: does it work for the business | The business case was approved on 2026-08-14 against run cost of $2,500 a month (N8) and about $1,800 a month of reviewer mechanical checks (N7), with filer time saved carrying the rest | The case's own sensitivity: at 30% adoption instead of 60%, payback runs to about 50 months and the case fails inside its three-year horizon. The model price is also quoted, not contracted (N9) | medium |

## 11. Assumptions

No assumptions-register.md is filled for this internal build, and the business case names that register as where its adoption and rate assumptions belong. Until it exists, this table is that register, which is why it carries the confidence and validation-method columns Gate 2 asks a register for, and not only the template's short index.

| # | The guess this plan is standing on | Impact if wrong | Confidence | How it gets validated | Validate by | Owner |
|---|---|---|---|---|---|---|
| A1 | Adoption reaches 50% of eligible reports by month two with no mandate | The business case fails inside its horizon, and K1 fires | medium | Share of eligible reports through the draft flow, read in product analytics | 2026-11-09, the first metrics review | Maya Chen |
| A2 | The model vendor will contract a clause forbidding training on Ledgerline data | The build does not launch on this vendor: K3 fires | low | The signed contract clause itself, not a sales assurance | 2026-10-09, before Gate 5 | the legal lead |
| A3 | Extraction holds a quality bar on Ledgerline's own receipt mix, including crumpled and foreign-language receipts | Drafts are corrected so heavily that objective 1 does not move even when adoption is high, the exact failure the discovery document warned about | low | The eval spec's labeled receipt set, drawn from Ledgerline's own receipts | 2026-10-09, before Gate 5 | Priya Nair |
| A4 | The quoted model price of about $0.22 a receipt holds at Ledgerline's own volume | Run cost rises above the $2,500 a month the business case carries | medium | A contracted price, at or below the quoted rate, from procurement | 2026-10-09, before Gate 5 | Priya Nair, with procurement |

A2 and A3 are the two rows that can stop the product rather than reshape it, which is why both also appear in section 9.

## 12. Open questions

| # | Question | Blocks | Owner | Needed by |
|---|---|---|---|---|
| Q1 | Can the finance system's approval events be joined to draft ids, so objective 1 can be read at all? | Section 6, and O1 with it | Priya Nair, with finance | 2026-10-09, Gate 5 |
| Q2 | What retention and deletion schedule applies to receipt images? | Section 5, and L6 | the legal lead | 2026-10-09, Gate 5 |
| Q3 | What extraction accuracy threshold does the eval spec commit to, and who agrees it? | L5, and the third row of the trade-off table | Daniel Okafor, with Priya Nair | 2026-11-09, after four weeks of live data (D-4) |
| Q4 | Do the three deferred non-functional rows get numbers, or a waiver their owner signs? | Section 5, and L2 | Priya Nair | 2026-10-09, Gate 5 |

Four questions, under the cap of five. Everything else this document could have listed was either decided and recorded as a trade-off above, or cut and recorded in section 7.

## 13. Companion documents

Read the triggers, record Yes or No with a reason, and open the templates the Yes rows name. The No rows are the record of what was considered and not needed; deleting them would lose that.

| Trigger | Applies here | Why, and what was opened | Stage |
|---|---|---|---|
| Users can lose data, money, or work if this misbehaves | Yes | A misread amount reaches finance if the filer accepts a bad draft; [failure-scenarios.md](../templates/delivery/failure-scenarios.md) is named in L3 | DELIVER |
| The behavior at the boundaries is not obvious from the stories | Yes | Multi-receipt photos and unreadable fields are boundary behavior; [edge-cases.md](../templates/delivery/edge-cases.md) in L3, and AC-3, AC-9 and AC-10 already carry three of them | BUILD into DELIVER |
| Any metric in section 6 is not already instrumented | Yes | The finance join behind objective 1 does not exist; Q1 owns it and [analytics-instrumentation-spec.md](../templates/delivery/analytics-instrumentation-spec.md) is where the event spec goes | DELIVER |
| A support or success team will field questions about this | Yes | Filers will ask the three finance reviewers, so [support-runbook.md](../templates/delivery/support-runbook.md) names who answers what rather than leaving it to whoever replies first | DELIVER |
| Existing users or existing data have to move | No | Nothing migrates: existing reports stay in the finance system untouched and the draft flow only adds a new way to start one | DELIVER |
| This replaces something people currently rely on | No | The manual filing path stays open and unchanged; objective 3 is voluntary adoption precisely because nothing is being taken away | OPERATE |
| Anyone outside the team has to be told it shipped | Yes | Every Ledgerline filer is a user, so [launch-comms-plan.md](../templates/delivery/launch-comms-plan.md) applies even though nobody outside the company hears about it | DELIVER |
| It touches what customers pay for, or what tier they are on | No | An internal tool with no customer, no price and no tier | PLANNING |
| It processes personal data | Yes | Receipts carry personal data; the [compliance impact assessment](../templates/operate/compliance-impact-assessment.md) in L6 is the document this build opens, and Q2 is its open question | DESIGN |
| A regulator, licence condition, or scheme rule is in scope | No | No financial or data regulator applies to an internal expense tool, so the regulated module does not fire (V8). The personal-data work above is handled by L6, not by the module | DEFINE and DELIVER |
| Anyone will use this with a screen reader, a keyboard only, or at low vision | Yes | Filers and reviewers include both; [accessibility-checklist.md](../templates/architecture/accessibility-checklist.md) is not filled for this chain and is named as a gap in section 5 rather than assumed away | DESIGN |
| An availability or latency promise is made to anyone outside the team | No | There is nobody outside the team to promise it to; section 5 records the absence rather than implying a target exists | DELIVER |
| A third party has to ship something for this to work | Yes | The model vendor, on both terms (A2) and price (A4); the dependency register that carries them is drafted in DESIGN, after this document | DESIGN |
| A model produces any part of the output | Yes | The whole draft is model output, so the AI overlay in L5 is part of this spec, not an attachment to it | AI overlay, from DEFINE |
| The business case has not been made anywhere else | No | Made in [ledgerline-business-case.md](ledgerline-business-case.md) and approved at Gate 1 on 2026-08-14; its tripwire is K1 | PLANNING |
| More than one team has to change something | Yes, and no charter | Finance's own system has to expose the join in Q1, so this is not one squad's work. A [program charter](../templates/planning/program-charter.md) was judged heavier than one dependency with a named owner, and the call is recorded here rather than left as a blank row | PLANNING |

## Sign-off

| Role | Name | Date | What they are signing |
|---|---|---|---|
| Product owner | Maya Chen | 2026-08-28 | The problem, the objectives, and the scope boundary |
| Engineering lead | Priya Nair | 2026-08-28 | Feasibility, the deferred non-functional rows in section 5, and the estimate |
| Design lead | none appointed | n/a | This build has no separate design lead. Maya Chen carries the usability evidence in section 10 and the accessibility position in section 5, and that is recorded here rather than smoothed over with a name that does not exist |
| Business sponsor | Daniel Okafor | 2026-08-28 | The business case this PRD spends: the objectives, the ROI logic, and the budget behind them |
| Gate 2 approver | Daniel Okafor | 2026-08-28 | That Gate 2 in [os/STAGE-GATES.md](../os/STAGE-GATES.md) is met. He did not write this document; Maya Chen did |

Every row above is an ILLUSTRATIVE record by a fictional cast, per V8. No real person signed this document, and nothing here should be read as evidence that a review of any kind took place.

---

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Section 0 is under 150 words and a reader who stops there is not misled. It carries the one number, the one exclusion and the stop condition, and names them as such
- [x] "Who implements this" is answered, and if the answer is a model, the AI overlay is attached. A human team builds it; the overlay attaches anyway, because the product contains a model, and it is L5
- [x] Background links to discovery evidence rather than restating it. The interview counts are quoted because they are load bearing; the rest is a link
- [x] Every objective has metric, baseline, and target, and no target is still ILLUSTRATIVE. O1 and O3 are discovery's two signals, agreed with Daniel Okafor on 2026-08-12; O2's target is its own metric owner's, on a baseline section 2 labels directional. The one unagreed number in this product is the eval threshold, which is Q3, not an objective
- [x] Every must story carries an acceptance criteria ID. All five rows in section 3, and all ten criteria AC-1 to AC-10 appear there
- [x] Functional scope rows each trace to a story. Each of REQ-1 to REQ-6 names the story it serves, and section 3 keys its rows by the same ids
- [x] At least one guardrail metric is named, with an owner and an instrumented source. Reviewer-caught extraction errors per 100 drafted reports, Priya Nair, from the reviewer flag button
- [x] Out of scope names the exclusions a reader would otherwise assume in. X1 is the one nobody asked about, and it is the row that matters most
- [x] Launch criteria are all checkable, each with an owner. Seven rows, each naming the artifact that verifies it; none of those artifacts is claimed to exist yet
- [x] At least one kill criterion has a threshold, a check point, and a named caller. All three do
- [x] All four risks carry an answer, counter-evidence, and a confidence level. No counter-evidence cell says "none"
- [x] Every low-confidence risk and open question has an owner and a date. Feasibility is low and routes to A3, dated 2026-10-09; Q1 to Q4 each carry both
- [x] Open questions number five or fewer, and the rest have been routed. Four, with the rest recorded as trade-offs or as section 7 cuts
- [x] Every load-bearing assumption has a validate-by date. A1 to A4, each with a date and a method, because no separate register exists to hold them
- [x] The companion table has been read and the triggered rows opened. Section 13 records Yes or No with a reason on all sixteen rows; the triggered documents are named in section 8, and every one of them that is not filled for this chain is named as a gap rather than assumed done
- [x] [spec-review](../skills/spec-review/SKILL.md) has run and no blocking finding is outstanding. It ran in the Gate 2 sitting on 2026-08-28; its three findings are the trade-offs recorded above, D-2, D-3 and D-4, each accepted in writing rather than left open
- [x] If the product contains an AI or machine-learning feature and a regulator applies to it, the regulated module template is in use as shipped. N/A: the product contains a model and no financial or data regulator applies to an internal expense tool, so the overlay does not fire (V8)
- [x] The sign-off block names real people, and the Gate 2 approver did not write this document. Within the fiction it names this chain's cast, and the Gate 2 approver is Daniel Okafor, not the author. In the repository they are invented people, which the header states outright

This PRD closes at Gate 2 alongside the [vision](expense-copilot-vision.md), the [product strategy](expense-copilot-product-strategy.md), the [roadmap](expense-copilot-roadmap.md) and the [acceptance criteria](expense-copilot-acceptance-criteria.md) (V8), and it is one of the artifacts the development handoff carries when DESIGN closes at Gate 3.
