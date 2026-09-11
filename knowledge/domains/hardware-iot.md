---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Hardware and IoT", "IoT", "connected devices", "embedded hardware", "hardware-iot"]
---
# Hardware and IoT

Software fails forward: you ship a fix and the failure is over. A connected device fails in someone's kitchen, barn, or substation, and the fix travels through a radio link you do not control before it changes anything. Shipping is not the finish line here. A unit that leaves the factory keeps costing you, in support calls, warranty claims, and security patches, for as long as it stays plugged in, and a device with no funded update path is a liability the day it ships, not the day it breaks.

Certification and connectivity are also gates you cross before you have a product at all. A feature a software team would ship on Tuesday needs a fresh radio-compliance report, a component months out on allocation, or a carrier's certification before one unit reaches a customer. Plan around the test lab and the fab, not the sprint.

**Adjacent industries:** robotics reads this card and adds the robot safety standards that bound features: ISO 10218 for industrial robots, ISO/TS 15066 for collaborative operation, whose force and speed limits decide what a cobot may do near a person, and ISO 13482 for personal-care robots; autonomy in shared spaces raises the handoff and override question in [Automotive and mobility](automotive-mobility.md). Semiconductor and EDA product work reads this card with the release gate moved earlier: tape-out is irreversible and very expensive, so roadmaps commit years ahead, and revenue arrives through design wins at device makers on multi-year cycles (practitioner estimate: 18 to 36 months). US export controls on advanced computing items and the Entity List decide which customers and markets exist at all; export control is covered in [Aerospace and defence](aerospace-defence.md). As of 2026-09-11; verify and confirm with counsel.

## Questions a PM must ask

1. What is the device's expected field life, and who pays for security updates in year six, after the team that built it has moved on? No funded end-of-life plan means a recall waiting for a slow news day.
2. Which regulatory regime applies to this exact combination of radio, power, and claimed use, in each market it ships to? Certification is per market and per hardware revision.
3. What does the device do when connectivity is lost for a day, a week, a season? Offline behavior is a requirement, not a fallback, wherever the network does not reliably reach.
4. Who can push firmware to this fleet, how is it signed, and can an update roll back if it bricks units? No rollback path means a single point of failure for the whole install base.
5. What is the bill of materials' single-source exposure, and what happens to the roadmap if one component goes on allocation? A spec assuming infinite chip supply is a plan for a market that no longer exists.
6. What data does the device collect, where does it go, and can the answer change after a customer has installed it? A privacy-policy update cannot rewrite what a sensor already recorded.
7. Does the device fail loud or fail quiet? A sensor that stops reporting instead of alarming, like a leak detector gone silent, causes the worst incidents, because nobody knows to call support.
8. What triggers a recall instead of a routine over-the-air fix, and who has authority to call it? The gap between patching and notifying a regulator is where liability concentrates.

## Gatekeepers

- **Radio-equipment certification bodies and notified bodies.** Every radio inside the device, Wi-Fi, Bluetooth, or cellular, needs authorization before sale: FCC equipment authorization in the US, and in the EU conformity assessment under the Radio Equipment Directive, which the manufacturer may carry out as internal production control when the harmonised standards are fully applied and which needs a notified body only on the other assessment routes or where those standards are not fully applied; the directive's delegated cybersecurity requirements are becoming mandatory for connected products (verify the current compliance date before relying on it).
- **National product-security regulators.** The UK's Product Security and Telecommunications Infrastructure Act bans default and universal passwords and requires a published vulnerability-disclosure policy, enforced by the Office for Product Safety and Standards; California's IoT security law imposes a comparable duty.
- **Market-surveillance authorities under the EU Cyber Resilience Act.** Products with digital elements sold into the EU carry security-by-design and vulnerability-reporting duties for the support period promised at sale.
- **Carrier and interoperability certification programs.** A cellular module cannot attach to a network without the carrier's own certification; a data plan that fails this gate never reaches the field.
- **Consumer product-safety regulators.** A national safety regulator, such as the US Consumer Product Safety Commission, can compel a fleet-wide recall independent of any over-the-air plan already announced.
- **Test houses and safety-mark bodies.** Underwriters Laboratories, TUV, and similar labs gate the safety marks, and increasingly the IoT security marks built on standards like ETSI EN 303 645, that buyers require before listing a product.
- **Customs and supply-chain due-diligence regimes.** Import compliance, including the EU's conflict-minerals regulation covering tin, tantalum, tungsten, and gold, can hold a shipment at a border regardless of how finished the product is.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Field failure rate (RMA rate) | Real-world reliability versus the lab number | Counts only units that come back; a device that fails quiet, or gets discarded, never enters the numerator |
| OTA update success rate | Whether the fleet is receiving fixes | Retried successes count the same as first-try ones, and a bricked device usually cannot report its own failure |
| Fleet patch coverage | Security exposure across the install base | Eligible for an update is not the same as running it; an offline device is invisible to the metric, not counted against it |
| Time to patch a disclosed vulnerability | Speed of the security response | The mean hides a long tail of intermittently connected devices that take months, usually the ones attackers find first |
| Mean time between failures, lab versus field | Whether the design tolerance matches reality | Lab MTBF runs in a controlled chamber; heat, dust, humidity, and a customer's wiring are not in the model |
| Certification cycle time | Speed to market per hardware revision | Counted from test submission, not the earlier date a late spec change forced a re-spin |
| Warranty cost per unit shipped | Economics of the install base | Reserve accounting can defer a cost to a later quarter, flattering the quarter a defect surfaces in |
| Bricking rate after an update | Safety of the OTA pipeline | Understated by construction: a bricked device typically cannot phone home to report it, so the number is a floor |
| Single-source component exposure | Supply-chain risk | Looks fine until the one supplier has an allocation event, then it explains the whole roadmap slip at once |
| Device connectivity rate | Fleet health | Online is self-reported; a unit stuck in a boot loop that still pings the network can register as healthy |

