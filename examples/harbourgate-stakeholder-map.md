# Stakeholder Map: Harbourgate Checkout Modernization (Quay)

Fills [templates/execution/stakeholder-map.md](../templates/execution/stakeholder-map.md). Everything here is invented: Harbourgate is a fictional mid-market retailer, Quay is the fictional payment service this map tracks, every person named below is fictional, and every number, date and identifier is ILLUSTRATIVE, carried from the shared data sheet in the [Harbourgate journey](harbourgate-journey.md) rather than from any real payments stack, market or organisation. See the [examples index](README.md).

**Initiative:** Harbourgate Checkout Modernization (Quay) · **Map owner:** Ife Adeyemi, Product Manager · **Last reviewed:** 2026-10-14, at Gate 6

Stage: DISCOVER through OPERATE, first required at [Gate 2: requirements signed off](../os/STAGE-GATES.md), first drawn at or before Gate 2 attempt 2, 2026-04-07
Knowledge: [Grove on managerial output](../knowledge/high-output-management.md)
Skill: [stakeholder-update](../skills/stakeholder-update/SKILL.md)

## 1. The map

Thirteen named people, drawn from the cast table in the [Harbourgate journey](harbourgate-journey.md). Dani Ferreira, Kestrel's merchant success manager, is the journey's one counterparty and is tracked on the integrations register instead of here, since she carries no decision inside Harbourgate. Interest and influence are scored as this map's owner would say them to the person's face.

| Name | Role or function | Interest (H/M/L) | Influence (H/M/L) | RACI on this initiative | Cadence | Current concerns (their words, not yours) |
|---|---|---|---|---|---|---|
| Ife Adeyemi | Product Manager, owner of the product and every artifact | H | H | A | Daily standup; chairs every gate attempt | "I am the one who benefits if the completion date holds. I should not be the only voice deciding whether Gate 5 goes" (2026-06-16, ahead of the Gate 5 attempt 1 NO-GO) |
| Tomasz Wierzbicki | Engineering Lead; design owner; cutover lead with authority to abort | H | H | R | Daily standup; abort authority for any step that is not a clear N17 trigger, on-call calls the trigger without discussion | "Nine hours in, the file count still was not converging. Nobody's job is to keep going once that is true" (2026-06-13, Rehearsal 1, N37) |
| Bea Lindqvist | Senior Engineer, payments; caretaker of the wrapper from 2026-04-24; owns Quay's reconciliation service | H | M | R | Weekly risk and dependency review | "I inherited a wrapper nobody had touched since 2021. I am not debugging four years of undocumented behaviour in the middle of a migration" (2026-04-24, when R2 closed) |
| Noor Haddad | QA Lead | H | M | C | Gate reviews; facilitated the postmortem | "We wrote two failure scenarios down and never exercised either one. That is not a pass" (2026-06-03, Gate 4 attempt 1, NOT MET) |
| Priya Raman | Head of Finance Operations | H | H | A | Daily during a drain; monthly otherwise | "A £50-a-day tolerance only means something if the straddle set actually drains. Until it does I cannot close on time" (2026-06-19, ADR-0004, N35, N36) |
| Rohan Iyer | Chief Financial Officer, sponsor and budget owner | M | H | A | Monthly sponsor sync; ad hoc at any accepted-risk decision | "One provider is one point of failure. I will accept that risk in writing, but I want it reviewed on a calendar, not left as a line in a register" (2026-08-24, D-022, R4) |
| Saoirse Whelan | Fraud and Risk Lead | H | M | C | Weekly risk review during BUILD; monthly after | "My team saw the same card authorised twice before anyone on the payments side did. I need the decline stream, not a dashboard built after the fact" (2026-05-19, R1) |
| Hamid Qureshi | Information Security Lead and PCI DSS owner | H | H | A | Gate 3 review; monthly DEP-7 and R8 review through 2027-01-15 (wrapper log deletion, N58) | "The wrapper's logs held a name and a masked card number in plain text for as long as nobody looked" (2026-04-08, STRIDE walk, F1). Later: "Scoring a finding a 4 is not the same as it being safe" (2026-06-16, F2 re-routed as R14) |
| Lena Baptiste | Head of Store Operations, 61 shops and their kiosks | L at Gate 2, M by Gate 6 (see section 4) | H | A | Named owner for the kiosk SLO (N32) and BR-004 at Gate 2 attempt 2, 2026-04-07, with the number itself not agreed at that signing; she agreed the number only on 2026-06-25, once she had the walk-through of what the cutover does to a shop at opening; no standing cadence until the store cohorts were scoped, then weekly through the store cohorts, continuing on R11 (kiosk fallback usage) through its 2026-10-23 review | "My name has been on the kiosk SLO since April and nobody has shown me what the cutover does to a shop at opening. Sixty-one shops, and the earliest opens at eight" (2026-06-25, cutover plan v2 drafted, N1, N32, N48, BR-004) |
| Callum Fraser | Support Lead | M | M | C | Briefed ahead of every cohort; on-call rota review | "I signed Gate 5 with a condition, not a blank cheque. My team needs the runbook before the first ticket, not after" (2026-07-08, Gate 5 attempt 2, GO WITH CONDITIONS) |
| Grace Mbeki | Data Engineering Lead | M | M | C | Monthly, tied to DEP-4's progress | "Reporting reads the old table shape. If that shape changes before I have moved it, the order-history page breaks quietly, not loudly" (2026-04-08, ADR-0002) |
| Anneliese Vogt | Legal Counsel and Data Protection Officer | M | H | R | Fortnightly contract check-in through 2026-12-15 (contract termination), then to 2027-06-15 for the provider portal wind-down (N52) | "Ninety days is the floor in both contracts, not a target. If the notice date slips, the termination date moves with it" (2026-09-14, D-023, N51) |
| Ines Castellanos | Design Lead | L | L | I | Informed at each gate; no standing cadence | "Guest checkout stays exactly as it is while this runs. I need that written down, not assumed, since it is the thing everyone wants to bolt onto a migration" (2026-04-07, Gate 2 attempt 2, out-of-scope table carried from the seed) |

