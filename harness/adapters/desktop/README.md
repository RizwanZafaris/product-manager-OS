# Desktop MCP adapter

An MCP server that exposes one tool per entry in [MANIFEST.json](../../MANIFEST.json), so any desktop client that speaks MCP gets the same task list, off the same contract, as the CLI and the agent runtime.

The tools are generated at server start by reading the manifest. Nothing is hand listed. A hand listed tool set would be a second source of truth, and the two would drift the first time a router row changed.

## What it exposes

| Item | Detail |
|---|---|
| Tools | One per manifest entry, currently 41. The tool name is the entry id, verbatim, so ids and tools count one to one. |
| Description | Built from the entry: the router row, the literal triggers, the stage and gate, the tier, the skill to follow, where output lands, and the invariant ids that bind the run. |
| Result | The plan for that route: skill to follow, files to read first, templates the output lands in, the invariant rules in full, the manifest note, routing readiness, and a JSON block for a machine consumer. |
| Arguments | `request`, the user's own words, quoted back as data. `include_file_text`, off by default, inlines the text of the files under Read first. |

Both arguments are optional and neither one changes the route. The route is the tool you called.

## What it is not

It is a task list and plan surface, not an autonomous runner. A tool call runs no model call, writes no file, sends nothing, and signs no gate. It hands you the plan and the governing files, and you or your client does the work under them.

The gate stays where [INVARIANTS.md](../../INVARIANTS.md) puts it: a named human signs it in [STAGE-GATES.md](../../../os/STAGE-GATES.md). The tier in a description is a tier name, never a model id; the mapping lives in [omniroute.config.json](../../../routing/omniroute.config.json) and nowhere else.

## Point a desktop client at it

Any MCP client that launches a stdio server takes a command and arguments. Use these:

| Field | Value |
|---|---|
| Command | your `python3`, version 3.10 or newer, with the MCP SDK installed |
| Arguments | the absolute path to `harness/adapters/desktop/server.py` |
| Working directory | the repository root, or set `PMOS_ROOT` to it |
| Environment | `OMNIROUTE_BASE_URL` and `OMNIROUTE_API_KEY` if the client will place model calls of its own. This server places none. |

The server finds the repository by walking up from its own file until it sees `harness/MANIFEST.json`, so the working directory usually needs no help. `PMOS_ROOT` overrides that when a client launches from somewhere unrelated.

## Run it and check it yourself

| Command | What it does |
|---|---|
| `python3 harness/adapters/desktop/server.py` | Serves MCP over stdio. Needs the SDK. |
| `python3 harness/adapters/desktop/server.py --list` | Prints the generated tool names, tiers, and stages. Standard library only. |
| `python3 harness/adapters/desktop/server.py --plan write-prd` | Prints one route's plan. Standard library only. |
| `python3 harness/adapters/desktop/selftest.py` | Checks the tool count against the manifest, the schemas, and the SDK-absent path. Exit 1 on any failure. |

## Two ways it fails closed

Before the first tool is generated, the server runs [check_manifest.py](../../../tools/check_manifest.py). If the manifest and the router table in [CLAUDE.md](../../../CLAUDE.md) disagree, or a named path does not resolve, the server prints the first problems and refuses to start. If the checker itself cannot be loaded, that is also a refusal: an unchecked contract is not served. `--no-gate` exists for debugging a broken contract and never for serving.

When a route names a file the tree does not have, the plan carries a halt and queue section instead of a substitute path. Improvising a replacement would be the fabrication the invariants forbid.

## The one dependency, and what happens without it

Standard library, plus the MCP SDK for this adapter only. The import is wrapped, so a missing SDK is a supported state rather than a traceback:

```
product-manager-OS desktop adapter needs the MCP SDK, which is not installed
for this interpreter (No module named 'mcp'). Install it with: python3 -m pip
install mcp (Python 3.10 or newer), then run: python3
harness/adapters/desktop/server.py. Until then use --list or --plan, which
need only the standard library.
```

One line to stderr, exit status 2, and `--list` and `--plan` keep working.

## Credentials

Read from the environment at call time by whatever places a model call. Never written to disk inside this repository, never logged, and never echoed into a tool result. A plan reports presence only: the name and whether it is set.

## Files

| File | Role |
|---|---|
| [manifest_tools.py](manifest_tools.py) | Every decision: tool names, descriptions, schemas, plan text. Imports no SDK, so it is testable with no server and no client. |
| [server.py](server.py) | The thin MCP shell, the agreement gate, and the command line. The only place the SDK is imported. |
| [selftest.py](selftest.py) | What can be checked without a live client. |
