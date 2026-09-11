# Decision Log: Sahulat Bill Pay

Fills [templates/execution/decision-log.md](../templates/execution/decision-log.md). Everything here is invented: Sahulat is a fictional mobile-money wallet run by a fictional Pakistani electronic money institution, Hira Baig its only fictional product manager, and every date, name and figure in this log is ILLUSTRATIVE, drawn from the shared data sheet in [the Sahulat journey](sahulat-journey.md) rather than from any real wallet, market or regulator. See the [examples index](README.md).

**Initiative:** Sahulat Bill Pay · **Log owner:** Hira Baig · **Started:** 2026-01-16
**Entries:** 8 · **Open reversals:** 0 · **Last entry:** 2026-08-28
**Status:** reviewed at every gate through Gate 6 (PIVOT, 2026-08-28); next review opens with the 2026-09-07 DISCOVER pass

Stage: all stages, read at every gate in [STAGE-GATES](../os/STAGE-GATES.md)
Knowledge: [knowledge index](../knowledge/INDEX.md)
Skill: [decision-memo](../skills/decision-memo/SKILL.md)

## 1. Index

Newest first, so a reader finds the entry in a glance and reads section 3 only for the one that matters.

ID numbers come from the journey's shared identifier sheet, not from dates: D3 (decided 2026-04-03) sits above D4 (decided 2026-03-20) here because the index and section 3 both order by decision date, not by id.

| ID | Decision, in one line | Date | Decider | Type | Status |
|---|---|---|---|---|---|
| D8 | Pivot Rel-2 to agent-assisted bill pay, not persist on balance-first or sunset | 2026-08-28 | Faisal Mirza | scope | holding |
| D7 | Pause the nationwide step four days on the M3 guardrail breach | 2026-07-10 | Zainab Qureshi | other | holding |
| D6 | Stage the rollout: 600 Lahore pilot agents before nationwide | 2026-07-01 | Faisal Mirza | sequencing | holding |
| D5 | Drop Mehran Water from Rel-1 after its reference-validation failures | 2026-05-21 | Hira Baig | scope | holding |
| D3 | Reject Darya BillLink; integrate BillBridge directly | 2026-04-03 | Faisal Mirza | vendor | holding |
| D4 | Set the Rel-1 customer fee at PKR 0 per bill | 2026-03-20 | Faisal Mirza | pricing | holding |
| D2 | Define at one-pager weight with stories and criteria, not the full BRD/FRD stack | 2026-03-05 | Hira Baig | other | holding |
| D1 | Enter DISCOVER on bill pay, not a keep-balance cashback promotion | 2026-01-16 | Faisal Mirza | sequencing | holding |

## 2. When to log, and when not to

Hira Baig's bar, applied to every candidate entry since 2026-01-16: an entry earns a row when it closed off an option that cost something to give up, not when it merely recorded a task.

| Log it | Do not log it |
|---|---|
| Two or more people debated it for over ten minutes | It was never in question |
| Anyone could reasonably reopen it in three months | It is a task, and the tracker already holds it |
| It closed off an option that cost something to give up | It restates something already decided; link the original instead |
| A new joiner would otherwise ask "why is it like this?" | It changes system structure, which belongs in an [ADR](../templates/architecture/adr.md) |
| It was decided under time pressure or with thin evidence | It is a preference nobody will act on |

**Log within a day of deciding.** Every entry below is dated the same day as its decision.

## 3. Decisions

ADR-2 (the USSD payment as a two-phase state machine with an idempotency key, 2026-04-09) and ADR-3 (bill-pay postings through the existing trust-account sub-ledger, no new ledger, 2026-04-09) never earned a row here: both are structural, never argued as a business option, and are filed in the product workspace's `architecture/` folder, filled using [templates/architecture/adr.md](../templates/architecture/adr.md) per [PRODUCT-WORKSPACE.md](../os/PRODUCT-WORKSPACE.md), linked rather than duplicated. ADR-1 does have a matching entry, D3, because rejecting the Darya rail was also a vendor and revenue-share call.

