---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Telecom", "Telecommunications", "carriers", "MVNO", "telecom"]
---
# Telecom

A telecom product sits on top of two networks built for different purposes at different times: a global one, held together by interconnect agreements among carriers who might also be competitors, and a national one, licensed by a regulator with the power to decide whether you may transmit at all. The distinctive fact of this domain is that basic functions, placing a call, sending a message, moving a number between providers, work only because a chain of agreements with other carriers holds. You can build a flawless app and still fail a customer because a partner three networks away dropped the call.

The second distinctive fact is that telecom carries statutory duties most software never touches: lawful interception, emergency-call routing, and numbering are obligations attached to the license, not features you choose to build. A billing error here is not a bug ticket; it is a regulatory complaint with its own clock.

**Adjacent industries:** communications platforms (SMS, voice and messaging APIs, UCaaS and contact-centre platforms) read this card, because the gatekeepers are still carriers and numbering rules; they now stand between your customer and the recipient. In the US, application-to-person messaging on long codes needs 10DLC brand and campaign registration, and carriers filter unregistered or complained-about traffic; India requires DLT registration of senders and templates; WhatsApp Business messages need template approval under Meta's policy. Any of these can stop delivery without an error your customer sees, so split delivery rate by carrier and route instead of blending it. Consent law (the TCPA in the US) makes a customer's careless send partly the platform's problem. Voice products carry STIR/SHAKEN caller authentication and VoIP emergency-calling duties (Kari's Law, and dispatchable location under RAY BAUM'S Act). As of 2026-09-11; verify and confirm with counsel.

## Questions a PM must ask

1. Which license or authorization covers this product (network operator, MVNO, reseller, VoIP provider), and what obligations came bundled with it? The license, not the roadmap, sets the floor of what you must support.
2. Which interconnect and roaming partners does this feature depend on, and what happens when one is slow, wrong, or down? A call is only as reliable as the least reliable carrier in the path.
3. Does this feature touch a number: porting, allocation, or presentation? Numbering is a national resource administered under rules you did not write and cannot renegotiate per feature.
4. Can this product fulfil a lawful-intercept or data-retention request today, in every market it operates in, on the timeline the law requires? "We'll add that later" is not an answer a regulator or a court accepts.
5. What happens to an emergency call or message when this feature is active? Anything touching the calling path has to prove it does not degrade emergency routing.
6. Where does call-detail and location data flow, who can request it, and under what legal process? Call records are some of the most sensitive personal data a company holds, and retention rules vary sharply by country.
7. How does billing reconcile with network-layer usage, and what happens when they disagree? A subscriber's complaint is truth until your systems can prove otherwise.
8. What is the fallback when the primary network path fails: another carrier, a cached route, a manual process? A network-unavailable screen is a support cost multiplied across every affected subscriber.

## Gatekeepers

- **The national telecom regulator.** Bodies such as Ofcom in the UK, the FCC in the US, or Pakistan's PTA license spectrum and services, set consumer-protection and billing rules, and can suspend a license over a breach a product team never saw coming.
- **The numbering administrator.** Whoever holds the national numbering plan, often the regulator itself, allocates ranges and sets portability rules; a product that assumes numbers are yours to manage has misread who owns them.
- **Law-enforcement and lawful-intercept authorities.** Regimes such as the UK's Investigatory Powers Act or the US CALEA statute require a technical capability to intercept traffic on request; building this in after launch costs far more than designing for it.
- **Interconnect and roaming partners.** Other carriers are simultaneously your suppliers, your customers, and sometimes your competitors; a peering or settlement dispute can silently degrade service with no bug behind it.
- **The data-protection authority.** Call-detail records and location data are personal data everywhere the GDPR or an equivalent regime applies; the EU's own data-retention directive was struck down by its top court for being disproportionate, and national retention rules have stayed unsettled since.
- **GSMA and device or SIM certification schemes.** Standards such as embedded-SIM provisioning gate whether a device can even be activated on a network, independent of anything your product does.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| ARPU (average revenue per user) | Revenue efficiency per subscriber | Blended ARPU hides a shift toward heavy discounting or a richer prepaid mix, and bundling lets revenue move between products without the number showing it |
| Churn rate | Subscriber retention | Voluntary churn and non-payment disconnection are tracked differently, and a subscriber who ports out mid-cycle can vanish before billing notices |
| Network availability | Reliability of the network | A national average hides the rural cell or single exchange down for days; the SLA is usually measured at the core, not the last link to the handset |
| Call and message completion rate | End-to-end delivery success | A failure on one interconnect partner dilutes into a national average that looks fine everywhere else |
| Number-porting completion time | Whether switching providers actually works | Measuring from request accepted, rather than request made, makes a regulator's own target easier to hit on paper |
| Lawful-intercept fulfillment time | Whether a statutory duty is met | Meeting an internal SLA does not mean the data delivered was complete or matched the right subscriber |
| Billing dispute rate | Billing accuracy | A low rate can mean accurate billing, or that customers, especially low-usage prepaid ones, do not bother disputing a small overcharge |
| Fraud loss rate (SIM-swap, interconnect bypass) | Exposure to telecom-specific fraud | Reported loss is bounded by what your own detection systems catch, so a quiet quarter can mean better fraud or a blind detector |
| Regulatory filing on-time rate | Compliance discipline | Filed on time is not filed correctly; regulators often flag data-quality problems well after a filing was accepted |

