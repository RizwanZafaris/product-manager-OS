# Sahulat Business Model Canvas

Fills [frameworks/strategy/business-model-canvas.md](../frameworks/strategy/business-model-canvas.md). Everything here is invented: Sahulat, its customers, agents, billers, partners and people are fictional, and every number is ILLUSTRATIVE, taken from the [Sahulat journey data sheet](sahulat-journey.md) or its [coverage sheet](sahulat-coverage-sheet.md).

**Owner:** Hira Baig, Product Manager · **Date:** 2026-09-24 · **Stage:** PLANNING · **Status:** Check A fails; route to commission schedule v8 and the D4 fee question

## What it is for

This canvas models Sahulat's post-pivot business model for agent-assisted bill pay. A biller pays the fee through BillBridge, the agent assists the customer at the counter, Falak Telecom supplies the USSD session, and Sutlej Bank Limited is Sahulat's settlement bank.

The model does not close at the proposed PKR 5 agent commission and the October Falak Telecom tariff. The per-bill contribution is negative, so adding paying wallets would increase the loss unless the fee, commission, SMS cost or USSD cost changes.

Source data: [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md).

## Run it when

This canvas is being run before the pricing and business-case decisions for the assisted-payment pivot. It is specifically ahead of Bilal Hasan's commission schedule v8, due 2026-09-30.

The result routes to:

- Bilal Hasan's commission schedule v8, including the proposed PKR 5 assisted-payment commission.
- The D4 fee question, because the customer fee is PKR 0 per bill in Rel-1 and the model does not cover its variable cost at the October tariff.
- The fixed-cost question, which remains Open: Bilal Hasan owns the answer.

## Inputs you need first

- The post-pivot customer and agent evidence: 41 of 53 observed bill payments were performed by the agent, and the pass-2 agent evidence includes CN16, CN17 and E8.
- The quoted BillBridge economics: PKR 10 biller-paid fee, PKR 3 to BillBridge, and PKR 7 net to Sahulat per bill.
- The decided customer fee: PKR 0 per bill in Rel-1.
- The proposed agent commission: PKR 5 per bill, with v8 due 2026-09-30.
- The October Falak Telecom tariff: PKR 0.65 per USSD session, with 2 sessions per bill as the CN25 estimate.
- The SMS cost: PKR 1.2 per message.
- The observed paying-wallet volume and bill frequency: 31,200 bills from 24,600 wallets in four weeks, or 1.27 bills per wallet in that period.
- Fixed cost: Open: Bilal Hasan.

## The worksheet

### Part 1: the nine blocks

