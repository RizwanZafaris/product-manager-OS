# Decision Log: Expense Copilot

Fills [templates/execution/decision-log.md](../templates/execution/decision-log.md). Everything here is invented and ILLUSTRATIVE: Ledgerline, its people and every date and figure below are fiction, drawn from [expense-copilot-journey.md](expense-copilot-journey.md)'s data sheet (D-1 to D-6) and [ledgerline-journey.md](ledgerline-journey.md)'s N-rows, not a record of any real expense-tool decision. See the [examples index](README.md).

**Initiative:** Expense Copilot, internal v1 · **Log owner:** Maya Chen · **Started:** 2026-08-14
**Entries:** 6 · **Open reversals:** 0 · **Last entry:** 2026-09-08
**Status:** read in full at Gate 3, 2026-09-11 (V12, V16)

Stage: all stages, read at every gate in [STAGE-GATES](../os/STAGE-GATES.md)
Knowledge: [knowledge index](../knowledge/INDEX.md)
Skill: [decision-memo](../skills/decision-memo/SKILL.md)

## 1. Index

Newest first, so a reader finds the entry in a glance and reads section 3 only for the one that matters. ID numbers come from [expense-copilot-journey.md](expense-copilot-journey.md)'s shared identifiers, not from dates; D-2, D-3 and D-4 share one date, 2026-08-28, the Gate 2 sitting where vision, strategy, roadmap, PRD and acceptance criteria were all approved together (V8), and are listed newest-first by id within that tie since the sheet gives no finer order for one sitting.

| ID | Decision, in one line | Date | Decider | Type | Status |
|---|---|---|---|---|---|
| D-6 | Defer the AI overlay's guardrails, eval spec and red-team review to the PRD's existing Gate 5 launch criteria rather than duplicate them at Gate 3 | 2026-09-08 | Maya Chen | scope | holding |
| D-5 | Post-launch backlog: fund row 4 (per-diem rules) ahead of row 3 (corporate-card feed matching) despite row 3's higher RICE score | 2026-09-01 | Maya Chen | sequencing | holding |
| D-4 | Ship with an ILLUSTRATIVE accuracy threshold in the eval spec, not a finance-agreed number | 2026-08-28 | Daniel Okafor | metric | holding |
| D-3 | Ship a static policy mapping in v1; admin corrections are logged but not fed back into suggestions | 2026-08-28 | Maya Chen | scope | holding |
| D-2 | Ship one receipt per item in v1, not multi-receipt capture in one photo | 2026-08-28 | Maya Chen | scope | holding |
| D-1 | GO: proceed from DISCOVER into DEFINE | 2026-08-14 | Daniel Okafor | scope | holding |

## 2. When to log, and when not to

Applied to this initiative since Gate 1 on 2026-08-14 (D-1): an entry earns a row when it closed off an option that cost something to give up, not when it merely recorded a task.

| Log it | Do not log it |
|---|---|
| Two or more people debated it for over ten minutes | It was never in question |
| Anyone could reasonably reopen it in three months | It is a task, and the tracker already holds it |
| It closed off an option that cost something to give up | It restates something already decided; link the original instead |
| A new joiner would otherwise ask "why is it like this?" | It changes system structure, which belongs in an [ADR](../templates/architecture/adr.md) |
| It was decided under time pressure or with thin evidence | It is a preference nobody will act on |

**Log within a day of deciding.** Every entry below is dated the same day as its decision, per the journey's own Decision log table.

## 3. Decisions

ADR-0001 (expense-copilot-adr.md, not yet written), accepted 2026-09-03 per V9, never earned a row here: it is structural, the receipt-pipeline call, and D-2 below is the scope half of the same decision, filed once as an ADR rather than duplicated. D-2's entry names the ADR rather than restating its content.

### D-6: Defer the AI overlay's guardrails, eval spec and red-team review to the PRD's existing Gate 5 launch criteria rather than duplicate them at Gate 3

