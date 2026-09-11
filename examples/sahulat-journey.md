# Journey: Sahulat Bill Pay, a solo PM from zero to one

Fills no template: this file is the index and data sheet for the fourteen Sahulat artifacts named in the artifact map below, each of which fills one. Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan run by a fictional licensed electronic-money institution, the people, agents, customers, billers, bank, aggregator and telco are fiction, and every number is ILLUSTRATIVE, chosen so that fourteen documents agree with each other and not to describe any real wallet, market or regulator. Where a real regulation or scheme is named, it is named as a thing the fictional team must comply with, never as a source of a figure. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager, the only PM in the company · **Date:** 2026-08-28 · **Status:** Complete through Gate 6 (PIVOT); the next DISCOVER pass opens 2026-09-07 · **Workspace:** `products/sahulat-bill-pay/` per [PRODUCT-WORKSPACE.md](../os/PRODUCT-WORKSPACE.md) · **Sector cards:** [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md), [payments acquiring](../knowledge/domains/payments-acquiring.md)

## The story in one page

**The setting.** Sahulat is a mobile-money wallet run by Sahulat Digital (Private) Limited, a fictional electronic-money institution licensed under the State Bank of Pakistan's EMI Regulations, with about 140 staff, nine engineers, 3,200 active agents and exactly one product manager. Most customers reach the wallet through a USSD short code on a feature phone, or through the shopkeeper agent behind a counter; the smartphone app is a minority channel. At the end of 2025 the wallet had 1.9 million registered wallets, 410,000 active in the trailing 30 days, and one uncomfortable number: 61 percent of cash-ins were fully cashed out again within 48 hours. That is the remittance pass-through wearing an inclusion story that the [mobile-money card](../knowledge/domains/mobile-money-wallets.md) warns about, and the board's 2026 key result, 520,000 active wallets by year end, had nothing in the pipeline that would put a payment on the ledger. The feature this journey follows is paying an electricity or gas bill from the wallet, with cash-in through the agent network. The [payments-acquiring card](../knowledge/domains/payments-acquiring.md) is read for one question it asks better than any other: what happens when a payment is approved and the fulfilment behind it fails afterward, which became acceptance criterion AC-9 and risk R3.

**The people.** All fictional.

| Name | Role | Owns in this journey |
|---|---|---|
| Hira Baig | Product Manager, the only PM | Every artifact; the product-owner line on every gate; the pencil method (Method 1 in [CONDUCTOR.md](../os/CONDUCTOR.md)), self-interviewing from the bank files |
| Faisal Mirza | Chief Executive, sponsor | The sponsor line on every gate; decider on D1, D3, D4, D6 and D8 |
| Zainab Qureshi | Engineering lead, nine engineers, four on the squad | ADR-1 to ADR-3, DEP-2, risks R2 and R5, the USSD completion guardrail and the halt she called in D7 |
| Tariq Sohail | Head of agent network | Access to agents for research, risk R1, the float top-up hotline that was the Gate 5 condition |
| Amna Rasheed | Head of compliance and regulatory affairs | DEP-3, the KYC tier configuration AC-13 checks against, the objection recorded in D2 |
| Bilal Hasan | Finance and treasury lead | The trust-account reconciliation guardrail, DEP-4 (agent commission schedule), risk R4, the open post-pivot commission line |
| Naveed Akhtar | Customer support lead, call centre and agent helpline | The helpline tags the trigger and the review depend on, the support audience in the comms plan, story SAHULAT-S9 |
| Sara Lodhi | Data analyst, part time on this product | Queries NS-01, NS-02, PT-01, FP-01, BP-01 and BL-01; the counterfactual in the review; the day-1 report |
| Usman Javed | Agent operations officer, Lahore; note-taker | Notes for INT-001 to INT-014; the field observation of 2026-08-11 and 2026-08-12 |
| Mariam Gill | QA engineer | Criterion verification at Gate 4, UAT, the QA line at Gate 5 |
| Shazia, Rafiq, Kamran | Personas P1, P2 and P3 | Composites of the sessions each cites; Kamran carries the ASSUMPTION label |

External parties, all fictional: Darya Bank Limited and its bill-pay rail, Darya BillLink; BillBridge, a bill aggregator; the billers Ravi Power (electricity), Chenab Gas and Mehran Water; and Falak Telecom, the mobile operator whose USSD gateway and short code Sahulat rides on.

**DISCOVER, 2026-01-12 to 2026-02-27.** The trigger was two numbers, not a wish: 412 agent-helpline calls in four weeks asking whether Sahulat could pay a utility bill, against a feature that did not exist, beside the 61 percent pass-through. Faisal's first ask was a cashback promotion for customers who kept a balance; the opportunity assessment of 2026-01-15 named "customers will keep a balance in order to pay from it" as the riskiest assumption on the table, and D1 sent Hira into discovery on bills instead of into a promotion. She wrote the research plan, piloted the guide on two sessions and cut a leading question from it (the question was the hypothesis in disguise), ran fourteen sessions with Usman taking notes, eight customers and six agents, and built two evidenced personas and one labelled assumption: Kamran, the salaried balance-keeper, standing on two sessions. Gate 1 attempt 1 on 2026-02-20 came back MORE DISCOVERY on two lines: a cost of inaction with no arithmetic beside it, and a success signal that was usage. Attempt 2 on 2026-02-27 went GO with the signal rewritten as an outcome outside the product: a bill due in the household is paid through Sahulat before its due date, and no late surcharge is paid that month.

**PLANNING, 2026-03-02 to 2026-03-04.** The vision put the 2029 destination in Shazia's terms, and the north star sheet chose wallets with at least one on-ledger payment in the trailing 30 days, 96,000 in December 2025, because the card puts active on-ledger balance at the root, not registrations, and the sheet deliberately swaps balance for on-ledger payments since six of eight customers moved money out the same day (T2). Both were written before DEFINE so that Gate 6 would have something to score.

**DEFINE, 2026-03-05 to 2026-03-25.** The [WHICH-DOCUMENT](../os/WHICH-DOCUMENT.md) tree pointed at the full BRD/PRD/FRD stack, since a sponsor signs and both a regulator and the BillBridge contract are in scope; Hira overrode it to one-pager weight with user stories and acceptance criteria attached, logged as D2 over Amna's objection that a regulator in scope calls for the full stack; the resolution was her compliance memo, carried as DEP-3, and the objection is in the log. Gate 2 attempt 1 on 2026-03-18 was RETURNED for adjectives: one criterion said "promptly", one guardrail had no digit in it. Attempt 2 on 2026-03-25 was SIGNED by Hira Baig, Zainab Qureshi, Faisal Mirza and Amna Rasheed, and the one-pager's outcome metrics carried the hypothesis in a form that could fail: half of bill payments funded from a balance held for more than 48 hours.