### D8: Pivot Rel-2 to agent-assisted bill pay, not persist on balance-first or sunset

- **Date:** 2026-08-28 · **Decider:** Faisal Mirza
- **Type:** scope
- **Context:** the review window closed 2026-08-17 (N55); the 2026-08-21 post-launch review found the pay-from-balance hypothesis missing badly, and agents, not customers, turned out to be doing most of the paying.
- **Options considered:** A. persist, funding a second push at balance-first (more reminder SMS, a savings feature); B. pivot to agent-assisted bill pay, the wallet as record and receipt, not funding source; C. sunset bill pay and reassign the capacity.
- **Decision and rationale:** B. Bills funded from a balance held over 48 hours reached 9 percent against a 50 percent target, while 78 percent were funded by a cash-in within two hours of payment, matching theme T2, seen in six of eight customer sessions. M2 missed its target more than fivefold (9 against 50 percent, N43); sunsetting discarded a moved north star and a working USSD state machine, lookup and BillBridge integration. Given up: the pay-from-balance hypothesis, Kamran as a persona, and the saved-reference, app-flow and reminder-SMS work built for it. Supersedes the one-pager's proposal; does not reverse D1, since bill pay itself remains the bet. Commits to: a proposed PKR 5 per bill agent-assistance commission (N39, target). Open: Bilal Hasan owns commission schedule v8, due 2026-09-30.
- **Evidence it rested on:** the 2026-08-21 review: 31,200 bills against a 40,000 target, 9 percent against 50 percent, 78 percent cash-in-funded, Usman Javed's field observation (41 of 53 payments agent-performed), and premortem risk R6, scored 2 of 5, which is the risk that arrived.
- **What would change our mind:** the 2026-09-07 DISCOVER pass, centred on Rafiq, finding the agent-performed share below half at the next field observation.
- **Reverses or is reversed by:** none.
- **Who was told:** Gate 6 attempt 1 sign-off, 2026-08-28; the review itself circulated 2026-08-21 to Faisal Mirza, Zainab Qureshi, Tariq Sohail, Amna Rasheed, Bilal Hasan and Naveed Akhtar.

### D7: Pause the nationwide step four days on the M3 guardrail breach

- **Date:** 2026-07-10 · **Decider:** Zainab Qureshi, named halt-caller on the M3 guardrail
- **Type:** other
- **Context:** in launch week, a 2026-07-09 timeout spike took LD-1's daily USSD bill-pay session completion reading below the 90 percent floor (N67), with duplicate-payment tickets already arriving.
- **Options considered:** A. continue toward the planned 2026-07-20 nationwide date; B. pause nationwide until the timeout fix ships and completion recovers; C. roll back Rel-1 from the 600 pilot agents entirely.
- **Decision and rationale:** B. The floor and Zainab's name against it existed so this call would not need a meeting. Continuing risked carrying the dropped-session defect, the AC-8 resume half already accepted as a Gate 4 miss, onto the whole network; a full rollback discarded four days of pilot behavior over a fix already in progress. Given up: the 2026-07-20 nationwide date, moved four days to 2026-07-24.
- **Evidence it rested on:** the Falak Telecom gateway logs on dashboard LD-1 (N67, below 90 percent), duplicate-payment tickets already arriving, and the Gate 4 attempt 1 record naming the AC-8 miss. Later (2026-07-12): the week closed at 87 percent with 61 duplicate-payment tickets (N46, N47).
- **What would change our mind:** completion back above 90 percent for a full week with the timeout fix verified. Later (2026-07-24): the fix shipped 2026-07-14, completion held above the floor for the week that followed, and nationwide proceeded 2026-07-24 as this entry's condition closed.
- **Reverses or is reversed by:** none; delays but does not reverse D6.
- **Who was told:** the on-call channel and Tariq Sohail, owner of the Gate 5 float-hotline condition, both 2026-07-10; Faisal Mirza, who approved the pause message; and agents, via the pause message Zainab derived from the comms plan's holding statement, 2026-07-10; logged against the guardrail row in the north star sheet.

