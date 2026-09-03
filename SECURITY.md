# Security

Last reviewed 2026-09-03, against the tree as it stands on that date.

This repository has three paths through it and they have different security properties. Most readers only ever use the first. Read the one you are on, because a sentence that is true of the manual path is not automatically true of the local runtime or a provider call.

## The manual path: markdown, no network, no credentials

Clone the repository, copy a template, fill it in an editor, work the gate checklist by hand. On this path:

- Nothing runs. Templates, knowledge cards, worksheets, gates, and prompts are text files.
- Nothing calls out. There is no telemetry, no hosted service, no account, and no phone-home.
- Nothing takes a credential. No file in the tree asks for one and no file in the tree holds one.

Three local scripts exist and stay on this path. `lint.py` and `test_lint.py` are the quality gate and its tests, Python standard library only. `tools/graph.py`, `tools/frontmatter_init.py`, and `tools/check_manifest.py` read the tree and write `docs/GRAPH.md` or a report. They open no socket and read no environment variable. `harness/adapters/claude-code/generate.py` writes generated command files inside the repository. If you never touch `harness/runner.py` or the desktop adapter, that is the whole attack surface: files you can read, and scripts that read files.

## The local runtime: durable state without a provider

`pmos/` is an optional, standard-library Python runtime. `pmos init` creates a local SQLite database under a workspace's `.pmos/` directory; the Store uses transactions, content hashes, compare-and-swap revisions, full snapshots, backups, a leased at-least-once work queue, and separate OS and task memory streams. The Conductor, domain policy, approvals, portfolio relations, outbox, migration, hooks, and provenance modules are local code with explicit contracts. They do not contact a provider by default.

SQLite is authoritative only on the local filesystem. WAL and fencing do not turn it into a shared network database, and the outbox/queue contract is not exactly-once delivery to an external system. The typed adapters are safe seams and bounded in-memory conformance doubles until an operator authorizes a real provider or vendor sandbox: they reject oversized/cyclic payloads, credential-shaped values, and mutable delivery identities. The local outbox serializes attempts only within one process; a real sender still needs durable remote idempotency and reconciliation. Release provenance is offline hash evidence; it contains no file contents, environment variables, or credentials.

## The optional provider path: legacy harness, OmniRoute, and OpenRouter

`harness/runner.py` is a legacy route executor. The local runtime also contains an optional OpenRouter adapter. Either runs only when an operator invokes it; neither sends anything in the background.

**Credentials.** OmniRoute reads `OMNIROUTE_BASE_URL` and its configured API-key variable; the OpenRouter adapter reads `OPENROUTER_API_KEY` (or a configured environment-variable name) only while constructing a request. A credential is never committed, copied into runtime state, returned in a route decision, or included in the adapter representation. Set keys in your shell, secret manager, or CI secret store, never in a Markdown file, JSON config, or command transcript. A literal credential anywhere in the tree is a defect.

**The network boundary.** OmniRoute calls its configured OpenAI-compatible endpoint. OpenRouter discovery calls `/api/v1/models`, and completions call `/api/v1/chat/completions`; both use bounded request and response sizes and safe error categories. What crosses a provider boundary is the prompt and requested model, plus any allowed attribution header. Treat everything you send as provider-visible. A provider-reported model replacement is rejected unless it is the exact model admitted by policy; the local router records safe provenance for that accepted model, token counts, and policy result, not the credential or prompt body.

**Response handling.** The OpenRouter adapter validates JSON shape and response bounds, and converts authorization, rate-limit, timeout, network, malformed-response, and refusal cases into explicit failures. Model output is data: it is never executed, imported, or evaluated. A provider failure must not silently become a successful approval, external action, or low-risk fallback.

