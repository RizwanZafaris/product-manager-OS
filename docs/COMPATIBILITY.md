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
- Temperature 0, and at most 1024 output tokens. A model that cannot answer
  these eight small cases inside that cap fails the case it could not finish.
- The model id is pinned. An alias such as `auto/coding:free` is excluded,
  because the model that answered would be unknown and a row about an unknown
  model is a row about nothing.
- Gateway compression, semantic cache and memory injection are off, so the
  prompt the model saw is the prompt recorded and the answer is not a replay.
- Free tier only. Any call reporting a cost above zero aborts the run.

Reproduce it with the local gateway running:

```bash
python3 tools/model_matrix.py --list-models     # the selection and the exclusions
python3 tools/model_matrix.py                   # the run; writes docs/readiness/model-matrix.json
python3 tools/model_matrix.py --render          # rewrite the table below from that file
python3 tools/model_matrix.py --check           # prove the table below matches the file
```

### The table

<!-- BEGIN GENERATED: model-matrix -->
Not yet generated. Run `python3 tools/model_matrix.py --render`.
<!-- END GENERATED: model-matrix -->

### How to read a row

A pass count is not a quality score and does not transfer to work outside these
eight cases. What a row supports is a narrower and more useful judgement: which
tier in [harness/tiers.md](../harness/tiers.md) a model may be routed to.

- A model that fails **json-extract** or **field-gap** cannot be trusted with
  extraction work, which is the tier whose entire premise is that the answer is
  checkable against the input.
- A model that fails **not-stated** or **quoted-instruction** must not be given
  retrieved or customer-supplied material, whatever else it scores. Those two
  cases are the `no-fabrication` and `content-is-data` invariants in
  [harness/INVARIANTS.md](../harness/INVARIANTS.md), asked as questions.
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

## The execution-host matrix

| Host | What it gives you | Tested by | Not proven |
|---|---|---|---|
| A text editor, no model | Every template, framework, knowledge card and gate | The whole tree gate, `python3 lint.py --os` | Nothing is claimed beyond documents; that is the point |
| `pmos` runtime | Local store, conductor, domain model, hooks, routing | The root unit suites on Python 3.11 and 3.13 in CI | Multi-machine coordination; it is a local runtime |
| Claude Code plugin | One slash command per route, generated from the manifest | `python3 harness/adapters/claude-code/generate.py --check` in CI | That a live Claude Code session loads the plugin and a human drives a route end to end |
| Desktop MCP server | One MCP tool per route, generated at server start | `python3 harness/adapters/desktop/selftest.py` in CI | That a desktop client accepts the handshake, or that a tool call round trips over stdio |
| CLI adapter | The same route list at a shell prompt | Compilation of every tracked Python file in CI | An end-to-end session driven by someone other than a maintainer |
| OpenRouter runtime path | Tier-routed model calls through a local gateway | The model matrix above, and [tools/ext_ai_probe.py](../tools/ext_ai_probe.py) | Any provider other than the one measured |

Operating systems: the hosted gate runs on `ubuntu-latest`; the model matrix
above was run on macOS. There is no Windows evidence in this repository, so
there is no Windows row. Absence of a row is the honest form of that.

## The workflow matrix

A workflow is a route in [harness/MANIFEST.json](../harness/MANIFEST.json). Its
tier says what catches a wrong answer and when, which is the only question that
decides whether a given model may run it, see
[routing/README.md](../routing/README.md) for the doctrine and
[harness/tiers.md](../harness/tiers.md) for the decision procedure.

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

## Limits of this document

- Eight cases are eight cases. They were chosen because each one maps to an
  invariant or a tier the OS already depends on, not because they cover PM work.
- One run per cell. Free-tier capacity varies through the day, and a single
  sample cannot separate a model that fails a case from a model that failed a
  minute. A repeated bounded subset belongs here and is not here yet.
- Only free models were measured, because the release contract for this work
  set an incremental spend of zero. Paid models are therefore untested here,
  which is not a statement about them.
- The generated table is only as current as the run recorded in
  `docs/readiness/model-matrix.json`. `python3 tools/model_matrix.py --check`
  fails when the two disagree, so a stale table cannot pass quietly, but a
  table nobody re-ran after a provider changed its catalog is still a table
  about the day it was run.