**DESIGN, 2026-03-30 to 2026-04-15.** Darya Bank's term sheet arrived on 2026-03-30 and was rejected on 2026-04-03 (D3 and ADR-1, below). The premortem of 2026-04-08 produced risks R1 to R6, and R6, "customers do not hold a balance, so paying from balance is used by few", was scored likelihood 2 of 5 because the room believed in Kamran. ADR-2 made the USSD payment a two-phase state machine with an idempotency key, the answer to the card's question about a session that times out mid-transaction. Gate 3 was ACCEPTED on 2026-04-15.

**BUILD, 2026-04-20 to 2026-06-10.** Seven weeks, four engineers. On 2026-05-19 three of ten Mehran Water test bills failed reference validation; D5 dropped water from the first release, killed story SAHULAT-S7 with its id spent, and re-reviewed the affected criterion against Gate 2 rather than absorbing the change. Gate 4 on 2026-06-10 was MET with one listed miss: the resume half of AC-8 (a session dropped before debit resumes on the next dial) deferred to the second release with Zainab as owner. That accepted miss is the one that bit in launch week.

**DELIVER, 2026-06-15 to 2026-07-06.** UAT ran with 40 customers and 25 agents in the Lahore pilot district and closed three severity-1 defects. The rollback was performed in pre-production on 2026-06-22 in nine minutes. The comms plan wrote the launch facts once and the rollback holding statement before anyone needed it. Gate 5 on 2026-07-01 was CONDITIONAL GO: the agent float top-up hotline had to be live before the nationwide step, owner Tariq, by 2026-07-17. The review window was fixed at that gate, launch plus six weeks, before any number existed. Launch went to 600 pilot agents on 2026-07-06 (D6).

**OPERATE, 2026-07-06 to 2026-08-28.** On 2026-07-09 to 2026-07-10, LD-1's daily M3 reading fell below the 90 percent floor (N67), with duplicate-payment tickets already arriving, and Zainab, the named halt-caller, paused the nationwide step for four days (D7) while the timeout fix shipped. The week then closed on 2026-07-12 at 87 percent, with 61 duplicate-payment tickets for the week (N46, N47). On 2026-07-14 the daily reconciliation found one unexplained break of PKR 12,300, traced within the day to a BillBridge retry posting twice. Nationwide followed on 2026-07-24. The post-launch review on 2026-08-21 recorded 31,200 bills in the four weeks to 2026-08-16 against a target of 40,000, and 9 percent of payments funded from a held balance against a target of 50 percent; 78 percent were funded by a cash-in made within two hours of the payment, and in Usman's two days at twelve counters, 41 of 53 bill payments were performed by the agent on the customer's phone or the agent's own handset. Gate 6 on 2026-08-28 signed PIVOT (D8) with the Gate 1 signal line unticked, since no query for that outcome-level signal exists (Open: Sara Lodhi, by 2026-09-21): agent-assisted bill pay, where the customer hands cash to the agent and the wallet is the record and the receipt, not the funding source. The next DISCOVER pass opens 2026-09-07 with Rafiq at the centre, and it discards Kamran and the pay-from-balance signal while keeping bill lookup, the USSD state machine and the BillBridge integration.

**The rejected option.** Darya BillLink would have shipped about nine weeks sooner on a ready API and a catalogue of 210 billers against BillBridge's 160. It lost on two facts from the term sheet. Its settlement cut-off was 15:00 on bank working days, with later payments posting to the biller the next working day; in the interview sample three of eight most recent due dates fell on a weekend and six of eight customers pay on the due date itself, so the rail would have reproduced the surcharge the product exists to remove. And its revenue share took 60 percent of the biller-paid fee, leaving Sahulat PKR 4 per bill against PKR 7 through BillBridge. D3 in the decision log records the options, the nine weeks given up, and the condition that would reopen it: a cut-off after 20:00 seven days a week.

**The failed hypothesis and what it cost.** The hypothesis was that customers would keep a balance and pay bills from it. It rested on Kamran, a persona the team had labelled an assumption and then designed for anyway. Nine of the squad's 28 engineer-weeks went to balance-first work: saved payee references (SAHULAT-S5), the app flow (SAHULAT-S10) and the reminder SMS three days before a due date (SAHULAT-S11). The launch SMS campaign, 400,000 messages at PKR 1.2, spent PKR 480,000 telling customers to keep a balance. The agent commission schedule paid agents nothing for the assistance they gave at the counter for six weeks, because v7 priced an agent-performed bill at PKR 0 (N68), on the assumption customers would pay from balance. And the review window measured the wrong funding path for six weeks before anyone could say so. The premortem had written the failure down as R6 and scored it low; the review's reconciliation table is where the scoring error is visible, and the lesson filed for the next team is three sentences long.

## Data sheet

Every number any Sahulat artifact uses is in the first table, and an artifact that needs a number not listed here adds it here first. The whole sheet is ILLUSTRATIVE: every value is invented, and the source column names where the fiction says the number came from, never a real system or study. Firmness is one of measured, estimate, target, assumption, quoted (a price or SLA on paper, not yet contracted) or decided.

### Conventions the artifacts share

- Currency is PKR, always with the unit. Dates are YYYY-MM-DD. Percentages are written as "percent".
- Story ids are SAHULAT-S1 to SAHULAT-S11 and are never renumbered; SAHULAT-S7 is dead and its id is spent. Releases are Rel-1 and Rel-2, so that a release is never confused with a risk.
- Risks are R1 to R6, decisions D1 to D8, dependencies DEP-1 to DEP-4, architecture decisions ADR-1 to ADR-3, acceptance criteria AC-1 to AC-13, evidence notes E1 to E5, epics EP1 to EP3, research questions RQ1 to RQ4, themes T1 to T5, metrics M1 to M5, and one outcome signal, O1: the Gate 1 attempt 2 signal, defined and labelled in the user stories' section 2, cited (without the label) in the one-pager's section 4.
- Sessions are INT-001 to INT-014; participant codes are C-01 to C-08 for customers and A-01 to A-06 for agents. Names never appear in notes.
- Gate attempts are filed in the workspace as `gates/gate-1-attempt-1.md`, `gates/gate-1-attempt-2.md` and so on, one file per attempt, failures kept. No gate is declared passed by a document; a named person signs it.
- Anything still open is written as "Open:" followed by the name of the person who owns the answer, never as a blank.
- At this weight, problem framing stands in for discovery-document.md as the Gate 1 roll-up; the gate files record that substitution.

### Numbers (ILLUSTRATIVE)

