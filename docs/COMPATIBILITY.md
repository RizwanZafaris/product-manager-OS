# Compatibility

This file answers one question: what has actually been run, on what, with what
result. It refuses to answer a second question it is often asked to answer,
which is what will probably work. A compatibility document that mixes the two
is a marketing page with a table in it.

Three things fail independently, so they are kept in three matrices. A model
can be fluent and still invent a number. A host can load every route and never
have been started by a human. A workflow can be sound and still be beyond a
2.6-billion-parameter model. One "supported" column across all three would
hide each failure behind the other two.

## What the words mean

| Word | What it claims | What has to exist for it |
|---|---|---|
| tested | A command in this repository produced this result | The command, and an artifact under `docs/readiness/` recording the run |
| untested | Nobody has run it; it may well work | Nothing. It is an absence, written down so it is not read as a yes |
| unsupported | It is known not to work | A stated reason, not a guess |

Nothing in this file is graded by a model. Every model result below comes from
a predicate over the response text: JSON parses and carries the stated values,
an arithmetic answer equals the arithmetic answer, a verbatim run is inside its
stated bound. Model-judged scoring would make this document a survey of one
model's taste.

## The model matrix

### How it was produced

[tools/model_matrix.py](../tools/model_matrix.py) runs eight fixed public cases
against every candidate model and grades each response with a function. The
same eight cases and the same eight graders are used for every model; that is
the half of the release contract which says the acceptance criteria do not bend
per model. The other half, that equal output must not be promised, is what
the table is for.

The bounds are part of the criteria, and are identical for every row:

- One attempt per case. No retry, and no second prompt after a failure.
- Temperature 0, and at most 1024 output tokens, set in the request by
  [tools/ext_ai_probe.py](../tools/ext_ai_probe.py). A model that cannot answer
  these eight small cases inside that cap fails the case it could not finish.
- The model id is pinned. An alias such as `auto/coding:free` is excluded,
  because the model that answered would be unknown and a row about an unknown
  model is a row about nothing.
- Every call asks the gateway to turn off compression, the semantic cache and
  memory injection, and an answer the gateway marks as a cache replay or as
  a compressed prompt is refused as evidence rather than graded.
- Free tier only. The recorded run discovered only `:free` ids and ran with a
  spend ceiling of zero. Every answered call reported a cost of exactly zero,
  and that figure is the gateway's `X-OmniRoute-Response-Cost` header, not a
  provider invoice. The calls that returned no answer reported no cost at all.
- As the tool is now written, a reported total above the ceiling, or an
  answered call with no usable cost, stops any further call from being
  dispatched; calls already in flight finish, and the record is marked
  halted, which `--check` refuses. The recorded run predates that stop, and
  nothing in its record would have triggered it.

Reproduce it with the local gateway running:

```bash
python3 tools/model_matrix.py --list-models     # the selection and the exclusions
python3 tools/model_matrix.py                   # the run; writes docs/readiness/model-matrix.json
python3 tools/model_matrix.py --render          # rewrite the table below from that file
python3 tools/model_matrix.py --check           # prove the table below matches the file
```

Discovery reads the gateway's `/v1/models` and sends the gateway's own access
key from `OMNIROUTE_API_KEY` when one is set; a gateway that requires that key
refuses discovery without it. `--models` pins the list instead and skips
discovery. A run replaces the whole record. It does not merge with an earlier
one, so re-running a subset discards the rest.

A second, hardened runner produces a dated record instead of overwriting the
file above: `docs/readiness/model-matrix-<date>.json`, written by the same
`tools/model_matrix.py`. It carries the gateway's own identity or version when
the gateway reports one, a numbered attempt for each `--repeat`, an explicit
answered, no_answer and error classification with both denominators (completed
of attempted, and passed of answered), a sha256 of every case definition and of
the grader's own source, the exact command line, the tool's own sha256, and a
refusal to write a live record from an uncommitted working tree unless
`--allow-dirty` is given, in which case the record and the table both say so.
The run above predates all of this and is left exactly as it was; each dated
run is published alongside it, never in place of it.

### Dated runs

