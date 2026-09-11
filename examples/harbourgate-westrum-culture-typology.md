# Harbourgate Westrum Culture Typology

Fills [frameworks/assessment/westrum-culture-typology.md](../frameworks/assessment/westrum-culture-typology.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and amount is ILLUSTRATIVE, chosen to reconcile with the [Harbourgate journey](harbourgate-journey.md) and [coverage sheet](harbourgate-coverage-sheet.md), never to be quoted as a benchmark or copied as a target.

**Owner:** Ife Adeyemi, Product Manager · **Date:** 2026-06-18 · **Scored with:** Priya Raman, Head of Finance Operations, and Hamid Qureshi, Information Security Lead and PCI DSS owner · **Path:** from whoever first notices a problem to Tomasz Wierzbicki, who can stop a cohort · **Evidence:** HC40 in [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md)

## What it is for

This run tests how information travels on the Harbourgate payment migration path after the HG-INC-14 review. The evidence is dated and role-based: the fraud team, finance operations, a security reviewer and the product manager. The result is bureaucratic: information exists, moves through a proper channel, and can arrive after it matters or die at the boundary between functions.

The finding is not that people refused to speak. The dated events show information being raised, routed and sometimes acted on quickly. The structural problem is what happens between functions. DEP-2 remained requested until escalation, F2 remained in a backlog until the incident, and the finance analyst's report was traced quickly only after the dashboard was empty.

## Run it when

- A review has shown that information was known before action, as happened after HG-INC-14.
- A dependency or security finding is moving through a channel without an accountable cross-function response.
- A postmortem needs to distinguish a broken information path from a consequence that discourages speaking.
- A new trigger or register-routing rule needs to be checked against dated behaviour rather than stated values.

**Skip it when:** there is no authority to change how dependencies and findings are gathered, escalated or registered.

## Inputs you need first

- The five dated occasions in HC40, covering R1, DEP-2, F2, the empty finance dashboard and the declared Gate 5 conflict.
- The HG-INC-14 review and postmortem review of 2026-06-17.
- The risk and dependency records for R1, R14 and DEP-2.
- Two participants outside the scorer's reporting line: Priya Raman and Hamid Qureshi.

## The worksheet

### 1. The three types

| Behavior | 1, pathological | 2, bureaucratic | 3, generative |
|---|---|---|---|
| How information travels | held back, because carrying it is a personal risk | moves through the proper channel and lands after it matters | chased before anyone asks for it |
| What happens to the messenger | they pay for it once, visibly, and everyone else learns | heard, thanked, and never asked again | asked to come back with more, and taught where to look |
| Where responsibility sits | ducked, and whoever is holding it last loses | each function owns its box; the gaps between boxes are nobody's | shared across the boundary the work crosses |
| Contact across boundaries | discouraged, and going around a manager is an offence | permitted, unfunded, first thing cancelled | rewarded, and written into someone's objectives |
| What a failure produces | a cover story and a quiet reassignment | a fair process, a file, and no change to the system | an inquiry that changes something an outsider can point at |
| What a new idea meets | crushed, because it implies the old one was wrong | treated as a routing problem | welcomed, and given someone's time |

### 2. Evidence log

| # | What was known, and by which role | Date | Who they told | What happened next | Gap from known to acted on |
|---|---|---|---|---|---|
| E1 | The fraud team saw double authorisations, the event later recorded as R1 | 2026-05-19 | Product Manager and payments team | D-017 moved the migration to provider-by-provider flags on 2026-05-21 | 2 days |
| E2 | The dependency owner had not received Marlowe sandbox settlement files, DEP-2 | 2026-04-20 | Product Manager and dependency review | It was escalated on 2026-06-16, after remaining requested through the review path | 57 days |
| E3 | A security reviewer scored F2, the shared production SFTP drop, as a finding | 2026-04-08 | Security review and delivery path | It was routed to backlog HG-812, then reached the register as R14 on 2026-06-16 after HG-INC-14 | 69 days |
| E4 | A finance analyst saw that the finance dashboard was empty during the settlement-file incident | 2026-06-15 | Finance operations and the incident response path | The file was traced and the incident response began | 12 minutes |
| E5 | The Product Manager declared the conflict of deciding Gate 5 while owning the completion number | 2026-06-16 | Gate 5 review participants and sponsor path | The conflict was recorded during the NO-GO review | same day |

### 3. Scoring sheet

**Path scored:** from whoever first notices, including a finance analyst, fraud analyst or security reviewer, to Tomasz Wierzbicki, who can stop a cohort.

| Behavior | Score (1 to 3) | Event (ID and date) | Who else saw it |
|---|---|---|---|
| How information travels | 2 | E2, 2026-04-20 | Product Manager and dependency review participants |
| What happens to the messenger | 3 | E4, 2026-06-15 | Finance operations and incident response roles |
| Where responsibility sits | 2 | E3, 2026-04-08 | Security reviewer, Product Manager and delivery roles |
| Contact across boundaries | 2 | E2, 2026-04-20 | Product Manager, dependency owner and review participants |
| What a failure produces | 3 | HG-INC-14 review, 2026-06-17 | Postmortem participants, including responders |
| What a new idea meets | 2 | E2, 2026-04-20 | Product Manager and dependency review participants |

The six scores are dated against the evidence, and no score relies on atmosphere.

The intake rule does not change the reading. The two intake scores are 2 and 3, so neither is 1.

| Reading | Entry |
|---|---|
| Path scored | Whoever first notices, to Tomasz Wierzbicki, who can stop a cohort |
| Total | 2 + 3 + 2 + 2 + 3 + 2 = 14 |
| Floor | 2, on how information travels, where responsibility sits, contact across boundaries, and what a new idea meets |
| Band from total | 14, bureaucratic |
| Band after the intake rule | Bureaucratic, because neither intake behavior scored 1 |

**Intake rule:** a 1 on how information travels, or on what happens to the messenger, would cap the reading at pathological. That did not occur here.

## Reading the result

The total is 14 and the floor is 2. The reading is bureaucratic: information exists and moves through a recognised channel, but it can arrive after it matters or stop between functions.

The evidence has two different speeds:

- E4 shows a finance analyst's observation being traced in 12 minutes.
- E1 shows the fraud team's signal becoming D-017 in 2 days.
- E2 shows DEP-2 taking 57 days to escalate.
- E3 shows F2 taking 69 days to move from a security finding to the register.

The pattern is therefore not a messenger-consequence problem. It is a boundary and routing problem. A new forum is not the first fix. The structural fixes are:

1. Use a trigger instead of relying on a review date. A dependency at "requested" for more than the agreed period is escalated automatically at the weekly review. This is A6, due 2026-06-19 and verified by the register's review log on 2026-07-02.
2. Route findings above the register threshold into the risk register rather than leaving them in a backlog. F2 was initially scored 4 and routed to HG-812, but after HG-INC-14 the issue became R14 with a score of 9. The register must be the landing place when the finding crosses the threshold.
3. Keep one accountable name on each cross-function dependency row, with a bridge between the functions that must act.
4. Preserve rapid incident tracing, as shown by E4, while removing the need for an incident to force a boundary crossing.

The arithmetic is:

- Total = 2 + 3 + 2 + 2 + 3 + 2 = 14.
- Lowest score = 2.
- 14 falls in the bureaucratic band, 10 to 14.
- The intake cap does not apply because information travel is 2 and messenger treatment is 3.

## ILLUSTRATIVE example

This Harbourgate reading is ILLUSTRATIVE. The evidence is limited to roles and dated events from HC40.

E1 shows the fraud team raising the double-authorisation signal on 2026-05-19. D-017 followed on 2026-05-21, a gap of 2 days. E2 shows DEP-2 requested on 2026-04-20 and escalated on 2026-06-16, a gap of 57 days. E3 shows F2 scored on 2026-04-08 and reaching the register on 2026-06-16, a gap of 69 days. E4 shows a finance analyst noticing the empty dashboard on 2026-06-15, with the file traced in 12 minutes. E5 shows the Product Manager declaring the Gate 5 conflict on 2026-06-16, the same day.

| Behavior | Score (ILLUSTRATIVE) | Event |
|---|---|---|
| How information travels | 2 | E2, information travelled through the dependency channel, but DEP-2 remained requested for 57 days |
| What happens to the messenger | 3 | E4, the finance analyst's observation was acted on in 12 minutes |
| Where responsibility sits | 2 | E3, F2 sat between security review, backlog routing and the risk register |
| Contact across boundaries | 2 | E2, the dependency channel did not create timely action between Harbourgate and Marlowe support |
| What a failure produces | 3 | The 2026-06-17 review produced a written incident record and corrective actions |
| What a new idea meets | 2 | E2, the needed action was treated as a routing and dependency problem |

Total = 2 + 3 + 2 + 2 + 3 + 2 = 14 (ILLUSTRATIVE).

The floor is 2. The total bands as bureaucratic. The structural consequence is A6, due 2026-06-19 and verified on 2026-07-02, and the rule that findings above threshold land in the register rather than a backlog.

## The decision it feeds

Whether to add a channel or change a consequence.

This reading calls for a structural change, not a new forum:

- Keep the existing review path.
- Add A6 so a dependency at "requested" for more than the agreed period escalates automatically.
- Route findings above threshold into the register rather than a backlog.
- Carry R14 as the record of what happens when F2 is not routed to the register early enough.
- Use the register and dependency review to make cross-function ownership visible.

The result also sets the discount on status and backlog artifacts. A green status or a backlog entry is not sufficient evidence that a risk is being acted on. The dated event and the resulting register or decision entry are stronger evidence.

## Where the output lands

The output lands in the dependency and risk-routing changes following HG-INC-14:

- **A6:** automatic escalation for a dependency at "requested" for more than the agreed period, due 2026-06-19 and verified on 2026-07-02.
- **R14:** the pre-production production-SFTP-drop risk, entered in the register after the incident and closed on 2026-06-26 by A2.
- **Postmortem follow-up:** the 2026-06-17 review uses the finding to change the system rather than to ask for a new reporting forum.
- **Future dependency reviews:** the review log should show the trigger firing without requiring a person to decide whether to speak.

## Re-run trigger

Re-run after:

- A new sponsor, skip-level or incident-review facilitator.
- An incident where someone says afterwards that they already knew.
- A dependency remains in "requested" beyond the agreed period.
- A finding crosses the register threshold but remains in a backlog.
- A cohort is stopped because information arrived too late to matter.

The next run should preserve the same path definition and use dated events again, so movement can be compared rather than replacing one label with another.

## When this method misleads you

- **Scoring the company instead of the path.** This run is only about the Harbourgate payment migration path, from first observer to the person who can stop a cohort.
- **Scoring from one person's inbox.** Priya Raman and Hamid Qureshi do not report to Ife Adeyemi, so the score includes views outside the Product Manager's reporting line.
- **Turning it into a survey.** The result uses E1 to E5, not opinions about whether Harbourgate is generative.
- **Treating the 12-minute response as the whole culture.** E4 was fast, but E2 and E3 show that boundary routing can still take 57 and 69 days.
- **Treating the 69-day gap as messenger punishment.** The evidence supports a routing and ownership problem. It does not show that the security reviewer was punished for raising F2.
- **Calling F2 a permanent backlog item.** F2 was scored 4 initially, then became R14 at 9 after HG-INC-14. The point is to route a finding when it crosses the threshold, not to erase its earlier history.
- **Handing the bureaucratic label to the sponsor as a diagnosis.** Report the dated gaps, A6, and the register-routing rule. The label is for choosing the fix.

## Feeds

- [harbourgate-journey.md](harbourgate-journey.md), the R1, R14, DEP-2, F2 and HG-INC-14 records
- [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md), HC40, which records the five events, gaps, scores and result
- A6, the dependency trigger due 2026-06-19 and verified on 2026-07-02
- R14, the finding that moved from F2 and HG-812 into the risk register after HG-INC-14
- The risk register and dependency register, where the structural fixes must be visible
- The 2026-06-17 HG-INC-14 review, where the result is converted into corrective action
