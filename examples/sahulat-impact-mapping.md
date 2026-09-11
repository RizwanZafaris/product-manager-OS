# Impact mapping: Sahulat Bill Pay

Fills [frameworks/prioritization/impact-mapping.md](../frameworks/prioritization/impact-mapping.md). Everything here is invented: Sahulat, its people, customers, agents, billers, aggregator and telco are fictional, and every number is ILLUSTRATIVE, taken from the [Sahulat journey data sheet](sahulat-journey.md) and its [coverage sheet](sahulat-coverage-sheet.md).

**Owner:** Hira Baig, Product Manager · **Date:** 2026-03-06 · **Status:** Working map between D2 and the one-pager

## What it is for

This map connects the board key result to the actors, behavior changes and candidate deliverables for Sahulat bill pay. It is based on the ideas of Gojko Adzic, from Impact Mapping (2012), expressed in this repository's own words.

The goal is to move from 410,000 measured 30-day active wallets to the board target of 520,000 30-day active wallets by 2026-12-31.

**Arithmetic:** 520,000 target wallets minus 410,000 baseline wallets equals a gap of 110,000 30-day active wallets.

Every row below is a hypothesis. A deliverable is retained only when it has a path through an actor and a behavior change to the goal. P3, Kamran, is explicitly labelled ASSUMPTION. SAHULAT-S5, SAHULAT-S10 and SAHULAT-S11 hang only from the Kamran path and are marked **test**, rather than being treated as established scope.

## Run it when

- An objective exists and the team needs to turn it into scope without inheriting the backlog.
- A candidate feature needs a visible path to the board key result.
- The one-pager needs objectives, scope and out-of-scope decisions grounded in actor behavior.
- A hypothesis needs a cheap test before the team commits engineering capacity.

This map is being run on 2026-03-06, after D2 selected the one-pager weight and before the one-pager was written. The map does not decide that every deliverable will ship. It identifies which links need evidence or testing.

## Inputs you need first

- The goal, baseline and target from the Sahulat data sheet: N2 and N4 in [sahulat-journey.md](sahulat-journey.md).
- The actors and personas P1, P2 and P3 from the same data sheet.
- Evidence E2, E3 and E5 from [sahulat-journey.md](sahulat-journey.md).
- Candidate story identifiers SAHULAT-S1 to SAHULAT-S11 from [sahulat-journey.md](sahulat-journey.md).
- The later coverage note that this map is dated 2026-03-06 and feeds the one-pager, in [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md).

## The worksheet

### Level 1: the goal

| Goal (one sentence, an outcome, not a deliverable) | Metric | Baseline | Target | By when | Owner |
|---|---|---|---|---|---|
| Increase the number of wallets active in the trailing 30 days through on-ledger bill-pay behavior | 30-day active wallets | 410,000 wallets, N2, measured from the Core ledger, query NS-02 | 520,000 30-day active wallets, N4, target | 2026-12-31 | Faisal Mirza |

**Goal arithmetic:** 410,000 baseline wallets + 110,000 additional wallets = 520,000 target wallets.

### Level 2: actors

| Actor | Type | What they do today | Evidence |
|---|---|---|---|
| Shazia, P1 | primary user | Pays household bills in person on or near the due date, with a trip and sometimes a fee or surcharge. | P1; E2; the P1 sessions are listed in [sahulat-journey.md](sahulat-journey.md) |
| Rafiq, P2 | secondary user | Fields bill questions at the counter and refers customers to a shop when he cannot complete the bill payment. | P2; E3 |
| Kamran, P3, ASSUMPTION | primary user hypothesis | Is assumed to keep a wallet balance and to prefer paying bills from that balance. The evidence is limited to two customer sessions. | P3; E5; the ASSUMPTION label and its evidence boundary are recorded in [sahulat-journey.md](sahulat-journey.md) |
| Billers through BillBridge | secondary, external | Receive bill-payment postings through the aggregator and determine whether a payment is posted successfully. | BillBridge and biller context in [sahulat-journey.md](sahulat-journey.md) |
| Naveed's support desk | internal | Answers customer questions about whether a bill payment went through and needs a searchable payment reference. | Naveed Akhtar's support role and SAHULAT-S9 in [sahulat-journey.md](sahulat-journey.md) |
| Falak Telecom | hindering actor | Controls the USSD gateway and short-code menu on which the bill-pay journey depends. Delays or failures in the gateway can prevent the intended behavior. | Falak Telecom context in [sahulat-journey.md](sahulat-journey.md) |

### Level 3: impacts

An impact is a behavior change, not a feature. The links below are hypotheses about what each actor would do differently and why that behavior could contribute to the 110,000-wallet gap.