- **Date:** 2026-09-08 · **Decider:** Maya Chen
- **Type:** scope
- **Context:** the DESIGN-stage premortem on 2026-09-08 (V14), the same review that seeded the dependency and risk registers, raised whether the guardrails, eval spec and red-team review the PRD's Launch criteria already names for Gate 5 should also be drafted, in a lighter form, at Gate 3.
- **Options considered:** A. draft lighter versions of the eval spec, guardrails and red-team review now, at Gate 3; B. defer all three to the PRD's own Gate 5 launch criteria, unduplicated; C. draft only the eval spec now and defer the other two.
- **Decision and rationale:** B. [expense-copilot-prd.md](expense-copilot-prd.md)'s Launch criteria section already names the eval spec, guardrails, human approval gates and red-team review as Gate 5 documents, filled for this product; duplicating any of them in a lighter form at Gate 3 would create two documents that could disagree about the same guardrail. Given up: a Gate 3 rehearsal of the AI overlay that might have caught a guardrail gap before Gate 5 does.
- **Evidence it rested on:** [expense-copilot-prd.md](expense-copilot-prd.md)'s own Launch criteria section, which already names these four documents for Gate 5, due 2026-10-09 per N16; the 2026-09-08 premortem that raised the question (V14).
- **What would change our mind:** a Gate 3 reviewer finding a specific guardrail gap the dependency or risk register cannot hold until Gate 5.
- **Reverses or is reversed by:** none
- **Who was told:** the DESIGN-stage premortem attendees, 2026-09-08; carried into the development handoff (expense-copilot-development-handoff.md, not yet written), drafted 2026-09-10 per V15.

### D-5: Post-launch backlog: fund row 4 (per-diem rules) ahead of row 3 (corporate-card feed matching) despite row 3's higher RICE score

- **Date:** 2026-09-01 · **Decider:** Maya Chen
- **Type:** sequencing
- **Context:** [ledgerline-rice-scoring.md](ledgerline-rice-scoring.md), written the same day, scored row 3, corporate-card feed matching, above row 4, per-diem rules, in its Step 3 table, but row 3's confidence sits at opinion-level for a four-month effort.
- **Options considered:** A. fund row 3 first, following the RICE score as ranked; B. fund row 4 first, on the confidence gap behind row 3's score; C. fund neither until both scores are revisited.
- **Decision and rationale:** B. A higher RICE score resting on opinion-level confidence for a four-month effort is not a ranking to spend the first post-launch slot on unquestioned; row 4 is both in the PRD's own Out of scope list, corporate-card feed reconciliation and per-diem rules, and the smaller commitment. Given up: whatever lead row 3 would have banked by shipping first, and the RICE ranking's own stated order.
- **Evidence it rested on:** [ledgerline-rice-scoring.md](ledgerline-rice-scoring.md)'s Step 3 table, rows 3 and 4.
- **What would change our mind:** a two-week count of reports carrying a card line, the condition the journey's data sheet names as what reopens this call.
- **Reverses or is reversed by:** none
- **Who was told:** the core team, 2026-09-01.

### D-4: Ship with an ILLUSTRATIVE accuracy threshold in the eval spec, not a finance-agreed number

- **Date:** 2026-08-28 · **Decider:** Daniel Okafor
- **Type:** metric
- **Context:** at the Gate 2 sitting, [expense-copilot-prd.md](expense-copilot-prd.md)'s Trade-offs accepted table named this the uncomfortable row on purpose: the team had no baseline for machine extraction on Ledgerline's own receipt mix, so no accuracy number agreed with finance existed to put in the eval spec.
- **Options considered:** A. agree a number with finance now, even without a baseline; B. ship with an ILLUSTRATIVE threshold in the eval spec, revisited after four weeks of live data; C. hold Gate 2 until a baseline exists.
- **Decision and rationale:** B. Agreeing a number invented to fill the field would have made the eval gate look rigorous while measuring nothing, per the PRD's own account of this trade-off; holding Gate 2 for a baseline that requires live receipts traded a real slip in schedule for a number the team could get from four weeks of production data instead. Given up: an agreed finance number at Gate 2, and the appearance that this headline quality bar had a commitment behind it from day one.
- **Evidence it rested on:** [expense-copilot-prd.md](expense-copilot-prd.md)'s Trade-offs accepted table, row 3, and its Launch criteria's eval spec reference.
- **What would change our mind:** four weeks of live extraction data, the same window the PRD calendars its first metrics review for, giving finance a real number to agree to.
- **Reverses or is reversed by:** none
- **Who was told:** the Gate 2 sitting, 2026-08-28, signed by Maya Chen, Priya Nair and Daniel Okafor (V8).

### D-3: Ship a static policy mapping in v1; admin corrections are logged but not fed back into suggestions

