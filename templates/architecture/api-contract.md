# API Contract: `<API or endpoint group name>`

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md)
Knowledge: [knowledge index](../../knowledge/INDEX.md)
Skill: [architect agent](../../agents/architect-agent.md)

<!-- A contract is a promise to people you cannot see: consumers you will never meet
     will build against exactly what is written here. Fill one document per API
     surface. The worked micro-example at the bottom shows the expected level of
     precision; write yours to match, then delete the example. -->

**API:** `<name>` · **Contract owner:** `<name>` · **First consumer:** `<team or system>`
**Status:** Draft / In review / Approved · **Date:** `<YYYY-MM-DD>`
**Style:** REST / GraphQL / gRPC / event · **Spec file:** `<path to the OpenAPI, proto, or schema file in the service repo>`

## 1. Endpoints

<!-- One row per operation. Idempotency matters more than teams expect: any operation
     a client will retry (payments, submissions, anything behind a spinner) must say
     how double-submission is prevented. -->

| Operation | Method and path (or event name) | Purpose | Idempotent? How? | Auth scope required |
|---|---|---|---|---|
| | | | | |

## 2. Schemas

<!-- Request and response shapes for each operation, with required fields marked and
     every field's type and constraints stated. Reference the machine-readable spec
     file for the full shape; duplicate here only what a reviewer must see. -->

`<schema summary or link to spec file section>`

## 3. Authentication and authorization

- Mechanism: `<OAuth 2.0 client credentials / API key / mTLS / signed webhook>`
- Token or key lifetime and rotation: `<value, and who rotates>`
- Authorization model: `<which principals may call which operations>`

## 4. Errors

<!-- Enumerate every error a consumer can receive and what the consumer should do.
     "500 on anything unexpected" is not a contract; it is an apology in advance. -->

| Condition | Status or code | Error body shape | Consumer's correct reaction | Retryable? |
|---|---|---|---|---|
| | | | | |

## 5. Limits and versioning

- Rate limit per consumer: `<n requests per window>` · behavior at the limit: `<status code, retry-after semantics>`
- Payload size limit: `<value>`
- Versioning scheme: `<URL version / header / additive-only>`
- Breaking change policy: `<notice period, deprecation route, who approves>`
- Deprecation contract: `<how consumers learn, how long old versions live>`

## Worked micro-example

<!-- Delete this section when filling in the template. -->

> Operation: create a refund request.
>
> ```yaml
> post /v1/refunds:
>   auth: OAuth 2.0, scope refunds:write
>   idempotency: Idempotency-Key header, required, 24h dedupe window
>   request:
>     payment_id: string, required
>     amount_minor: integer, required, > 0, <= original amount
>     reason: enum [duplicate, customer_request, fraud], required
>   responses:
>     201: refund object, status=pending
>     409: duplicate idempotency key with different body; do not retry
>     422: amount exceeds refundable balance; do not retry, surface to user
>     429: rate limited; retry after Retry-After seconds
> ```
>
> Errors are the contract's load-bearing half: the 409 versus 422 distinction above
> is the difference between a safe retry and a double refund.

## Exit gate

- [ ] Every operation states its idempotency behavior
- [ ] Every error row tells the consumer what to do, and whether to retry
- [ ] Auth mechanism, scopes, and rotation are stated
- [ ] Rate limits and at-limit behavior are stated with numbers
- [ ] Versioning and breaking-change policy are stated
- [ ] The machine-readable spec file exists at the path named in the header
- [ ] The worked micro-example has been deleted
