# PESTLE scan: Sahulat Bill Pay

Fills [frameworks/strategy/pestle.md](../frameworks/strategy/pestle.md). Everything here is invented and ILLUSTRATIVE: Sahulat, its people, agents, customers, billers, bank, aggregator and telco are fictional, and the values below come from the Sahulat data sheets rather than describing any real wallet, market or regulator. See [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md).

**Owner:** Hira Baig, Product Manager, the only PM in the company · **Date:** 2026-02-28 · **Status:** Complete for PLANNING

## What it is for

This scan records external changes that could touch Sahulat Bill Pay in the next four quarters and turns each material change into an owned response. It feeds the vision's why-now: Sahulat's bill-pay path depends on Falak Telecom's USSD channel, the licence's permitted activities and tiered-KYC limit, and BillBridge's quoted posting terms.

The scan uses the product-specific evidence in [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md). It is not a general market report.

## Run it when

- A strategy or vision refresh needs dated facts for the why-now.
- A regulation, licence condition, platform policy or supplier term could change the product plan.
- A vendor term has a known effective date or a quoted service condition that could affect customer outcomes.
- The next planning review needs an external-change record before the product strategy is refreshed.

This scan is dated 2026-02-28. Changes that need a planned response are routed to the roadmap, risk register, dependency register or acceptance criteria rather than left as general monitoring.

## Inputs you need first

- The Sahulat product, its USSD channel and the bill-pay proposal, from [sahulat-journey.md](sahulat-journey.md).
- The Falak Telecom tariff notice, N62, and the quoted USSD session ceiling, N66.
- BillBridge's quoted posting terms, N36.
- Amna Rasheed's compliance confirmation that bill pay sits within the licence's permitted activities and the tiered-KYC limit, later recorded through DEP-3 and AC-13.
- The external-change prompts in the blank worksheet: political, economic, social, technological, legal and environmental.

## The worksheet

One row records each specific change or the dated absence of a material change. Direction uses helps, hurts or mixed. Horizon is the next four quarters. The response is an act, watch or ignore decision for Sahulat Bill Pay.

| Category | Specific change (dated, sourced) | Direction | Horizon (quarters) | Likelihood | So what for this product in the next four quarters | Response | Owner | Feeds |
|---|---|---|---|---|---|---|---|---|
| Political | Nothing material identified in the political scan on 2026-02-28. No political change in the available Sahulat data requires a product response. | mixed | Next four quarters | low | No current political change alters Sahulat's bill-pay scope, channel or rollout plan. | Ignore: recorded and dated so it is not re-raised without a new signal. | Hira Baig | Vision why-now |
| Economic | Nothing material identified in the economic scan on 2026-02-28. No economic change in the available Sahulat data requires a product response. | mixed | Next four quarters | low | No current economic change alters the bill-pay proposal or its near-term plan. | Ignore: recorded and dated so it is not re-raised without a new signal. | Hira Baig | Vision why-now |
| Social | Nothing material identified in the social scan on 2026-02-28. No social change in the available Sahulat data requires a product response. | mixed | Next four quarters | low | The existing customer evidence remains the reason to investigate bill pay, but no new social change is added by this scan. | Ignore: recorded and dated so it is not re-raised without a new signal. | Hira Baig | Vision why-now |
| Technological | Falak Telecom's quoted USSD tariff changes from PKR 0.40 to PKR 0.65 per session, effective 2026-10-01, with a quoted session ceiling of 180 seconds, N62 and N66. The increase is PKR 0.65 minus PKR 0.40 = PKR 0.25 per session. | hurts | 2 to 3 | high | USSD bill pay becomes more expensive after 2026-10-01. Repeated or unnecessary sessions can reduce the contribution of a bill payment and make lookup, retry and confirmation behavior more important. | Act: add the tariff change and session-minimization response to the roadmap and risk register, with an owner. | Zainab Qureshi | Vision why-now; risk register |
| Technological | BillBridge's quoted posting terms, N36: posting to the biller within 30 minutes, seven days a week, with settlement to the biller T+1 through Sahulat's settlement bank. The signal to watch is a posting that exceeds 30 minutes or is unavailable outside the seven-day window; re-check on 2026-10-01, the Falak Telecom tariff effective date. | mixed | 2 to 3 | medium | The quoted terms help the product if they hold, but a quote is not a guarantee. A posting delay or a service-window gap would surface as a biller-posting failure in the service blueprint. | Watch: Hira Baig re-checks on 2026-10-01; a breach of the 30-minute or seven-day terms routes to the risk register. | Hira Baig | Risk register; Vision why-now |
| Legal | The team must confirm that bill pay is within the licence's permitted activities and record the applicable tiered-KYC limit before the bill-pay scope is treated as compliant. This confirmation later lands in DEP-3, needed by 2026-05-29, and the limit is named in AC-13. The team must comply with the State Bank of Pakistan's EMI Regulations and applicable tiered-KYC requirements. | mixed | 1 | high | The confirmation sets whether the proposed bill-pay activity can proceed and the tiered-KYC limit sets a hard refusal path for an ineligible payment. A legal compliance item is not a watch item. | Act: route the confirmation to DEP-3 and the tier-limit refusal to AC-13, with the compliance owner accountable. | Amna Rasheed | Dependency DEP-3; acceptance criterion AC-13; Vision why-now |
| Environmental | Nothing material identified in the environmental scan on 2026-02-28. No environmental change in the available Sahulat data requires a product response. | mixed | Next four quarters | low | No current environmental change alters Sahulat's bill-pay scope, channel or operating plan. | Ignore: recorded and dated so it is not re-raised without a new signal. | Hira Baig | Vision why-now |

