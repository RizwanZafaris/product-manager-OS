# Product Requirements Document: [feature or product name]

Stage: DEFINE, feeds Gate 2 (requirements signed off)
Knowledge: [Cagan on product teams](../../knowledge/cagan-product-teams.md)
Skill: [ai-prd](../../skills/ai-prd/SKILL.md)

> **Delete any section you do not need.** This template is a superset, not a form. An empty section is worse than no section: it reads as an unanswered question and it teaches readers to skim. Delete what does not apply, or write "N/A because <reason>". Never leave a heading standing over white space.
>
> **Is a full PRD the right weight?** A change one squad ships in a few sprints belongs in [one-pager.md](one-pager.md); a sprint of work behind a flag belongs in a ticket with acceptance criteria attached. [os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md) decides between them in three questions.

<!-- The general-purpose PRD for this OS. It states what the product does and how
     you will know it worked. The why-fund-it case lives in brd.md; the how-it-is
     built lives in the architecture templates; the function-by-function detail
     lives in frd.md.

     Fill these three fields first, in this order: the objectives table in section
     2, the four risks in section 9, and the out-of-scope table in section 7.
     A PRD with those three answered is already useful; the rest is detail.

     Based on the ideas in Inspired by Marty Cagan: a spec is only as good as its
     answers to the four risks: will they use it (value), can they use it
     (usability), can we build it (feasibility), does it work for the business
     (viability). Section 9 forces each risk to a named answer.

     Two overlays can extend this document:
     - Product contains a model: add the AI overlay, starting with
       ../ai/eval-spec.md, because acceptance criteria for model behavior are
       eval sets, not sentences.
     - Product answers to a financial or data regulator: the regulated module
       governs; see ../../modules/regulated/README.md and use its template as
       shipped, unmodified. -->

**Owner:** [name] · **Engineering lead:** [name] · **Design lead:** [name]
**Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved · **Version:** [n]
**Links:** [BRD](brd.md) · [problem framing](../discovery/problem-framing.md) · [FRD](frd.md)

## 1. Background

[Three to six sentences: the problem, who has it, and the evidence weight behind it. Link, do not restate; the discovery file is the source of truth. End with the hypothesis this product tests, copied from the discovery document.]

## 2. Objectives

| # | Objective | Metric | Baseline | Target | Measured where |
|---|---|---|---|---|---|
| O1 | | | | | |
| O2 | | | | | |

<!-- Objectives are outcomes in user or business terms, never "ship X". Targets
     unagreed with the metric owner are labeled ILLUSTRATIVE until agreed. -->

## 3. Users and stories

**Primary persona:** [link to personas.md block]

| # | Story | Persona | Priority (must / should / later) | Acceptance criteria ID |
|---|---|---|---|---|
| US1 | As a [persona], I want [action], so that [outcome]. | | must | AC-[n] in [acceptance-criteria.md](acceptance-criteria.md) |
| US2 | | | | |

<!-- Every "must" story needs an acceptance criteria ID before Gate 2. A must
     without testable acceptance is a hope, not a requirement. -->

## 4. Functional scope

| # | Capability | What it does, in one sentence | Story it serves | Detail |
|---|---|---|---|---|
| F1 | | | US[n] | FR-[n] in [frd.md](frd.md) |

<!-- This table is the contract of record for WHAT ships. The FRD decomposes each
     row; if the two disagree, this table wins and the FRD gets fixed. -->

## 5. Non-functional summary

[One paragraph naming the binding non-functional constraints: the latency, availability, scale, security, accessibility, and retention targets live in nfr.md with numbers and owners. Name here only the ones that shape scope, e.g. "must work offline in the field".]

Full register: [nfr.md](nfr.md)

## 6. Success metrics and instrumentation

| Metric | Type (leading / lagging / guardrail) | Instrumented where | Owner | Reviewed when |
|---|---|---|---|---|
| | | | | |

<!-- A guardrail metric is one this product must NOT damage (e.g. support ticket
     volume, page load elsewhere). Every launch needs at least one. If the
     instrumentation does not exist yet, building it is functional scope: add the
     row to section 4. -->

## 7. Out of scope

| # | Excluded | Why | Where it went (backlog / never / other team) |
|---|---|---|---|
| | | | |

## 8. Launch criteria

<!-- The conditions under which this ships. These become Gate 4 and Gate 5
     inputs; delivery templates verify them. Anything unmeasurable here will be
     argued about in the launch meeting, so make each row checkable. -->

| # | Criterion | Verified by (artifact or test) | Owner |
|---|---|---|---|
| L1 | All "must" stories pass their acceptance criteria | [acceptance-criteria.md](acceptance-criteria.md) | |
| L2 | Non-functional targets met or waived by their owner | [nfr.md](nfr.md) | |
| L3 | [rollback tested / support briefed / docs live / add your own] | | |

## 9. Four risks, answered

| Risk | Answer, with evidence | Confidence (high / medium / low) |
|---|---|---|
| Value: will they use it | | |
| Usability: can they use it | | |
| Feasibility: can we build it | | |
| Viability: does it work for the business | | |

<!-- Low confidence is a legal answer; it routes the risk into
     assumptions-register.md with a validation method. An empty cell is not. -->

## 10. Open questions

| # | Question | Blocks (section or story) | Owner | Needed by |
|---|---|---|---|---|
| | | | | |

---

## Exit gate (feeds Gate 2: requirements signed off)

- [ ] Background links to discovery evidence rather than restating it
- [ ] Every objective has metric, baseline, and target, ILLUSTRATIVE where unagreed
- [ ] Every must story carries an acceptance criteria ID
- [ ] Functional scope rows each trace to a story
- [ ] At least one guardrail metric is named with an owner
- [ ] Launch criteria are all checkable, each with an owner
- [ ] All four risks carry an answer and a confidence level
- [ ] Every low-confidence risk and open question has an owner and a date
- [ ] If the product contains a model, the AI overlay is attached; if regulated, the regulated module template is in use