| Actor | Impact (behavior change) | How you would observe it | Why it moves the goal |
|---|---|---|---|
| Shazia, P1 | Starts looking up a household bill through Sahulat before making an in-person trip. | Bill-lookup events on the ledger and USSD logs, linked to wallets that become 30-day active. | A bill-related wallet action creates a reason for a registered wallet to return and can move it into the active-wallet measure. |
| Shazia, P1 | Starts paying an electricity or gas bill through Sahulat before the due date. | Successful bill-payment postings through BillBridge, with the wallet active in the trailing 30 days. | A completed payment is an on-ledger behavior that can support recurring wallet activity. |
| Shazia, P1 | Gets and keeps proof that the payment posted, instead of making a repeat attempt or returning to a shop. | SMS reference delivery and support contacts about uncertain payment status. | Confidence in the first payment can reduce failed repeat attempts and support another bill payment in a later active window. |
| Rafiq, P2 | Starts helping a customer complete a bill payment during the same agent visit. | Agent-assisted payment records and agent-reported bill-pay activity. | The agent can turn a bill question into an on-ledger payment for customers who would otherwise leave the wallet journey incomplete. |
| Rafiq, P2 | Stops referring bill-paying customers to the shop across the road. | Agent debriefs and support or referral notes showing fewer referrals. | Keeping the transaction at the Sahulat counter gives the wallet an opportunity to record active use. |
| Kamran, P3, ASSUMPTION | Starts keeping a wallet balance for more than two days so a future bill can be paid from it. | Balance history and bill payments funded from a balance held more than two days. | If this assumption is true, stored balance may create repeat wallet activity without a same-day cash-in. |
| Billers through BillBridge | Accept bill payments from Sahulat and post them to the customer account within the agreed service path. | BillBridge posting status, biller confirmation and exceptions in reconciliation. | A payment that posts successfully can prevent a customer from abandoning the channel and can support repeat use. |
| Naveed's support desk | Resolves a payment-status question on the first call by searching the bill reference. | Support lookup time and repeat contacts for the same payment. | Fast resolution protects trust in the wallet and reduces abandonment after an uncertain payment. |
| Falak Telecom | Keeps the Sahulat bill-pay menu available and responsive for the required customer journey. | USSD availability, session logs and bill-pay completion signals. | If the gateway blocks the journey, customers cannot look up or pay a bill through Sahulat, so the path to active-wallet growth stops. |

### Level 4: deliverables

All sizes remain open. **Open: Zainab Qureshi** owns the engineering sizing answer. The deliverable decisions below are scope hypotheses, not engineering commitments.

| Deliverable | Impact it serves | Assumption connecting them | Cheapest test of the assumption | Size | Keep, test, or cut |
|---|---|---|---|---|---|
| SAHULAT-S1, USSD lookup of a Ravi Power bill by reference | Shazia starts looking up a household bill through Sahulat | If Shazia can enter the reference and see the amount and due date, she will use Sahulat before making an in-person trip. | Walk through the USSD lookup with P1 participants using the bill reference and ask what they would do next. | Open: Zainab Qureshi | Keep, subject to the lookup behavior test |
| SAHULAT-S2, pay from wallet balance and receive an SMS reference | Shazia starts paying an electricity or gas bill through Sahulat; Shazia gets and keeps proof | If the payment completes and the SMS contains a reference, Shazia will trust the payment rather than repeat it or return to a shop. | Test a paper or scripted payment flow with P1 and ask the participant to find and explain the payment proof. | Open: Zainab Qureshi | Keep, subject to payment and proof tests |
| SAHULAT-S3, cash in at an agent and pay in the same visit | Rafiq starts helping a customer complete a bill payment during the same agent visit | If cash-in and bill payment can happen in one visit, the customer will not need a second trip. | Role-play the full same-visit journey with Rafiq and a P1 customer, without building the integration. | Open: Zainab Qureshi | Keep, subject to same-visit test |
| SAHULAT-S4, confirmation on the agent handset for a customer payment | Rafiq starts helping a customer complete a bill payment during the same agent visit | If Rafiq sees confirmation, he can vouch for the payment when asked. | Show a scripted confirmation message to Rafiq after a simulated payment and ask what evidence he would use at the counter. | Open: Zainab Qureshi | Keep, with the confirmation behavior still to test |
| SAHULAT-S5, save a reference after paying | Kamran, P3, ASSUMPTION, starts keeping a wallet balance for more than two days | If Kamran can save the reference, he will keep money in the wallet for the next bill instead of cashing out or funding the payment on the same day. | Test the saved-reference and balance-holding proposition with the two P3 sessions and explicitly seek disconfirming behavior. | Open: Zainab Qureshi | **Test**, only on the Kamran path |
| SAHULAT-S6, pay a Chenab Gas bill through the same channel | Shazia starts paying an electricity or gas bill through Sahulat | If the same bill-pay behavior works for a second household utility, Shazia will use the channel for more than one payment. | Test a Chenab Gas reference in the same scripted lookup and payment flow. | Open: Zainab Qureshi | Keep, subject to the cross-biller test |
| SAHULAT-S7, pay a Mehran Water bill through the same channel | Shazia starts paying an electricity or gas bill through Sahulat | If water can use the same flow, the household can consolidate another bill into Sahulat. | Validate a sample Mehran Water reference through the existing bill-pay test path before committing build scope. | Open: Zainab Qureshi | Keep for this map, with validation required before later scope decisions |
| SAHULAT-S8, tell the customer whether money moved after a dropped session | Shazia gets and keeps proof that the payment posted | If a dropped session reports the payment state, Shazia will wait for the result rather than dial again and risk a repeat payment. | Simulate a dropped session after payment and ask P1 what action she would take after each status message. | Open: Zainab Qureshi | Keep, subject to the dropped-session test |
| SAHULAT-S9, support lookup by bill reference | Naveed's support desk resolves a payment-status question on the first call | If the support desk can find the payment by reference, it can answer the first contact without sending the customer elsewhere. | Give a support agent scripted payment references and measure whether the correct status can be found in the proposed lookup flow. | Open: Zainab Qureshi | Keep, subject to support lookup test |
| SAHULAT-S10, app lookup and payment flow | Kamran, P3, ASSUMPTION, starts keeping a wallet balance for more than two days | If Kamran can use the app instead of USSD, he will choose the app and keep a balance for future bill payments. | Compare the app proposition with the USSD proposition in the P3 sessions, without building the app flow. | Open: Zainab Qureshi | **Test**, only on the Kamran path |
| SAHULAT-S11, reminder SMS three days before a saved bill's due date | Kamran, P3, ASSUMPTION, starts keeping a wallet balance for more than two days | If Kamran receives a reminder, he will cash in before the surcharge and leave the money in the wallet until payment. | Test the reminder proposition with the P3 evidence and ask what actually caused the last balance to remain for more than two days. | Open: Zainab Qureshi | **Test**, only on the Kamran path |

