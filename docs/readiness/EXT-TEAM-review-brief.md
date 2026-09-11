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

You do not need to be a Python expert, and you do not need to read every
file in the digest. The sections below name the six places where a defect would be most
expensive, and each says what "wrong" would look like. If you can read a
function and ask "what happens if this fails halfway", you can do this review.

Budget about an hour.

## What you are reviewing

<!-- This table used to carry a commit, a digest and a file count typed in by
     hand. They were right for one afternoon. The tree moved, the brief did
     not, and a reviewer following it would have checked out a commit seven
     merges old and confirmed a digest that no longer described anything. The
     values now come from the tree you have in front of you, and the record at
     the bottom asks you to write down what you actually saw. -->

The candidate is the head of `main` at the moment you start, and nothing
else. Establish what that is yourself rather than taking a number from this
file:

```bash
git fetch origin main && git checkout origin/main
git rev-parse HEAD                     # the commit you are reviewing
python3 tools/review_gate.py --digest  # {"files": N, "sha256": "..."}
```

Write both values into the record at the bottom. If either changes while you
are reviewing, the tree moved under you; start again from the new head, because
an acceptance covers the tree that was read and no other.

Then find the hosted run for that exact commit and note its result:

```bash
gh run list --branch main --limit 1    # the run for the SHA you just printed
```

It is expected to be red on the two `gate` jobs for exactly one criterion,
CI-6, which is the criterion your review closes. Any other red is a finding.

## Run it yourself first

One command, about 90 seconds. Do not take the reported result on trust; it is
the thing under review.

```bash
python3 tools/ci_gate.py
```

Expect `release gates: 20/21 passed`, with the one failure being
`readiness-local` reporting `failing : 1 criteria`, and that criterion CI-6.
The number of gates has grown since this brief was first written and will grow
again; what matters is that the only red is the review record you are about to
write. Any other red is a finding.

If that fails on your machine differently from how it fails on CI, that
difference is itself a finding and worth more than anything below. One such
difference is already known and documented: on an exFAT, FAT or SMB volume
under macOS, sidecar files named `._name` appear beside every entry, and the
loaders were not written to expect them. If you see `UnicodeDecodeError` or
`runtime root contains unknown or unsafe entry`, check the changelog for the
entry that closes it before filing it again.

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

- `STATE.md` models one product at one stage, so the document path has no
  portfolio view. The `pmos/` domain model is a separate surface and does:
  an organization holds products, a product holds initiatives, and
  `score_initiative`, `allocate_capacity`, `sequence_initiative` and `rollup`
  in `pmos/domain.py` carry score, capacity per named period, and sequence.
  Nothing derives one surface from the other, which is the limit worth
  checking.
- There is no identity, RBAC, or immutable audit log. A gate is signed by a
  person editing a file.
- No integration adapter has been verified against a vendor sandbox.
- Every test of the AI layer stubs the gateway. The layer has been observed
  against a live model exactly as far as `tools/ext_ai_probe.py` records:
  on 2026-09-09, three pinned calls to a free model through the local
  OmniRoute gateway, at a $0 ceiling, with the resolved model, cache and
  compression outcome, token counts and gateway-reported cost written to the
  evidence file. That file is not in this tree, and EXT-AI in
  `external-gates.json` stays `required` until evidence tied to the release
  commit is verified independently. `--dry-run` still shows what a run would
  do without touching the socket.

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

## Recording your review

<!-- Until this existed, closing this gate meant hand-writing a JSON file with
     a closed schema and a correct tree digest. Nobody did, so the check stayed
     red, red became its normal state, and three pull requests were merged with
     it failing. A gate nobody can close is a gate everybody learns to ignore. -->

One command, run from the repository root after you have actually reviewed:

```bash
python3 tools/review_gate.py --record \
  --reviewer "Your Name" \
  --scope "what you actually read" \
  --evidence "python3 tools/ci_gate.py|20/21 passed; the one red is CI-6" \
  --finding "P2|accepted|one-line summary|where you saw it"
```

`--scope`, `--evidence` and `--finding` repeat. Omit `--finding` if you found
nothing, which is a legitimate outcome and is recorded as such.

Three things it will refuse, on purpose:

- **A review that ran nothing.** `--evidence` is required. A review with no
  command behind it is a reading, and this gate is not for readings.
- **A review with no stated scope.** A later reader has to know what the
  acceptance covered.
- **A self-attestation.** If the name you give matches an author in the
  repository's recent history, it refuses and writes nothing. That is the one
  property this gate exists for: the person who wrote the change must not be
  able to close the check on it by running a command.

It records a claim and never dresses it as proof. The record it writes says
`identity_assurance: unauthenticated-local-claim`, because nothing here
authenticates anyone. Only `accepted` is recordable; a rejection is expressed
by leaving the gate red and saying so where the change is being discussed.

The record binds to the exact tree you reviewed. Any later change makes it
stale again, which is correct: your acceptance covered what you read.

## The record



Fill this in and the gate has its evidence. An unsigned or undated record does
not close it.

```
Reviewer name        :
Reviewer contact     :
Relationship to work : (must be: did not implement this release)
Date reviewed        :
Commit reviewed      : (output of git rev-parse HEAD)
Digest confirmed     : (files and sha256 from review_gate.py --digest)
ci_gate.py result    : 20/21 with CI-6 the only red / other:
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
