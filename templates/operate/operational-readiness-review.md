# Operational Readiness Review: [product or service name]

**Stage:** DELIVER into OPERATE (feeds [Gate 5](../../os/STAGE-GATES.md), rechecked at [Gate 6](../../os/STAGE-GATES.md))
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [drafting agent](../../agents/drafting-agent.md)

<!-- Release readiness asks "can we ship it?". This review asks "can we run it at
     3 a.m. with the author on vacation?". Complete it before first production
     traffic, and re-run it at Gate 6 and after any incident that exposed a gap.

     The strongest section is number 6: checks derived from past incidents. Generic
     checklists catch generic failures; your incident history catches yours. -->

**Service owner:** [name] · **On-call lead:** [name] · **Review date:** [YYYY-MM-DD]

## 1. Service overview

- What it does, in one sentence a responder can act on: [sentence]
- Criticality tier: [tier, per your org's definitions] · Users affected when down: [who, how many]
- Upstream dependencies: [list, from ../execution/dependency-register.md]
- Downstream consumers: [who breaks if we break]

## 2. Runbooks

<!-- A runbook that has never been rehearsed is a hypothesis. The italic row shows a
     completed entry. -->

| Scenario | Runbook location | Last rehearsed | Rehearsed by |
|---|---|---|---|
| | | [YYYY-MM-DD or "never"] | |
| *service restart after bad deploy* | *runbooks/restart.md in the service repo* | *[date]* | *[name]* |

## 3. On-call and escalation

- Rotation: [who is in it, cadence] · Paging tool and policy: [tool, what pages vs. what waits]
- Escalation path: [first responder] then [name] then [name], with time thresholds: [n minutes each]
- The one person who knows this system best, and the plan for when they are away: [name, plan]

## 4. Backup and recovery

- Data covered by backups: [what] · Backup cadence: [n]
- Recovery point objective (max acceptable data loss): [n] · Recovery time objective: [n]
- Last successful RESTORE test, not backup test: [YYYY-MM-DD, by whom]
- Where restore steps live: [location]

## 5. Blast radius and containment

- Worst credible failure and who it reaches: [description]
- Kill switch or feature flag to isolate this service or feature: [what and where, or a gap row below]
- Rate limits and load shedding in place: [what protects the neighbors]

## 6. Checks derived from past incidents

<!-- Mine your incident reviews, your team's and the wider org's. Each past incident
     that could recur here becomes a concrete check with evidence. -->

| Past incident (yours or a neighboring team's) | Check added here | Evidence it holds | Verified date |
|---|---|---|---|
| | | | |

## 7. Gaps found by this review

| Gap | Risk if unfixed | Owner | Fix by |
|---|---|---|---|
| | | | |

## Exit gate

This review passes when:

- [ ] Every runbook scenario in section 2 exists and the highest-risk one was rehearsed
- [ ] The escalation path is names and thresholds, not team labels
- [ ] A restore has actually been tested, not just backups taken
- [ ] A kill switch or containment mechanism exists, or its absence is a gap row with a date
- [ ] Section 6 has at least one row, because no team has zero relevant incident history
- [ ] Every gap has an owner and a date

Signed: [service owner], [role], [YYYY-MM-DD]
