# Development Handoff: Expense Copilot

Fills [templates/architecture/development-handoff.md](../templates/architecture/development-handoff.md). Part of the [Ledgerline Expense Copilot journey](expense-copilot-journey.md): the internal v1 Ledgerline's own finance team commissioned for Ledgerline's own filers, from the understood problem to a development-ready handoff at Gate 3. Everything here is invented and ILLUSTRATIVE, drawn from that journey's data sheet and from [ledgerline-journey.md](ledgerline-journey.md)'s data sheet; no figure is a target to copy. See the [examples index](README.md).

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md)
Knowledge: [knowledge index](../knowledge/INDEX.md)
Skill: [architect agent](../agents/architect-agent.md)

**Handoff owner:** Maya Chen, Product Manager · **Prepared:** 2026-09-10 (V15)

This is the package DESIGN hands to BUILD at Gate 3: every section below points at one of the other thirteen artifacts in this chain, at the revision Gate 3 approved (V15, V16), so nothing here is copied out of them and nothing here can drift from them unnoticed. Ledgerline's internal build carries no separate security lead; Priya Nair signs both Gate 3's architect and security-reviewer lines herself, a fact this package names rather than smooths over, the same way [expense-copilot-risk-register.md](expense-copilot-risk-register.md) and [expense-copilot-dependency-register.md](expense-copilot-dependency-register.md) already do.

## 1. Problem

Link: [expense-copilot-problem-framing.md](expense-copilot-problem-framing.md)
Link: [expense-copilot-discovery.md](expense-copilot-discovery.md)

The problem framing (V1) carries the evidenced problem and the cost of inaction; the discovery document carries the GO that closed Gate 1 (V2). Between them they hold the trigger, the target user and the hypothesis this build answers, at the revision Gate 1 approved.

## 2. Vision and strategy

Link: [expense-copilot-vision.md](expense-copilot-vision.md)
Link: [expense-copilot-product-strategy.md](expense-copilot-product-strategy.md)

The vision (V3) carries the future state this release moves toward; the product strategy (V4) carries the bets it makes and the guiding policy behind them. Both were approved at Gate 2 alongside the PRD and the roadmap (V8).

## 3. Outcomes and success measures

Link: [expense-copilot-roadmap.md](expense-copilot-roadmap.md)

The roadmap (V5) carries the objectives each Now and Next initiative serves, with a baseline and a target on each success-metric row. No separate OKR sheet exists for this internal build; OKR and north-star instances for the internal v1 are out of scope for this chain, so the roadmap is this section's whole source rather than one of two.

## 4. Scope and exclusions

Link: [expense-copilot-prd.md](expense-copilot-prd.md)

The PRD, Version 2, is the document signed at Gate 2 (V6, V8). Its Functional scope table carries what ships, REQ-1 to REQ-6, and its Out of scope section carries what was deliberately left out.

## 5. Requirements and acceptance criteria

Link: [expense-copilot-prd.md](expense-copilot-prd.md)
Link: [expense-copilot-acceptance-criteria.md](expense-copilot-acceptance-criteria.md)

The PRD carries the signed requirements, REQ-1 to REQ-6; the acceptance criteria (V7) carry AC-1 to AC-10, each verifying one REQ id, approved the same Gate 2 sitting (V8).

## 6. Evidence and decisions

Link: [expense-copilot-decision-log.md](expense-copilot-decision-log.md)
Link: [expense-copilot-adr.md](expense-copilot-adr.md)

The decision log (V12) carries D-1 to D-6, read in full at Gate 3; ADR-0001 (V9) carries the receipt-pipeline decision that the decision log's D-2 entry names rather than restates.

## 7. Dependencies

Link: [expense-copilot-dependency-register.md](expense-copilot-dependency-register.md)

The dependency register (V13) carries DEPV-1 to DEPV-4, each with an owner and a needed-by date, drafted at the same 2026-09-08 review that ran the premortem.

## 8. Interface and data contracts

Link: [expense-copilot-data-model.md](expense-copilot-data-model.md)
Link: [expense-copilot-api-contract.md](expense-copilot-api-contract.md)

The data model (V10) carries the five entities and their relationships; the API contract (V11) carries the six resources, one set per REQ id that needs an endpoint. Both were drafted the same day, 2026-09-05.

## 9. Unresolved risks and constraints

Link: [expense-copilot-risk-register.md](expense-copilot-risk-register.md)

The risk register (V14) carries RV-1 to RV-4, scored from the 2026-09-08 premortem run with the premortem worksheet, each an open risk carried forward on purpose rather than closed by omission.

## Development-ready check

Every section above links at least one artifact from this journey, and none carries a `Gap:` line: section 1 links the problem framing and the discovery document; section 2 links the vision and the product strategy; section 3 links the roadmap; section 4 and section 5 both link the PRD, and section 5 also links the acceptance criteria; section 6 links the decision log and the ADR; section 7 links the dependency register; section 8 links the data model and the API contract; section 9 links the risk register. Every one of those thirteen files exists in this journey today, so every link above resolves in the workspace.

Gate 1 was GO on 2026-08-14, decided by Maya Chen and Daniel Okafor (V2). Gate 2 was SIGNED on 2026-08-28, by Maya Chen, Priya Nair and Daniel Okafor, approving the vision, the product strategy, the roadmap, the PRD and the acceptance criteria together (V8). Gate 3 was REVIEWED AND ACCEPTED on 2026-09-11, by Maya Chen as product owner and Priya Nair as architect or senior engineer and, this build carrying no separate security lead, as security reviewer too (V16). All three approvals are fictional sign-offs by this chain's own cast, and none is stale as of this Gate 3 date.

This package is development ready: Gate 1, Gate 2 and Gate 3 are all approved and none is stale; every section above is linked to a real file in this journey; and no section carries a `Gap:` line.

**Reviewed by:** Maya Chen, Product Manager, and Priya Nair, Engineering Lead · **Review date:** 2026-09-11

## Approval

- Gate 1, DISCOVER, GO, 2026-08-14: Maya Chen, Product Manager, product owner; Daniel Okafor, Finance Lead, sponsor. Fictional sign-off, per V2.
- Gate 2, DEFINE, SIGNED, 2026-08-28: Maya Chen, Product Manager; Priya Nair, Engineering Lead; Daniel Okafor, Finance Lead, business sponsor. Fictional sign-off, per V8.
- Gate 3, DESIGN, REVIEWED AND ACCEPTED, 2026-09-11: Maya Chen, Product Manager, product owner; Priya Nair, Engineering Lead, architect or senior engineer and security reviewer, this build carrying no separate security lead. Fictional sign-off, per V16.

Full journey: [expense-copilot-journey.md](expense-copilot-journey.md); shared figures: [ledgerline-journey.md](ledgerline-journey.md).