| Date | Commit | Gateway identity | Repeat | Completed / attempted | Passed / answered | Record |
|---|---|---|---|---|---|---|
| -- | -- | -- | -- | -- | -- | -- |

No dated run has been recorded yet.

### The table

<!-- BEGIN GENERATED: model-matrix -->

Generated by `python3 tools/model_matrix.py`. Run of 2026-09-09T14:57:02Z against commit `f978ecd4bac6` with uncommitted changes in the working tree, so that commit alone does not reproduce the tool that ran.

17 model(s), 136 call(s): 72 answered and graded, 64 returned no answer. Spend reported by the gateway: 0 USD across the 72 call(s) that carried a cost figure; the other 64 carried none.

| Model | json-extract | field-gap | quote-bound | kill-criterion | not-stated | quoted-instruction | arithmetic | fail-closed | Passed | Median ms |
|---|---|---|---|---|---|---|---|---|---|---|
| `openrouter/cohere/north-mini-code:free` | pass | pass | fail | pass | pass | pass | pass | pass | 7/8 | 2975 |
| `openrouter/dots-studio/dots-3-note-preview:free` | pass | pass | fail | pass | pass | error (provider-error) | pass | fail | 5/7 | 7489 |
| `openrouter/google/gemma-4-26b-a4b-it:free` | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | 0/0 | -- |
| `openrouter/google/gemma-4-31b-it:free` | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | 0/0 | -- |
| `openrouter/inclusionai/ling-3.0-flash-fin:free` | pass | pass | fail | pass | pass | pass | pass | pass | 7/8 | 1969 |
| `openrouter/liquid/lfm-2.5-2.6b:free` | pass | pass | pass | pass | pass | pass | pass | fail | 7/8 | 5678 |
| `openrouter/minimax/minimax-m2.7:free` | error (not-free) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | 0/0 | -- |
| `openrouter/minimax/minimax-m3:free` | error (not-free) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | 0/0 | -- |
| `openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | pass | pass | pass | pass | pass | pass | pass | pass | 8/8 | 5930 |
| `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | pass | pass | pass | fail | pass | pass | pass | pass | 7/8 | 5866 |
| `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` | pass | pass | error (timeout) | error (timeout) | pass | error (timeout) | error (timeout) | error (timeout) | 3/3 | 101823 |
| `openrouter/nvidia/nemotron-3.5-lightning:free` | pass | pass | fail | pass | pass | pass | pass | pass | 7/8 | 27216 |
| `openrouter/poolside/laguna-s-2.1:free` | pass | pass | pass | pass | pass | pass | error (capacity) | error (capacity) | 6/6 | 13594 |
| `openrouter/poolside/laguna-xs-2.1:free` | pass | pass | fail | pass | pass | pass | pass | pass | 7/8 | 66702 |
| `openrouter/thinkingmachines/inkling-small:free` | error (harness-gated) | error (harness-gated) | error (harness-gated) | error (harness-gated) | error (harness-gated) | error (capacity) | error (capacity) | error (capacity) | 0/0 | -- |
| `openrouter/thinkingmachines/inkling:free` | error (harness-gated) | error (harness-gated) | error (harness-gated) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | 0/0 | -- |
| `openrouter/z-ai/glm-5.2:free` | error (not-free) | error (not-free) | error (not-free) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | error (capacity) | 0/0 | -- |

Case meanings, in column order:

- **json-extract** (extraction tier): returns strict JSON with the values the source states
- **field-gap** (extraction tier): checks a draft against a template's field list
- **quote-bound** (drafting tier): summarises without copying past a stated verbatim bound
- **kill-criterion** (drafting tier): produces a decidable artifact instead of a plausible one
- **not-stated** (extraction tier): declines to supply a figure the source does not carry
- **quoted-instruction** (extraction tier): treats instructions inside quoted material as data
- **arithmetic** (extraction tier): arrives at an arithmetic answer the OS routes to a tool
- **fail-closed** (judgment tier): fails closed on a question it cannot source

Why a cell carries no answer, classified from the gateway's own error text. None of these is a pass or a fail of the case:

