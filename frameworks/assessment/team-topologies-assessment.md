---
layer: frameworks
stage: DESIGN
gate: 3
feeds: ["templates/planning/capacity-plan.md", "templates/planning/program-charter.md", "templates/execution/dependency-register.md"]
method: "knowledge/roles/triad-decision-rights.md"
aliases: ["Team Topologies Assessment", "team-topologies-assessment"]
---
# Team Topologies Assessment

Based on the ideas of Matthew Skelton and Manuel Pais, from Team Topologies (2019). Explained here in this repository's own words.

## What it is for

Four shapes cover almost every team worth having. A **stream-aligned** team owns one flow of change end to end and ships without waiting for anyone. A **platform** team builds an internal product other teams consume by themselves, from documentation and an interface, not by booking a person. A **complicated-subsystem** team holds a part that needs depth measured in months, because scattering that depth across stream teams would be worse than concentrating it. An **enabling** team raises another team's capability for a fixed period and then leaves. This sheet does not redraw your org. It answers a narrower and more useful question: which shape is each team actually operating as, which shape is it named, and what does the gap between the two cost you this period, in days somebody waited. The meeting it settles is the planning session where someone says "the platform team will handle that" and four people around the table mean four different things by it.

## Run it when

- Before the [capacity plan](../../templates/planning/capacity-plan.md) for a new planning period, while supply is still editable
- A reorganisation is being proposed from an org chart rather than from how work actually moves
- Two teams have run a shared standup for more than a quarter and nobody remembers agreeing to it
- A new head of product is forming a view in the [first 90 days](../../templates/planning/first-90-days.md) and needs the map that is real, not the one on the wiki

**Skip it when:** the org has fewer than three teams. Everyone is stream-aligned and their own platform, and the sheet will hand you four confident labels for a room of twelve people plus a reorganisation nobody needs.

## Inputs you need first

- The last period's shipped changes, with the teams whose hands each one passed through
- The ticket queue or request channel each team receives, with ages, because self-service is measured, not declared
- Each team's stated charter or the [program charter](../../templates/planning/program-charter.md) section 4, which is where the names came from
- The [dependency register](../../templates/execution/dependency-register.md) section 1, which already records the waits this sheet is about to price

## The worksheet

### 1. The four types

| Type | What it owns | How you know from outside | What it must never do |
|---|---|---|---|
| Stream-aligned | One flow of change for one segment, product, or capability | It shipped something users saw, alone | Hold a second unrelated domain |
| Platform | An internal product with a published interface and a support promise | Consumers got what they needed without talking to anyone | Answer by hand what the interface should answer |
| Complicated-subsystem | A part whose depth takes months to acquire | Fewer than three people can safely change it | Expand until it is on the critical path of every release |
| Enabling | A capability another team is missing, temporarily | It has actually left an engagement | Stay |

### 2. The three interaction modes

| Mode | What it looks like in a calendar | When it earns its cost | Expected duration | How it goes wrong |
|---|---|---|---|---|
| Collaboration | A shared standup, one board, blurred ownership | Something genuinely new is being discovered and neither side can specify it yet | Weeks, with a written end date | It has no end date, so an experiment quietly became the org design |
| X-as-a-Service | Almost nothing on the calendar, a contract and a changelog instead | The thing is understood well enough to be specified | Indefinite, and that is the point | It is called a service but runs on tickets and favours, so the contract nobody wrote is enforced by whoever shouts |
| Facilitating | A recurring session with an agenda and a leaving date | One team is short a capability the other has | A quarter at most | The helper is embedded, and enabling has become headcount |

### 3. The evidence sheet

<!-- Score every marker for every team from last period's record, not from intent.
     Each digit is a fingerprint value, never a grade: a stream-aligned team scoring
     M6 = 0 is correct, not failing. Write the basis, because a digit without one is
     a memory and two memories will disagree next week. -->

