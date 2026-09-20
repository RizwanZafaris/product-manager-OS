# Release evidence: what a tagged Product Manager OS release has to carry

Stage: ALL STAGES, read before any release is tagged
Knowledge: [readiness criteria](criteria.json)
Skill: none. This is a checklist for a person, not a procedure for a runtime

<!-- This file serves two gates in external-gates.json. EXT-CI requires an
     immutable commit SHA, a hosted workflow run URL, and all matrix jobs
     successful; that evidence exists today and is recorded below. EXT-RELEASE
     requires a signed or protected tag, an artifact digest, a provenance
     manifest, and a rollback artifact; two of those four can be produced from
     a commit by anyone, and two cannot. This file says which is which, and
     the record at the end is filled: 0.8.0 was tagged and published.
     Neither gate is marked verified anywhere: tools/readiness.py reports every
     external gate as verified false by construction, because a repository
     cannot award itself release evidence. -->

## EXT-CI: hosted CI on the exact release commit

| Evidence required | Status |
|---|---|
| Immutable commit SHA | `d598e4ddd087b0457709c9bbd27cb3db84047ef2`, the merge of #45 into main, which is the commit `v0.8.0` tags |
| Hosted workflow run URL | https://github.com/RizwanZafaris/product-manager-OS/actions/runs/35534938768 |
| All matrix jobs successful | `gate (3.11)`, `gate (3.13)` and `deletable-harness`, all three successful |

That is the whole of what EXT-CI asks for, and it is now recorded against the
tagged commit itself rather than against a candidate. It previously named
`2f31ef3`, the merge of #42. Re-record it again for the next tag, because the
gate is about the exact commit and not about main in general.

## EXT-RELEASE: tag, artifact, provenance, rollback

**The artifact digest can be produced by anyone, and it is reproducible.**
The repository ships one artifact, a pure-Python wheel, built by its own
standard-library backend with no build package installed:

```bash
python3 -c "import pmos_build_backend as b; print(b.build_wheel('dist'))"
python3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('dist/product_manager_os-0.8.0-py3-none-any.whl').read_bytes()).hexdigest())"
```

Built twice from `2f31ef3` and again from the tagged commit `d598e4d`, that
wheel is byte-identical every time:

| Artifact | Value |
|---|---|
| Wheel | `product_manager_os-0.8.0-py3-none-any.whl` |
| Size | 214,034 bytes |
| SHA-256 | `0da525ddc9325002cd70dfb2b759d9ac8ae2c84f5904ff90d42c43fa6fbf171d` |

