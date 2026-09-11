# Program Charter: Northstar Service Reliability

Fills [templates/planning/program-charter.md](../templates/planning/program-charter.md). Everything here is invented: Northstar Works is a fictional software company, Quay is not used here, and the program, products, people and figures are ILLUSTRATIVE. See the [examples index](README.md).

**Program lead:** Mira Sen · **Sponsor:** Daniel Okafor · **Date:** 2026-10-30 · **Status:** Chartered
**Links:** business case, roadmap and capacity plan not included in this standalone excerpt; see the [business case](../templates/planning/business-case.md), [roadmap](../templates/planning/roadmap.md) and [capacity plan](../templates/planning/capacity-plan.md) templates

> **Fictional context, ILLUSTRATIVE:** Northstar Works sells a fictional operations platform called Beacon. Mira Sen leads product operations, Daniel Okafor sponsors the program, and the initiative leads are Priya Nair, Tomas Lindqvist and Elena Petrova. The program joins three initiatives that improve one customer outcome: Beacon customers complete important operational work without avoidable interruption.

## 1. Why this program exists

Beacon customers lose time when service interruptions, unclear ownership and delayed operational information prevent them from completing routine work. The program serves Northstar Works' product strategy bet that dependable workflows, visible status and faster recovery will increase customer trust and retention. When the program is done, customers will complete the covered workflows with fewer interruptions, while Beacon teams will have one agreed operating rhythm for reliability work across the three initiatives.

## 2. Outcomes

All figures ILLUSTRATIVE. Targets are agreed for this charter and are not claims about current Beacon performance.

| # | Outcome | Metric | Baseline | Target | By when | Owner |
|---|---|---|---|---|---|---|
| P1 | Customers complete covered workflows without an avoidable interruption | Share of covered workflow attempts completed without an interruption | 61%, measured before the program | 75% | 2026-12-21 | Priya Nair |
| P2 | Customers receive useful operational information before they need support | Share of covered incidents with a customer-visible status update before the next customer action | 0%, the program has not yet established this capability | 50% | 2026-12-21 | Tomas Lindqvist |
| P3 | Beacon teams recover from covered incidents with less delay | Share of covered incidents with an owner and recovery decision recorded in the decision log | Not yet measured | 100% | 2026-12-21 | Elena Petrova |

## 3. Scope

| Initiative in scope | Team | What it delivers | Outcome it serves | Definition document |
|---|---|---|---|---|
| Workflow resilience | Beacon Core team, led by Priya Nair | Recovery handling and retry behaviour for the covered workflows | P1 | PRD approved at Gate 2 |
| Customer status | Beacon Communications team, led by Tomas Lindqvist | Customer-visible status messages and an operational status surface | P2 | BRD and PRD approved at Gate 2 |
| Incident operating model | Beacon Operations team, led by Elena Petrova | Incident ownership, recovery decisions and a shared review process | P3 | One-pager approved at Gate 2 |

| Out of scope | Why | Revisit when |
|---|---|---|
| Rebuilding Beacon's underlying hosting platform | A neighbouring infrastructure program owns platform replacement, and duplicating that work would create two sources of truth | Revisit through the dependency register after the infrastructure program confirms its interface |
| New customer-facing capabilities unrelated to reliability | They do not serve the shared program outcome and would compete for the confirmed capacity | Revisit at the next roadmap review if the sponsor changes the program outcome |
| A separate support organisation or staffing model | The program changes operating practice, not organisational structure | Revisit if the sponsor approves an operating-model change |

The agreed interface with the infrastructure program is limited to service health signals and incident escalation. Elena Petrova owns the Beacon side of that interface, and the infrastructure program lead owns the platform side.

## 4. Governance and decision rights

| Decision area | Responsible | Accountable (exactly one) | Consulted | Informed |
|---|---|---|---|---|
| Scope change to any initiative | Mira Sen | Daniel Okafor | Priya Nair, Tomas Lindqvist, Elena Petrova | Initiative teams |
| Budget and headcount | Mira Sen | Daniel Okafor | Priya Nair, Tomas Lindqvist, Elena Petrova | Initiative teams |
| Sequencing across initiatives | Mira Sen | Mira Sen | Priya Nair, Tomas Lindqvist, Elena Petrova | Daniel Okafor |
| Launch go or no-go | Elena Petrova | Daniel Okafor | Priya Nair, Tomas Lindqvist, Mira Sen | Initiative teams |
| External commitments (customers, partners, regulators) | Tomas Lindqvist | Daniel Okafor | Mira Sen, Priya Nair, Elena Petrova | Initiative teams |

**Escalation ladder**, which the [escalation skill](../skills/escalation/SKILL.md) drives:

