# Developer Experience Spec: Corbelline Address API v2

Fills [templates/definition/developer-experience-spec.md](../templates/definition/developer-experience-spec.md). Everything here is invented for this standalone example: Corbelline Labs is a fictional company selling an address autocomplete, validation and geocoding API to online retailers and delivery platforms, its people are fictional, and every count, percentage, limit, quota, name and date is ILLUSTRATIVE, not drawn from any real company or market. There is no journey or data sheet behind it. See the [examples index](README.md).

**Owner:** Sunniva Albright, Product Manager, Developer Platform · **Developer relations lead:** Kofi Marchand · **Engineering lead:** Halima Brandt
**Date:** 2026-10-30 · **Status:** Signed at Gate 2 with two open items (sections 2 and 5)
**PRD:** the Address API v2 PRD, in the product workspace, not tracked in this repository · **API contract:** written in DESIGN, due 2026-12-04

Why v2: v1 shipped in 2023 with three endpoints, a key model that needed manual approval for production keys, and error bodies that were the web framework's defaults. v2 keeps the endpoints' purpose and changes everything a developer touches in the first hour. Every v1 number below is the baseline v2 is judged against.

## 1. Developer persona and job

| Persona | Role and context | Job: when..., I want to..., so I can... | What they use today instead | Evidence |
|---|---|---|---|---|
| Checkout engineer | Front-end or full-stack engineer at an online retailer with 20 to 200 staff, often on a hosted storefront with a plugin layer | When a customer types an address at checkout, I want suggestions and a validated result in the same field, so I can stop paying for failed deliveries | The storefront's built-in form, or a competitor's autocomplete | 14 interviews, June to August 2026; 38% of v1 support tickets come from this role (ILLUSTRATIVE) |
| Logistics backend developer | Backend engineer at a regional delivery platform | When merchants send orders in bulk, I want to validate and geocode thousands of addresses a minute, so I can start routing from coordinates I trust | An in-house geocoder plus manual correction | 6 interviews; 9 of the top 20 v1 accounts by volume are such platforms (ILLUSTRATIVE) |

| Adopter (writes the code) | Approver (permits the dependency) | Payer (owns the budget) |
|---|---|---|
| The two engineers above: needs a working call in minutes, an SDK in their language, and errors that say what to fix | The customer's security or platform review: needs scoped keys, SSO for the dashboard, an audit log, data processing terms, and for EU customers a processing region | Head of e-commerce or engineering manager: needs a predictable monthly bill and a way to cap it |

## 2. Time to first call

| Field | Value |
|---|---|
| Start event | `docs_first_view`: the first documentation page view from a browser later linked to the account. Fallback: `signup_started`, when no linked documentation view exists in the 30 days before sign-up |
| End event | First 2xx response from `/v2/validate` or `/v2/autocomplete` made with a key belonging to the developer's own project |
| Population | Developers whose `signup_started` falls in the calendar month |
| Statistics | Median and 90th percentile among developers who reached a first call; completion within 7 days of start |
| Target | Median 10 minutes or less; 90th percentile 45 minutes or less; completion within 7 days at least 55% (ILLUSTRATIVE) |
| Baseline | v1, June to August 2026: median 3 hours 10 minutes, 90th percentile 2 days 4 hours, completion within 7 days 40% (604 of 1,520). Measured the old way, from account creation, the same developers' median was 47 minutes (all ILLUSTRATIVE) |
| Instrumented by | Kofi Marchand; the events are in the v2 analytics instrumentation spec, in the product workspace |

The baseline row is the reason the start event moved. From account creation, v1 looked like a 47-minute onboarding; from the first documentation view it was more than three hours, and the difference was spent reading, waiting for production-key approval, and giving up.

| Funnel step | Event | Count in baseline window (monthly average) | Conversion from the previous step |
|---|---|---|---|
| Documentation first view | `docs_first_view` | 4,800 | Not applicable |
| Sign-up started | `signup_started` | 1,520 | 32% |
| Account created | `account_created` | 1,310 | 86% |
| Key created | `key_created` | 1,180 | 90% |
| First call attempted | `first_request` | 860 | 73% |
| First successful call within 7 days | `first_2xx` | 604 | 70% |

(All funnel figures ILLUSTRATIVE.) Two losses carry the v2 design. 320 of 1,180 developers created a key and never called (27%); in v1 a production key waited up to one business day for approval, which v2 removes (section 5). And 256 of 860 developers who attempted a call never got a 2xx (30%); their first errors are the rows of section 7.

