---
layer: templates
stage: DESIGN
gate: 3
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Observability Requirements", "observability"]
---
# Observability Requirements: `<system name>`

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md)
Knowledge: [knowledge index](../../knowledge/INDEX.md)
Skill: [architect agent](../../agents/architect-agent.md); [metrics-tree](../../skills/metrics-tree/SKILL.md) for the product metrics it must emit

<!-- The SLO and error-budget discipline here is based on the ideas in Site
     Reliability Engineering, edited by Betsy Beyer, Chris Jones, Jennifer Petoff,
     and Niall Richard Murphy (Google, 2016), encoded in this repo's own words.
     The core move: pick a small number of user-visible service level objectives,
     alert on the objectives rather than on machine internals, and treat the gap
     between the objective and perfection as a budget the team may spend on change.

     Observability is a launch requirement, not an operations afterthought: if the
     dashboard and alerts do not exist, the feature is not done. This document is
     checked again at Gate 5 by the release readiness checklist. -->

**System:** `<name>` · **Owner:** `<name>` · **Date:** `<YYYY-MM-DD>`
**Status:** Draft / In review / Approved

## 1. Service level objectives

<!-- Two to four SLOs, each phrased from the user's side. The example row shows the
     expected shape; replace it. A target with no measurement window is not an SLO. -->

| SLI (what is measured, from the user's view) | Target | Window | Measured where |
|---|---|---|---|
| requests answered successfully (non-5xx) | 99.9% | rolling 30 days | load balancer logs |
| | | | |

- Error budget policy: when the budget for a window is spent, `<what the team stops or starts: feature freeze, reliability sprint, review>`. Decided by: `<name>`.

## 2. Logs

| Event class | Fields required (minimum) | Retention | PII handling |
|---|---|---|---|
| request logs | timestamp, route, status, latency, caller id, trace id | `<period>` | `<mask or exclude which fields, per the data model>` |
| business events | event name, entity id, actor, outcome, trace id | `<period>` | |
| security events | `<per security-architecture.md section 3>` | `<period>` | |

## 3. Traces and correlation

- Trace propagation: `<mechanism and header>` across `<which services and integrations>`
- One id joins user report to logs to trace: `<which id, and where a support agent finds it>`

## 4. Alerts

<!-- Alert on symptoms users feel (SLO burn), page a human only for what needs a
     human now. Every page must have a runbook link; an alert without a next action
     trains people to ignore alerts. -->

| Alert | Condition and threshold | Severity (page / ticket) | Routes to | Runbook |
|---|---|---|---|---|
| | | | | |

## 5. Dashboard

- Dashboard location: `<link>` · Dashboard owner: `<name>`
- Shows, at minimum: each SLO with budget remaining, traffic, error rate, latency percentiles, and the health of each row in the integrations register.

## 6. Synthetic failure check

<!-- Prove the alerts work before users do. Schedule one deliberate failure in a
     pre-production or controlled environment and record what happened. -->

- Check performed: `<what was broken on purpose, and where>`
- Date and operator: `<YYYY-MM-DD, name>`
- Result: `<did the alert fire, in how long, and did the runbook work as written>`
- Fixes filed from the check: `<links>`

## Exit gate

- [ ] Every SLO has a target, a window, and a measurement location
- [ ] The error budget policy names what changes when the budget is spent, and who decides
- [ ] Log fields, retention, and PII handling are stated per event class
- [ ] Every paging alert links a runbook that exists
- [ ] The dashboard exists at the linked location and has a named owner
- [ ] A synthetic failure check has been run and its result recorded
- [ ] The example SLO row has been replaced with real ones