## Reading

- **ITU-T Recommendation E.164**, the international public telecommunication numbering plan, the reference underneath every number your product dials, ports, or displays.
- **The EU's European Electronic Communications Code**, Directive (EU) 2018/1972, the rulebook behind switching rights, numbering, and universal service across the EU market.
- **The UK Investigatory Powers Act 2016**, setting out technical capability notices for lawful interception. Read it even outside the UK; most national intercept regimes borrow the same shape.
- **The US Communications Assistance for Law Enforcement Act (CALEA)**, the American equivalent duty, useful as a contrast in how differently two major markets write the same requirement.
- **Digital Rights Ireland**, Court of Justice of the European Union, C-293/12, 2014 (verify the exact date before relying), which struck down the EU's data-retention directive as disproportionate. The standing lesson that "the law requires us to keep this" has an expiry date of its own.
- **GSMA's eSIM specification (SGP.22)**, the industry standard deciding whether a device can be remotely provisioned onto your network at all.

**Conductor overlay:** this domain sharpens DESIGN-2 (integrations are interconnect, roaming, and peering partners you do not control), DEFINE-5 (how requirements fail: numbering and lawful-intercept edge cases are the requirements, not exceptions to them), DELIVER-6 (regulated overlay drift, as license conditions and intercept obligations change under a live network), and OPERATE-4 (cost to run includes interconnect settlement, not only infrastructure spend).

**Templates this bends:** [integrations](../../templates/architecture/integrations.md) (interconnect and roaming partners carry SLAs and failure behavior as first-class rows), [compliance-impact-assessment](../../templates/operate/compliance-impact-assessment.md) (lawful-intercept and data-retention duties per market), [sla-slo-definition](../../templates/delivery/sla-slo-definition.md) (network availability defined the way the regulator and the wholesale contract measure it), and [nfr](../../templates/definition/nfr.md) (numbering and portability performance as numbered requirements).

**Filled in this repo:** [domain-telecom-nfr.md](../../examples/domain-telecom-nfr.md) fills the [nfr](../../templates/definition/nfr.md) template directly for this domain, for Fennwick Mobile: port-out completion time measured against the regulator's switching process and the portability clearing data, emergency-call availability with handset location (Advanced Mobile Location), lawful-intercept fulfilment within the statutory clock, billing accuracy under the regulator's metering and billing conditions, and regulator outage notification, with the host-network dependency named in every availability row. [harbourgate-sla-slo-definition.md](../../examples/harbourgate-sla-slo-definition.md) exists and fills the sla-slo-definition template this card also bends, correcting the earlier claim that no filled example exists; its availability and error-budget mechanics are the nearest reading, though it is not telecom. For the other two bent templates, [harbourgate-integrations.md](../../examples/harbourgate-integrations.md) and [harbourgate-compliance-impact-assessment.md](../../examples/harbourgate-compliance-impact-assessment.md) remain the nearest reading, though neither registers a carrier or evidences CALEA or the Investigatory Powers Act.

**Worked example (ILLUSTRATIVE):** A numbering row, in the shape of `templates/definition/nfr.md` section 2, for a fictional MVNO, Fennwick Mobile. Every name, owner and number below is invented.

| Requirement | Target (number) or owner for the number | Measured how and where | Verified by |
|---|---|---|---|
| Mobile number port-out completion time, donor confirms | 95% within 1 working day of donor confirmation, per PTA's portability determination (verify the current threshold before relying) | Portability gateway timestamp, from donor confirmation to first successful call on the recipient network, not from the customer's original request | Weekly cross-check against the regulator's own portability dashboard; owner: Ayesha Noor, Regulatory Affairs Lead |
| Lawful-intercept fulfilment time | 100% of valid requests actioned within the statutory window; owner: Ayesha Noor, baseline due 2026 Q4 | Intercept-request log matched to the statutory clock's start, not to internal ticket-open time | Quarterly attestation to the licensing regulator |

This is what changes: a generic availability row becomes two rows a non-telecom NFR would never carry, each one tied to a duty the license imposes rather than a target the team chose.