[OPEN: developers whose browsers block the documentation analytics cookie fall back to `signup_started`, which shortens their measured time, and their share is unknown. Kofi Marchand owns an estimate from server-side documentation logs, due 2026-12-15.]

## 3. Quickstart and sandbox

- Quickstart steps, from landing to a successful response, target 4 steps and 5 minutes:
  1. Sign up with an email address or a code-hosting account login
  2. Copy the test key shown on the welcome screen; test keys need no approval
  3. Run the pre-filled request shown under the key, in curl or one of the three GA SDKs
  4. Read the validated address in the response, with each field explained beside it
- Last run end to end by someone outside the team: moderated sessions on 2026-10-21 and 2026-10-22 with 8 developers who had never used Corbelline. 6 of 8 finished in under 5 minutes; the slowest took 11 minutes, and both slow sessions lost time to a corporate proxy blocking the sandbox host. The quickstart now lists the host names to allow (ILLUSTRATIVE)
- Sandbox contents: test keys, 40 fixture addresses across six countries, and deterministic triggers: the postcode `00000` returns the ambiguity error, and the request header `Corbelline-Simulate: rate_limited` returns a 429
- Sandbox cost and limits: free, 10 requests per second
- Moving from sandbox to production: change the key and nothing else. One base URL serves both, and the key's prefix selects the environment. This was chosen because v1's second most common first error was a test key sent to the production host (section 7)

| Difference between sandbox and production | Why it exists | Where a developer learns of it |
|---|---|---|
| Addresses outside the 40 fixtures return a synthetic result marked `"sandbox": true` and `"verified": false`, never a real lookup | Real lookups cost money per call and carry third-party data terms | The `sandbox` field in every response, and the quickstart page |
| No billing and no monthly quota | Testing must not cost anything | The dashboard's Usage tab, which says "sandbox: not billed" |
| Rate limit of 10 requests per second | Set equal to the free plan's production limit, so nothing changes on promotion | The rate limits page |

## 4. SDKs and tooling

| Language or tool | Evidence for it | Generated or handwritten | Status (preview / GA / community) | Support window | Owner |
|---|---|---|---|---|---|
| JavaScript and TypeScript, browser widget and Node | 58% of v1 calls by client header | Generated core; handwritten autocomplete widget | GA at launch | 18 months after the next major ships | Luca Ferrand |
| Python | 19% of v1 calls | Generated | GA at launch | 18 months after the next major ships | Amira Solberg |
| PHP | 11% of v1 calls, mostly storefront plugins | Generated, plus a storefront plugin Corbelline maintains | GA at launch | 18 months after the next major ships | Luca Ferrand |
| Java | 6% of v1 calls | Generated | Preview at launch; GA once two enterprise customers run it in production | 12 months while in preview | Amira Solberg |
| Everything else | 6% of v1 calls, raw HTTP | Not applicable | OpenAPI file only | Not applicable | Not applicable |

(Call shares ILLUSTRATIVE.) Machine-readable description published at: `/v2/openapi.json` on the documentation site · Sample apps: a checkout address form for the browser widget, and a bulk validation script in Python

## 5. Authentication experience

- Mechanism and why: API keys. Secret keys for servers; publishable keys for browsers, limited to autocomplete and to an allow-list of origins. OAuth was considered and rejected for v2, because every call is server to server or from the customer's own checkout page, and there is no third-party user to delegate for
- Steps from sign-up to a working test key: 2 · to a working production key: 3 (verify the email address; add a payment method on paid plans), with no approval wait. v1 needed up to one business day of manual approval
- Key types and prefixes: `cbl_test_sk_` and `cbl_live_sk_` for secret keys; `cbl_test_pk_` and `cbl_live_pk_` for publishable keys
- Scopes or permissions: `validate`, `autocomplete`, `geocode`, `usage:read`. A new secret key gets `validate` and `autocomplete`; `geocode` is added on request because it is billed at a higher rate
- Rotation without downtime: two active secret keys per project, each showing its last-used time in the dashboard
- Leaked key handling: the prefixes are distinctive so public-code secret scanners can recognise them. A reported key is revoked within 15 minutes and its owner emailed with the revocation time and the rotation steps
- What the approver gets: SSO for the dashboard on the Enterprise plan; an audit log of key creation, rotation and revocation; data processing terms; and a processing region. [OPEN: whether EU-only processing ships at v2 GA or later; Halima Brandt, engineering lead, owns the decision, needed by 2026-11-20, because two enterprise evaluations are waiting on it]

## 6. Rate limits and quotas

