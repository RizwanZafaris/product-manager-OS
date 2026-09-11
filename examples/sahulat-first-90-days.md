# First 90 Days: Hira Baig, Product Manager, Sahulat Bill Pay

Fills [templates/planning/first-90-days.md](../templates/planning/first-90-days.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, Hira Baig and every other person are fictional, and every number and date is ILLUSTRATIVE, drawn from the shared data sheets in [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md). See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager · **Date:** 2026-02-28 · **Status:** Closed at day 90; bill pay walked to Gate 1 attempt 2 on 2026-02-27

**Start date:** 2025-12-01 · **Written:** 2025-12-01 · **Shared with:** Faisal Mirza

## 1. The mandate, in the words of the person who hired you

- **What they said the job is:** "The board will hold me to active wallets next year, not registrations. Find me something that keeps money on the ledger." (MQ-1, Faisal Mirza, 2025-12-01)
- **What they said would count as success at 90 days:** "Come back by the end of February with one thing worth building and the reason it will work." (MQ-2, Faisal Mirza, 2025-12-01)
- **What they said is broken today:** "We pay agents twice for money that never stays." (MQ-3, Faisal Mirza, 2025-12-01)
- **Where your read already differs:** The first useful bet may be a payment that puts money on the ledger, not a cashback promotion intended to make customers hold a balance.

## 2. The three questions you must answer to be useful

| # | Question | Why it decides something | How you will answer it | Answered by |
|---|---|---|---|---|
| Q1 | Is the ledger problem a real customer and business problem, rather than only a board metric? | If money enters and leaves immediately, a product that creates an on-ledger payment is more relevant than a promotion that asks customers to hold money without a job to do. | Compare the active-wallet and pass-through baselines, then speak with customers and agents about what the money is for and when it leaves. | day 75 |
| Q2 | Is there a concrete payment job worth taking into discovery now? | A bill-pay bet competes with the cashback promotion for the first 90-day commitment. The answer must identify a problem customers already pay to solve. | Add the BILL-ASK tag, review the helpline evidence, and test the bill-paying job with customers and agents without proposing a solution in the sessions. | day 75 |
| Q3 | What evidence would make bill pay worth building, and what signal should Gate 1 use? | Gate 1 needs a problem, an outcome signal and a reason to proceed, not a feature request or usage target. | Run the planned customer and agent sessions, synthesize the costs and behaviours, and take the problem framing and opportunity assessment to Gate 1. | day 89 |

**Answers at day 90:**

- **Q1:** The business had 410,000 30-day active wallets in December 2025 (N2), against a 2026 target of 520,000 by 2026-12-31 (N4), while 61 percent of cash-ins were fully cashed out within 48 hours (N10). The customer and agent conversations showed that money often enters for a bill or another immediate purpose and leaves the same day. The ledger problem is real, but a balance-holding promotion is not yet the right answer.
- **Q2:** Yes. The trigger was 412 agent-helpline calls asking about bill pay in the four weeks to 2026-01-09 (N13). The bill-paying job had a visible customer cost, including a median 70-minute round trip and PKR 60 transport per trip (N20), and it could create an on-ledger payment rather than only another cash-in and cash-out cycle.
- **Q3:** Gate 1 attempt 2 on 2026-02-27 set the outcome signal as: a bill due in the household is paid through Sahulat before its due date, and no late surcharge is paid that month. The evidence was 14 research sessions, 8 customers and 6 agents, from 2026-01-26 to 2026-02-13 (N17), plus the cost and behaviour evidence used in the problem framing. Gate 1 attempt 2 was GO.

## 3. Days 1 to 30: learn, and change nothing structural

**Posture:** listen, document, and earn the right to be wrong later.

| # | Action | Output that proves it happened | By day |
|---|---|---|---|
| 1 | Meet every function that can block a launch: engineering, design, data, support, sales, legal, finance, operations | Meeting notes with concerns in each function's words, plus an input list for the stakeholder map. The stakeholder map was not completed. | 15 |
| 2 | Read the last two quarters of decisions and postmortems | A private list of three decisions to revisit, including the cashback promotion sequencing question and the missing payment job behind the pass-through problem | 20 |
| 3 | Watch the product being used by a real customer, unassisted | Observation notes from the customer and agent context, including the same-day movement of money and the effort involved in paying a bill | 25 |
| 4 | Find the numbers: what is instrumented, what is trusted, what is quoted and unsourced | A metric inventory naming N2, N4, N10, N13 and N14, with their sources, owners or open ownership called out | 30 |
| 5 | Run the first bill-pay evidence check without proposing a solution | A tagged helpline read showing CN4's early BILL-ASK volume (198 calls in the tag's first two weeks), the bill-paying cost, and the balance-holding assumption as the risk to test. N13's full four-week count of 412 calls closes 2026-01-09 and feeds the opportunity assessment after month one, not this check | 30 |

**The one thing you may change in month one:** Add the BILL-ASK tag to the agent helpline, at Hira Baig's request and with Naveed Akhtar, on 2025-12-12. It was small, visible and reversible. It produced CN4, 198 calls in the tag's first two weeks from 2025-12-13 to 2025-12-26, a subset of N13's 412 calls counted over the full four-week window that closes 2026-01-09. No structural product, team or process change was made.

## 4. Days 31 to 60: form a view and test it in public

**Posture:** commit to a reading, invite the strongest objection to it.