| Block | Prompt | Answer | Evidence | Confidence (high / med / low) |
|---|---|---|---|---|
| Customer segments | Who pays, who uses, and which segment we build for first | **Primary payer:** billers paying the PKR 10 fee through BillBridge, with PKR 7 net to Sahulat per bill. **Primary user:** agents assisting wallet customers at the counter. **End customer:** Sahulat wallet holders who hand cash to the agent and receive the wallet record and receipt. Build first for agent-assisted wallet bill pay, not balance-first bill pay. | BillBridge rate card, N31 and N32; D8; N45, 41 of 53 observed payments performed by the agent; N53, 24,600 wallets paid at least one bill; CN22, 426 of 734 survey respondents reported an assisted payment in the last seven days | med |
| Value propositions | What problem we solve per segment, in the customer's words | **Billers:** receive bill payments through BillBridge, with posting within 30 minutes, seven days a week. **Agents:** earn a proposed PKR 5 per assisted bill and can serve a bill request already arriving at the counter. **Wallet customers:** pay a bill in the agent visit, without a second trip, and receive an SMS reference as proof. Sahulat's value is the wallet record and receipt, not the funding source. | N36; N39; SAHULAT-S3; N20, median 70 minutes and PKR 60 transport per bill-paying trip; N21, PKR 30 to 50 bill-shop fee; N45; CN13; D8 | med |
| Channels | How each segment hears about us, buys, and gets onboarded | **Billers:** BillBridge integration and biller settlement flow. **Agents:** existing Sahulat agent network, agent app and agent operations, beginning with the 600-agent Lahore pilot cohort. **Wallet customers:** the agent counter, Sahulat USSD, SMS confirmation and the customer's existing wallet relationship. Onboarding is assisted at the counter, with the agent initiating or helping with the wallet payment and the customer receiving confirmation. | N5, 3,200 active agents; N6, 600 pilot agents in Lahore; N13, 412 bill-pay questions through the agent helpline; N45; N46; N53; CN13; CN28 | med |
| Customer relationships | Self-serve, assisted, or managed, per segment, and what that costs | **Billers:** managed integration and settlement relationship through BillBridge and Sutlej Bank Limited. **Agents:** assisted operational relationship through agent operations, the float top-up hotline and the agent helpline. **Wallet customers:** agent-assisted first, with USSD and SMS as the payment and proof surfaces. The variable service cost model includes PKR 5 proposed agent commission, PKR 1.2 SMS, and 2 USSD sessions at the October tariff. | N36; N39; N40; N46; N52, 38 of 600 pilot agents reported a float stock-out on 2026-07-08; N60, paper slips raised in 5 of 6 pilot agent debriefs; CN25 and CN26 | high |
| Revenue streams | What each segment pays for, by which value metric, how often | Biller-paid fee per bill: **PKR 10 per bill**, less **PKR 3 to BillBridge**, leaves **PKR 7 to Sahulat per bill**. The value metric is a bill successfully paid and posted, and the frequency is per bill. The customer fee is **PKR 0 per bill** in Rel-1, so the customer is not a payer in the current model. Agent commission is a cost, not revenue. | N31, quoted; N32, quoted; N33, decided; N36, quoted; CN26 | high |
| Key resources | The assets the model cannot run without: data, integrations, people, licences | BillBridge integration and biller catalogue; Sahulat wallet ledger and trust-account sub-ledger; USSD gateway and short code from Falak Telecom; settlement relationship with Sutlej Bank Limited; the agent network; bill-pay, support and reconciliation teams; the licence and compliance work needed for the assisted flow; bill and payment status data. | DEP-1; ADR-3; N5; N36; N46; Sutlej Bank Limited in the coverage sheet; DEP-3; CN13; CN28 | med |
| Key activities | The two or three things we must do well every week | 1. Process bill lookup, agent-assisted payment, BillBridge posting and SMS proof without duplicate or unexplained ledger outcomes. 2. Keep agents able to assist on bill-peak days through float monitoring, the hotline and commission operations. 3. Reconcile the trust-account flow and review contribution by bill and paying wallet before scaling. | N48, one unexplained break of PKR 12,300, explained within the day; N52; N57, 44 percent of monthly bill payments fall from the 5th to the 10th; N47; N49; CN26 and CN27 | high |
| Key partnerships | Who supplies or distributes something we will not build, and why they want to | **BillBridge:** biller aggregation and posting, in exchange for PKR 3 of the PKR 10 biller-paid fee. **Billers:** supply the bill obligation and pay the fee for a posted bill. **Falak Telecom:** supplies the USSD gateway and short code, charging the session tariff. **Sutlej Bank Limited:** provides Sahulat's settlement-bank path for T+1 settlement to billers. **Agents:** distribute and assist the service, with a proposed PKR 5 per bill. | N32; N36; N39; N40; N62; N66; DEP-1; Sutlej Bank Limited identifier in [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md) | med |
| Cost structure | The largest costs, fixed and variable, and which block drives each | **Variable per bill:** proposed agent commission PKR 5, SMS PKR 1.2, and 2 USSD sessions at PKR 0.65 each from 2026-10-01. Therefore, variable cost is PKR 5 + PKR 1.2 + (2 x PKR 0.65) = PKR 7.5 per bill. **Fixed cost:** Open: Bilal Hasan. Other operating costs include reconciliation, support, integration maintenance and agent operations, but no amount is present in the data sheets. The variable costs are driven by the agent relationship, customer proof, Falak Telecom and the assisted channel. | N39, target; N40, measured; N62, quoted; CN25, estimate; CN26, estimate; N48; N49; fixed cost Open: Bilal Hasan | med |

