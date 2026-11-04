---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["templates/execution/backlog.md", "templates/execution/decision-log.md", "templates/planning/partner-integration-brief.md"]
method: "knowledge/crossing-the-chasm.md"
aliases: ["Enterprise request triage", "enterprise-request-triage"]
---
# Enterprise request triage

No single originator. Weighting pipeline revenue by deal-stage probability is ordinary sales-forecasting practice, and scoring a request against strategic fit and effort is the move the [RICE scoring sheet](rice-scoring-sheet.md) makes with different inputs. The hinge scale, the one-customer test and the four-outcome decision rule are this repository's own, drawn from the out-of-segment deal tell in the [Crossing the Chasm card](../../knowledge/crossing-the-chasm.md). Explained here in this repository's own words.

## What it is for

In a company that sells to other companies, a large share of feature requests arrive attached to a deal: an account executive needs it to close, a customer success manager needs it to renew, and both arrive with a number and a date. The number is real and the pressure is legitimate, which is exactly why these requests skip the queue unless something stops them. This sheet turns each one into a row with stated arithmetic: how much revenue actually hinges on it, how many accounts share the underlying problem, whether it fits the strategy, and what it costs to build and carry. A fixed rule then sends it to one of four outcomes: build into core, configure, partner, or decline with a written answer. The sheet does not rank what it admits; a request that earns "build" enters the [backlog](../../templates/execution/backlog.md) and competes there on [RICE](rice-scoring-sheet.md) like everything else.

## Run it when

- A request arrives from sales or customer success carrying an account name, a contract value, and a date, and the backlog's sales intake row says it stays in the CRM until it is a product problem
- Two or more open deals are said to depend on the same capability, and nobody has checked whether the deals actually hinge on it
- A renewal is at risk and the account has put a feature in writing as the condition
- Quarterly, over every deal-attached request still open, so the declines are written down and the build rows are re-scored against the current pipeline

