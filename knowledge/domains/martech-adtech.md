---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["martech", "adtech", "marketing technology", "advertising technology", "martech-adtech"]
---
# Marketing and advertising technology

The distinctive fact is that the person whose data moves through your product is not your customer, is not present, and did not choose you. Everything downstream of that follows: consent is a product surface rather than a legal footnote, the identifier your model depends on can be removed by a browser vendor or a mobile platform without consulting you, and measurement is a claim about causation that your own numbers cannot settle. The second distinctive fact is that this domain's supply chain is made of other companies' liabilities. A publisher, a consent platform, an exchange and a buyer each carry their own obligations, and participation in an industry framework does not discharge any of them.

## Questions a PM must ask

1. What is the lawful basis for each purpose, and is the signal for it actually reaching the systems that act on it? Under the EU framework, consent is encoded and passed downstream, and a purpose acted on without the matching signal is processing without a basis, whatever the banner said.
2. Which identifier does this feature assume exists, and who can remove it? Safari and Firefox block third-party cookies by default, Apple's App Tracking Transparency put the mobile advertising identifier behind an opt-in prompt with famously low acceptance, and Chrome's Privacy Sandbox replaces cross-site tracking with aggregated and noised APIs. A roadmap built on an identifier is a roadmap held by a platform vendor.
3. Is this attribution or is it correlation with a good interface? Last-touch attribution assigns credit by recency, which is a rule rather than a finding, and the number it produces will be defended in a budget meeting as though it were measured.
4. Can the user withdraw as easily as they agreed, and does withdrawal propagate to every downstream system that already received the signal?
5. What is retained, for how long, and who can answer that question without opening a database?
6. Does this feature create a new joint controllership, and has anyone written down who is responsible for what?
7. What does this look like to a regulator reading it cold, rather than to a practitioner who has normalised it?
8. What happens to the product when the identifier goes away entirely, given that in this domain it always does?

## Gatekeepers

- **Data protection authorities.** The most consequential gatekeeper because they act after launch. The long-running Belgian proceeding against IAB Europe's Transparency and Consent Framework, resolved at the Brussels Market Court on 14 May 2025, confirmed that the consent string itself qualifies as personal data and that framework participation does not by itself make downstream real-time bidding lawful. Each participant owns its own processing.
- **Browser and mobile platform vendors.** Not regulators and more decisive in practice. They can remove the mechanism your product depends on with a release note, and there is no appeal.
- **The publisher's own privacy and revenue teams.** Hold the tag on the page. They will not deploy something that risks their consent posture or their inventory, whatever the commercial agreement says.
- **The advertiser's brand safety and procurement functions.** Own where the money is allowed to appear, which is a constraint on placement rather than a preference.
- **The consent management platform.** A dependency with veto power over your signal: if it does not carry a purpose or a vendor, you do not have permission, and you will discover this in production.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Attributed conversions | Which touchpoint the model credits | It is a rule applied to a log, not a measurement of cause. Change the window or the model and the answer changes while reality does not |
| Return on ad spend | Efficiency of the channel | Absorbs everything the model cannot see, so it flatters channels that intercept demand that already existed. Incrementality testing is the only honest check, and it costs money by design |
| Consent rate | Share of users who agreed | Depends far more on banner design than on user intent, which makes it a metric you can improve by making refusal harder. Regulators read that as a defect rather than an optimisation |
| Match rate | Share of records joined to an identity | Falls silently as platforms remove identifiers, so a stable series usually means the definition changed |
| Reach and impressions | Scale | Counts opportunities to be seen, not being seen. Viewability, fraud and bot traffic all live inside this number |
| Click-through rate | Engagement | Optimising it selects for curiosity and misclicks. It is the easiest metric in the domain to move and among the least connected to outcome |
| Cost per acquisition | Unit efficiency | Uses the same attribution model as the numerator above, so it inherits every assumption in it and presents them as arithmetic |
| Audience segment size | Targetability | Grows with looser matching. A larger segment usually means a weaker one |
| Deliverability | Whether messages arrive | Sending less to more engaged recipients improves it while shrinking the programme, so it rewards retreat |

## Reading

- **The Brussels Market Court ruling on IAB Europe, 14 May 2025.** Read it for two holdings a PM has to design around: the consent string is personal data, and participation in the framework does not make each participant's downstream processing lawful. It also narrowed the framework body's own controllership, which is what pushes responsibility back onto every publisher and vendor individually.
- **The Transparency and Consent Framework technical specification.** Read the string format and the propagation model rather than the policy summary. Understanding what is encoded, and what is not, tells you exactly which product decisions are unsupported by the signal you receive.
- **Apple's App Tracking Transparency and Google's Privacy Sandbox documentation.** Read both as statements of what measurement will be permitted to look like: aggregated, delayed and noised. Products designed for user-level truth are being asked to work with population-level estimates, and that is a product problem before it is an analytics one.

**Conductor overlay:** this domain sharpens DISCOVER-1 (the data subject is a third party who is not your user and cannot be interviewed as one), DEFINE-2 (consent and purpose limitation are functional requirements), DESIGN-2 (identity and consent propagation are the architecture), and OPERATE-1 (measurement claims need an incrementality design before they are quoted to anyone who allocates budget).

**Templates this bends:** [privacy-impact-assessment](../../templates/architecture/privacy-impact-assessment.md) (routine here rather than exceptional), [experiment-brief](../../templates/operate/experiment-brief.md) (a holdout is the only defence against attributing what would have happened anyway), [metrics-dictionary](../../templates/operate/metrics-dictionary.md) (each metric has to record its attribution model and window, or two teams will report different numbers for the same word), and [integrations](../../templates/architecture/integrations.md) (the supply chain is the product, and each hop carries its own obligations).
