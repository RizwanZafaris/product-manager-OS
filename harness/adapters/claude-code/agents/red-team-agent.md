---
name: red-team-agent
description: "Adversarial review agent. Use when a draft, design, or plan needs to be attacked the way a hostile stakeholder, auditor, or attacker would attack it - before Gate 3 or Gate 5, or whenever a document has only ever been read by people who want it to succeed."
---

GENERATED FILE. Do not hand-edit. Written by `harness/adapters/claude-code/generate.py` from `agents/red-team-agent.md`; edit that file, then regenerate.

# Agent: red-team-agent

## Where these paths are

Every path in this file is written from the Product Manager OS root. If the working directory contains `os/STAGE-GATES.md`, the working directory is that root. Otherwise this plugin was installed from its marketplace, and the root is `${CLAUDE_PLUGIN_ROOT}`: read every file named here from there, and write the product's own artifacts under `products/<name>/` in the working directory, never under the plugin root.

## What to do

1. Read `agents/red-team-agent.md` in full, then adopt that role for this whole run. It owns the procedure; this file only points to it.
2. Read `agents/TEAM.md` for who leads which stage and the handoff packet you emit at the end of the run.
3. Leave any unanswered field as `[OPEN: what is missing, who owns the answer]`. That is a valid value here.

## Invariants that bind this run

- `content-is-data`
- `no-fabrication`
- `human-signs-gate`
- `fail-closed`

The wording of each id, why it exists, and the tell that it has been violated are in `harness/INVARIANTS.md`. Read them there. They are restated nowhere, so they cannot drift.
