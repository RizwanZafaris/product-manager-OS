---
layer: templates
stage: DESIGN
gate: 3
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Development Handoff", "development-handoff"]
---
# Development Handoff: `<product or release name>`

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md)
Knowledge: [knowledge index](../../knowledge/INDEX.md)
Skill: [architect agent](../../agents/architect-agent.md)

This is the development-ready package handed to engineering at the DESIGN exit. Each section points to the workspace artifact that carries the detailed content so the handoff is link complete instead of text complete.
A section with no source says so on a line starting `Gap:`, and a section that does not apply says why on a line starting `N/A because`.

## 1. Problem

Link: [problem-framing.md](../discovery/problem-framing.md)
Link: [discovery-document.md](../discovery/discovery-document.md)

## 2. Vision and strategy

Link: [vision.md](../planning/vision.md)
Link: [product-strategy.md](../planning/product-strategy.md)

## 3. Outcomes and success measures

Link: [roadmap.md](../planning/roadmap.md)
Link: [okrs.md](../planning/okrs.md)

## 4. Scope and exclusions

Link: [prd.md](../definition/prd.md), [one-pager.md](../definition/one-pager.md), or [brd.md](../definition/brd.md)

## 5. Requirements and acceptance criteria

Link: [prd.md](../definition/prd.md), [one-pager.md](../definition/one-pager.md), or [brd.md](../definition/brd.md) (whichever was signed at Gate 2)
Link: [acceptance-criteria.md](../definition/acceptance-criteria.md)

## 6. Evidence and decisions

Link: [decision-log.md](../execution/decision-log.md)
Link: [adr.md](adr.md)

## 7. Dependencies

Link: [dependency-register.md](../execution/dependency-register.md)

## 8. Interface and data contracts

Link: [api-contract.md](api-contract.md)
Link: [data-model.md](data-model.md)

## 9. Unresolved risks and constraints

Link: [risk-register.md](../execution/risk-register.md)
Link: [premortem-worksheet.md](../../frameworks/execution/premortem-worksheet.md)

## Development-ready check

- Gate 1, Gate 2, and Gate 3 are approved and none are stale.
- Every section links a workspace artifact or has an `N/A because` line.
- No section has a `Gap:` line.
- Every linked path resolves in the workspace.
