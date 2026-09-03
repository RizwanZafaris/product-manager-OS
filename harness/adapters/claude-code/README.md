# Claude Code plugin adapter

This directory is a Claude Code plugin. It puts the router table of the Product Manager OS in front of you as slash commands, one per route, generated from [../../MANIFEST.json](../../MANIFEST.json).

It adds no procedure. Every command names the `SKILL.md` that owns the work, the templates the output lands in, the files to read first, the gate the output must pass, and the invariant ids that bind the run. The skills themselves are not copied here. `skills` is a symlink to the repository's own [../../../skills](../../../skills) directory, so there is exactly one copy of every skill in the tree and no second copy to drift.

## What it installs

| Component | Path here | Count | Source |
|---|---|---|---|
| Plugin manifest | [.claude-plugin/plugin.json](.claude-plugin/plugin.json) | 1 | Generated. `name` and `version` come from the manifest. |
| Slash commands | `commands/*.md` | 41 | Generated, one per manifest entry, named by its route id. |
| Skills | `skills` | 28 | Symlink to `skills/` at the repository root. Referenced, never copied. |
| Generator | [generate.py](generate.py) | 1 | Hand written. Standard library only. |

Commands are namespaced by the plugin name, so the route ids become `/product-manager-os-harness:write-prd`, `/product-manager-os-harness:run-premortem`, and so on. Read one to see the shape: [commands/write-prd.md](commands/write-prd.md).

Every command sets `disable-model-invocation: true`. That is deliberate. The commands are the face a person types at; model invoked work goes through the skills, which [skills/write-prd/SKILL.md](skills/write-prd/SKILL.md) and its siblings already carry. Claude cannot pick a route on your behalf and skip the row you asked for.

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
| List the routes | `/help`, then the custom commands tab | 41 commands under the plugin name |
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

The generator is the only thing that writes `commands/` and `plugin.json`. It rewrites what changed, deletes any command file whose route left the manifest, and touches nothing else. `--check` writes nothing and names each file that is missing, changed by hand, or no longer in the manifest.

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
