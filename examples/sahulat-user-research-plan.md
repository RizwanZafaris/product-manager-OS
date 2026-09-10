# User Research Plan: Sahulat Bill Pay

Fills [templates/discovery/user-research-plan.md](../templates/discovery/user-research-plan.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, every session, quote, date and count below is ILLUSTRATIVE, drawn from the rest of the [Sahulat journey](sahulat-journey.md), and none of it describes any real wallet, market or regulator. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager, the only PM · **Date:** 2026-01-19 · **Status:** Synthesized (2026-02-16); retrospective note added 2026-08-28 · **Note-taker:** Usman Javed · **Journey:** [Sahulat Bill Pay](sahulat-journey.md), DISCOVER, feeds Gate 1 · **Sector cards:** [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md), [payments acquiring](../knowledge/domains/payments-acquiring.md)

## 1. Research questions

| # | Research question | Why it matters to the decision at hand |
|---|---|---|
| RQ1 | How households pay utility bills today and what each payment costs in time, money and surcharge | Faisal's original ask was a cashback promotion for balance-keepers; the team needs a priced baseline for what a bill costs today before designing anything, the arithmetic Gate 1's cost-of-inaction line stands on |
| RQ2 | What happens to money between a cash-in and the moment it leaves the wallet, and what decides the timing | The ledger already shows the money does not sit: 61 percent of cash-ins are fully cashed out again within 48 hours (N10, measured) and the median month-end balance is PKR 340 (N12, measured). The early ledger cut later formalized as BP-01 (N64, estimate) puts about 246,000 wallets on a bill-shaped cash-in pattern; the cashback premise, that this money would stay available to pay from, is untested, and only interviews can say why households move it out and what would change the timing. This is the question behind the worked micro-example below: whether balance-first work enters Rel-1 scope at all |
| RQ3 | What an agent does today when a customer asks about a bill, and what it costs the agent | 3,200 agents are the channel most of this base already uses. The answer decides whether the agent is designed as its own persona and channel, not a stand-in for the wallet holder |
| RQ4 | Where USSD sessions fail from the customer's side, and what the customer does next | The [mobile money and wallets card](../knowledge/domains/mobile-money-wallets.md) warns a dropped USSD session cannot retry silently like an app. The answer decides whether dropped-session handling is a must, not a should, in Rel-1 |

## 2. Method

- **Method:** semi-structured interviews, in person. Customers are met at home or nearby in Lahore; agents are interviewed at their own counter between customers, matching the [mobile money and wallets card](../knowledge/domains/mobile-money-wallets.md)'s treatment of the agent as its own persona and channel, not a stand-in for the wallet holder.
- **Why this method answers the RQs:** the bill or counter in view prices the trip, fee and referral rather than only describing them; it cannot measure how common a pattern is across the full active-wallet base, or the gateway's true completion rate, both log questions, not interview ones. Every session ran in Lahore, so nothing here speaks to another city's bank-branch hours, agent density or bill mix.
- **Sessions planned:** 14 as a cap, or until sessions stop producing a new theme, whichever comes first: 8 customers (INT-001 to INT-008), 6 agents (INT-009 to INT-014). INT-014's note records the stopping condition met, not only the cap reached. Fielded 2026-01-26 to 2026-02-13 (N17, measured).
- **Session length:** 45 minutes customers, 30 minutes agents at the counter (N61, decided) · **Recording:** Yes, audio on the interviewer's phone with verbal consent confirmed at the start; a participant code, never a name, in every note. Where consent slips and audio are archived long-term is Open: Amna Rasheed.
- **Incentive:** PKR 500 mobile airtime per session, paid regardless of what the session found (N61, decided).

## 3. Screener

| Criterion | Include if | Exclude if |
|---|---|---|
| Household bill payment (customer segment) | Paid at least one household utility bill, electricity, gas or water, in the last three months | Has not personally paid one in that window |
| Wallet activity (customer segment) | Holds an active Sahulat wallet with a cash-in in the last 30 days | Wallet inactive, or no cash-in in the last 30 days |
| Bill-paying role (customer segment) | Is the person in the household who carries the paper bill to pay it | Someone else in the household always pays |
| Agent tenure and activity (agent segment) | Actively operating a Sahulat agent counter for three months or more, handling day-to-day cash-in and cash-out | Agent code inactive, or onboarded less than three months ago |
| Conflict of interest, both segments | No employment or contract relationship with Sahulat Digital, Falak Telecom, BillBridge or Darya Bank, and no relationship with a competing wallet | Works for or consults to any of the above |

**Recruiting source:** customers are recruited through the agent helpline's BILL-ASK tag and screened by phone before scheduling; agents are recruited from Tariq Sohail's active-agent roster, prioritising Lahore, where the eventual pilot is expected to sit. Usman Javed books every session and takes notes; Hira Baig leads every session.

**Recruiting bias, named:** every customer in this sample had already called the helpline asking about a bill, which is the "recruiting people who already like you" failure mode this file's own table below warns against: BILL-ASK callers may already be more bill-conscious than the wider active-wallet base, and the bias is not capped anywhere in this round. It can inflate T1's trip-and-fee pattern and skew RQ2 toward customers primed to talk about bills. The next round should recruit customers from the behavior-based ledger proxy behind N64 (query BP-01) instead, or cap BILL-ASK callers at no more than half the customer sample.

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
7. Tell me about the last time a Sahulat session on your phone stopped in the middle. What happened next? (both segments: customers are asked this directly; the guide's agent track carries the same question in the same block, asking what happened the last time a customer's session stopped in the middle at the agent's counter, and that Block B question is where INT-012's dropped-session line actually came from)

**Prioritization:**
8. Of everything we discussed, what would you fix first? Why that one?

**Commitment probe (signal, not sale):**
9. Customers, paraphrased from the guide's own commitment question: if a fix for the trip and the fee you just described existed, what would you do next, try it with your next real bill, introduce us to a neighbour, put a visit on the calendar, and when? Agents, paraphrased from the guide's own Block E question: what did you earn from the last customer you sent to the bill shop, was that typical, and what is the most and least you have made off a referral? This is a past-behavior question, not a hypothetical about future pay; whether an agent would expect to be paid for performing the payment himself was not asked this round (see RQ3 below).

**Close:** thank them; ask who else is worth talking to; ask for the artifacts they mentioned, the bill itself, a bill-shop receipt, a message about a dropped session.

The full script, with time budgets, probes and a "never ask" table, lives in [sahulat-interview-guide.md](sahulat-interview-guide.md). Its revision log records the one mid-flight change: the question that closed v1's Block D, "Would you keep money in the wallet if you could pay bills?", piloted on INT-001 and INT-002, both of whom answered yes within a second with no story behind it, was cut before INT-003 ran; question 5 above replaced it.

## 5. Session notes

Fourteen sessions ran; all fourteen are noted in the table below, and two are excerpted in full observation/interpretation blocks (INT-007, INT-011); the rest are one-line summaries, some of which state an interpretation ("contradicts T2") alongside the note rather than keeping the two apart, since a full block was not built for them. INT-004's full raw record, with its two most-cited quotes, lives in [sahulat-interview-notes.md](sahulat-interview-notes.md), copied into this table on 2026-02-03.

| ID | Date | Participant | Segment | Note |
|---|---|---|---|---|
| INT-001 | 2026-01-26 | C-01 | Customer | Guide v1 pilot |
| INT-002 | 2026-01-26 | C-02 | Customer | Guide v1 pilot; v1's balance question read as leading, cut before the next session |
| INT-003 | 2026-01-29 | C-03 | Customer | Keeps a salary balance for days, "two or three thousand" (E5); contradicts T2 |
| INT-004 | 2026-02-02 | C-04 | Customer | Full record: [sahulat-interview-notes.md](sahulat-interview-notes.md) (E1, E2) |
| INT-005 | 2026-02-03 | C-05 | Customer | Pays at a bill shop, on the due date; a Saturday this cycle |
| INT-006 | 2026-02-05 | C-06 | Customer | Holds a balance most months; contradicts T2 |
| INT-007 | 2026-02-06 | C-07 | Customer | Worked below (E4) |
| INT-008 | 2026-02-09 | C-08 | Customer | Usually pays at a bank branch on the due date; this cycle's due date was a Sunday, the branch was shut, and she paid late (T5) |
| INT-009 | 2026-02-04 | A-01 | Agent | Refers bill questions to the corner shop |
| INT-010 | 2026-02-04 | A-02 | Agent | Cash-in money is gone again within the hour |
| INT-011 | 2026-02-04 | A-03 | Agent | Worked below (E3) |
| INT-012 | 2026-02-06 | A-04 | Agent | Describes a customer redialing after a dropped session |
| INT-013 | 2026-02-11 | A-05 | Agent | Confirms the bill-shop referral and its PKR 30 to 50 fee |
| INT-014 | 2026-02-13 | A-06 | Agent | Last session; no new theme, fielding closed here |

### Session INT-007

- **Date:** 2026-02-06 · **Participant:** C-07 · **Segment:** Customer
- **Screener criteria met:** paid an electricity bill in the last three months; wallet with a cash-in in the last 30 days; carries the paper bill herself

| Timestamp | Observation (what was said or done) | Interpretation (what it might mean) | RQ touched |
|---|---|---|---|
| 21:15 | "The screen went off in the middle and I did not know if the money went. I waited ten minutes for the message and then dialed again." (E4) | A dropped USSD session leaves no visible sign a debit posted; the customer's own remedy, after waiting five to ten minutes with no status message, is to dial again, not to retry immediately | RQ4 |

**Strongest moment of the session:** 21:15, the line quoted above.
**Commitments made, if any:** none.

### Session INT-011

- **Date:** 2026-02-04 · **Participant:** A-03 · **Segment:** Agent
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
| T2: money enters the wallet for a purpose and leaves the same day | INT-001, 002, 004, 005, 007, 008, 009, 010 | INT-003, INT-006 | High | The cashback premise assumed the opposite of what six of eight customers and two of six agents describe; per the worked micro-example's falsification rule below, balance-first stories (SAHULAT-S5, SAHULAT-S10 and SAHULAT-S11) stay out of Rel-1 on this evidence, lookup-and-pay only |
| T3: agents field bill questions daily and refer customers to a shop | INT-009, 010, 011, 012, 013, 014 | none observed | High | Demand already reaches the counter and is referred away for a fee the agent does not share in; a design that keeps the agent central matches where the demand already sits |
| T4: a dropped USSD session produces a repeat attempt, not a wait | INT-004, 007, 008, 012 | none observed | Medium | A customer who cannot tell whether money moved will retry blind; the flow must say so inside the same short-code interaction |
| T5: weekend and after-hours due dates produce surcharges | INT-004, 005, 008 | none observed | Medium | Whichever rail posts the bill has to survive a due date outside a bank's working hours, or it reproduces the surcharge this product exists to remove |

**Surprises:** the team expected more customers to already keep a standing balance, the shape of Faisal's cashback ask. The sessions said the opposite for the majority: eight supporting T2 against two contradicting is not close, and the two of eight who do hold one (N26) sit below the plan's own three-of-eight bar for keeping balance-first work in scope, set out below. **Rule result: 2 of 8 against a bar of 3 of 8.** Per the micro-example, the balance-first stories, SAHULAT-S5, SAHULAT-S10 and SAHULAT-S11, do not enter Rel-1 scope on this evidence.

**Answers to the research questions (all figures ILLUSTRATIVE; firmness word after each N-id):**

| RQ | Answer as evidenced | Open remainder |
|---|---|---|
| RQ1 | Households pay in person, split evenly bank branch/bill shop (4 of 8 each, N63, measured, told), mostly on the due date (6 of 8, N25, measured, told); three of eight most recent due dates fell on a Saturday or Sunday (N24, measured, shown): median 70-minute trip, PKR 60 transport (N20, estimate, told); shop fee PKR 30 to 50 (N21, estimate, told by agents); 5 of 8 paid a late surcharge in three months, median PKR 200 (N18, measured, shown or told; N19, estimate, from the 4 bills shown); three bills a month (N22, measured, bills shown), median electricity bill PKR 2,400 (N23, measured, small sample) | Which single moment in the trip a phone-based flow can credibly replace is a DESIGN question this plan does not answer |
| RQ2 | The ledger already answers whether the money sits: 61 percent of cash-ins are fully cashed out within 48 hours (N10, measured) and the median month-end balance is PKR 340 (N12, measured). The interviews answer why and what decides the timing: money enters for a purpose and leaves the same day for six of eight customers and two of six agents (T2). Only INT-003 and INT-006 held a balance over two days (N26, measured, told); N26's denominator of eight includes INT-001 and INT-002, who ran guide v1 and were not asked the two-day-balance question directly, since it was only added in v2 (see the guide's revision log). Both are coded, from their own Block B walk-through, as same-day cash-in-to-cash-out: T2's own supporting-session list above already places INT-001 and INT-002 among the six describing this pattern, not the two contradicting it. Restricted to the six sessions actually asked the v2 question, the result is 2 of 6, still below the three-of-eight bar. N64's proxy (estimate) puts ~246,000 wallets on a bill-shaped cash-in pattern | Whether a bill-specific reason to hold funds changes the hold rate for the minority who already do it is untested; the personas artifact carries it forward as a labeled assumption, not a finding |
| RQ3 | All six agent sessions describe fielding bill questions daily and referring the customer to a bill shop for a fee agents put at PKR 30 to 50 a bill (N21, estimate, told by agents), and do not share in | Blocks C and E of the guide asked where agents send bill customers today, what that shop charges, and what agents earned from their last referral; whether an agent would pay a bill on a customer's behalf himself, and for what commission, was not asked this round. Open: Hira Baig, next DISCOVER pass |
| RQ4 | A dropped USSD session produces a repeat dial after five to ten minutes with no status message, not an immediate retry, in four of fourteen sessions across both segments (theme T4; E4, INT-007 at 21:15; INT-004 notes at 14:30); the customer cannot tell from the screen whether the debit posted before dialing again | The gateway's own failure rate is an engineering-log question the interviews cannot answer. Open: Zainab Qureshi, once instrumentation exists |

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
| *Population* | *Adults who personally pay at least one household electricity, gas or water bill and hold an active Sahulat wallet with a cash-in in the last 30 days, matching the screener in section 3; agents excluded, since balance-keeping is a customer behavior, not an agent one* |
| *Method and its limits* | *Semi-structured interviews with the bill in hand where the participant has it. It can describe what eight customers say they do with money that sits in the wallet; it cannot say what share of the active-wallet base behaves the same way* |
| *Sample* | *Eight customers of the fourteen total sessions (N17), the customer segment only; two of the eight, INT-001 and INT-002, ran guide v1 and were not asked the two-day-balance question directly, see section 6's RQ2 answer for how they were coded* |
| *Analysis plan, written before fielding* | *Code each customer session for whether money sat in the wallet more than two days, what it was held for, and whether the reason was bill-related or unrelated. Map directly to RQ2 and nowhere else* |
| *Consent and incentive* | *Audio recorded with verbal consent confirmed at the start, participant code only in every note, matching section 2; PKR 500 mobile airtime, paid regardless of what the session found (N61)* |

