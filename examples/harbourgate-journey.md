# Harbourgate Journey: modernising a regulated brownfield checkout

Fills no template. This file is the index and data sheet for the Harbourgate journey, the sixteen filled artifacts that complete [checkout-modernization-brownfield.md](checkout-modernization-brownfield.md) from Gate 4 through the retirement of the legacy path. Everything here is invented: Harbourgate is a fictional mid-market retailer, Kestrel, Marlowe and Tidewater are fictional payment providers, every person is fictional, and every number, date, rate and pound is ILLUSTRATIVE, chosen so that the sixteen artifacts reconcile with each other and with the earlier example, never to be quoted as a benchmark or copied as a target. See the [examples index](README.md).

**Owner:** Ife Adeyemi, Product Manager · **Date:** 2026-10-16 · **Status:** Journey complete through Gate 6; legacy sunset in execution · **Seed:** [checkout-modernization-brownfield.md](checkout-modernization-brownfield.md), written 2026-06-01 with Gate 4 in progress · **Sector cards:** [payments acquiring](../knowledge/domains/payments-acquiring.md), [retail in-store](../knowledge/domains/retail-in-store.md), [ecommerce](../knowledge/domains/ecommerce.md) · **Loop:** [os/OPERATING-LOOP.md](../os/OPERATING-LOOP.md), gates in [os/STAGE-GATES.md](../os/STAGE-GATES.md)

## The journey in one page

**The setting.** Harbourgate sells through a web store, an app and 61 shops, each shop with one kiosk where a customer orders an out-of-stock size for home delivery and pays on a PIN pad. All of it pays through one nine-year-old checkout, code-named checkout-pay, which reached three card providers at three different times: Kestrel for the web in 2017, Marlowe in 2019 as a second acquirer with a cascade rule that retried Kestrel declines through it, and Tidewater in 2021 for the kiosks, through a wrapper written by a contractor who left the same year. Harbourgate is the merchant of record. PCI DSS reaches it through its acquiring contracts, the card schemes' rules reach it through the same contracts, and the Marlowe path carries the card number through Harbourgate's own servers, which is why seven systems sit in the PCI assessment scope. The problem the earlier example reconstructed stands unchanged: one order in nine that reaches the payment step never completes it, and nobody can say which provider is responsible, because Marlowe does not log declines at all. The new payment service that replaces the layer is called Quay.

**The people.** Every name is fiction; roles are what the artifacts need.

| Name | Role | Where they carry weight |
|---|---|---|
| Ife Adeyemi | Product Manager, owner of the product and of every artifact | Decider at every gate; declared the conflict of deciding Gate 5 while owning the completion number |
| Tomasz Wierzbicki | Engineering Lead; design owner; cutover lead with authority to abort | Aborted rehearsal 1; owned finding an owner for the wrapper |
| Bea Lindqvist | Senior Engineer, payments; caretaker of the contractor's wrapper from 2026-04-24; owns Quay's reconciliation service | Incident owner for HG-INC-14; owns the integrations register and the dashboard |
| Noor Haddad | QA Lead | Gate 4 QA signature; facilitated the postmortem |
| Priya Raman | Head of Finance Operations | Agreed the decline baselines; signs every reconciliation; accountable for the daily close |
| Rohan Iyer | Chief Financial Officer, sponsor and budget owner | Accepted R4 by name in D-022; Gate 6 sponsor signature |
| Saoirse Whelan | Fraud and Risk Lead | Her team saw the double authorisations first, 2026-05-19 |
| Hamid Qureshi | Information Security Lead and PCI DSS owner | The adversary in the STRIDE walk; security reviewer at Gate 3; regulatory owner where the shipped overlay did not apply |
| Lena Baptiste | Head of Store Operations, 61 shops and their kiosks | The difficult quadrant: high influence, low interest until the kiosks were touched |
| Callum Fraser | Support Lead | Support and on-call briefings; Gate 5 support signature with a written condition |
| Grace Mbeki | Data Engineering Lead | Reporting reads the legacy table shape; owns DEP-4 |
| Anneliese Vogt | Legal Counsel and Data Protection Officer | Compliance sign-off; sent the provider termination notices |
| Ines Castellanos | Design Lead | Owns the deferred guest checkout redesign; Gate 5 design line |
| Dani Ferreira | Kestrel merchant success manager (counterparty) | Named contact on integrations I-1 to I-4 and DEP-1 |
| Roles without names | The contractor who wrote the wrapper (left 2021); the finance analyst who noticed the empty dashboard; the on-call engineer; store associates | Postmortem cause rows use roles, never names |

**The stages.** DISCOVER was reconstructed, not run, between 2026-03-09 and 2026-03-23. DEFINE produced a full PRD, the non-functional requirements and the business rules; Gate 2 was returned on 2026-03-31 for lacking a measurable "at least as good as the old path" and signed on 2026-04-07 against per-provider decline baselines that finance agreed. DESIGN was short, because the reconstruction had already settled the direction: ADR-0001 to ADR-0003 on 2026-04-08 and 2026-04-09, the STRIDE walk on 2026-04-08, the premortem on 2026-04-09, and Gate 3 on 2026-04-10, accepted with a known miss (the wrapper had no owner, so the gate recorded an owner for finding one, with a date). BUILD carried the decision pair the earlier example kept: D-011 on 2026-04-14 ramped by traffic percentage with a shadow comparison, the fraud team saw double authorisations on 2026-05-19, and D-017 on 2026-05-21 moved to one provider at a time behind a per-provider flag, sending AC-3 back to Gate 2 for re-signing on 2026-05-28. Gate 4 failed once on 2026-06-03, because two failure scenarios had been described and not exercised, and was met on 2026-06-09. DELIVER is where this journey earns its place: a cutover plan on 2026-06-02, a rehearsal that failed on 2026-06-13, an incident on 2026-06-15, a NO-GO at Gate 5 on 2026-06-16, a reshaped plan on 2026-06-18, two clean rehearsals, a GO WITH CONDITIONS on 2026-07-08, and three providers' traffic shifted in cohorts between 2026-07-13 and 2026-09-07. OPERATE measured the four weeks to 2026-10-05, and Gate 6 on 2026-10-14 recorded PERSIST for Quay, with the legacy path's sunset as the scheduled consequence: shutdown 2026-12-15, post-sunset check 2027-01-14, the old table shape removed 2027-03-31.

**The rejected option.** The architecture that lost, in ADR-0003, was a new wrapper over all three providers: keep Kestrel, Marlowe and Tidewater, put a routing layer in front, and gain the ability to send any order to any acquirer. It lost on operational risk, and the argument was the contractor's wrapper itself: a wrapper is what an integration becomes when it is nobody's, and three providers behind one layer meant three settlement file formats, three decline vocabularies, three on-call surfaces and three contracts, forever, in exchange for a routing flexibility that the 2019 cascade rule had shown produces double authorisations rather than approvals. Quay routes every card payment through Kestrel, which already carried 58% of volume and whose terminal SDK covers the kiosk PIN pads, and the other two integrations are retired without functional change; the one exception, the 2026-05-08 log-scrubbing patch (G2), was a security fix approved by Hamid Qureshi as an exception to the out-of-scope row. The price is named in the ADR: a single provider is a single point of failure, R4, accepted by name in D-022.

