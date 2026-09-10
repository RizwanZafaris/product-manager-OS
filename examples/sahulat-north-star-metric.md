# North Star Sheet: Sahulat Bill Pay

Fills [templates/planning/north-star-metric.md](../templates/planning/north-star-metric.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, Hira Baig its only fictional product manager, and every number, name and date is ILLUSTRATIVE, drawn from the shared data sheet in [the Sahulat journey](sahulat-journey.md) rather than describing any real wallet or market. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager · **Date:** 2026-03-04 · **Status:** Signed 2026-03-04 by Faisal Mirza as sponsor; amended 2026-07-01 to fix the review date against the Gate 5 window, and again 2026-08-21 with the first review's readings; read again at Gate 6, 2026-08-28 (PIVOT, decision D8) · **Vision:** [the vision](sahulat-vision.md)

## 1. The metric

All figures in this table are ILLUSTRATIVE, drawn from the Sahulat data sheet.

| Field | Answer |
|---|---|
| North star metric | Wallets with at least one on-ledger payment in the trailing 30 days (M5), a monthly count |
| The customer value it expresses | Money a household put into Sahulat was still there when it was needed for something that stayed on the ledger, a bill among other things, rather than leaving the wallet the same day it arrived. Every wallet counted here is a household for whom the inclusion story is a fact this month, not a registration from a promotion two years ago |
| Vanity test | If every customer silently stopped valuing an on-ledger payment tomorrow, this count would fall inside the same rolling 30-day window it is measured on, because a wallet drops out the moment 30 days pass with no further on-ledger payment. It cannot only rise the way registered wallets (N1, 1,900,000 wallets) can: that count never falls, and it is exactly the trap this metric is chosen to avoid |
| Source system | Query NS-01 against the core ledger. Already live at signing: NS-01 computed the December 2025 baseline before this sheet existed |
| Current value | 96,000 wallets (N14), December 2025, the baseline this sheet was signed against. Amended 2026-08-21: 118,000 wallets (N15), 30 days to 2026-08-16, at the first review |

Rejected candidates, kept so the reasoning survives: registered wallets (N1, 1,900,000 wallets) is the trap the [mobile-money card](../knowledge/domains/mobile-money-wallets.md) names first, since it counts a customer who cashed out once during a sign-up push the same as one who transacts every week, and the total never falls. Thirty-day active wallets (N2 and N3, also the board's own key result, N4) came closer and was argued for in the vision conversation, but "active" is satisfied by a wallet that cashes in and cashes straight back out, which is exactly the 61 percent pass-through (N10) the wallet already carries too much of. Wallets with an on-ledger payment is the only one of the three candidates that a pass-through cycle cannot move on its own, which is the property the card's rule points at: active, on-ledger use belongs at the root, not registrations.

## 2. Input metric tree

All current and target figures below are ILLUSTRATIVE.

| Input metric | Causal claim (how it feeds the north star) | Owner (one name) | Current | Target |
|---|---|---|---|---|
| Bill-pay conversion: wallets paying at least one bill this month | A completed bill payment is itself an on-ledger payment event, so a wallet that converts from a bill lookup to a paid bill lands in M5's numerator directly, with no step between it and the star | Hira Baig | 0 wallets at signing, pre-launch. Amended 2026-08-21: 24,600 wallets, 31,200 bills, 5.8 percent of the 422,000-wallet active base (N53, against N3) | 40,000 bills in the four weeks to 2026-08-16, the one-pager's M1 target set 2026-03-25; missed, at 31,200 bills. No separate wallet-count target was ever set for this row, an open gap owned by Hira Baig |
| Cash-in to on-ledger spend within seven days | A cash-in that survives past the counter, instead of being cashed straight back out, is the raw material for a future on-ledger payment; growing this input is the mirror image of shrinking the pass-through guardrail in section 3 | Tariq Sohail | Not directly queried yet; a derived proxy ceiling stands in: at most 39 percent of cash-ins survive the 48-hour pass-through window at baseline (100 minus N10's 61 percent), and at most 42 percent at the 2026-08-21 amendment (100 minus N11's 58 percent) | Open: Tariq Sohail owns building the true seven-day on-ledger-spend query; until it exists, this row is bounded by the pass-through guardrail's inverse rather than measured on its own terms |
| M3, USSD bill-pay session completion | The USSD short code is the majority channel; a session that completes is a lookup that became a posted payment, and a session that drops mid-payment (theme T4, quote E4) is a customer who did not convert this month and may not dial again (risk R2) | Zainab Qureshi | Floor 90 percent. Week 1, to 2026-07-12: 87 percent, below floor. Amended 2026-08-21: 92 percent (N46) | 90 percent sustained, which doubles as guardrail 1 in section 3; no ceiling ambition beyond the floor has been set |
| Agents with float on bill-peak days | A same-visit cash-in-and-pay (story SAHULAT-S3) needs the agent's cash float, not only the customer's balance; an agent out of float on a bill-peak day is a payment the wallet never records, whatever the USSD menu can do | Tariq Sohail | No bill-peak-day baseline existed at signing. Amended 2026-07-08: 38 of 600 pilot agents reported a float stock-out on the year's first bill-peak day (N52); bill-peak days, the 5th to the 10th of the month, carry 44 percent of monthly bill volume (N57) | Open: Tariq Sohail; no stock-out ceiling had been set before launch, the same gap the float top-up hotline, the Gate 5 condition live 2026-07-17, exists to close |

## 3. Guardrails

Floors and ceilings below are ILLUSTRATIVE.

| Guardrail metric | Floor or ceiling | Who calls the halt | Why it guards |
|---|---|---|---|
| M3, USSD bill-pay session completion (N46) | Floor: 90 percent | Zainab Qureshi | Stops the north star's gain from being bought by a channel that silently fails half its sessions; a customer who gets no confirmation redials and risks paying twice (risk R2, theme T4), which would show as growth in attempts standing in for growth in value. Fired once: the week 1 reading of 87 percent triggered decision D7 on 2026-07-10, a four-day pause on the nationwide step while the timeout fix shipped, alongside 61 duplicate-payment tickets (N47) that same week |
| Trust-account reconciliation, unexplained breaks over PKR 1,000 at day end (N48) | Ceiling: 0 breaks per day | Bilal Hasan | Pooled customer funds moving through a new BillBridge integration are every customer's money at once if the trust account and individual wallet balances drift; a north star that rose because money was mispositioned in the ledger is not evidence of value delivered. Tested once: a PKR 12,300 break on 2026-07-14, explained within the day as a BillBridge retry posting twice; no halt was called because the same-day explanation held |
| M4, pass-through share (N10, N11) | Ceiling: must not rise above 61 percent | Hira Baig | Guards the metric itself against the inclusion story the [mobile-money card](../knowledge/domains/mobile-money-wallets.md) warns about: if the pass-through share climbed alongside M5, the wallets M5 counted would be growing for a reason unconnected to bill pay, and the star's rise would be coincidence rather than the causal claim in section 2, row 1. Held at 58 percent at the 2026-08-21 amendment (N11), below the ceiling; no halt was called |

## 4. Review cadence

- **Cadence:** Monthly, plus each Gate 6
- **Standing questions:** did each input move; did the north star follow; which causal claim looks weakest; what replaces it if it fails
- **Last review:** 2026-08-21, the four weeks to 2026-08-16, run by Hira Baig with Sara Lodhi as query owner. Row 2's claim looked weakest: M2, the one-pager's hypothesis metric, share of bill payments funded from a balance held more than 48 hours, measured a narrower thing than row 2 does, and both read badly for the same underlying reason, the balance-keeper persona Kamran (P3) was never representative of the base (risk R6). Nobody reconciled M2 against row 2 before launch; the mismatch is logged here rather than resolved, because decision D8 pivoted the product on 2026-08-28 before any input owner retuned it. What replaces it: the DISCOVER pass opening 2026-09-07 puts Rafiq (P2) at the centre and drops the balance-holding framing entirely; agent-assisted spend, not customer balance-holding, is the mechanism the next input owner defines
- **Next review:** 2026-09-21, run by Hira Baig, the first of the recurring monthly cadence now that a launched product exists to review every month

## Exit gate

This sheet is fit to steer by when:

- [x] The north star passes the written vanity test and is computed by a named source system. Section 1: the vanity test is written in full, and query NS-01 already computed the December 2025 figure before this sheet was signed
- [x] Every input carries a causal claim and exactly one named owner. Section 2: four rows, each with one mechanism sentence and one name
- [x] There are three to five inputs, not a dashboard's worth. Four
- [x] At least one guardrail exists, with a numeric floor and a named halt-caller. Three, in section 3, one of which fired: Zainab Qureshi's M3 floor, on decision D7
- [x] The review cadence is scheduled with an owner, not left as an intention. Monthly, next on 2026-09-21, Hira Baig
- [x] OKRs and PRD success metrics in flight trace to this tree, or the mismatch is logged. M1 traces cleanly to row 1; M2's mismatch against row 2 is named in section 4 rather than quietly dropped

Signed: Faisal Mirza, Chief Executive, sponsor, 2026-03-04. Read again at Gate 6, 2026-08-28, alongside the post-launch review; the pivot did not reopen this signature, because decision D8 replaces what feeds the tree's rows, not the tree's structure or the star itself.
