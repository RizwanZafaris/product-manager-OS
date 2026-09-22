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

Expect `release gates: 21/22 passed`, with the one failure being
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

Put your own review output (the transcript) in a file under
`docs/readiness/review-transcripts/` first, then run one command from the
repository root:

```bash
python3.11 tools/review_gate.py --record \
  --reviewer "Your Name" \
  --scope "what you actually read" \
  --evidence "python3 lint.py --os|ok (OS tree mode, 11 checks)" \
  --evidence "python3 tools/ci_gate.py|exit=1|release gates: 24/25 passed" \
  --finding "P2|accepted|one-line summary|where you saw it" \
  --transcript docs/readiness/review-transcripts/your-review.md
```

`--scope`, `--evidence` and `--finding` repeat. The command in each
`--evidence` must be a check this repository defines: the argv of a gate in
`tools/ci_gate.py` (`python3.11 tools/ci_gate.py --manifest` lists them), or
an entry of `EVIDENCE_COMMANDS` beside it, which today is the full sweep
`python3 tools/ci_gate.py` and the sweep narrowed to one gate,
`python3 tools/ci_gate.py --gate <id>`. It must be written exactly as there,
program `python3` included, with no other arguments; anything else is
refused before it runs, with a message naming that list. It is run the way
`ci_gate.py` runs a gate: in the gate's directory, with `ci_gate.py`'s
environment, with `python3` replaced by the interpreter running
`review_gate.py`, and with no shell. It is refused unless it exits 0 and the
text after the `|` appears in what it prints. Quote the command's output
rather than summarising it. A command you know exits non-zero is recorded by
declaring it, `COMMAND|exit=N|RESULT`, as the `ci_gate.py` line above does:
at record time the old record is stale, so CI-6 is red and a full sweep
cannot report every gate passed.

What it will refuse, on purpose:

- **A review that ran nothing.** `--evidence` is required. A review with no
  command behind it is a reading, and this gate is not for readings.
- **Evidence the command does not print, or a run that failed.** The command
  is run. A result that is not in its output, an exit code other than the one
  declared (0 by default), or a command that cannot be parsed or started is
  refused. The refusal shows what you recorded, and the start and end of what
  the command printed, where a gate sweep's verdict line sits. Before this,
  the result was free text nothing compared to anything: a record claiming
  `26/26 passed` on a tree that was not 26/26 was accepted. That holds only
  for records `--record` writes. See the next paragraphs for what the gate
  can and cannot check afterwards.
- **A review with no findings.** If you found nothing, record that:
  `--finding "P3|accepted|no defect found|what you read to conclude it"`. An
  empty list is indistinguishable from a field nobody filled.
- **A transcript outside the transcript directory.** `--transcript` must
  name a file already in the reviewed tree under
  `docs/readiness/review-transcripts/`. Its hash goes into the record, so the
  file is bound to the same digest as the code. The directory rule stops
  README.md, or the change's own source, from standing in as "the
  transcript". Nothing checks who wrote the file, or that git tracks it: the
  digest reads the filesystem, so an untracked file is accepted locally.
  Commit it with the record. A clean checkout without it digests
  differently, so the record is stale there.
- **A review with no stated scope.** A later reader has to know what the
  acceptance covered.
- **A self-attestation, as far as it can tell.** If the name you give matches
  an author in the repository's recent history, it refuses and writes
  nothing. Read the next section before relying on that.

It records a claim and never dresses it as proof. The record it writes says
`identity_assurance: unauthenticated-local-claim`, because nothing here
authenticates anyone. Only `accepted` is recordable; a rejection is expressed
by leaving the gate red and saying so where the change is being discussed.

The record binds to the exact tree you reviewed. Any later change makes it
stale again, which is correct: your acceptance covered what you read.

A plain run of the gate, which is what `ci_gate.py` does, checks the record
against itself. Each recorded command must be on the allowlist, each recorded
result must appear in the output recorded beside it, and the transcript must hash to the value in the record. That
catches an edit to one half of an evidence item. It does not catch an edit
to both halves. It also cannot tell a record `--record` wrote from one typed
by hand, so a hand-written record whose results and outputs agree passes.
It re-runs nothing.

`python3.11 tools/review_gate.py --reexecute` is the check that tests the
record against the tree. It re-runs every recorded command and fails unless
each one exits with the recorded code and prints the recorded result. It is
opt-in and `ci_gate.py` does not call it, because a recorded gate sweep takes
minutes. Run it before trusting a record you did not watch being written.

### What this guard cannot do

Two limits. Both are printed by the tool itself, beside "identity not
authenticated":

- **The self-attestation refusal cannot fire on a model name here.** It
  compares the reviewer string to the author names and emails git reports
  for the last 40 commits (`git log -40 --format='%an%n%ae'`). Measured on
  2026-09-21 at `ab4b1eb`, `git log -40 --format='%an <%ae>' | sort -u`
  returned one entry, the human owner, although 30 of those 40 commits carry a
  `Co-Authored-By: Claude` trailer. A trailer is not an author, so a model's
  name, the authoring model's included, never matches and always passes. The
  whole history does list `Claude <noreply@anthropic.com>` as an author, but
  only on commits older than that window. The refusal does not read them, so
  "Claude" passes it today like any other model name.
- **`independent_implementation` is not elicited.** The tool writes it as
  `true` on every record, and the validator rejects any record where it is not
  `true`. The one field saying the reviewer implemented none of the tree is
  therefore generated by the tool, never asked of the reviewer, and never
  checked against anything.

A third limit is about the evidence itself. The allowlist guarantees one
thing: every recorded command is a check this repository defines, exactly as
it defines it, so no wrapper written into the command (`sh -c`, `find -exec`,
a git `!` alias, `echo`, `python3 -c`) can put a result beside a real tool
that the tool never printed. The interpreter that runs `review_gate.py`, and
the machine it runs on, are trusted: whoever runs the tool controls both. Earlier rounds used a denylist of shells and command runners, and
an unlisted runner restored that chain every time. The allowlist does not
guarantee the output came from the tree the record pins. An allowlisted
check can still be run against a tree that differs from the one recorded,
and a hand-written record can carry output from anywhere; the tree-digest
comparison is what covers the first (the record goes stale when the tree
changes), and `--reexecute`, which re-runs each check on the tree as it is
now, is what covers the second. The checks are themselves files in the tree,
so a change that edits a check changes what that check proves. The digest
covers that edit; nothing here judges it. Read the diff to the checks.

So a record that passes is well-formed and current. It is not proof that a
review happened. Whether a party outside the authoring session read the
change, and who that party was, is the owner's attestation, not the tool's.

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
ci_gate.py result    : 21/22 with CI-6 the only red / other:
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