| ID | Name | Value, with unit | Source inside the fiction | Firmness |
|---|---|---|---|---|
| N1 | Registered wallets | 1,900,000 wallets | Core ledger, 2025-12-31 | measured |
| N2 | 30-day active wallets, December 2025 | 410,000 wallets | Core ledger, query NS-02 | measured |
| N3 | 30-day active wallets at review (30 days to 2026-08-16) | 422,000 wallets | Query NS-02 | measured |
| N4 | Board key result for 2026 | 520,000 30-day active wallets by 2026-12-31 | Board OKR sheet, December 2025 | target |
| N5 | Active agents | 3,200 agents | Agent management system, 2025-12-31 | measured |
| N6 | Pilot cohort | 600 agents in the Lahore pilot district | Cohort list attached to D6 | decided |
| N7 | Company size | About 140 staff, of whom 9 engineers and 1 PM | HR roster, January 2026 | measured |
| N8 | Squad capacity for BUILD | 4 engineers x 7 weeks = 28 engineer-weeks, plus 1 QA and the PM | Capacity note, 2026-04-16 | estimate |
| N9 | Cash-ins per month | 1,150,000 cash-ins | Core ledger, December 2025 | measured |
| N10 | Pass-through share, baseline | 61 percent of cash-ins fully cashed out within 48 hours | Query PT-01, Q4 2025 | measured |
| N11 | Pass-through share at review | 58 percent, four weeks to 2026-08-16 | Query PT-01 | measured |
| N12 | Median wallet balance at month end | PKR 340 | Core ledger, 2025-12-31 | measured |
| N13 | Helpline calls asking about bill pay | 412 calls in the four weeks to 2026-01-09 | Agent helpline, tag BILL-ASK | measured |
| N14 | North star, December 2025 | 96,000 wallets with at least one on-ledger payment in the trailing 30 days | Query NS-01 | measured |
| N15 | North star at review | 118,000 wallets, 30 days to 2026-08-16 | Query NS-01 | measured |
| N16 | Share of the north star gain already in the pre-launch trend | About a third of the 22,000 gain | Sara Lodhi's slope from January to June 2026 | estimate |
| N17 | Research sessions | 14 sessions: 8 customers (INT-001 to INT-008), 6 agents (INT-009 to INT-014), 2026-01-26 to 2026-02-13 | Research plan section 5 | measured |
| N18 | Customers who paid a late surcharge in the last three months | 5 of 8, the bill shown in 4 of the 5 | Interview notes, FACT and COST lines | measured, shown or told |
| N19 | Median late surcharge paid | PKR 200 per bill | The 4 bills shown | estimate |
| N20 | Bill-paying trip | Median 70 minutes round trip and PKR 60 transport per trip | 8 customer sessions, told | estimate |
| N21 | Bill-shop fee for paying on a customer's behalf | PKR 30 to 50 per bill | Agent sessions INT-009 to INT-014, told | estimate |
| N22 | Bills per household per month in the sample | 3 bills: electricity, gas, water | 8 customer sessions, bills shown | measured |
| N23 | Median electricity bill in the sample | PKR 2,400 per month | Bills shown in 7 sessions | measured, small sample |
| N24 | Customers whose most recent due date fell on a Saturday or Sunday | 3 of 8 | Bills shown | measured |
| N25 | Customers who pay on the due date itself | 6 of 8 | Told | measured, told |
| N26 | Customers who held a wallet balance for more than two days in the last month | 2 of 8: INT-003 and INT-006 | Told | measured, told; the only evidence under P3 |
| N27 | Cost of inaction to one household per year | 12 trips x 70 minutes = 840 minutes (14 hours); 12 x PKR 60 = PKR 720 transport; surcharges of PKR 200 about four times a year = PKR 800 for the five of eight who paid one; bill-shop fees of 3 x PKR 30 to 50 x 12 = PKR 1,080 to 1,800 for the four of eight who use a shop | Problem framing section 5, arithmetic shown | estimate |
| N28 | Cost of inaction to the business per month | 1,150,000 x 0.61 = 701,500 pass-through cycles x (PKR 15 + PKR 20) = PKR 24.6 million a month in agent commission on money that never stays; and a key-result gap of 520,000 minus 410,000 = 110,000 wallets with nothing in the pipeline | Problem framing section 5 | estimate |
| N29 | Agent commission, cash-in | PKR 15 per cash-in | Commission schedule v6, 2025-10-01 | measured |
| N30 | Agent commission, cash-out | PKR 20 per cash-out | Commission schedule v6 | measured |
| N31 | Biller-paid fee per bill through BillBridge | PKR 10 per bill | BillBridge indicative quote, 2026-01-13; confirmed on the rate card 2026-02-10 | quoted |
| N32 | BillBridge share and Sahulat net | PKR 3 to BillBridge, PKR 7 to Sahulat per bill | BillBridge indicative quote, 2026-01-13; confirmed on the rate card 2026-02-10 | quoted |
| N33 | Customer fee in Rel-1 | PKR 0 per bill | D4, 2026-03-20 | decided |
| N34 | Darya BillLink revenue share | 60 percent of the biller-paid fee to Darya; Sahulat net PKR 4 per bill | Darya term sheet, 2026-03-30 | quoted |
| N35 | Darya settlement cut-off | 15:00 on bank working days; later payments post to the biller the next working day | Darya term sheet | quoted |
| N36 | BillBridge posting SLA | Posts to the biller within 30 minutes, seven days a week; settlement to the biller T+1 through Sahulat's settlement bank | BillBridge rate card | quoted |
| N37 | Biller catalogues | Darya 210 billers; BillBridge 160 billers | Term sheet and rate card | quoted |
| N38 | Time the Darya path would have saved | About 9 weeks to launch | Zainab Qureshi's estimate, 2026-04-01 | estimate |
| N39 | Agent commission on assisted bill pay, post-pivot | PKR 5 per bill proposed | D8; Open: Bilal Hasan owns commission schedule v8 by 2026-09-30 | target |
| N40 | SMS cost | PKR 1.2 per message | Falak Telecom contract | measured |
| N41 | Launch SMS campaign | 400,000 messages x PKR 1.2 = PKR 480,000 | Campaign log, 2026-07-20 | measured |
| N42 | M1, bills paid per month | Baseline 0; target 40,000 bills in the four weeks to 2026-08-16; actual 31,200. Measurement window per N55: the last four full weeks inside the Gate 5 review window, 2026-07-20 to 2026-08-16 | One-pager section 4; query BL-01 on the ledger | target; measured |
| N43 | M2, share of bill payments funded from a balance held more than 48 hours | Target 50 percent; actual 9 percent | One-pager section 4; query FP-01 | target; measured |
| N44 | Share of bill payments funded by a cash-in within two hours before payment | 78 percent | Query FP-01 | measured |
| N45 | Observed bill payments performed by the agent on the customer's phone or the agent's handset | 41 of 53 across 12 counters, 2026-08-11 and 2026-08-12 | Usman Javed's field observation notes | measured, observed, small sample |
| N46 | M3, USSD bill-pay session completion | Floor 90 percent; week 1 (to 2026-07-12) 87 percent; at review 92 percent | Falak Telecom USSD gateway logs, dashboard LD-1 | target; measured |
| N47 | Duplicate-payment tickets | 61 in week 1; 3 in week 6 | Support system, tag DUP-PAY | measured |
| N48 | Trust-account reconciliation, unexplained breaks over PKR 1,000 at day end | Guardrail 0 per day; one break of PKR 12,300 on 2026-07-14, explained within the day as a BillBridge retry posting twice | Daily reconciliation, Bilal Hasan | target; measured |
| N49 | Operational load in the review window | 2 incidents (2026-07-09 USSD timeout spike; 2026-07-14 duplicate posting); on-call pages 11 in week 1, 1 in week 6 | Incident log, paging log | measured |
| N50 | Rollback rehearsal | Performed in pre-production on 2026-06-22; 9 minutes elapsed | Release readiness, rollback section | measured |
| N51 | UAT | 40 customers and 25 agents, 2026-06-15 to 2026-06-24; 3 severity-1 defects found and closed | UAT log | measured |
| N52 | Agents reporting a float stock-out on a bill-peak day in launch week | 38 of 600 pilot agents on 2026-07-08 | Agent helpline, tag FLOAT-OUT | measured |
| N53 | Wallets that paid at least one bill in the four weeks to 2026-08-16 | 24,600 wallets (31,200 bills), 5.8 percent of N3 | Ledger, query BL-01 | measured |
| N54 | Engineer-weeks spent on balance-first work | 9 of 28: SAHULAT-S5, SAHULAT-S10, SAHULAT-S11 | Sprint log | measured |
| N55 | Review window | Launch 2026-07-06 plus 6 weeks = 2026-08-17. M1 and M2 are measured over the last four full weeks inside it, 2026-07-20 to 2026-08-16 | Set at Gate 5, 2026-07-01 | decided |
| N56 | Acceptance thresholds | Bill lookup within 8 seconds at p95 on USSD; SMS confirmation within 60 seconds; status SMS after a dropped session within 2 minutes; "already paid" message window 24 hours (the block itself is per wallet, reference and bill month, ADR-2); support lookup within 5 seconds; reversal of a failed posting within 24 hours; cash-in credit spendable within 30 seconds | Acceptance criteria, agreed at Gate 2 attempt 2 | decided |
| N57 | Bill-peak days | The 5th to the 10th of the month carry 44 percent of monthly bill payments | Ledger, July and August 2026 | measured |
| N58 | Mehran Water reference validation | 3 of 10 test bills failed, 2026-05-19 | Test log | measured |
| N59 | Tickets asking for water bills after launch | 6 tickets in six weeks | Support system | measured |
| N60 | Agents reporting customers asking for a paper slip | Raised in 5 of 6 pilot agent debriefs | Agent debrief notes, 2026-07-27 | measured, told |
| N61 | Session logistics | Customers 45 minutes, agents 30 minutes at the counter; incentive PKR 500 mobile airtime | Research plan section 2 | decided |
| N62 | Falak Telecom USSD tariff change | PKR 0.40 to PKR 0.65 per session, effective 2026-10-01 | Tariff notice, 2025-12-18 | quoted |
| N63 | Where the sample pays today | 4 of 8 at a bank branch, 4 of 8 at a bill shop | Told | measured, told |
| N64 | Shazia-type wallets, proxy | 246,000 wallets with a cash-in on the 5th to 10th in two of the last three months | First ledger cut, Sara Lodhi, 2026-01 (for the opportunity assessment); formalized as query BP-01, February 2026 | estimate |
| N65 | Opportunity ceiling, fee revenue | 246,000 x 2 bills x PKR 7 = PKR 3.44 million a month at full adoption | Opportunity assessment question 3 | estimate |
| N66 | USSD session ceiling | 180 seconds per session on Falak Telecom's gateway | Gateway specification | quoted |
| N67 | M3 daily reading on LD-1, 2026-07-09 to 2026-07-10 | Below the 90 percent floor | Dashboard LD-1 | measured |
| N68 | Agent commission, bill-pay line, v7 | PKR 0 per agent-performed bill; cash-in commission unchanged at PKR 15 (N29) | Commission schedule v7, 2026-06-24 | decided |

