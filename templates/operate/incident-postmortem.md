---
layer: templates
stage: OPERATE
gate: 6
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Incident Postmortem", "incident-postmortem"]
---
# Incident Postmortem: [incident short name]

**Stage:** OPERATE (feeds [Gate 6: outcomes verified, learn or sunset](../../os/STAGE-GATES.md)); an event review, run once per qualifying incident. Verified actions become section 6 checks in [operational-readiness-review.md](operational-readiness-review.md)
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [postmortem-facilitator](../../skills/postmortem-facilitator/SKILL.md)

<!-- A postmortem exists to make the same incident impossible, not to find out who to
     be disappointed in. The blameless discipline here restates, in this repository's
     own words, the practice Google's SRE writing calls postmortem culture and the
     practice Amazon runs as the Correction of Error review: assume everyone acted
     reasonably on the information they had, and interrogate the system that handed
     them that information. The moment a cause row contains a person's name, the next
     incident's responders learn to hide things, and this document starts collecting
     fiction.

     This is not the launch review. post-launch-review.md judges whether a launch met
     its goals; this file dissects one operational failure. Write it within a week of
     resolution, while the timeline is still in people's heads and chat scrollback. -->

**Incident owner (writes this doc):** [name] · **Facilitator (runs the review):** [name]
**Incident date:** [YYYY-MM-DD] · **Review date:** [YYYY-MM-DD] · **Status:** [draft / reviewed / actions verified]

## 1. Facts, severity, and timeline

- One-sentence summary a person outside the team can understand: [sentence]
- Severity: [level, per your org's definitions] · Duration from first impact to full resolution: [n hours/minutes]
- Detected by: [alert / customer report / employee noticed], which is itself a finding
- Systems and features involved: [list]

<!-- Timeline entries are observations with timestamps, not interpretations. "The
     deploy went out" and "the first alert fired" are facts; "we should have caught
     it" belongs in section 3. Pull times from logs and chat, not memory. -->

| Time (with zone) | What happened | Source (log, alert, chat link) |
|---|---|---|
| [HH:MM] | [first impact] | [where this is recorded] |
| [HH:MM] | [detection] | |
| [HH:MM] | [mitigation applied] | |
| [HH:MM] | [full resolution confirmed] | |

## 2. Customer and business impact

<!-- Quantify or say why you cannot. "Some users saw errors" is not an impact
     statement; it is the absence of one. Every number is labeled ILLUSTRATIVE or
     traced to the query or dashboard that produced it. -->

- Users or accounts affected: [n, and how you counted]
- What they experienced, in their terms: [what broke from the outside]
- Business impact: [revenue, SLA credits, support volume, trust, with numbers where they exist]
- Commitments breached, if any: [SLA or contract clause, or "none"]

## 3. Contributing causes

<!-- Systems language only: process, tooling, alerting, documentation, design.
     Incidents are almost never one cause; write every condition that had to be true.
     "Why was that possible?" asked a few times per row gets you past the trigger to
     the conditions. No cause row names a person; "the on-call engineer" as a role is
     acceptable, a name is not. -->

| # | Contributing cause (systems language) | Why it was possible | Category (process / tooling / alerting / docs / design) |
|---|---|---|---|
| 1 | [e.g. the deploy pipeline had no canary stage for this service] | [why] | [category] |
| 2 | [e.g. the alert threshold was set above the level customers notice] | [why] | [category] |
| 3 | [add rows until the incident could not have happened without each one] | | |

## 4. What worked

<!-- Postmortems that only list failures teach responders that showing up earns
     criticism. Name what limited the damage: a runbook that held, a rehearsed
     escalation, a kill switch that killed. These are the behaviors to keep funding. -->

- [what worked, and what it saved]

## 5. Corrective actions

<!-- One action per cause row above, minimum. "Be more careful" is not an action; a
     pipeline change, an alert, a runbook, a removed permission is. The verification
     method says how a reviewer will confirm the action landed, not who promises it
     will. Track these to done; an unverified action is the next incident's cause
     row. -->

| Action | Addresses cause # | Owner | Due date | Verification method | Status |
|---|---|---|---|---|---|
| [concrete change] | [#] | [name] | [YYYY-MM-DD] | [e.g. failed-canary test in CI, alert fired in a drill] | [open / done / verified] |
| | | | | | |

## Exit gate

This postmortem is done when:

- [ ] The timeline is built from recorded sources, with detection and resolution both timestamped
- [ ] Impact is quantified, or the reason it cannot be is stated
- [ ] No cause row contains a person's name
- [ ] Every cause row has at least one corrective action, and every action has an owner, a due date, and a verification method
- [ ] Verified actions that change how the service is run are copied into section 6 of [operational-readiness-review.md](operational-readiness-review.md)
- [ ] The review happened out loud with the responders in the room, not by document circulation alone

Signed: [incident owner], [role], [YYYY-MM-DD]