| Limit | Applies to (key / project / account / endpoint) | Value per plan | At the limit: status, body code, retry signal | Seen before the limit how | Raised by whom, how fast |
|---|---|---|---|---|---|
| Request rate | Key | Free 10 per second; Growth 50 per second; Enterprise negotiated, with a 10-second burst at twice the limit | 429, `rate_limited`, `Retry-After` in seconds | Remaining-request headers on every response, names fixed in the API contract | Growth: a dashboard form, answered within one business day for a dated peak; Enterprise: the account manager |
| Monthly lookups | Project | Free 2,000; Growth 100,000 included, then billed per 1,000; Enterprise by contract | Free: hard stop, 429, `quota_exhausted`. Growth: no stop; overage is billed, and an optional spend cap set by the customer stops calls with `spend_cap_reached` | Usage meter in the dashboard; email at 80% and at 100% | Free: upgrade. Growth: the customer raises or removes their own cap |
| Batch size on bulk validate | Request | 100 addresses per request on every plan | 413, `batch_too_large`, the message gives the limit | The endpoint page, and the SDKs' batching helper | Not raisable. Larger jobs use the asynchronous batch endpoint planned for v2.1 |

Product reasoning for these values: the free quota lets one developer build and test a checkout integration end to end within a month without paying; the median v1 free project used 640 lookups in its first month (ILLUSTRATIVE). The free rate equals the sandbox rate so promotion changes nothing. Growth gets overage rather than a hard stop, because a checkout that stops validating on the last day of the month loses that day's orders; the spend cap gives the payer the control section 1 says they need. v1's free rate of 25 per second came from a load test and did not match the sandbox's 5, which is how a promotion used to break an integration on its first production day. Lowering any value in this table for an existing plan is a breaking change under section 8.

## 7. Errors as experience

