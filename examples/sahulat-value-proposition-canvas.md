# Sahulat Value Proposition Canvas: Rafiq, pass 2

Fills [frameworks/strategy/value-proposition-canvas.md](../frameworks/strategy/value-proposition-canvas.md). Everything here is invented and every number is ILLUSTRATIVE: Sahulat, its people, agents, customers, billers, bank, aggregator and telco are fiction, and the values below were chosen so that this canvas agrees with [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md), not to describe any real wallet or market.

**Owner:** Hira Baig, Product Manager, the only PM · **Date:** 2026-09-22 · **Pass:** 2, DISCOVER · **Segment:** P2 Rafiq, the corner-shop agent

## What it is for

This canvas tests the proposed Sahulat value proposition for Rafiq, the agent who already performs bill payments for customers. It separates Rafiq's jobs, pains and gains from the proposed value map, then checks whether each rank-3 item has a linked response.

The profile uses the pass-1 agent sessions INT-009 to INT-014 and the pass-2 evidence from INT-015 to INT-020, the design sprint and SV-1. The value map tests the agent-initiated flow from D9, a stamped counter slip, the proposed PKR 5 line from N39, and the float hotline that followed N52.

The result is fit on paper only. The proposed PKR 5 line is below the PKR 30 to 50 shop fee reported in N21 and below the PKR 20 informal charge reported by 2 of 6 agents in CN17:

- PKR 5 is PKR 25 to 45 below the PKR 30 to 50 shop fee: PKR 30 to 50 minus PKR 5 = PKR 25 to 45.
- PKR 5 is PKR 15 below the PKR 20 informal charge: PKR 20 minus PKR 5 = PKR 15.
- The comparison shows a pricing hypothesis, not willingness to accept the line. It does not establish product-market fit.

## Run it when

- A candidate assisted-payment flow exists and needs testing against Rafiq's actual counter work before more product work is committed.
- The pass-1 evidence shows agents already perform bill payments, while the pass-2 work tests whether a supported flow changes the unpaid time, proof and float problems.
- The proposed PKR 5 commission line needs checking against the existing PKR 30 to 50 shop fee and the PKR 20 informal charge.
- The team needs to distinguish observed assisted payments from evidence that agents will use or pay for the proposed Sahulat flow.

**Skip it when:** no agent job map or interview evidence exists. That condition is not present here: INT-009 to INT-014, INT-015 to INT-020, N45, N52, N60, CN16, CN17 and CN22 provide evidence for the profile. The evidence is still not a product-market-fit result.

## Inputs you need first

- Agent evidence from INT-009 to INT-014, including E3 and N21.
- Pass-2 agent evidence from INT-015 to INT-020, including E6, E7, E8 and CN16 to CN17.
- Observed assisted-payment behavior: N45 and CN13.
- Agent survey evidence: CN20 to CN24, especially CN22 and OUT-5.
- The candidate flow recorded in D9: an agent initiates payment into the customer's own wallet and the customer confirms on her own phone.
- The proposed PKR 5 agent commission from N39 and the float hotline response to N52.
- The design sprint result in CN19, which is directional prototype evidence, not evidence of sustained product use.

## The worksheet

### Part 1: customer profile

