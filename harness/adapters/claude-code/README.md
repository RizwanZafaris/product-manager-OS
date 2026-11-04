# Claude Code plugin adapter

This directory is a Claude Code plugin. It puts the router table of the Product Manager OS in front of you as slash commands, one per route, generated from [../../MANIFEST.json](../../MANIFEST.json).

It adds no procedure. Every command names the `SKILL.md` that owns the work, the templates the output lands in, the files to read first, the gate the output must pass, and the invariant ids that bind the run. The skills themselves are not copied here. `skills` is a symlink to the repository's own [../../../skills](../../../skills) directory, so there is exactly one copy of every skill in the tree and no second copy to drift.

## What it installs

| Component | Path here | Count | Source |
|---|---|---|---|
| Plugin manifest | [.claude-plugin/plugin.json](.claude-plugin/plugin.json) | 1 | Generated. `name` and `version` come from the manifest. |
| Slash commands | `commands/*.md` | 43 | Generated, one per manifest entry, named by its route id. |
| Agent pointers | `agents/*.md` | 11 | Generated, one per role file in `agents/` at the repository root, except `hermes-agent.md`, which is an integration file rather than a role. Each names its role file and adds nothing. |
| Marketplace plugin | [../../../.claude-plugin/](../../../.claude-plugin/plugin.json) | 2 | Generated: `plugin.json` and `marketplace.json` at the repository root. See below. |
| Skills | `skills` | 29 | Symlink to `skills/` at the repository root. Referenced, never copied. Skills under `skills/runtime/` are runtime skills listed in `skills/runtime-manifest.json`. |
| Generator | [generate.py](generate.py) | 1 | Hand written. Standard library only. |

This plugin is route-only. Every command hands you the plan for that route: the skill to follow, the files to read first, the templates the output lands in, and the gate it must pass, then stops. It runs no model call of its own, writes nothing, and signs no gate. `build-development-handoff`, the DESIGN-exit route for the development handoff, is generated the same way as every other command; its plan does not fill the template or run the check for you, it tells you to run `pmos handoff --path <workspace> --product-id <id> --json` yourself and read `handoff/CONTEXT.md` for what the package is still missing. Runtime status works the same way: this plugin carries no tool that opens the runtime, so the `phases` a product is actually in come from the `pmos` CLI (`pmos status`), never from a command here. The desktop MCP adapter is the one adapter with a tool of its own for that, `pmos_status`; see [its README](../desktop/README.md).

Commands are namespaced by the plugin name, so the route ids become `/product-manager-os-harness:write-prd`, `/product-manager-os-harness:run-premortem`, and so on. Read one to see the shape: [commands/write-prd.md](commands/write-prd.md).

Every command sets `disable-model-invocation: true`. That is deliberate. The commands are the face a person types at; model invoked work goes through the skills, which [skills/write-prd/SKILL.md](skills/write-prd/SKILL.md) and its siblings already carry. Claude cannot pick a route on your behalf and skip the row you asked for.

## Install it from the marketplace

This repository is its own Claude Code marketplace. In any project, on Claude Code 2.1.275 or later:

```text
/plugin install pmos --marketplace RizwanZafaris/product-manager-OS
```

Or in two steps on an older version: `/plugin marketplace add RizwanZafaris/product-manager-OS`, then `/plugin install pmos@product-manager-os`.

The marketplace installs a different plugin from the one in this directory, and the difference is deliberate. A plugin installed from a GitHub marketplace is copied into Claude Code's plugin cache, and only the plugin's own directory is copied. Rooted here, it would arrive without the skills, templates and gates every command names, because they sit three levels up. So [../../../.claude-plugin/marketplace.json](../../../.claude-plugin/marketplace.json) lists one plugin, `pmos`, rooted at the repository itself (`"source": "./"`), and [../../../.claude-plugin/plugin.json](../../../.claude-plugin/plugin.json) points its commands at `commands/` here and adds `learn/skills/` to the default `skills/` scan. The cache copy is then the whole tree, about 15 MB, and every command's "Where these paths are" section tells Claude to read from `${CLAUDE_PLUGIN_ROOT}`, which Claude Code substitutes inline, whenever the working directory is not a clone.

| | `pmos` (marketplace) | `product-manager-os-harness` (this directory) |
|---|---|---|
| Installed with | `/plugin install pmos --marketplace RizwanZafaris/product-manager-OS` | `claude --plugin-dir ./harness/adapters/claude-code`, from a clone |
| Works from | Any project | The repository root only |
| Commands | `/pmos:<route>` | `/product-manager-os-harness:<route>` |
| Version | The release version, read from `pyproject.toml` | The route table's version, read from `harness/MANIFEST.json` |

