# Product Manager OS 0.8.0

Stage: ALL STAGES, published with the 0.8.0 tag
Knowledge: [the changelog entry this summarises](../../CHANGELOG.md)
Skill: none. These are release notes for a reader, not a procedure for a runtime

<!-- Draft. The tag, its protection and the authorizing name are filled by
     whoever authorizes the release; everything else here is measured. Keep the
     "what this release is not" section: it is the part a reader needs most. -->

## What this release is

A product-management operating system you can run with Python and a text
editor: 667 documents, 29 skills, 108 templates, a six-gate stage loop, and a
dependency-free `pmos` runtime that records answers, evidence and gate
approvals and refuses to call a product ready when they do not hold.

Highlights of this version:

- **The runtime carries a real chain.** `examples/journey-chain.md` is generated
  by driving the command line from the committed expense copilot documents: all
  26 questions of Gates 1 to 3 answered with evidence citing those files, a
  development handoff reported ready on nine linked sections, and that readiness
  withdrawn once one cited document changes.
- **Readiness cannot be faked.** A handoff section counts only when it links a
  file carrying an artifact block, and an exemption needs its reason. Before
  this, nine sections could point at one scratch file and report ready.
- **Products can adopt revised questions.** `pmos repin` re-pins a product to
  the shipped question banks, keeps every stored answer, and lets the changed
  banks' gates go stale until they are proved again.
- **Status tells you what to do next.** The command line opens with where the
  product stands, the next command, and the document to open.
- **25 release gates** run on every commit, covering the runtime suites, the
  document tree, the workspace lifecycle, and the two generated run records.

## What this release is not

It is a source tag and a wheel built from it. It is not a provider
certification and not a release attestation. Nobody outside this repository has
yet completed the new-user journey against it, and no independent team has
reviewed a release candidate: those gates stay open in
[docs/readiness/external-gates.json](../readiness/external-gates.json). A green
local run proves the executable local contract and nothing beyond it.

## Verifying what you downloaded

```bash
python3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('product_manager_os-0.8.0-py3-none-any.whl').read_bytes()).hexdigest())"
python3 -c "from pmos.release import verify_provenance; print(verify_provenance('.', 'provenance.json'))"
```

Run the second one from a checkout of the tagged source. `pmos verify` is not
the command for this: it checks a runtime and refuses before it reads a
manifest, so it needs a workspace you have run `pmos init` in.

The wheel is built by the repository's own standard-library backend and is
byte-identical on repeated builds from the same commit, so the digest below is
reproducible rather than asserted.

## Rolling back

There is no earlier published artifact to roll back to. The repository carries
the tags v0.3.0 and v0.4.0, but neither was ever published as a release and
neither carries an artifact, so this is the first release to ship a wheel. The
rollback is to stop using it and pin the previous commit. The next release will
have a real answer here.