| # | Category (job / pain / gain) | Sub-type (functional / social / emotional; leave blank for pains and gains) | What it is, in the customer's words | Rank 1 to 3 | Evidence |
|---|---|---|---|---|---|
| 1 | Job | functional | Do the customer's bill at my counter while she is there, instead of sending her to the shop across the road. | 3 | E3: "Six or seven people a day ask me if I can do their bill." N45 records 41 of 53 observed bill payments performed by the agent. CN16 records 11, 6, 9, 14, 2 and 8 assisted payments in the last seven days for INT-015 to INT-020. CN22 records 426 of 734 survey respondents reporting at least one assisted bill payment in the last seven days. |
| 2 | Job | social | Be the shopkeeper customers can rely on for a bill question and a completed payment, rather than the person who has to refer them elsewhere. | 2 | E3: Rafiq sends customers to the shop across the road and the other shop keeps the fifty. T3 records that agents field bill questions daily and refer customers to a shop. N60 records customers asking for a paper slip in 5 of 6 pilot agent debriefs. |
| 3 | Pain | n/a | I spend time doing a customer's bill and nobody pays me for it otherwise. | 3 | OUT-5 is "minimize the unpaid time spent on a customer's bill." E8: "I take twenty extra for doing the bill. Nobody pays me for it otherwise." CN17 records 2 of 6 agents adding PKR 20 each time. The proposed line is PKR 5, so the open question is whether it changes the unpaid-time pain. |
| 4 | Pain | n/a | The float can run out on a bill-peak day, so I cannot complete the same-visit payment. | 3 | N52 records 38 of 600 pilot agents reporting a float stock-out on 2026-07-08. R1 names float running out on bill-peak days as a risk. N57 records that the 5th to the 10th of the month carry 44 percent of monthly bill payments. |
| 5 | Gain | n/a | I get a clear, official amount for doing the bill, instead of relying on an informal charge. | 3 | E8 records the PKR 20 informal charge. CN17 records 2 of 6 agents using it. N39 proposes PKR 5 per bill. CN22 records a median of 9 assisted payments per assisting agent in the last seven days, but does not show that any agent would accept PKR 5 from Sahulat. |
| 6 | Gain | n/a | The customer leaves with proof she accepts, so she does not come back asking whether the bill went through. | 3 | E7: "I write the SMS number on a chit and stamp it. They show the chit, not the phone." N60 records paper-slip requests in 5 of 6 pilot agent debriefs. CN13 records that the customer asked for a paper slip in 17 of the 41 assisted payments. |

### Part 2: value map