### Part 2: consistency check A, revenue covers cost

The calculation uses 1.27 bills per paying wallet in four weeks and the CN27 annualised estimate of about 16.5 bills per year.

| Line | Value | Source |
|---|---|---|
| Revenue per customer per year | PKR 7 per bill x 16.5 bills per year = **PKR 115.5 per paying wallet per year** | N32, quoted; CN27, estimate |
| Variable cost to serve per customer per year, inference, support, infrastructure | Commission: PKR 5 x 16.5 = PKR 82.5. SMS: PKR 1.2 x 16.5 = PKR 19.8. USSD: 2 sessions per bill x PKR 0.65 x 16.5 bills = PKR 21.45. Total: PKR 82.5 + PKR 19.8 + PKR 21.45 = **PKR 123.75 per paying wallet per year** | N39, target; N40, measured; N62, quoted; CN25, estimate; CN27, estimate |
| Contribution per customer, revenue minus cost to serve | **PKR 115.5 - PKR 123.75 = minus PKR 8.25 per paying wallet per year**. Per bill: **PKR 7 - PKR 5 - PKR 1.2 - (2 x PKR 0.65) = minus PKR 0.5** | CN26, estimate; CN27, estimate |
| Cost to acquire one customer | **Open: Bilal Hasan.** The launch SMS cost is a measured campaign cost, not a complete acquisition-cost measure: PKR 480,000 / 24,600 paying wallets = **PKR 19.5 per paying wallet** in the review cohort | N41, measured; N53, measured; CN27, estimate |
| Fixed cost per year, team and tooling | **Open: Bilal Hasan.** No fixed-cost amount is present in the data sheets | Coverage sheet, Open owner convention |
| Break-even customer count, fixed cost divided by contribution | **Not defined while contribution is negative.** The arithmetic would be fixed cost / minus PKR 8.25 per paying wallet per year, which cannot produce a positive break-even count. A fixed-cost amount is also Open: Bilal Hasan | CN27, estimate; fixed cost Open: Bilal Hasan |
| Customer count the strategy assumes at the end of the horizon | **No end-of-horizon strategy count is set.** The latest measured reference is 24,600 wallets that paid at least one bill in the four weeks to 2026-08-16, with 31,200 bills | N53, measured; N42, target and measured |

**Result:** Check A fails. The October tariff arithmetic is:

`PKR 7 - PKR 5 - PKR 1.2 - (2 x PKR 0.65) = PKR 7 - PKR 5 - PKR 1.2 - PKR 1.3 = minus PKR 0.5 per bill`

At the observed annualised frequency:

`minus PKR 0.5 x 16.5 bills = minus PKR 8.25 per paying wallet per year`

This routes to Bilal Hasan's commission schedule v8 due 2026-09-30 and reopens the D4 question about a PKR 0 customer fee. Fixed cost stays Open: Bilal Hasan.

### Part 3: consistency check B, proposition matches segment

| Segment (from the segment block) | Value proposition written for it | Channel that reaches it | Revenue stream it pays |
|---|---|---|---|
| Billers paying through BillBridge | A bill payment is posted through BillBridge within 30 minutes, seven days a week, with settlement to the biller T+1 through Sahulat's settlement bank | BillBridge integration and biller settlement relationship | PKR 10 biller-paid fee per bill, of which PKR 3 goes to BillBridge and PKR 7 goes to Sahulat |
| Agents | The agent can assist a customer's bill payment at the counter and is proposed to receive PKR 5 per assisted bill | Existing Sahulat agent network, agent app, agent operations and float top-up hotline | No agent revenue stream. The proposed PKR 5 per bill is an agent cost to Sahulat |
| Sahulat wallet customers | Pay a bill during the agent visit without a second trip and receive the wallet record and SMS reference as proof | Agent counter, Sahulat USSD and SMS confirmation | PKR 0 customer fee per bill in Rel-1, so the customer pays no fee in the current model |