Both manifests and the marketplace file are generated by [generate.py](generate.py), and `--check` covers all three.

Two limits, measured on Claude Code 2.1.318 rather than assumed:

- **Role agents do not load from the marketplace plugin yet.** `plugin.json` lists the generated pointers in `agents/` here, one per role file in [../../../agents/](../../../agents/README.md), because a default scan of the root `agents/` directory would load its README and team protocol as agents. On that version an explicit agents list loaded no agent in a throwaway plugin while the same file in a default `agents/` folder did, so no agent count is claimed anywhere. Reach a role through `/pmos:run-agent-role`. The pointers do load under `--plugin-dir`, where `agents/` here is the default folder.
- **Three names are both a skill and a command:** `write-prd`, `design-review` and `write-vision-strategy`. `claude plugin details pmos` lists each twice. Either one reaches the same skill, because the command only routes to it.

`claude plugin details pmos` measured about 9,500 tokens of always-on descriptions per session on that version.

## Install it locally

Nothing is fetched. The plugin loads from this directory on disk, so it works with no network at install time and no marketplace.

```bash
# From the repository root. One session, nothing written outside the session.
claude --plugin-dir ./harness/adapters/claude-code
```

Start it from the repository root. Every path a command names is repo relative, the way the router table writes them, so the session has to be sitting in the repository for `skills/write-prd/SKILL.md` to mean anything. One route, `tutor-learning-path`, names `learn/skills/tutor/SKILL.md`, which lives outside `skills/` and so is reached through the repository rather than through the plugin's symlink.

Then in the session:

| Step | What you type | What you should see |
|---|---|---|
| List the routes | `/help`, then the custom commands tab | 43 commands under the plugin name |
| Run one | `/product-manager-os-harness:write-prd a PRD for the payout retry screen` | The route card, then the skill it routes to |
| Pick up an edit | `/reload-plugins` | Commands reloaded without restarting |

To validate the plugin without starting a session:

```bash
claude plugin validate ./harness/adapters/claude-code
```

Expect `Validation passed with warnings`. The one warning is that `skills` is a symlink and the validator does not follow symlinks. A session does follow it. Validate the real directory with `claude plugin validate .` from the repository root, which reads `skills/` in place.

## Regenerate after the manifest changes

```bash
python3 harness/adapters/claude-code/generate.py            # write the files
python3 harness/adapters/claude-code/generate.py --check     # exit 1 if they drifted
```

The generator is the only thing that writes `commands/`, `agents/`, both `plugin.json` files and `marketplace.json`. It rewrites what changed, deletes any command or agent pointer whose source left the tree, and touches nothing else. `--check` writes nothing and names each file that is missing, changed by hand, or no longer in the manifest.

Run `--check` in CI beside the other two gates. Each one proves a different thing and none of them substitutes for another:

| Command | What it proves |
|---|---|
| `python3 lint.py --os` | The tree is structurally valid: no banned strings, no secrets, links resolve. |
| `python3 tools/check_manifest.py` | The manifest and the router table in [../../../CLAUDE.md](../../../CLAUDE.md) agree row for row. |
| `python3 harness/adapters/claude-code/generate.py --check` | This plugin still matches the manifest. |

A green run of all three says the routing is consistent. It says nothing about whether any document produced through it is true, testable, or worth writing. That is the three checks in [../../INVARIANTS.md](../../INVARIANTS.md), and the last of them is a person.

## What this adapter refuses

| Refused | Why |
|---|---|
| Copying a skill into this directory | A copy is a file that drifts. The symlink means one skill, one copy. |
| Writing a model id into a command | The tier to model mapping lives in `routing/omniroute.config.json` and nowhere else. |
| Restating an invariant | Commands carry the ids only. The wording lives in [../../INVARIANTS.md](../../INVARIANTS.md). |
| Storing state or credentials | The harness stores no state. `OMNIROUTE_BASE_URL` and `OMNIROUTE_API_KEY` are read from the environment at call time and are never written under this directory. |
| Hand edits to a generated file | They are overwritten on the next run and reported by `--check` in the meantime. |

Delete this directory and the OS still runs exactly as `AGENTS.md` describes. The adapter is a face, not a dependency.
