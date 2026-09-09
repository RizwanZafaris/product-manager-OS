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
| [Developer tools and APIs](devtools-api.md) | Your users write code against you, and your interface is a contract | A breaking change is paid for by people who did not choose it; the deprecation notice is the product |
| [Marketing and advertising technology](martech-adtech.md) | You process data about people who are not your customers | Consent is a product surface; the identifier you depend on belongs to a platform vendor |
| [Cybersecurity and GRC](cybersecurity-grc.md) | You sell a control, an evidence trail, or an incident response | You are an attack surface with privileged access; the customer's reporting clock starts before they know what happened |
| [Marketplaces](marketplaces.md) | Two sides with opposed interests, and you take a cut of the match | Liquidity beats size; the better you match, the stronger the incentive to leave |
| [ERP and enterprise finance](erp.md) | Your product is the financial record, or the operations that feed it | An auditor can refuse to sign because of how you store a change; the famous failures were cutovers, not defects |
| [HR technology](hr-tech.md) | Your product decides who is hired, paid, promoted, scheduled or reviewed | Your customer carries the liability and cannot delegate it; the people it acts on are not your users |
| [Fintech](fintech.md) | Money moves, is stored, or is decided on by your product, and none of the financial-services rows below fits better | Pointer card: routes to the regulated module for a model that decides, and to the fourteen financial-services cards below for the rails and licences |
| [Hardware and IoT](hardware-iot.md) | You ship a physical device with firmware, a fleet and an update path | A bug is a recall; certification and the supply chain gate every launch |
| [Telecom](telecom.md) | You are a carrier, an MVNO, or you build network products | Numbering, interconnect and lawful duties are the product's floor; billing is where trust is lost |
| [Public sector and govtech](public-sector-govtech.md) | Government buys, runs or mandates your product | Procurement is the funnel; accessibility, records and identity are duties the buyer cannot waive |
| [Automotive and mobility](automotive-mobility.md) | Your software rides in a vehicle, or moves people and vehicles around a city | Functional safety and homologation decide the release date; the driver is a worker, a customer, or both |
| [Energy and utilities](energy-utilities.md) | You sell, meter, balance or charge energy under a regulated tariff | Outage duties and tariff rules are set by the regulator; demand response is a contract with the grid |
| [Manufacturing and industrial](manufacturing-industrial.md) | Your software runs on or beside the plant floor | A change to a safety-rated system is a validated change; OT is not IT and the plant does not reboot |
| [Agritech](agritech.md) | Your users grow, trade or finance crops and livestock, often smallholders | Weather and the harvest calendar set the roadmap; connectivity and trust decide adoption |
| [PropTech and real estate](proptech-real-estate.md) | You list, sell, manage or finance property | Fair-housing and disclosure duties reach your ranking and your ads; the transaction is a chain of gatekeepers |
| [Travel and hospitality](travel-hospitality.md) | You sell or run trips, rooms, seats or loyalty | Distribution is a negotiated channel; disruption handling and refunds are regulated promises |
| [Media and publishing](media-publishing.md) | You publish, subscribe, monetise or moderate content | The paywall and the ad stack pull in opposite directions; copyright and moderation duties never end |
| [LegalTech](legaltech.md) | Lawyers or their clients rely on your product for legal work | Privilege, professional conduct and unauthorised-practice rules are gatekeepers; an error is a malpractice claim |
| [Pharma and life sciences](pharma-life-sciences.md) | Your software touches trials, drug safety, or regulated manufacturing | Validated systems and audit trails are the requirement; the patient is far away and the inspector is not |
| [Retail in store](retail-in-store.md) | You run the counter, the shelf, the inventory or the loyalty programme of a physical store | The queue is the metric; a POS outage is a closed store |
| [Food delivery and quick commerce](food-delivery-quick-commerce.md) | You deliver meals or groceries on demand with couriers and dark stores | Unit economics per order and the courier's status as a worker decide the business; food safety is a duty |

### Financial services

The money sectors get their own table because they share one fact the general table does not: the licence to operate is held by someone with a veto, and every rail the product rides was built by a third party with its own rulebook. Pick the row whose licence and rail are yours; a product that spans two rows reads both.

| Domain | Pick it when | Essence |
|---|---|---|
| [Core banking](core-banking.md) | You hold deposits, run accounts and a ledger, and move money in and out for retail or SME customers | The ledger is the product and the cutover is the risk; a reconciliation break is a regulatory event |
| [Transaction banking](transaction-banking.md) | Corporates run cash, liquidity, bulk payments or trade finance through you | The treasurer buys certainty and cut-off times; a file that fails at 4 p.m. is a client lost |
| [Remittances](remittances.md) | You move money across borders for people or small businesses, corridor by corridor | A corridor is a licence, a rail, an FX spread and a payout network; each can close on you |
| [Payments acquiring](payments-acquiring.md) | You accept card or account payments for merchants, online or at the counter | Authorisation rate is the number merchants leave over; chargebacks and scheme fines arrive months later |
| [Card issuing](card-issuing.md) | You issue cards, run a card programme, or process on an issuer's behalf | The network's rules outrank your roadmap; disputes and tokenisation are where the cost hides |
| [Lending and credit](lending-credit.md) | You decide who gets credit, on what terms, and how it is collected | Every decision is a regulated decision about a person; collections is where the promise is tested |
| [Embedded finance and BaaS](embedded-finance-baas.md) | Another company offers accounts, payments or credit through you, or you through a sponsor | The licence belongs to someone else; when the sponsor pulls it, the product stops |
| [Wealth and investing](wealth-investing.md) | You hold, advise on or execute investments for retail or professional clients | Suitability and best execution are duties, not features; the client's loss is your file |
| [Capital markets](capital-markets.md) | You run a venue, market data, or post-trade clearing and settlement | Latency, fairness and surveillance are regulated properties; a settlement fail has a price per day |
| [Insurance](insurance.md) | You underwrite, distribute or settle claims on insurance, or embed it in another product | The claim is the product; pricing is regulated for fairness and reserves are regulated for solvency |
| [Crypto and digital assets](crypto-digital-assets.md) | You custody, exchange, issue or move digital assets | Custody is the liability; the travel rule and licensing decide which corridors exist at all |
| [RegTech, AML and KYC](regtech-aml-kyc.md) | You sell identity verification, screening or transaction monitoring to regulated firms | Your false negatives are the customer's enforcement action; your false positives are their operating cost |
| [Mobile money and wallets](mobile-money-wallets.md) | You run a wallet for people the banks did not reach, with agents, cash and feature phones | Cash-in cash-out is the network; the agent's float and the USSD session decide whether the product exists |
| [Islamic finance](islamic-finance.md) | Your products must be Shariah-compliant, or you serve customers who require it | The Shariah board is a gatekeeper with a veto; the contract structure is the product |

Fintech stays a pointer card on purpose. The part of its pack that concerns a model making a financial decision already exists as [the regulated module](../../modules/regulated/README.md), the material that seeded this repository, and the fourteen financial-services cards above carry the rest: the rails, the licences and the gatekeepers that a model does not change.

## How the Conductor uses this table

When a product's STATE.md records a Domain, any stage question that asks about gatekeepers or metrics should be answered with the named card open. Recording "none" is a valid answer and better than a guessed domain: a card applied to the wrong market sharpens the wrong questions.

## Graduation rule

A domain gets a card when its gatekeepers or metrics change what a stage question means, not before. A per-domain template pack (a healthtech PRD variant, an ecommerce launch plan) ships only when a card proves insufficient in real use, matching the rule the [knowledge index](../README.md) applies to method cards. Cards first, templates on evidence.
