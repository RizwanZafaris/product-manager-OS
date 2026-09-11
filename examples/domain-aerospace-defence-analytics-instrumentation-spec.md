# Analytics Instrumentation Spec: Meridian Planner, allied air force deployment

Fills [templates/delivery/analytics-instrumentation-spec.md](../templates/delivery/analytics-instrumentation-spec.md), bent by [knowledge/domains/aerospace-defence.md](../knowledge/domains/aerospace-defence.md). Everything here is invented: Halyard Systems is a fictional mission-planning software vendor, the allied air force customer and every name, identifier, and count are fiction built to illustrate the format, labelled ILLUSTRATIVE. See the [examples index](README.md).

**Owner:** Dana Okafor, Halyard Systems product lead (ILLUSTRATIVE) · **Engineering counterpart:** Miles Tran, platform engineering (ILLUSTRATIVE) · **Last updated:** 2026-09-11
**PRD:** not filled for this example (ILLUSTRATIVE) · **Analytics platform:** an on-premises event store maintained inside the accredited enclave; nothing reaches Halyard's own cloud analytics tooling (ILLUSTRATIVE)

Meridian Planner is a mission-planning application Halyard Systems deploys onto an allied air force's disconnected, accredited network. The source contains export-controlled technical data under the US Munitions List. This spec exists because the domain card's first and third questions turn identity and egress from a tooling choice into a gate an accreditor and export-control counsel both have to clear before section 4 can be signed.

## 1. Metrics this spec serves

| Metric | Defined in | Computed from (events below) | Reported where |
|---|---|---|---|
| Time to first approved mission plan in an exercise | PRD section 4 (ILLUSTRATIVE) | `plan_approved` where `attempt_count` = 1 | customer-side dashboard, tile 1 (ILLUSTRATIVE) |
| Plan revisions per exercise | PRD section 4 (ILLUSTRATIVE) | `plan_revised` grouped by `exercise_id` | customer-side dashboard, tile 2 (ILLUSTRATIVE) |

## 2. Event taxonomy

Naming convention for this product: object_action, snake_case, past tense.

| Event name | Fires when (exact trigger) | Properties (from section 3) | Required for launch | Owner |
|---|---|---|---|---|
| `plan_approved` | a mission plan is signed off by the approving role in-app | `role_session_id`, `exercise_id`, `attempt_count` | yes | Miles Tran (ILLUSTRATIVE) |
| `plan_revised` | an approved plan is reopened and re-saved | `role_session_id`, `exercise_id`, `revision_reason` | yes | Miles Tran (ILLUSTRATIVE) |

## 3. Property dictionary

| Property | Type | Allowed values or format | PII class (none / pseudonymous / direct) | Notes |
|---|---|---|---|---|
| `role_session_id` | string | opaque token issued by the customer's identity system, rotated per exercise | pseudonymous | never a name, service number, or device serial |
| `exercise_id` | string | customer-assigned exercise code | none | no unit or location encoded in the code by design |
| `attempt_count` | integer | 1 or greater | none | |
| `revision_reason` | enum | `weather`, `asset_change`, `tasking_change`, `other` | none | free text is never collected; `other` carries no comment field |

## 4. Identity and platforms

- User identifier in events: role_session_id, a pseudonymous identifier issued by the customer's own identity system and rotated per exercise, never a name, service number, or device serial
- Anonymous-to-known stitching: not needed, because the customer's identity system is the only place role_session_id maps to a person, and that mapping never leaves the customer's own systems (ILLUSTRATIVE)
- Platforms covered: the in-enclave desktop client · Gaps: no mobile client exists for this deployment, so there is nothing to instrument there (ILLUSTRATIVE)
- Environment separation: the accredited network has no staging environment; QA runs on an accredited replica maintained by the customer, never on production data
- Egress (a fifth bullet this domain adds beyond the template's four): none by default; any export runs through the customer's own periodic, human-reviewed data-release procedure, and through export-control review when technical data crosses a border, not an analytics pipeline setting

## 5. QA plan

- Verification method: debug view walkthrough per event, run on the accredited replica (ILLUSTRATIVE)
- Environment: accredited replica · Verifier: Miles Tran (ILLUSTRATIVE) · Verify by: 2026-10-02, before Gate 5 (ILLUSTRATIVE)
- [x] Every event marked required in section 2 was seen firing with correct properties (ILLUSTRATIVE)
- [x] Every metric in section 1 was computed once from replica data and the number was sane (ILLUSTRATIVE)
- Known instrumentation gaps shipping anyway: none (ILLUSTRATIVE)

## 6. Dashboards and consumers

| Dashboard | Link | Primary audience | Owner | Exists before launch |
|---|---|---|---|---|
| Exercise readiness tile set | hosted inside the customer's own enclave, no external link (ILLUSTRATIVE) | customer operations lead | customer security officer (ILLUSTRATIVE) | yes |

## Exit gate

This spec is done when:

- [x] Every PRD success metric traces to named events, and every event serves a named metric (ILLUSTRATIVE)
- [x] Every property has a type and a PII class (ILLUSTRATIVE)
- [x] The QA plan has a named verifier and a date before Gate 5 (ILLUSTRATIVE)
- [x] The launch dashboard exists and reads from these events, not from a manual export (ILLUSTRATIVE)

Signed: Dana Okafor, product lead, 2026-09-11 (ILLUSTRATIVE)