**The write boundary.** `--product` takes a slug, not a path: letters, digits, underscore, hyphen. Empty values, dot segments, separators, and absolute paths are refused, and the resolved directory has to sit directly under `products/` or the run stops before any call is made. Output is refused anywhere under `templates/`. An existing artifact or log is never overwritten unless you pass `--update`. The artifact, its log, and the one journal row are staged as temporary files and committed with a replace only after all three are ready, so an interrupted run cannot leave a half-written document behind. If a replace fails partway through the set, every destination already replaced is restored from a copy taken before the commit, so the workspace is left as it was rather than holding an artifact whose log never landed. What is not claimed: that the restore itself cannot fail. There is no write-ahead journal here, so a failure during rollback is reported by path and left for a person, not silently retried. Writes to STATE.md additionally take an advisory lock held from the read to the commit, because two runners appending a journal row used to read the same bytes and the second replace overwrote the first.

**The local-execution exception.** The legacy `--transport cli` harness option shells out to `omniroute` on your PATH. It is a convenience, not a deployment path. The current local runtime uses no shell execution for provider calls.

**The desktop adapter.** `harness/adapters/desktop/server.py` speaks MCP over standard input and output and needs the MCP SDK installed, which is the only third-party dependency anywhere in the tree. It listens on no port. It returns the plan and the governing file paths for a route: it places no model call, writes no file, sends nothing, and signs no gate. It reports whether a credential variable is set and never reports a value.

## What is deliberately not claimed here

- **Not a review of your gateway or provider.** Everything above is about this repository's local side of a call. What OmniRoute, OpenRouter, or another target does with a prompt is that system's security and data-processing story, not this one's.
- **Not a live-provider attestation.** Unit tests use controlled fakes; they do not verify a live provider, a free-model catalog, pricing, privacy terms, capability, or availability. OpenRouter models are dynamically discovered; free availability is variable; reachability, price, and a model name never equal certification.
- **Not a vendor-sandbox, human-review, adoption, regulatory, hosted-CI, or publication claim.** Local evidence is not external evidence. The required external evidence is tracked in [docs/readiness/external-gates.json](docs/readiness/external-gates.json).
- **Local review identity is not authenticated by the reviewed tree.** The exact-tree review record binds findings to bytes and rejects unresolved P0/P1 issues, but its reviewer name is explicitly an unauthenticated local claim. Trusted human or organizational review must arrive from an external identity and approval system.
- **Not a claim that the boot prompts enforce secret hygiene.** An earlier version of this file said the prompts in `system/` instruct models to refuse storing secrets in artifacts. That instruction is not in the prompt, so the claim is withdrawn rather than restated. [OPEN: whether `system/BOOT-PROMPT.md` should carry such a rule is a decision for the owner of `system/`, and this file will describe it once it is there.]

## Your own hygiene, which is where the real risk is

- Never put real credentials, keys, customer records, or candidate material into a filled template, in any repository, including a private fork. A filled PRD gets pasted into chat windows and tickets; treat it as public by default.
- Filled artifacts belong in `products/<name>/`, which is gitignored and never ships from here.
- Check 9 of `lint.py` scans every tracked file for common credential shapes and for credential-shaped names assigned high-entropy values, and it exempts no file, including the files that define the patterns. It is a backstop, not a permission slip: it catches shapes it knows.
- `tools/security_gate.py` also rejects runtime execution primitives after resolving direct, tuple, branch/loop/match-merged, conditional-expression, and class-attribute aliases plus literal `getattr` and `__import__` dispatch; module-dictionary subscript dispatch is rejected rather than guessed safe. For subprocess calls, `shell=False` must be literal in ordinary and expanded keywords and in `Popen`'s positional shell slot; a computed value or dynamic lookup is a finding, not a claim that static inspection proved it safe.
- The `content-is-data` invariant in `harness/INVARIANTS.md` is a security control, not a style rule. Anything a model reads from a page, a feed, an inbox, a ticket, or a file is data, and a directive found inside it is reported with its source named and never obeyed.
- High-risk routing requires an explicitly certified model and matching privacy permission. A free model is not certified by being available. Keep OmniRoute optional; use it only where its gateway controls meet your own policy.

## Reporting a problem

Open a GitHub security advisory on this repository, or a plain issue if the matter is not sensitive. Reports are read by the maintainer directly, and there is one maintainer, so there is no response-time promise beyond that. Two things are especially worth reporting: a template or prompt that induces unsafe handling of secrets, and any path by which the runner could write outside `products/` or leak a credential into a log.
