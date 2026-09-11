# Harbourgate Team Topologies Assessment

Fills [frameworks/assessment/team-topologies-assessment.md](../frameworks/assessment/team-topologies-assessment.md). Everything here is invented: Harbourgate, Quay, the payments squad and every person are fictional, and every number, date and identifier is ILLUSTRATIVE, taken from the [Harbourgate journey](harbourgate-journey.md) and its [coverage sheet](harbourgate-coverage-sheet.md).

**Owner:** Tomasz Wierzbicki, Engineering Lead · **Date:** 2026-10-16 · **Product:** Harbourgate · **Record:** post-drain assessment, HC46

## What it is for

This assessment identifies the operating shape of Harbourgate's payments squad after the drain. The squad is named stream-aligned, but its scored markers fit platform more strongly. It publishes internal interfaces that other teams consume without booking a squad member: Quay API v1, the decline event stream and the nightly ERP export I-11.

The decision is a rename, not an organisational move. The payments squad remains responsible for one domain, card payments with reconciliation, while its platform interfaces and consumer relationships are made explicit.

## Run it when

- Before the next capacity plan, while the payments squad's supply and consumer demand are still editable
- After the provider drain has completed and the squad's operating behaviour can be scored from evidence
- When a team name no longer describes how other teams consume its work
- When a collaboration has ended and a contract or published interface should replace recurring coordination

**Skip it when:** the organisation has fewer than three teams. That condition does not apply to Harbourgate's assessment of the payments squad.

## Inputs you need first

- The post-drain deployment record, including HC47's evidence that Quay deployed alone
- The dependency register, including DEP-4, DEP-6 and DEP-7
- The squad's current name and domain ownership
- The interaction records for finance operations, InfoSec and data engineering
- The [Harbourgate journey](harbourgate-journey.md) and [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), especially HC46 and HC47

## The worksheet

### 1. The four types

| Type | What it owns | How you know from outside | What it must never do |
|---|---|---|---|
| Stream-aligned | One flow of change for one segment, product, or capability | It shipped something users saw, alone | Hold a second unrelated domain |
| Platform | An internal product with a published interface and a support promise | Consumers got what they needed without talking to anyone | Answer by hand what the interface should answer |
| Complicated-subsystem | A part whose depth takes months to acquire | Fewer than three people can safely change it | Expand until it is on the critical path of every release |
| Enabling | A capability another team is missing, temporarily | It has actually left an engagement | Stay |

The payments squad has one domain, card payments with reconciliation, and therefore does not present as a complicated-subsystem or enabling team. Its consumers use the decline stream without a ticket, and its finance export is an interface rather than a recurring request for squad time.

### 2. The three interaction modes

| Mode | What it looks like in a calendar | When it earns its cost | Expected duration | How it goes wrong |
|---|---|---|---|---|
| Collaboration | A shared standup, one board, blurred ownership | Something genuinely new is being discovered and neither side can specify it yet | Weeks, with a written end date | It has no end date, so an experiment quietly became the org design |
| X-as-a-Service | Almost nothing on the calendar, a contract and a changelog instead | The thing is understood well enough to be specified | Indefinite, and that is the point | It is called a service but runs on tickets and favours, so the contract nobody wrote is enforced by whoever shouts |
| Facilitating | A recurring session with an agenda and a leaving date | One team is short a capability the other has | A quarter at most | The helper is embedded, and enabling has become headcount |

The finance operations engagement was collaboration during the drain, from 2026-07-08 to 2026-09-15, and ended on schedule into X-as-a-Service through I-11. InfoSec is facilitating, with its exit represented by DEP-7. Data engineering consumes the legacy table-shape contract as X-as-a-Service under ADR-0002.

### 3. The evidence sheet

The six markers are scored from the post-drain record. Each digit is a fingerprint value, not a grade.

| Marker | 0 | 1 | 2 |
|---|---|---|---|
| M1 flow ownership | every change needs two or more other teams | one handoff was needed | shipped a user-visible change alone |
| M2 self-service | consumers book a named person | a ticket, answered on a published turnaround | documentation and an interface, no ticket |
| M3 exit | permanently embedded | end dates intended, none observed | every engagement has an end date and one was honoured |
| M4 depth | any engineer on the team can do the work | specialist, learnable in weeks | months to acquire, fewer than three people hold it |
| M5 load fit | three or more domains held | two | one |
| M6 consumers | end users only | one or two internal teams | three or more internal teams |

| Team | M1 | Basis | M2 | Basis | M3 | Basis | M4 | Basis | M5 | Basis | M6 | Basis |
|---|---:|---|---:|---|---:|---|---:|---|---:|---|---:|---|
| Payments squad | 2 | HC47 records Quay deploying alone in the post-drain window | 2 | DEP-6 was met through the decline event stream with no ticket | 0 | No engagements are recorded | 1 | The reconciliation matcher is learnable in weeks | 2 | One domain, card payments with reconciliation | 2 | Consumers are the order service, fraud and finance |