*The second row is the one most plans omit. A stakeholder who cannot say what result would change the plan is asking for a document, not a study.*

## Exit gate (feeds Gate 1: problem worth solving)

- [x] Every research question maps to a live decision, not curiosity: RQ1 to RQ4 each name the decision they inform in section 1, the Gate 1 cost-of-inaction arithmetic (RQ1, no Rel-1 existed on 2026-01-19) and three later Rel-1 scope choices (RQ2 to RQ4)
- [x] Screener screens on behavior, not attitude: paid a bill, holds an active wallet, carries the paper bill; no "cares about" criterion anywhere in section 3
- [x] Script contains no pitch and no "would you use" questions: the one question that came close, the v1 balance question, was piloted on INT-001 and INT-002 and cut before the remaining twelve sessions ran, section 4
- [x] At least five sessions completed and noted in this file: fourteen, section 5; three carry a full observation/interpretation block, INT-004 in [sahulat-interview-notes.md](sahulat-interview-notes.md), INT-007 and INT-011 below in this file; the remaining eleven are one-line summaries only
- [x] Every theme cites three or more supporting session IDs and lists contradictions: T5 sits exactly at the floor, three sessions, section 6
- [x] Each RQ has an evidenced answer or an explicit open remainder: section 6, all four

This checklist is the author's own read, not a gate result. Note added after Gate 1 attempt 2 (2026-02-27): Gate 1 attempt 1 (2026-02-20) was RETURNED on two lines: an arithmetic-free cost of inaction, returned to [sahulat-problem-framing.md](sahulat-problem-framing.md) section 5, and a usage-based success signal, recorded in `gates/gate-1-attempt-1.md`; neither line lives in this plan. Attempt 2 (2026-02-27) was signed GO by Faisal Mirza and Hira Baig, this document unchanged between attempts.

**Retrospective note, added 2026-08-28 after Gate 6.** The row this file is proudest of is the worked micro-example's second row: the result that would change the plan arrived, two of eight, not three, and the plan did not change. The override was not DESIGN's to make: Rel-1 scope, with SAHULAT-S5, S10 and S11 in it, was set at DEFINE and signed at Gate 2 on 2026-03-25, before DESIGN's premortem ever ran. DESIGN's premortem of 2026-04-08 then scored R6, "customers do not hold a balance," at likelihood 2 of 5, and that low score compounded a scope decision DEFINE had already made against this plan's own falsification rule. A research plan can write the falsification rule down and still watch DEFINE and DESIGN both decline to read it.