**The failed hypothesis and what it cost.** D-019 on 2026-06-02 assumed a provider migration behaves like a core migration: freeze, move, verify, switch, one weekend per provider. Rehearsal 1 on 2026-06-13 ran that sequence against Marlowe on production-shaped data and could not pass its own verify phase: 1,529 of the 1,742 lines in Marlowe's settlement file carried legacy references that Quay's reconciliation did not recognise, because settlement lags authorisation by up to three days and refunds lag by months, so there is no instant at which a provider has nothing in flight. The rehearsal was aborted at 9 hours 10 minutes, and its scheduled ingestion job, left enabled in pre-production with the only credentials Marlowe issues, consumed and deleted Monday's production settlement file at 07:00 on 2026-06-15. Finance's daily close ran 5 hours 40 minutes late, nobody was paged because no alert existed for a missing file, and the whole thing is written up as HG-INC-14. The plan changed under D-021 to a phased traffic shift: cohorts of 5%, 50% and 100% of each provider's orders, six, 30 and 61 shops for the kiosks, no freeze, no shadow, and the legacy path kept ingesting its own files and serving its own refunds until each provider drained. The hypothesis cost six weeks on the completion date (2026-07-26 to 2026-09-07), about four engineer-weeks on ADR-0004, one cancelled cutover weekend and one late finance close. What it bought is in the register: R9 and R14 exist now, and the rehearsal that fails is the one worth running.

## Data sheet (every value ILLUSTRATIVE)

Every artifact in the journey takes its numbers from this sheet and cites the row. Firmness uses four words: measured (recorded in a named fictional system or document), estimate (derived from measured rows by arithmetic shown), target (agreed and not yet true), assumption (believed, with an owner). A number not on this sheet does not appear in any artifact.

### Inherited from the seed, unchanged

These facts come from [checkout-modernization-brownfield.md](checkout-modernization-brownfield.md) and no artifact may contradict them: Ife Adeyemi entered the loop on 2026-03-09; one order in nine that reaches the payment step never completes it; three providers, one behind a wrapper written by a contractor who left in 2021; two of the three log to different systems and one logs no declines; personas were skipped with the reason recorded; the competitive analysis framed the decision as "rebuild the payment layer in place, or route through a single provider and retire two integrations", with "keep the stack and only fix the logging" as the non-product alternative; Gate 1 was reconstructed and labelled so; the reconstruction cost two weeks of a senior PM; a full PRD was chosen; the out-of-scope table holds the wrapper, the guest checkout redesign and the order-history page; the new path keeps writing the old table shape for at least two quarters with a removal date in the data model; D-011 (2026-04-14) and D-017 (2026-05-21) stand with their options, rationale and audiences as written; Gate 2 was returned once and signed on the second attempt against decline rate per provider with finance agreeing the baseline; Gate 3 passed with the wrapper-owner miss recorded as an owner for finding an owner; D-017 sent one acceptance criterion back to Gate 2; and the double-authorisation risk sat in the register as a medium, raised by an engineer at the premortem.

### Numbers

All ILLUSTRATIVE. Pounds are the fictional retailer's currency; percentages are of the base named in the row.

