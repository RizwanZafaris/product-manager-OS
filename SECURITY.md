# Security

Last reviewed 2026-09-03, against the tree as it stands on that date. The path inventory, the script list below it, and the agent-CLI section were re-checked against the tree on 2026-09-10; the rest of this file carries the earlier date.

This repository has four paths through it and they have different security properties. Most readers only ever use the first. Read the one you are on, because a sentence that is true of the manual path is not automatically true of an agent CLI, the local runtime, or a provider call.

## The manual path: markdown, no network, no credentials

Clone the repository, copy a template, fill it in an editor, work the gate checklist by hand. On this path:

- Nothing runs. Templates, knowledge cards, worksheets, gates, and prompts are text files.
- Nothing calls out. There is no telemetry, no hosted service, no account, and no phone-home.
- Nothing takes a credential. No file in the tree asks for one and no file in the tree holds one.

Six local scripts stay on this path. `lint.py` and `tests/test_lint.py` are the quality gate and its tests, Python standard library only. `tools/graph.py`, `tools/frontmatter_init.py`, and `tools/check_manifest.py` read the tree and write `docs/GRAPH.md` or a report. They open no socket and read no environment variable. `harness/adapters/claude-code/generate.py` writes generated command files inside the repository.

Those six are not the whole executable surface of the tree, and this file used to say they were. `tools/` holds eighteen scripts in all. Most of the fifteen not named above are gate and readiness runners that read files and print findings; `tools/init_product.py` is the quickstart tool that writes a workspace under `products/`; and one leaves this path entirely, because `tools/ext_ai_probe.py` reads `OPENROUTER_API_KEY` (or an OmniRoute gateway variable) and makes the outbound calls described under the provider path below. So the manual path is files you can read and scripts that read files, and three tracked entry points step off it when you invoke them: `harness/runner.py`, the desktop adapter, and that probe. A fourth needs no invocation at all, and is the section immediately below.

## The agent-CLI path: a committed hook that runs on session events

Method 3 in [README.md](README.md) is an agent CLI reading [CLAUDE.md](CLAUDE.md) or [AGENTS.md](AGENTS.md). Two tracked files make that path different from the manual one, and they are the only part of this tree that runs without being asked.

`.claude/settings.json` registers `.claude/hooks/pmos_hook.py` on seven Claude Code events: session start, prompt submit, before and after every `Bash`, `PowerShell`, `Write`, `Edit`, `NotebookEdit`, and `mcp__*` tool call, and on stop, subagent stop, and task completion. Claude Code reads that settings file when it opens the repository, so cloning the tree and starting a session is enough to arm the layer. Delete `.claude/` and it is gone; nothing else in the tree depends on it.

The hook itself reads one JSON payload from standard input, refuses anything over 1 MiB, and imports `pmos/hooks.py` from the project directory. That policy module is standard library only, opens no socket, and reads no environment variable; the hook adapter around it reads one, `CLAUDE_PROJECT_DIR`, to locate the repository. What the policy does is refuse. It denies a write whose destination is outside the project or lands on `.git`, `.env`, `modules/regulated/`, or a `.pem`, `.key`, or `.p12` file. It denies a payload carrying credential-shaped material, such as a provider key or a key, token, or password assignment. It blocks destructive shell commands. It asks for human approval before any MCP connector call and before any tool name it does not recognize, because an unknown connector's own description is not a trustworthy capability declaration. One limit belongs with that list: only the `PreToolUse` refusals reach Claude Code as a permission decision. A refusal raised on a `PostToolUse` event serialises to an empty object, so that branch of the policy does not currently change what the CLI does, and this file will say otherwise only when the code does.

One event does more than decide. On stop, subagent stop, and task completion the hook spawns `python3 tools/ci_gate.py --gate compile --gate os-tree` inside the repository, with `shell=False` and a 180-second timeout, and blocks the stop when that returns non-zero. That subprocess runs `git ls-files`, compiles every tracked Python file into a temporary directory, and runs the document-tree check. It writes nothing into the repository and calls nothing out. It is still repository code executing because a session ended rather than because anyone ran it, which is the fact this file omitted, and it is the reason the manual path's guarantees are stated for the manual path only.

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