**Path arithmetic and concentration:**

- Board gap: 520,000 target wallets minus 410,000 baseline wallets equals 110,000 additional 30-day active wallets.
- Kamran path deliverables: SAHULAT-S5 + SAHULAT-S10 + SAHULAT-S11 = 3 deliverables.
- Shazia's direct bill-pay path: SAHULAT-S1 + SAHULAT-S2 + SAHULAT-S6 + SAHULAT-S7 + SAHULAT-S8 = 5 deliverables.
- Same-visit agent path: SAHULAT-S3 + SAHULAT-S4 = 2 deliverables.
- Support path: SAHULAT-S9 = 1 deliverable.
- Total deliverables: 3 + 5 + 2 + 1 = 11, matching SAHULAT-S1 to SAHULAT-S11.
- Kamran's three deliverables are not assigned to Shazia, Rafiq, billers, Naveed's support desk or Falak Telecom. They hang only from the P3, ASSUMPTION path.

The Kamran path has the most balance-first deliverables, but it has the weakest evidence: E5 is one statement from INT-003, and the persona cites INT-003 and INT-006 only. E2 points in the opposite direction, with the customer saying money is put in the wallet only when needed for same-day sending. E3 supports the agent path, with the agent reporting six or seven bill questions a day and referring customers to the shop.

**Paths read aloud:**

- “To increase 30-day active wallets from 410,000 to 520,000 by 2026-12-31, Shazia starts paying household bills through Sahulat, because the bill lookup, payment and proof flow lets her complete the task without relying on an in-person trip.”
- “To increase 30-day active wallets from 410,000 to 520,000 by 2026-12-31, Rafiq starts helping customers pay during the same visit, because the same-visit flow prevents a bill question from ending in a referral.”
- “To increase 30-day active wallets from 410,000 to 520,000 by 2026-12-31, Kamran, an ASSUMPTION, starts keeping a balance for more than two days, because saved references, an app flow and a reminder SMS make future balance-funded payments more likely.”
- “To increase 30-day active wallets from 410,000 to 520,000 by 2026-12-31, Naveed's support desk resolves payment-status questions on the first call, because a reference lookup protects confidence after an uncertain payment.”
- “To increase 30-day active wallets from 410,000 to 520,000 by 2026-12-31, Falak Telecom keeps the bill-pay menu available and responsive, because without the gateway the customer cannot complete the bill-pay journey.”

## Reading the result

The map contains 11 deliverables across five actor paths:

| Actor path | Deliverables | Count | Reading |
|---|---|---:|---|
| Shazia, P1 | SAHULAT-S1, S2, S6, S7, S8 | 5 | Largest concentration. The direct customer path is the clearest route to an on-ledger payment, but each deliverable remains a hypothesis. |
| Rafiq, P2 | SAHULAT-S3, S4 | 2 | A shorter path with evidence from E3 that bill questions already reach agents. |
| Kamran, P3, ASSUMPTION | SAHULAT-S5, S10, S11 | 3 | The most concentrated balance-first sub-path, but the least secure evidence. All three are test, not keep. |
| Naveed's support desk | SAHULAT-S9 | 1 | A supporting path that protects trust after a payment-status question. |
| Falak Telecom | Gateway behavior, with no SAHULAT story assigned yet | 0 | A hindering actor and dependency. The map records the risk without inventing a deliverable identifier. |
| Billers through BillBridge | Posting behavior, with no SAHULAT story assigned yet | 0 | A required external behavior. The map records the hypothesis without inventing a story identifier. |

The shortest direct path to the goal is:

1. Shazia, P1, looks up a bill.
2. Shazia pays the bill through Sahulat.
3. The biller through BillBridge posts the payment.
4. Shazia receives proof and returns for later bill activity.

The cheapest tests are the lookup and proof flows, the same-visit agent role-play, and the explicit Kamran balance-holding test. The link most likely to be wrong is the Kamran deliverable-to-impact link. E5 supports the existence of one balance-keeper, while E2 says the opposite behavior is present. Therefore SAHULAT-S5, SAHULAT-S10 and SAHULAT-S11 are marked **test** and do not receive an unqualified keep decision.

The map also exposes two non-deliverable dependencies:

- Billers through BillBridge must post payments reliably. If they do not, the customer behavior does not produce trusted active use.
- Falak Telecom must keep the USSD route available and responsive. If it hinders the journey, the Shazia and Rafiq paths cannot be observed.

## ILLUSTRATIVE example

Sahulat's board key result is to increase 30-day active wallets from 410,000 to 520,000 by 2026-12-31.

The board gap is:

**520,000 - 410,000 = 110,000 additional 30-day active wallets.**

The map does not claim that every bill payment creates a new active wallet. It identifies the behavior that must be tested: a customer uses Sahulat for a bill, the payment posts through BillBridge, and the customer trusts the result enough to use the wallet again.

The strongest evidenced path is Shazia, P1, because the research includes the household bill-running behavior and E2 describes same-day use of wallet money. The agent path is also grounded in E3, where an agent reports six or seven bill questions a day and refers customers to another shop. The Kamran path is deliberately weaker. E5 shows one customer who keeps two or three thousand in the wallet because salary comes there, but that is not enough evidence to treat saved references, an app flow and reminder SMS as proven drivers of wallet activity.

The resulting decisions are:

- Keep the direct bill lookup, payment, proof, same-visit agent and support hypotheses visible.
- Test the three Kamran-only deliverables separately.
- Do not allow SAHULAT-S5, SAHULAT-S10 or SAHULAT-S11 to acquire a second actor path.
- Keep Falak Telecom and BillBridge visible as actors that can hinder or enable the goal.
- Leave all sizes **Open: Zainab Qureshi** until the engineering lead estimates them.

## The trap

The map could have been drawn backward from a preferred balance-first backlog. That would have put SAHULAT-S5, SAHULAT-S10 and SAHULAT-S11 under a general customer impact and made the weak Kamran evidence invisible.

Instead, the map preserves the ASSUMPTION label on P3 and keeps those three deliverables on the Kamran path only. E2 is a counter-signal to the balance-first hypothesis, while E5 is the evidence that originally made the hypothesis attractive. The correct response is a test, not a wider impact claim.

The map also includes hindering and enabling external actors. Falak Telecom can block the USSD path, and billers through BillBridge can determine whether a payment is trusted after the customer has initiated it. Omitting them would make the tree look tidy while hiding the conditions that can break it.

## Feeds

- [sahulat-journey.md](sahulat-journey.md): N2, N4, P1 to P3, E2, E3, E5 and SAHULAT-S1 to SAHULAT-S11.
- [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md): the 2026-03-06 placement of this impact map between D2 and the one-pager, and its role in the DEFINE entry.
- The one-pager: goal, impact hypotheses, the three Kamran-only items marked **test**, and the out-of-scope reasoning.
- The assumptions register: the deliverable-to-impact links, especially the balance-first links for SAHULAT-S5, SAHULAT-S10 and SAHULAT-S11.
- The decision log: the later scope decisions and any cut or test decision that follows from this map.
- Method background: Gojko Adzic's *Impact Mapping* (2012), represented in the blank worksheet at [frameworks/prioritization/impact-mapping.md](../frameworks/prioritization/impact-mapping.md).

**Exit-gate walk:** Hira Baig, Product Manager, signed 2026-03-06. Goal, actors, impacts and deliverables have paths; SAHULAT-S5, SAHULAT-S10 and SAHULAT-S11 are marked **test** and hang only from Kamran, P3, ASSUMPTION; sizes remain **Open: Zainab Qureshi**.
