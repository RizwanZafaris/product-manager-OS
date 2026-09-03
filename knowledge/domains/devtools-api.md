---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["devtools", "developer tools", "API products", "platform", "devtools-api"]
---
# Developer tools, APIs and platforms

The distinctive fact here is that your users write code against you, so your interface is a contract rather than a screen, and the cost of changing it is paid by people who are not in the room. Every other domain can redesign a page and call it an improvement. Change a field name here and you break builds at companies whose names you do not know, on a schedule you do not control. The second distinctive fact is that your buyer is frequently not your user and your user is frequently not the beneficiary: an engineer adopts, a platform team permits, and a finance owner pays, and losing any of the three loses the account.

## Questions a PM must ask

1. Is this change breaking? A change is breaking if any correct client written against the documented contract stops working, and that includes stricter validation, a narrowed enum, a changed default, a new required field, and a rate limit lowered.
2. What is the deprecation period, who announced it, and where does a developer find it without asking you? Google's Maps Platform terms commit to roughly one year of continued operation after a deprecation announcement, with experimental and preview surfaces explicitly excluded. Publishing the policy is the product decision; the timeline is the consequence.
3. Which surfaces are covered by that promise and which are not? A lifecycle with named stages, experimental, preview, general availability, legacy, deprecated, decommissioned, is what lets you move fast on one surface without breaking trust on another. Without it every endpoint carries the strictest implied guarantee.
4. Who is the adopter, who is the approver, and who is the payer? An SDK an engineer loves and a security team will not permit is not adopted.
5. What does the first hour look like for someone who has never seen this? Time to first successful call is the only funnel step you fully control, and it is where most of the loss happens.
6. What happens at the boundary: rate limits, quota exhaustion, partial failure, retries? The error path is the API's real user experience, because the happy path is written once and the error path is hit forever.
7. If you deprecate this, can you see who is still calling it, and can you reach them? A deprecation you cannot measure is an outage you have scheduled without knowing the date.
8. What did the pricing change do to the smallest customers? Repricing a platform is a breaking change with no migration guide.

## Gatekeepers

- **The platform or architecture review.** Decides what may be introduced as a dependency. Cares about licence, supply-chain provenance, maintenance signal and exit cost, not about your feature list.
- **Security and third-party risk.** Owns SSO, scopes, token handling, tenancy isolation and the questionnaire. An SDK that requests broad scopes is a review that does not end.
- **The developer community itself.** The one gatekeeper with no formal authority and the most practical power. Trust here is an asset accumulated slowly and spent in a single announcement, and the public record of platform repricings and API restrictions is a record of that asset being spent.
- **Legal, on the terms of service.** What clients may do with your data and output is a product constraint written by someone else, and it changes what integrations are even possible.
- **Your own release process.** The versioning policy is a gate you impose on yourself. If the policy is unwritten, the gate does not exist and the next breaking change ships by accident.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Time to first successful call | Whether onboarding works | Measured from account creation it hides the hours spent before that, in documentation, provisioning and approval, which is where most abandonment happens |
| API calls or requests per period | Traffic | Says nothing about value or breadth. One noisy poller and one deep integration look identical, and a retry storm looks like growth |
| Registered developers | Reach | Counts accounts, not integrations. Signups after a conference are the most reliably meaningless number in this domain |
| Integrations in production | Real adoption | Definitions drift. Set the bar at sustained traffic from a distinct client over a period, or it becomes a count of experiments |
| Endpoint or SDK version distribution | Migration progress before a decommission | Aggregates hide the tail, and the tail is where the outage will be. Read it per customer, not as a percentage |
| Error rate | Reliability | Blends client mistakes with your defects. Split by status class: a rising rate of client errors is usually a documentation defect wearing a 4xx |
| Uptime against the service level agreement | Availability | A monthly average absorbs the outage on the customer's launch day. Exclusions for maintenance and dependencies can make the contractual number unlike the experienced one |
| Documentation page views | Interest | High views on one page usually mean it is confusing, not popular |
| Support tickets per integration | Friction | Falls when developers give up and stop asking. Read it beside retention, never alone |

## Reading

- **Google Maps Platform deprecation policy and launch stages.** Worth reading as a specimen rather than for the product: it states a deprecation period, names the lifecycle stages, and explicitly excludes experimental and preview surfaces from the promise. That combination is the thing to copy, and it is what allows a platform to keep moving without repricing trust.
- **Any large platform repricing or access restriction, read afterwards.** The pattern repeats: a pricing or access change lands with a short window, an ecosystem that built on assumed continuity reacts, and the platform absorbs a reputational cost far larger than the revenue in dispute. The product lesson is that migration cost falls on people who did not choose it, so the notice period is the product.
- **Semantic versioning, and where it stops helping.** A version number communicates intent between maintainers. It does not tell you who is affected, and it cannot substitute for telemetry on which clients call what.

**Conductor overlay:** this domain sharpens DISCOVER-1 (name the adopter, the approver and the payer separately), DEFINE-1 (the contract is the artifact, so the interface specification is the requirement rather than a design detail), DESIGN-3 (versioning, deprecation and the error contract are architecture), and OPERATE-3 (a deprecation is a delivery programme with named customers, not an announcement).

**Templates this bends:** [api-contract](../../templates/architecture/api-contract.md) (the primary artifact of this domain), [nfr](../../templates/definition/nfr.md) (rate limits, quotas and the service level are requirements with numbers, not aspirations), [sla-slo-definition](../../templates/delivery/sla-slo-definition.md) (what is excluded from the measurement matters more than the target), and [migration-cutover-plan](../../templates/delivery/migration-cutover-plan.md) (used for the customers' migration rather than your own).