### Shared identifiers

| ID | What it names | Defined in | Cited by |
|---|---|---|---|
| RQ1 | How households pay utility bills today and what each payment costs in time, money and surcharge | research plan | guide, notes, problem framing |
| RQ2 | What happens to money between a cash-in and the moment it leaves the wallet, and what decides the timing | research plan | guide, notes, personas, one-pager |
| RQ3 | What an agent does today when a customer asks about a bill, and what it costs the agent | research plan | guide, notes, personas |
| RQ4 | Where USSD sessions fail from the customer's side, and what the customer does next | research plan | guide, notes, acceptance criteria |
| INT-001, INT-002 | Pilot sessions, C-01 and C-02, 2026-01-26 (guide v1) | research plan | guide revision log |
| INT-003 | C-03, 2026-01-29; keeps a salary balance | research plan | personas (P3), E5 |
| INT-004 | C-04, 2026-02-02; the interview-notes artifact; surcharge bill shown, Sunday due date | research plan | notes, E1, E2, problem framing |
| INT-005 | C-05, 2026-02-03 | research plan | personas (P1) |
| INT-006 | C-06, 2026-02-05; keeps a balance | research plan | personas (P3) |
| INT-007 | C-07, 2026-02-06; dropped USSD session, dialed again | research plan | E4, acceptance criteria |
| INT-008 | C-08, 2026-02-09 | research plan | personas (P1) |
| INT-009 to INT-014 | Agents A-01 to A-06, 2026-02-04 to 2026-02-13 | research plan | personas (P2), E3 |
| T1 | Bills are paid in person on or near the due date, with a trip and often a fee (INT-001, 002, 004, 005, 007, 008) | research plan section 6 | problem framing |
| T2 | Money enters the wallet for a purpose and leaves the same day (INT-001, 002, 004, 005, 007, 008, 009, 010; contradicted by INT-003, INT-006) | research plan section 6 | personas, R6, review |
| T3 | Agents field bill questions daily and refer customers to a shop (INT-009 to INT-014) | research plan section 6 | personas (P2), SAHULAT-S3, SAHULAT-S4 |
| T4 | A dropped USSD session produces a blind repeat dial after a five-to-ten-minute wait for a status message that never comes (INT-004, 007, 008, 012) | research plan section 6 | SAHULAT-S8, AC-7, AC-8, AC-10, R2 |
| T5 | Weekend and after-hours due dates produce surcharges (INT-004, 005, 008) | research plan section 6 | D3, ADR-1 |
| E1 | INT-004 at 02:10: "The bill was due on a Sunday. The bank was shut, the shop man charged me fifty, and the office still put the fine on the next bill." | interview notes section 8 | problem framing, D3 |
| E2 | INT-004 at 18:35: "I only put money in the phone when I need to send it that day. Why would I leave it there?" | interview notes section 8 | personas, R6, review |
| E3 | INT-011 at 06:50: "Six or seven people a day ask me if I can do their bill. I send them to the shop across the road and he keeps the fifty." | research plan section 5 | personas (P2), SAHULAT-S3, D8 |
| E4 | INT-007 at 21:15: "The screen went off in the middle and I did not know if the money went. I waited ten minutes for the message and then dialed again." | research plan section 5 | SAHULAT-S8, AC-7, AC-8, R2 |
| E5 | INT-003 at 11:40: "I keep two or three thousand in it because my salary comes there." | personas (P3 behaviors), sourced to INT-003 | personas (P3), the hypothesis |
| P1 | Shazia, the household bill-runner; cites INT-001, 002, 004, 005, 007, 008 | personas | one-pager, stories, vision |
| P2 | Rafiq, the corner-shop agent; cites INT-009 to INT-014 | personas | stories, comms plan, D8 |
| P3 | Kamran, the salaried balance-keeper (ASSUMPTION); cites INT-003, INT-006 only | personas | one-pager M2, R6, review |
| EP1 | Look up and pay a bill (SAHULAT-S1, S2, S5, S6, S7, S10, S11) | user stories | acceptance criteria |
| EP2 | The agent counter (SAHULAT-S3, S4) | user stories | comms plan, D8 |
| EP3 | Safety and support (SAHULAT-S8, S9) | user stories | acceptance criteria |
| SAHULAT-S1 | As Shazia, I want to look up my Ravi Power bill by the reference number printed on it over USSD, so that I know the amount and due date without the paper bill (must, Rel-1) | user stories | AC-1, AC-2 |
| SAHULAT-S2 | As Shazia, I want to pay the bill from my wallet balance and get an SMS with a reference, so that I hold proof before the due date (must, Rel-1) | user stories | AC-3, AC-4, AC-9, AC-10, AC-13 |
| SAHULAT-S3 | As Shazia, I want to cash in at an agent and pay the bill in the same visit, so that I make no second trip (must, Rel-1) | user stories | AC-5 |
| SAHULAT-S4 | As Rafiq, I want to see a confirmation on my agent handset when a customer I cashed in pays a bill, so that I can vouch for it when asked (should, Rel-2) | user stories | D8, next pass |
| SAHULAT-S5 | As Shazia, I want to save a reference after paying, so that next month I do not re-enter it (should, Rel-1; balance-first) | user stories | N54 |
| SAHULAT-S6 | As Shazia, I want to pay a Chenab Gas bill the same way, so that both monthly bills go through one channel (must, Rel-1) | user stories | AC-6 |
| SAHULAT-S7 | As Shazia, I want to pay a Mehran Water bill the same way (must at Gate 2; killed by D5 on 2026-05-21, id spent) | user stories | one-pager not-doing list, D5 |
| SAHULAT-S8 | As Shazia, I want a session that drops mid-payment to tell me whether money moved, so that I do not pay twice (must, Rel-1) | user stories | AC-7, AC-8, AC-10, R2 |
| SAHULAT-S9 | As a support agent on Naveed's team, I want to look up a bill payment by reference, so that I answer "did it go through" on the first call (should, Rel-1) | user stories | AC-11 |
| SAHULAT-S10 | As Shazia on the app, I want the same lookup and pay flow, so that I am not forced onto USSD (should, Rel-1; balance-first) | user stories | N54 |
| SAHULAT-S11 | As Shazia, I want an SMS three days before a saved bill's due date, so that I cash in before the surcharge (should, Rel-1; balance-first) | user stories | AC-12, N54 |
| AC-1 to AC-13 | The pass-or-fail contract: AC-1 lookup happy path; AC-2 unknown reference; AC-3 pay and SMS; AC-4 insufficient balance; AC-5 same-visit cash-in and pay; AC-6 gas; AC-7 dropped after debit; AC-8 dropped before debit, resume (Gate 4 miss); AC-9 biller posting fails after debit, reversal; AC-10 duplicate blocked; AC-11 support lookup; AC-12 reminder SMS and opt-out; AC-13 tier limit refused with the limit named | acceptance criteria | stories, Gate 2, Gate 4 |
| M1 | Bills paid per month (N42) | one-pager section 4 | north star input, review |
| M2 | Share of bill payments funded from a balance held more than 48 hours (N43); the hypothesis | one-pager section 4 | review, D8 |
| M3 | USSD bill-pay session completion (N46); guardrail, floor 90 percent, halt-caller Zainab Qureshi | one-pager, north star sheet | D7, review |
| M4 | Pass-through share (N10, N11); guardrail, must not rise above 61 percent, halt-caller Hira Baig | north star sheet | review |
| M5 | The north star (N14, N15), query NS-01 | north star sheet | vision, review |
| R1 | Agent float runs out on bill-peak days, so the same-visit cash-in fails at the counter; likelihood 4, impact 4; owner Tariq Sohail; arrived (N52) | premortem 2026-04-08, risk register (workspace `delivery/`, not in this example set) | Gate 5 condition, review |
| R2 | A USSD session times out mid-payment and the customer pays twice; 4 x 4; owner Zainab Qureshi; arrived as the fear and the completion breach, not as a double debit: M3 87 percent week 1 (N46), 61 DUP-PAY tickets (N47), zero confirmed second debits because AC-10 held | risk register (workspace `delivery/`, not in this example set) | AC-7, AC-8, AC-10, D7 |
| R3 | BillBridge posts late to a biller and a surcharge lands anyway; 2 x 4; owner Hira Baig; did not arrive in the window (0 confirmed, 4 claims unverified) | risk register (workspace `delivery/`, not in this example set) | AC-9 |
| R4 | A trust-account reconciliation break from an aggregator retry; 3 x 3; owner Bilal Hasan; arrived once (N48) | risk register (workspace `delivery/`, not in this example set) | review |
| R5 | Falak Telecom delays the USSD menu change past UAT; 3 x 3; owner Zainab Qureshi; did not arrive (DEP-2 met five days late, inside UAT) | risk register (workspace `delivery/`, not in this example set) | DEP-2 |
| R6 | Customers do not hold a balance, so paying from balance is used by few; scored 2 x 5; owner Hira Baig; arrived (N43) | risk register (workspace `delivery/`, not in this example set) | review, D8 |
| D1 | 2026-01-16: enter DISCOVER on bill pay, not on a keep-balance cashback promotion; decider Faisal Mirza; sequencing | decision log | opportunity assessment |
| D2 | 2026-03-05: artifact weight is the one-pager with stories and criteria, not the BRD stack; decider Hira Baig; objection from Amna Rasheed recorded; other | decision log | one-pager |
| D3 | 2026-04-03: reject Darya BillLink; integrate BillBridge directly (N34, N35, N37 against N38); decider Faisal Mirza; vendor; reopens if Darya's cut-off moves past 20:00 seven days a week | decision log, ADR-1 | one-pager not-doing list |
| D4 | 2026-03-20: customer fee PKR 0 in Rel-1; decider Faisal Mirza; pricing | decision log | one-pager |
| D5 | 2026-05-21: drop Mehran Water from Rel-1 after N58; SAHULAT-S7 killed; criterion re-reviewed against Gate 2; decider Hira Baig; scope | decision log | stories, one-pager |
| D6 | 2026-07-01: staged rollout, 600 Lahore agents first, nationwide planned 2026-07-20; decider Faisal Mirza; sequencing | decision log | comms plan |
| D7 | 2026-07-10: pause the nationwide step four days on the M3 breach; decider Zainab Qureshi as halt-caller; nationwide moved to 2026-07-24; other | decision log | north star sheet, review |
| D8 | 2026-08-28: Gate 6 PIVOT to agent-assisted bill pay; next DISCOVER pass 2026-09-07; decider Faisal Mirza; scope; supersedes the one-pager's proposal, does not reverse D1 | decision log | review, Gate 6 |
| DEP-1 | BillBridge biller catalogue, test environment and settlement schedule; needed by 2026-04-27; met 2026-04-30 | dependency register (workspace, not in this example set) | Gate 3, BUILD |
| DEP-2 | Falak Telecom adds "Bill pay" to the short-code menu; needed by 2026-06-14; met 2026-06-19 | dependency register (workspace, not in this example set) | R5, UAT |
| DEP-3 | Amna Rasheed's compliance memo that bill pay sits within the licence's permitted activities and the notification is filed; needed by 2026-05-29; memo dated 2026-05-22 | dependency register (workspace, not in this example set) | D2, Gate 2, Gate 5 |
| DEP-4 | Agent commission schedule v7 adding the bill-pay line, paying PKR 0 per agent-performed bill, cash-in commission unchanged (N68); needed by 2026-06-26; met 2026-06-24; v8 open after D8 | dependency register (workspace, not in this example set) | Gate 5, N39 |
| ADR-1 | 2026-04-03: direct BillBridge integration, not the Darya rail; the structural half of D3 | architecture decision record | D3 |
| ADR-2 | 2026-04-09: USSD payment as a two-phase state machine with an idempotency key per wallet, reference and bill month, so a dropped session can be reported or resumed | architecture decision record | AC-7, AC-8, AC-10 |
| ADR-3 | 2026-04-09: bill-pay postings through the existing trust-account sub-ledger, no new ledger | architecture decision record | R4, N48 |
| NS-01 | Ledger query behind M5 | north star sheet section 1 | review |
| NS-02 | Ledger query behind N2, N3 | data sheet only (N2, N3) | north star sheet |
| PT-01 | Ledger query behind M4 | one-pager section 4, review | data-sheet rows |
| FP-01 | Ledger query behind M2 | one-pager section 4, review | data-sheet rows |
| BP-01 | Ledger query behind N64 | problem framing section 6, personas | data-sheet rows |
| BL-01 | Ledger query behind M1 and N53 | one-pager section 4, review | data-sheet rows |
| LD-1 | The launch dashboard: M1, M3, N47, N48 daily | comms plan section 6 | review |
| BILL-ASK, DUP-PAY, FLOAT-OUT | Helpline and support tags behind N13, N47, N52 | support system | problem framing, review |