**The scale is three points on purpose.** The digits describe how work moved in the post-drain record. The payments squad's M2 score is 2 because DEP-6 was met through a published decline event stream without a ticket, not because self-service was merely intended.

### 4. Fit, and the arithmetic

The payments squad's scored digits are:

**M1 = 2, M2 = 2, M3 = 0, M4 = 1, M5 = 2, M6 = 2.**

| Type | Expected digits |
|---|---|
| Stream-aligned | M1 = 2, M4 = 0 or 1, M5 = 2, M6 = 0 |
| Platform | M1 = 2, M2 = 2, M5 = 2, M6 = 2 |
| Complicated-subsystem | M2 = 0 or 1, M4 = 2, M5 = 2, M6 = 1 or 2 |
| Enabling | M1 = 0 or 1, M3 = 2, M4 = 2, M6 = 2 |

| Type | Marker checks | Arithmetic | Fit |
|---|---|---|---:|
| Stream-aligned | M1 = 2, M4 = 0 or 1, M5 = 2, M6 = 0 | 1 + 1 + 1 + 0 = 3 | 3 of 4 |
| Platform | M1 = 2, M2 = 2, M5 = 2, M6 = 2 | 1 + 1 + 1 + 1 = 4 | 4 of 4 |
| Complicated-subsystem | M2 = 0 or 1, M4 = 2, M5 = 2, M6 = 1 or 2 | 0 + 0 + 1 + 1 = 2 | 2 of 4 |
| Enabling | M1 = 0 or 1, M3 = 2, M4 = 2, M6 = 2 | 0 + 0 + 0 + 1 = 1 | 1 of 4 |

Platform is the operating type because its fit is the highest at 4 of 4. There is no tie to break.

The platform fit has four exact-value matches:

- M1 = 2: 1
- M2 = 2: 1
- M5 = 2: 1
- M6 = 2: 1
- Total: 1 + 1 + 1 + 1 = 4 exact-value matches

The stream-aligned fit has two exact-value matches and one range match:

- M1 = 2: 1
- M4 = 0 or 1, with the observed value 1: range match, not an exact-value match
- M5 = 2: 1
- M6 = 0: 0
- Total: 1 + 0 + 1 + 0 = 2 exact-value matches

The result is platform, 4 of 4. The squad's stream-aligned name no longer matches its operating shape.

**Decision rule:** highest fit is the operating type. The payments squad's highest fit is platform at 4 of 4, so the decision is a rename.

### 5. Named against operating, and the bill

| Team | Named type | Operating type | Fit | The mismatch in one line | Cost this period, measured | Who pays it | The move |
|---|---|---|---:|---|---|---|---|
| Payments squad | stream-aligned | platform | 4 of 4 | The squad is named for a user-facing flow, but its evidence shows an internal product with interfaces consumed without tickets |  |  | Rename the squad to platform, and publish Quay API v1, the decline event stream and the ERP export I-11 as its interfaces |

The cost is left blank because no handoffs per change, median days waited, open ticket age or people embedded with no end date is measured in HC46. The assessment does not convert the mismatch into an unmeasured cost.

The published interface set is:

| Interface | Consumer or purpose | Evidence |
|---|---|---|
| Quay API v1 | Internal payment capability for the checkout surfaces and order service | Quay is the payment service operating after the drain |
| Decline event stream | Fraud and risk consumption without a ticket | DEP-6 was delivered through the decline event stream with no ticket |
| I-11, Finance ERP export | Nightly reconciliation output for finance operations | I-11 is the published finance boundary |

### 6. Interaction mode audit

| Consumer, provider | Mode named | Mode actually running | Evidence | Running for | Verdict |
|---|---|---|---|---|---|
| Finance operations, payments squad | Collaboration | Collaboration, then X-as-a-Service | Drain collaboration ran from 2026-07-08 to 2026-09-15 and ended on schedule into I-11 | 10 weeks | correct |
| InfoSec, payments squad | Facilitating | Facilitating | InfoSec has a facilitating engagement with an exit at DEP-7 | 27 weeks | correct, with exit at DEP-7 |
| Data engineering, payments squad | X-as-a-Service | X-as-a-Service | The legacy table-shape contract is ADR-0002, with reporting migration tracked by DEP-4 | 26 weeks | correct |

Finance operations' collaboration has ended. The continuing relationship is an X-as-a-Service contract through I-11, so the squad should not preserve the drain collaboration as the default operating model.

InfoSec remains in a facilitating mode until its exit at DEP-7. The engagement has a named exit rather than an unbounded embedding.

Data engineering's relationship is X-as-a-Service because ADR-0002 defines the legacy table-shape contract and DEP-4 records the migration away from it. That contract remains explicit while the table shape is retained.

## Reading the result

The payments squad scores 4 of 4 for platform and 3 of 4 for stream-aligned. Its named type is therefore wrong, not the team. The correct move is a rename, not a reorganisation.

The rename should make three interfaces visible:

1. Quay API v1
2. The decline event stream
3. I-11, the nightly Finance ERP export

M2 is supported by DEP-6 being met through the decline event stream with no ticket. M3 is not a platform fit marker, but its zero is consistent with the squad having no temporary engagements. M5 confirms that the squad holds one domain, card payments with reconciliation, rather than several unrelated domains.

The interaction audit supports the same reading:

- Finance operations' drain collaboration ran from 2026-07-08 to 2026-09-15, lasted 10 weeks, and ended on schedule into X-as-a-Service through I-11.
- InfoSec is facilitating, with an exit at DEP-7.
- Data engineering is using X-as-a-Service through the ADR-0002 contract, with DEP-4 tracking the eventual reporting migration.

The assessment does not price a wait cost because HC46 does not measure one of the worksheet's permitted cost units. The blank is intentional.

## ILLUSTRATIVE example

Invented for Harbourgate's fictional payments squad. All numbers and identifiers are ILLUSTRATIVE.

| Team | Named | Digits M1 to M6 | Operating type | Fit | Cost this period |
|---|---|---|---|---:|---|
| Payments squad | stream-aligned | 2, 2, 0, 1, 2, 2 | platform | 4 of 4 |  |

The squad was named stream-aligned, but its 4 of 4 platform fit is higher than its 3 of 4 stream-aligned fit. Its interfaces are Quay API v1, the decline event stream and I-11. Finance operations' collaboration ended on schedule into the I-11 service relationship. InfoSec's facilitating engagement has an exit at DEP-7, and data engineering consumes the ADR-0002 table-shape contract as X-as-a-Service.

## The decision it feeds

Rename the payments squad from stream-aligned to platform in the next planning and charter records.

The rename should also make the squad's internal product boundaries explicit:

- Quay API v1 is the payment capability interface.
- The decline event stream is the self-service interface used by fraud and risk through DEP-6.
- I-11 is the finance operations interface.

The squad remains responsible for one domain, card payments with reconciliation. No measured cost is entered because HC46 contains no permitted cost figure.

## Where the output lands

- [Capacity plan](../templates/planning/capacity-plan.md), section 2, where the squad's supply is planned as a platform team, and section 4, where consumer demand is represented through published interfaces rather than assumed embedded work
- [Program charter](../templates/planning/program-charter.md), section 4, where the operating type replaces the stream-aligned name if a charter is used
- [Dependency register](../templates/execution/dependency-register.md), section 1, where DEP-4, DEP-6 and DEP-7 continue to describe the consumer and enabling relationships
- [Harbourgate journey](harbourgate-journey.md), which records the product, cast and shared identifiers
- [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), HC46 and HC47, which provide the assessment digits and post-drain evidence

## Re-run trigger

Re-run when the payments squad is added to, split, merged or renamed, or when a reporting line moves.

Re-run at the start of the next planning period before the capacity plan's supply table is filled. Re-run earlier if the published interfaces change, if the finance relationship returns to collaboration, if the InfoSec engagement passes DEP-7, or if DEP-4 changes the data engineering contract.

## When this method misleads you

A post-drain record can overstate platform fit if the interface is documented but consumers still need a named person. This assessment therefore uses DEP-6 being met with no ticket as evidence for M2, rather than treating the existence of an event stream as sufficient by itself.

A team can also look platform-shaped because a temporary migration has created several consumers. The payments squad's M5 score remains tied to the single domain recorded in HC46, card payments with reconciliation. The assessment does not infer additional domains from the number of interfaces.

The interaction audit can also hide a collaboration that has ended but whose meetings continue by habit. Finance operations' collaboration is recorded as ended on 2026-09-15, with the relationship continuing through I-11 as X-as-a-Service. InfoSec is not labelled permanent enabling because DEP-7 supplies an exit. Data engineering is X-as-a-Service because ADR-0002 is the contract, while DEP-4 records the remaining migration work.

The method describes how work moves. It does not decide whether Quay's roadmap is valuable, whether the legacy table shape should be removed sooner, or whether the squad needs more people. Those questions remain with the capacity plan and the dependency register.

## Feeds

- [Capacity plan](../templates/planning/capacity-plan.md), sections 2 and 4, for platform supply and measured demand
- [Program charter](../templates/planning/program-charter.md), section 4, for the operating type and squad name
- [Dependency register](../templates/execution/dependency-register.md), section 1, for DEP-4, DEP-6 and DEP-7
- [Solution architecture one-pager](../templates/architecture/solution-architecture.md), sections 2 and 3, for Quay's published boundaries and integration points
- [Stakeholder map](../templates/execution/stakeholder-map.md), section 2, for the real owners of finance, InfoSec and data engineering relationships
- Reviewed as part of the post-drain operating review, after Gate 6, using HC46
- Method background: [triad decision rights](../knowledge/roles/triad-decision-rights.md) and [PM specializations](../knowledge/roles/specializations.md); [knowledge index](../knowledge/INDEX.md)