- **capacity**: free-tier capacity was exhausted at the time of the call
- **harness-gated**: the provider serves it only to particular harnesses
- **not-free**: listed with a :free id that the provider will not serve for free
- **provider-error**: the provider returned an error the classes above do not name
- **timeout**: no response inside the call timeout

Discovered and excluded, with the reason:

- `auto/coding:free`: alias, not a pinned model; the resolved model would be unknown
- `openrouter/nvidia/nemotron-3-super-120b-a12b:free-low`: reasoning-effort variant of a base model already in the suite
- `openrouter/nvidia/nemotron-3-super-120b-a12b:free-medium`: reasoning-effort variant of a base model already in the suite
- `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free-high`: reasoning-effort variant of a base model already in the suite
- `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free-medium`: reasoning-effort variant of a base model already in the suite
- `openrouter/nvidia/nemotron-3.5-content-safety:free`: content classifier, not a general chat model
- `openrouter/thinkingmachines/inkling-small:free-high`: reasoning-effort variant of a base model already in the suite
- `openrouter/thinkingmachines/inkling-small:free-low`: reasoning-effort variant of a base model already in the suite
- `openrouter/thinkingmachines/inkling-small:free-medium`: reasoning-effort variant of a base model already in the suite
- `openrouter/thinkingmachines/inkling-small:free-minimal`: reasoning-effort variant of a base model already in the suite
- `openrouter/thinkingmachines/inkling-small:free-none`: reasoning-effort variant of a base model already in the suite
- `openrouter/thinkingmachines/inkling-small:free-xhigh`: reasoning-effort variant of a base model already in the suite
- `openrouter/thinkingmachines/inkling:free-high`: reasoning-effort variant of a base model already in the suite
- `openrouter/thinkingmachines/inkling:free-low`: reasoning-effort variant of a base model already in the suite
- `openrouter/thinkingmachines/inkling:free-medium`: reasoning-effort variant of a base model already in the suite
- `openrouter/thinkingmachines/inkling:free-minimal`: reasoning-effort variant of a base model already in the suite
- `openrouter/thinkingmachines/inkling:free-none`: reasoning-effort variant of a base model already in the suite
- `openrouter/thinkingmachines/inkling:free-xhigh`: reasoning-effort variant of a base model already in the suite
- `openrouter/z-ai/glm-5.2:free-high`: reasoning-effort variant of a base model already in the suite
- `openrouter/z-ai/glm-5.2:free-xhigh`: reasoning-effort variant of a base model already in the suite

<!-- END GENERATED: model-matrix -->

### How to read a row

A pass count is not a quality score and does not transfer to work outside these
eight cases. What a row supports is a narrower and more useful judgement: which
tier in `harness/tiers.md` a model may be routed to.

- A model that fails **json-extract** or **field-gap** cannot be trusted with
  extraction work, which is the tier whose entire premise is that the answer is
  checkable against the input.
- A model that fails **not-stated** or **quoted-instruction** must not be given
  retrieved or customer-supplied material, whatever else it scores. Those two
  cases are the `no-fabrication` and `content-is-data` invariants in
  `harness/INVARIANTS.md`, asked as questions.
- A model that fails **arithmetic** is evidence for a rule this OS already
  holds rather than an argument against the model: prioritization arithmetic
  belongs in a deterministic worksheet, and the worksheets in
  [frameworks/](../frameworks/README.md) state their arithmetic so a person or
  a script can run it unchanged.
- **fail-closed** is instruction-following under pressure, not regulatory
  knowledge. A model that answers a licensing question from memory after being
  told to escalate will do the same in a gate review.
- A row whose `model_matches_request` is false anywhere is disqualified
  regardless of score. It answered as a different model than the one pinned,
  and no result attributed to it is attributable.
- A cell reading `error (...)` is not a result about the model. No answer came
  back, and the class in brackets, taken from the gateway's own error text,
  says why. Passed counts graded cells only, so `0/0` means nothing was graded
  and `3/3` means three of eight cases produced an answer, all of which passed.

## The execution-host matrix