- **Date:** 2026-08-28 · **Decider:** Maya Chen
- **Type:** scope
- **Context:** [expense-copilot-prd.md](expense-copilot-prd.md)'s Trade-offs accepted table weighed a category suggestion trained on Ledgerline's own corrected mappings from day one against a static mapping with corrections merely logged.
- **Options considered:** A. train suggestions on corrected mappings from day one; B. ship a static mapping in v1, log corrections, feed them back in a later release; C. give the finance admin no correction capability in v1.
- **Decision and rationale:** B. The feedback loop needed a review step nobody had capacity to design before the launch window, and an unreviewed loop is how a wrong mapping becomes policy, per the PRD's own account; giving the admin no correction capability at all left every future bounce on the same rule REQ-6 exists to fix. Given up: a mapping that improves itself inside v1; the finance admin who corrects the same mapping more than once this quarter pays for it, per the PRD.
- **Evidence it rested on:** [expense-copilot-prd.md](expense-copilot-prd.md)'s Trade-offs accepted table, row 2, and its Functional scope row 6.
- **What would change our mind:** capacity to design the review step the feedback loop needs, opening in a later release.
- **Reverses or is reversed by:** none
- **Who was told:** the Gate 2 sitting, 2026-08-28 (V8).

### D-2: Ship one receipt per item in v1, not multi-receipt capture in one photo

- **Date:** 2026-08-28 · **Decider:** Maya Chen
- **Type:** scope
- **Context:** [expense-copilot-prd.md](expense-copilot-prd.md)'s Trade-offs accepted table weighed multi-receipt capture in one photo, what filers with a stack of receipts wanted, against the extraction eval set's inability to hold a threshold on overlapping receipts.
- **Options considered:** A. ship multi-receipt capture in v1; B. ship one receipt per item, filers photograph one at a time; C. delay v1 until the eval set can score overlapping receipts.
- **Decision and rationale:** B. Shipping a feature that fails on the messiest real case would have cost trust the rest of the product needs, per the PRD's own account; delaying v1 for an eval set that does not yet exist traded a real launch date for a capability nobody had scoped. Given up: a faster filing path for filers with a stack of restaurant slips, who keep photographing one at a time instead. The architectural half of this call, one model call per receipt, matched to one photo or one forwarded-email attachment, is filed once as ADR-0001 (expense-copilot-adr.md, not yet written), accepted 2026-09-03 (V9), linked rather than duplicated here.
- **Evidence it rested on:** [expense-copilot-prd.md](expense-copilot-prd.md)'s Trade-offs accepted table, row 1, and its Functional scope row 1's own note, "one receipt per item in v1."
- **What would change our mind:** an extraction eval set that can hold a threshold on overlapping receipts.
- **Reverses or is reversed by:** none
- **Who was told:** the Gate 2 sitting, 2026-08-28 (V8).

### D-1: GO: proceed from DISCOVER into DEFINE

- **Date:** 2026-08-14 · **Decider:** Daniel Okafor
- **Type:** scope
- **Context:** discovery ran from the problem framing drafted 2026-08-13 (V1) to the GO on 2026-08-14 (V2), the same window [ledgerline-business-case.md](ledgerline-business-case.md) was written and approved at Gate 1.
- **Options considered:** A. GO, proceed into DEFINE; B. run more discovery before committing; C. stop, the trigger does not justify a build.
- **Decision and rationale:** A. [expense-copilot-discovery.md](expense-copilot-discovery.md)'s own Go or no-go section closed with a GO; the journey's shared identifiers name Daniel Okafor as sponsor and this entry's decider, with Maya Chen as product owner co-signing the same Gate 1 (V2). Given up: the option to run a second discovery pass before committing engineering time to DEFINE.
- **Evidence it rested on:** [expense-copilot-discovery.md](expense-copilot-discovery.md)'s Go or no-go section; [ledgerline-business-case.md](ledgerline-business-case.md), written the same window.
- **What would change our mind:** a discovery finding that the trigger, support tickets tagged "expenses," did not describe a problem worth solving.
- **Reverses or is reversed by:** none
- **Who was told:** Gate 1, 2026-08-14, signed by Maya Chen and Daniel Okafor (V2).

---

## 4. How this log fails