| # | Category (product/service / pain reliever / gain creator) | What we offer | Which Part 1 item it addresses | Evidence it works, not a feature description |
|---|---|---|---|---|
| 1 | Product/service | An agent-initiated bill-pay flow in which Rafiq starts the payment on the agent flow, while the customer confirms on her own phone and the payment enters the customer's own wallet. The customer does not share her PIN. | [item #1], [item #2] | N45 shows the current agent-assisted behavior: 41 of 53 observed payments were performed by the agent. E6 shows the current PIN-sharing problem, while D9 and SQ1 define the proposed customer-confirmed alternative. CN19 records SQ1 with 4 positive and 1 negative response in the sprint, but this was a prototype response, not sustained product usage. |
| 2 | Pain reliever | A stamped counter slip paired with the Sahulat payment reference, plus the float hotline for agents when float is at risk on bill-peak days. | [item #4], [item #6] | CN13 records 17 paper-slip requests among 41 assisted payments, and N60 records paper-slip requests in 5 of 6 pilot agent debriefs, so the slip responds to observed proof behavior. N52 records 38 of 600 pilot agents reporting a float stock-out, so the hotline responds to a named operational failure. Neither observation proves that the proposed slip or hotline resolves the pain. |
| 3 | Gain creator | A proposed PKR 5 agent commission per assisted bill, recorded as the post-pivot line in N39. | [item #3], [item #5] | The proposed amount can be compared with the current evidence: PKR 5 is PKR 25 to 45 below the PKR 30 to 50 shop fee in N21, and PKR 15 below the PKR 20 informal charge reported by 2 of 6 agents in CN17. E8 confirms that payment for the work matters. These comparisons show the value proposition is plausible to test, not that agents accept it. |

### Part 3: the fit test

| Part 1 item (rank 3 only) | Linked value map item | Fit status: on paper / evidenced / none |
|---|---|---|
| Item 1, do the customer's bill at my counter | Item 1, agent-initiated customer-confirmed flow | on paper |
| Item 3, avoid unpaid time | Item 3, proposed PKR 5 commission | on paper |
| Item 4, avoid a float stock-out | Item 2, float hotline | on paper |
| Item 5, receive a clear official amount | Item 3, proposed PKR 5 commission | on paper |
| Item 6, give the customer accepted proof | Item 2, stamped counter slip and payment reference | on paper |

**Decision rule:** there are 5 rank-3 rows:

1. Item 1, job.
2. Item 3, pain.
3. Item 4, pain.
4. Item 5, gain.
5. Item 6, gain.

All 5 have a linked value-map row. The map therefore addresses the profile on paper, which supports problem-solution fit at the hypothesis level.

The arithmetic around the commission does not support a product-market-fit claim:

- Existing shop fee range: PKR 30 to 50.
- Proposed Sahulat line: PKR 5.
- Difference: PKR 30 to 50 minus PKR 5 = PKR 25 to 45.
- Informal charge reported by 2 of 6 agents: PKR 20.
- Difference: PKR 20 minus PKR 5 = PKR 15.
- SV-1 assisted-payment evidence: 426 of 734 respondents, 58 percent, reported at least one assisted bill payment in the last seven days, and the median was 9 assisted payments per assisting agent in those seven days. This shows the behavior exists, not that the proposed flow or PKR 5 line caused it.

The fit level is therefore **problem-solution fit on paper only**. Product-market fit is not claimed. Business-model fit is not claimed. The commission schedule remains open with Bilal Hasan by 2026-09-30, and the contribution arithmetic belongs in the business model canvas.

## Reading the result

- **Every rank-3 job, pain and gain has a linked row.** The proposed flow, stamped slip, float hotline and PKR 5 line cover the profile on paper.
- **No link is evidenced as sustained product behavior.** CN19 gives a directional sprint result for SQ1, while N45 and CN22 describe existing assisted behavior rather than use of the proposed product.
- **The commission comparison is a warning, not a win.** PKR 5 is below both the PKR 30 to 50 shop fee and the PKR 20 informal charge. The lower amount could be attractive if it is reliable and official, but that remains an assumption.
- **The proof problem is observed.** N60 and CN13 support the need for a stamped slip. E7 also shows that Rafiq currently writes the SMS number on a chit and stamps it. The canvas still does not show that customers accept the proposed slip and reference as sufficient proof.
- **The float problem is observed.** N52 supports a hotline response, but the canvas does not yet show that the hotline prevents a stock-out or makes Rafiq willing to use the new flow.
- **Decision:** carry the five rank-3 links into the next test. Test whether Rafiq performs the agent-initiated flow, whether the customer confirms without sharing a PIN, whether the stamped slip is accepted, and whether the PKR 5 line changes the unpaid-time objection. Do not describe the result as product-market fit.

## ILLUSTRATIVE example

This Sahulat worksheet is itself the ILLUSTRATIVE example of the value proposition canvas method. Rank-3 item 1 (do the customer's bill at my counter) links to value-map item 1 (the agent-initiated, customer-confirmed flow) on the strength of N45's 41-of-53 observed agent-performed payments, but that link is marked on paper only because N45 describes existing assisted behavior, not use of the proposed flow. Rank-3 item 4 (avoid a float stock-out) links only to value-map item 2 (the float hotline), evidenced by N52's 38-of-600 stock-out reports, not to item 1, because an agent-initiated payment flow has no mechanism of its own for keeping float stocked. The fit test in Part 3 carries every rank-3 link forward as on paper, not evidenced, which is the expected state for a DISCOVER-pass canvas.

## The trap

The trap is treating existing agent-assisted payments as proof that Rafiq wants this particular Sahulat flow. N45 records 41 of 53 payments performed by an agent, and CN22 records 426 of 734 respondents reporting an assisted payment in the last seven days. Neither figure proves that the agent will use an agent-initiated flow with customer confirmation, accept a stamped slip as the proof format, or prefer PKR 5 to the current PKR 30 to 50 shop fee or PKR 20 informal charge.

A second trap is converting E8 into a pricing conclusion. E8 shows that one agent takes PKR 20 because "nobody pays me for it otherwise." It does not show that the same agent would replace PKR 20 with PKR 5, or that the other 4 of 6 agents would accept PKR 5.

A third trap is treating the sprint grid as usage evidence. CN19 records 4 positive and 1 negative for SQ1, and 3 positive, 1 negative and 1 neutral for SQ2. Those responses support further testing. They do not establish product-market fit.

## Feeds

- [sahulat-journey.md](sahulat-journey.md): canonical Sahulat data sheet, identifiers, D8 pivot and N21, N39, N45, N52 and N60.
- [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md): pass-2 evidence, including E6 to E8, CN13, CN16 to CN17, CN19, CN22 and OUT-5.
- [../frameworks/strategy/business-model-canvas.md](../frameworks/strategy/business-model-canvas.md): the proposed PKR 5 commission and the contribution check, ahead of commission schedule v8.
- [../frameworks/discovery/assumption-mapping.md](../frameworks/discovery/assumption-mapping.md): AS-1, AS-2, AS-3, AS-5 and AS-6, which remain hypotheses after this canvas.
- [../frameworks/discovery/design-sprint-runbook.md](../frameworks/discovery/design-sprint-runbook.md): SQ1 and SQ2, including the distinction between prototype response and product usage.
- Method: the value proposition canvas ideas of Alexander Osterwalder, Yves Pigneur, Gregory Bernarda and Alan Smith, from *Value Proposition Design* (2014), applied in the repository's own words.
