# Changelog

Every notable change to this repository is recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this repository uses [semantic versioning](https://semver.org/spec/v2.0.0.html).

What a version number means here, since this is a document system and not a library:

- **MAJOR** changes rename or remove a template field, move or delete a file that other files link to, or change what a gate demands. These are the changes that break a fork or a half-filled document, so they only happen on a major version, and this file names the migration for each one.
- **MINOR** adds a template, a knowledge card, a skill, or a section. Existing filled documents keep working untouched.
- **PATCH** fixes wording, links, typos, or a lint rule that was wrong.

The stability promise is stated in [README.md](README.md) and repeated here so it survives a fork: within a major version, template field names and file paths do not change under you.

## Unreleased

Nothing yet.

## 0.1.0, 2026-09-02

First public release. Honest inventory of what exists, rather than a list of what was done to get here.

### Added

- **The operating loop.** Six stages and six gates in `os/`: `OPERATING-LOOP.md` (stage entry and exit definitions), `STAGE-GATES.md` (six fill-in gate forms with sign-off lines and skip-risk warnings), `HOW-TO-RUN-A-PRODUCT.md` (one fictional product taken through all six gates), `WHICH-DOCUMENT.md` (how much document a decision deserves), and `PRODUCT-WORKSPACE.md` (where a product's filled artifacts live).
- **Templates**, fill-in and editor-only, across seven groups: `discovery/` (six, including competitive analysis), `definition/` (eight, including the one-pager weight), `architecture/` (nine), `execution/` (four), `delivery/` (five), `operate/` (three), `planning/` (three, including the first 90 days), and the `ai/` overlay (nine).
- **Knowledge layer.** Ten canon cards with named attribution, a stated trap, and a "skip it when" line, plus an index of eighteen more methods in one line each.
- **Skills**: `ai-prd`, `roadmap-builder`, `program-premortem`, `reg-gap-check`, `feedback-synthesis`. **Agents**: research, drafting, validation, red team, Hermes.
- **System prompts** for models with no file access: `system/BOOT-PROMPT.md` with a file manifest, and five copyable role blocks in `system/ROLE-PROMPTS.md`.
- **Routing** for API-tier use: `routing/omniroute.config.json` and its tier doctrine.
- **The regulated overlay** at `modules/regulated/`, a byte-exact import from its canonical source repository, hash-pinned by the quality gate and never edited here.
- **Worked examples** in `examples/`: a greenfield discovery document and PRD for a fictional expense copilot, and a brownfield example of a legacy checkout modernization that carries a reversed decision.
- **Quality gate.** `lint.py` in two modes: the original regulated PRD gate, and `--os` tree mode with nine whole-tree checks. `test_lint.py` covers every check.

### Known gaps

Stated rather than hidden, because a changelog that only lists wins is marketing.

- The gate does not check traceability between documents: a requirement ID that exists in a PRD and nowhere else passes.
- `knowledge/` holds canon, not per-product memory. Product memory is a folder convention in `os/PRODUCT-WORKSPACE.md`, not software.
- Install is `git clone`. There is no packaged plugin, and no plugin manifest is validated in CI.
- The banned-metric check matches literal strings, so a spelled-out variant walks through it.
