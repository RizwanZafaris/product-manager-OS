---
layer: templates
stage: DEFINE
gate: 2
feeds: []
method: "knowledge/cagan-product-teams.md"
aliases: ["One-Pager"]
---
# One-Pager: [feature or change name]

Stage: DEFINE, feeds Gate 2 (requirements signed off)
Knowledge: [Cagan on product teams](../../knowledge/cagan-product-teams.md)
Skill: [write-prd](../../skills/write-prd/SKILL.md); [ai-prd](../../skills/ai-prd/SKILL.md) when the product contains a model

<!-- The light weight of the DEFINE stage. Use it when one squad ships a real
     user-facing change over a few sprints and one or two stakeholders must not be
     surprised. Anything heavier than that belongs in prd.md; anything lighter
     belongs in a ticket. ../../os/WHICH-DOCUMENT.md picks between them.

     Fill these three fields first, in this order: the problem in section 1, the
     one metric in section 4, and the not-doing list in section 5. A one-pager with
     those three answered is useful even if nothing else is filled in.

     Delete any section you do not need. An empty section is worse than no
     section: it reads as an unanswered question. Write "N/A because <reason>"
     where the honest answer is that the section does not apply here.

     This document must stay on one page. When it stops fitting, that is the
     signal to promote it to prd.md, not to shrink the font. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved
**Reviewers who must not be surprised:** [names, one line]

## 1. Problem

[Two or three sentences in the user's terms, with one piece of evidence and its source ID. Link the discovery work rather than restating it; the source of truth is the filled copy of ../discovery/discovery-document.md.]

## 2. Proposal

[Three or four sentences: what changes for the user, stated so an engineer and a support lead read it the same way. No implementation detail that the team has not already agreed.]

## 3. Scope

| # | In scope, one line each | Story or ticket |
|---|---|---|
| 1 | | |
| 2 | | |

## 4. How we will know it worked

| Metric | Baseline | Target | Measured where | Owner |
|---|---|---|---|---|
| | | | | |
| Guardrail: what this must not damage | | must not worsen | | |

<!-- One outcome metric and one guardrail is the floor. Targets nobody has agreed
     with the metric owner are labeled ILLUSTRATIVE until they are agreed. -->

## 5. Not doing

[Three to five lines. The adjacent things people will assume are included, and the one-line reason each is out. This section is why a one-pager can be short.]

## 6. Acceptance

<!-- Even at this weight, every "must" needs a condition that can fail. Given /
     when / then blocks live in acceptance-criteria.md if there are more than
     three; up to three, write them here. -->

| # | Given, when, then | Owner |
|---|---|---|
| AC1 | | |

## 7. Risks and open questions

| # | Risk or question | Owner | Needed by |
|---|---|---|---|
| | | | |

<!-- If the product contains a model, the AI overlay still applies at this weight:
     an eval row from ../ai/eval-spec.md replaces any prose criterion about model
     output. If a financial or data regulator governs the product, stop and use
     the regulated module instead: ../../modules/regulated/README.md. -->

---

## Exit gate (feeds Gate 2: requirements signed off)

- [ ] The problem cites evidence with a source ID rather than asserting it
- [ ] One outcome metric and one guardrail metric, each with a baseline and an owner
- [ ] The not-doing list is written and the reviewers have read it
- [ ] Every must has an acceptance criterion that can fail
- [ ] Every risk and open question has an owner and a date
- [ ] It still fits on one page, or it has been promoted to [prd.md](prd.md)
