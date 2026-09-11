# Ansoff Matrix: Sahulat Bill Pay, candidate moves

Fills [frameworks/strategy/ansoff-matrix.md](../frameworks/strategy/ansoff-matrix.md). Everything here is ILLUSTRATIVE: Sahulat, its people, companies, customers, figures and decisions are fictional, and the figures are taken from the [Sahulat journey data sheet](sahulat-journey.md) and the [coverage sheet](sahulat-coverage-sheet.md).

**Owner:** Hira Baig, Product Manager · **Date:** 2026-03-02 · **Stage:** PLANNING

## What it is for

This matrix places four candidate moves around the Sahulat wallet:

- The cashback promotion is market penetration, because it uses the existing wallet for existing wallet holders. D1 rejected it in favour of bill pay.
- Bill pay for existing wallet holders is product development, because bill pay had not shipped and been measured.
- App-first bill pay is market development, because it takes the bill-pay proposition to smartphone-first customers rather than the existing USSD and agent-led audience.
- Merchant QR and bill-linked credit are diversification, because both the product and the market are new to Sahulat's current bill-pay proposition.

The current position is established by the [Sahulat journey](sahulat-journey.md): 1,900,000 registered wallets, 410,000 30-day active wallets, 61 percent of cash-ins fully cashed out within 48 hours, and a median wallet balance of PKR 340. The matrix therefore treats balance retention as an assumption to test, not as a reason to fund a cashback promotion.

## Run it when

- The roadmap mixes the cashback promotion, bill pay, app-first bill pay, and merchant QR or bill-linked credit as if they carry the same risk.
- A new audience is described as the same market because the underlying wallet is unchanged.
- A new capability is described as penetration because it uses an existing wallet.
- The vision's non-goals need to control capacity allocation.

The matrix is being run beside the vision on 2026-03-02. It does not reopen the vision's non-goals. It records the revisit conditions that would be needed before those non-goals could be reconsidered.

## Inputs you need first

- Candidate moves from the planning discussion.
- Evidence for the current wallet and its balance behaviour from [sahulat-journey.md](sahulat-journey.md).
- The bill-pay demand signal, including 412 agent-helpline calls in the four weeks to 2026-01-09 and the 14 research sessions, from [sahulat-journey.md](sahulat-journey.md).
- The vision's non-goals and revisit conditions, extended in [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md).
- Capacity: 9 engineers in the company, with 4 engineers assigned to the bill-pay squad.

## The worksheet

<!-- "New market" means a user group whose buyer, buying process, or job differs from the one served today. "New product" means a capability not shipped and measured. Risk band by cell: penetration 1, product development 2, market development 3, diversification 4. -->

| Move | Product: existing or new (why) | Market: existing or new (why) | Cell | Risk band 1 to 4 | What we know about the market (evidence) | What we know about the product (evidence) | Evidence required before funding | Share of period capacity |
|---|---|---|---|---|---|---|---|---|
| Cashback promotion for wallet holders to keep a balance | Existing, the wallet and cash-in experience already exist | Existing, current Sahulat wallet holders | Market penetration | 1 | 61 percent of cash-ins were fully cashed out within 48 hours, and the median wallet balance was PKR 340. This shows the balance-retention problem, not demand for cashback. D1 rejected the move. | The wallet and cash-in already exist, but the promotion's effect on held balances is not measured | A measured baseline and a target. D1 rejected the move before funding, using the 61 percent pass-through baseline and PKR 340 median wallet balance | None, rejected at D1 |
| Bill pay for existing wallet holders | New, bill pay had not shipped and been measured | Existing, current Sahulat wallet holders who need to pay household bills | Product development | 2 | 412 agent-helpline calls asked about bill pay in the four weeks to 2026-01-09. Discovery included 14 sessions, with eight customers and six agents. | No bill-pay capability had shipped and been measured. The proposed product uses the existing wallet, agent network, USSD channel and BillBridge integration; the same lookup-and-pay flow is expected to extend to the app screen for wallet holders who already use it, which is a channel for the existing audience, not the smartphone-first acquisition move the next row addresses | Validated problem evidence from existing users, through interviews or tickets, and a prototype test. The 412 calls and 14 sessions provide the problem evidence. The prototype test remains the evidence bar for the next funding decision | Four engineers out of nine, 4 ÷ 9 of period capacity |
| App-first bill pay for smartphone-first customers | Existing for this classification, the bill-pay proposition is taken through the existing product to a different channel-led audience | New, smartphone-first customers are not the current USSD and agent-led audience | Market development | 3 | The smartphone app is a minority channel. The existing evidence does not establish five conversations with smartphone-first bill-pay customers, their named alternative, or a proven acquisition channel | Bill pay had not shipped and been measured, but the move is classified here because its defining change is the new market and channel strategy | Five or more conversations with the new group, one named alternative they use today, and a channel that can be proved to reach them. The vision's non-goal is no app-first strategy in this horizon, so this evidence bar is not opened during the period | None. The vision's non-goal is no app-first strategy; revisit only through the vision's stated revisit condition |
| Merchant QR and bill-linked credit | New, merchant QR and bill-linked credit have not shipped and been measured | New, merchants and credit users are outside the current wallet bill-pay market | Diversification | 4 | No market evidence has been gathered for merchant QR or bill-linked credit in this planning pass | No product evidence exists for either capability | A separate [business case](../templates/planning/business-case.md) with its own Gate 1, and a beachhead defined per [Crossing the Chasm](../knowledge/crossing-the-chasm.md). The vision's non-goals are no merchant acquiring and no credit in this horizon, so neither move is funded | None. The vision's non-goals are no merchant acquiring and no credit; revisit only through the vision's stated revisit conditions |