## Reading

- **ETSI EN 303 645**, the European baseline for consumer IoT cybersecurity: no default passwords, a published vulnerability-disclosure policy, and a stated minimum security-update period at sale. Read it before drafting your own requirements.
- **The EU Cyber Resilience Act**, placing security-by-design, vulnerability handling, and incident reporting for products with digital elements into EU law. Read the scope carve-outs closely; a product you assume is exempt often is not.
- **The EU Radio Equipment Directive** and its delegated act on cybersecurity requirements for internet-connected radio equipment, the instrument turning "we should probably encrypt that" into a certification blocker.
- **The UK Product Security and Telecommunications Infrastructure Act 2022**, with guidance from the Office for Product Safety and Standards, specific on what "no default passwords" requires in practice.
- **California's IoT security law (SB-327)**, effective 2020, an early US state law requiring reasonable security features, including unique preprogrammed passwords.
- **The Mirai botnet, 2016.** Default credentials on ordinary cameras and routers built a botnet that disrupted major internet services through a DNS provider. Every "it's just a light bulb" argument dies here.
- **NIST SP 800-213 and the NISTIR 8259 series**, US federal guidance on IoT device cybersecurity baselines, a checklist for what a secure device implements.

**Conductor overlay:** this domain sharpens DESIGN-2 (integrations now include certification bodies, carriers, and contract manufacturers, each with its own lead time), DESIGN-6 (seeing it misbehave means fleet telemetry from devices that may be offline exactly when it matters), BUILD-3 (failure rehearsal has to include a bricked-fleet scenario, not only a service outage), DELIVER-6 (a certification held today can lapse under a regulation whose delegated requirements are still phasing in), and OPERATE-4 (cost to run includes warranty and patch support for every unit still in the field, not only the ones sold this quarter).

**Templates this bends:** [nfr](../../templates/definition/nfr.md) (environmental tolerance, power budget, and connectivity assumptions become numbered requirements, not narrative), [integrations](../../templates/architecture/integrations.md) (certification bodies, carriers, and contract manufacturers get rows with lead times and failure behavior), [failure-scenarios](../../templates/delivery/failure-scenarios.md) (bricked-fleet and fail-quiet sensor scenarios sit beside the usual service outages), and [release-readiness](../../templates/delivery/release-readiness.md) (certification and safety-mark sign-off become go or no-go rows, not launch-week paperwork).

**Filled in this repo:** [domain-hardware-iot-nfr.md](../../examples/domain-hardware-iot-nfr.md) fills the [nfr](../../templates/definition/nfr.md) template directly for this domain, for Cistern Sentry: a fail-loud requirement (the device alarms locally when it loses connectivity rather than going silent), battery life at the reporting interval, FCC Part 15 and EU Radio Equipment Directive cybersecurity radio certification, signed OTA updates with staged rings and brick recovery, the field temperature and humidity envelope, UK PSTI Act requirements, and EU Cyber Resilience Act vulnerability reporting, with one untested low-battery field condition left open with an owner. For the other three bent templates, [harbourgate-integrations.md](../../examples/harbourgate-integrations.md) and [harbourgate-release-readiness.md](../../examples/harbourgate-release-readiness.md) remain the nearest reading for the third-party-dependency and phased GO shape, though neither carries a certification body, carrier, or radio sign-off row. [harbourgate-failure-scenarios.md](../../examples/harbourgate-failure-scenarios.md) exists but is a payments outage set, not a fleet or sensor scenario.

**Worked example (ILLUSTRATIVE):** a filled NFR row for a fictional connected leak detector, "Cistern Sentry," following the [nfr](../../templates/definition/nfr.md) shape used in [harbourgate-nfr.md](../../examples/harbourgate-nfr.md):

| Requirement | Target or owner | Measured how and where | Verified by |
|---|---|---|---|
| The device alarms locally (audible + app push) within 90 seconds of losing its Wi-Fi or Zigbee connection to the hub, rather than going silent, so a connectivity loss cannot be mistaken for a dry, safe basement | 90 s, measured from last successful heartbeat to local alarm trigger (target, NFR-14) | Bench test, 40 units, connection killed at hub; p95 alarm latency logged against the 90 s target | Bench test log, 2026-08-11: met at bench (p95 = 61 s); field validation pending on a unit with a battery below 20%, where the radio's transmit-power fallback has not yet been tested against the alarm's own power draw |

A generic NFR row states an uptime or latency target for a service you run; this one specifies fail-loud behavior for the exact failure this sector's questions call out (a sensor that stops reporting instead of alarming), and ties the "met" status to a condition the bench test has not yet covered, low battery, rather than declaring the requirement closed.