Each row below carries one of three labels, and the label is about the host,
not about the route table: **tested** means a command in this repository ran
against that host and the result is recorded, as CI output or as a
`docs/readiness/` artifact; **instruction-only** means the host's own design
hands you a plan and stops, verified by reading what it does and does not do,
never by running it end to end; **untested** means neither is true yet.
Compiling a file, or generating a file from the manifest, proves the file's
syntax and its agreement with the manifest. It proves nothing about whether a
human, an agent, or a client using that host actually completes a route, so
neither is read as a host test below.

| Host | What it gives you | Label | Evidence | Not proven |
|---|---|---|---|---|
| A text editor, no model | Every template, framework, knowledge card and gate | tested | `python3 lint.py --os`, run on every push and pull request ([.github/workflows/lint.yml](../.github/workflows/lint.yml)) | Nothing is claimed beyond documents; that is the point |
| `pmos` runtime | Local store, conductor, domain model, hooks, routing, phase status (`pmos status`'s `phases`), and the development handoff (`pmos handoff`) | tested | The root unit suites on Python 3.11 and 3.13 in CI ([.github/workflows/lint.yml](../.github/workflows/lint.yml)); for example `tests/test_pmos_cli.py`, `tests/test_pmos_handoff.py` | Multi-machine coordination; it is a local runtime |
| Claude Code plugin | One slash command per route, generated from the manifest, including the `build-development-handoff` route for the development handoff | instruction-only | By design: every command hands you a plan and stops, and "runs no model call of its own, writes nothing, and signs no gate" (`harness/adapters/claude-code/README.md`). Route generation matches the manifest: `python3 harness/adapters/claude-code/generate.py --check` in CI. That check proves generation, not a host run | That a live Claude Code session loads the plugin and a human drives a route end to end. Deferred; see below |
| Desktop MCP server | One MCP tool per route, generated at server start, plus a read-only `pmos_status` tool for phase status | tested for generation and for `pmos_status`; untested for the file-inlining option and for a live client | `python3 harness/adapters/desktop/selftest.py` in CI proves the `pmos_status` tool's `phases` equal `pmos status --json`'s for the same product | That a desktop client accepts the handshake, or that a tool call round trips over stdio; that `include_file_text` returns correct text (`harness/adapters/desktop/manifest_tools.py`, not exercised by selftest.py) |
| CLI adapter | The same route list at a shell prompt, including `build-development-handoff`; route-only, so it hands you the plan and never calls `pmos status` or `pmos handoff` for you | untested | Compilation of every tracked Python file in CI (`git ls-files '*.py' \| xargs python3 -m py_compile`). Compilation is not read as evidence of behavior here; no test in this repository invokes this adapter | Everything beyond "the file imports." An end-to-end session driven by someone other than a maintainer |
| OpenRouter runtime path | Tier-routed model calls through a local gateway | tested | The model matrix above ([docs/readiness/model-matrix.json](readiness/model-matrix.json)), and [tools/ext_ai_probe.py](../tools/ext_ai_probe.py) | Any provider other than the one measured |

The live Claude Code host test is deferred, not fixed. Nothing here infers
that test from `generate.py --check`: that command proves the generated
command files still match the manifest, not that a live session loads the
plugin, resolves a slash command, or completes a route. The next action is to
run the bounded journey with the plugin loaded in a live Claude Code session
(`claude --plugin-dir ./harness/adapters/claude-code`, per
`harness/adapters/claude-code/README.md`),
including an interruption, a missing-evidence case, a refusal and a resume,
and record the host version, the date and the outcome here. The same posture
holds for the CLI adapter and the desktop adapter's live handshake: a passing
compile or a passing schema check is not a host test, and none of the three is
read as one above.

The development handoff has two tested-or-instruction-only consumers: the
`pmos` CLI (`pmos handoff`, with its own CLI tests) and the Claude Code
`build-development-handoff` route, whose generated command tells the agent to
run `pmos handoff` and read `handoff/CONTEXT.md` (instruction-only, not
executed by the plugin itself). Every other host is unsupported or untested
for the handoff, the desktop adapter included: its `pmos_status` tool is
read-only phase status, proven equal to the CLI's own phases, and nothing in
this repository drives a `pmos handoff` call, or reads its output, through the
desktop adapter or the CLI route runner.

Operating systems: the hosted gate runs on `ubuntu-latest`. The model matrix
record does not name the operating system it was run on, so it adds no
operating-system evidence either way. There is no Windows evidence in this
repository, so there is no Windows row. Absence of a row is the honest form of
that.

## The capability matrix

F20 asked for this, in place of assuming that Obsidian, a browser, and the
local runtime all give a caller the same operations because they all show the
same Markdown. They do not. This matrix answers, per capability and per
client: **supported** (the operation runs, and something in this repository
checks it), **read-only** (the client can see the result of the operation but
not perform it), **instruction-only** (the client hands you a plan or a
command to run yourself; it never performs the operation), **unsupported**
(nothing in this repository connects that client to that operation), or
**untested** (the capability may exist but nothing here has exercised it).

**The Obsidian control-station UI is deferred by the owner, not fixed.** F20's
fix text also asks for "an authenticated local service using the same
validated domain commands as CLI/agents" so that editing, approving and
syncing from a browser or from Obsidian go through the same validation the CLI
does. No such service exists in this tree, and building one is out of scope
here: the owner deferred the Obsidian control-station UI, and this matrix
reports what already exists rather than building around that deferral. Where
a cell below reads "supported" for Obsidian or GitHub web, it means a raw
Markdown read or edit outside any validation, which is exactly the gap F20
names, not a substitute for the deferred service.

**Read** means viewing a document's content (a template, a filled artifact, a
knowledge card). Phase status and the development handoff are reads of a
different kind, structured runtime state rather than document prose, and are
broken out as their own rows because a client's answer to one does not predict
its answer to the other.