### D6: Stage the rollout: 600 Lahore pilot agents before nationwide

- **Date:** 2026-07-01 · **Decider:** Faisal Mirza
- **Type:** sequencing
- **Context:** Gate 5 attempt 1 reached CONDITIONAL GO with one condition open, an agent float top-up hotline owned by Tariq Sohail, and premortem risk R1 (float running out on a bill-peak day) already scored likelihood 4 of 5.
- **Options considered:** A. launch nationwide to all active agents on day one; B. stage 600 Lahore pilot agents first, nationwide once the hotline condition closes; C. hold the whole launch until the hotline is live everywhere.
- **Decision and rationale:** B. A day-one nationwide launch risked R1 at national scale before the hotline existed; holding the whole launch traded a bounded pilot risk for an open-ended delay against the board's year-end key result. Given up: two weeks of nationwide key-result movement (2026-07-06 to the planned 2026-07-20) and one cutover instead of two.
- **Evidence it rested on:** premortem risk R1, 2026-04-08, and the Gate 5 attempt 1 condition itself.
- **What would change our mind:** the float top-up hotline going live before 2026-07-06, which would have removed the case for staging at all.
- **Reverses or is reversed by:** none.
- **Who was told:** Gate 5 attempt 1 sign-off, 2026-07-01, and the launch comms plan's audience rows.

### D5: Drop Mehran Water from Rel-1 after its reference-validation failures

- **Date:** 2026-05-21 · **Decider:** Hira Baig
- **Type:** scope
- **Context:** on 2026-05-19, three of ten Mehran Water test bills failed reference validation, about three weeks before Gate 4, while Ravi Power and Chenab Gas passed the same suite cleanly.
- **Options considered:** A. ship Rel-1 on schedule with water included; B. delay all three billers until Mehran Water's format is fixed; C. drop water from Rel-1, ship electricity and gas, return water once fixed.
- **Decision and rationale:** C. A 30 percent failure rate on a live payment path was not something to carry into Gate 4; delaying all three held two working billers hostage to one broken one. SAHULAT-S7 was killed, its id spent, and the affected scope row and criterion were re-reviewed against Gate 2 rather than folded quietly into Gate 4. Given up: the all three household bills in one channel promise (N22). Later (2026-08-17): 6 tickets asking where water went arrived in the six weeks after the 2026-07-06 launch (N59).
- **Evidence it rested on:** the 2026-05-19 test log: three of ten failures against zero on the same suite for the other two billers.
- **What would change our mind:** Mehran Water's reference format passing the suite the other two billers cleared.
- **Reverses or is reversed by:** none.
- **Who was told:** engineering standup, 2026-05-21; the amended one-pager was re-reviewed by Faisal Mirza, Zainab Qureshi and Amna Rasheed that week rather than re-signed at a new gate attempt, since it removed scope.

### D3: Reject Darya BillLink; integrate BillBridge directly