| Failure mode | What it looks like | The rule |
|---|---|---|
| Winners only | Every entry lists what was chosen and no option that lost | An entry with no losing option is an announcement, not a decision. Reject it at review |
| Committee as decider | "The team decided", or three names in the decider field | Exactly one name. A group can agree; only a person can be asked why |
| Edited history | An old entry now describes what the team currently believes | Entries are immutable. A change of mind is a new id that names the old one |
| Rationale is the outcome | "We chose A because A was better" | The rationale names the trade: what A cost, and why that cost was acceptable |
| Silent staleness | Entries from two strategies ago, all still marked holding | Review status at every gate. Mark superseded by circumstance rather than leaving it |
| Log kept by one person | Entries stop when that person is on leave | The owner is named, and the review is on a recurring agenda, not in someone's memory |
| Nobody was told | A correct decision that half the team acts against | "Who was told" is a required field, and blank means the decision has not landed yet |

Applied to this log: winners only was not observed, every entry above names at least two options that lost. Committee as decider was not observed: each entry keeps exactly one named decider, Daniel Okafor for D-1 and D-4, Maya Chen for D-2, D-3, D-5 and D-6, even where more than one person signed the gate the decision fed (D-1, D-4). Rationale is the outcome was not observed: every entry states what was given up, not only that the chosen option was better. Edited history was not observed: all six entries are original here, none rewrites an earlier one. Silent staleness: D-1 to D-6 were reviewed at Gate 3 on 2026-09-11 (V16), where none was marked superseded, see section 5. Log kept by one person is a real exposure here, not a false one: Maya Chen owns every entry in this log except the two Daniel Okafor decided, and the mitigation is that status is reviewed at every gate rather than resting in anyone's memory. Nobody was told was not observed: every entry names who was told.

## 5. Gate review

| Gate | Reviewed on | Entries still holding | Marked superseded | New reversals |
|---|---|---|---|---|
| Gate 1 | 2026-08-14 | 1 (D-1) | 0 | 0 |
| Gate 2 | 2026-08-28 | 4 (D-1 to D-4) | 0 | 0 |
| Gate 3 | 2026-09-11 | 6 (D-1 to D-6) | 0 | 0 |

No entry has been marked superseded by circumstance. D-1 holds: the internal build remains the initiative Gate 3 closes toward a development-ready handoff, and nothing since has questioned entering DEFINE. D-2 and D-3 hold: both are v1 scope calls about receipt capture and category mapping that the DESIGN-stage artifacts, the data model (V10) and the API contract (V11), build on rather than revisit. D-4 holds: the ILLUSTRATIVE threshold it accepted is still the PRD's own answer, unrevised before the first metrics review the PRD calendars four weeks after launch, a date past this journey's Gate 3 close. D-5 holds: its own reopening condition, a two-week count of reports carrying a card line, cannot fire before go-live, so it stands unchanged through Gate 3. D-6 holds: Gate 3 itself is the review that closed it, the same day this log was last reviewed.

## Exit gate

- [x] Every entry has a matching index row, and every index row has an entry: D-1 to D-6 in both section 1 and section 3.
- [x] Every entry has exactly one decider, by name: Daniel Okafor (D-1, D-4), Maya Chen (D-2, D-3, D-5, D-6).
- [x] Every entry lists the options that lost, not only the winner: three options in every entry above.
- [x] Every rationale names what was given up, not only what was gained: stated in every entry.
- [x] Every entry records the evidence it rested on, or says plainly that it was judgment: every entry cites a dated artifact, the discovery document, the business case, the PRD's Trade-offs table, the premortem or the RICE sheet.
- [x] Every entry names what would change our mind: stated in every entry.
- [x] No entry has been edited into a different decision; reversals are new ids: none of D-1 to D-6 reverses another.
- [x] Entry dates are within a day or two of the decisions they record: every entry is dated the day of the decision, per the journey's own Decision log table.
- [x] Status has been reviewed at the most recent gate, and stale entries are marked superseded rather than left holding: reviewed 2026-09-11 in section 5; none found stale, with the reasoning stated rather than assumed.
- [x] Structural technology decisions are in [ADRs](../templates/architecture/adr.md), linked rather than duplicated here: ADR-0001 (expense-copilot-adr.md, not yet written) is named in D-2's entry, in plain text since the file does not yet exist in this repository, and is not duplicated here.
- [x] The worked example above has been removed: no worked micro-example appears in this file.

Reviewed and current as of 2026-09-11: Maya Chen, log owner, at Gate 3 (V16).