## 2. Decision areas

Eight areas, each with exactly one Accountable name, covering the ground this journey actually contested: scope, money, the cohort mechanics of the cutover, and the two closures (PCI scope, contract termination) that only complete after the last shop shifts.

| Decision area | Responsible | Accountable (exactly one) | Consulted | Informed |
|---|---|---|---|---|
| Scope changes | Tomasz Wierzbicki | Ife Adeyemi | Rohan Iyer, Hamid Qureshi | Noor Haddad, Callum Fraser |
| Budget | Ife Adeyemi | Rohan Iyer | Priya Raman | Tomasz Wierzbicki, Bea Lindqvist |
| Go or no-go per cohort | Tomasz Wierzbicki | Ife Adeyemi | Priya Raman, Noor Haddad, Callum Fraser, Ines Castellanos, Grace Mbeki, Anneliese Vogt | Rohan Iyer, Lena Baptiste |
| Abort during a cutover window | On-call engineer (rotation) | Tomasz Wierzbicki | None (the N17 trigger is called by on-call without discussion) | Ife Adeyemi, Lena Baptiste, Callum Fraser |
| Reconciliation sign-off | Bea Lindqvist | Priya Raman | Grace Mbeki | Rohan Iyer, Ife Adeyemi |
| PCI scope | Bea Lindqvist | Hamid Qureshi | Anneliese Vogt | Ife Adeyemi, Rohan Iyer |
| Store cohort schedule | Tomasz Wierzbicki | Lena Baptiste | Ife Adeyemi, Bea Lindqvist | Callum Fraser |
| Contract termination | Anneliese Vogt | Rohan Iyer | Ife Adeyemi, Priya Raman | Hamid Qureshi, Grace Mbeki |

"Go or no-go per cohort" carries a named tension the map does not smooth over: Ife Adeyemi is Accountable for the call and also the person whose completion date it moves, which is the conflict she named against herself on 2026-06-16 rather than leaving it for someone else to notice. It stayed with her because no other name in the cast held both the cutover context and the authority to halt scope. Two checks cover it, both recorded in the release readiness sign-offs rather than smoothed away: "abort during a cutover window" sits with Tomasz Wierzbicki, a genuinely separate Accountable with authority to abort any step that is not a clear N17 trigger, while on-call calls an N17 rollback without asking anyone; and the conflict itself was accepted, not just declared, by Rohan Iyer, the sponsor whose budget the completion date serves, at Gate 5 attempt 2 on 2026-07-08, the independent check this decision area does not otherwise carry.

