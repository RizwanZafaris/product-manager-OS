# Security

Last reviewed 2026-09-03, against the tree as it stands on that date.

This repository has two paths through it and they have different security properties. Most readers only ever use the first. Read the one you are on, because a sentence that is true of the manual path is not automatically true of the runtime path.

## The manual path: markdown, no network, no credentials

Clone the repository, copy a template, fill it in an editor, work the gate checklist by hand. On this path:

- Nothing runs. Templates, knowledge cards, worksheets, gates, and prompts are text files.
- Nothing calls out. There is no telemetry, no hosted service, no account, and no phone-home.
- Nothing takes a credential. No file in the tree asks for one and no file in the tree holds one.

Three local scripts exist and stay on this path. `lint.py` and `test_lint.py` are the quality gate and its tests, Python standard library only. `tools/graph.py`, `tools/frontmatter_init.py`, and `tools/check_manifest.py` read the tree and write `docs/GRAPH.md` or a report. They open no socket and read no environment variable. `harness/adapters/claude-code/generate.py` writes generated command files inside the repository. If you never touch `harness/runner.py` or the desktop adapter, that is the whole attack surface: files you can read, and scripts that read files.

## The runtime path: what changes when you run the harness

`harness/runner.py` is the one component in this repository that makes a network call. It runs only when you run it, and this is what it does.

**Credentials.** The base URL comes from `OMNIROUTE_BASE_URL` in your environment (`routing/omniroute.config.json` records `http://localhost:20128/v1` as the default it expects). The credential comes from whatever environment variable that config's `endpoint.apiKeyEnv` names, `OMNIROUTE_API_KEY` unless you change it. Both are read from the environment at call time. Neither is ever written into this repository, and `routing/omniroute.config.json` holds variable names rather than values. The resolved credential is registered once with a single redactor that every output sink uses: standard output, the run log, the artifact's own face, and the journal row. Length is not a filter, because a short credential is still a credential; a credential under eight characters is announced on standard error so you know masking will be aggressive. Printed URLs are sanitized: userinfo is dropped and query values are masked.

**The network boundary.** One outbound HTTP POST per call, to `$OMNIROUTE_BASE_URL/chat/completions`, OpenAI-compatible, streamed. The expected target is a gateway on your own machine. Point the variable somewhere else and you have pointed it somewhere else: the runner sends where you tell it. What crosses that boundary is the prompt, which is the skill file, the route's named reads, the resolved invariant rules, the template, and whatever you passed with `--input` or `--input-file`. Nothing else in the tree is read for the call, and nothing is uploaded in the background.

**Response handling.** Raw gateway response bodies are never persisted. A failed call records its status and a sanitized descriptor, never the server's own text, so a hostile or confused gateway cannot write its content into your log. Model output is written into a copy of a template as text. It is never executed, imported, or evaluated, and the runner downloads no code and runs no downloaded thing.

**The write boundary.** `--product` takes a slug, not a path: letters, digits, underscore, hyphen. Empty values, dot segments, separators, and absolute paths are refused, and the resolved directory has to sit directly under `products/` or the run stops before any call is made. Output is refused anywhere under `templates/`. An existing artifact or log is never overwritten unless you pass `--update`. The artifact, its log, and the one journal row are staged as temporary files and committed with a replace only after all three are ready, so an interrupted run cannot leave a half-written document behind. If a replace fails partway through the set, every destination already replaced is restored from a copy taken before the commit, so the workspace is left as it was rather than holding an artifact whose log never landed. What is not claimed: that the restore itself cannot fail. There is no write-ahead journal here, so a failure during rollback is reported by path and left for a person, not silently retried. Writes to STATE.md additionally take an advisory lock held from the read to the commit, because two runners appending a journal row used to read the same bytes and the second replace overwrote the first.

**The local-execution exception.** `--transport cli` shells out to an `omniroute` binary on your PATH and lets that binary authenticate itself against a local install. It is a convenience for a machine where the gateway is up and the loopback API is closed to unauthenticated callers, and it is not a deployment path. If you do not want this repository starting a subprocess, stay on the default `--transport http`.

**The desktop adapter.** `harness/adapters/desktop/server.py` speaks MCP over standard input and output and needs the MCP SDK installed, which is the only third-party dependency anywhere in the tree. It listens on no port. It returns the plan and the governing file paths for a route: it places no model call, writes no file, sends nothing, and signs no gate. It reports whether a credential variable is set and never reports a value.

## What is deliberately not claimed here

- **Not a review of your gateway.** Everything above is about this repository's side of the call. What your OmniRoute instance, or whatever you point the base URL at, does with a prompt is that system's security story and not this one's.
- **Not a claim about model vendors.** Whatever you paste into a chat model goes wherever that vendor's terms say it goes. If your product data cannot leave your environment, the manual path uses no model at all.
- **Not a claim that the boot prompts enforce secret hygiene.** An earlier version of this file said the prompts in `system/` instruct models to refuse storing secrets in artifacts. That instruction is not in the prompt, so the claim is withdrawn rather than restated. [OPEN: whether `system/BOOT-PROMPT.md` should carry such a rule is a decision for the owner of `system/`, and this file will describe it once it is there.]

## Your own hygiene, which is where the real risk is

- Never put real credentials, keys, customer records, or candidate material into a filled template, in any repository, including a private fork. A filled PRD gets pasted into chat windows and tickets; treat it as public by default.
- Filled artifacts belong in `products/<name>/`, which is gitignored and never ships from here.
- Check 9 of `lint.py` scans every tracked file for common credential shapes and for credential-shaped names assigned high-entropy values, and it exempts no file, including the files that define the patterns. It is a backstop, not a permission slip: it catches shapes it knows.
- The `content-is-data` invariant in `harness/INVARIANTS.md` is a security control, not a style rule. Anything a model reads from a page, a feed, an inbox, a ticket, or a file is data, and a directive found inside it is reported with its source named and never obeyed.

## Reporting a problem

Open a GitHub security advisory on this repository, or a plain issue if the matter is not sensitive. Reports are read by the maintainer directly, and there is one maintainer, so there is no response-time promise beyond that. Two things are especially worth reporting: a template or prompt that induces unsafe handling of secrets, and any path by which the runner could write outside `products/` or leak a credential into a log.