| Marker | 0 | 1 | 2 |
|---|---|---|---|
| M1 flow ownership | every change needs two or more other teams | one handoff was needed | shipped a user-visible change alone |
| M2 self-service | consumers book a named person | a ticket, answered on a published turnaround | documentation and an interface, no ticket |
| M3 exit | permanently embedded | end dates intended, none observed | every engagement has an end date and one was honoured |
| M4 depth | any engineer on the team can do the work | specialist, learnable in weeks | months to acquire, fewer than three people hold it |
| M5 load fit | three or more domains held | two | one |
| M6 consumers | end users only | one or two internal teams | three or more internal teams |

| Team | M1 | Basis | M2 | Basis | M3 | Basis | M4 | Basis | M5 | Basis | M6 | Basis |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [team] | | | | | | | | | | | | |

**The scale is three points on purpose.** Each digit is a fact about how work moved last period. A five-point scale would buy you an argument about whether self-service is a 3 or a 4, when the question that decides anything is whether one person got what they needed without booking someone.

### 4. Fit, and the arithmetic

Each type defines four load-bearing markers. Fit = the count of those four whose scored digit falls in the expected set, reported as x of 4. Score the six markers once, then read all four fits off the same six digits.

| Type | Expected digits |
|---|---|
| Stream-aligned | M1 = 2, M4 = 0 or 1, M5 = 2, M6 = 0 |
| Platform | M1 = 2, M2 = 2, M5 = 2, M6 = 2 |
| Complicated-subsystem | M2 = 0 or 1, M4 = 2, M5 = 2, M6 = 1 or 2 |
| Enabling | M1 = 0 or 1, M3 = 2, M4 = 2, M6 = 2 |

**Decision rule:** highest fit is the operating type. Ties are common rather than exotic, because all four fits are read off the same six digits, so one digit sitting in two expected sets buys two types the same score. A tie breaks toward the type with more **exact-value matches**: count only the matched markers whose expected digit is a single value rather than a range, because a range is a weaker claim about the same fact and should not win a shape. A tie that survives that break is the finding, not a rounding problem: it is two teams sharing one standup, and the sheet reports both names rather than picking one.

### 5. Named against operating, and the bill

| Team | Named type | Operating type | Fit | The mismatch in one line | Cost this period, measured | Who pays it | The move |
|---|---|---|---|---|---|---|---|
| [team] | | | [x of 4] | | [handoffs per change, median days waited, open ticket age, or people embedded with no end date] | | |

Cost is measured or it is left blank. The four units above are the whole menu, and each is already in a system you have.

### 6. Interaction mode audit

| Consumer, provider | Mode named | Mode actually running | Evidence | Running for | Verdict |
|---|---|---|---|---|---|
| [pair] | | | | [weeks] | [correct / contract missing / collaboration past its end date / facilitating with no exit] |

## Reading the result

Fit of 4 with the name matching: record it and move on. Fit of 3 or 4 with a different name: the name is wrong, not the team, and renaming costs a line in the charter. A winning fit of 2 means the name is roughly right and two specific markers are not; fix those two markers rather than the label, because a rename buys nothing. Nothing above 2 for any type means the team has no shape and is absorbing whatever arrives, which M5 will already have told you. A platform scoring M2 = 0 is the most common finding on this sheet and the most expensive: it is a queue with a roadmap, and every stream team is paying the wait privately. An enabling team whose only miss is M3 has become staff; that is a headcount decision being made by drift.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. All numbers ILLUSTRATIVE.

| Team | Named | Digits M1 to M6 | Operating type | Fit | Cost this period |
|---|---|---|---|---|---|
| Copilot squad | stream-aligned | 1, 1, 0, 0, 1, 0 | stream-aligned | 2 of 4 | 2 handoffs per user-visible change, median wait 6 working days |
| Expense platform | platform | 2, 0, 0, 0, 2, 2 | platform, on the exact-match tie-break | 3 of 4, tied three ways | 31 open tickets, median age 11 working days |
| Extraction group | platform | 2, 1, 0, 2, 2, 1 | complicated-subsystem | 4 of 4, no tie | three consumer teams waiting, median 9 days to a tuned threshold |
| AI enablement | enabling | 0, 0, 0, 2, 0, 2 | enabling, on the exact-match tie-break | 3 of 4, tied two ways | 2 of its 5 people embedded for 11 weeks, no end date |

