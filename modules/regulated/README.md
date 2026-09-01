# Regulated module

The flagship module of Product Manager OS, and the one that seeded the whole repository. Every design rule the OS runs on, gates that can fail, controls with named owners, graceful degradation as structure rather than aspiration, was proven here first.

**Canonical source: the standalone regulated-ai-prd repository, currently pre-release; it opens publicly at its v0.1 tag.** This directory is a copy, not a fork. The standalone repository is where the material lives, where issues are filed, and where every fix lands first. Nothing regulated is ever fixed here and back-ported; it is fixed there and re-copied.

## The byte-exact policy

Two files in this module carry verified regulatory citations, each read against primary text on the date its header states:

| File | Status |
|---|---|
| `templates/regulated-ai-prd-template.md` | Byte-exact copy. sha256 pinned in the root `lint.py`. Never edited in this repository. |
| `examples/dispute-summary/PRD.md` | Byte-exact copy. sha256 pinned in the root `lint.py`. Never edited in this repository. |

A regulatory citation is only worth what its verification is worth. Rewording a verified citation, even to improve it, silently destroys the verification while keeping the confident prose, which is the worst possible trade. So these two files are copied at the byte level, the OS-wide quality gate pins their hashes, and any drift fails the build. If you believe either file is wrong, open an issue against the canonical repository.

The remaining files (`SKILL.md`, `lint.py`, `test_lint.py`) are verbatim copies kept runnable in place, so the module's own review gate works from this directory without the standalone repository present:

```bash
cd modules/regulated
python3 lint.py --template templates/regulated-ai-prd-template.md
python3 lint.py examples/dispute-summary/PRD.md
python3 -m unittest test_lint.py -v
```

## When this overlay activates

The core operating loop (see `../../os/OPERATING-LOOP.md`) treats this module as an overlay, not a stage. It activates when the product runs under a financial or data regulator: a licensed payments flow, a credit decision, a KYC or screening step, anything where a supervisor can ask for the document trail. When it activates, it binds at two gates, wired in through `../../os/STAGE-GATES.md`:

- **Gate 2 (requirements signed off).** The regulated PRD template replaces or extends `../../templates/definition/prd.md`. Its section 0 overlay is answered before the first requirement is written, because a license condition beats a sprint plan every time.
- **Gate 5 (release readiness green).** The module's lint gate and the template's review-gate checklist must both pass before launch.

If the product also contains a model, which is the usual reason to be here, the AI overlay in `../../templates/ai/` applies alongside this one. The regulated template's eval tables and guardrail rows are the stricter superset; where the two overlap, this module wins.

## How to use it

1. Read `examples/dispute-summary/PRD.md` first. The template shows the questions; the example shows what an answer that survives a review looks like.
2. Copy `templates/regulated-ai-prd-template.md` into your own working area. Do not fill it in inside this directory; files here are reference material, and the hash pin will fail the build if you touch the two protected ones.
3. Fill every field. "N/A because [reason]" is an answer. A blank is not.
4. Run `python3 lint.py <your-file>.md` from this directory until it exits clean.
5. Take the result to Gate 2 with your second line.

## Scope, honestly stated

The v1 overlay maps to two instruments only: the CBUAE Guidance Note on consumer protection and AI/ML adoption by licensed financial institutions (issued 11 February 2026) and EU AI Act Annex IV technical documentation fields. Other regulators are deliberately out of scope until their primary text has been read and cited. An overlay that name-drops twelve regulators and cites none of them is worse than one that covers two and shows its work. The canonical repository's README carries the full scope table, the currency and sunset policy, and the list of what the gate does not catch.

None of this is legal or regulatory advice, and a green lint run means the document is complete, not that it is true.
