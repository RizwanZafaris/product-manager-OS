---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Domain Index"]
---
# Domain Index

The knowledge cards one level up answer WHY a method exists. This layer answers a different question: what changes about the operating loop when your product lives in a specific market. A domain card does not add stages or gates. It sharpens the questions the loop already asks, names the gatekeepers who can stop a launch that engineering cannot see, and replaces generic metrics with the ones practitioners in that market are actually judged on.

Every card carries the same five parts: the questions a PM must ask before trusting any plan, the gatekeepers with the power to block, the metrics that matter and how each one lies, one or two canonical readings in this repository's own words, and two closing lines that wire the card into the rest of the OS: which Conductor questions the domain sharpens, and which templates it bends.

Skip this layer entirely when none of the rows below describe your product. A domain card for a market you do not operate in is trivia, and filling your head with another market's gatekeepers is how a plan grows sections nobody will ever read.

## Pick your domain

| Domain | Pick it when | Essence |
|---|---|---|
| [Ecommerce](ecommerce.md) | You sell or broker physical or digital goods for money per order | Margin lives in a waterfall, not a percentage; the tax man arrives without a warehouse |
| [Streaming and OTT](streaming-ott.md) | You deliver licensed or original video or audio on subscription or ads | The content you rent defines what you can build; churn is the whole business |
| [Gaming](gaming.md) | You ship a game or game-like product with a session loop | Retention loops pay the bills; certification and loot-box law guard the door |
| [B2B SaaS](saas-b2b.md) | You sell software on contract or subscription to companies | The buyer, the user, and the blocker are three different people |
| [Consumer social](consumer-social.md) | Your product's value comes from users seeing other users' content | Growth is a loop you design; moderation is a cost you carry forever |
| [Healthtech](healthtech.md) | Your product touches patients, clinicians, or health data | Intended use decides whether you built software or a medical device |
| [Edtech](edtech.md) | Your product teaches, and a school or district might pay for it | Engagement is easy to show and efficacy is not; the district buys, the teacher decides |
| [Logistics](logistics.md) | You move physical things and promise when they arrive | The last mile eats the margin; exceptions are the product |
| [AI products](ai-products.md) | The product itself contains a model whose output users rely on | Wrong answers are a cost of goods sold; evals are your acceptance criteria |
| [Fintech](fintech.md) | Money moves, is stored, or is decided on by your product | Pointer card only: fintech's domain pack is the regulated module |

Fintech is the exception in this table on purpose. Its pack already exists as [the regulated module](../../modules/regulated/README.md), the material that seeded this repository, so its card routes there and duplicates nothing.

## How the Conductor uses this table

When a product's STATE.md records a Domain, any stage question that asks about gatekeepers or metrics should be answered with the named card open. Recording "none" is a valid answer and better than a guessed domain: a card applied to the wrong market sharpens the wrong questions.

## Graduation rule

A domain gets a card when its gatekeepers or metrics change what a stage question means, not before. A per-domain template pack (a healthtech PRD variant, an ecommerce launch plan) ships only when a card proves insufficient in real use, matching the rule the [knowledge index](../README.md) applies to method cards. Cards first, templates on evidence.
