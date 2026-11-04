# Admin Entitlements Spec: Plumline Workflows enterprise admin

Fills [templates/definition/admin-entitlements-spec.md](../templates/definition/admin-entitlements-spec.md). Everything here is invented for this standalone example: Plumline is a fictional software company, Plumline Workflows its fictional form-and-approval product sold to mid-market and enterprise operations teams, the people are fictional, and every number, name and date is ILLUSTRATIVE, not drawn from any real vendor or customer. The identity providers named in section 3 are real products, named only as the fictional test plan's targets. There is no external Plumline journey or data sheet. See the [examples index](README.md).

All figures are ILLUSTRATIVE.

**Owner:** Rosalind Achebe, Product Manager, Admin and Identity · **Security reviewer:** Kenji Varga, Security Engineering Lead · **Date:** 2026-11-13 · **Status:** Approved
**Parent PRD:** the product workspace's own `prd.md`, "Enterprise admin v1" (not tracked in this repository) · **Tiers taken from:** the workspace's own `pricing-packaging.md`, section 3: Free, Team, Business, Enterprise

## 1. Tenancy model

- Tenant unit: organization. A contract buys one organization; an Enterprise contract may buy several, each a separate tenant with its own admins
- Hierarchy inside a tenant: organization, then workspaces, then forms and their submissions
- One person in several tenants: allowed, switched from the organization menu; when SSO is enforced in a tenant, its session is separate from the person's other tenants
- The customer's top admin role is called: Owner, and the minimum number a tenant must keep: 1, with a console banner while only 1 exists
- Vendor staff access to tenant data: never by default; an Owner or Admin approves each support session, for at most 4 hours, scoped to named workspaces, logged as events A-07

## 2. Role matrix

| ID | Permission | Owner | Admin | Billing admin | Member | Guest | Auditor, read-only | Scope for S cells |
|---|---|---|---|---|---|---|---|---|
| P-01 | Invite a user | Y | Y | N | S | N | N | Member: Guests only, to workspaces the Member belongs to, and only if the Admin setting "members invite guests" is on |
| P-02 | Remove or suspend a user | Y | Y | N | N | N | N | |
| P-03 | Change a user's role | Y | S | N | N | N | N | Admin: any role except Owner, and never their own |
| P-04 | Configure SSO and enforcement | Y | Y | N | N | N | N | |
| P-05 | Configure SCIM provisioning | Y | Y | N | N | N | N | |
| P-06 | View the audit log | Y | Y | S | N | N | Y | Billing admin: billing events A-08 only |
| P-07 | Export the audit log | Y | Y | N | N | N | Y | |
| P-08 | Manage billing, plan and seats | Y | N | Y | N | N | N | |
| P-09 | Create, rotate or revoke API keys | Y | Y | N | S | N | N | Member: personal keys carrying no more than the Member's own permissions |
| P-10 | Export all tenant data | Y | N | N | N | N | N | |
| P-11 | Approve a vendor support-access session | Y | Y | N | N | N | N | |
| P-12 | Delete the tenant | Y | N | N | N | N | N | |
| P-13 | Create a workspace | Y | Y | N | S | N | N | Member: only if the Admin setting "members create workspaces" is on |
| P-14 | Build, submit, and approve forms | Y | Y | N | S | S | N | Member: in workspaces they belong to. Guest: submit only, to forms shared with them |

- Custom roles: offered on Enterprise, built from the permission rows above, capped at 20 per tenant
- Default role for a new user: Member, and for a user created by SSO just-in-time provisioning: Member, unless a group mapping in section 4 says otherwise

**Invariants** that hold whatever the roles say:

| ID | Invariant | Enforced where |
|---|---|---|
| INV-01 | A tenant always has at least 1 Owner; the last one cannot be removed, suspended or demoted | API and interface |
| INV-02 | Nobody can grant a permission they do not hold, including through a custom role | API |
| INV-03 | An Auditor never holds P-14, so an audit export never contains form content | API, and the custom-role builder refuses the combination |
| INV-04 | A Guest never holds P-01 to P-13, and never occupies a paid seat | API and billing |

## 3. SSO