| ID | Number | Value (unit) | Source inside the fiction | Firmness |
|---|---|---|---|---|
| N1 | Shops | 61 shops | Store operations register, 2026-03 | measured |
| N2 | Kiosks | 61 kiosks, one per shop | Store operations register | measured |
| N3 | Orders reaching the payment step, average day | 6,400 orders/day | Order data, February 2026 | measured |
| N4 | Orders reaching the payment step, peak day | 31,000 orders/day | Order data, 2025-11-28 | measured |
| N5 | Payment-step non-completion at entry | 1 order in 9, 11.1% of orders reaching the step | Order data, February 2026; the seed's problem statement | measured |
| N6 | Non-completing orders, average day | 711 orders/day (N3 x N5) | Arithmetic on N3 and N5 | estimate |
| N7 | Recoverable share of non-completing orders | 35% of N6 | Reconstructed problem framing, owner Ife Adeyemi | assumption |
| N8 | Recoverable orders, average day | 250 orders/day (711 x 35%, rounded) | Arithmetic on N6 and N7 | estimate |
| N9 | Average order value | £64 per order | Finance, quarter ending 2026-03-31 | measured |
| N10 | Cost of inaction | £16,000/day, about £5.8M/year (250 x £64 x 365) | Reconstructed problem framing | estimate |
| N11 | Card value settled, average day | £410,000/day | Finance daily close, February 2026 | measured |
| N12 | Volume share by provider at entry | Kestrel 58%, Marlowe 27%, Tidewater kiosks 15% of N3 | Payment tables, February 2026 | measured |
| N13 | Decline rate baseline, Kestrel | 6.8% of authorisation attempts, trailing 4 weeks to 2026-04-03 | Payment tables; agreed by Priya Raman at Gate 2 attempt 2 | measured |
| N14 | Decline rate baseline, Marlowe | 9.9% of authorisation attempts, same window | Marlowe monthly statements (attempt and approval counts), since Marlowe logs no declines; agreed by Priya Raman | estimate |
| N15 | Decline rate baseline, Tidewater kiosks | 3.1% of authorisation attempts, same window | Wrapper log files | measured |
| N16 | AC-3 tolerance | Baseline + 0.5 percentage points, trailing 7 days, per migrated cohort | Gate 2 attempt 3, D-018 | target |
| N17 | Rollback trigger | Cohort decline rate above baseline + 2 percentage points over 30 minutes, or Kestrel 5xx above 2% of calls over 5 minutes; called by on-call without discussion | Release readiness section 4 | target |
| N18 | Decline rate at Gate 6 | Kestrel connector 6.5%; former Marlowe cohort 8.7%; kiosks 3.0% of attempts | Decline event stream, 2026-09-08 to 2026-10-05 | measured |
| N19 | Payment-step non-completion at Gate 6 | 7.4% of orders reaching the step | Order data, 2026-09-08 to 2026-10-05 | measured |
| N20 | Declines carrying provider and reason class | 0% of Marlowe declines at entry; 100% of all declines at Gate 6 | Decline event stream | measured |
| N21 | Support tickets tagged "payment failed" | 210 tickets/week in March 2026; 140 tickets/week in September 2026 | Support tool | measured |
| N22 | On-call pages for the payment path | 11 pages in March 2026; 4 pages in September 2026 | On-call tool | measured |
| N23 | Authorise latency, end to end, p95 | Target 2,000 ms; measured 1,350 ms in the Kestrel sandbox on 2026-06-05 | NFR section 1; load test 2026-06-05 | target; measured |
| N24 | Payment requests per second | Average 6 req/s; peak minute 24 req/s on 2025-11-28; design ceiling 50 req/s (Kestrel per-account limit, MSA schedule 2); breaks at 80 req/s (payment table write path); requests per order by call type: see N24a, which reconciles this row's average and peak against N3 and N4 | Payment API request logs (every Quay call, including status polls and retries, not orders); load test 2026-06-05; Kestrel MSA | measured; measured; measured; measured |
| N24a | Payment requests per order, by call type | Average day: 1 authorise + 3 status polls (checkout client polls roughly every 500 ms against the 1.35 s median Kestrel response, N23) + 0.3 retries (about 30% of orders trigger the one network-error retry the API contract allows, N61) + 3 webhooks (order-service capture confirmation, finance settlement ping, kiosk store-floor status push, N32) = about 7.3 requests per order. At N3's 6,400 orders/day that is about 46,700 order-driven requests/day (0.54 req/s); the remaining 471,700 req/day of N24's measured 6 req/s average (518,400 req/day) is Quay's own clock-driven traffic, health checks and the I-2 reconciliation poll (N30), which runs whether or not an order is in flight. Peak minute: N4's 31,000-order peak day averages 21.5 orders/minute (31,000 / 1,440); a peak-minute concentration factor of about 5x that average, the same flash-sale spike N4 cites, puts about 108 orders in the single busiest minute, about 790 order-driven requests at 7.3 per order, against the 1,440 requests N24 measures in that minute (24 req/s x 60 s); the remaining roughly 650 is the same clock-driven background traffic, itself somewhat elevated under load | Derived from N3, N4, N12, N23, N24, N30, N32, N61 | derived |
| N25 | Availability of the payment step | 99.9% of minutes, monthly | NFR section 2, observability SLO 1 | target |
| N26 | Kestrel committed SLA | 99.9% monthly availability | Kestrel master services agreement, schedule 3, held by Anneliese Vogt | measured |
| N27 | Marlowe committed SLA | 99.5% monthly availability | Marlowe contract of 2019, schedule 1 | measured |
| N28 | Tidewater SLA | No SLA clause in the 2021 contract | Tidewater contract of 2021, read by Anneliese Vogt 2026-04-03 | measured |
| N29 | Recovery time objective | 30 minutes during the drain (flag flip to legacy, rehearsed 3 min 50 s); 60 minutes after sunset (Kestrel region failover, MSA schedule 3) | NFR section 2 | target |
| N30 | Recovery point objective, authorisations | 0 minutes: Kestrel is the record; Quay persists the intent and idempotency key before the call and the outcome after, closing any gap through I-2 status polling and daily reconciliation | NFR section 2 | target |
| N31 | Kiosk fallback | "Pay at the till" shown within 10 s of a failed call; basket held 30 minutes | Store operations policy, Lena Baptiste | target |
| N32 | Kiosk store-floor SLO | 99.5% of kiosk payment attempts show an outcome within 10 s, per shop per day; alert when any shop is below 95% over 2 hours | Observability SLO 3 | target |
| N33 | Settlement file arrival | Kestrel daily 06:30, covering the previous day; Marlowe daily 06:30, weekend settlements on Monday's file; Tidewater weekly, Mondays 06:30 | Provider file specifications, held by Bea Lindqvist | measured |
| N34 | Settlement-file-absent alert | Page at 07:45 if no file has landed since 06:30; live in production 2026-07-09 | Corrective action A3 | target, then measured |
| N35 | Reconciliation tolerance | £50 per provider per day on settled versus captured value; 0 lines on count once the straddle set is classified | Finance close policy v3, Priya Raman | target |
| N36 | Straddle drain | Straddle set reaches 0 lines by T+3 days (Marlowe, Kestrel) and T+8 days (Tidewater) after a cohort reaches 100% | ADR-0004 | target |
| N37 | Rehearsal 1 | 2026-06-13, pre-production, production-shaped copy; aborted at 9 h 10 min against a planned 6 h; 1,529 of 1,742 Marlowe settlement lines unmatched; £111,500 in the file | Rehearsal log | measured |
| N38 | Rehearsal 2 | 2026-06-27, 5 h 20 min, 2 issues found and fixed (legacy refunds returned 422; voided authorisations double-counted) | Rehearsal log | measured |
| N39 | Rehearsal 3 | 2026-07-04, 4 h 45 min, no issues | Rehearsal log | measured |
| N40 | Rollback rehearsal | Flag flip to legacy 3 min 50 s; restore after flag removal 22 minutes; both 2026-07-04 in pre-production | Rehearsal log | measured |
| N41 | HG-INC-14 | First impact 07:00, detected 08:10 by a finance analyst, resolved 12:40 on 2026-06-15; 5 h 40 min; severity 3 on Harbourgate's 1 to 4 scale | Incident record | measured |
| N42 | Finance close delay | 5 h 40 min late on 2026-06-15; 5,190 settlement lines and £332,000 reconciled late | Finance close log | measured |
| N43 | Cost of the failed hypothesis | 6 weeks on the completion date (2026-07-26 to 2026-09-07); about 4 engineer-weeks on ADR-0004; 1 cancelled cutover weekend; 1 late finance close | D-021, engineering estimate | estimate |
| N44 | Cost of D-017 | Roughly one month on the completion date (2026-06-30 to 2026-07-26) | The seed, D-017 | estimate |
| N45 | Cost of the reconstruction | 2 weeks of a senior PM's time | The seed | measured |
| N46 | Cohort sizes | Web providers: 5%, 50%, 100% of that provider's orders by order-id hash; kiosks: 6, 30, 61 shops | Cutover plan v2 | target |
| N47 | Cohort dwell | 3 days at 5% and 4 days at 50% for web providers; 7 days per store cohort | Cutover plan v2 | target |
| N48 | Store shift window | 06:00 to 07:30 local, before the earliest shop opens at 08:00 | Cutover plan v2, agreed by Lena Baptiste | target |
| N49 | Legacy flag removal (point of no return per cohort) | 14 days after 100%: Marlowe 2026-08-03, Tidewater 2026-08-31, Kestrel legacy 2026-09-21 | Cutover plan v2 section 4 | target, then measured |
| N50 | Returns policy | 90 days from delivery; legacy refund capability retained to 2026-11-15 (2026-08-17 + 90 days) | Harbourgate returns policy v9 | measured |
| N51 | Provider contract notice | 90 days minimum; notices sent 2026-09-14 for termination on 2026-12-15 (92 days) | Marlowe and Tidewater contracts, D-023 | measured |
| N52 | Portal wind-down access | 6 months after termination, to 2027-06-15, for refunds and disputes on legacy-authorised orders | Wind-down clause in both contracts, held by Anneliese Vogt | measured |
| N53 | Legacy path running cost | £9,400/month: Marlowe minimum £2,100, Tidewater minimum £1,650, legacy infrastructure £5,650 | Finance, September 2026 | measured |
| N54 | On-call share consumed by the legacy path | 0.4 FTE | Engineering estimate, Tomasz Wierzbicki | estimate |
| N55 | PCI DSS systems in assessment scope | 7 at entry; 5 during the drain; 3 after sunset | InfoSec scope register, Hamid Qureshi | measured; measured; target |
| N56 | Blended card processing cost | 1.38% of card value at entry; 1.29% after consolidation | Finance; Kestrel interchange-plus schedule | measured; estimate |
| N57 | Step-up authentication threshold | Card-not-present orders above £250, or any fraud-rule flag | Fraud policy v6, Saoirse Whelan | measured |
| N58 | Retention | Card token 13 months after last use; masked PAN (first 6, last 4) and expiry 13 months; cardholder name, billing address and email 7 years with the order; decline events 13 months; settlement files 7 years; wrapper log files deleted by 2027-01-15 | Harbourgate retention schedule v3, Anneliese Vogt | measured |
| N59 | Legacy-authorised orders inside the returns window at 2026-11-15, when BR-002 ends | 1,900 orders | Finance estimate | estimate |
| N60 | Legacy refund volume after the final shift | 41 refunds/day in September 2026, 12 refunds/day by 2026-10-15 | Reconciliation service | measured |
| N61 | Kestrel call policy in Quay | Timeout 8 s; one retry after 2 s on network error only, same idempotency key; idempotency window 24 h; rate limit 50 req/s total across consumers, 429 with Retry-After | API contract sections 1, 4 and 5 | target |
| N62 | Decline reason class "other" | 6% of Kestrel declines at Gate 5 attempt 2; 1.5% after the mapping fix of 2026-08-14 | Decline event stream | measured |
| N63 | The payments squad | 5 engineers, 1 QA lead, 1 PM | Engineering | measured |
| N64 | Peak change freeze | 2026-11-13 to 2026-12-04: no Quay or flag changes except rollbacks | D-022, cutover plan v2 | target |
| N65 | Old table shape | Removal date 2027-03-31 (ADR-0002); reporting migrated off it by 2027-02-27 (DEP-4) | Data model section 6, ADR-0002 | target |
| N66 | Tidewater client certificate expiry | 2027-02-03 | The certificate, read by Hamid Qureshi 2026-04-08 | measured |
| N67 | Gate 6 review window | 2026-09-07 + 4 weeks, to 2026-10-05; chosen at Gate 5 attempt 2 on 2026-07-08 | Release readiness header | measured |
| N68 | Risk and threat scoring | Likelihood 1 to 3 x impact 1 to 3; register threshold 6 | Risk register section 1; security checklist section 2 | measured |
| N69 | Marlowe support response | 4 hours, ticket queue only; responded in 2 h 10 min on 2026-06-15 | Marlowe contract of 2019; ticket MRL-88213 | measured |
| N70 | Plan v1 weekends (D-019) | Marlowe 2026-06-27 and 28; Tidewater 2026-07-11 and 12; Kestrel legacy 2026-07-25 and 26 | Cutover plan v1 | target, abandoned |
| N71 | Plan v2 cohort dates (D-021) | Marlowe 2026-07-13, 07-16, 07-20; Tidewater 2026-08-03, 08-10, 08-17; Kestrel legacy 2026-08-31, 09-03, 09-07 | Cutover plan v2 | measured |
| N72 | Synthetic failure check | 2026-07-02, Bea Lindqvist: Marlowe file withheld in pre-production; page fired at 07:46, runbook completed in 11 minutes | Observability section 6 | measured |

