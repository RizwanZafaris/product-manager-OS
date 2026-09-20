# Release evidence: what a tagged Product Manager OS release has to carry

Stage: ALL STAGES, read before any release is tagged
Knowledge: [readiness criteria](criteria.json)
Skill: none. This is a checklist for a person, not a procedure for a runtime

<!-- This file serves two gates in external-gates.json. EXT-CI requires an
     immutable commit SHA, a hosted workflow run URL, and all matrix jobs
     successful; that evidence exists today and is recorded below. EXT-RELEASE
     requires a signed or protected tag, an artifact digest, a provenance
     manifest, and a rollback artifact; two of those four can be produced from
     a commit by anyone, and two cannot. This file says which is which and
     leaves the record to be filled by whoever authorizes the tag.
     Neither gate is marked verified anywhere: tools/readiness.py reports every
     external gate as verified false by construction, because a repository
     cannot award itself release evidence. -->

## EXT-CI: hosted CI on the exact release commit

| Evidence required | Status |
|---|---|
| Immutable commit SHA | `2f31ef3`, the merge of #42 into main |
| Hosted workflow run URL | https://github.com/RizwanZafaris/product-manager-OS/actions/runs/35522785674 |
| All matrix jobs successful | `gate (3.11)`, `gate (3.13)` and `deletable-harness`, all three successful |

That is the whole of what EXT-CI asks for, on a commit that is already on main.
Re-record it against whatever commit is finally tagged, because the gate is
about the exact commit and not about main in general.

## EXT-RELEASE: tag, artifact, provenance, rollback

**The artifact digest can be produced by anyone, and it is reproducible.**
The repository ships one artifact, a pure-Python wheel, built by its own
standard-library backend with no build package installed:

```bash
python3 -c "import pmos_build_backend as b; print(b.build_wheel('dist'))"
python3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('dist/product_manager_os-0.8.0-py3-none-any.whl').read_bytes()).hexdigest())"
```

Built twice from `2f31ef3`, that wheel is byte-identical both times:

| Artifact | Value |
|---|---|
| Wheel | `product_manager_os-0.8.0-py3-none-any.whl` |
| Size | 214,034 bytes |
| SHA-256 | `0da525ddc9325002cd70dfb2b759d9ac8ae2c84f5904ff90d42c43fa6fbf171d` |

**The provenance manifest can be produced by anyone.** It inventories every
tracked file with its digest and records no file contents and no secrets:

```bash
python3 -m pmos.cli provenance --path . --output docs/release/provenance.json
python3 -m pmos.cli verify --path . --provenance docs/release/provenance.json
```

On `2f31ef3` it covers 772 artifacts, 97 skills and 25 configuration files.
Generate it from the tagged commit, not from a working tree, and publish it
beside the wheel rather than committing it: a manifest committed into the tree
it describes is stale the moment anything changes.

**The tag needs the owner.** EXT-RELEASE asks for a signed or protected tag,
and its own `owner_action` says to create the authorized tag only after the
applicable gates are verified. Nobody else can authorize it, and no automation
in this repository should.

**There is no rollback artifact, and this is the first release.** The gate asks
for one because a release that cannot be undone is not a release. Today this
repository has published none, so there is no earlier artifact to roll back to,
and the honest rollback for 0.8.0 is to stop using it and pin the previous
commit. Say that in the release notes rather than leaving the field blank, and
the second release will have a real answer.

## Before the tag

1. `python3 tools/ci_gate.py` passes on the candidate commit, all gates.
2. `python3 tools/readiness.py --local` reports 100 of 100, which means the
   CI-6 record covers the exact tree being tagged.
3. The CHANGELOG's `Unreleased` heading becomes a dated version heading, and
   the stability promise in it still describes what ships.
4. Hosted CI has run on that exact commit and every matrix job succeeded.
5. The wheel is built from that commit and its digest is recorded below.
6. The provenance manifest is generated from that commit and published with it.

## The record

Fill this in when the release is tagged, and leave it filled.

| Field | Value |
|---|---|
| Release version | 0.8.0 |
| Tagged commit SHA | <full sha of the commit the tag points at> |
| Tag protection or signature | <protected ruleset, or signing key id> |
| Hosted CI run for that SHA | <url> |
| Wheel filename | `product_manager_os-0.8.0-py3-none-any.whl` |
| Wheel SHA-256 | `0da525ddc9325002cd70dfb2b759d9ac8ae2c84f5904ff90d42c43fa6fbf171d` |
| Provenance manifest SHA-256 | generate from the tagged commit; it changes with any tracked file |
| Rollback artifact | none: first release, the rollback is to pin the previous commit |
| Authorized by | <name> on <date> |

The wheel digest above was measured twice on `2f31ef3` and again on this
release candidate, unchanged both times, because documentation does not enter
the wheel. Re-measure it if anything under `pmos/` or the packaging metadata
changes before the tag. The provenance digest is deliberately not recorded
here: it covers every tracked file, so only the manifest generated from the
tagged commit is the right one to publish.
