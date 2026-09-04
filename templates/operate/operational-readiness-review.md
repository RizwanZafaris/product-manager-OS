---
layer: templates
stage: DELIVER
gate: 5
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Operational Readiness Review", "operational-readiness-review"]
---
# Operational Readiness Review: [product or service name]

**Stage:** DELIVER into OPERATE (feeds [Gate 5](../../os/STAGE-GATES.md), rechecked at [Gate 6](../../os/STAGE-GATES.md))
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [launch-readiness](../../skills/launch-readiness/SKILL.md)

<!-- Release readiness asks "can we ship it?". This review asks "can we run it at
     3 a.m. with the author on vacation?". Complete it before first production
     traffic, and re-run it at Gate 6 and after any incident that exposed a gap.

     The strongest section is number 6: checks derived from past incidents. Generic
     checklists catch generic failures; your incident history catches yours. -->

**Service owner:** [name] · **On-call lead:** [name] · **Review date:** [YYYY-MM-DD]

## 1. Service overview

<!-- Written for the person paged at three in the morning who has never seen
     this service. If it cannot be understood cold, it will not be read then. -->


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

<!-- Names, not teams, and the path when the first name does not answer.
     Every escalation ladder is written in daylight and used at night. -->


- Rotation: [who is in it, cadence] · Paging tool and policy: [tool, what pages vs. what waits]
- Escalation path: [first responder] then [name] then [name], with time thresholds: [n minutes each]
- The one person who knows this system best, and the plan for when they are away: [name, plan]

## 4. Backup and recovery

<!-- A backup that has never been restored is a belief. Record the last
     restore, where it ran, and how long it took. -->


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
     that could recur here becomes a concrete check with evidence. The reviews you
     are mining are filled copies of incident-postmortem.md in this directory; its
     verified corrective actions are this table's best rows. -->

| Past incident (yours or a neighboring team's) | Check added here | Evidence it holds | Verified date |
|---|---|---|---|
| | | | |

## 7. Gaps found by this review

| Gap | Risk if unfixed | Owner | Fix by |
|---|---|---|---|
| | | | |

## How this review fails

<!-- Every row is a document that reads as ready. The pattern: something was
     written and never executed, and writing is not the part that fails at
     three in the morning. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| A rota with no names | Slots filled with a team name or a placeholder, signed off as complete | Every slot names a primary and a backup, and both know they are on it |
| Runbooks never executed | Reviewed, tidied, and never once run end to end | At least one full execution per runbook, recently, with the elapsed time recorded |
| Alerts that page for everything or nothing | Dashboards green while the pager is silent through a real breach | Each alert links to a runbook and has a tested path to a named human |
| Backups never restored | "Backups are running" in the report, and no restore attempted | A restore into a clean environment on a stated cadence, checked against the source |
| Sign-off by a team | Several leads approve, and nobody owns it after launch | One named accountable approver per service, with a date |

## Exit gate

<!-- Checkable by someone who did not write this document, which is the
     test of whether a gate is a gate. -->


This review passes when:

- [ ] Every runbook scenario in section 2 exists and the highest-risk one was rehearsed
- [ ] The escalation path is names and thresholds, not team labels
- [ ] A restore has actually been tested, not just backups taken
- [ ] A kill switch or containment mechanism exists, or its absence is a gap row with a date
- [ ] Section 6 has at least one row, because no team has zero relevant incident history
- [ ] Every gap has an owner and a date

Signed: [service owner], [role], [YYYY-MM-DD]