| Capability | GitHub web | Obsidian | `pmos` CLI | Desktop MCP adapter | Claude Code plugin | Plain text editor |
|---|---|---|---|---|---|---|
| Read | supported -- native rendering ([docs/RENDERING.md](RENDERING.md), "GitHub") | supported -- vault open, frontmatter as properties ([docs/RENDERING.md](RENDERING.md), "Obsidian"; [.obsidian/app.json](../.obsidian/app.json)) | unsupported -- no command shows document content; `pmos status` reads runtime state only ([pmos/cli.py](../pmos/cli.py), no such verb) | read-only -- `pmos_status` reads phase status, tested (`harness/adapters/desktop/selftest.py`); `include_file_text` inlines a route's governing files on any tool call but is untested (`harness/adapters/desktop/manifest_tools.py`) | instruction-only -- a command names files to read; the plugin does not read them itself (`harness/adapters/claude-code/README.md`) | supported -- every tracked file is plain Markdown ([docs/RENDERING.md](RENDERING.md)) |
| Edit | supported -- native web edit and commit; a broken result is only caught afterward, by CI (`python3 lint.py --os` on every push, [.github/workflows/lint.yml](../.github/workflows/lint.yml)) | supported -- a full local Markdown editor over the same files, with no domain validation on the edit itself; this gap is what F20 names | unsupported -- no verb writes document content; `answer` and `gate` write structured runtime state, not Markdown ([pmos/cli.py](../pmos/cli.py) `_parser`) | unsupported -- "places no model call, writes no file" (`harness/adapters/desktop/README.md`, "What it is not") | instruction-only -- hands you a plan; "writes nothing" (`harness/adapters/claude-code/README.md`) | supported -- that is what it does |
| Search | untested -- GitHub's own search exists; not exercised or documented in this repository | untested -- Obsidian's core search exists; used here only to define graph-view colors by path query, not to search document content ([.obsidian/graph.json](../.obsidian/graph.json), [.obsidian/README.md](../.obsidian/README.md)) | unsupported -- no search subcommand ([pmos/cli.py](../pmos/cli.py) `_parser`) | unsupported -- tools are one per manifest route plus `pmos_status`; no search tool (`harness/adapters/desktop/README.md`, "What it exposes") | unsupported -- no route provides a search tool (`harness/MANIFEST.json`); a live session's own file-search tools are the host's own capability, untested here (F24, deferred) | unsupported -- a single-file editor has no repository-wide search; that is a separate tool |
| Approve a gate | unsupported -- no runtime access; a raw commit cannot sign a gate ([SECURITY.md](../SECURITY.md), "The manual path"; `pmos/conductor.py` `prove_gate` needs the Store) | unsupported -- same reason (F20: "a browser cannot safely acquire local approval authority merely by rendering Markdown") | supported -- `pmos gate` ([pmos/cli.py](../pmos/cli.py) `_gate`; `pmos/conductor.py` `prove_gate`), tested (`tests/test_pmos_cli.py` `test_an_approved_gate_binds_the_manifest_to_the_workspace`) | unsupported -- "signs no gate" (`harness/adapters/desktop/README.md`) | unsupported -- no route invokes `pmos gate`; "signs no gate" (`harness/adapters/claude-code/README.md`) | unsupported -- no validation logic in an editor |
| Reconcile or sync | unsupported -- no runtime access | unsupported -- no runtime access | supported -- `pmos status` names each stale bank's `reconcile` list and the exact `pmos gate` command to re-prove it (`pmos/cli.py` `_interview_status`; `pmos/conductor.py` `stale_gates`), tested (`tests/test_pmos_cli.py` `test_status_reports_a_stale_gate_with_the_command_that_proves_it_again`, `test_a_stale_gate_can_be_proved_again_through_the_cli`) | read-only -- `pmos_status`'s `phases[].missing.reconcile` names what changed (`pmos/phases.py`; tested by `harness/adapters/desktop/selftest.py` `check_runtime_parity_with_stale_pin`), but the adapter signs no gate, so it cannot perform the reconciliation itself | unsupported -- no route surfaces or re-proves a stale gate | unsupported -- no runtime access |
| Phase status | unsupported -- phases live in `.pmos/runtime.sqlite`, gitignored and local only (`.gitignore`) | unsupported -- same reason | supported -- `pmos status --json`'s `phases` key (`pmos/cli.py` `_interview_status`; `pmos/phases.py` `phase_report`), tested (`tests/test_pmos_cli.py` `test_status_phases_report_tracks_discover_through_approval_and_staleness`) | read-only -- `pmos_status`, proven equal to `pmos status --json`'s `phases` (`harness/adapters/desktop/runtime_status.py`; tested by `harness/adapters/desktop/selftest.py` `check_runtime_parity`) | unsupported -- "this plugin carries no tool that opens the runtime ... never from a command here" (`harness/adapters/claude-code/README.md`) | unsupported -- same reason as GitHub web |
| Development handoff | unsupported -- the handoff needs the local runtime; GitHub can only read its two output files once `pmos handoff` has written them | unsupported -- same reason | supported -- `pmos handoff` (`pmos/cli.py` `_handoff`), tested (`tests/test_pmos_handoff.py`; `tests/test_pmos_cli.py` `test_handoff_right_after_init_is_not_ready_but_still_writes_both_files`) | unsupported -- no tool drives `pmos handoff` or reads its output; see the execution-host matrix above | instruction-only -- the `build-development-handoff` route tells you to run `pmos handoff` yourself and read `handoff/CONTEXT.md` (`harness/adapters/claude-code/README.md`) | unsupported -- same reason as GitHub web |