| Level | Who | Responds within | Takes |
|---|---|---|---|
| 1 | Mira Sen, program lead | 2 working days | Cross-team conflicts and slips inside the current planning period |
| 2 | Daniel Okafor, sponsor | 5 working days | Budget, dates or scope that changes an outcome |
| 3 | Northstar steering forum, chaired by Daniel Okafor | Next monthly meeting, or an ad hoc meeting before the next working day when launch safety is at risk | Matters level 2 cannot settle, including unresolved trade-offs between initiatives |

## 5. Cadence

Every row has a written output. A meeting without an output is not part of this program cadence.

| Ritual | Frequency | Attendees | Output |
|---|---|---|---|
| Status report | Weekly | Initiative leads, program lead | a status report (not included; see the [status-report.md template](../templates/execution/status-report.md)), written not presented |
| Program review | Monthly | Program lead, sponsor, initiative leads | Decisions in a decision log (not included; see the [decision-log.md template](../templates/execution/decision-log.md)) |
| Steering update | Quarterly | Sponsor, steering forum | an exec update with asks (not included; see the [exec-update.md template](../templates/planning/exec-update.md)) |
| Gate reviews | Per stage, per initiative | Per [STAGE-GATES.md](../os/STAGE-GATES.md) | Signed gate |

## 6. Resources and constraints

- **Teams and capacity:** Three confirmed teams, with 28 engineer-weeks in the capacity plan (not included in this standalone excerpt; see the [capacity plan template](../templates/planning/capacity-plan.md)): 12 for Workflow Resilience, 9 for Customer Status and 7 for the Incident Operating Model. Arithmetic: 12 + 9 + 7 = 28 engineer-weeks. The figures are ILLUSTRATIVE estimates recorded in the capacity plan.
- **Budget envelope:** Sponsor-approved envelope for the program period, recorded in the capacity plan. It covers the three initiatives and their required testing and operational work, and does not cover the neighbouring infrastructure program.
- **Hard constraints:** Gate reviews follow [STAGE-GATES.md](../os/STAGE-GATES.md). Customer-facing status changes require review by the Beacon Operations team before release. No initiative may make an external commitment without the decision right in section 4.
- **Dependencies on other teams:** The infrastructure program supplies service health signals and receives Beacon escalation through the dependency register (not included; see the [dependency-register.md template](../templates/execution/dependency-register.md)).

## 7. Risks and assumptions

| Top risk or assumption | Tracked in | Owner |
|---|---|---|
| The three teams can deliver against one shared outcome without local sequencing decisions pulling them apart | assumptions register (not included; see the [assumptions-register.md template](../templates/definition/assumptions-register.md)) row A1 | Mira Sen |
| The infrastructure program provides the agreed health signal in time for Workflow Resilience testing | risk register (not included; see the [risk-register.md template](../templates/execution/risk-register.md)) row R1 | Elena Petrova |
| Customers understand the new status information and use it instead of opening a support request | risk register row R2 | Tomas Lindqvist |
| Retry behaviour can be introduced without creating duplicate customer actions | risk register row R3 | Priya Nair |
| The 28 engineer-weeks in the capacity plan remain available for the program period | risk register row R4 | Daniel Okafor |

**Premortem run on:** 2026-10-30. See the risk and assumptions registers.

## 8. Change control

A change to an outcome, an initiative's scope, the budget, or a committed date goes through a change request (not included; see the [change-request.md template](../templates/execution/change-request.md)) and is approved by the accountable name in section 4. Everything smaller is a decision log entry. The charter itself changes only by the sponsor's signature, recorded here.

| Date | Change to this charter | Approved by |
|---|---|---|
| 2026-10-30 | Initial charter approved for the three-initiative Northstar Service Reliability program | Daniel Okafor |

---

## Exit gate (feeds Gate 2: requirements signed off)

Done when every box is honestly ticked. The chartered copy goes with each initiative's definition set to [Gate 2](../os/STAGE-GATES.md).

- [x] Outcomes are measurable changes with baselines, targets, dates, and owners, not deliverables
- [x] Every in-scope initiative names its team, its outcome, and its definition document
- [x] Out of scope has reasons, and neighbouring programs have agreed interfaces
- [x] Every decision area has exactly one accountable name
- [x] The escalation ladder names people and response times
- [x] Every cadence row has a written output
- [x] Capacity is confirmed in the capacity plan, not assumed
- [x] A premortem ran before kickoff and its findings are register rows
- [x] Signed by the sponsor, Daniel Okafor, 2026-10-30

Signed at Gate 2, 2026-10-30: Daniel Okafor, sponsor; Mira Sen, program lead.