- **Date:** 2026-04-03 · **Decider:** Faisal Mirza
- **Type:** vendor
- **Context:** Darya Bank's term sheet, 2026-03-30, offered a ready API and 210 billers against BillBridge's 160, with Zainab Qureshi estimating Darya would ship about nine weeks sooner. Theme T5, weekend and after-hours due dates producing surcharges (INT-004, 005, 008; E1), sharpened the comparison: BillBridge posts within 30 minutes, seven days a week, with T+1 settlement.
- **Options considered:** A. integrate Darya BillLink; B. integrate BillBridge directly; C. run both, routed by bill type.
- **Decision and rationale:** B. Darya's revenue share took 60 percent of the biller-paid fee, netting Sahulat PKR 4 a bill against BillBridge's PKR 7; Darya's 15:00 weekday cutoff would post a weekend-due bill the next working day, reproducing the surcharge this feature exists to remove, since three of eight customers' most recent due dates fell on a weekend and six of eight pay on the due date itself. Option C doubled integration surface for a fraction of the catalogue gain. Given up: about nine weeks to launch, and 210 billers against 160.
- **Evidence it rested on:** Darya's term sheet against BillBridge's rate card and posting SLA, and the interview sample's due-date and payment-timing counts.
- **What would change our mind:** Darya's cutoff moving past 20:00, seven days a week; this makes specific the vision's section 5 bank-rail revisit condition (same-day posting seven days a week).
- **Reverses or is reversed by:** none. The structural half of this call is filed once as ADR-1, filed in the product workspace's `architecture/` folder using [templates/architecture/adr.md](../templates/architecture/adr.md), linked rather than duplicated here.
- **Who was told:** engineering standup and the sponsor sync, both 2026-04-03. Later (2026-05-21): folded into the one-pager's not-doing list at its amendment.

### D4: Set the Rel-1 customer fee at PKR 0 per bill

- **Date:** 2026-03-20 · **Decider:** Faisal Mirza
- **Type:** pricing
- **Context:** Faisal's early framing leaned toward a per-bill fee, a new revenue line sized against the PKR 30 to 50 a bill-shop already charges.
- **Options considered:** A. charge a fee under the bill-shop's PKR 30 to 50; B. PKR 0 in Rel-1; C. fee on the app channel only, free on USSD.
- **Decision and rationale:** B. A counter fee on day one would blunt the exact value the problem framing states: a trip and a surcharge removed in one visit. Option C split a customer who moves between USSD and the app in ways nobody could explain. Given up: near-term fee revenue against the roughly 246,000-wallet addressable proxy.
- **Evidence it rested on:** the bill-shop fee range told in interviews, and the cost-of-inaction table; no data on demand at a nonzero fee exists, so this is judgment on launch-week optics.
- **What would change our mind:** adoption proving durable without a fee, or a repricing case once volume clears its target.
- **Reverses or is reversed by:** none.
- **Who was told:** the product channel, 2026-03-20; landed in the one-pager's not-doing list the same week.

### D2: Define at one-pager weight with stories and criteria, not the full BRD/FRD stack

- **Date:** 2026-03-05 · **Decider:** Hira Baig
- **Type:** other
- **Context:** at DEFINE's start, the stakes-audience-reversibility test that picks document weight was run; Amna Rasheed argued for the full BRD/FRD stack, since a regulator, the State Bank of Pakistan's EMI framework, is in scope for money settled to a biller. The tree in WHICH-DOCUMENT itself routes a sponsor-signed, regulator-in-scope decision to the full stack; option A overrides it.
- **Options considered:** A. one-pager weight with stories and acceptance criteria; B. the full BRD/FRD stack; C. a middle PRD weight without the regulatory annex.
- **Decision and rationale:** A, decided by Hira Baig as document owner, with Amna's objection recorded rather than resolved by vote. One squad, one release, and no new ledger expected argued for the lighter weight; the regulatory question was routed to a separate compliance memo (DEP-3, needed by 2026-05-29) rather than to promoting the whole document. Given up: the fuller audit trail a BRD/FRD pair would have produced, for reaching Gate 2 sooner without one.
- **Evidence it rested on:** the stakes-audience-reversibility test: stakes bounded, since the regulatory question was routed to a compliance memo rather than carried by document weight; audience limited to one squad and one release; reversibility high, since no new ledger was expected. No data resolves this against Amna's live objection, so it is judgment under a standing dissent.
- **What would change our mind:** the compliance memo finding bill pay outside the licence's permitted activities.
- **Reverses or is reversed by:** none.
- **Who was told:** the DEFINE kickoff, 2026-03-05, Amna's objection minuted. Later (2026-05-22): resolved by her compliance memo, needed 2026-05-29, delivered 2026-05-22.

