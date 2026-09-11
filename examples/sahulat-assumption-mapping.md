# Assumption mapping: Sahulat Bill Pay, pass 2

Fills [frameworks/discovery/assumption-mapping.md](../frameworks/discovery/assumption-mapping.md). Everything here is invented: Sahulat, its people, agents, customers, billers, bank, aggregator and telco are fictional, and every number is ILLUSTRATIVE, chosen so that this worksheet agrees with the [Sahulat journey data sheet](sahulat-journey.md) and the [Sahulat coverage sheet](sahulat-coverage-sheet.md).

**Owner:** Hira Baig, Product Manager · **Date:** 2026-09-07 · **Learning cards added:** 2026-09-29 · **Decision context:** D8, Gate 6 PIVOT

## What it is for

D8 pivots Sahulat from wallet-funded bill pay to agent-assisted bill pay. The customer hands cash to the agent, the wallet remains the record and receipt, and the next pass tests whether the agent can initiate the payment without taking the customer's PIN.

This map applies R6's lesson: an assumption named as risky is not retired by a plausible story. Each assumption needs linked evidence, and evidence that shows the opposite is not counted as support.

Sources: [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md).

## Run it when

- A one-pager or PRD is drafted and the team can list its beliefs but not its evidence.
- Before Gate 1 of the second DISCOVER pass, after D8 has selected agent-assisted bill pay.
- Before an experiment is proposed, so the team can say which assumption it could falsify.

**Skip it when:** the idea is a compliance mandate or a fix for something broken. This pivot is neither, so the map is required.

## Inputs you need first

- The pivot recorded by D8 on 2026-08-28.
- The agent behavior observed in N45 and CN13.
- The paper-slip evidence in N60 and E7.
- The PIN-sharing evidence in CN13 and E6.
- The proposed commission in N39, the float evidence in N52, and the per-bill arithmetic in CN26.
- The licence dependency owned by Amna Rasheed, recorded as AS-7.
- The [Sahulat journey data sheet](sahulat-journey.md) and [Sahulat coverage sheet](sahulat-coverage-sheet.md).

## The worksheet

### 1. Inventory

| ID | It must be true that | Type (D / F / V) | Importance (1 to 3) | Evidence (1 to 3) | Priority = importance minus evidence | Grid cell |
|---|---|---|---:|---:|---:|---|
| AS-1 | For agent-assisted bill pay to work, agents keep assisting if they receive the proposed PKR 5 commission per bill. | D | 3 | 1, the PKR 5 line is proposed, and the observed informal PKR 20 charge is not evidence that the proposed commission is accepted (N39, CN17, E8). | 3 - 1 = 2 | Test now |
| AS-2 | Customers accept an SMS reference as proof without also requiring a paper slip. | D | 2 | 1, five of six pilot agent debriefs reported paper-slip requests, and an agent said customers show the stamped chit rather than the phone (N60, E7). | 2 - 1 = 1 | Test next |
| AS-3 | Customers confirm an agent-keyed payment on their own phone without handing over their PIN. | D | 3 | 1, 24 of 41 observed assisted payments involved the agent being told or entering the customer's PIN, and E6 records the same behavior (CN13, E6). | 3 - 1 = 2 | Test now |
| AS-4 | The agent app can show a confirmation for a payment keyed into a customer's wallet within Rel-2. | F | 2 | 1, the confirmation is a pass-2 hypothesis and no agent-app confirmation has been observed (AS-4, D9). | 2 - 1 = 1 | Test next |
| AS-5 | Agents hold enough float on bill-peak days for same-visit assisted bill pay. | F | 2 | 1, 38 of 600 pilot agents reported a float stock-out on a bill-peak day (N52). | 2 - 1 = 1 | Test next |
| AS-6 | PKR 7 net per bill covers the PKR 5 commission, the PKR 1.2 SMS and the USSD sessions at the October tariff. | V | 3 | 2, the inputs and arithmetic are documented, but the October tariff is quoted and the contribution is not yet an observed operating result (N32, N39, N40, N62, CN25, CN26). | 3 - 2 = 1 | Test next |
| AS-7 | The licence permits an agent to initiate a payment from a customer's wallet with the customer's confirmation. | V | 3 | 1, the answer is Open with Amna Rasheed and no linked licence confirmation for this pivot is recorded (AS-7, DEP-3). | 3 - 1 = 2 | Test now |

The evidence scores are deliberately conservative. CN13 and E6 show PIN sharing, so they do not support AS-3. N60 and E7 show demand for paper proof, so they do not support AS-2. N52 shows a float failure, so it does not support AS-5.