**The provenance manifest can be produced by anyone.** It inventories every
tracked file with its digest and records no file contents and no secrets:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pmos.cli provenance --path . --output /tmp/provenance.json
python3 -c "from pmos.release import verify_provenance; print(verify_provenance('.', '/tmp/provenance.json'))"
```

Both details matter. Python writes `__pycache__` on import, before the manifest
walks the tree, so a manifest generated without `PYTHONDONTWRITEBYTECODE=1`
inventories build caches and will not reproduce: measured on the same commit,
a plain run counted 716 artifacts and a run with bytecode off counted 702, the
difference being fourteen `.pyc` files. And `pmos verify` is not the way to
check a manifest: it checks a runtime and refuses before reading one, so it
needs a workspace that has been through `pmos init`. `verify_provenance` takes
a tree and a manifest and needs no runtime.

Generated that way from a pristine clone of `d598e4d` it covers 703 artifacts,
97 skills and 25 configuration files, and `verify_provenance` returns
`VerificationResult(ok=True, errors=())` against that clone. It covered 702
before `docs/release/RELEASE-NOTES-0.8.0.md` was added, which is the whole of
the difference: the manifest changes with any tracked file.
Generate it from the tagged commit, not from a working tree, and publish it
beside the wheel rather than committing it: a manifest committed into the tree
it describes is stale the moment anything changes.

**The tag needed the owner, and the owner created it.** EXT-RELEASE asks for a
signed or protected tag, and its own `owner_action` says to create the
authorized tag only after the applicable gates are verified. Nobody else can
authorize it, and no automation in this repository should.

Half of that requirement is unmet, and the record below says so rather than
reporting a protection that does not exist. The tag is annotated but unsigned,
and ruleset 22968065 covers the `main` branch, not tags, so `v0.8.0` can be
moved by anyone with push access. It was moved twice on the day it was created,
each time because it had been placed on a commit behind main, and nothing in
this repository or in GitHub stopped it. A tag ruleset would.

**There is no rollback artifact.** The gate asks for one because a release that
cannot be undone is not a release. The repository carries the tags v0.3.0 and
v0.4.0, but neither was published as a release and neither carries an artifact,
so there is no earlier artifact to roll back to,
and the honest rollback for 0.8.0 is to stop using it and pin the previous
commit. Say that in the release notes rather than leaving the field blank, and
the second release will have a real answer.

## Before the tag

1. `python3 tools/ci_gate.py` passes on the candidate commit, all gates.
2. `python3 tools/readiness.py --local` reports 100 of 100, which means the
   CI-6 record covers the exact tree being tagged.
3. The CHANGELOG's `Unreleased` heading becomes a dated version heading, on the
   day the tag is created and not before. Nothing in this repository should
   assert a release date while no tag carries it. Replace the heading and its
   opening paragraph with exactly this, putting the tag's own date in:

   ```markdown
   ## 0.8.0, <YYYY-MM-DD of the tag>

   This release adds executable local engineering capability: a dependency-free
   `pmos` runtime, the stage-gate loop it drives, and the checks that keep the
   documents honest. It is a source tag and a pure-Python wheel built from that
   tag. It is not a provider certification, not a release attestation, and not
   evidence that anyone outside this repository has adopted or reviewed it:
   those requirements stay open in `docs/readiness/external-gates.json`, and
   `docs/readiness/EXT-RELEASE-checklist.md` records which of them this release
   carries evidence for and which it does not.
   ```

   Make those two paths markdown links when you paste it: they resolve from the
   repository root, where the CHANGELOG sits, and would not resolve from here.
   If the day this names passes before the change lands, redate it before
   merging rather than merging a date no tag will carry. That happened to
   0.8.0: the heading was written on 2026-09-20 and merged on 2026-09-21.
4. Hosted CI has run on that exact commit and every matrix job succeeded.
5. The wheel is built from that commit and its digest is recorded below.
6. The provenance manifest is generated from that commit and published with it.

## The record

Fill this in when the release is tagged, and leave it filled.

| Field | Value |
|---|---|
| Release version | 0.8.0 |
| Tagged commit SHA | `d598e4ddd087b0457709c9bbd27cb3db84047ef2` |
| Tag protection or signature | none: annotated, unsigned, and not covered by ruleset 22968065, which targets the `main` branch |
| Hosted CI run for that SHA | https://github.com/RizwanZafaris/product-manager-OS/actions/runs/35534938768, all three matrix jobs successful |
| Wheel filename | `product_manager_os-0.8.0-py3-none-any.whl` |
| Wheel SHA-256 | `0da525ddc9325002cd70dfb2b759d9ac8ae2c84f5904ff90d42c43fa6fbf171d` |
| Provenance manifest SHA-256 | `f5727cb95d14f3083e3df92c5169f54a0df22194f390cc3ba24c35d30590ff4d`, the file published with the release |
| Provenance tree SHA-256 | `2e46f7fa42f85698d327e6b3c8fd0fd6a4f5909a2ea556e461adf1110f138be2`, recorded inside that manifest |
| Published release | https://github.com/RizwanZafaris/product-manager-OS/releases/tag/v0.8.0, carrying the wheel and the manifest |
| Rollback artifact | none: the tags v0.3.0 and v0.4.0 published no release and no artifact, so the rollback is to pin the previous commit |
| Authorized by | Rizwan Zafar, 2026-09-21 in +04, which GitHub records as 2026-09-20T20:23:53Z |

The wheel digest above was measured on `2f31ef3`, on the release candidate, and
again on the tagged commit, unchanged every time, because documentation does not
enter the wheel. Re-measure it if anything under `pmos/` or the packaging
metadata changes before a tag. The provenance digest was blank here until a tag
existed, because only the manifest generated from the tagged commit is the right
one to publish; that manifest now exists and is attached to the release, so its
digest is recorded above and a reader can tell they have the right one.