### Shared identifiers

Any artifact that refers to one of these uses the ID exactly as written.

**Architecture decision records**

| ID | Title (the decision) | Date | Status |
|---|---|---|---|
| ADR-0001 | Build Quay as a separate payment service in front of the checkout, not inside checkout-pay | 2026-04-08 | Accepted |
| ADR-0002 | Keep writing the legacy payment table shape from Quay until 2027-03-31 | 2026-04-08 | Accepted |
| ADR-0003 | Route every card payment through Kestrel from Quay and retire the Marlowe and Tidewater integrations | 2026-04-09 | Accepted; the filled artifact |
| ADR-0004 | Reconcile settlement for both paths from one ledger, matching on either reference, for the length of the drain | 2026-06-19 | Accepted; born from HG-INC-14 |

**Decision log entries** (D-011 and D-017 are the seed's; the rest continue the sequence)

| ID | Decision | Date | Decider | Relation |
|---|---|---|---|---|
| D-011 | Ramp the new path by traffic percentage with shadow comparison | 2026-04-14 | Ife Adeyemi | Reversed by D-017 |
| D-017 | Migrate provider by provider behind a per-provider flag | 2026-05-21 | Ife Adeyemi | Reverses D-011 |
| D-018 | Re-sign AC-3 against each provider's trailing 4-week decline baseline plus 0.5 percentage points | 2026-05-28 | Ife Adeyemi, Priya Raman | Gate 2 attempt 3 |
| D-019 | Cut each provider over in one weekend: freeze, move, verify, switch | 2026-06-02 | Ife Adeyemi, Tomasz Wierzbicki | Reversed by D-021 |
| D-020 | Treat rehearsal 1 as an incident; cancel the 2026-06-27 cutover; record Gate 5 attempt 1 as NO-GO | 2026-06-16 | Ife Adeyemi | Produces HG-INC-14 |
| D-021 | Shift each provider's traffic in cohorts with a legacy drain; no freeze, no shadow | 2026-06-18 | Ife Adeyemi, Tomasz Wierzbicki, Priya Raman | Reverses D-019 |
| D-022 | Accept R4 (a Kestrel outage stops all card payments) with the kiosk fallback, the peak freeze, and review on 2027-01-31, then quarterly | 2026-08-24 | Rohan Iyer | Accepted risk |
| D-023 | Send termination notices to Marlowe and Tidewater for 2026-12-15 | 2026-09-14 | Rohan Iyer, Anneliese Vogt | Pre-commits the sunset D-024 ratifies |
| D-024 | Gate 6: PERSIST for Quay; retire the legacy path by 2026-12-15 with Ife Adeyemi as owner | 2026-10-14 | Ife Adeyemi, Rohan Iyer | The sunset plan's decision source |
| D-025 | What the legacy path taught, one paragraph, filed after the post-sunset check | 2027-01-14 (target) | Ife Adeyemi | Sunset plan section 7 |

**Risks** (score is L x I on the 1 to 3 scales; register threshold 6)

| ID | Risk (event) | Category | Score at premortem or entry | What happened |
|---|---|---|---|---|
| R1 | Shadow-comparison retries authorise the same card twice | security | 4 (L2 x I2), raised by an engineer at the premortem of 2026-04-09 | Occurred 2026-05-19; closed 2026-05-21 by D-017 |
| R2 | Nobody owns the contractor's wrapper when it misbehaves | delivery | 6 (L3 x I2) | Closed 2026-04-24: Bea Lindqvist named caretaker |
| R3 | Marlowe issues no sandbox settlement files, so reconciliation is tested against production files | delivery | 4 (L2 x I2), mitigation "read the production drop with the keep flag" | Occurred 2026-06-13 (rehearsal 1) and 2026-06-15 (HG-INC-14); re-scored 9 on 2026-06-15; closed 2026-07-03 when ADR-0004 removed the need |
| R4 | A Kestrel outage stops every card payment on every surface | viability | 3 (L1 x I3) | Accepted by Rohan Iyer, D-022, 2026-08-24; revisit 2027-01-31 |
| R5 | A change to the legacy table shape breaks reporting, finance reconciliation or the order-history page | delivery | 6 (L2 x I3) | Mitigated by ADR-0002 and DEP-4; open, reviewed monthly |
| R6 | A kiosk cohort flip fails while shops are trading | delivery | 6 (L2 x I3) | Mitigated by N48 and per-shop rollback; closed 2026-08-17, did not occur |
| R7 | A refund against a legacy-authorised order fails after that provider is shifted | value | 9 (L3 x I3), raised 2026-06-16 | Mitigated by BR-002, BR-009 and N50; open until 2027-06-15 |
| R8 | The wrapper's log files hold the masked PAN and the cardholder name in plain text | security | 6 (L3 x I2), from finding F1 | Scrubbing patch 2026-05-08; logs deleted by 2027-01-15; open until deletion |
| R9 | Lines authorised on the legacy path and settled after a shift go unmatched | delivery | 9 (L3 x I3), added 2026-06-16 | Mitigated by ADR-0004; closed 2026-09-15 after the last drain |
| R10 | Peak trading lands inside the drain, and a rollback would need providers whose contracts are under notice | delivery | 6 (L2 x I3) | Raised at the premortem as peak trading during the migration; re-worded 2026-06-18 under D-021. Mitigated by N64 and keeping the legacy path warm to 2026-12-15; open, review 2026-12-05 |
| R11 | Associates stop using kiosks after seeing the "pay at the till" fallback | usability | 4 (L2 x I2) | Weekly kiosk-use report per shop, Lena Baptiste; open |
| R12 | The Kestrel terminal SDK needs a kiosk firmware update that shops must schedule | delivery | 4 (L2 x I2) | Closed 2026-07-30 via DEP-5 |
| R13 | Unsigned Marlowe callbacks could mark an order paid | security | 6 (L2 x I3), from finding F3 | IP allowlist 2026-04-17; closed 2026-08-03 when the Marlowe flag was removed |
| R14 | Pre-production shares the production SFTP drop, so a rehearsal can consume a live file | security | Scored 4 at the STRIDE walk as F2 and sent to backlog item HG-812, never a register row | Occurred 2026-06-15; added at 9; closed 2026-06-26 by A2 |
| R15 | A kiosk authorisation lands after the kiosk has shown "pay at the till", leaving a second payment authorised for up to 24 h | value | 6 (L2 x I3), raised 2026-10-16 from the API contract's open item | Open; owner Bea Lindqvist; review 2026-11-13 |

**Dependencies**

| ID | Deliverable | Owning team and contact | Needed by | Committed | Status at 2026-10-16 |
|---|---|---|---|---|---|
| DEP-1 | Kestrel terminal SDK certified for the kiosk PIN pad model | Kestrel, Dani Ferreira | 2026-07-20 | 2026-07-10 | delivered 2026-07-09 |
| DEP-2 | Marlowe sandbox settlement files | Marlowe merchant support, ticket queue | 2026-06-05 | never committed; requested 2026-04-20 | closed 2026-07-03, need removed by ADR-0004 |
| DEP-3 | Finance daily-close runbook updated for dual-path reconciliation | Finance operations, Priya Raman | 2026-07-10 | 2026-07-08 | delivered 2026-07-08 |
| DEP-4 | Reporting migrated off the legacy table shape | Data engineering, Grace Mbeki | 2027-02-27 | 2027-02-27 | in progress |
| DEP-5 | Kiosk firmware update scheduled across 61 shops | Store operations, Lena Baptiste | 2026-08-01 | 2026-07-28 | delivered 2026-07-30 |
| DEP-6 | Fraud rules re-pointed at the decline event stream | Fraud and risk, Saoirse Whelan | 2026-07-13 | 2026-07-06 | delivered 2026-07-06 |
| DEP-7 | PCI DSS scope re-assessment booked for after the sunset | InfoSec, Hamid Qureshi, with the external assessor | 2026-12-15 | 2026-11-20 | in progress |
| DEP-8 | Termination notices to Marlowe and Tidewater | Legal, Anneliese Vogt | 2026-09-15 | 2026-09-14 | delivered 2026-09-14 |

**Stories and acceptance criteria**

| Story | Title | Acceptance criterion |
|---|---|---|
| HARBOURGATE-S1 | Pay by card on web and app through Quay and Kestrel hosted fields | AC-1: no card number reaches a Harbourgate server; AC-3: decline rate per migrated cohort no worse than baseline + 0.5 percentage points over a trailing 7 days (re-signed 2026-05-28, D-018) |
| HARBOURGATE-S2 | Pay by card at a kiosk through the Kestrel terminal SDK | AC-2: kiosk payment completes end to end on the certified PIN pad; AC-3 applies |
| HARBOURGATE-S3 | Show a decline with a reason class and offer one retry with a different method | AC-5: a declined card is never re-submitted automatically |
| HARBOURGATE-S4 | Per-provider routing flag with two-person change | AC-6: a flag change needs two named approvers and is logged with both names |
| HARBOURGATE-S5 | Route a refund to the provider that authorised the order | AC-7: a refund on a legacy-authorised order reaches the original provider |
| HARBOURGATE-S6 | Ingest settlement files and reconcile daily per provider across both paths | AC-8: daily reconciliation passes within N35 including the straddle set (amended 2026-07-03 from ADR-0004) |
| HARBOURGATE-S7 | Write the legacy table shape from Quay | AC-9: the order-history page and reporting read Quay's rows unchanged |
| HARBOURGATE-S8 | Log every decline from every provider into one event stream | AC-4: every decline carries provider, reason class and trace id |
| HARBOURGATE-S9 | Kiosk offline fallback | AC-10: "pay at the till" within 10 s; basket held 30 minutes |
| HARBOURGATE-S10 | Step-up authentication through Kestrel | AC-11: step-up invoked exactly when BR-005 says |
| HARBOURGATE-S11 | Capture on dispatch, void on fulfilment failure | AC-12: capture happens at dispatch; an authorisation with no dispatch inside 24 h is voided |
| HARBOURGATE-S12 | Settlement-file-absent alert | AC-13: a page fires by 07:45 when no file has landed (added 2026-06-19) |

**Business rules**

| ID | Rule, short form | Status |
|---|---|---|
| BR-001 | WHEN an authorisation is declined THEN offer one retry with a different method and never re-submit the same card automatically | active |
| BR-002 | WHEN a refund is requested against an order authorised on a legacy provider THEN route it to that provider through the legacy path | active until 2026-11-15, then BR-009 |
| BR-003 | WHEN settled value differs from captured value by more than £50 for a provider on a day THEN finance close is blocked until reconciled | active |
| BR-004 | WHEN a kiosk gets no outcome within 10 s THEN show "pay at the till" and hold the basket 30 minutes | active |
| BR-005 | WHEN a card-not-present order exceeds £250 or a fraud rule flags it THEN require step-up authentication | active |
| BR-006 | WHEN a payment is authorised and the order is not dispatched within 24 h THEN void the authorisation rather than capture | active |
| BR-007 | WHEN a per-provider routing flag is changed THEN two named approvers must record the change | active until the last flag is removed 2026-09-21 |
| BR-008 | WHEN Kestrel declines THEN retry the authorisation through Marlowe (the 2019 cascade) | retired 2026-07-20, replaced by BR-001 |
| BR-009 | WHEN a refund is requested against a legacy-authorised order after 2026-11-15 THEN finance operations refund through the provider portal within 5 working days | entered the register 2026-10-14 under D-024; active from 2026-11-16 |

**Integrations register rows**

| ID | Counterparty and direction | Note |
|---|---|---|
| I-1 | Kestrel authorisation API, outbound | REST over TLS, OAuth 2.0 client credentials, SLA N26 |
| I-2 | Kestrel status webhooks, inbound | HMAC-signed |
| I-3 | Kestrel terminal SDK on kiosks, outbound | Terminal keys; DEP-1 |
| I-4 | Kestrel settlement file, inbound SFTP | Daily 06:30, N33 |
| I-5 | Marlowe authorisation API, outbound, legacy | API key; card number in transit; SLA N27; retired 2026-12-15 |
| I-6 | Marlowe settlement file, inbound SFTP | Daily 06:30, weekend settlements on Monday's file; no sandbox; the file in HG-INC-14 |
| I-7 | Tidewater through the contractor's wrapper, outbound, legacy | XML over HTTPS; client certificate expiring N66; no SLA clause, N28 |
| I-8 | Tidewater settlement file, inbound SFTP | Weekly, Mondays 06:30 |
| I-9 | Fraud rules engine, internal, inbound event stream | Owner Saoirse Whelan's team; DEP-6 |
| I-10 | Order service and order-history page, internal | Reads the legacy table shape; ADR-0002 |
| I-11 | Finance ERP export, outbound nightly | From the reconciliation service |

**Security findings, incident and corrective actions**

| ID | Item |
|---|---|
| F1 | Wrapper log files hold the masked PAN and cardholder name in plain text; score 6; became R8 |
| F2 | Pre-production shares the production SFTP drop; score 4; routed to backlog HG-812, not to the register; became R14 after HG-INC-14 |
| F3 | Marlowe callbacks are unsigned; score 6; became R13 |
| F4 | One person can flip the routing flag; score 4; mitigated by BR-007 and AC-6 |
| HG-INC-14 | The cutover rehearsal consumed the Marlowe production settlement file; 2026-06-15; N41, N42 |
| A1 | Dual-path reconciliation with a classified straddle set (ADR-0004); cause 1; Bea Lindqvist; due 2026-07-03; verified by rehearsal 3 passing the amended AC-8, 2026-07-04 (N39); straddle logic first exercised in rehearsal 2 (N38) |
| A2 | Separate SFTP drop per environment; pre-production credentials cannot read the production drop; cause 3; Hamid Qureshi; due 2026-06-26; verified by a failed read attempt on 2026-06-26 |
| A3 | Settlement-file-absent page at 07:45; cause 4; Bea Lindqvist; due 2026-07-09; verified by N72 and the live page of 2026-07-10 |
| A4 | Production ingestion job exits non-zero on "no file"; cause 4; Bea Lindqvist; due 2026-06-26; verified in CI |
| A5 | Abort checklist gains "disable every pre-production schedule"; cause 5; Tomasz Wierzbicki; due 2026-06-19; verified at the rehearsal 2 abort drill |
| A6 | A dependency at "requested" for more than 4 weeks is escalated automatically at the weekly review; cause 2; Ife Adeyemi; due 2026-06-19; verified by the register's review log, 2026-07-02 |
| G1 | Compliance gap: the Tidewater contract has no data-processing clause covering the wrapper's log retention; Anneliese Vogt; closed 2026-07-31, before the first kiosk cohort, by agreeing in writing that the logs are deleted at sunset |
| G2 | Compliance gap: wrapper logs hold name and masked PAN outside the retention schedule; Hamid Qureshi; closed 2026-05-08 by the scrubbing patch, approved by Hamid Qureshi as the out-of-scope exception, deletion N58 |
| G3 | Compliance gap: PCI scope reduction not yet evidenced by an assessor; Hamid Qureshi; DEP-7 |

**Gate attempts**

| Gate | Attempt | Date | Outcome |
|---|---|---|---|
| Gate 1 | reconstructed, not run | 2026-03-23 | Filed as context, never cited as evidence |
| Gate 2 | 1 | 2026-03-31 | RETURNED: no measurable "at least as good as the old path" |
| Gate 2 | 2 | 2026-04-07 | SIGNED against N13 to N15 |
| Gate 2 | 3 | 2026-05-28 | SIGNED: AC-3 only, re-signed under D-018 |
| Gate 3 | 1 | 2026-04-10 | REVIEWED AND ACCEPTED with the wrapper-owner miss: Tomasz Wierzbicki to name an owner by 2026-04-24 |
| Gate 4 | 1 | 2026-06-03 | NOT MET: two failure scenarios described, not exercised |
| Gate 4 | 2 | 2026-06-09 | MET |
| Gate 5 | 1 | 2026-06-16 | NO-GO: rollback line unknown, reconciliation line failed, after rehearsal 1 |
| Gate 5 | 2 | 2026-07-08 | GO WITH CONDITIONS for the Marlowe cohorts, cohort 1 first; the filled release readiness |
| Gate 5 | 3 | 2026-07-29 | GO WITH CONDITIONS for the Tidewater store cohorts: DEP-5 delivered and G1 closed before cohort 1 (met 2026-07-30 and 2026-07-31) |
| Gate 5 | 4 | 2026-08-26 | GO for the Kestrel legacy connector cohorts |
| Gate 6 | 1 | 2026-10-14 | PERSIST for Quay; legacy sunset scheduled, D-024 |

### Timeline

| Date | Event | Stage |
|---|---|---|
| 2026-03-09 | Ife Adeyemi enters the loop | DISCOVER |
| 2026-03-23 | Reconstructed Gate 1 filed and labelled | DISCOVER |
| 2026-03-31 | Gate 2 attempt 1 returned | DEFINE |
| 2026-04-03 | Baseline window closes (N13 to N15); Anneliese Vogt reads the three contracts | DEFINE |
| 2026-04-07 | Gate 2 attempt 2 signed; NFR and business rules approved | DEFINE |
| 2026-04-08 | ADR-0001, ADR-0002; STRIDE walk with Hamid Qureshi as adversary | DESIGN |
| 2026-04-09 | ADR-0003; premortem; risk register R1 to R6 and R10 to R12, plus R8 and R13 from STRIDE findings F1 and F3 | DESIGN |
| 2026-04-10 | Gate 3 accepted with the wrapper-owner miss | DESIGN |
| 2026-04-14 | D-011 | BUILD |
| 2026-04-17 | IP allowlist on Marlowe callbacks (R13) | BUILD |
| 2026-04-20 | DEP-2 requested from Marlowe | BUILD |
| 2026-04-24 | Bea Lindqvist named caretaker of the wrapper; R2 closed | BUILD |
| 2026-05-06 | Percentage ramp with shadow comparison begins | BUILD |
| 2026-05-08 | Wrapper log scrubbing patch (R8, G2) | BUILD |
| 2026-05-19 | Fraud team reports double authorisations; R1 occurs | BUILD |
| 2026-05-21 | D-017; AC-3 sent back to Gate 2 | BUILD |
| 2026-05-28 | Gate 2 attempt 3: AC-3 re-signed, D-018 | BUILD |
| 2026-06-01 | The seed example is written, Gate 4 in progress | BUILD |
| 2026-06-02 | Cutover plan v1, D-019: one weekend per provider | BUILD |
| 2026-06-03 | Gate 4 attempt 1 not met | BUILD |
| 2026-06-05 | Load test: N23, N24 | BUILD |
| 2026-06-09 | Gate 4 attempt 2 met | BUILD |
| 2026-06-13 | Rehearsal 1 aborted at 9 h 10 min | DELIVER |
| 2026-06-15 | HG-INC-14: rehearsal job consumes the production Marlowe file; close 5 h 40 min late | DELIVER |
| 2026-06-16 | D-020; Gate 5 attempt 1 NO-GO; R7, R9 and R14 added | DELIVER |
| 2026-06-17 | Postmortem review, out loud, responders in the room | DELIVER |
| 2026-06-18 | D-021: phased traffic shift with legacy drain | DELIVER |
| 2026-06-19 | ADR-0004; A5 and A6 done; AC-13 added | DELIVER |
| 2026-06-25 | Cutover plan v2 drafted | DELIVER |
| 2026-06-26 | A2 and A4 done; R14 closed | DELIVER |
| 2026-06-27 | Rehearsal 2, 5 h 20 min, 2 issues | DELIVER |
| 2026-06-30 | PCI scope review by Hamid Qureshi | DELIVER |
| 2026-07-01 | reg-gap-check run; module does not apply; regulatory owner named | DELIVER |
| 2026-07-02 | Synthetic failure check N72 | DELIVER |
| 2026-07-03 | ADR-0004 built; AC-8 amended; R3 and DEP-2 closed | DELIVER |
| 2026-07-04 | Rehearsal 3 clean; rollback timed N40 | DELIVER |
| 2026-07-06 | Compliance impact assessment signed; pre-read circulated; DEP-6 delivered | DELIVER |
| 2026-07-08 | Gate 5 attempt 2: GO WITH CONDITIONS; cutover plan v2 approved; DEP-3 delivered | DELIVER |
| 2026-07-09 | Condition C1 met: alert live; DEP-1 delivered | DELIVER |
| 2026-07-10 | Condition C2 met: runbook published, support briefed | DELIVER |
| 2026-07-13 | Marlowe cohort 1, 5% | DELIVER |
| 2026-07-16 | Marlowe cohort 2, 50% | DELIVER |
| 2026-07-20 | Marlowe cohort 3, 100%; BR-008 retired | DELIVER |
| 2026-07-23 | Marlowe straddle set at 0 | DELIVER |
| 2026-07-29 | Gate 5 attempt 3: GO WITH CONDITIONS for store cohorts (DEP-5 delivered and G1 closed before cohort 1) | DELIVER |
| 2026-07-30 | DEP-5 delivered | DELIVER |
| 2026-07-31 | G1 closed before the first kiosk cohort | DELIVER |
| 2026-08-03 | Tidewater cohort 1, 6 shops; Marlowe flag removed; R13 closed | DELIVER |
| 2026-08-10 | Tidewater cohort 2, 30 shops | DELIVER |
| 2026-08-14 | Reason-class mapping fix (N62) | DELIVER |
| 2026-08-17 | Tidewater cohort 3, 61 shops; R6 closed | DELIVER |
| 2026-08-24 | D-022: R4 accepted | DELIVER |
| 2026-08-26 | Gate 5 attempt 4: GO for Kestrel legacy connector cohorts | DELIVER |
| 2026-08-31 | Kestrel legacy cohort 1, 5%; Tidewater flag removed | DELIVER |
| 2026-09-03 | Kestrel legacy cohort 2, 50% | DELIVER |
| 2026-09-07 | Kestrel legacy cohort 3, 100%; last order on the legacy path | DELIVER |
| 2026-09-14 | D-023; DEP-8 delivered: termination notices sent | OPERATE |
| 2026-09-15 | R9 closed after the last drain | OPERATE |
| 2026-09-21 | Kestrel legacy flag removed; BR-007 lapses | OPERATE |
| 2026-10-05 | Gate 6 review window closes | OPERATE |
| 2026-10-09 | Metrics review | OPERATE |
| 2026-10-14 | Gate 6: PERSIST; D-024 | OPERATE |
| 2026-10-16 | Sunset plan written; this index dated; R15 added | OPERATE |
| 2026-10-19 | Internal announcement and support briefing; legacy feature freeze | OPERATE |
| 2026-10-20 | N24a added: requests-per-order derivation closing N24's open item | OPERATE |
| 2026-11-13 to 2026-12-04 | Peak change freeze (N64) | OPERATE |
| 2026-11-15 | Legacy refund capability ends; BR-009 takes over next day | OPERATE |
| 2026-11-20 | DEP-7 committed date: assessor booked | OPERATE |
| 2026-12-15 | Legacy path shutdown; Marlowe and Tidewater contracts end | OPERATE |
| 2027-01-14 | Post-sunset check; D-025 | OPERATE |
| 2027-01-15 | Wrapper logs and legacy credentials deleted | OPERATE |
| 2027-02-27 | DEP-4: reporting off the legacy table shape | OPERATE |
| 2027-03-31 | Legacy table shape removed (ADR-0002) | OPERATE |
| 2027-06-15 | Provider portal wind-down access ends (N52) | OPERATE |

## Artifact map

Sixteen files, each filling one template with its H2 structure intact and its exit gate walked at the bottom by a named fictional signer. The brief says what the document decides and which data-sheet rows it draws on.

| File | Fills | Stage and gate | Brief |
|---|---|---|---|
| [harbourgate-adr.md](harbourgate-adr.md) | [templates/architecture/adr.md](../templates/architecture/adr.md) | DESIGN, feeds Gate 3 | ADR-0003 decides to route every card payment through Kestrel from Quay and retire the Marlowe and Tidewater integrations, and records why a new wrapper over all three providers lost on operational risk, with the contractor's wrapper as the evidence. Its consequences seed R4, R5 and the sunset plan. Uses N12, N13 to N15, N26 to N28, N55, N56, N66; ADR-0001, ADR-0002, ADR-0004; R2, R4, R5; D-011, D-017. |
| [harbourgate-system-design.md](harbourgate-system-design.md) | [templates/architecture/system-design.md](../templates/architecture/system-design.md) | DESIGN, feeds Gate 3 | Fixes the shape of Quay and its Kestrel connector beside the legacy path it must live with, stating the legacy table shape and the routing flag (per-provider from D-017, 2026-05-21) as constraints and putting the wrapper-over-three option in the alternatives table next to "fix the logging only". Goals are numbers from the NFR and components carry owners from the cast. Uses N3, N4, N23 to N25, N29, N30, N65; ADR-0001 to ADR-0003; R4, R5, R8, R13; I-1 to I-11; HARBOURGATE-S1 to S12. |
| [harbourgate-api-contract.md](harbourgate-api-contract.md) | [templates/architecture/api-contract.md](../templates/architecture/api-contract.md) | DESIGN, feeds Gate 3 | Quay's internal API v1 (authorise, capture, void, refund, status event) with the idempotency and error rules that make BR-001 and BR-002 enforceable, including the 402 versus 409 versus 503 distinctions the checkout clients must honour. Its consumers are the web checkout, the app, the kiosk, the order service, and finance operations tooling. Uses N24, N57, N61; HARBOURGATE-S1, S3, S5, S10, S11; AC-5, AC-7; BR-001, BR-002, BR-005, BR-006. |
| [harbourgate-integrations.md](harbourgate-integrations.md) | [templates/architecture/integrations.md](../templates/architecture/integrations.md) | DESIGN, feeds Gate 3 | Eleven boundary rows, I-1 to I-11, each with an owner, an SLA source and a failure behaviour a customer would recognise, including two legacy providers being retired (flags removed 2026-08-03 and 2026-08-31; integrations retire 2026-12-15). The failure drill names Kestrel as a counterparty (I-1 with I-3, and I-2 and I-4 behind them) as the worst single failure and I-6 as the one that actually failed. Uses N26 to N28, N31, N33, N34, N61, N66, N69; I-1 to I-11; R3, R4, R13, R14; DEP-1, DEP-2. |
| [harbourgate-security-architecture.md](harbourgate-security-architecture.md) | [templates/architecture/security-architecture.md](../templates/architecture/security-architecture.md) | DESIGN, feeds Gate 3 | The STRIDE walk of 2026-04-08 with Hamid Qureshi as the adversary, producing F1 to F4: two reached the register at 6, and F2, scored 4 and sent to backlog HG-812, became HG-INC-14. Standing checks say where Kestrel credentials and terminal keys live and how they rotate. Uses N55, N58, N68; F1 to F4; R8, R13, R14; BR-007; I-1 to I-8. |
| [harbourgate-observability.md](harbourgate-observability.md) | [templates/architecture/observability.md](../templates/architecture/observability.md) | DESIGN, feeds Gate 3; re-checked at Gate 5 | Four SLOs with targets and alert thresholds drafted before code existed (the kiosk SLO's thresholds provisional until Lena Baptiste agreed them on 2026-06-25), one alert added after the incident (the 07:45 settlement-file page), a dashboard with a named owner, and the synthetic failure check of 2026-07-02 recorded with its elapsed time. Uses N17, N23, N25, N32, N34, N58, N72; AC-4, AC-13; A3; I-1, I-4, I-6, I-8. |
| [harbourgate-nfr.md](harbourgate-nfr.md) | [templates/definition/nfr.md](../templates/definition/nfr.md) | DEFINE, feeds Gate 2 | Every non-functional number the design and the readiness document later cite, with a named owner for the one number not agreed at Gate 2 (the kiosk SLO) and one waiver, localisation, with a revisit date. Every row names the artifact that proves it. Uses N23 to N32, N24a, N35, N55, N58; AC-3, AC-9, AC-10; R4. |
| [harbourgate-business-rules.md](harbourgate-business-rules.md) | [templates/definition/business-rules.md](../templates/definition/business-rules.md) | DEFINE, feeds Gate 2; amended through DELIVER | BR-001 to BR-009, with the 2019 cascade rule BR-008 retired on 2026-07-20 because it produced double authorisations, and the refund-to-original-rail rule BR-002 that the sunset plan depends on, each with a business owner outside the product team. Uses N35, N50, N57; BR-001 to BR-009; AC-5 to AC-8, AC-11, AC-12; D-017, D-021, D-024; HARBOURGATE-S3 to S6, S9 to S11. |
| [harbourgate-dependency-register.md](harbourgate-dependency-register.md) | [templates/execution/dependency-register.md](../templates/execution/dependency-register.md) | DESIGN, feeds Gate 3; reviewed weekly through DELIVER | DEP-1 to DEP-8 with both dates on every row, and a weekly review log that shows DEP-2 sitting at "requested" for eight weeks before rehearsal 1 proved why it mattered. Reverse dependencies list what Quay owes the order-history page, the fraud team and finance. Uses DEP-1 to DEP-8; N33, N65; R3, R5, R12; A6. |
| [harbourgate-stakeholder-map.md](harbourgate-stakeholder-map.md) | [templates/execution/stakeholder-map.md](../templates/execution/stakeholder-map.md) | DISCOVER through OPERATE, first required at Gate 2 | Thirteen named people with RACI per decision area (one Accountable each), concerns in their own words with dates, and Lena Baptiste's engagement row for the difficult quadrant, walked through the 06:00 store window before the first kiosk cohort. Uses the cast table; N1, N48; D-022, D-023; the decision areas scope, budget, go or no-go per cohort, abort during a window, reconciliation sign-off, PCI scope, store cohort schedule, contract termination. |
| [harbourgate-risk-register.md](harbourgate-risk-register.md) | [templates/execution/risk-register.md](../templates/execution/risk-register.md) | DESIGN, feeds Gate 3; reviewed weekly | R1 to R15 on the 1 to 9 scale: R1 to R6 and R10 to R12 from the premortem of 2026-04-09, R8 and R13 from F1 and F3, R7, R9 and R14 added 2026-06-16, R15 added 2026-10-16, with R1 at 4 that occurred, R14 that never got a row until it occurred, R4 accepted by name, and the closed table that keeps the history. Uses R1 to R15; N68; D-017, D-021, D-022; F1 to F3; DEP-2. |
| [harbourgate-migration-cutover-plan.md](harbourgate-migration-cutover-plan.md) | [templates/delivery/migration-cutover-plan.md](../templates/delivery/migration-cutover-plan.md) | DELIVER, feeds Gate 5 | Version 2 of the plan, phased by cohort per provider with a legacy drain, with the one-weekend shape of D-019 recorded as the rejected shape and why rehearsal 1 killed it; three rehearsals with elapsed times, a rollback timed at 3 min 50 s, and reconciliation checks with a £50 tolerance signed by Priya Raman. Uses N33, N35 to N40, N46 to N49, N70, N71; D-019, D-021; ADR-0004; R6, R7, R9; A1, A2, A4, A5. |
| [harbourgate-release-readiness.md](harbourgate-release-readiness.md) | [templates/delivery/release-readiness.md](../templates/delivery/release-readiness.md) | DELIVER, this file is Gate 5 (attempt 2) | The GO WITH CONDITIONS of 2026-07-08 for the Marlowe cohorts, cohort 1 first, with two written conditions carrying owners and dates, three known issues distinguished from conditions, a rollback trigger a dashboard can show, and a section 7 that says the AI overlay did not fire and names what the regulatory owner used instead. Uses N17, N40, N62, N67; AC-1 to AC-13; A2, A3; the Gate 5 attempt rows; every sign-off name in the cast. |
| [harbourgate-incident-postmortem.md](harbourgate-incident-postmortem.md) | [templates/operate/incident-postmortem.md](../templates/operate/incident-postmortem.md) | OPERATE event review, written in DELIVER, feeds Gate 6 | HG-INC-14 with a timeline from logs and chat, impact in numbers (5 h 40 min, 5,190 lines, £332,000), five contributing causes in systems language with no name in any of them, five things that worked, and six corrective actions each with a verification method. Uses N33, N34, N37, N41, N42, N69; A1 to A6; R3, R9, R14; F2; DEP-2; D-020, D-021. |
| [harbourgate-sunset-eol-plan.md](harbourgate-sunset-eol-plan.md) | [templates/operate/sunset-eol-plan.md](../templates/operate/sunset-eol-plan.md) | OPERATE, executes the consequence of Gate 6 | Executes D-024: retire the legacy payment layer, its two provider contracts and the contractor's wrapper by 2026-12-15, with the refund tail (BR-002, BR-009) inside the plan and the table-shape removal of 2027-03-31 explicitly outside it. Uses N50 to N55, N59, N60, N64 to N66; D-023 to D-025; BR-002, BR-009; DEP-4, DEP-7, DEP-8; I-5 to I-8. |
| [harbourgate-compliance-impact-assessment.md](harbourgate-compliance-impact-assessment.md) | [templates/operate/compliance-impact-assessment.md](../templates/operate/compliance-impact-assessment.md) | DEFINE and DELIVER, feeds Gate 2 and Gate 5; re-verified at sunset | Records that PCI DSS, the card schemes' rules, the market's strong customer authentication requirement and UK GDPR apply and the scoping fact for each, that no model is present so the regulated overlay did not fire and reg-gap-check was run anyway, that the DPIA for the fraud rules engine (I-9) was found required on the 2026-10-16 correction, and four gaps, G1 to G3 plus HG-INC-14, with owners. Signed by Anneliese Vogt and Hamid Qureshi on 2026-07-06; corrected 2026-10-16. Uses N55, N57, N58; G1 to G3, HG-INC-14; R8; I-1, I-5, I-7, I-9; N41, N42; DEP-7; D-023. |

## What this journey teaches

- **ADR (harbourgate-adr.md):** the rejected option has to be one somebody wanted. The wrapper over three providers was the engineers' first instinct, and the ADR names the condition that would reopen it, so a successor can reverse it intelligently instead of relitigating it.
- **System design:** on a brownfield product the constraints table is longer than the goals list, and that is correct. The legacy table shape and the per-provider flag are facts the design lives with, not choices it makes.
- **API contract:** the error rows are the contract. A 402 that must not be retried on the same card is the difference between BR-001 and a double authorisation, and the fraud team, not the API team, is who noticed the last time.
- **Integrations register:** the failure-behaviour column needs a noun a customer would recognise. "Retry" describes I-6's mechanism; "finance closes late and nobody is paged" is what its failure looked like.
- **Security architecture:** a score of 4 is a decision not to act, not an absence of risk. F2 was found, scored honestly, routed to a backlog nobody scheduled, and it produced the journey's only incident.
- **Observability:** thresholds are set before the first incident so that the incident can be measured against them. The one alert that did not exist, the 07:45 settlement-file page, is the one the incident needed.
- **NFR:** a number nobody agreed is still better than an adjective. The Marlowe baseline was an estimate from monthly statements with finance's name beside it, and it was enough to sign AC-3 against.
- **Business rules:** rules retire in public. BR-008 stayed in the register as retired, with the date and the reason, so the July behaviour and the June behaviour are both explicable.
- **Dependency register:** "requested" is a status, not a plan. DEP-2 sat there for eight weeks, and the corrective action A6 is the register learning to escalate on age rather than on mood.
- **Stakeholder map:** the person who can stop you is often not paying attention. Lena Baptiste had the store window and the per-shop rollback explained to her before the first kiosk cohort, not after.
- **Risk register:** the premortem found R1, scored it a medium, and it happened anyway. The register's job was to make the reversal cheap, and it did: D-017 did not have to rediscover the options.
- **Migration cutover plan:** a payment provider is not a database. There is no instant at which it has nothing in flight, so freeze-move-switch cannot work, and the plan says so in the "why that shape" row rather than pretending the weekend was never proposed.
- **Release readiness:** a condition is a thing the release may not proceed without, and a known issue is a thing it may. The runbook gap was raised as an issue and written down as a condition, which is the only reason it was met by 2026-07-10.
- **Incident postmortem:** the rehearsal that fails is the one worth running, and the incident it caused is written in systems language: a shared drop, a job that deletes on success, a scheduler nobody disabled, an alert that did not exist.
- **Sunset plan:** a shutdown is a launch in reverse. The refund tail, the contract notices and the certificate expiry set the dates, and the table shape that must outlive the path is named as staying, so nobody deletes it by tidiness.
- **Compliance impact assessment:** "the overlay did not fire" is an answer with a name on it. PCI DSS, the scheme rules and the data protection regime did apply, and the assessment says who holds each obligation rather than ticking a box that covers none of them.