## 3. Engagement plan for the difficult quadrant

One person sits in the dangerous quadrant on this initiative: high influence, low interest, until the work reached something she actually ran.

| Name | What would move them from bystander to sponsor | Who engages them | By when |
|---|---|---|---|
| Lena Baptiste, Head of Store Operations | Walk the 61-shop store cohort schedule against the agreed shift window (N48: 06:00 to 07:30 local, before the earliest shop opens at 08:00), so every shift lands and completes before a till opens, plus the per-shop rollback path if a kiosk cohort fails mid-window | Tomasz Wierzbicki, with Ife Adeyemi present for the schedule and Bea Lindqvist for the rollback mechanics | 2026-07-31, before the first kiosk cohort (6 shops) on 2026-08-03 |

The walk happened on 2026-06-25, when cutover plan v2 was drafted with the store shift window in it, and was confirmed again when Gate 5 attempt 3 returned GO for the store cohorts on 2026-07-29 and DEP-5, the kiosk firmware update across all 61 shops, delivered on 2026-07-30: the two closures her own team had been waiting on before the first cohort, not the legal gap G1, which was Anneliese Vogt's and closed separately on 2026-07-31. By 2026-08-17, when the third and largest store cohort (61 shops) shifted, her weekly kiosk-use report was already a standing artifact rather than a new ask, and R6 (a kiosk cohort flip failing while shops trade) closed the same day, having never occurred. She moved from bystander to sponsor between those two dates, not because her interest in payment architecture grew, but because the schedule stopped being something that happened to her shops and became something she had timed herself.

## 4. Map health

- Stakeholders who joined or left since last review: none. Dani Ferreira remains off this map by design, tracked as a counterparty on the integrations register rather than as a Harbourgate stakeholder.
- Lena Baptiste's interest score: L at Gate 2 attempt 2, 2026-04-07, which is the score section 3's difficult quadrant is built on, since that is what put her there in the first place. It read M by this review: her cadence had settled into a standing weekly report by the third store cohort (2026-08-17) rather than an unprompted ask, the change section 3 narrates.
- Concerns that changed since the last review, Gate 5 attempt 2 on 2026-07-08: Callum Fraser's condition closed when the runbook published and support was briefed on 2026-07-10 (condition C2, two days after that review); Rohan Iyer accepted R4 in writing, D-022, 2026-08-24; Lena Baptiste's interest moved from L to M between the store window walk (2026-06-25) and the third store cohort (2026-08-17), above; Anneliese Vogt sent the termination notices, D-023, 2026-09-14; Grace Mbeki's concern stays open, tracked against DEP-4, due 2027-02-27. Saoirse Whelan's concern closed on 2026-07-06, two days before the 2026-07-08 review, and was already reflected there rather than being new since.
- This map was not reviewed at Gate 5 attempt 3 (2026-07-29) or attempt 4 (2026-08-26), so the gap between the 2026-07-08 review and this one is 14 weeks against the risk register's weekly cadence. Recorded here rather than smoothed over: the next review should not let a gate attempt pass without one.
- Anyone with veto power not yet met face to face: none. Lena Baptiste, the last name in this category, was walked through the store window in section 3 before the first kiosk cohort; Rohan Iyer's R4 acceptance (D-022, 2026-08-24) was taken in a scheduled sponsor sync, not by email.

## How this map fails

<!-- A stakeholder map drawn from the org chart tells you who exists. The
     useful version tells you who can stop you and what they want, which is
     rarely the same list. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Titles instead of interests | Boxes with roles, and nothing about what each person is protecting | Every row carries an interest: what they want, and what they fear |
| No record of what they can block | Names and influence ratings, and no specific decision attached | Name the decision each person can stop. Influence with no decision attached is gossip |
| Drawn once | An org chart from before the last reorganisation, still cited | Re-read it at the cadence of the risk register, and date the review |
| Influence guessed | The senior title is assumed powerful, and the real blocker is elsewhere | Cite a recent thing the person actually stopped or unblocked |
| No plan for the person against it | The objector is listed and then avoided until launch | One named next step per opponent, before the work starts rather than after |