### D1: Enter DISCOVER on bill pay, not a keep-balance cashback promotion

- **Date:** 2026-01-16 · **Decider:** Faisal Mirza
- **Type:** sequencing
- **Context:** the board's 2026 key result of 520,000 30-day active wallets, against 410,000 active at 2025-12-31, had nothing in the roadmap to close it. Faisal's first ask was a cashback promotion for balance-keeping. On 2026-01-12 Hira put 412 helpline calls asking about bill pay beside a 61 percent cash-out-within-48-hours pattern; the 2026-01-15 opportunity assessment named "customers will keep a balance in order to pay from it" the riskiest assumption either idea depended on.
- **Options considered:** A. fund the cashback promotion directly, skipping discovery; B. open a DISCOVER pass on bill pay, testing the helpline signal first; C. do neither, and let the gap ride another quarter.
- **Decision and rationale:** B. Bill pay had a named trigger (N13, 412 calls) and a sized ceiling (N65) the promotion did not have; the promotion rested on the same untested balance-keeping behavior, so testing it first was cheaper than building on it. Given up: about six weeks a promotion could have run in the time DISCOVER instead took (2026-01-16 to 2026-02-27).
- **Evidence it rested on:** the 2026-01-15 opportunity assessment, the helpline's 412 calls in four weeks, and the core ledger's Q4 2025 cash-in and cash-out pattern.
- **What would change our mind:** a repeat assessment showing a larger, better-evidenced gap elsewhere, or the helpline signal drying up before Gate 1.
- **Reverses or is reversed by:** none.
- **Who was told:** the product channel and the weekly sponsor sync with Faisal Mirza, both 2026-01-16.

---

## 4. How this log fails

| Failure mode | What it looks like | The rule |
|---|---|---|
| Winners only | Every entry lists what was chosen and no option that lost | An entry with no losing option is an announcement, not a decision. Reject it at review |
| Committee as decider | "The team decided", or three names in the decider field | Exactly one name. A group can agree; only a person can be asked why |
| Edited history | An old entry now describes what the team currently believes | Entries are immutable. A change of mind is a new id that names the old one |
| Rationale is the outcome | "We chose A because A was better" | The rationale names the trade: what A cost, and why that cost was acceptable |
| Silent staleness | Entries from two strategies ago, all still marked holding | Review status at every gate. Mark superseded by circumstance rather than leaving it |
| Log kept by one person | Entries stop when that person is on leave | The owner is named, and the review is on a recurring agenda, not in someone's memory |
| Nobody was told | A correct decision that half the team acts against | "Who was told" is a required field, and blank means the decision has not landed yet |

Applied to this log: the closest call was silent staleness, after D8's Gate 6 pivot left D1 to D7 all still marked holding with no stated reason; section 5's closing paragraph argues each one, rather than assuming the pivot leaves them untouched. The other six modes were checked against every entry, not assumed clear. Winners only and committee as decider were not observed: every entry lists a losing option, and every entry keeps exactly one named decider. Rationale is the outcome was not observed: every entry, including D2 and D4, states what was given up rather than only that the chosen option was better. Edited history was not observed: entries are immutable, and a later fact appears only as a dated "Later:" line appended after the original text, never as a rewrite of it. Nobody was told was not observed: "Who was told" is a required field, and it is filled in every entry. Log kept by one person is a real exposure here, not a false one: Hira Baig is the only PM and the only owner, so the whole log depends on one person by construction. The mitigation is not that the owner never changed; it is that status is reviewed at every gate (section 5), a standing item on that agenda rather than something resting in anyone's memory.

## 5. Gate review

Run at every stage gate, dated to the day the gate itself was attempted or, where conditional, the day it was signed.

