# Program Charter: [program name]

Stage: PLANNING track, feeds [Gate 2: requirements signed off](../../os/STAGE-GATES.md) and is re-read at every later gate
Knowledge: [RACI worksheet](../../frameworks/execution/raci.md)
Skill: [drafting agent](../../agents/drafting-agent.md) for the first draft; [program-premortem](../../skills/program-premortem/SKILL.md) before kickoff

> **Delete any section you do not need.** A program is several initiatives sharing one outcome, one sponsor, and one cadence. One initiative with one team needs a BRD and a PRD at the weight [os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md) picks, not a charter. Never leave a heading standing over white space.

<!-- The one-page agreement on what the program exists to change, who decides
     what, and how it is run. Signed once, re-read at every gate, because the
     argument it settles ("who can change scope") otherwise restarts in month three.

     Neighbours: the business case (business-case.md) compared the options and
     picked this one; the BRD (../definition/brd.md) carries each initiative's
     funding case; the stakeholder map (../execution/stakeholder-map.md) copies the
     RACI from here and adds the per-person engagement plan; the risk register owns
     the risks.

     Fill first: outcomes (section 2), scope boundaries (section 3), the RACI
     (section 4). -->

**Program lead:** [name] · **Sponsor:** [name, whose budget this spends] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Chartered
**Links:** [business case](business-case.md) · [roadmap](roadmap.md) · [capacity plan](capacity-plan.md)

## 1. Why this program exists

[Three sentences: the problem from Gate 1, the bet it serves in [product-strategy.md](product-strategy.md), and what is different when the program is done.]

## 2. Outcomes

<!-- Measurable changes in the world, never deliverables. "Ship the new approval
     flow" is scope; "first-submission approval rate up from [x] to [y]" is an
     outcome. Three to five rows. An unagreed target is ILLUSTRATIVE. -->

| # | Outcome | Metric | Baseline | Target | By when | Owner |
|---|---|---|---|---|---|---|
| P1 | | | | | | |
| P2 | | | | | | |

## 3. Scope

| Initiative in scope | Team | What it delivers | Outcome it serves | Definition document |
|---|---|---|---|---|
| | | | P[n] | [its BRD, PRD, or one-pager] |

| Out of scope | Why | Revisit when |
|---|---|---|
| | | |

<!-- Where a neighbouring program owns something this one touches, write the agreed
     interface and who agreed it as an out-of-scope row. Unwritten boundaries are
     discovered at integration time. -->

## 4. Governance and decision rights

<!-- One accountable name per decision area. Two names in that column means nobody
     is accountable and the sponsor finds out at launch. Consulted is a short list;
     "everyone" is the anti-pattern the RACI worksheet warns about. -->

| Decision area | Responsible | Accountable (exactly one) | Consulted | Informed |
|---|---|---|---|---|
| Scope change to any initiative | | | | |
| Budget and headcount | | | | |
| Sequencing across initiatives | | | | |
| Launch go or no-go | | | | |
| External commitments (customers, partners, regulators) | | | | |

**Escalation ladder**, which the [escalation skill](../../skills/escalation/SKILL.md) drives:

| Level | Who | Responds within | Takes |
|---|---|---|---|
| 1 | Program lead | [2 working days] | Cross-team conflicts, slips inside a quarter |
| 2 | Sponsor | [5 working days] | Budget, dates, scope that changes an outcome |
| 3 | [Steering forum] | Next meeting, or an ad hoc one within [n] days | What level 2 cannot settle |

## 5. Cadence

<!-- Every row names a written output. A meeting with no written output will be
     held again. -->

| Ritual | Frequency | Attendees | Output |
|---|---|---|---|
| Status report | Weekly | Initiative leads, program lead | [status-report.md](../execution/status-report.md), written not presented |
| Program review | Monthly | Program lead, sponsor, initiative leads | Decisions in [decision-log.md](../execution/decision-log.md) |
| Steering update | Quarterly | Sponsor, steering forum | [exec-update.md](exec-update.md) with asks |
| Gate reviews | Per stage, per initiative | Per [STAGE-GATES.md](../../os/STAGE-GATES.md) | Signed gate |

## 6. Resources and constraints

- **Teams and capacity:** [teams, with the plannable figure from the capacity plan; a charter that assumes capacity nobody confirmed is a wish with a sponsor]
- **Budget envelope:** [amount, period, what it does not cover]
- **Hard constraints:** [dates, regulations, platforms, each with its source]
- **Dependencies on other teams:** [names, in the [dependency register](../execution/dependency-register.md)]

## 7. Risks and assumptions

| Top risk or assumption | Tracked in | Owner |
|---|---|---|
| | [risk-register.md](../execution/risk-register.md) or [assumptions-register.md](../definition/assumptions-register.md) row | |

**Premortem run on:** [YYYY-MM-DD, or "not yet"; findings are register rows, not a paragraph here]

## 8. Change control

A change to an outcome, an initiative's scope, the budget, or a committed date goes through [change-request.md](../execution/change-request.md) and is approved by the accountable name in section 4. Everything smaller is a decision log entry. The charter itself changes only by the sponsor's signature, recorded here.

| Date | Change to this charter | Approved by |
|---|---|---|
| | | |

---

## Exit gate (feeds Gate 2: requirements signed off)

Done when every box is honestly ticked. The chartered copy goes with each initiative's definition set to [Gate 2](../../os/STAGE-GATES.md).

- [ ] Outcomes are measurable changes with baselines, targets, dates, and owners, not deliverables
- [ ] Every in-scope initiative names its team, its outcome, and its definition document
- [ ] Out of scope has reasons, and neighbouring programs have agreed interfaces
- [ ] Every decision area has exactly one accountable name
- [ ] The escalation ladder names people and response times
- [ ] Every cadence row has a written output
- [ ] Capacity is confirmed in [capacity-plan.md](capacity-plan.md), not assumed
- [ ] A premortem ran before kickoff and its findings are register rows
- [ ] Signed by the sponsor, [name], [date]