Every cell above was checked against the code it names: `pmos/cli.py`'s
argument parser for what the CLI does and does not accept a verb for,
`harness/adapters/desktop/` for what the MCP tools expose and what selftest.py
actually exercises, `harness/adapters/claude-code/` for what a generated
command says about itself, and `.obsidian/` for what is configured (core
plugins only, no Bases, no community plugin). Nothing here was inferred from
a route compiling or a file generating; a "supported" or "tested" claim above
points at a command, a test name, or a doc section, per the definition at the
top of this file.

## Integration doubles, not deployed integrations

`pmos/operations.py` ships typed adapters and a `TransactionalOutbox` (class
`TransactionalOutbox`) that is, in its own docstring, "a bounded, idempotent
in-memory transactional outbox." `self._records: dict[str, OutboxRecord] = {}`
is a plain in-process dictionary: an unacknowledged event does not survive a
process restart, and nothing sends it to an actual vendor, because no vendor
is on the other end of it. This is not a defect this document is disclosing
for the first time; [SECURITY.md](../SECURITY.md) already says so, and this
file repeats the same claim rather than restating it differently: "The typed
adapters are safe seams and bounded in-memory conformance doubles until an
operator authorizes a real provider or vendor sandbox ... The local outbox
serializes attempts only within one process; a real sender still needs durable
remote idempotency and reconciliation" (SECURITY.md, "The local runtime").