Error body fields: `type` (the error's documentation URL), `title`, `status`, `detail`, `code`, `request_id`, `param`, in the shape of RFC 9457 · Message rule: says what went wrong and what to do next, in one or two sentences, never a framework class name

The v1 baseline: of the 256 developers a month who attempted a call and never got a 2xx, the first error was a malformed or truncated key for 98 (38%), a test key sent to the production host for 71 (28%), an origin not on a browser key's allow-list for 39 (15%), a country sent as a name for 27 (11%), and something else for 21 (8%) (ILLUSTRATIVE). The second of those disappears in v2 with the single base URL. The rest, and one error v2 introduces, are below.

| Error a newcomer meets first | Status and code | Message text, exactly | Documentation link | Fixable in one step? |
|---|---|---|---|---|
| Key copied with a space, or cut short | 401, `invalid_api_key` | "The API key in the Authorization header is not recognised. Keys start with cbl_test_ or cbl_live_ and are 48 characters long. Copy it again from Dashboard, Keys." | Authentication | Yes |
| Browser key used from an origin not on its allow-list | 403, `origin_not_allowed` | "Requests from http://localhost:3000 are not allowed for this publishable key. Add the origin under Dashboard, Keys, Allowed origins." | Publishable keys | Yes |
| Country sent as a name | 422, `invalid_country` | "country must be a two-letter ISO 3166-1 code such as DE or SE. Received: Germany." | Validate reference | Yes |
| Secret key sent from a browser, new in v2 | 403, `secret_key_in_browser` | "This secret key was sent from a browser, where anyone can read it. Use a publishable key in browsers, and rotate this secret key now under Dashboard, Keys." | Key types | No: the key must be rotated, and saying so is the point of the message |
| Free quota used up | 429, `quota_exhausted` | "This project has used its 2,000 free lookups for this month. Lookups resume on the 1st, or upgrade under Dashboard, Billing." | Plans | Yes |

## 8. Versioning and deprecation

| Lifecycle stage | What it promises | Notice before a breaking change or removal | How the stage is shown to developers |
|---|---|---|---|
| Experimental | Nothing: may change or vanish, never on by default | None | `experimental` label in the documentation, and a `Corbelline-Stage` response header |
| Preview | Breaking changes possible, no service level | 30 days | `preview` label, and the response header |
| Generally available | Breaking changes only in a new major version | The previous major stays available at least 12 months after the next major is generally available | No label |
| Deprecated | Works unchanged until its sunset date | Announced with its date: at least 12 months for a GA major, 30 days for a preview surface | The Sunset header of RFC 8594, carrying the date, on every response; a monthly email to every project that called it in the last 30 days; a dashboard banner |
| Decommissioned | A call returns 410 with code `version_retired` and the migration guide link for 90 days, then 404 | Not applicable | The 410 body |

- Breaking changes, as this product defines them: removing or renaming a field or an endpoint; adding a required parameter; narrowing validation, so input that was accepted is rejected; changing a default; removing an enum value; changing an error code a client may branch on; lowering a rate limit or quota on an existing plan; shortening a notice window
- How notice reaches active callers: direct email to the owners of every project that called the surface in the last 30 days, the Sunset header, and the dashboard banner. A changelog entry is the record, not the notice
- Migration guide published: written before the deprecation announcement and published with it
- Per-customer telemetry on deprecated surfaces: v1 calls by project, in the usage warehouse; the developer relations team contacts the top 50 v1 projects by volume by name. Owner: Kofi Marchand
- v1 schedule: deprecated when v2 is generally available, target 2027-02-01; decommissioned no earlier than 2028-02-01

## 9. Changelog and status page

- Changelog: the documentation site's changelog page; dated entries tagged breaking, new, fixed or deprecated; a feed and an email digest; every breaking entry links its migration guide. Owner: Kofi Marchand
- Status page: components Autocomplete, Validate, Geocode, Dashboard and Documentation; first post within 10 minutes of detection for any incident affecting more than 1% of requests over 5 minutes; updates every 30 minutes until resolved; a public postmortem within 5 business days for any incident longer than 30 minutes. Owner: Halima Brandt
- External service levels: the v2 SLA definition, in the product workspace, not tracked in this repository

## 10. Developer-facing success metrics

| Metric | Definition | Target | How it lies, or its counter-metric | Source |
|---|---|---|---|---|
| Time to first call | Section 2 | Median 10 minutes, 90th percentile 45 minutes | Survivorship: read with completion within 7 days | `docs_first_view` to `first_2xx` |
| Completion within 7 days | Section 2 | 55% (v1: 40%) | Rises if the population quietly narrows; the population is fixed in section 2 | Same events |
| Integrations in production | Distinct project with at least 1,000 production lookups a week for four consecutive weeks | 400 by 2027-06-30 (v1: 260) | Definition drift; the bar changes only by a new revision of this row | Usage warehouse |
| First-week client error rate | 4xx responses / all responses for projects in their first 7 days, by code | Below 8% (v1: 19%) | A rising rate is usually a documentation defect | Gateway logs |
| Support tickets per active integration | Tickets per 100 active integrations per month | 6 or fewer (v1: 11) | Falls when developers give up; read beside 90-day integration retention | Support tool |
| Deprecated surface share | v1 calls / all calls, and per project | Below 10% by 2027-11-01, and no project above 100,000 v1 calls a month by 2027-12-01 | The aggregate hides the tail; read the per-project list | Gateway logs |

(Targets and v1 values ILLUSTRATIVE.)

## 11. How this spec passes while developers still struggle

Three rows of the template's table applied here; the others were checked at the spec review on 2026-10-27 and did not.

| Failure | The tell | What happened here |
|---|---|---|
| Time to first call measured from sign-up | The start event is account creation | v1 reported 47 minutes from account creation; from the first documentation view the same developers took more than three hours. Section 2 now starts the clock earlier |
| Limits set by infrastructure alone | The limit equals the last load test's ceiling | v1's free limit of 25 per second came from a load test, against a sandbox at 5. Section 6 now sets both to 10 and writes the reasoning |
| The approver forgotten | Security review blocks enterprise deals after launch | The EU processing region is the approver's open question in section 5, with an owner and a decision date before DESIGN starts |

## Exit gate

- [x] Section 1 names the adopter, the approver and the payer separately, each with evidence
- [x] Time to first call has a start event earlier than account creation or a written reason why not, an end event, a statistic, a numeric target, and completion within 7 days beside it (the cookie gap is open in section 2, with an owner)
- [x] The quickstart has a step count and was run end to end by someone outside the team, on a stated date (2026-10-21 and 2026-10-22, 8 developers)
- [x] Every known difference between sandbox and production is listed (three)
- [x] Every SDK has evidence for its language, an owner and a support window
- [x] Every rate limit and quota has a number, a behaviour at the limit, a way to see it coming, and a raise path
- [x] The errors a newcomer meets first each have written message text and a documentation link
- [x] Each lifecycle stage has a notice period in days, notice reaches active callers directly, and lowering a limit or shortening a window is listed as breaking
- [x] The changelog and the status page each have an owner and a time target
- [x] Every developer-facing metric has its way of lying, or a counter-metric, beside it
- [x] The rows in the NFR and the API contract that implement sections 6 to 8 are linked, or named as open questions for DESIGN (NFR-07 to NFR-12 in the v2 NFR; the contract is due 2026-12-04 and inherits sections 6 to 8 as its open questions)

Signed: Sunniva Albright, Product Manager, Developer Platform, 2026-10-30