**Result:** Check B passes. Each segment has one proposition, one channel and a stated payment relationship. The agent and customer rows are users or beneficiaries rather than current payers, while the biller row is the revenue-paying segment.

## Reading the result

- **Check A fails on contribution.** The proposed assisted-payment commission, SMS cost and October USSD tariff total PKR 7.5 per bill against PKR 7 net revenue. The model loses PKR 0.5 per bill and minus PKR 8.25 per paying wallet per year at the CN27 annualised frequency.
- **The next decision is not more acquisition.** The 24,600-wallet review cohort is already a measured reference, but more paying wallets at negative contribution increase the loss.
- **Route to v8.** Bilal Hasan owns commission schedule v8, due 2026-09-30. The schedule must answer whether the proposed PKR 5 commission changes.
- **Route to D4.** The customer fee remains PKR 0 per bill in Rel-1, but the negative contribution means that pricing decision must be revisited rather than treated as closed.
- **Fixed cost remains Open.** Bilal Hasan owns the fixed-cost amount and the resulting break-even calculation.
- **Check B passes.** The value propositions are assigned to billers, agents and wallet customers, and each row identifies its channel and payment relationship.

## ILLUSTRATIVE example

This is an ILLUSTRATIVE model for a fictional Sahulat agent-assisted bill-pay service. The fictional billers pay through BillBridge, agents assist customers, Falak Telecom supplies USSD sessions, and Sutlej Bank Limited supplies the settlement-bank path.

The model is deliberately shown as failing:

- Revenue per bill: PKR 7.
- Proposed agent commission: PKR 5.
- SMS cost: PKR 1.2.
- October USSD cost: 2 x PKR 0.65 = PKR 1.3.
- Contribution: PKR 7 - PKR 5 - PKR 1.2 - PKR 1.3 = minus PKR 0.5 per bill.
- Annualised contribution per paying wallet: minus PKR 0.5 x 16.5 bills = minus PKR 8.25.

The failure is useful because it prevents the team from presenting a complete-looking canvas as a viable model. The commission schedule and customer-fee decision must change, or the model does not close.

## The trap

The trap is writing "biller-paid fee" in the revenue block and stopping there. The value metric is one posted bill, so the cost of one assisted posted bill must be calculated beside it.

For Sahulat, the revenue block looks positive until the variable costs are placed on the same unit:

`PKR 7 revenue - PKR 5 commission - PKR 1.2 SMS - PKR 1.3 USSD = minus PKR 0.5`

The other trap is calling the PKR 480,000 launch SMS campaign the cost to acquire one customer without qualification. It produces a review-cohort proxy of:

`PKR 480,000 / 24,600 paying wallets = PKR 19.5 per paying wallet`

That is not a complete acquisition-cost measure. Open: Bilal Hasan owns the complete cost question.

## Feeds

- Bilal Hasan's commission schedule v8, due 2026-09-30: revisit the proposed PKR 5 agent commission.
- D4 fee question: revisit the decided PKR 0 customer fee in light of the minus PKR 0.5 per-bill contribution.
- Fixed-cost and break-even model: Open: Bilal Hasan.
- [Sahulat journey data sheet](sahulat-journey.md): canonical product, evidence and number source.
- [Sahulat coverage sheet](sahulat-coverage-sheet.md): post-pivot assumptions, CN25 to CN27 arithmetic and Sutlej Bank Limited identifier.
- [Business model canvas worksheet](../frameworks/strategy/business-model-canvas.md): completed framework and consistency rules, based on the ideas of Alexander Osterwalder and Yves Pigneur, in *Business Model Generation* (2010).

**Exit gate walk:** Hira Baig, Product Manager, reviewed the nine blocks and Check B on 2026-09-24. Check A is recorded as failed. Hira Baig routes the model to Bilal Hasan for commission schedule v8 by 2026-09-30, reopens the D4 fee question, and leaves fixed cost Open: Bilal Hasan.
