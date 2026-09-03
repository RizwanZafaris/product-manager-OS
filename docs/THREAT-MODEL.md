# PM OS Threat Model

## Scope and boundary

The local security gates provide **local evidence** about this repository at a
specific commit. Local evidence is not external evidence. It does not prove a
live sandbox behaved safely, that a provider retained or deleted data as
promised, that a user understood a workflow, or that a regulator accepts a
control. Those are separate, time-bound attestations.

The PM OS treats prompts, imported research, tickets, documents, model output,
and connector responses as untrusted data. They cannot authorize tool use,
external effects, changes to approvals, or changes to policy. A runtime hook
requires an explicit actor, revision, evidence hashes, approval identifier, and
idempotency key at the relevant boundary. These boundary fields are typed and
nonempty: booleans or arbitrary truthy values do not count as approvals,
idempotency keys, revisions, or evidence. Unknown and case-mismatched tool
names require explicit approval rather than inheriting a silent allow.

## Assets and trust boundaries

Assets include product artifacts, evidence hashes, approval records, audit
history, task memory, credentials supplied through the environment, and the
availability of the local workspace. Trust boundaries are the local filesystem,
the agent runtime, an optional model provider, optional integration adapters,
and a human approver. No credential belongs in a document, log, test fixture,
or commit.

## Threats and controls

| Threat | Local control | Remaining external evidence |
| --- | --- | --- |
| Prompt injection | Hooks deny tool authority originating from untrusted content; every MCP connector call requires explicit approval because connector names and payloads are not a trustworthy read-only declaration. | Adversarial live sandbox run and operator review. |
| Credential disclosure | Tracked-source scanner rejects common key shapes; hook audit stores only allow-listed metadata. | Provider/account rotation and access-log review. |
| Disguised local execution | The source gate resolves direct, tuple, branch/loop/match-merged, conditional-expression, and class-attribute aliases plus literal `getattr` and `__import__` dispatch for forbidden execution; mutable module-dictionary subscript dispatch is rejected. Subprocess `shell` is accepted only as literal `False`, including expanded keywords and `Popen`'s positional slot. | Runtime sandboxing, code review, and endpoint monitoring. |
| Workspace escape | Relative paths are normalized and write hooks deny destinations outside the repository. | OS permissions and endpoint protection. |
| Approval drift | Regulated approvals bind evidence hashes and invalidate when evidence changes. | Legal, compliance, and regulatory review. |
| Audit tampering | Audit exports are hash-chain verified before use. | Independent review of the exact release SHA. |
| Research consent expiry or withdrawal | Research retrieval, quoting, and public evidence enumeration hide content once the participant's scope is inactive or retention has expired. | Consent process, data-subject requests, and retention-policy review. |
| Adapter payload exhaustion or credential retention | In-memory adapters bound record, collection, depth, text, and canonical-payload sizes; recursive secret-shaped values are rejected and outcome/payload views are immutable. | Production storage quotas, credential rotation, and provider-side data handling. |
| Duplicate or forged external delivery acknowledgement | The local outbox serializes same-process attempts, binds an idempotency key to event type and payload, and accepts acknowledgement only with the sender's exact nonempty external ID. | Durable cross-process locking, remote idempotency support, and remote reconciliation evidence. |
| Provider outage or mutation | Routing records provider/model provenance and supports bounded fallbacks. | Provider status, contract, and incident evidence. |

## Dependency surface and exception inventory

The Python package declares an empty runtime dependency surface and the local
gates use only the standard library. Any new lockfile, package dependency,
network connector, sandbox exception, or subprocess exception is a change to
the threat model and must be reviewed before release. The explicit exception
inventory is: optional OpenRouter HTTPS calls when configured by the operator;
optional OmniRoute/desktop adapter integrations documented in `SECURITY.md`;
and subprocesses whose argv is fixed by a checked-in CI or test command. None
of these exceptions is proof of a live sandbox, provider assurance, user
research, or regulatory approval.

## Release evidence

Before a release, keep the exact commit SHA, local gate output, test results,
dependency diff, migration/backup result, and a named reviewer decision. Mark
external claims as pending until their signed evidence is attached. Never turn
a passing local test into a claim that a provider, user, sandbox, or regulator
has verified the system.
