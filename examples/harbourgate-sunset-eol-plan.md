---
layer: examples
stage: OPERATE
gate: 6
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Harbourgate Sunset / End-of-Life Plan"]
---
# Sunset / End-of-Life Plan: Harbourgate legacy payment path (Marlowe, Tidewater, the contractor's wrapper)

Fills [templates/operate/sunset-eol-plan.md](../templates/operate/sunset-eol-plan.md). Everything here is invented: Harbourgate is a fictional mid-market retailer, Kestrel, Marlowe and Tidewater are fictional payment providers, Quay is the fictional payment service that replaced the legacy path, every person is fictional, and every number, date and identifier is ILLUSTRATIVE, carried from the shared data sheet in the [Harbourgate journey](harbourgate-journey.md) rather than from any real payments stack. See the [examples index](README.md).

**Stage:** OPERATE (executes the legacy-retirement consequence of [Gate 6: outcomes verified, learn or sunset](../os/STAGE-GATES.md)'s PERSIST decision for Quay, D-024; Quay itself persists, and is not this file's subject)
**Knowledge:** [knowledge index](../knowledge/INDEX.md)
**Skill:** [decision-memo](../skills/decision-memo/SKILL.md) for the call itself; [gtm-launch-planner](../skills/gtm-launch-planner/SKILL.md) for the comms sequence