### Timeline

| Date | Event | Stage | Record |
|---|---|---|---|
| 2026-01-12 | Trigger: N13 and N10 put side by side | DISCOVER | problem framing section 2 |
| 2026-01-15 | Opportunity assessment: recommends discovery; riskiest assumption named | DISCOVER | opportunity assessment |
| 2026-01-16 | D1 | DISCOVER | decision log |
| 2026-01-19 | Research plan, status Planned | DISCOVER | research plan |
| 2026-01-26 | Guide v1 piloted on INT-001, INT-002 | DISCOVER | guide section 7 |
| 2026-01-28 | Guide v2: leading question cut | DISCOVER | guide section 7 |
| 2026-01-26 to 2026-02-13 | INT-001 to INT-014 | DISCOVER | research plan section 5 |
| 2026-02-02 | INT-004, the interview-notes artifact | DISCOVER | interview notes |
| 2026-02-16 | Research plan synthesized; problem framing | DISCOVER | both |
| 2026-02-17 | Personas P1, P2, P3 (ASSUMPTION) | DISCOVER | personas |
| 2026-02-20 | Gate 1 attempt 1: MORE DISCOVERY | Gate 1 | `gates/gate-1-attempt-1.md` |
| 2026-02-27 | Gate 1 attempt 2: GO, signed Hira Baig and Faisal Mirza | Gate 1 | `gates/gate-1-attempt-2.md` |
| 2026-03-02 | Vision | PLANNING | vision |
| 2026-03-04 | North star sheet | PLANNING | north star sheet |
| 2026-03-05 | D2, artifact weight | DEFINE | decision log |
| 2026-03-09 | One-pager | DEFINE | one-pager |
| 2026-03-11 | User stories | DEFINE | user stories |
| 2026-03-13 | Acceptance criteria | DEFINE | acceptance criteria |
| 2026-03-18 | Gate 2 attempt 1: RETURNED | Gate 2 | `gates/gate-2-attempt-1.md` |
| 2026-03-20 | D4, customer fee | DEFINE | decision log |
| 2026-03-25 | Gate 2 attempt 2: SIGNED, Hira Baig, Zainab Qureshi, Faisal Mirza, Amna Rasheed | Gate 2 | `gates/gate-2-attempt-2.md` |
| 2026-03-30 | Darya term sheet received | DESIGN | D3 context |
| 2026-04-03 | D3 and ADR-1 | DESIGN | decision log |
| 2026-04-08 | Premortem: R1 to R6 | DESIGN | risk register |
| 2026-04-09 | ADR-2, ADR-3 | DESIGN | architecture records |
| 2026-04-15 | Gate 3 attempt 1: REVIEWED AND ACCEPTED | Gate 3 | `gates/gate-3-attempt-1.md` |
| 2026-04-20 | BUILD starts | BUILD | sprint log |
| 2026-04-30 | DEP-1 met | BUILD | dependency register |
| 2026-05-19 | N58, water validation fails | BUILD | test log |
| 2026-05-21 | D5; one-pager and stories amended; criterion re-reviewed | BUILD, back to Gate 2 | decision log |
| 2026-05-22 | DEP-3 memo | BUILD | dependency register |
| 2026-06-05 | BUILD ends | BUILD | sprint log |
| 2026-06-10 | Gate 4 attempt 1: MET, one miss (AC-8 resume half) | Gate 4 | `gates/gate-4-attempt-1.md` |
| 2026-06-15 to 2026-06-24 | UAT (N51) | DELIVER | UAT log |
| 2026-06-19 | DEP-2 met | DELIVER | dependency register |
| 2026-06-22 | Rollback rehearsal (N50) | DELIVER | release readiness |
| 2026-06-24 | DEP-4 met | DELIVER | dependency register |
| 2026-06-26 | Rollback holding statement drafted | DELIVER | comms plan section 5 |
| 2026-07-01 | Gate 5 attempt 1: CONDITIONAL GO; D6; comms plan signed; review window set (N55) | Gate 5 | `gates/gate-5-attempt-1.md` |
| 2026-07-06 | Launch to 600 pilot agents | OPERATE | comms plan section 1 |
| 2026-07-08 | Bill-peak day in launch week; N52 | OPERATE | helpline |
| 2026-07-09 | USSD timeout spike; LD-1 daily M3 below floor (N67) | OPERATE | incident log |
| 2026-07-10 | D7, nationwide step paused | OPERATE | decision log |
| 2026-07-12 | Week 1 closes: M3 87 percent, 61 DUP-PAY tickets (N46, N47) | OPERATE | comms plan |
| 2026-07-14 | Timeout fix shipped; reconciliation break (N48) explained | OPERATE | incident log |
| 2026-07-17 | Gate 5 condition closed: float top-up hotline live | OPERATE | gate 5 attempt file |
| 2026-07-24 | Nationwide rollout | OPERATE | comms plan |
| 2026-07-27 | Pilot agent debriefs (N60) | OPERATE | debrief notes |
| 2026-08-11, 2026-08-12 | Field observation at 12 counters (N45) | OPERATE | observation notes |
| 2026-08-17 | Review window closes | OPERATE | N55 |
| 2026-08-21 | Post-launch review | OPERATE | post-launch review |
| 2026-08-28 | Gate 6 attempt 1: signed PIVOT with the Gate 1 signal line unticked (no query exists; Open: Sara Lodhi, by 2026-09-21); D8 | Gate 6 | `gates/gate-6-attempt-1.md` |
| 2026-09-07 | Next DISCOVER pass opens, Rafiq at the centre | DISCOVER, pass 2 | product README |
| 2026-09-21 | First recurring metrics review | OPERATE | metrics review, scheduled |
| 2026-09-30 | Commission schedule v8 due (N39) | Open | Bilal Hasan |