| # | Action | Output | By day |
|---|---|---|---|
| 1 | Write your diagnosis of the product's central problem, in one page | A diagnosis circulated for argument: households pay utility bills in person near the due date, while Sahulat's cash-in behaviour shows that money often does not stay in the wallet long enough to support an on-ledger payment | 40 |
| 2 | Take the diagnosis to the three people most likely to disagree | The diagnosis reviewed with Faisal Mirza, Zainab Qureshi and Sara Lodhi, with the balance-first assumption and the evidence limits written into the opportunity assessment | 45 |
| 3 | Decide which loop stage the product is actually in and what gate it skipped | An entry in [sahulat-decision-log.md](sahulat-decision-log.md) recording D1: enter DISCOVER on bill pay, not on a keep-balance cashback promotion | 50 |
| 4 | Rework the roadmap with the team, not for them | A discovery-first roadmap draft with the cashback promotion given up and bill pay taken to Gate 1 before build | 60 |
| 5 | Judge task-relevant maturity per person for the work you intend to delegate | A private note on delegation readiness for the work at hand, with the judgement to be revisited after the discovery evidence | 60 |

## 5. Days 61 to 90: commit, in writing, to something that can fail

**Posture:** one commitment with a date and a number attached.

- **The commitment:** Walk Sahulat bill pay to Gate 1 by 2026-02-27, with the outcome signal that a bill due in the household is paid through Sahulat before its due date, and no late surcharge is paid that month. The agreed NS-01 baseline was 96,000 wallets with at least one on-ledger payment in the trailing 30 days (N14).
- **The metric owner who agreed the baseline:** Sara Lodhi, 2026-01-30; NS-01 baseline, 96,000 wallets (N14).
- **What you gave up to make room for it:** The cashback promotion intended to make customers keep a balance, recorded in D1.
- **How it can fail, and what you will do then:** If the research cannot show a customer problem, an outcome signal or a credible reason to proceed, return to Faisal Mirza with the evidence and do not take bill pay through Gate 1.

| # | Action | Output | By day |
|---|---|---|---|
| 1 | Publish the plan for the next two quarters, with the cuts named | A discovery and Gate 1 plan reviewed with Faisal Mirza, with cashback promotion work cut and bill pay named as the commitment | 75 |
| 2 | Close the operating gap found on day 50, or schedule it with an owner | Gate 1 packet in gate order: opportunity assessment, research evidence, problem framing and the outcome signal, with the Gate 1 attempt recorded | 85 |
| 3 | Review this document against section 1 with your manager | Day-90 note with Faisal Mirza on 2026-02-28: the day-one read was wrong about the cashback promotion being the best first move, and right that the product needed an on-ledger payment job | 90 |

Gate 1 attempt 1 on 2026-02-20 was MORE DISCOVERY because the cost of inaction lacked arithmetic and the success signal was usage. Gate 1 attempt 2 on 2026-02-27 was GO after the signal was rewritten as the household outcome above.

## 6. First meetings

| Person | Function | What this first meeting is for | Held on |
|---|---|---|---|
| Faisal Mirza | Chief Executive, sponsor | Hear the mandate, the 90-day success test and the broken operating assumption | 2025-12-01 |
| Zainab Qureshi | Engineering lead | Understand technical constraints and what could block a payment launch | 2025-12-02 |
| Tariq Sohail | Head of agent network | Understand agent behaviour, customer questions and the cash-in context | 2025-12-03 |
| Amna Rasheed | Head of compliance and regulatory affairs | Identify licence, notification and compliance constraints | 2025-12-04 |
| Bilal Hasan | Finance and treasury lead | Understand agent economics, reconciliation and the cost of money moving through the wallet | 2025-12-05 |
| Naveed Akhtar | Customer support lead | Establish what customers and agents already ask support, then add the BILL-ASK tag | 2025-12-08 |
| Sara Lodhi | Data analyst | Establish trusted baselines and agree the NS-01 baseline | 2025-12-09 |
| Usman Javed | Agent operations officer | Observe the agent counter and plan field access | 2025-12-10 |
| Mariam Gill | QA engineer | Understand how a future bill-pay flow could be tested without assuming its design | 2025-12-11 |

Full map: not created. The stakeholder-map box remains unticked.

## 7. What you will deliberately not do in 90 days

- Do not launch or optimize the cashback promotion before testing the bill-pay and balance-holding assumptions.
- Do not build bill pay before the discovery evidence and Gate 1 decision.
- Do not make a structural team, product or tool change in month one beyond the reversible BILL-ASK tag.
- Do not treat registrations as the success measure when the mandate is about active wallets and on-ledger payment behaviour.
- Do not build a stakeholder map and claim it exists; the map remains an explicit gap.

## Exit gate

This plan is fit to share with your manager when:

- [x] The mandate section quotes an actual conversation, not an inference. MQ-1 to MQ-3 are quoted from Faisal Mirza's 2025-12-01 conversation.
- [x] There are exactly three learning questions, each answerable inside the window. Q1 and Q2 are answered by day 75, once the customer and agent sessions (2026-01-26 to 2026-02-13) were in; Q3 is answered by day 89, the day of Gate 1 attempt 2's GO.
- [x] Month one contains no structural change beyond the one named reversible item. The only change was the BILL-ASK tag added on 2025-12-12.
- [x] The diagnosis in month two was tested against named people who disagreed. The diagnosis was taken to Faisal Mirza, Zainab Qureshi and Sara Lodhi, with the balance-first assumption and evidence limits open to challenge.
- [x] The 90-day commitment carries a number, a date, and a metric owner who agreed the baseline. The commitment uses the NS-01 baseline of 96,000 wallets, the 2026-02-27 Gate 1 date and Sara Lodhi's agreement on 2026-01-30.
- [x] Something was given up to make room for the commitment. D1 gave up the cashback promotion.
- [ ] The stakeholder map exists as its own document and this plan links to it. No stakeholder map was completed.
- [x] The not-doing list is written down.

Signed: Hira Baig, Product Manager, 2026-02-28
