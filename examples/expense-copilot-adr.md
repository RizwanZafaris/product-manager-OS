# ADR 0001: Extract fields from one receipt per model call, never batch multiple receipts into one call

Fills [templates/architecture/adr.md](../templates/architecture/adr.md). Everything here is invented: Ledgerline is the fictional mid-market software company of [ledgerline-journey.md](ledgerline-journey.md) and [expense-copilot-journey.md](expense-copilot-journey.md), the Expense Copilot is its fictional internal expense tool, every person named below is fictional, and every number, date and identifier is ILLUSTRATIVE, carried from those two data sheets rather than from any real receipt-processing system. See the [examples index](README.md).

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md)
Knowledge: [knowledge index](../knowledge/INDEX.md)
Skill: [architect agent](../agents/architect-agent.md)

**Status:** Accepted · **Date:** 2026-09-03 · **Deciders:** Priya Nair, Engineering Lead; Maya Chen, Product Manager

## Context

The Expense Copilot drafts a line item, merchant, date, amount and currency, from a photographed or forwarded receipt (REQ-1, REQ-2), so a filer can accept, edit or reject it rather than retype it (AC-1, AC-2). Filers commonly hold more than one receipt at a time, a stack of restaurant slips being the PRD's own example, and the team's first instinct was to let one model call read a whole photographed stack at once. The extraction eval set built for this slice could not hold a threshold on overlapping receipts in a single image, the same limit the PRD's Trade-offs accepted table records against multi-receipt capture, and the same call the decision log already made at D-2: ship one receipt per item in v1, not multi-receipt capture in one photo. The PRD's never-invent rule, [templates/ai/hallucination-controls.md](../templates/ai/hallucination-controls.md), already binds field extraction: a field the model cannot read stays blank and flagged rather than guessed (AC-3), and that rule is easiest to keep honest when one call has exactly one receipt to answer for. REQ-1 covers ingestion of a photo or a forwarded email, and AC-10 requires a photo carrying more than one receipt to be rejected back to the filer with a per-receipt prompt rather than silently drafted, so the pipeline needs a rule for exactly this case before it ships.

## Decision

We will extract fields from one receipt per model call, matched to one uploaded photo or one forwarded-email attachment. We will not batch multiple receipts into a single extraction call.

## Consequences

- A field the model cannot read on that one receipt stays blank and flagged rather than guessed, per the PRD's never-invent rule (AC-3), so the extraction eval set only ever has to hold a threshold on one receipt at a time.
- Filers with a stack of receipts photograph and submit one at a time, per the PRD's Trade-offs accepted table; this is the cost the PRD already named for the filer, not a new one.
- A photo carrying more than one receipt is rejected back to the filer with a per-receipt prompt (AC-10) rather than drafted from a guess at which receipt was meant.
- If monthly receipt volume outgrows the internal baseline, one model call per receipt raises cost or latency rather than amortizing across a batch; this is tracked as RV-4 in the risk register (expense-copilot-risk-register.md, not yet written).

---

### Rejected option: batch multiple receipts into a single extraction call

Reading a whole photographed stack in one model call was the team's first instinct, because it would spare a filer with several receipts from a photograph, review, repeat loop. It lost on the same ground the PRD's Trade-offs accepted table already recorded for v1: the extraction eval set could not hold a threshold on overlapping receipts in a single image, so a batched call had no agreed way to say it had passed. Shipping a feature that fails on the messiest real case, several overlapping receipts in one frame, would have cost trust the rest of the copilot needs. This is the same option the decision log rejected at D-2; this ADR gives it its architectural half rather than reopening it. It is not reopened by this ADR.

## Exit gate

- [x] The title states the decision, not the topic: "Extract fields from one receipt per model call, never batch multiple receipts into one call", not "Receipt extraction pipeline"
- [x] Status, date, and deciders are filled in: Accepted, 2026-09-03, Priya Nair and Maya Chen
- [x] Context explains the forces, not just the requirement: the eval set's limit on overlapping receipts, the never-invent rule, and REQ-1, REQ-2 and AC-10's own text
- [x] The decision is one or two sentences in active voice: "We will extract fields from one receipt per model call... We will not batch multiple receipts into a single extraction call."
- [x] At least one negative consequence is recorded: filers photograph one receipt at a time, and RV-4's cost or latency exposure if volume outgrows the internal baseline
- [x] If this supersedes an earlier ADR, that ADR's status line now points here: not applicable; ADR-0001 is this product's first architecture decision record

Reviewed at [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md) as part of the whole DESIGN set and accepted 2026-09-11. Signed off by Maya Chen, Product Manager and product owner, and Priya Nair, Engineering Lead, signing as architect or senior engineer and, this build carrying no separate security lead, as security reviewer too. See [expense-copilot-journey.md](expense-copilot-journey.md) for how this decision reached Gate 3, and [ledgerline-journey.md](ledgerline-journey.md) for the shared figures it draws on.
