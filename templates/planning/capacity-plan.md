# Capacity Plan: [team, program, or product], [period]

Stage: PLANNING track, feeds the [roadmap](roadmap.md) and [Gate 2: requirements signed off](../../os/STAGE-GATES.md), where a signed plan needs a team that can carry it
Knowledge: [estimation sheet](../../frameworks/execution/estimation-sheet.md)
Skill: [estimator agent](../../agents/estimator-agent.md)

> **Delete any section you do not need.** One squad planning one quarter fills sections 2, 3, and 5 and stops. The full form is for several teams sharing one roadmap. Never leave a heading standing over white space.

<!-- Sets the supply of team time against the demand the roadmap places on it, so
     that Now holds only what the team can carry and Next is honest. It does not
     decide order or outcome; the roadmap (roadmap.md) does. The estimation sheet
     gives each initiative its range; the hiring scorecard
     (../execution/hiring-scorecard.md) fills the seats this plan shows are missing;
     the tech-debt register (../execution/tech-debt-register.md) supplies the debt
     interest row in section 4.

     Fill first: supply (section 2), demand (section 3), the 80 percent line
     (section 5). -->

**Owner:** [name] · **Period:** [quarter] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved
**Unit:** [team-weeks or person-days, one unit for the whole file] · **Linked roadmap:** [roadmap.md copy]

## 1. The rules

<!-- Stated so every reviewer argues from the same arithmetic. Edit the numbers to
     your context; keep the rules. -->

- **The 80 percent rule.** Committed work is planned to no more than 80 percent of net available capacity. The other 20 percent absorbs interrupts, estimate error, and the standing demand nobody scheduled. When committed demand exceeds the line, an initiative moves to Next; the line does not move.
- **Ranges, not numbers.** Every initiative carries a low, likely, and high figure from the estimation sheet. The planning figure is the likely value, or the high value when confidence is low.
- **One unit.** A file that mixes person-days and team-weeks hides a factor of five somewhere.

## 2. Supply per team

<!-- Gross is people times working weeks. Subtract what is already spoken for
     before drawing the line. The italic row is ILLUSTRATIVE. -->

| Team | People | Weeks | Gross | Leave | On-call and support | Recurring load (hiring, onboarding, meetings) | Net | Plannable (80 percent of net) |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |
| *extraction squad (ILLUSTRATIVE)* | *6* | *13* | *78* | *8* | *6* | *4* | *60* | *48* |

## 3. Demand per initiative

<!-- Rows in roadmap order. The estimator agent checks each row for the work that
     estimates leave out: compliance review, operational readiness, migration,
     instrumentation, documentation. -->

| Initiative (roadmap ref) | Team | Low | Likely | High | Confidence | Planning figure | Missing work checked? | Order |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | 1 |
| | | | | | | | | 2 |

## 4. Standing demand

<!-- Work that happens whether or not it is planned. Last period's actuals beat
     this period's hopes. -->

| Item | Team | Units per period | Source |
|---|---|---|---|
| Tech debt interest | | | interest total in [tech-debt-register.md](../execution/tech-debt-register.md) |
| Support and defect fixing | | | last period's actual |
| Platform, security, and compliance mandates | | | [named mandate] |
| Experiment and analytics support | | | [experiment brief or analytics spec] |

## 5. The balance

<!-- Committed demand is standing demand plus initiatives above the line, in
     order, until the next one would break the plannable figure. Everything below
     the line is Next, by name, so the roadmap and this file agree. The italic row
     is ILLUSTRATIVE. -->

| Team | Plannable | Standing demand | Initiatives above the line | Committed | Utilization | Over or under | Moves to Next |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| *extraction squad (ILLUSTRATIVE)* | *48* | *13* | *R-1, R-2, R-3 = 42* | *55* | *115 percent* | *over by 7* | *R-3; R-1 and R-2 commit* |

## 6. Gaps and hiring

<!-- A gap is a decision, not a note. Hiring takes longer than the period this
     plan covers, so a hire fixes the next plan; this one descopes or borrows. -->

| Gap | Team | Units short | Option (hire / borrow / descope / defer) | Decision owner | Needed by | Scorecard |
|---|---|---|---|---|---|---|
| | | | | | | [hiring-scorecard.md](../execution/hiring-scorecard.md) copy |

## 7. Assumptions this plan rests on

| Assumption | If wrong | Tracked in |
|---|---|---|
| [e.g. no attrition on the extraction squad this quarter] | | [risk-register.md](../execution/risk-register.md) row |
| [e.g. the compliance mandate stays at [n] units] | | [assumptions-register.md](../definition/assumptions-register.md) row |

---

## Exit gate (feeds the roadmap and Gate 2: requirements signed off)

Done when every box is honestly ticked. The approved copy sets the Now column of [roadmap.md](roadmap.md) and travels with the definition set to [Gate 2](../../os/STAGE-GATES.md).

- [ ] One unit is used throughout
- [ ] Every supply row subtracts leave, on-call, and recurring load before the 80 percent line is drawn
- [ ] Every demand row carries low, likely, and high figures, and says whether missing work was checked
- [ ] Standing demand includes debt interest and last period's support actual
- [ ] No team is committed above its plannable figure; anything over the line is named and moved to Next
- [ ] Every gap has an option, a decision owner, and a needed-by date
- [ ] The roadmap's Now column matches what sits above the line here
- [ ] The ILLUSTRATIVE rows have been deleted
- [ ] Signed by [name], [date]