## Artifact map

Each file fills one template at the path given, keeps that template's H2 structure, walks its exit gate at the bottom, and links back here. Every number in a file is a row above; every id is in the identifier table.

| File | Fills | Stage and gate | What it decides, and the rows it uses |
|---|---|---|---|
| [sahulat-user-research-plan.md](sahulat-user-research-plan.md) | [templates/discovery/user-research-plan.md](../templates/discovery/user-research-plan.md) | DISCOVER, feeds Gate 1 | Decides what the team must learn before any solution is drawn (RQ1 to RQ4), the method and the behavior-based screener, and in section 6 which themes have three or more sessions behind them; it is the file every persona and evidence row points back to. Uses N17 to N26, N61, N63 and N64, session ids INT-001 to INT-014, themes T1 to T5, answers RQ2 with the pass-through finding, and leaves the balance-keeper question as the open remainder that becomes P3. |
| [sahulat-interview-guide.md](sahulat-interview-guide.md) | [templates/discovery/interview-guide.md](../templates/discovery/interview-guide.md) | DISCOVER, feeds Gate 1 | Decides which question blocks serve which research question, and records in its revision log the v1 to v2 change that cut the leading question about keeping a balance after the two pilot sessions. Uses RQ1 to RQ4, N61 for logistics (Hira leads, Usman takes notes), and INT-001 and INT-002 in the revision log. |
| [sahulat-interview-notes.md](sahulat-interview-notes.md) | [templates/discovery/interview-notes.md](../templates/discovery/interview-notes.md) | DISCOVER, feeds Gate 1 | The raw tagged record of one session, INT-004 (C-04, 2026-02-02), with the surcharge bill shown, the Sunday due date, and the line about never leaving money in the phone, kept apart from what Hira thought it meant. Uses N18, N19, N20 and N24 as its facts, N22 and N25 only as generalizations, the commitment that C-04 let Usman observe her at her agent's counter on 2026-02-09, and hands off E1 and E2. |
| [sahulat-personas.md](sahulat-personas.md) | [templates/discovery/personas.md](../templates/discovery/personas.md) | DISCOVER, feeds Gate 1 | Decides who the product is for: P1 Shazia on six sessions, P2 Rafiq on six, with the agent as a persona per the mobile-money card, and P3 Kamran carrying the ASSUMPTION label on two sessions with its unevidenced claims listed, not hidden. Uses N17, N20, N21, N22, N26 and N64, the session ids per persona, E2, E3 and E5, and names Shazia as Kamran's anti-persona. |
| [sahulat-problem-framing.md](sahulat-problem-framing.md) | [templates/discovery/problem-framing.md](../templates/discovery/problem-framing.md) | DISCOVER, feeds Gate 1 | Decides the one problem sentence Gate 1 states identically, with no solution word in it, and shows the cost-of-inaction arithmetic whose absence failed attempt 1. Uses N10, N13, N18 to N20, N24, N25, N27, N28 and N64, evidence rows E1 to E4 with strength labels, and the decision requested of Faisal Mirza by 2026-02-20. |
| [sahulat-opportunity-assessment.md](sahulat-opportunity-assessment.md) | [templates/discovery/opportunity-assessment.md](../templates/discovery/opportunity-assessment.md) | DISCOVER, feeds Gate 1 | Recommends on 2026-01-15, and Faisal Mirza decides on 2026-01-16 (D1), that bill pay earns discovery effort, in ten answers of one to three sentences, with most claims marked assumption and "customers will keep a balance in order to pay from it" named as the riskiest one. Uses N1, N2, N4, N5, N10, N13, N14, N31, N32, N57, N64 and N65, and logs the go as D1. |
| [sahulat-one-pager.md](sahulat-one-pager.md) | [templates/definition/one-pager.md](../templates/definition/one-pager.md) | DEFINE, feeds Gate 2 | Decides scope at the one-pager weight: the problem with E1 and E2 as source ids, the proposal, the Rel-1 scope with story ids, outcome metrics M1 and M2 (the hypothesis, written so it could fail), guardrails M3 and M4 with digits, and a not-doing list of things people wanted (water after D5, a customer fee, the app first, the Darya rail, merchant QR). Uses N42, N43, N46, N10, N33, SAHULAT-S1 to S11, AC-1 to AC-13, R1 to R6, D2 to D5, amended 2026-05-21 per D5. |
| [sahulat-acceptance-criteria.md](sahulat-acceptance-criteria.md) | [templates/definition/acceptance-criteria.md](../templates/definition/acceptance-criteria.md) | DEFINE, feeds Gate 2, verified at Gate 4 | Decides the pass-or-fail contract AC-1 to AC-13 with every threshold labelled ILLUSTRATIVE, the dropped-session and duplicate cases that R2 later exercised, AC-9 from the acquiring card's question about approved payments whose fulfilment fails, and AC-13 for the tier limit. Uses N56 and N66, stories SAHULAT-S1 to S11 in the coverage summary, and records the resume half of AC-8 as the Gate 4 miss with Zainab Qureshi as owner. |
| [sahulat-user-stories.md](sahulat-user-stories.md) | [templates/definition/user-stories.md](../templates/definition/user-stories.md) | DEFINE, feeds Gate 2, worked through BUILD | Decides the walking skeleton (Shazia looks up one Ravi Power bill by reference on USSD, pays it from balance, and gets an SMS reference), the Rel-1 and Rel-2 slices, defines SAHULAT-S1 to S11 under EP1 to EP3, kills S7 at D5 with its id spent, and runs INVEST on the five post-D5 musts, S8 failing on E and S, the original Gate 2 verdicts not preserved. Uses P1 to P3, AC-1 to AC-13 in traceability, N58 and D5, and the single one-pager objective every story serves. |
| [sahulat-vision.md](sahulat-vision.md) | [templates/planning/vision.md](../templates/planning/vision.md) | PLANNING track, feeds every stage | Decides the 2029 destination in Shazia's terms (the month's bills settled without a trip, the paper bill proof of nothing she needs), the why-now, and non-goals with revisit conditions: no credit, no balance-dependent design ahead of a DISCOVER pass finding three of eight or more customers holding a balance, no merchant acquiring, no app-first strategy, no bank rail, and no scheme interoperability work in this horizon. Uses N1, N2, N10, N13, N14 and N62, names M5 as the north star, and states the observation that would mean it failed. |
| [sahulat-north-star-metric.md](sahulat-north-star-metric.md) | [templates/planning/north-star-metric.md](../templates/planning/north-star-metric.md) | PLANNING track, scored at Gate 6 | Decides the north star M5 with its vanity test written, four inputs each with one owner (wallets paying at least one bill this month, Hira; cash-in to on-ledger spend within seven days, Tariq; M3, Zainab; agents with float on bill-peak days, Tariq), and three guardrails with a numeric floor or ceiling and named halt-callers, one of which Zainab pulled in D7. Uses N14, N15, N10, N11, N46, N48, N53 and N57, reads the 2026-08-21 post-launch review as its first review, and schedules the first recurring monthly review for 2026-09-21. |
| [sahulat-decision-log.md](sahulat-decision-log.md) | [templates/execution/decision-log.md](../templates/execution/decision-log.md) | All stages, reviewed at every gate | Holds D1 to D8 with the index newest first, the options that lost and what each decision gave up: D3 rejecting Darya on N34, N35 and N37 against N38 with its reopen condition, D5 as the explicit return to Gate 2, D7 as a guardrail halt by its named caller, D8 as the pivot, and a gate-review table across all six gates. Uses N33 to N39, N46 and N58, every gate attempt date, and links ADR-1 to ADR-3 rather than duplicating them. |
| [sahulat-launch-comms-plan.md](sahulat-launch-comms-plan.md) | [templates/delivery/launch-comms-plan.md](../templates/delivery/launch-comms-plan.md) | DELIVER, feeds Gate 5 | Decides the one set of launch facts (what ships 2026-07-06, staged per D6), the audience rows with an action, an owner and a sign-off each (pilot agents, all agents, support, on-call, customers by SMS, billers via BillBridge, the board), the T-minus timeline with support briefed before any external message, and the rollback holding statement approved by Faisal Mirza with Naveed Akhtar as designated sender; never sent, and D7's pause message was derived from it. Uses N5, N6, N40, N41, N50, D6, the Gate 5 condition, and the day-1 report of M1 and M3 from LD-1, Sara Lodhi to Faisal and Hira. |
| [sahulat-post-launch-review.md](sahulat-post-launch-review.md) | [templates/operate/post-launch-review.md](../templates/operate/post-launch-review.md) | OPERATE, feeds Gate 6 | Decides, with targets quoted from the one-pager (and the signal from `gates/gate-1-attempt-2.md`), that M1 missed (31,200 against 40,000), M2 missed badly (9 percent against 50 percent), M3 recovered to 92 percent after the week-1 breach, reconciles R1 to R6 against what arrived plus the unpredicted agent-assisted behaviour, and sends every follow-up out of the file toward the PIVOT Gate 6 signs a week later. Uses N42 to N53, N16, N59 and N60, the verbatim quotes, R1 to R6, D7 and D8, and schedules the first recurring metrics review for 2026-09-21. |

