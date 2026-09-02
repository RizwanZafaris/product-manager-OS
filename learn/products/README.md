# Practice Workspaces

This folder is where learning-path exercises accumulate: one subfolder per fictional product, holding your progress ledger and your filled practice artifacts. It mirrors the real workspace convention in [PRODUCT-WORKSPACE.md](../../os/PRODUCT-WORKSPACE.md) on purpose, so the habits you build here transfer file for file. The differences are few and absolute, and they all come down to one line: nothing in here is true.

## The layout

```
learn/products/
└── streakline/
    ├── PROGRESS.md      the path's ledger block, copied in, plus one line per session
    ├── discovery/       filled practice copies of templates/discovery/
    ├── definition/      filled practice copies of templates/definition/
    ├── planning/        practice roadmap, OKRs, GTM and growth plans
    └── execution/       practice risk register, decision log, stakeholder map
```

Create stage folders as a path step needs them; an empty scaffold is decoration. `PROGRESS.md` is the one mandatory file: the checkbox ledger from your path, plus the tutor's session lines (date, step, scores, weakest area, card to re-read).

## The rules

1. **Copy templates out, fill the copies, keep the template's file name.** Same rule as real work, for the same reason: the habit is the curriculum.
2. **Every piece of evidence is labeled "invented:".** The label is not bureaucracy; it is the habit that keeps practice material from ever masquerading as fact. The tutor fails unlabeled evidence on sight.
3. **Nothing here ever migrates.** No practice artifact, number, quote, or persona may be cited in a real product workspace, pasted into `products/` at the repo root, or graduated into `knowledge/`. Practice is quarantined by definition, not by quality.
4. **Delete freely.** Real workspaces keep failed gate attempts because they are memory. Practice workspaces can be reset whenever a rerun would teach more than the archaeology; only `PROGRESS.md` is worth preserving across a reset.

## Why this is not products/

The repo-root `products/` name is reserved for real product work and will never ship a directory here; that guarantee is made in [PRODUCT-WORKSPACE.md](../../os/PRODUCT-WORKSPACE.md) and this folder does not weaken it. Practice lives under `learn/` so that a grep, a backup, or a new teammate can tell truth from training data by path alone. If a fictional product starts feeling worth building for real, that is a fine outcome: start it fresh in a real workspace, at Gate 1, with real evidence, and take nothing with you but what you learned.

## Housekeeping

Practice folders are yours, not the repository's: they are untracked working state, like `products/`, and a clone used by a team should add `learn/products/*/` to `.gitignore` except this README. The paths that feed this folder live one level up, starting at [the learn index](../INDEX.md).
