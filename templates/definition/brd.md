---
layer: templates
stage: DEFINE
gate: 2
feeds: []
method: "knowledge/okrs.md"
aliases: ["BRD", "Business Requirements Document"]
---
# Business Requirements Document: [initiative name]

Stage: DEFINE, feeds Gate 2 (requirements signed off)
Knowledge: [OKRs](../../knowledge/okrs.md)
Skill: [write-prd](../../skills/write-prd/SKILL.md)

<!-- The BRD answers one question: why should the business fund this, and on what
     terms? It is written for the sponsor and the people who control money and
     headcount. The PRD (prd.md) answers what the product does; keep the two
     separate so a funding debate never edits a requirement and a requirement
     debate never reopens funding.

     Every business objective here should trace to a stated company objective or
     OKR. An initiative that serves no stated objective is either strategy the
     company has not written down yet, or a pet project. Find out which before
     Gate 2. -->

**Owner:** [name] · **Sponsor:** [name, the person whose budget this spends]
**Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Signed off · **Version:** [n]

## 1. Business objectives

| # | Objective | Company objective or OKR it serves | Metric | Baseline | Target | By when |
|---|---|---|---|---|---|---|
| BO1 | | | | | | |
| BO2 | | | | | | |

<!-- Two or three objectives. If you have six, this is a program, not an
     initiative; split it. Baseline "unknown" is allowed only with a named owner
     and date for producing it. -->

## 2. Background and problem

[Three to five sentences. Link the framed problem rather than restating it: ../discovery/problem-framing.md. State what happens if the business does nothing, drawn from that file's cost of inaction.]

## 3. Scope

### In scope

| # | Capability or change, in business terms | Serves objective |
|---|---|---|
| S1 | | BO[n] |

### Out of scope

| # | Explicitly excluded | Why | Revisit when |
|---|---|---|---|
| X1 | | | |

<!-- Out of scope is the most read part of a BRD in month three. Write it as
     armor: each exclusion names its reason so it survives the meeting where
     someone tries to sneak it back in. -->

## 4. Stakeholders

| Name | Function | Stake in this initiative | Decision rights (approves / consulted / informed) |
|---|---|---|---|
| | | | |

<!-- Decision rights, agreed now, are cheaper than a launch-week turf argument.
     Exactly one row should hold final approval. -->

## 5. Constraints

| Constraint | Type (budget / deadline / regulatory / platform / people) | Hard or soft | Source |
|---|---|---|---|
| | | | |

<!-- A hard constraint cannot move without the sponsor's signature. Label
     honestly: teams that call every preference "hard" lose the word when they
     need it. If any constraint is regulatory AND the product contains an AI or
     machine-learning feature, the regulated overlay applies at Gate 2; see
     ../../os/STAGE-GATES.md for the rule, which governs, and
     ../../modules/regulated/README.md for the module. A regulatory constraint
     on a product with no model in it is carried at Gate 2 by the regulatory
     owner instead. -->

## 6. Financial case

- **Cost to build:** [estimate with range, and who produced it]
- **Cost to run:** [per month or year once live]
- **Expected return:** [revenue, saving, or risk reduction, with the calculation method written out]
- **Payback horizon:** [when cumulative return passes cumulative cost]
- **Sensitivity:** [the one assumption that, if wrong, breaks this case; it must also appear in assumptions-register.md]

<!-- Every number here is ILLUSTRATIVE until the finance partner named below has
     agreed the method in writing. A return figure whose method was never written
     down is a number that gets withdrawn under questioning. -->

**Finance partner who agreed the calculation method:** [name, date]

## 7. Success measurement

- **Who measures:** [name] · **Where:** [dashboard or report]
- **Review cadence after launch:** [when BO metrics are reviewed, and by whom]
- **Sunset trigger:** [the result that would cause the business to unwind this]

## 8. Sponsor sign-off

- **I confirm the objectives, scope, constraints, and financial case above, and I fund the DEFINE and DESIGN stages.**
- **Sponsor:** [name] · **Signature or approval record:** [link] · **Date:** [YYYY-MM-DD]

---

## Exit gate (feeds Gate 2: requirements signed off)

- [ ] Every objective traces to a stated company objective or OKR
- [ ] Every objective has metric, baseline, and target, or a named owner and date for the missing number
- [ ] Out of scope is populated, with reasons
- [ ] Exactly one stakeholder holds final approval
- [ ] Financial case method agreed with a named finance partner, or labeled ILLUSTRATIVE with an owner and date
- [ ] The sensitivity assumption appears in [assumptions-register.md](assumptions-register.md)
- [ ] Sponsor sign-off recorded with a date
