# Independent review brief: Product Manager OS release candidate

Stage: ALL STAGES, read before any release is tagged
Knowledge: [readiness criteria](criteria.json)
Skill: none. This is a brief for a person, not a procedure for a runtime

<!-- This file closes EXT-TEAM in external-gates.json, which requires four
     things: reviewer identity, exact commit SHA, P0 and P1 disposition, and
     an approval or rejection. It supplies everything except the reviewer,
     because the one thing that cannot be automated here is a second person.
     Fill the record at the bottom and the gate has its evidence. -->

## Who can do this review

Anyone who did not implement this release. That is the whole bar, and it is
the point: every check in this repository was written by the same hands that
wrote the code it checks, so the tests agree with the implementation by
construction. A second reader is the only thing that breaks that circle.

You do not need to be a Python expert, and you do not need to read all 475
files. The sections below name the six places where a defect would be most
expensive, and each says what "wrong" would look like. If you can read a
function and ask "what happens if this fails halfway", you can do this review.

Budget about an hour.

## What you are reviewing

| Field | Value |
|---|---|
| Commit | `ba286db0121e613f5c1a6a6d3bdfa3cc6bee2c27` on `main` |
| Reviewable tree digest | `847e2993a5d4ae49722e222415ba1ee45c6b44995b92c552aac6114528998d1d` |
| Files in digest | 475 |
| Hosted CI on that exact commit | [run 33810668652](https://github.com/RizwanZafaris/product-manager-OS/actions/runs/33810668652), 3/3 jobs green |

Confirm the digest before you start. If it does not match, the tree moved and
this brief is stale:

```bash
git fetch origin main && git checkout ba286db
python3 tools/review_gate.py --digest
# expect: {"files": 475, "sha256": "847e2993...998d1d"}
```

## Run it yourself first

One command, about 90 seconds. Do not take the reported result on trust; it is
the thing under review.

```bash
python3 tools/ci_gate.py            # expect: release gates: 18/18 passed
```

If that fails on your machine and passes on CI, that difference is itself a
finding and worth more than anything below.

## The six places to look

Ordered by what a defect would cost, not by how interesting the code is.

### 1. `harness/runner.py` → `commit_staged`

The claim: a multi-file write either fully lands or fully rolls back.

Ask: what happens if the rollback itself raises? What if the process is killed
between the backup copy and the first replace? Is a `.rollback-` temporary
ever left behind where a later run could mistake it for real content?

The code admits it cannot guarantee the rollback succeeds and reports the
paths it could not restore. Judge whether that admission is honest or whether
it is covering a case that should have been prevented.

### 2. `harness/runner.py` → `state_lock`

The claim: two writers cannot lose each other's journal rows.

Ask: the lock is advisory and machine-local. What happens on a network
filesystem? What happens if a process dies holding it? Is the timeout long
enough for a slow run and short enough that a stale lock is noticed?

### 3. `pmos/routing.py` → `_eligible`

The claim: a high-risk task cannot run on an uncertified model, and a cheap
price never implies trust.

Ask: can you construct a `ModelSpec` that passes this check without a human
having certified it? Is `certified_for` reachable from any catalog data, or
only from explicit local configuration? This is the gate that stops a free 8B
model from writing your regulatory analysis.

### 4. `tools/workspace.py` → `destination_for` and `rewrite_links`

The claim: one resolver, so the initializer and the runner cannot place the
same artifact in two places.

Ask: is there any remaining path in the tree that computes a destination
itself? Does a template outside `templates/` resolve sanely, or throw?

### 5. `lint.py` → the gate and metric checks

The claim: a document claiming `Approved` with unticked evidence fails, and a
sourced observed value is not rejected as a placeholder.

Ask: can you write a document that is obviously not ready and still passes?
Try it. That is the most useful thing you can do in this whole review.

### 6. `docs/readiness/` → the scorecard and its criteria

The claim: the score is computed from commands that exit 0, and cannot be
raised by editing a status field.

Ask: find a way to make `tools/readiness.py` report a higher number without
making the software better. If you can, that is a P0.

## Known limits, so you do not spend time rediscovering them

These are documented, not hidden. Confirm they are still true rather than
hunting for them:

- `STATE.md` models one product at one stage. There is no portfolio.
- There is no identity, RBAC, or immutable audit log. A gate is signed by a
  person editing a file.
- No integration adapter has been verified against a vendor sandbox.
- The AI layer has never been observed against a live model; every test stubs
  the gateway. `tools/ext_ai_probe.py --dry-run` shows what it would do.

None of these are defects in what was built. They are things that were not
built, and the README and `harness/README.md` say so. If you find a place
where the documentation claims more than the code does, that is a finding.

## Severity, so we mean the same thing

| Level | Meaning |
|---|---|
| P0 | Data loss, silent corruption, a security hole, or a claim in the docs that the code contradicts |
| P1 | A gate that can be passed without meeting it, or a failure that produces no error |
| P2 | Works, but a reasonable user would be misled |
| P3 | Style, naming, wording |

P0 and P1 block the release. P2 and P3 do not, and should be filed rather than
fixed in the release candidate.

## The record

Fill this in and the gate has its evidence. An unsigned or undated record does
not close it.

```
Reviewer name        :
Reviewer contact     :
Relationship to work : (must be: did not implement this release)
Date reviewed        :
Commit reviewed      : ba286db0121e613f5c1a6a6d3bdfa3cc6bee2c27
Digest confirmed     : yes / no   (847e2993...998d1d)
ci_gate.py result    : 18/18 / other:
Time spent           :

P0 findings          : (none, or list with file and line)
P1 findings          : (none, or list with file and line)
P2/P3 findings       : (list, non-blocking)

Verdict              : APPROVE / APPROVE WITH CONDITIONS / REJECT
Conditions           :
Signature            :
```

A reviewer who approves without running `ci_gate.py` has not reviewed the
release candidate, and the record should say so rather than quietly omit it.