**Capacity arithmetic.**

- Bill-pay squad share: 4 engineers ÷ 9 engineers = 4/9 of period capacity.
- Cashback promotion: no capacity, because D1 rejected it.
- App-first bill pay: no capacity, because the vision says no app-first strategy in this horizon.
- Merchant QR: no capacity, because the vision says no merchant acquiring in this horizon.
- Bill-linked credit: no capacity, because the vision says no credit in this horizon.

The remaining capacity is not silently assigned to the rejected or non-goal moves. The bill-pay allocation is the funded planning choice, with the four-engineer squad drawn from the nine-engineer company capacity recorded in the [Sahulat journey](sahulat-journey.md).

**Evidence bars by band.**

- **Band 1:** a measured baseline and a target. The cashback promotion did not pass this bar as a funding proposal and was rejected at D1.
- **Band 2:** validated problem evidence from existing users, through interviews or tickets, and a prototype test. Bill pay has the 412-call and 14-session problem evidence. The prototype test remains required before further funding.
- **Band 3:** five or more conversations with the new group, one named alternative they use today, and a channel that can be proved to reach them. App-first bill pay is not funded because the vision excludes an app-first strategy in this horizon.
- **Band 4:** a separate [business case](../templates/planning/business-case.md) with its own Gate 1, and a beachhead defined per [Crossing the Chasm](../knowledge/crossing-the-chasm.md). Merchant QR and bill-linked credit are not funded because the vision excludes merchant acquiring and credit in this horizon.

**Decision rule.** No move is funded above its evidence bar. The current funded move is bill pay for existing wallet holders, at band 2, with four engineers from the nine-engineer company. The app-first, merchant QR and bill-linked credit moves receive no capacity. No bank rail and no scheme interoperability work are added to this horizon.

## Reading the result

- **Most capacity is in the band 2 bill-pay move.** This is appropriate for a product that has a validated problem signal but has not yet measured the new capability. The four-engineer allocation is 4 ÷ 9 of period capacity.
- **The cashback proposal is not treated as a free band 1 win.** It is penetration by cell, but D1 rejected it after the 61 percent pass-through baseline and PKR 340 median wallet balance showed that the balance-retention assumption was not established.
- **App-first bill pay is not penetration.** Its channel-led audience is a new market for the current Sahulat audience, so it is band 3 even though the wallet remains the same.
- **Merchant QR and bill-linked credit remain outside the period.** They are separate diversification bets, not extensions of bill pay. Each needs its own business case and beachhead before funding.
- **The vision controls the capacity exceptions.** No credit, no balance-dependent design ahead of a DISCOVER pass finding three of eight or more customers holding a balance, no merchant acquiring, no app-first strategy, no bank rail, and no scheme interoperability work are funded in this horizon.

## ILLUSTRATIVE example

This is the same ILLUSTRATIVE Sahulat placement recapped compactly.

| Move | Cell | Band | Capacity |
|---|---|---|---|
| Cashback promotion for wallet holders | Market penetration | 1 | None, rejected at D1 |
| Bill pay for existing wallet holders | Product development | 2 | 4 engineers of 9, 4/9 of period capacity |
| App-first bill pay for smartphone-first customers | Market development | 3 | None, vision non-goal |
| Merchant QR and bill-linked credit | Diversification | 4 | None, vision non-goals |

Reading: the only funded move is bill pay, at band 2, with four of the company's nine engineers. The cashback promotion looks like band 1 but carries no capacity because D1 rejected it on the 61 percent pass-through baseline and PKR 340 median wallet balance. App-first bill pay, merchant QR and bill-linked credit all sit above the funded band and receive no capacity while the vision's non-goals stand.

## The trap

The trap is calling every move penetration because Sahulat already has a wallet.

The cashback promotion is penetration, but D1 rejected it because the available evidence showed 61 percent of cash-ins fully cashed out within 48 hours and a median wallet balance of PKR 340. Bill pay is product development because Sahulat had not shipped and measured bill pay. App-first bill pay is market development because the smartphone-first audience and channel-led acquisition path differ from the existing USSD and agent-led audience. Merchant QR and bill-linked credit are diversification because both the product and the market are new.

The code or account shell does not set the cell. The user's job, buying or access process, and the capability being offered set the cell.

## Feeds

- [Sahulat vision](sahulat-vision.md): the destination, non-goals and revisit conditions.
- [Sahulat journey](sahulat-journey.md): the canonical wallet, research, capacity and decision data.
- [Sahulat coverage sheet](sahulat-coverage-sheet.md): the 2026-03-02 placement and the coverage-file context.
- [templates/planning/product-strategy.md](../templates/planning/product-strategy.md): section 2, where to play and the risk band per bet.
- [templates/planning/growth-plan.md](../templates/planning/growth-plan.md): section 2, the next growth bet, and section 4, the cheapest experiment.
- [templates/planning/roadmap.md](../templates/planning/roadmap.md): Next and Later carry the band; band 4 moves remain parked until a business case exists.
- [templates/planning/business-case.md](../templates/planning/business-case.md): required for any band 4 move.
- PLANNING track.
- Method background: [Crossing the Chasm](../knowledge/crossing-the-chasm.md) for the beachhead rule; no Ansoff card exists. The matrix itself is based on the ideas of H. Igor Ansoff, from "Strategies for Diversification," Harvard Business Review (1957).
