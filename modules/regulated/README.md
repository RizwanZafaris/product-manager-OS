# Regulated module

The flagship module of Product Manager OS, and the one that seeded the whole repository. Every design rule the OS runs on, gates that can fail, controls with named owners, graceful degradation as structure rather than aspiration, was proven here first.

**Canonical source: the standalone regulated-ai-prd repository. It is private today; the plan remains for it to open publicly at its v0.1 tag.** This directory is a copy, not a fork, of the five files pinned in the table below. The standalone repository is where that material lives and where its fixes land first: nothing in the pinned set is ever edited here and back-ported, it is fixed there and re-copied. This file, `README.md`, is not part of the pinned set: it is authored in this repository, states this repository's own import policy, and carries the interim reporting process below for while the standalone repository stays private.

## The byte-exact policy

Two files in this module carry verified regulatory citations, each read against primary text on the date its header states:

| File | Status |
|---|---|
| `templates/regulated-ai-prd-template.md` | Byte-exact copy. sha256 pinned in the root `lint.py`. Never edited in this repository. |
| `examples/dispute-summary/PRD.md` | Byte-exact copy. sha256 pinned in the root `lint.py`. Never edited in this repository. |

A regulatory citation is only worth what its verification is worth. Rewording a verified citation, even to improve it, silently destroys the verification while keeping the confident prose, which is the worst possible trade. So these two files are copied at the byte level, the OS-wide quality gate pins their hashes, and any drift fails the build. If you believe either file is wrong, see "Reporting an error in this module" below: the canonical repository is not a reachable destination for that report while it stays private.

The remaining files (`SKILL.md`, `lint.py`, `test_lint.py`) are verbatim copies kept runnable in place, so the module's own review gate works from this directory without the standalone repository present:

```bash
cd modules/regulated
python3 lint.py --template templates/regulated-ai-prd-template.md
python3 lint.py examples/dispute-summary/PRD.md
python3 -m unittest test_lint.py -v
```

## Reporting an error in this module

The standalone regulated-ai-prd repository is private, so it is not a destination a reader of this copy can reach. Until it is public, this is the interim process:

- Issues about this module, meaning its two cited instruments, its five pinned files, or this README, are accepted in this repository. Open them against `modules/regulated/`.
- The upstream copy has an owner: the repository owner.
- Freshness review: 2026-12-14, about 90 days from when this process was written. By that date the repository owner re-reads the two cited instruments against primary text, confirms this module still matches them or updates it, and records the next review date.
- The canonical URL and the source commit this copy was taken from will be published here once the standalone repository is public. No URL is given above because none is public yet to give.

## When this overlay activates

The core operating loop (see `../../os/OPERATING-LOOP.md`) treats this module as an overlay, not a stage. It activates on one condition, stated in full here and in `../../os/STAGE-GATES.md`: the product contains an AI or machine-learning feature, and a financial or data regulator applies to it. Both halves are required. A licensed payments flow, a credit decision, or a KYC or screening step with no model in it does not activate this overlay, because the module's two cited instruments are both about AI and machine learning and cover nothing else; see "The regulated overlay, and what it does not cover" in `../../os/STAGE-GATES.md` for what such a product brings instead.

The table below is the one tested applicability truth table this file and `../../os/STAGE-GATES.md` both point to. Neither file keeps a second copy of it.

| Case | AI or ML feature | Financial or data regulator applies | Overlay activates |
|---|---|---|---|
| AI and regulated | Yes | Yes | Yes |
| AI and unregulated | Yes | No | No |
| Non-AI and regulated | No | Yes | No |
| Neither | No | No | No |

When it activates, it binds at two gates, wired in through `../../os/STAGE-GATES.md`:

- **Gate 2 (requirements signed off).** The regulated PRD template replaces or extends `../../templates/definition/prd.md`. Its section 0 overlay is answered before the first requirement is written, because a license condition beats a sprint plan every time.
- **Gate 5 (release readiness green).** The module's lint gate and the template's review-gate checklist must both pass before launch.

The AI overlay in `../../templates/ai/` always applies alongside this one, because this module never activates without a model present. The regulated template's eval tables and guardrail rows are the stricter superset; where the two overlap, this module wins.

## How to use it

1. Read `examples/dispute-summary/PRD.md` first. The template shows the questions; the example shows what an answer that survives a review looks like.
2. Copy `templates/regulated-ai-prd-template.md` into your own working area. Do not fill it in inside this directory; files here are reference material, and the hash pin will fail the build if you touch the two protected ones.
3. Fill every field. "N/A because [reason]" is an answer. A blank is not.
4. Run `python3 lint.py <your-file>.md` from this directory until it exits clean.
5. Take the result to Gate 2 with your second line.

## Scope, honestly stated

The v1 overlay maps to two instruments only: the CBUAE Guidance Note on consumer protection and AI/ML adoption by licensed financial institutions (issued 11 February 2026) and EU AI Act Annex IV technical documentation fields. Other regulators are deliberately out of scope until their primary text has been read and cited. An overlay that name-drops twelve regulators and cites none of them is worse than one that covers two and shows its work. The canonical repository's README carries the full scope table, the currency and sunset policy, and the list of what the gate does not catch.

None of this is legal or regulatory advice, and a green lint run means the document is complete, not that it is true.