**Skip it when:** the request has no contract attached (a self-serve user's idea is feedback, and it goes to the [feedback program](../../templates/operate/feedback-program.md) or [feedback synthesis](../../skills/feedback-synthesis/SKILL.md)); the ask is a document rather than a feature, such as a SOC 2 report or a data processing agreement, which goes to security or legal; or it is a defect, which goes to the support and severity process. Scoring a missing PDF of a certificate against strategic fit is a ceremony with arithmetic in it.

## Inputs you need first

- The open requests, each restated as the buyer's problem rather than the solution they proposed: "approvals must follow our spend bands per department", not "add seven approval levels"
- For each requesting account: pipeline value or renewal value, stage or health band, and the artifact that shows the deal depends on the request, from the CRM and the account team
- Measured stage-to-close rates from the CRM, if they exist, and health-band loss rates from customer success
- The product strategy's where-to-play and not-doing lines, from the [product strategy](../../templates/planning/product-strategy.md), and the current key results from the [OKR sheet](../../templates/planning/okrs.md)
- Evidence from accounts that did not ask: support tags, [evidence notes](../../templates/discovery/evidence-note.md) from interviews, and losses in the [win-loss review](../../templates/operate/win-loss-review.md)
- A build estimate and an annual carrying cost from the people who would do the work, per the [estimation sheet](../execution/estimation-sheet.md)
- The roadmap's Now column, for the hurdle in step 4

## The worksheet

**Step 1: one row per underlying problem.** Merge asks that are the same problem in different words; a "SAML" request and a "log in with our identity provider" request are one row. Count accounts by contracting parent entity, never by subsidiary, business unit, or contact, because three business units of one bank are one customer for every purpose this sheet has.

| ID | Problem, in the buyer's words | Ask type (capability / configuration / integration / deployment model) | Source (deal / renewal / QBR / ticket) | Raised by, on |
|---|---|---|---|---|
| [R1] | | | | [name], [YYYY-MM-DD] |

**Step 2: revenue that hinges on it.** One line per requesting account. For a pipeline account, value is the deal's annual contract value and p is the probability the deal closes. For an installed account, value is its annual recurring revenue and p is the probability of losing or shrinking the renewal. In both cases h is how much of that outcome actually depends on this request.

e = value x p x h, per account. E = the sum of e over every requesting account.

| Probability p | Pipeline | Renewal |
|---|---|---|
| Use first | The CRM's measured stage-to-close rate for this stage | Customer success's measured loss rate for this health band |
| Placeholder only if nothing is measured, and labeled as such in the row | discovery 0.1, solution validated 0.25, proposal 0.5, negotiation 0.75 | healthy 0.1, watch 0.25, at risk 0.5 |

| Hinge h | Rule |
|---|---|
| 1.0 | Written: an RFP mandatory item, a contract or order-form clause, a security questionnaire item, or the buyer's written renewal condition, linked in the row |
| 0.5 | Named by the buyer, not the rep, as one of their top three criteria, in a call note or an email |
| 0.2 | Mentioned, or asserted by the account team with no buyer artifact |
| 0 | The deal is already lost or closed, or the rep's own forecast note says it closes without this |

| Request | Account (parent) | Pipeline or renewal | Value | p | Source of p | h | Hinge artifact | e |
|---|---|---|---|---|---|---|---|---|
| [R1] | [account] | | [annual amount] | | [measured / placeholder] | [1.0 / 0.5 / 0.2 / 0] | [link] | [value x p x h] |

**Step 3: breadth and the one-customer test.** N_req is the number of distinct requesting parents. N_ev is the number of accounts in the strategy's target segment that did not ask but show the same problem, each with its evidence. C is concentration: the largest single e divided by E.

The request is flagged ONE-CUSTOMER when N_req = 1, or C is 0.6 or more, unless N_ev is 3 or more. A flagged request cannot be built into core, whatever its yield.

| Request | N_req | N_ev, with evidence | Largest e | E | C = largest e / E | One-customer flag |
|---|---|---|---|---|---|---|
| [R1] | | [n: ticket tags, notes, losses] | | | | [yes / no] |

**Step 4: fit, cost, and yield.** Fit F scores the request against the strategy, citing the line it rests on.

| Fit F | Rule |
|---|---|
| 3 | Serves the strategy's target segment and moves a current key result |
| 2 | Serves the target segment; no current key result |
| 1 | Serves an adjacent segment the strategy names as a later move |
| 0 | Outside where-to-play, or contradicts a not-doing line |

Cost is annualized over a stated horizon H in years, so a cheap build with a heavy support tail is not mistaken for a cheap request: K = build person-months / H + carrying person-months per year. Yield Y = E / K, in revenue per person-month per year.

The hurdle Y* is what the capacity would earn if this request did not take it: the yield of the lowest-ranked item in the roadmap's Now column, computed the same way. Where Now items carry no revenue figure, use the floor Y* = annual recurring revenue / research and development person-months per year, and write that the floor was used. The floor is the average, not the margin, so it is generous to the request; the Now-column hurdle is the honest one.

| Request | F | Strategy line cited | Build (pm) | Carry (pm per year) | K = build / H + carry | Y = E / K | Y* (and which hurdle) |
|---|---|---|---|---|---|---|---|
| [R1] | [0 to 3] | | | | [arithmetic shown] | [arithmetic shown] | |

**Step 5: two tests that need no arithmetic.**

- **Configure test.** Passes only if all three hold: the problem is met by an existing setting, template, role, or rule, or by a new general setting offered to every account on the plan; it costs 0.5 person-months or less; and it adds no code path that runs for one account only. A per-account branch is a fork, not a configuration.
- **Partner test.** Passes if the problem is an integration with, or a capability of, a system that a partner already sells or maintains, or could build on an extension point every account can use, such as the public API or webhooks.

**Step 6: the decision rule.** Apply in order; the first rule that matches decides.

1. **F = 0:** decline with a written answer, or partner if the partner test passes. Never build or configure.
2. **Configure test passes:** configure. No yield needed.
3. **One-customer flag:** partner if the partner test passes and the account will fund the partner's work; otherwise decline with a written answer that names what would reopen it (N_req + N_ev reaching 3).
4. **Partner test passes:** partner, written into a [partner integration brief](../../templates/planning/partner-integration-brief.md). Any change to core is limited to a general extension point.
5. **F is 2 or more, Y is at least Y*, and N_req + N_ev is 3 or more:** build into core. The row enters the backlog with this sheet attached; no date is promised to any account until the item is ranked and in Now.
6. **Anything else:** decline with a written answer.

**The written answer.** Sent to the account team within [n] working days of intake, logged in the [decision log](../../templates/execution/decision-log.md), and short enough for the account team to forward unedited:

> We will not build [request] in [period]. What we heard: [the problem, in the buyer's words]. Why: [the one rule that fired, in plain words]. What you can do instead: [configuration, workaround, or partner]. What would change our answer: [the trigger, such as two more accounts with the same problem].

## Reading the result

- **The highest-yield row lands outside core.** This is the sheet working, not failing. A request one logo wants, at a high value, is the most expensive kind to build, because the carrying cost is paid for every account forever and the revenue comes from one.
- **A build row's yield sits within about 20 percent of the hurdle.** Treat it as a tie, because E rests on probabilities and estimates with wider error than that gap; let RICE settle it in the backlog rather than letting this sheet pretend to precision.
- **Most of E rests on h = 0.2.** The demand is the account team's belief, not the buyer's. Go back for the artifact before scoring again; a request that cannot produce one at 0.5 or above is usually a negotiating position.
- **N_ev is large and N_req is small.** The problem is broad and the sales motion has not surfaced it. That is a discovery finding, worth an [evidence note](../../templates/discovery/evidence-note.md) of its own, whatever this row decides.
- **The same account appears in a third of the rows.** Check C across the whole sheet, not only per request: one account steering the roadmap through many small asks is the one-customer trap in instalments.

## ILLUSTRATIVE example

Invented. Marram is a fictional purchase-approval product sold to mid-market finance teams. Its strategy's target segment is mid-market finance teams with more than one department buying; its not-doing list includes single-tenant and on-premise deployments. Annual recurring revenue 21,000,000; research and development 45 people, 540 person-months a year; Now items carry no revenue figure, so the floor is used: Y* = 21,000,000 / 540 = about 38,900 per person-month. Horizon H = 2 years. Every figure is ILLUSTRATIVE.

**R1, approval chains by spend band per department** (existing setting allows three levels). Four accounts:

| Account | Type | Value | p | h | e |
|---|---|---|---|---|---|
| A1 | Pipeline, proposal | 110,000 | 0.5 | 0.5 | 110,000 x 0.5 x 0.5 = 27,500 |
| A2 | Pipeline, solution validated | 80,000 | 0.25 | 1.0 | 80,000 x 0.25 x 1.0 = 20,000 |
| A3 | Renewal, watch | 150,000 | 0.25 | 1.0 | 150,000 x 0.25 x 1.0 = 37,500 |
| A4 | Renewal, healthy | 60,000 | 0.1 | 0.5 | 60,000 x 0.1 x 0.5 = 3,000 |

E = 27,500 + 20,000 + 37,500 + 3,000 = 88,000. N_req = 4; N_ev = 5 (support tickets tagged "approval workaround" from five other target-segment accounts). C = 37,500 / 88,000 = 0.43, not flagged. F = 3 (target segment; moves the key result on multi-department adoption). Build 3 pm, carry 0.5 pm a year: K = 3 / 2 + 0.5 = 2.0. Y = 88,000 / 2.0 = 44,000, above 38,900. Configure test fails (new code beyond 0.5 pm); partner test fails. Rule 5: **build into core.**

**R2, a nightly export in one prospect's own data-lake schema.** One account, a bank in negotiation: e = 600,000 x 0.75 x 1.0 = 450,000, with h = 1.0 because the order form's data schedule names it. E = 450,000; N_req = 1, N_ev = 0, C = 450,000 / 450,000 = 1.0, so flagged. F = 2. Build 3 pm, carry 1 pm a year: K = 3 / 2 + 1 = 2.5; Y = 450,000 / 2.5 = 180,000, the highest yield on the sheet. Configure test fails (the mapping runs for one account only). Rule 3, with the partner test passing on the public export API and the bank agreeing to fund the work: **partner.** Marram's implementation partner builds the mapping outside the product; no code enters core.

**The other three, in brief.**

| Request | Key numbers | Rule that fired | Outcome |
|---|---|---|---|
| R3, a native connector to a mid-market ERP | Six accounts, E = 140,000; build 8 pm, carry 3 pm a year, K = 8 / 2 + 3 = 7.0, Y = 20,000; F = 3 | 4: an integration-platform partner already maintains a connector for that ERP | Partner, with a partner integration brief |
| R4, company logo on the right of the purchase-order PDF | Two accounts; the PDF template editor already supports placement | 2: configure test passes | Configure; customer success shows both admins |
| R5, on-premise deployment | One account, a public-sector prospect: e = 400,000 x 0.25 x 1.0 = 100,000; F = 0 | 1: contradicts the not-doing list | Decline with a written answer |

The written answer for R5: "We will not offer an on-premise deployment in the next four quarters. What we heard: your procurement rules require that purchase data does not leave your own infrastructure. Why: Marram runs as one multi-tenant service and does not ship single-tenant or on-premise builds. What you can do instead: the regional hosting option keeps data in your country, and our security pack documents where every copy lives. What would change our answer: a change to our deployment strategy, which we would announce to you directly."

R2 is the row to study. Ranked by yield it beats R1 about four times over; ranked by the rule it never reaches core, and the bank still gets its export, paid for by the bank, maintained by the partner, and absent from every other customer's release notes.

## The trap

Hinge inflation. The account team attaches every request to the largest open deal and marks it as the thing the deal hinges on, because that is the fastest way through this sheet, and E then reports the whole deal's value against a request the buyer mentioned once. The tell is a column of h = 1.0 with an empty hinge-artifact column, or an artifact that turns out to be the rep's own call summary. The rule that stops it is in the scale: 1.0 needs a buyer's written document, linked, and the [win-loss review](../../templates/operate/win-loss-review.md) checks the claim after the deal closes, because a deal that closed without the "mandatory" item says something about the next hinge that rep reports.

The quieter version is logo splitting. Three business units of one parent each file the same request, N_req reads 3, and the one-customer test passes. The tell: the requesting accounts share a procurement contact, a master agreement, or a parent on the order form. Step 1 counts by contracting parent for exactly this reason.

## Feeds

- [Backlog](../../templates/execution/backlog.md): a build row enters through section 1's sales intake row, carrying this sheet's row as the product problem that row demands
- [RICE scoring sheet](rice-scoring-sheet.md): a build row is ranked there against everything else; this sheet admits, RICE orders
- [Decision log](../../templates/execution/decision-log.md): every decline and every partner routing, with the written answer sent
- [Partner integration brief](../../templates/planning/partner-integration-brief.md): one per partner row
- [Admin entitlements spec](../../templates/definition/admin-entitlements-spec.md): a request that is really an entitlement ask, such as SSO on a lower plan for one deal, becomes a logged per-tenant override there, never a code change
- [Sales enablement one-pager](../../templates/delivery/sales-enablement-one-pager.md): the feature-request route reps are told to follow
- The PLANNING track of the [operating loop](../../os/OPERATING-LOOP.md), via the [roadmap builder](../../skills/roadmap-builder/SKILL.md)
- Method background: [Crossing the Chasm](../../knowledge/crossing-the-chasm.md) and the [B2B SaaS domain card](../../knowledge/domains/saas-b2b.md)