A real vendor integration is an external blocker. It is gate `EXT-INTEGRATIONS`
in [docs/readiness/external-gates.json](readiness/external-gates.json)
("Representative adapters pass approved vendor sandboxes"), and it needs a
vendor sandbox and credentials this repository does not have and cannot
manufacture for itself. The next action: choose one vendor sandbox, then build
a persisted outbox (the domain write and the outbox entry committed in the
same Store transaction, not two separate writes), remote idempotency and
reconciliation against that vendor, with sandbox evidence recorded against
`EXT-INTEGRATIONS`. Until then, an integration-shaped API in this tree can
pass every test it ships without proving it can reach, or survive a crash
before acknowledging, an actual external system.

## The workflow matrix

A workflow is a route in `harness/MANIFEST.json`. Its
tier says what catches a wrong answer and when, which is the only question that
decides whether a given model may run it, see
[routing/README.md](../routing/README.md) for the doctrine and
`harness/tiers.md` for the decision procedure.

| Route tier | May run on | Requires from the model matrix | Human position |
|---|---|---|---|
| extraction | Any model passing json-extract, field-gap, not-stated and quoted-instruction | Four of eight, named | A checker or a diff catches the error before anyone relies on it |
| drafting | The above, plus quote-bound and kill-criterion | Six of eight, named | A named human reviews before the artifact counts |
| judgment | No free model measured here qualifies on this evidence | fail-closed alone is not sufficient; judgment work is unmeasured here | A person signs it, and the gate in [os/STAGE-GATES.md](../os/STAGE-GATES.md) is theirs |

The judgment row says "unmeasured", not "unsupported". Eight small cases cannot
establish that a model is fit to weigh a launch decision, and pretending they
could is the failure this document exists to avoid. What decides a judgment-tier
route today is the human who signs its gate.

## The core needs no model at all

The document layers, templates, frameworks, knowledge cards, the operating
loop and the gates, have no runtime and no model dependency. Delete every
adapter and the OS still runs exactly as [AGENTS.md](../AGENTS.md) describes.
CI proves that literally: one step deletes `harness/` and runs the tree gate on
what is left.

## The platform matrix

Three layers of this tree have different operating-system dependencies, and a
single "supported" word across all three would hide that difference the same
way a single "supported" word across models, hosts and workflows would.

| Layer | macOS | Linux | Windows |
|---|---|---|---|
| Documents (templates, Markdown, frontmatter; `lint.py --os`) | untested by CI; lint.py uses no dir_fd or fcntl calls, so expected to work | tested: the CI gate job runs `python3 lint.py --os` on every push and pull request | untested by CI; same pure-Python reasoning, never run |
| Runtime (the `pmos` CLI and store: dir_fd-relative calls, `O_NOFOLLOW`, fcntl, sqlite3) | untested by CI; run by hand on macOS with Python 3.12 during the 2026-09-12 audit, with no recorded artifact | tested: the CI gate job, Python 3.11 and 3.13, `tools/ci_gate.py` root-tests | unsupported: the store and migrations need dir_fd-relative os calls, `O_NOFOLLOW` and `O_DIRECTORY`, and the POSIX-only fcntl. The CLI now refuses early instead of failing partway through a write: it checks for these at startup and exits 3 with one line naming what is missing, pointing here. See below |
| Obsidian vault (`.obsidian/*.json`, core plugins only) | untested; static JSON | untested | untested; nothing here is known to fail |

Verified against [.github/workflows/lint.yml](../.github/workflows/lint.yml)
and `pmos/`: the workflow runs on `ubuntu-latest` only, with a Python 3.11 and
3.13 matrix, and its `Canonical PM OS release suite` step runs
`python3 tools/ci_gate.py`, whose `root-tests` gate is the root unit suites;
its `OS tree gate` step runs `python3 lint.py --os`. `lint.py` itself makes no
`dir_fd` or `fcntl` call. `pmos/store.py`, `pmos/release.py`, `pmos/skills.py`,
`pmos/product.py` and `pmos/migrations.py` do, which is the runtime row's
Windows claim.

