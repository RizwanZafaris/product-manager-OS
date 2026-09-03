---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["cybersecurity", "security products", "GRC", "compliance tooling", "cybersecurity-grc"]
---
# Cybersecurity and GRC

The distinctive fact is that your product is bought because of a fear and judged during an incident, which means the demo and the failure mode are separated by months and the thing that sells is not the thing that matters. The second is that a security product is itself an attack surface with privileged access to everything it protects, so a defect here is not a bug, it is a breach at every customer at once. The third is timing: incident reporting deadlines in this domain run from awareness or determination rather than from the end of an investigation, so a customer's clock starts while they still do not know what happened, and your product either helps them meet that clock or it does not.

## Questions a PM must ask

1. What clock does this customer live on when something goes wrong? A US public company files a Form 8-K within four business days of determining an incident is material, with the determination itself due without unreasonable delay. An EU essential entity under NIS2 owes an early warning within twenty four hours of awareness and a fuller notification at seventy two. A financial entity under DORA can owe an initial notification within four hours of classifying an incident as major. GDPR runs seventy two hours from awareness. None of these wait for your investigation to finish.
2. Does the product produce the artifact the clock demands, in the form the regulator or auditor expects, or does it produce a dashboard someone must then translate under time pressure?
3. What access does this feature require, and what happens if that access is abused or the product is compromised? Agents, connectors and privileged integrations are the shortest path an attacker can take into every one of your customers.
4. Which certification is the entry price for the market you are selling into, and how long does obtaining it actually take? A SOC 2 Type II requires an observation window before a report exists, and an authorisation for US federal use is a programme rather than a purchase.
5. What is the false positive cost? An alerting product's real constraint is analyst attention, and a detection nobody can triage is a detection that trains people to ignore the console.
6. How do you handle a vulnerability in your own product: who can report it, on what timeline do you fix and disclose, and is that written down before you need it?
7. Does this feature claim to establish compliance, or to produce evidence of it? The first is a claim you cannot support, and buyers who repeat it back to their auditor will find that out at your expense.
8. What does the product do when it is degraded? A security control that fails open is a control that is absent exactly when it is being tested.

## Gatekeepers

- **The CISO and the security architecture review.** The buyer and the blocker in one person. Cares about the blast radius of your agent, your tenancy model and your own breach history.
- **The external auditor and the assessor.** Decide whether your evidence is accepted. What matters is whether the artifact is complete, attributable and tamper-evident, not whether the interface is good.
- **Procurement and third-party risk.** Owns the questionnaire, the insurance requirement and the subprocessor list. In this domain the questionnaire is longer and the tolerance for a missing certification is lower than anywhere else.
- **The regulator, indirectly.** You are rarely regulated; your customer is, and their obligations become your requirements. SEC disclosure rules, NIS2 and DORA reach you through the customer's need to comply.
- **Your own security team.** The one gatekeeper you can overrule and should not. In a domain where you are the attack surface, the internal review is the last honest gate before the customer's.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Mean time to detect | Speed of discovery | Averaged over incidents you eventually found. The ones you never detected are absent from the denominator, which is the population you actually care about |
| Mean time to respond or remediate | Speed of containment | Improves by closing tickets rather than fixing causes, and a re-opened incident often restarts the clock as a new one |
| Alerts raised | Coverage | Rewards noise. More alerts with the same analyst headcount is a reduction in real coverage |
| False positive rate | Signal quality | Only counts what someone bothered to triage and label. Alerts closed in bulk are recorded as neither true nor false |
| Vulnerabilities found | Product effectiveness | Counts findings, not risk. A scanner tuned for volume outperforms one tuned for exploitability on this metric and underperforms it in reality |
| Patch or remediation coverage | Exposure closed | Denominators are chosen locally. Coverage of assets you know about says nothing about the assets you do not |
| Compliance posture score | Readiness | A weighted average of controls you selected. It moves when the framework mapping changes and reads as though the organisation got safer |
| Time to certification | Sales unblocking | Measures the audit, not the security. A clean report attests that stated controls operated over a window, which is a narrower claim than buyers hear |
| Customers breached while using the product | The only outcome metric | Almost never collected, heavily confounded, and the closest thing this domain has to truth. Its absence from most dashboards is itself the finding |

## Reading

- **SEC final rule 33-11216 on cybersecurity risk management, strategy, governance and incident disclosure**, adopted 26 July 2023, effective 5 September 2023, with Form 8-K Item 1.05 compliance from 18 December 2023 and an additional period for smaller reporting companies. Read Item 1.05 directly. The four business days run from the materiality determination rather than from discovery, and the determination must be made without unreasonable delay, which is the sentence that actually governs how a customer will use your product.
- **NIS2 Article 23 and DORA Article 19 reporting timelines.** Read them beside the SEC rule to see how differently the same incident is counted across regimes. A multinational customer is on several of these clocks at once, and reconciling them is a product opportunity and a support burden.
- **A published coordinated vulnerability disclosure policy, any credible one.** Read it as a template for your own. The product decision is the timeline and who may report; publishing it before you need it is the difference between a researcher who works with you and one who publishes first.

**Conductor overlay:** this domain sharpens DISCOVER-3 (the evidence is incident history, and it is the hardest evidence in any domain to obtain because disclosing it costs the source something), DEFINE-3 (retention, attribution and tamper-evidence are requirements drawn from a framework rather than from preference), DESIGN-1 (your own threat model is a first-class design artifact because you are the attack surface), and DELIVER-3 (readiness includes your disclosure policy and your own incident response, not only the customer's).

**Templates this bends:** [security-architecture](../../templates/architecture/security-architecture.md) (about your product as a target, not only as a control), [nfr](../../templates/definition/nfr.md) (reporting deadlines become hard requirements with named regimes behind them), [failure-scenarios](../../templates/delivery/failure-scenarios.md) (fail-open versus fail-closed is the central decision and belongs written down), and [incident-postmortem](../../templates/operate/incident-postmortem.md) (used for your own incidents, which your customers will read).