### 2. Grid

| | Evidence 1 (none) | Evidence 2 (weak) | Evidence 3 (strong) |
|---|---|---|---|
| Importance 3 | Test now | Test next | Watch |
| Importance 2 | Test next | Watch | Accept |
| Importance 1 | Accept | Accept | Accept |

| Assumption | Calculation | Resulting cell |
|---|---:|---|
| AS-1 | Importance 3 - evidence 1 = 2 | Test now |
| AS-2 | Importance 2 - evidence 1 = 1 | Test next |
| AS-3 | Importance 3 - evidence 1 = 2 | Test now |
| AS-4 | Importance 2 - evidence 1 = 1 | Test next |
| AS-5 | Importance 2 - evidence 1 = 1 | Test next |
| AS-6 | Importance 3 - evidence 2 = 1 | Test next |
| AS-7 | Importance 3 - evidence 1 = 2 | Test now |

**Decision rule:** test in descending priority. The test-now group is AS-1, AS-3 and AS-7. AS-1, AS-3 and AS-7 tie at priority 2, so desirability is tested before feasibility and viability. AS-2, AS-4, AS-5 and AS-6 follow at priority 1. Nothing in Test now waits for a sprint.

### 3. Test card

#### Test card, AS-1

| Field | Entry |
|---|---|
| Assumption ID | AS-1 |
| We believe that | Agents keep assisting if they receive the proposed PKR 5 commission per bill. |
| To test it we will | Show agents the proposed commission and ask them to commit to a real assisted-payment trial, then compare the commitment with their recent assisted-payment behavior. Use the pass-2 agent evidence from INT-015 to INT-020 and the agent survey result. |
| We will measure | The number of agents who commit to the trial, the number who already performed an assisted payment in the last seven days, and the proposed commission response. Sources: CN14, CN16, CN22 and N39. |
| We are right if | Open: Hira Baig owns the pass criterion before the test runs. The threshold must distinguish acceptance of the PKR 5 line from an informal PKR 20 charge. |
| Cost and duration | Open: Hira Baig owns the test cost and duration with Tariq Sohail. |

#### Test card, AS-3

| Field | Entry |
|---|---|
| Assumption ID | AS-3 |
| We believe that | Customers confirm an agent-keyed payment on their own phone without handing over their PIN. |
| To test it we will | Run an agent-assisted payment prototype in which the agent keys the payment, the customer confirms on the customer's phone, and the customer is instructed not to disclose the PIN. Observe the interaction and record any request to share or enter the PIN. |
| We will measure | Assisted payments completed with no PIN disclosure, compared with assisted payments involving PIN disclosure. Source baseline: 24 of 41 observed assisted payments involved the agent being told or entering the PIN (CN13), with the specific note E6. |
| We are right if | Open: Hira Baig owns the pass criterion before the test runs. The test must require no PIN disclosure for a payment to count as a pass. |
| Cost and duration | Open: Hira Baig owns the test cost and duration with Zainab Qureshi and Tariq Sohail. |

#### Test card, AS-7

| Field | Entry |
|---|---|
| Assumption ID | AS-7 |
| We believe that | The licence permits an agent to initiate a payment from a customer's wallet with the customer's confirmation. |
| To test it we will | Ask Amna Rasheed to review the proposed agent-assisted flow against the licence's permitted activities and record whether the customer's confirmation changes the answer. |
| We will measure | A written compliance decision that states whether the agent-initiated, customer-confirmed payment is permitted, and any notification or control required. Source: AS-7 and DEP-3. |
| We are right if | The written answer confirms that the flow is permitted with the customer's confirmation and names any required control. Open: Amna Rasheed owns the answer. |
| Cost and duration | Open: Amna Rasheed owns the review timing and any filing requirement. |

#### Test card, follow-on assumptions

| Assumption ID | Entry |
|---|---|
| AS-2 | Test next with the proof format. The available evidence is mixed toward a paper slip: N60 and E7. The test should compare an SMS reference with the stamped counter slip described in SQ2. Open: Hira Baig owns the threshold before the test runs. |
| AS-4 | Test next with an agent-app confirmation prototype. No evidence yet shows that the app can confirm an agent-keyed payment. Open: Zainab Qureshi owns the technical test. |
| AS-5 | Test next on bill-peak days. The starting evidence is 38 of 600 pilot agents reporting a stock-out on 2026-07-08, N52. Open: Tariq Sohail owns the float test and pass criterion. |
| AS-6 | Test next with the contribution arithmetic and the October tariff. The current arithmetic is recorded in CN26 and is not a pass. Open: Bilal Hasan owns the commission schedule v8 and the viability decision. |