### Arithmetic recorded for the material changes

- Falak Telecom tariff increase: PKR 0.65 per session minus PKR 0.40 per session = PKR 0.25 additional quoted cost per session.
- The quoted session ceiling remains 180 seconds. No additional cost or rate is inferred from that ceiling.
- BillBridge's quoted terms remain a service condition, not a derived figure: posting within 30 minutes, seven days a week, with settlement to the biller T+1 through Sahulat's settlement bank.

### Response detail

- **Falak Telecom, act:** Zainab Qureshi owns the roadmap and risk-register response. The product must account for the effective date, the PKR 0.25 per-session increase and the 180-second session ceiling.
- **Licence and tiered-KYC, act:** Amna Rasheed owns the compliance confirmation. DEP-3 records that bill pay sits within the licence's permitted activities and that the notification is filed. AC-13 records the tier-limit refusal path without inventing or restating a missing limit figure.
- **BillBridge, watch:** Hira Baig watches whether the quoted posting condition remains within 30 minutes, seven days a week. The signal is a posting that exceeds 30 minutes or a posting that is unavailable outside a seven-day service window. Re-check on 2026-10-01, the Falak Telecom tariff effective date. If the quoted condition changes or a biller-posting failure appears, route it to the risk register.

**Prompts per category applied.** Political: no material procurement, public-budget, trade or sanctions change was identified. Economic: no material interest-rate, hiring-freeze, travel-freeze or budget-cycle change was identified. Social: no new change to work patterns, automation expectations or trust evidence was identified. Technological: the Falak Telecom tariff and USSD ceiling were reviewed, along with BillBridge's quoted posting terms. Legal: permitted activities and the tiered-KYC limit were treated as compliance work. Environmental: no material reporting, carbon-accounting or physical-risk change was identified.

**Decision rule applied.** The Falak Telecom tariff has a known effective date inside the next four quarters, so it is act. The licence and tiered-KYC confirmation is legal compliance work, so it is act rather than watch. BillBridge is watch because its terms are quoted and the scan has a concrete signal and re-check date, recorded as its own row rather than as prose only. Political, economic, social and environmental are recorded as dated nothing-material rows. The scan therefore has two act rows, one watch row and four recorded stable rows, seven rows in all.

## Reading the result

- **Act rows:** the Falak Telecom tariff change and the licence and tiered-KYC confirmation are the plan-changing findings.
- **Falak Telecom:** the arithmetic is explicit. PKR 0.65 minus PKR 0.40 equals PKR 0.25 per USSD session, effective 2026-10-01. Zainab Qureshi owns the response.
- **Legal:** Amna Rasheed owns the permitted-activities confirmation and the tier-limit guardrail. DEP-3 and AC-13 are the landing places.
- **Watch row:** BillBridge's quoted terms help the product if they hold, but the team must watch the 30-minute, seven-days-a-week posting condition rather than treat a quote as a guarantee.
- **Stable rows:** political, economic, social and environmental were checked on 2026-02-28 and have no material change recorded.
- **Why now:** Sahulat's bill-pay opportunity is externally time-bound by the Falak Telecom tariff change and conditionally bounded by compliance confirmation and the tiered-KYC limit. Those dated constraints belong in the vision's why-now, not only in a later risk register.

## ILLUSTRATIVE example

This Sahulat worksheet is itself the ILLUSTRATIVE example of the PESTLE method. The Falak Telecom tariff row shows a dated, sourced change (PKR 0.40 to PKR 0.65 per session, effective 2026-10-01, N62) turned into an act row with an owner, a horizon of roughly two to three quarters from the 2026-02-28 scan date, and a landing place in the roadmap and risk register. The BillBridge row shows the opposite case: a quoted term with no effective date of its own, so it becomes a watch row with a named signal (a posting over 30 minutes, or unavailable outside the seven-day window) and a re-check date rather than an act row. The legal row shows a compliance item with a deadline about one quarter out (DEP-3, needed by 2026-05-29) treated as act rather than watch, because a licence confirmation is not something the team can merely observe.

## The trap

The failure mode here would be to describe bill pay as an opportunity while omitting the outside changes that can alter its economics or legal scope. The Falak Telecom tariff is not a general telecommunications headline: its arithmetic changes Sahulat's cost per USSD session from PKR 0.40 to PKR 0.65, an increase of PKR 0.25. The licence confirmation and tiered-KYC limit are not background notes: they determine the permitted activity and the refusal path.

The opposite failure would be to turn the scan into a news digest. The dated nothing-material rows keep the scan honest, while the BillBridge row names the signal and the re-check date. Every act row has an owner and a named landing place.

## Feeds

- [sahulat-journey.md](sahulat-journey.md): product context, N36, N62, N66, DEP-3 and AC-13.
- [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md): the coverage artifact map and the 2026-02-28 PESTLE timeline entry.
- [frameworks/strategy/pestle.md](../frameworks/strategy/pestle.md): the blank worksheet and method guidance.
- Vision's why-now: the dated Falak Telecom tariff change, the compliance confirmation and the tiered-KYC limit.
- Roadmap and risk register: the Falak Telecom act row.
- Dependency register and acceptance criteria: DEP-3 and AC-13.

**Exit-gate walk, signed:** Hira Baig, Product Manager, 2026-02-28. The scan has two act rows with named owners and landing places, one watch row (BillBridge) with its own worksheet row, a signal and a re-check date, and dated nothing-material rows for political, economic, social and environmental.