- Protocols: SAML 2.0 and OIDC · Identity providers tested against: Okta, Microsoft Entra ID, Google Workspace, and a generic SAML test provider run by the QA team
- Plan that unlocks it: Business and Enterprise
- Domain verification: a DNS TXT record per email domain, required before enforcement: yes
- Enforcement options: optional, or required for every user except break-glass accounts
- Break-glass accounts: up to 2 per tenant, held by the customer's Owners, password plus hardware-key second factor; every sign-in emits A-01 marked break-glass and emails all Owners within 1 minute
- Existing password users when enforcement is switched on: sessions end at their next request; passwords are disabled, not deleted, and come back if enforcement is switched off
- Just-in-time provisioning: on by default, default role Member; identity-provider groups set the role only through SCIM group push, on Enterprise
- Session lifetime and re-authentication for admin actions: 12 hours; P-04, P-05, P-10 and P-12 re-prompt unless the user signed in within the last 15 minutes
- Signing certificate expiry: Owners and Admins emailed 30, 7, and 1 days before, with a console banner from day 30
- Admin can test the connection before enforcing it: yes, a "test sign-in" runs a full round trip for the testing admin only and shows the attributes received

## 4. SCIM provisioning

| Operation | Supported | What the product does | Latency target (mirrored in nfr.md) |
|---|---|---|---|
| Create user | yes | Member role, or the mapped group role; no welcome email, because the customer's identity provider owns onboarding | 5 minutes, NFR-21 |
| Update attributes | yes | Name, email, and department; those three fields are then locked from manual edit | 5 minutes, NFR-21 |
| Deactivate user | yes | Sessions revoked, API keys revoked, seat released for reuse with billing trued up at period end, private share links disabled. Public form links the user owns stay live and pass to the content custodian. [OPEN: security wants a deactivated user's public form links switched off; customer success says that breaks live intake forms customers depend on. Owner: Rosalind Achebe, decision with Kenji Varga by 2026-12-04, recorded in the decision log] | 10 minutes, NFR-22 |
| Delete user | yes | Their forms and submissions transfer to the content custodian, a named Owner chosen in SCIM settings | 10 minutes, NFR-22 |
| Push groups | yes, Enterprise | One group maps to one role. A user in two mapped groups gets the lower-privilege role, and A-09 records the conflict | 5 minutes, NFR-21 |
| Change group membership | yes, Enterprise | Role change applied, logged as A-03 | 5 minutes, NFR-21 |

- Conflict rule when SCIM and a manual admin edit disagree: SCIM wins; provisioned fields are locked, and a role can be edited by hand only while group push is off
- Sync errors surface to the customer admin as: A-09 events, plus a daily email digest to Owners and Admins while any error is unresolved
- Plan that unlocks it: Enterprise

## 5. Audit log

| ID | Event | Actor recorded | Target recorded | Other fields | Visible on plan | Retention |
|---|---|---|---|---|---|---|
| A-01 | Sign-in success and failure | user, IP, method | tenant | break-glass marker, failure reason | Team (this event only), Business, Enterprise | Team 7 days; Business 90 days; Enterprise 400 days |
| A-02 | SSO or SCIM configuration changed | admin | configuration | before and after values | Business, Enterprise | as A-01 |
| A-03 | User invited, removed, suspended, or role changed | admin or SCIM | user | old and new role, source (console, API, SCIM) | Business, Enterprise | as A-01 |
| A-04 | Permission denied on an admin action | user | the attempted action | permission ID | Business, Enterprise | as A-01 |
| A-05 | Data export or bulk download | user | workspace or tenant | row count, file format | Business, Enterprise | as A-01 |
| A-06 | API key created, rotated, or revoked | user | key ID, never the key | scopes | Business, Enterprise | as A-01 |
| A-07 | Vendor support-access session started and ended | Plumline staff member | workspaces in scope | approver, reason, duration | Business, Enterprise | as A-01 |
| A-08 | Plan, seats, or billing changed | Owner or Billing admin | subscription | old and new values | Business, Enterprise | as A-01 |
| A-09 | SCIM sync error | SCIM | user or group | error, payload field | Enterprise | as A-01 |
| A-10 | Form permissions changed (shared, unshared, made public) | user | form | old and new audience | Business, Enterprise | as A-01 |

- Timestamps in: UTC, with the viewer's offset shown in the console · Log is append-only, and reading it is itself logged: yes, as A-05 when exported
- Export: console download on Business; console, API, and streaming to the customer's security tooling on Enterprise
- What happens to the log when the tenant is deleted: retained for 30 days for the customer to export, then deleted with the tenant

## 6. Plan to entitlement mapping

| Entitlement | Free | Team | Business | Enterprise | Enforced at (API and interface / interface only) | Over-limit behaviour | On downgrade |
|---|---|---|---|---|---|---|---|
| Seats | 3 | up to 50 | up to 500 | per contract | API and interface | Free: invite blocked with an upgrade prompt. Team and Business: invite allowed, overage billed pro rata on the next invoice | The Owner picks who stays within 14 days; after that the most recently active users stay and the rest are suspended, never deleted |
| SSO | no | no | yes | yes | API and interface | n/a | Configuration kept read-only for 30 days; enforcement switched off; every SSO user is sent a password-set email |
| SCIM | no | no | no | yes | API | Provisioning calls return 403 and emit A-09 | Provisioning stops; existing users stay; identity-provider pushes fail visibly |
| Audit log retention | none | 7 days, A-01 only | 90 days | 400 days | API | n/a | Events older than the new limit kept read-only and exportable for 30 days, then deleted |
| Custom roles | no | no | no | yes, up to 20 | API and interface | The 21st role is refused | Users on a custom role move to Member; Owners told 14 days before |
| Data residency choice | US only | US only | US only | EU or US, chosen at creation | API | n/a | Data stays in its region; no move |
| API rate limit | none | 60 requests a minute | 300 | 1,200 | API | 429 with a retry-after header | New limit from the next billing period |

- Why SSO starts at Business rather than Team: Team accounts average 9 seats and are mostly bought on a card without a security review, so the support cost of SSO set-up was judged to outweigh the security benefit at that size. Kenji Varga records his disagreement on the security cost in the decision log entry of 2026-10-22; the choice is revisited at the next pricing review
- Per-tenant overrides: granted only by the head of sales operations with Rosalind Achebe's approval, logged in the entitlement admin tool with an expiry of at most 12 months; open overrides today: 4, listed in that tool, each entering through [enterprise request triage](../frameworks/prioritization/enterprise-request-triage.md)

## 7. Data residency and tenant isolation

| Data class | Stored where | Processed where | Subprocessors | Pinned to the tenant's region? | Owner of the answer |
|---|---|---|---|---|---|
| Primary records | Tenant's region | Tenant's region | Cloud host | Yes | Maeve Duarte, Engineering Lead |
| Backups | Tenant's region, second zone | Tenant's region | Cloud host | Yes | Maeve Duarte |
| Logs and traces | Tenant's region; error reports scrubbed of form content | Tenant's region | Cloud host, error-tracking vendor (EU instance for EU tenants) | Yes | Kenji Varga |
| Search indexes and caches | Tenant's region | Tenant's region | Cloud host | Yes | Maeve Duarte |
| Analytics and warehouse copies | US, for every tenant | US | Product-analytics vendor | No. [OPEN: either strip every tenant-entered value from analytics events, or route EU tenants to the vendor's EU instance. Owner: Kenji Varga, by 2026-12-11. Until then the subprocessor list says so, and no EU Enterprise contract signs with a residency clause that covers analytics] | Kenji Varga |
| Model or AI processing, if any | None today | None today | None | n/a: the planned field-suggestion feature needs this row filled before its own Gate 2 | Rosalind Achebe |
| Support and ticketing tools | US | US | Ticketing vendor | No; disclosed in the subprocessor list, and ticket attachments deleted after 30 days | Ines Calloway, Support Lead |

- Regions offered: EU and US, chosen at tenant creation; changing region later is a Plumline-run migration with up to 4 hours of read-only time, requested through support
- Isolation model: shared tables keyed by tenant ID on every plan, with per-tenant data keys on Enterprise; dedicated deployment is not offered
- What prevents a cross-tenant read in code: the tenant scope is applied in the data-access layer, a build check rejects any query without it, and the test `test_cross_tenant_read_denied` runs in CI against every API resource
- Encryption keys: vendor-managed on every plan, with per-tenant data keys on Enterprise; customer-managed keys are not offered
- Limits that stop one tenant degrading another: the per-tenant API rate limits in section 6, and a cap of 20 concurrent workflow jobs per tenant
- Detail lives in: the workspace's own copies of the [privacy impact assessment](../templates/architecture/privacy-impact-assessment.md), the [data model](../templates/architecture/data-model.md) section 5, and the [security architecture checklist](../templates/architecture/security-architecture.md)

## 8. What the customer admin can self-serve

| Admin task | Console | API | Needs vendor support (why) | Target (minutes or steps) |
|---|---|---|---|---|
| Add, remove, and change roles of users | yes | yes | no | Under 1 minute per user |
| Connect, test, and enforce SSO | yes | no | no | 30 minutes, 6 steps, including the test sign-in |
| Rotate the SSO signing certificate | yes | no | no | 5 minutes |
| Set up SCIM | yes | n/a | no | 20 minutes with the identity provider's admin |
| View and export the audit log | yes | Enterprise | no | Export of 30 days in under 1 minute |
| Change plan or seats; download invoices | yes | no | Downgrade from Enterprise only, because it ends a contract | 2 minutes for upgrades and seat changes |
| Export all tenant data | yes | no | no | Archive ready within 1 hour, link emailed to the Owner |
| Approve or deny a vendor support-access session | yes | no | no | One click from the email or console |
| Choose or change data region | At creation only | no | Changing region after creation, because it is a migration Plumline runs | Change: up to 4 hours read-only |
| Delete the tenant | yes, Owner only, after a 7-day cooling-off period | no | no | 3 steps plus re-authentication |

## 9. How this spec fails

The template's failure table, with the third column saying what this spec does about each.

| Failure | The tell | What this spec does |
|---|---|---|
| Permissions enforced only in the interface | A member's API token can still list every user | Every N cell in section 2 is listed for an API negative test in the workspace's acceptance criteria, AC-40 to AC-89, one per N cell |
| Deprovisioning that leaves a way in | A deactivated user's API key still works | The deactivate row names sessions, keys, seat, and share links, with a 10-minute target in NFR-22; the public-link question is open with an owner and a date |
| An audit log of the easy events | Role changes, exports, and vendor access are missing | Section 5 was filled from the three security questionnaires the Q3 pipeline returned, not from the events already emitted |
| Residency answered for the database only | Backups, logs, analytics, and support tools missing | Every data class has a row; analytics is honestly No, with an owner and a date |
| Downgrade left undefined | No on-downgrade column | Answered for every entitlement in section 6 |
| Sales exceptions written as code | A plan-name conditional for one deal | Entitlements are per-tenant data; the 4 open overrides are listed, dated, and triaged |
| Enforced SSO with no way back in | No break-glass line | Up to 2 break-glass accounts per tenant, alerted on every use |
| Custom roles nobody can read | Many roles and no one can say what one grants | Roles are bundles of section 2 rows, capped at 20, listed in the console with their rows |

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Section 1 names the tenant unit, the top admin role with its minimum count, and the vendor staff access rule with its audit event
- [x] Every permission row has an ID and a Y, N or S in every role column, with the scope written for each S
- [x] Every N cell names, or is listed for, an API negative test in acceptance-criteria.md (AC-40 to AC-89, one per N cell in the workspace's acceptance criteria)
- [x] Section 3 answers enforcement, break-glass, just-in-time default role, and certificate expiry warning
- [x] The SCIM deactivate row names sessions, tokens, shared links, and seat release, and its latency is a row in nfr.md section 4 (NFR-22; the public-link behaviour is open with an owner and a date)
- [x] The audit log lists admin actions, authentication, data export, and vendor access events, each with a retention per plan
- [x] Every entitlement row cites the tiers in pricing-packaging.md and answers over-limit and on-downgrade behaviour
- [x] Every data class in section 7 has a residency answer, or an owner and a date (analytics: Kenji Varga, 2026-12-11)
- [x] The isolation model is named with the test that proves a cross-tenant read fails
- [x] Every "needs vendor support" cell in section 8 carries a reason
- [x] The security reviewer has signed below

Signed: Rosalind Achebe, Product Manager, Admin and Identity, 2026-11-13 · Kenji Varga, Security Engineering Lead, 2026-11-13
