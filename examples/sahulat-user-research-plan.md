# User Research Plan: Sahulat Bill Pay

Fills [templates/discovery/user-research-plan.md](../templates/discovery/user-research-plan.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, every session, quote, date and count below is fiction built to agree with the rest of the [Sahulat journey](sahulat-journey.md), and none of it describes any real wallet, market or regulator. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager, the only PM · **Date:** 2026-01-19 · **Status:** Synthesized (2026-02-16) · **Note-taker:** Usman Javed · **Journey:** [Sahulat Bill Pay](sahulat-journey.md), DISCOVER, feeds Gate 1 · **Sector cards:** [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md), [payments acquiring](../knowledge/domains/payments-acquiring.md)

## 1. Research questions

| # | Research question | Why it matters to the decision at hand |
|---|---|---|
| RQ1 | How households pay utility bills today and what each payment costs in time, money and surcharge | Faisal's original ask was a cashback promotion for balance-keepers; the team needs a priced baseline for what a bill costs today before designing anything |
| RQ2 | What happens to money between a cash-in and the moment it leaves the wallet, and what decides the timing | The cashback premise, that money in the wallet stays available, is untested. N64's ledger proxy puts about 246,000 wallets on a bill-shaped cash-in pattern; only interviews can say whether that money is held or spent the same day |
| RQ3 | What an agent does today when a customer asks about a bill, and what it costs the agent | 3,200 agents are the channel most of this base already uses; a design routing around an agent who already fields this need fights its own channel |
| RQ4 | Where USSD sessions fail from the customer's side, and what the customer does next | The [mobile money and wallets card](../knowledge/domains/mobile-money-wallets.md) warns a dropped USSD session cannot retry silently like an app; app assumptions here will misjudge most failures |

## 2. Method

- **Method:** semi-structured interviews, in person. Customers are met at home or nearby in Lahore; agents are interviewed at their own counter between customers, matching the [mobile money and wallets card](../knowledge/domains/mobile-money-wallets.md)'s treatment of the agent as its own persona and channel, not a stand-in for the wallet holder.
- **Why this method answers the RQs:** the bill or counter in view prices the trip, fee and referral rather than only describing them; it cannot measure how common a pattern is across the full active-wallet base, or the gateway's true completion rate, both log questions, not interview ones.
- **Sessions planned:** 14: 8 customers (INT-001 to INT-008), 6 agents (INT-009 to INT-014), fielded 2026-01-26 to 2026-02-13 (N17).
- **Session length:** 45 minutes customers, 30 minutes agents at the counter (N61) · **Recording:** Yes, audio on the interviewer's phone with verbal consent confirmed at the start; a participant code, never a name, in every note. Where consent slips and audio are archived long-term is Open: Amna Rasheed.
- **Incentive:** PKR 500 mobile airtime per session, paid regardless of what the session found (N61).

## 3. Screener

| Criterion | Include if | Exclude if |
|---|---|---|
| Household bill payment (customer segment) | Paid at least one household utility bill, electricity, gas or water, in the last three months | Has not personally paid one in that window |
| Wallet activity (customer segment) | Holds an active Sahulat wallet with a cash-in in the last 30 days | Wallet inactive, or no cash-in in the last 30 days |
| Bill-paying role (customer segment) | Is the person in the household who carries the paper bill to pay it | Someone else in the household always pays |
| Agent tenure and activity (agent segment) | Actively operating a Sahulat agent counter for three months or more, handling day-to-day cash-in and cash-out | Agent code inactive, or onboarded less than three months ago |
| Conflict of interest, both segments | No employment or contract relationship with Sahulat Digital, Falak Telecom, BillBridge or Darya Bank, and no relationship with a competing wallet | Works for or consults to any of the above |

**Recruiting source:** customers are recruited through the agent helpline's BILL-ASK tag and screened by phone before scheduling; agents are recruited from Tariq Sohail's active-agent roster, prioritising Lahore, where the eventual pilot is expected to sit. Usman Javed books every session and takes notes; Hira Baig leads every session.

## 4. Interview script

**Opening (2 minutes customers, 1 minute agents):** introduce Hira and Usman; state this studies how bills get handled today, not anything being built; confirm consent; a code, never a name, in the record.

**Warm-up:**
1. Tell me about the bills your household pays every month, electricity, gas, water or anything else, and who usually deals with them. (customers)
2. Tell me about a normal day at your counter: where does Sahulat cash-in and cash-out sit against everything else you sell? (agents)

**Behavior and pain:**
3. Walk me through the last time you paid an electricity or gas bill, from when you knew it was due to when it was actually paid. Show me the bill if you have it. (customers)
4. Where did that go slower or worse than you wanted, and what did that cost you in time, money or a fine? (customers)
5. The last time money sat in your Sahulat wallet for more than two days, what was it for? (customers; the question that replaced a leading one after the pilot, see the interview guide's revision log)
6. Tell me about the last time a customer asked you about paying a bill. What did you tell them, and where did you send them? (agents)
7. Tell me about the last time a Sahulat session on your phone stopped in the middle. What happened next? (both segments)

**Prioritization:**
8. Of everything we discussed, what would you fix first? Why that one?

**Commitment probe (signal, not sale):**
9. If a fix for the trip and the fee you just described existed, what would you be willing to do next: try it with your next real bill, introduce us to a neighbour who pays the same way, or put a follow-up visit on the calendar?

**Close:** thank them; ask who else is worth talking to; ask for the artifacts they mentioned, the bill itself, a bill-shop receipt, a message about a dropped session.

The full script, with time budgets, probes and a "never ask" table, lives in [sahulat-interview-guide.md](sahulat-interview-guide.md). Its revision log records the one mid-flight change: v1's closing question, "Would you pay your electricity or gas bill from your Sahulat wallet if you could?", piloted on INT-001 and INT-002, both of whom answered yes within a second with no story behind it, was cut before INT-003 ran; question 5 above replaced it.

## 5. Session notes

Fourteen sessions ran; two are worked in full below, the rest summarised. INT-004's full raw record, with its two most-cited quotes, lives in [sahulat-interview-notes.md](sahulat-interview-notes.md), copied into this table on 2026-02-03.

| ID | Date | Participant | Segment | Note |
|---|---|---|---|---|
| INT-001 | 2026-01-26 | C-01 | Customer | Guide v1 pilot |
| INT-002 | 2026-01-26 | C-02 | Customer | Guide v1 pilot; v1's balance question read as leading, cut before the next session |
| INT-003 | 2026-01-29 | C-03 | Customer | Keeps a salary balance for days, "two or three thousand" (E5); contradicts T2 |
| INT-004 | 2026-02-02 | C-04 | Customer | Full record: [sahulat-interview-notes.md](sahulat-interview-notes.md) (E1, E2) |
| INT-005 | 2026-02-03 | C-05 | Customer | Pays at a bill shop, on the due date; a Saturday this cycle |
| INT-006 | 2026-02-05 | C-06 | Customer | Holds a balance most months; contradicts T2 |
| INT-007 | 2026-02-06 | C-07 | Customer | Worked below (E4) |
| INT-008 | 2026-02-09 | C-08 | Customer | Pays at a bank branch, on the due date; a Sunday this cycle |
| INT-009 | 2026-02-04 | A-01 | Agent | Refers bill questions to the corner shop |
| INT-010 | 2026-02-05 | A-02 | Agent | Cash-in money is gone again within the hour |
| INT-011 | 2026-02-06 | A-03 | Agent | Worked below (E3) |
| INT-012 | 2026-02-09 | A-04 | Agent | Describes a customer redialing after a dropped session |
| INT-013 | 2026-02-11 | A-05 | Agent | Confirms the bill-shop referral and its PKR 30 to 50 fee |
| INT-014 | 2026-02-13 | A-06 | Agent | Last session; no new theme, fielding closed here |

### Session INT-007

- **Date:** 2026-02-06 · **Participant:** C-07 · **Segment:** Customer
- **Screener criteria met:** paid an electricity bill in the last three months; wallet with a cash-in in the last 30 days; carries the paper bill herself

| Timestamp | Observation (what was said or done) | Interpretation (what it might mean) | RQ touched |
|---|---|---|---|
| 21:15 | "The screen went off in the middle and I did not know if the money went. I waited ten minutes for the message and then dialed again." (E4) | A dropped USSD session leaves no visible sign a debit posted; the customer's own remedy is to retry within minutes, not wait for a status message | RQ4 |

**Strongest moment of the session:** 21:15, the line quoted above.
**Commitments made, if any:** none.

### Session INT-011

- **Date:** 2026-02-06 · **Participant:** A-03 · **Segment:** Agent
- **Screener criteria met:** operating the same counter for over a year; handles cash-in and cash-out daily

| Timestamp | Observation (what was said or done) | Interpretation (what it might mean) | RQ touched |
|---|---|---|---|
| 06:50 | "Six or seven people a day ask me if I can do their bill. I send them to the shop across the road and he keeps the fifty." (E3) | Bill-pay demand already reaches the agent counter every day; today it is referred away, at a fee the agent can name exactly and does not share in | RQ3 |

**Strongest moment of the session:** 06:50, the line quoted above.
**Commitments made, if any:** agreed to be contacted again if a pilot opens in his area.

## 6. Synthesis themes

| Theme | Sessions supporting it (IDs) | Contradicting sessions (IDs) | Confidence (high / medium / low) | So what: implication for the product decision |
|---|---|---|---|---|
| T1: bills are paid in person on or near the due date, with a trip and often a fee | INT-001, 002, 004, 005, 007, 008 | none observed | High | The trip itself, not only the amount owed, is the cost worth removing |
| T2: money enters the wallet for a purpose and leaves the same day | INT-001, 002, 004, 005, 007, 008, 009, 010 | INT-003, INT-006 | High | The cashback premise assumed the opposite of what six of eight customers and two of six agents describe; any Rel-1 story that pays "from balance" needs its own falsification test, see the worked micro-example below |
| T3: agents field bill questions daily and refer customers to a shop | INT-009, 010, 011, 012, 013, 014 | none observed | High | Demand already reaches the counter and is referred away for a fee the agent does not share in; a design that keeps the agent central matches where the demand already sits |
| T4: a dropped USSD session produces a repeat attempt, not a wait | INT-004, 007, 008, 012 | none observed | Medium | A customer who cannot tell whether money moved will retry blind; the flow must say so inside the same short-code interaction |
| T5: weekend and after-hours due dates produce surcharges | INT-004, 005, 008 | none observed | Medium | Whichever rail posts the bill has to survive a due date outside a bank's working hours, or it reproduces the surcharge this product exists to remove |

**Surprises:** the team expected more customers to already keep a standing balance, the shape of Faisal's cashback ask. The sessions said the opposite for the majority: eight supporting T2 against two contradicting is not close, and the two of eight who do hold one (N26) sit below the plan's own three-of-eight bar for keeping balance-first work in scope, set out below.

**Answers to the research questions:**

| RQ | Answer as evidenced | Open remainder |
|---|---|---|
| RQ1 | Households pay in person, split evenly bank branch/bill shop (4 of 8 each, N63), mostly on the due date (6 of 8, N25): median 70-minute trip, PKR 60 transport (N20); shop fee PKR 30 to 50 (N21); 5 of 8 paid a late surcharge in three months, median PKR 200 (N18, N19); three bills a month (N22), median electricity bill PKR 2,400 (N23) | Which single moment in the trip a phone-based flow can credibly replace is a DESIGN question this plan does not answer |
| RQ2 | Money enters for a purpose, leaves the same day: six of eight customers, two of six agents (T2). Only INT-003 and INT-006 held a balance over two days (N26); N64's proxy puts ~246,000 wallets on a bill-shaped cash-in pattern, but only this study says whether that money sits or moves, and for most, it moves | Whether a bill-specific reason to hold funds changes the hold rate for the minority who already do it is untested; the personas artifact carries it forward as a labeled assumption, not a finding |
| RQ3 | All six agent sessions describe fielding bill questions daily and referring the customer to a bill shop for a fee the agent names precisely, PKR 30 to 50 (N21), and does not share in | Whether an agent would rather perform the payment on the customer's behalf, and for what commission, was not asked this round. Open: Tariq Sohail |
| RQ4 | A dropped USSD session produces an immediate repeat attempt, not a wait, in four of fourteen sessions across both segments (theme T4); the customer cannot tell from the screen whether the debit posted before dialing again | The gateway's own failure rate is an engineering-log question the interviews cannot answer. Open: Zainab Qureshi, once instrumentation exists |

---

## How this plan fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Recruiting people who already like you | The screener quietly selects current, happy, engaged users | Screen for the population the question is about, and cap prior usage |
| Leading questions | "How much would this help you?", about a feature you want to build | Two people review the guide for leading wording before it is used |
| Sample size by convenience | A number chosen from recruiter availability, justified afterwards | Set it from the method: per segment, or until sessions stop producing new themes |
| No analysis plan | The guide is written, transcripts arrive, themes are invented while reading | Write how findings will be coded and how they map to the decision, before fielding |
| Run to justify a decision | The conclusion arrives with the brief | Ask the requester in writing what result would change the plan. If none, do not run it |

### Worked micro-example (ILLUSTRATIVE, invented)

| Field | Filled |
|---|---|
| *Decision this informs* | *Whether Rel-1 scope includes the balance-first stories, saved payee references, an app-first flow, and a reminder SMS before a due date, alongside the core lookup-and-pay flow, or ships lookup-and-pay only and waits for evidence* |
| *What result would change the plan* | *If fewer than three of eight customers report keeping a wallet balance for more than two days in the last month, the balance-first stories do not enter Rel-1 scope* |
| *Population* | *Adults who personally pay at least one household electricity or gas bill and hold an active Sahulat wallet with a cash-in in the last 30 days; agents excluded, since balance-keeping is a customer behavior, not an agent one* |
| *Method and its limits* | *Semi-structured interviews with the bill in hand where the participant has it. It can describe what eight customers say they do with money that sits in the wallet; it cannot say what share of the active-wallet base behaves the same way* |
| *Sample* | *Eight customers of the fourteen total sessions (N17), the customer segment only* |
| *Analysis plan, written before fielding* | *Code every customer session for whether money sat in the wallet more than two days, what it was held for, and whether the reason was bill-related or unrelated. Map directly to RQ2 and nowhere else* |
| *Consent and incentive* | *Audio recorded with verbal consent where offered, participant code only in every note; PKR 500 mobile airtime, paid regardless of what the session found (N61)* |

*The second row is the one most plans omit. A stakeholder who cannot say what result would change the plan is asking for a document, not a study.*

## Exit gate (feeds Gate 1: problem worth solving)

- [x] Every research question maps to a live decision, not curiosity: RQ1 to RQ4 each gate a specific Rel-1 scope choice, named in section 1
- [x] Screener screens on behavior, not attitude: paid a bill, holds an active wallet, carries the paper bill; no "cares about" criterion anywhere in section 3
- [x] Script contains no pitch and no "would you use" questions: the one question that came close, the v1 balance question, was piloted on INT-001 and INT-002 and cut before the remaining twelve sessions ran, section 4
- [x] At least five sessions completed and noted in this file: fourteen, section 5
- [x] Every theme cites three or more supporting session IDs and lists contradictions: T5 sits exactly at the floor, three sessions, section 6
- [x] Each RQ has an evidenced answer or an explicit open remainder: section 6, all four

This checklist is the author's own read, not a gate result. Gate 1 attempt 1 (2026-02-20) returned [sahulat-problem-framing.md](sahulat-problem-framing.md) for arithmetic-free cost of inaction and a usage-based success signal, not this plan; attempt 2 (2026-02-27) was signed GO by Faisal Mirza and Hira Baig, this document unchanged between attempts. The row this file is proudest of is the worked micro-example's second row: the result that would change the plan arrived, two of eight, not three, and DESIGN's premortem scored the risk low anyway. A research plan can only write the falsification rule down; it cannot make an organisation follow it.
