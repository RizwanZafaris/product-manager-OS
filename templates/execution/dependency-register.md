# Dependency Register: `<initiative name>`

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md), governed weekly through DELIVER
Knowledge: [knowledge index](../../knowledge/INDEX.md)
Skill: [program-premortem](../../skills/program-premortem/SKILL.md)

<!-- Dependencies are where schedules go to die, because the work sits on someone
     else's backlog under someone else's priorities. The register exists to make
     that visible weekly, not to decorate a kickoff deck. Rule of the file: a
     dependency is not "agreed" until the owning team has the work on their own
     plan with a date; a verbal yes in a meeting is a lead, not a commitment. -->

**Initiative:** `<name>` · **Register owner:** `<name>` · **Review cadence:** weekly, `<day and meeting>`
**Last reviewed:** `<YYYY-MM-DD>`

## 1. The register

<!-- Status vocabulary, fixed: requested (we asked), committed (on their plan, with
     their date), in progress, delivered, at risk (their date now lands after our
     needed-by), blocked (they have stopped). "At risk" is computed, not felt:
     compare their date to needed-by every week and let the column tell the truth.
     The example row shows the precision expected; delete it once real rows exist. -->

| # | Dependency (deliverable, not a team name) | Owning team | Their named contact | Needed by (our date) | Their committed date | Status | Escalation contact (their manager or ours) |
|---|---|---|---|---|---|---|---|
| 1 | Payments team exposes refund status webhook in sandbox | Payments platform | `<name>` | 2026-05-10 | 2026-05-03 | committed | `<name, role>` |
| | | | | | | | |

## 2. Escalation ladder

<!-- Agree the ladder before you need it. An escalation is a service to the project,
     not an act of aggression; the register makes it boring and procedural. -->

1. Slip detected at weekly review: register owner contacts the named contact within one working day.
2. No recovery plan within `<n>` working days: escalate to the escalation contact on the row.
3. Still unresolved and the needed-by date is inside `<n>` weeks: raise at `<steering meeting>`, and the dependency becomes a risk register row with a mitigation.

## 3. Reverse dependencies

<!-- Work other teams need from this initiative. Filling this section is what earns
     the goodwill the escalation ladder spends. -->

| Deliverable we owe | To team | Their needed-by | Our committed date | Status |
|---|---|---|---|---|
| | | | | |

## 4. Weekly review notes

| Date | Rows that changed status | Escalations opened or closed |
|---|---|---|
| | | |

## Exit gate

- [ ] Every dependency names a deliverable, a human contact, and an escalation contact
- [ ] Every row shows both our needed-by date and their committed date
- [ ] No row claims "committed" without the work on the owning team's own plan
- [ ] Every at-risk or blocked row has a corresponding risk register entry
- [ ] Reverse dependencies are filled in, not left as a courtesy blank
- [ ] The weekly review has an entry from the current or previous week
- [ ] The example row has been deleted