**Owner:** Ife Adeyemi, Product Manager · **Decision source:** D-024, Gate 6, 2026-10-14, in [the Harbourgate journey](harbourgate-journey.md#data-sheet-every-value-illustrative) (metrics review held 2026-10-09; this journey carries no separate metrics-review artifact, so Gate 6 is the decision record) · **Decided:** 2026-10-14
**Shutdown date (public):** 2026-12-15 · **Last updated:** 2026-10-16

## 1. The decision

- Rationale, two sentences: non-completion fell from 11.1% at entry (N5) to 7.4% at Gate 6 (N19), and every decline now carries provider and reason class, up from 0% of Marlowe declines at entry (N20), so the legacy path has no remaining function except cost (N53). D-024 itself reads: "Gate 6: PERSIST for Quay; retire the legacy path by 2026-12-15 with Ife Adeyemi as owner."
- Decider: Ife Adeyemi, Product Manager, with Rohan Iyer, Chief Financial Officer and sponsor, co-signing D-024 as budget owner. What would have reversed it: a Gate 6 review finding decline rates or non-completion worse than the entry baseline, which the 2026-09-08 to 2026-10-05 review window did not find (N18, N19).
- What this sunset frees up: £9,400 a month in legacy running cost (N53: Marlowe minimum £2,100, Tidewater minimum £1,650, legacy infrastructure £5,650); 0.4 FTE of on-call currently consumed by the legacy path, an engineering estimate (N54); and a reduction in PCI DSS assessment scope from 7 systems at entry to a target of 3 after sunset (N55), which DEP-7 books an assessor to confirm.
- Rejected: retain Marlowe as a warm standby acquirer to offset R4 (a Kestrel outage stopping every card payment). ADR-0003 (2026-04-09) rejected keeping either legacy provider at all, on operational risk; D-022 (2026-08-24) is the later decision that accepted R4 itself, with the kiosk fallback, the peak freeze and a quarterly review, rather than building any standby. Retaining Marlowe would have kept £2,100/month (N53), I-5's card-in-transit PCI scope (N55) and a second on-call surface, in exchange for a failover path whose own contract carries only a 99.5% SLA (N27).

## 2. Who is affected

| Segment | Count | Revenue or usage at stake | Contractual obligations (notice period, SLA) | Regulator notice needed |
|---|---|---|---|---|
| Customers with an order authorised on Marlowe or Tidewater who can still draw a refund or dispute through the provider portals (N52) | N59 counts 1,900 orders, but as "legacy-authorised orders inside the returns window at shutdown", the N50 90-day window, not the N52 portal window this row is defined against; that count does not size this row. [OPEN: a count against the N52 window is not on the data sheet; owner Ife Adeyemi] | Refund and dispute capability on those orders, not revenue | Harbourgate's own returns policy v9 sets a 90-day returns window from delivery (N50); the wind-down clause in both provider contracts keeps portal access open to 2027-06-15 (N52), which is the longer window and the one this segment is defined against | no |
| Marlowe, counterparty | 1 contract | £2,100/month minimum fee ends; card value through Marlowe was already at 0% since Marlowe cohort 3 reached 100% on 2026-07-20 (N71); its straddle set drained 2026-07-23; its routing flag was removed 2026-08-03 (N49) | 2019 contract, 90-day minimum termination notice (N51); notice sent 2026-09-14 for a 2026-12-15 end date, 92 days, a 2-day margin over the floor | no; commercial notice only, sent under DEP-8 |
| Tidewater, counterparty | 1 contract | £1,650/month minimum fee ends; no SLA clause existed to begin with (N28) | 2021 contract, 90-day minimum termination notice (N51); same 2026-09-14 notice, same 2026-12-15 end date | no; commercial notice only, sent under DEP-8 |
| Finance Operations (Priya Raman's team) | 1 team | Refund workflow changes from automated (BR-002) to manual portal (BR-009) for the tail | Internal only; process change effective 2026-11-16 | no |
| InfoSec / PCI DSS assessment scope (Hamid Qureshi) | 7 systems in scope at entry, target 3 after sunset (N55) | No revenue; assessment cost and audit burden | PCI DSS is an industry standard reaching Harbourgate as merchant of record through its acquiring contracts, not through a regulator; a revalidated scope and updated Attestation of Compliance are submitted to Kestrel, the remaining acquirer, after DEP-7's assessment; an external assessor was chosen by Hamid Qureshi as a G3 condition, not mandated by the scope change itself | no (no regulator; contractual revalidation) |
| Store associates and shop kiosks | 61 shops (N1), already on Kestrel since Tidewater cohort 3 (2026-08-17) | None; kiosks already migrated, this row exists so nobody assumes a second kiosk cutover is coming | None remaining; BR-004's fallback behaviour is unchanged by this plan | no |
| Reporting / Data engineering (Grace Mbeki) | 1 team | Reporting queries read the legacy table shape until DEP-4 completes; the table shape itself stays live until 2027-03-31 (N65, ADR-0002) regardless of DEP-4's date | Internal only; DEP-4 committed date 2027-02-27 | no |

- If any regulated obligation applies, run the [compliance impact assessment](../templates/operate/compliance-impact-assessment.md) before announcing anything: the Harbourgate compliance impact assessment covering PCI DSS, the card schemes' rules, the market's strong customer authentication requirement and UK GDPR was signed 2026-07-06, before the migration itself, and its gaps G1 to G3 are tracked to closure rather than reopened by this plan; G3 (PCI scope reduction not yet evidenced by an assessor) is exactly what DEP-7 closes. The assessment itself is due for re-verification before 2026-12-15 (see section 4).

## 3. Migration path

No customer migrates anything: every order-facing surface (web, app, all 61 kiosks) has run on Quay through Kestrel since 2026-09-07, three months before this shutdown date. What remains is a tail of legacy-authorised orders whose refund and dispute path still points at Marlowe or Tidewater until the portal wind-down closes, the counterparties themselves, and three internal segments that must each change something.

| Segment | Destination | What they must do | By when | Help offered (docs / tooling / humans) | Owner |
|---|---|---|---|---|---|
| Legacy-authorised orders still able to draw a refund or dispute | Refund or dispute via Marlowe/Tidewater's wind-down portal (manual, BR-009) | Nothing; the customer-facing return flow is unchanged, Finance Operations does the manual step behind it | Through 2026-11-15 automated (BR-002); 2026-11-16 through 2027-06-15 manual via the portal (BR-009, N52), a volume falling from 41 refunds a day in September 2026 to 12 a day by 2026-10-15 (N60), which is why a manual step within 5 working days is sustainable | Runbook update for the manual refund and dispute step, owned by Priya Raman | Priya Raman, Head of Finance Operations |
| Marlowe (counterparty) | Contract ends; no replacement, Kestrel already carries the volume | Acknowledge termination notice; keep the wind-down portal reachable through 2027-06-15 (N52) | 2026-12-15 | Termination notice sent under DEP-8, 2026-09-14 | Anneliese Vogt, Legal Counsel |
| Tidewater (counterparty) | Contract ends; no replacement, Kestrel already carries the volume | Acknowledge termination notice; keep the wind-down portal reachable through 2027-06-15 (N52); no action needed on the client certificate (N66, expires 2027-02-03, after the contract itself has ended) | 2026-12-15 | Termination notice sent under DEP-8, 2026-09-14 | Anneliese Vogt, Legal Counsel |
| Finance Operations | Manual refund and dispute portal process (BR-009) | Switch the runbook from the automated BR-002 step to the manual portal step; nothing customer-facing changes | Runbook switch by 2026-11-16 | Runbook update owned by Priya Raman | Priya Raman, Head of Finance Operations |
| InfoSec / PCI DSS scope | Revalidated scope on Kestrel alone | Complete DEP-7's assessment; submit the revalidated scope and updated AOC to Kestrel | 2026-12-15 | External assessor booked under DEP-7 | Hamid Qureshi, Information Security Lead |
| Store associates and shop kiosks | Already on Kestrel | No action; migration completed 2026-08-17 (Tidewater cohort 3), this row exists only so nobody schedules a second cutover | 2026-08-17 (completed, Tidewater cohort 3) | not applicable | Lena Baptiste, Head of Store Operations |
| Reporting reading the legacy table shape | Quay's own rows, already written since ADR-0002 | Migrate the reporting queries themselves; the table shape stays live regardless, until 2027-03-31 (N65, ADR-0002) | 2027-02-27 (DEP-4 committed date); table shape removal is 2027-03-31 and is not this plan's step | Data engineering support, Grace Mbeki | Grace Mbeki, Data Engineering Lead |

- Data export: none required; Quay writes the same table shape the legacy path did (ADR-0002), so no customer-facing data moves. The wrapper's own log files, which carry masked PAN and cardholder name (F1; new lines scrubbed from 2026-05-08, existing files still hold the data until deletion), are deleted rather than exported, by 2027-01-15 (N58). The wrapper host stays up, off traffic, solely to hold these files until that deletion; its own infrastructure teardown (section 6) follows the 2027-01-15 log deletion, not the 2026-12-15 contract end.
- Pricing or refund handling for prepaid customers: not applicable; orders are authorised at checkout and captured on dispatch (BR-006), there is no prepaid balance to settle.

## 4. Timeline

| Stage | Date | Owner | Done |
|---|---|---|---|
| Internal announce and support briefing | 2026-10-19 | Ife Adeyemi; Callum Fraser briefs Support | pending |
| Public announce | not applicable; no customer-facing product changes, so no public announcement is made | Ife Adeyemi | not applicable |
| New signups / sales stop | not applicable; Marlowe and Tidewater were never customer-selectable, routing was internal | not applicable | not applicable |
| Feature freeze (legacy path, security fixes only) | 2026-10-19 | Tomasz Wierzbicki, Engineering Lead | pending |
| Read-only / rollback-warm only: legacy path serves no refunds, stays warm only for rollback (R10) | 2026-11-16 to 2026-12-15 | Tomasz Wierzbicki | pending |
| Compliance impact assessment re-verified for the sunset | before 2026-12-15 | Anneliese Vogt, Hamid Qureshi; closes G3 via DEP-7 | pending |
| Peak change freeze (Quay and every routing flag, rollbacks excepted) | 2026-11-13 to 2026-12-04 (N64) | Tomasz Wierzbicki | pending |
| Legacy refund automation (BR-002) ends, manual portal (BR-009) begins | 2026-11-15 / 2026-11-16, verified pre-freeze | Priya Raman | pending |
| Shutdown: Marlowe and Tidewater contracts end, I-5 through I-8 credentials revoked | 2026-12-15 | Ife Adeyemi; Anneliese Vogt confirms the contracts; Tomasz Wierzbicki confirms credentials | pending |
| Post-sunset check | 2027-01-14 | Ife Adeyemi | pending |
| Data deletion complete (wrapper logs, N58) | 2027-01-15 | Bea Lindqvist (job owner); verified by Hamid Qureshi | pending |
| Reporting migrated off the legacy table shape | 2027-02-27 (DEP-4) | Grace Mbeki | pending |
| Legacy table shape removal (not this plan's step) | Stays; removal 2027-03-31 under ADR-0002 is a data-model change owned outside this plan | Grace Mbeki (system design and dependency register) | not applicable |

The shutdown sits after the peak change freeze by design: 2026-12-15 is eleven days after the freeze lifts on 2026-12-04 (N64), so a contract-termination cutover is never attempted during the freeze window that exists to protect peak trading.

The BR-002 to BR-009 refund switchover on 2026-11-15/16 falls inside that freeze window without breaking it: the switch is date-driven behaviour shipped before the freeze begins (the API contract returns 422 Unprocessable Content, code legacy_refund_window_closed, after 2026-11-15), and Priya Raman verifies it pre-freeze, before 2026-11-13, rather than changing anything in Quay or a routing flag during the freeze itself.

The Tidewater client certificate expires 2027-02-03 (N66), which caps how far the shutdown could slip without renewing a certificate on a wrapper nobody owned; the 2026-12-15 date leaves 50 days of margin against that expiry.

## 5. Comms cascade

| Audience | Message owner | Channel | Date | Sent |
|---|---|---|---|---|
| Engineering and on-call | Tomasz Wierzbicki | Team channel | 2026-10-19 | pending |
| Support (Callum Fraser's team) | Callum Fraser | Briefing plus written runbook | 2026-10-19 | pending |
| Finance Operations | Priya Raman | Team meeting plus runbook update | 2026-10-19 | pending |
| Data engineering (Grace Mbeki) | Grace Mbeki | Team channel plus DEP-4 tracking | 2026-10-19 | pending |
| Marlowe (counterparty) | Anneliese Vogt | Formal termination notice | 2026-09-14 | sent (DEP-8) |
| Tidewater (counterparty) | Anneliese Vogt | Formal termination notice | 2026-09-14 | sent (DEP-8) |
| InfoSec (Hamid Qureshi) and the external PCI assessor | Hamid Qureshi | Assessment booking, DEP-7 | committed 2026-11-20, needed by 2026-12-15 | pending |
| Rohan Iyer, CFO and sponsor | Ife Adeyemi | Written update alongside D-024 | 2026-10-14 | sent |

Every internal message in this cascade states the 2026-12-15 shutdown date, the BR-002 to BR-009 refund switch, and the 2027-01-15 wrapper log deletion date, per the rule that every message carries the shutdown date, the migration path and the data deadline.

No public or customer channel appears in this cascade: every order-facing surface has been on Quay since 2026-09-07, so there is nothing for a customer to notice and nothing to explain to one. This is unlike a product sunset, and the exit gate below accepts an "internal only" reading of section 5 for that reason.

## 6. Decommission steps

- [ ] Billing stopped and final invoices handled: Priya Raman, against Marlowe's and Tidewater's final statements after 2026-12-15
- [ ] Integrations and API consumers notified and disconnected (see the [integrations register](harbourgate-integrations.md)): I-5 (Marlowe authorisation API key), I-6 (Marlowe settlement file SFTP key), I-7 (Tidewater client certificate, through the contractor's wrapper) and I-8 (Tidewater settlement file SFTP key) all revoked 2026-12-15; owner Tomasz Wierzbicki, verified by the credentials being revoked, not merely the flags removed (the last routing flags, Marlowe's and Tidewater's, were already removed on 2026-08-03 and 2026-08-31 respectively; BR-007's two-person change control lapsed with the last flag on 2026-09-21). This box excludes Finance Operations' own portal logins, which stay active for BR-009 refunds and disputes through 2027-06-15 (N52), since those are human logins, not API credentials
- [ ] Quay's legacy adapter and checkout-pay's own payment layer removed: Bea Lindqvist for the legacy adapter, Tomasz Wierzbicki for the checkout-pay payment layer, after 2026-12-15; verified by code removal and by the infrastructure line below reading zero
- [ ] Infrastructure torn down, recurring costs at zero: Tomasz Wierzbicki, verified against the £9,400/month legacy running cost (N53) reading zero on the finance close after 2027-01-15, once the wrapper host (kept live only to hold the log files until their deletion) is decommissioned alongside the log deletion
- [ ] Monitoring and alerts retired, on-call rotation updated: Bea Lindqvist, the settlement-file-absent alert (N34, A3) narrowed to Kestrel only; the 0.4 FTE legacy on-call share (N54, estimate) removed from the rotation
- [ ] Public docs, marketing pages and app store listings removed or archived: not applicable, owner of record Ife Adeyemi; the legacy providers were never named in any customer-facing surface
- [ ] Contracts and vendor commitments closed out: Anneliese Vogt, both contracts formally closed 2026-12-15, wind-down portal access confirmed reachable through 2027-06-15 (N52)

## 7. Post-sunset check

- On 2027-01-14 (30 days after shutdown): the Marlowe (£2,100/month) and Tidewater (£1,650/month) contract fees confirmed ended against N53, and the 2026-12-15 credential revocations (section 6) confirmed still in effect, by Ife Adeyemi. This date also carries D-025.
- On 2027-01-15: wrapper log file deletion verified (N58) by Hamid Qureshi, against the deletion job Bea Lindqvist owns as the wrapper's caretaker; this is also when the wrapper host is decommissioned, so the full £9,400/month legacy running cost (N53), including the £5,650 infrastructure line, is confirmed at zero only on the first finance close after this date, by Tomasz Wierzbicki (section 6).
- What this product taught us, one paragraph, logged in the [decision log](../templates/execution/decision-log.md): D-025, target 2027-01-14, owner Ife Adeyemi. Drafted here ahead of that filing: a legacy integration with no named owner is not a dormant risk but an active one, as finding F1 (the wrapper's log files holding plain-text card and cardholder data, found 2026-04-08) showed before Bea Lindqvist was named caretaker on 2026-04-24; and a migration rehearsal that fails against production-shaped data, as rehearsal 1 did on 2026-06-13, is worth six weeks on the completion date (N43, engineering estimate), since it is the rehearsal that finds the failure before a customer does, at the cost HG-INC-14 records.

## What this file does not cover

- The removal of the legacy table shape itself (2027-03-31, ADR-0002) sits in the [system design](harbourgate-system-design.md) and [dependency register](harbourgate-dependency-register.md) as DEP-4's downstream consequence; this plan tracks DEP-4 to its 2027-02-27 committed date and stops there, since the table's removal is a data-model change, not a sunset decommission step.
- The refund and dispute tail is executed in section 3; the rules themselves (BR-002 through 2026-11-15, BR-009 from 2026-11-16 through the 2027-06-15 portal wind-down, N52) are owned and changed only in the [business rules register](harbourgate-business-rules.md), not re-litigated here.
- Whether Kestrel becoming a single point of failure (R4) should be revisited is out of scope for a sunset plan; D-022 already accepted R4 by name on 2026-08-24 with a 2027-01-31 revisit date that belongs to the risk register, not to this decommission.

## Exit gate

This plan is done when:

- [x] Every affected segment has a migration row with a date and an owner. Section 2 and section 3 list the same seven segments: the refund and dispute tail (Priya Raman, portal access through 2027-06-15), both counterparties (Anneliese Vogt, 2026-12-15), Finance Operations (Priya Raman, 2026-11-16 runbook switch), PCI scope (Hamid Qureshi, 2026-12-15), stores (Lena Baptiste, already migrated 2026-08-17), and reporting (Grace Mbeki, 2027-02-27); the "no customer migrates anything" fact is stated rather than left implicit, since every order-facing surface moved to Quay three months before this plan's shutdown date.
- [x] The timeline respects every notice period in section 2. The 2026-09-14 termination notices give 92 days against Marlowe's and Tidewater's 90-day minimum (N51), a 2-day margin; the 2026-12-15 shutdown sits after the 2026-11-13 to 2026-12-04 peak freeze (N64), eleven days after it lifts, rather than inside it.
- [x] Support is briefed before the public announcement. There is no public announcement (section 5), so this box is satisfied by the internal briefing sequence instead: Callum Fraser's team is briefed 2026-10-19, ahead of the 2026-12-15 shutdown.
- [x] Every decommission box has a named owner. Priya Raman (billing), Tomasz Wierzbicki (integrations, the checkout-pay layer, infrastructure), Bea Lindqvist (the legacy adapter, monitoring) and Anneliese Vogt (contracts) hold the six live boxes in section 6; the one not-applicable box (public docs) states why and names Ife Adeyemi as its owner of record.
- [x] The post-sunset check has a date and a person. 2027-01-14, Ife Adeyemi, carrying D-025 as its output and confirming the contract fees ended and the credential revocations held; the wrapper log deletion has its own date, 2027-01-15, owned by Hamid Qureshi (verification) and Bea Lindqvist (the job), and the zero-infrastructure-cost confirmation follows it, on the first finance close after 2027-01-15, owned by Tomasz Wierzbicki.

Signed: Ife Adeyemi, Product Manager, 2026-10-16. Rohan Iyer, Chief Financial Officer and sponsor, co-signed the underlying decision at D-024, 2026-10-14; his signature covers the budget consequence (the £9,400/month released, N53), not this execution plan, which is Ife Adeyemi's alone to run. See the [Harbourgate journey](harbourgate-journey.md) for how this file's D-023 to D-025 fit the wider migration, and the [dependency register](harbourgate-dependency-register.md) for DEP-4, DEP-7 and DEP-8 in full.