### What this looked like on this map

| Person and role | What they want | What they fear | What they can block | Evidence of influence | Next step |
|---|---|---|---|---|---|
| Grace Mbeki, Data Engineering Lead | Reporting keeps reading the table shape it reads today until DEP-4 moves it | A column change lands on that table before DEP-4 migrates reporting off it | Any pull request touching the legacy table's columns, held for her sign-off under R5 | Flagged in her own words at ADR-0002 (2026-04-08); R5's mitigation names the block by hand, not by policy: "any pull request touching that table's columns is blocked in review until Grace Mbeki signs off" | None open: DEP-4 is on track for 2027-02-27, ahead of the table's 2027-03-31 removal, reviewed monthly |
| Callum Fraser, Support Lead | The runbook in place before the first ticket, not after | A cohort ships and support is briefed the same day it fails | Gate 5 sign-off for the cohort it covers | Signed Gate 5 attempt 2 GO WITH CONDITIONS rather than GO: condition C2 held rollout to cohort 1 until the runbook published and support was briefed, 2026-07-10 | None open: C2 closed three days before cohort 1 started, 2026-07-13 |
| Noor Haddad, QA Lead | Failure scenarios exercised, not just written down | A pass recorded against a scenario nobody ran | UAT sign-off at Gate 5 | Held Gate 4 attempt 1 to NOT MET on exactly this point, then signed Gate 5 attempt 2 GO, without condition, against rehearsal 3's clean run | None open: UAT signed 2026-07-08 |

No one on this map is currently opposed to the plan it carries. The one recorded disagreement, the engineering team's preference in ADR-0003 for a routing layer over all three providers instead of Kestrel alone, was rejected in ADR-0003 on 2026-04-09 and accepted at Gate 3 on 2026-04-10; it was never a position held by a name this map tracks separately from Tomasz Wierzbicki, who co-signed the ADR that rejected it. If it resurfaces, ADR-0003 already names the reopening condition, a Kestrel availability miss or an R4 outage, and the accountable acceptor of R4, Rohan Iyer.

## Exit gate

- [x] Every function that can block launch appears in the map (legal, security, finance, support and operations checked explicitly): Anneliese Vogt (legal), Hamid Qureshi (security), Priya Raman (finance), Callum Fraser (support), Lena Baptiste (store operations)
- [x] Every decision area has exactly one Accountable name: eight rows in section 2, one Accountable each
- [x] Every high-influence stakeholder has a cadence with a real calendar entry: Ife Adeyemi (daily standup, chairs every gate attempt), Tomasz Wierzbicki (daily standup, abort authority on any non-N17 step), Priya Raman (daily during a drain, monthly otherwise), Rohan Iyer (monthly sponsor sync, ad hoc at any accepted-risk decision), Hamid Qureshi (Gate 3 review, monthly DEP-7 and R8 review through 2027-01-15), Lena Baptiste (weekly through the store cohorts, continuing on R11 through its 2026-10-23 review), Anneliese Vogt (fortnightly contract check-in through 2026-12-15, then to 2027-06-15 for the provider portal wind-down)
- [x] Concerns are recorded in the stakeholder's own words, dated: every row in section 1 carries a quoted concern and a date tied to a journey event
- [x] The difficult quadrant has an engagement row per person: one person qualifies, Lena Baptiste, and section 3 carries her row
- [x] The map has been reviewed within the current stage, not inherited from the last one: reviewed 2026-10-14 at Gate 6, section 4 records what changed since the prior review at Gate 5 attempt 2

Reviewed at Gate 6: outcomes verified, 2026-10-14, alongside D-024 (PERSIST for Quay, legacy sunset scheduled). The prior recorded review was Gate 5 attempt 2, 2026-07-08; section 4 also records that no review was logged at Gate 5 attempts 3 or 4, so this one closes a 14-week gap rather than picking up where the last one left off. Signed off by Ife Adeyemi, map owner and Product Manager, who is also the one name this map records as carrying a conflict of interest on the go or no-go decision area, disclosed rather than resolved by reassigning the row. See the [Harbourgate journey](harbourgate-journey.md) for the fuller cast, the decision log entries cited above, and how the store engagement in section 3 fits inside DELIVER's wider cutover story.