## What this journey teaches

- **The research plan:** the second row of the worked micro-example is the one that matters. Hira wrote down, before fielding, that if fewer than three of eight customers kept a balance the plan would change; two did, and the plan did not change, which is the failure the rest of the journey pays for.
- **The interview guide:** a leading question is the hypothesis wearing a question mark. "Would you keep money in the wallet if you could pay bills?" was cut after two pilots, and the replacement, "the last time money sat in the wallet for more than two days, what was it for?", drew the 19:00 answer in INT-004 (no recall of money ever sitting two days), beside E2.
- **The interview notes:** the record and the reading are kept apart so a later reader can disagree with the PM while trusting the notes. Section 2 of INT-004 was quoted unchanged in the review six months later; the interpretation in section 7 was not.
- **The personas:** a persona labelled ASSUMPTION is legal. Designing the outcome metric around one and scoring its risk low is the disguise the template warns about, and the label did not stop it because nobody read the label at DESIGN.
- **The problem framing:** the same cost of inaction failed Gate 1 once and passed it once. The difference was the arithmetic on the page, which is what let the sponsor argue with the number instead of resenting it.
- **The opportunity assessment:** the riskiest assumption was named in the first week and was still the one that failed. Naming it is cheap; the expensive part is treating it as a test with a result that changes the plan.
- **The one-pager:** a hypothesis written as a metric with a target and a date is falsifiable, and this one was falsified. The same hypothesis written as "customers will value paying from balance" would have survived the review.
- **The acceptance criteria:** the unhappy paths were the contract's value. AC-7, AC-8 and AC-10 came from one interview line (E4), and the half of AC-8 accepted as a miss at Gate 4 is the exact defect that breached the guardrail in launch week.
- **The user stories:** a killed id stays dead. SAHULAT-S7 was killed in BUILD by an explicit return to Gate 2, and the next pass will not reuse the number.
- **The vision:** the non-goals did the work. "No merchant acquiring" and "no bank rail" were each proposed by someone during the journey, and the argument happened once because the reason and the revisit condition were already written.
- **The north star sheet:** a guardrail with a digit and a named halt-caller is the only guardrail that fires. M3's floor of 90 percent and Zainab's name on it are why D7 exists; a floor of "must not degrade" would have produced a discussion instead.
- **The decision log:** the rejected option is worth more than the chosen one. D3 records the nine weeks and the 210 billers Sahulat gave up and the cut-off that would reopen the decision, so the next PM does not have to re-argue it from a term sheet nobody kept.
- **The launch comms plan:** the rollback message written while everyone was calm was never sent, and the pause message in D7 was derived from it in ten minutes because the launch facts existed once.
- **The post-launch review:** a review that records a miss produces a decision; a review that rounds up produces a zombie. The one-pager targets and the premortem rows were quoted unchanged; the Gate 1 signal was quoted but not measured.