### 4. Learning card

#### Learning card, SQ2 and AS-2

| Field | Entry |
|---|---|
| We believed that | Customers would leave with proof they accept, specifically the SMS reference plus a stamped counter slip, as tested by SQ2. |
| We observed | The design sprint grid recorded SQ2 as 3 positive, 1 negative and 1 neutral (CN19). Earlier evidence also recorded paper-slip requests in 5 of 6 pilot agent debriefs (N60), and an agent saying customers show the stamped chit rather than the phone (E7). |
| From that we learned | SQ2 is unclear: the sprint was not decisive, and the surrounding evidence shows that SMS proof alone may not replace a paper slip. |
| Therefore we will | Rewrite AS-2 as an unresolved proof-format assumption. The comparison test set for 2026-09-24 and 2026-09-25 by D9 (SMS reference against the stamped counter slip) has not run as of this card's date, 2026-09-29. Open: Hira Baig owns rescheduling it. The evidence score remains 1 until that test produces linked evidence. |

#### Learning card, AS-6

| Field | Entry |
|---|---|
| We believed that | PKR 7 net per bill would cover the proposed PKR 5 commission, the PKR 1.2 SMS and two USSD sessions at the October tariff. |
| We observed | CN26 records the arithmetic: PKR 7 - PKR 5 - PKR 1.2 - (2 x PKR 0.65) = PKR 7 - PKR 5 - PKR 1.2 - PKR 1.3 = PKR -0.5 a bill. At today's PKR 0.40 tariff, the same arithmetic is PKR 7 - PKR 5 - PKR 1.2 - (2 x PKR 0.40) = PKR 0.0 a bill. |
| From that we learned | AS-6 fails at the October tariff by PKR 0.5 a bill, and the proposed commission does not leave a positive contribution at that tariff. |
| Therefore we will | Rewrite AS-6 as failed evidence, route the commission and pricing decision to Bilal Hasan, and keep the evidence score at 2 because the result is documented arithmetic rather than an observed operating result. The business model does not close at the proposed commission and October tariff. |

## Reading the result

A test moves the evidence score, never the importance score. R6 is not rescued by lowering its importance: the earlier hypothesis failed because the team had too little evidence for the balance-keeping behavior and treated a labelled assumption as a design foundation.

The pass-2 map is not green:

- **Test now:** AS-1, AS-3 and AS-7, each with priority 2.
- **Test next:** AS-2, AS-4, AS-5 and AS-6, each with priority 1.
- **Learning recorded:** SQ2 remains unclear, and AS-6 fails by PKR 0.5 a bill at the October tariff.
- **Open ownership:** Amna Rasheed owns the licence answer for AS-7, Bilal Hasan owns the commission schedule v8 due 2026-09-30, and Hira Baig owns the pass criteria that are not yet fixed.

The failed AS-6 arithmetic does not change importance. It changes the evidence and routes a viability decision. The observed PIN sharing does not make AS-3 safe; it makes AS-3 urgent.

## ILLUSTRATIVE example

This worksheet has no separate unrelated example. The Sahulat rows above are the filled example, and all people, companies, dates, amounts, identifiers and findings are fictional and ILLUSTRATIVE.

## The trap

Evidence inflation would repeat R6. A proposed PKR 5 commission is not evidence that agents will accept it. Agents performing assisted payments is not evidence that they will do so for PKR 5. Customers receiving an SMS is not evidence that they will accept it as proof without a paper slip. A flow that currently involves PIN sharing is not evidence that customers will confirm safely on their own phone.

The mechanical rule is applied here: a score of 2 or 3 needs a linked note with a date or a linked data row. Where the linked evidence shows the opposite of the assumption, it remains evidence score 1 for that assumption. CN13 and E6 therefore keep AS-3 in Test now, while N60 and E7 keep AS-2 in Test next.

## Feeds

- [templates/definition/assumptions-register.md](../templates/definition/assumptions-register.md): AS-1 to AS-7 enter the register; AS-6's failed learning card enters the busted section.
- [templates/discovery/opportunity-solution-tree.md](../templates/discovery/opportunity-solution-tree.md): the agent-assisted solution carries AS-1 to AS-7 and their next tests.
- [templates/operate/experiment-brief.md](../templates/operate/experiment-brief.md): AS-1, AS-3 and AS-7 become experiment briefs if their tests outgrow the cards.
- Gate 1 of the second DISCOVER pass, after the tests have linked results.
- Method background: [knowledge/torres-continuous-discovery.md](../knowledge/torres-continuous-discovery.md).
- Source data: [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md).