| Gate | Reviewed on | Entries still holding | Marked superseded | New reversals |
|---|---|---|---|---|
| Gate 1 attempt 1: MORE DISCOVERY | 2026-02-20 | 1 (D1) | 0 | 0 |
| Gate 1 attempt 2: GO | 2026-02-27 | 1 (D1) | 0 | 0 |
| Gate 2 attempt 1: RETURNED | 2026-03-18 | 2 (D1, D2) | 0 | 0 |
| Gate 2 attempt 2: SIGNED | 2026-03-25 | 3 (D1, D2, D4) | 0 | 0 |
| Gate 3 attempt 1: REVIEWED AND ACCEPTED | 2026-04-15 | 4 (D1 to D4) | 0 | 0 |
| Gate 4 attempt 1: MET, one listed miss (AC-8 resume half) | 2026-06-10 | 5 (D1 to D5) | 0 | 0 |
| Gate 5 attempt 1: CONDITIONAL GO (float hotline, Tariq Sohail, by 2026-07-17) | 2026-07-01 | 6 (D1 to D6) | 0 | 0 |
| Gate 6 attempt 1: PIVOT (Gate 1 signal line unticked; Open: Sara Lodhi, by 2026-09-21) | 2026-08-28 | 8 (D1 to D8) | 0 | 0 |

No entry has been marked superseded by circumstance, and the pivot is checked against each of D1 to D7 rather than assumed clear of all of them. D1 holds: bill pay remains the product bet after the pivot, and D8 says so explicitly. D2 holds: the document-weight test turned on squad size, release count and the regulatory question, already resolved by Amna's memo; none of those three changed with the pivot, so the one-pager weight still fits the Rel-2 proposal. D3 holds: the vendor and revenue-share call was independent of which funding path a bill moves through; BillBridge still posts the bill either way. D4 holds: the PKR 0 launch-fee argument, removing the trip-and-surcharge cost in one visit, applies to agent-assisted pay as much as to balance-first pay. D5 holds: dropping Mehran Water was a data-quality call about one biller's reference format, unrelated to the funding hypothesis the pivot replaces. D6 holds: the staged-rollout sequencing had already run its course by 2026-07-24, before the pivot, and is not reopened by it. D7 holds: the guardrail pause is a closed, dated event that the pivot does not touch. D8 explicitly does not reverse D1: bill pay remains the product bet, only its funding mechanism changes.

## Exit gate

- [x] Every entry has a matching index row, and every index row has an entry: D1 to D8 in both section 1 and section 3.
- [x] Every entry has exactly one decider, by name: Faisal Mirza (D1, D3, D4, D6, D8), Hira Baig (D2, D5), Zainab Qureshi (D7).
- [x] Every entry lists the options that lost, not only the winner: three options in every entry.
- [x] Every rationale names what was given up, not only what was gained: stated in every entry.
- [x] Every entry records the evidence it rested on, or says plainly that it was judgment: D2 and D4 say so plainly; the rest cite a dated artifact.
- [x] Every entry names what would change our mind: stated in every entry.
- [x] No entry has been edited into a different decision; reversals are new ids: none of D1 to D8 reverses another; D8's non-reversal of D1 is stated in its own entry.
- [x] Entry dates are within a day or two of the decisions they record: every entry is dated the day of the decision.
- [x] Status has been reviewed at the most recent gate, and stale entries are marked superseded rather than left holding: reviewed 2026-08-28 in section 5; none found stale, with the reasoning stated rather than assumed.
- [x] Structural technology decisions are in [ADRs](../templates/architecture/adr.md), linked rather than duplicated here: ADR-1 named from D3, filed in the product workspace's `architecture/` folder; ADR-2 and ADR-3 named in section 3's opening note as decisions this log correctly never logged, filed the same way.
- [x] The worked example above has been removed: no worked micro-example appears in this file.

Reviewed and current as of 2026-08-28: Hira Baig, log owner. Open: Bilal Hasan owns the agent commission schedule v8 that D8's pivot requires, due 2026-09-30; whether it earns its own entry here is Hira Baig's call under section 2's bar.