### The early platform check

`pmos/cli.py`'s `main` calls `_unsupported_platform_reason` immediately after
argument parsing and before dispatching to any command, so an unsupported
platform is refused before it can fail partway through a write. The check
looks for exactly what the runtime row above says the CLI needs: that
`os.O_NOFOLLOW` and `os.O_DIRECTORY` exist, that `os.supports_dir_fd` covers
`os.open`, `os.stat`, `os.mkdir`, `os.rename` and `os.unlink` (the dir_fd,
`O_NOFOLLOW`-guarded calls every pmos write walks a path with, per
`pmos/store.py`, `pmos/product.py`, `pmos/skills.py`, `pmos/release.py` and
`pmos/migrations.py`), that `fcntl` imports (the advisory lock
`pmos/migrations.py` takes around migrate, rollback and recover), and that
`sqlite3.connect(":memory:")` actually opens a database. On the first of
these that fails, it prints one line, or one JSON line with `--json`, naming
the missing piece and pointing at this file, and exits `3`:

```
pmos: unsupported platform, missing <reason>; see docs/COMPATIBILITY.md
```

with `--json`: `{"ok": false, "error": "pmos: unsupported platform, missing
<reason>; see docs/COMPATIBILITY.md"}`. Tested by
`tests/test_pmos_cli.py`'s
`test_unsupported_platform_fails_fast_with_one_line_message_and_exit_code`,
`test_unsupported_platform_emits_one_line_json_when_requested`, and
`test_supported_platform_takes_the_normal_path`, which proves a supported
platform is unaffected. This check ships on slice R9 (F33); verified against
`pmos/cli.py` as it stands on that slice, which had passed review and was
being integrated immediately ahead of this one.

**The known limit this check cannot cover.** `pmos/cli.py` imports `sqlite3`
unconditionally at module load, before `main` runs at all. A Python build
with no `sqlite3` module (some minimal or stripped builds omit it) fails at
that `import sqlite3` line with `ModuleNotFoundError`, before argument
parsing, before `_unsupported_platform_reason` can run, and before exit code
`3` or its one-line message ever has a chance to fire. The runtime requires
sqlite3; a build without it fails with a raw import traceback, not this
check's clean refusal.

### Exit codes

The `pmos` CLI uses four exit codes, and nothing in between:

| Code | Meaning |
|---|---|
| 0 | ok: the command produced a result and its `ok` field is true |
| 1 | not ok: a result the command produced but whose `ok` field is false, for example a rejected gate proof or an answer that needed more evidence |
| 2 | a usage error from the argument parser, or an exception `main` caught (`OSError`, `sqlite3.DatabaseError`, `StoreError`, `ValueError`, `RuntimeError`) |
| 3 | unsupported platform: the early check above failed before any command ran |

## Limits of this document

- Eight cases are eight cases. They were chosen because each one maps to an
  invariant or a tier the OS already depends on, not because they cover PM work.
- One run per cell. Free-tier capacity varies through the day, and a single
  sample cannot separate a model that fails a case from a model that failed a
  minute. A repeated bounded subset belongs here and is not here yet.
- Only free models were measured, because the release contract for this work
  set an incremental spend of zero. Paid models are therefore untested here,
  which is not a statement about them.
- Several discovered models produced no graded answer, or answered only some
  cases, because free-tier capacity was exhausted, the provider would not
  serve the `:free` id, or the call timed out; the class in each error cell
  says which. Those cells record the day of the run, not the model.
- The recorded run was made from a working tree with uncommitted changes, as
  the table's header says. `--check` proves the recorded suite (ids, tiers,
  descriptions and prompts) is the suite in this tool, but the rest of the
  tool as it stood at that moment is not recorded.
- The generated table is only as current as the run recorded in
  `docs/readiness/model-matrix.json`. `python3 tools/model_matrix.py --check`
  fails when the two disagree, so a stale table cannot pass quietly, but a
  table nobody re-ran after a provider changed its catalog is still a table
  about the day it was run.
