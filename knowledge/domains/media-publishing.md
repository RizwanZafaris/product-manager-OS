---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Media and publishing", "digital publishing", "news technology", "media-publishing"]
---
# Media and publishing

Three parties are never the same person here: the reader who consumes, the creator or newsroom that produces, and the advertiser who often pays for both. A feed-ranking or monetization change that helps one predictably taxes another, and the decision about which one to protect is usually made by default, by whichever team's metric sits on the dashboard. The distinctive fact that follows is that the product is a liability surface for speech it did not write. Platforms carry duties around what stays up, what comes down, and how fast, and those duties now come with real deadlines and real fines, not only reputational risk; the moderation queue is a compliance function wearing a product-team badge. The EU's Digital Services Act sets binding notice-and-action, transparency, and, for very large platforms, systemic-risk obligations well beyond the US's more permissive Section 230 baseline, so a moderation design built to the US bar under-builds for a European audience.

**Adjacent industries:** creator-economy tools (monetisation, tipping, subscriptions and brand-deal platforms) read this card with two duties added. A platform that pays creators is a payer with tax-information reporting duties (US Forms 1099-K and 1099-NEC, the EU's DAC7) and, if it holds funds between fans and creators, possible money-transmission exposure; read [Embedded finance and BaaS](embedded-finance-baas.md). Sponsored-content tooling carries FTC endorsement-disclosure duties. Podcasts read this card as written: open RSS distribution means the publisher controls neither the player nor the listener data, download counts measured to the IAB podcast measurement guidelines are the ad currency and easy to inflate, and host-read ads carry the same disclosure duties. As of 2026-09-11; verify and confirm with counsel.

## Questions a PM must ask

1. Who are we optimizing for in this specific feature: the reader's time, the creator's reach and pay, or the advertiser's yield? Name it; a feed or paywall change rarely serves all three, and the tradeoff should be a decision, not a byproduct.
2. What is our moderation and takedown obligation, by market? The DSA requires a notice-and-action mechanism, statements of reasons, and an internal complaint system, with added duties for very large platforms; the US baseline under Section 230 is different and more permissive.
3. Who owns copyright liability when a user or a model reproduces someone else's work? The US DMCA's notice-and-takedown safe harbor and the EU Copyright Directive's Article 17 are structured differently, and "we took it down when notified" satisfies one regime more completely than the other.
4. How does the paywall or subscription mechanic change what gets written? A metered or hard paywall changes headline incentives and, at scale, changes what a newsroom assigns.
5. What does a creator actually get paid, on what schedule, and can they see the calculation? A payout formula a creator cannot audit produces the same trust failure as an opaque ranking algorithm, aimed at your supply side.
6. What happens to advertiser trust when brand safety fails next to disputed or moderated content? Ad revenue can evaporate faster than any engagement metric moves, on one high-profile placement failure.
7. Whose data is this, for targeting and personalization, and what legal basis covers it? A reader is a data subject under GDPR-style regimes whether or not your business model treats them as a customer.
8. What is the plan for a coordinated abuse event, a disinformation push or a mass-reported pile-on? Volume-based abuse is a predictable, recurring event here, not a black swan.

## Gatekeepers

- **The EU Digital Services Act (Regulation (EU) 2022/2065).** Requires notice-and-action mechanisms, statements of reasons, internal complaint handling, and, for platforms designated very large, systemic-risk assessment and independent audit; duties phase by size and reach (verify your platform's designation status before relying on a specific tier).
- **Copyright regimes: the US DMCA and the EU Copyright Directive (Directive (EU) 2019/790), Article 17.** The DMCA's notice-and-takedown safe harbor protects a platform that responds to specific notices; Article 17 pushes certain platforms toward proactive licensing or filtering, a materially higher bar (verify current implementation in the specific member state).
- **National press and advertising self-regulators**, or statutory press regulators where they exist. Editorial-standards, correction, and native-advertising disclosure rules are enforced outside the courts and can still cost a platform its ad-network or distribution access.
- **Data-protection authorities.** GDPR and equivalent regimes govern ad-tech identifiers, tracking consent, and profiling; a reader who pays nothing is still a data subject with rights.
- **App-store and ad-network policy teams.** Gate distribution and monetization directly; a moderation failure or ad-fraud pattern can get an app pulled or a publisher deprioritized in programmatic auctions with little notice.
- **Trust and safety, internally.** Owns the line on what may be published, recommended, or monetized; overruling this gatekeeper for growth is how a platform ends up explaining itself to a regulator.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Engagement time or pageviews | Reader attention | Rises with outrage-optimized ranking exactly as trust and brand-safety concerns rise with it; read together or not at all |
| Subscriber conversion rate | Paywall effectiveness | Improves by loosening the metered-article count in ways that quietly cut ad impressions, moving the loss to another dashboard |
| Subscription churn | Whether the content is worth paying for | A monthly figure hides the renewal-date cliff; cohort by signup month or a cancellation wave reads as a random dip |
| Creator payout per thousand views | Whether the supply side is compensated fairly | An opaque formula can hold this flat while ad yield underneath it rises, and creators only discover the gap by comparing notes |
| Ad viewability or brand-safety score | Whether impressions are worth what advertisers pay | Vendor-reported figures use vendor-favorable definitions; reconcile against independent verification before trusting it |
| Moderation queue age | Whether harmful content is actually handled | A shrinking queue can mean faster action or quieter auto-approval of borderline reports; check the approval rate alongside speed |
| Notice-and-action compliance rate | Regulatory exposure under DSA-style regimes | Counts notices actioned, not notices that should have been filed; under-reporting scale under-counts the true obligation |
| Copyright takedown turnaround | DMCA or Article 17 exposure | A fast turnaround on request looks compliant while proactive detection, which some regimes now expect, stays at zero |
| Programmatic ad revenue per session | Monetization efficiency | Rises with ad density in ways that directly increase abandonment and viewability complaints the same metric never captures |

## Reading

- **The EU Digital Services Act (Regulation (EU) 2022/2065).** Read the notice-and-action and statement-of-reasons articles directly; most moderation-flow designs assume a lighter duty than the text sets.
- **The US Digital Millennium Copyright Act, section 512.** Read the counter-notice provisions too; a takedown flow with no counter-notice path is not actually implementing the statute.
- **The EU Copyright Directive (Directive (EU) 2019/790), Article 17.** Read it beside the DMCA to see how differently the two regimes assign responsibility for user-uploaded copyrighted content.
- **Section 230 of the US Communications Decency Act.** The baseline US intermediary-liability shield; read it to see how much more permissive it is than the DSA.
- **A major platform's own transparency report on content moderation.** Read one from your category for the real order of magnitude of moderation volume and appeal rates, numbers that rarely appear in a product spec.
- **Reporting on a significant ad-fraud or brand-safety scandal in programmatic advertising.** The mechanism is almost always automated bidding meeting a supply chain nobody audited, the recurring shape of this domain's monetization failures.

**Conductor overlay:** this domain sharpens DISCOVER-1 (name the person: reader, creator, and advertiser are three different answers, and a feature usually serves one at the others' expense), DEFINE-6 (out of scope: what the moderation and copyright process explicitly will not catch at launch, written down and read by the sponsor before it becomes a regulator's question), DESIGN-2 (integrations: ad exchanges and payment or subscription processors are third-party pipes with their own outage and fraud behavior), and OPERATE-8 (the counter-metric: engagement or ad yield can rise while moderation backlog, brand-safety incidents, or takedown exposure rise with it).

**Templates this bends:** [personas](../../templates/discovery/personas.md) (reader, creator, and advertiser get separate treatment, not one blended user), [business-rules](../../templates/definition/business-rules.md) (moderation and copyright takedown rules carry a regulatory clock, not a support-team judgment call), [integrations](../../templates/architecture/integrations.md) (ad exchanges and subscription processors carry fraud and outage behavior as first-class rows), and [metrics-review](../../templates/operate/metrics-review.md) (a moderation and brand-safety counter-metric sits beside growth numbers every review, not in a separate trust-and-safety deck).

**Filled in this repo:** [domain-media-publishing-business-rules.md](../../examples/domain-media-publishing-business-rules.md) fills the [business-rules](../../templates/definition/business-rules.md) template directly for this domain, for Thornfield Post: the notice-and-action rule cited to DSA Articles 16 and 17 with no invented hour count where the regulation sets none, the DMCA counter-notice restoration window (10 to 14 business days), a corrections rule under the publisher's editorial code, paywall meter rules, and comment-moderation escalation under the UK Online Safety Act, with the standards editor, not engineering, as the source of truth for moderation rules. For the other three bent templates, [sahulat-personas.md](../../examples/sahulat-personas.md) and [ledgerline-metrics-review.md](../../examples/ledgerline-metrics-review.md) remain the nearest reading for a multi-persona document and a counter-metric-beside-growth habit, though neither carries a reader, a creator, and an advertiser as opposed interests, or a moderation-queue-age counter-metric. [harbourgate-integrations.md](../../examples/harbourgate-integrations.md) shows the owner-SLA-failure-behaviour row shape an ad-exchange or subscription-processor row needs, though its rows carry chargeback risk, not takedown-notice risk.

**Worked example (ILLUSTRATIVE):** a business-rules row this card's notice-and-action question would add, for a fictional news platform, Thornfield Post, none of it real:

| ID | Rule statement (WHEN ... THEN ...) | Trigger point | Source of truth | Business owner | Exceptions | Enforced by | Test traceability |
|---|---|---|---|---|---|---|---|
| BR-014 | WHEN a notice under the EU Digital Services Act is submitted against a piece of content reachable from an EU IP range THEN the platform records a statement of reasons and either removes, restricts, or rejects the notice within the internally set target of 24 hours, whichever the assessment supports | Notice intake queue, EU jurisdiction flag set at ingestion | Regulation (EU) 2022/2065 (Digital Services Act), Articles 16 and 17 (verify current article numbering and any applicable timeline before relying) | Head of Trust and Safety | A notice flagged as manifestly unfounded at intake is logged but does not start the removal clock; the statement of reasons is still required | FR-092 (notice intake) | AC-31: a test notice submitted from an EU-tagged session produces a timestamped statement of reasons visible to the notifier within the target window |

This is the rule an ordinary support-ticket SLA would never produce on its own: the clock and the statement-of-reasons requirement come from a regulation the register's source-of-truth column has to name, not from a judgment call the moderation team is free to make case by case.