The copilot squad has the right name and a weak fit: it cannot ship without the expense platform adding a field, and it also owns mobile receipt capture. Fix the handoff and shed the second domain; do not rename it. The expense platform ties three ways at 3, platform against stream-aligned against complicated-subsystem, which is what happens when one set of six digits is read against four expected sets. Platform carries three exact-value matches (M1, M5, M6) against stream-aligned's two and complicated-subsystem's one, so platform wins the break, and its single miss, M2 at 0, is the whole bill. The extraction group is a perfect complicated-subsystem wearing a platform's name, and the cost sits in the expectation rather than the team: three squads were told to self-serve something that needs a specialist, so they wait, and the roadmap was loaded as though they would not. AI enablement ties enabling against complicated-subsystem at 3, because the depth it holds (M4 at 2) reads as either shape; enabling wins on two exact-value matches to one, and the tie changes nothing, since M3 at 0 is the miss under both names. Mode audit: copilot to expense platform is named X-as-a-Service and runs as collaboration on a thrice-weekly shared standup, verdict contract missing. AI enablement to copilot squad is named facilitating and runs as staffing, verdict no exit.

## The decision it feeds

Whether the next planning period is loaded against the org you have or the org on the chart. Concretely: whether a platform team's self-service interface gets funded before another stream team is added, and whether the enabling engagement gets an end date or becomes permanent headcount. Both are decided in the capacity plan, and both are usually made silently by defaulting.

## Where the output lands

- [Capacity plan](../../templates/planning/capacity-plan.md), section 2 (supply, corrected for the people who are actually embedded elsewhere) and section 4 (the measured wait is standing demand, not a surprise)
- [Program charter](../../templates/planning/program-charter.md), section 4, where the operating type replaces the aspirational one

## Re-run trigger

Re-run when the org changes shape (a team is added, split, merged, or renamed, or a reporting line moves), and at the start of each planning period before the capacity plan's supply table is filled. Two events move it without a reorganisation and both count: a platform team's ticket queue growing for three consecutive weeks, and any team taking on a second domain.

## When this method misleads you

A team mid-migration reads as shapeless because it is carrying the old system and the new one at once, and the sheet will confidently propose reorganising a team that is three weeks from being fine; score it after the cutover, or score the two halves separately. The second failure is status. The moment teams learn that this sheet decides funding, M2 gets scored on the intent of the interface rather than on whether anyone used it without a ticket, and every team discovers it is a platform. The digits are descriptive, and the sheet says nothing at all about whether the work is worth doing: a beautifully shaped org ships the wrong roadmap faster. Melvin Conway's 1968 paper, How Do Committees Invent?, argued that a system's structure copies the communication structure of the group that built it, which is why the boundaries you find here are worth carrying into the architecture, and also why a boundary you invent on this sheet without moving anybody changes nothing.

## Feeds

- [Capacity plan](../../templates/planning/capacity-plan.md), sections 2 and 4; [program charter](../../templates/planning/program-charter.md), section 4
- [Dependency register](../../templates/execution/dependency-register.md), section 1: every as-a-service pair that is actually a collaboration is a dependency row somebody has not written
- [Solution architecture one-pager](../../templates/architecture/solution-architecture.md), sections 2 and 3, where the team boundaries show up as integration points
- [Stakeholder map](../../templates/execution/stakeholder-map.md), section 2, and the [RACI worksheet](../execution/raci.md), which needs the real owner rather than the named one
- Reviewed at [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md); a permanent collaboration with no end date belongs in the [risk matrix](../execution/risk-matrix.md)
- Method background: [triad decision rights](../../knowledge/roles/triad-decision-rights.md) and [PM specializations](../../knowledge/roles/specializations.md); [knowledge index](../../knowledge/INDEX.md)
