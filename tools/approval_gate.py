#!/usr/bin/env python3
"""Execute the approval-gate contract in templates/ai/human-approval-gates.md.

    python3 tools/approval_gate.py --check     # exit 1 when a document dropped a rule
    python3 tools/approval_gate.py --cases     # print the fixture verdicts

Why this exists. The template used to say when an approval is asked for, who
answers and what happens on silence, and stopped there. Nothing bound the yes
to the bytes the approver saw, so an edited payload, an approval that had
expired, one that had been revoked, and one already spent all executed exactly
like a fresh one, and a send whose outcome was never established could be
retried into a second real send. Prose alone cannot fail, so the six rules the
template now carries are also six fixtures here: decide() refuses each of them,
and check() refuses a copy of the document that has dropped the rule, the
record field or the negative criterion that names them, moved one of those rows
out of the section that holds it, lost one of the numbered sections, hidden the
rules inside an HTML comment, kept a rule's heading over a sentence that no
longer says it, marked the contract historical, or deleted the document
outright. It reads the template and every filled copy in examples/, because the
copy this contract is most likely to be missing from is the one a second
product writes next.

decide() is the reference executor, not the product's. A team implements R1 to
R6 in their own stack; this file is what makes the template's claim checkable
inside this repository, and what a reader can run to see each refusal happen.

It is also a pure function and keeps no state: it reads the approval and the
attempt it is handed and never writes the consumption back. R5 therefore holds
only for a caller that persists the move to consumed, or the attempt's outcome,
between attempts. A caller that persists neither hands decide() an approval that
still reads approved, with the same token and no prior outcome, and is told to
execute. The record fields exist so a real implementation has somewhere to put
that; this file cannot enforce that it does.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

TEMPLATE = "templates/ai/human-approval-gates.md"
EXAMPLE = "examples/ledgerline-human-approval-gates.md"
# Every filled copy, not only the one that exists today. A second product's
# copy is the cheapest place for this contract to quietly not arrive, and a
# checker that names one file would never look at it.
EXAMPLE_GLOB = "examples/*human-approval-gates*.md"

# Section 4 of the template. Each field is named in the document by this
# string; a document that dropped one cannot hold an approval this file would
# execute, so check() reports the loss rather than the tests passing anyway.
RECORD_FIELDS = (
    "Approval ID",
    "Action revision",
    "Approver identity and authority scope",
    "Issued at / Expires at",
    "State",
    "Single-use execution token",
    "Execution record",
)

# Section 4's state vocabulary. "approved" is the only state an execution may
# start from; every other state is a refusal, which is why they are enumerated
# rather than left to a truthy check on a string.
STATES = ("pending", "approved", "denied", "expired", "revoked", "superseded",
          "consumed")
EXECUTABLE_STATE = "approved"

# Section 5. The rule id, the refusal reason decide() returns for it, and the
# negative criterion in section 6 that has to fail for it.
RULES = (
    ("R1", "binding", "superseded", "NAC-1"),
    ("R2", "authority", "out-of-scope", "NAC-2"),
    ("R3", "expiry", "expired", "NAC-3"),
    ("R4", "revocation", "revoked", "NAC-4"),
    ("R5", "one-use", "replay", "NAC-5"),
    ("R6", "uncertain outcome", "unreconciled", "NAC-6"),
)

# What each rule's sentence has to still say. Keeping the "**R5 one-use.**"
# heading and replacing the sentence under it with "Reuse is fine; retry as
# often as you like." passes a check that only looks for the heading, so every
# term below has to appear in the sentence itself. Each term appears in BOTH the
# template's wording and the worked example's different wording, so the list
# constrains what the rule still has to say without dictating one phrasing.
_REFUSES = r"refus|never|must not|is not|does not|denied"
RULE_TERMS = {
    "R1": (r"supersed", r"revision"),
    "R2": (r"executor", r"approver"),
    "R3": (r"expir", _REFUSES),
    "R4": (r"revok", _REFUSES),
    "R5": (r"second", _REFUSES),
    "R6": (r"idempotency", r"retry", _REFUSES),
}
# So a failure reads as English rather than as the alternation.
TERM_NAMES = {_REFUSES: "that it refuses"}

# A phrase that tells the reader the contract is dead. Prefixing section 5 with
# "<!-- HISTORICAL, NO LONGER REQUIRED -->" leaves every structural match
# intact, so these are searched on the raw text, HTML comments included.
# "Not applicable" is deliberately absent: the worked example's fail-open
# register uses it honestly, to say that no gate fails open.
NULLIFIERS = (
    r"no longer required", r"no longer appl", r"\bhistorical\b",
    r"\bdeprecated\b", r"\bobsolete\b", r"not enforced",
    r"for reference only", r"informational only", r"does not apply",
)

# The outcome of the previous attempt on the same approval, when there was one.
# "unknown" is the timed-out send that has to be reconciled before any retry.
# This field was unvalidated while the approval's own state was enforced, so
# prior_outcome="Unknown" (wrong capitalisation) silently turned off R6 and half
# of R5 and the attempt was ALLOWED. The vocabulary is enforced in
# Attempt.__post_init__ now: a typo raises rather than quietly executing, which
# is the failure class this whole file exists to make visible.
OUTCOMES = (None, "done", "refused", "unknown")


def revision(parameters) -> str:
    """The action revision: a hash of the exact parameters, not of a summary."""
    payload = json.dumps(parameters, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Approval:
    approval_id: str
    action_revision: str
    approver: str
    authority_scope: dict           # e.g. {"action": "send", "max_amount": 500}
    issued_at: int
    expires_at: int
    state: str
    execution_token: str
    attempts: tuple = field(default_factory=tuple)

    def __post_init__(self):
        if self.state not in STATES:
            raise ValueError("unknown approval state: %r" % (self.state,))


@dataclass(frozen=True)
class Attempt:
    """One execution attempt: the parameters as they stand now, plus the token
    presented and what is known about any earlier attempt."""
    parameters: dict
    execution_token: str
    at: int
    # One of OUTCOMES. Enforced, not documented: see the note there.
    prior_outcome: str = None
    reconciled: bool = False

    def __post_init__(self):
        if self.prior_outcome not in OUTCOMES:
            raise ValueError("unknown prior outcome: %r" %
                             (self.prior_outcome,))


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str
    rule: str = ""


def _in_scope(scope: dict, parameters: dict) -> bool:
    """Does this approver's authority still cover this action? Every key the
    scope names is checked; a scope that names nothing covers nothing, which is
    deliberate: an empty scope is an unanswered question, not a blank cheque."""
    if not scope:
        return False
    for key, allowed in scope.items():
        if key.startswith("max_"):
            value = parameters.get(key[len("max_"):])
            # A ceiling on something that is not a number is a scope nobody can
            # evaluate. Comparing them raises in Python 3, and an exception is
            # not a documented refusal path: the caller sees a crash where the
            # contract promises a decision, so it is refused instead.
            if not _numeric(value) or not _numeric(allowed):
                return False
            if value > allowed:
                return False
        elif parameters.get(key) != allowed:
            return False
    return True


def _numeric(value) -> bool:
    """True for a real number. bool is int in Python, and True > 500 is a
    comparison nobody meant to authorise, so it is excluded."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def decide(approval: Approval, attempt: Attempt) -> Decision:
    """Refuse or allow one execution attempt. The order matters: an expired
    approval for an edited payload is refused for the first reason found, and
    every branch below is reachable from the fixtures in CASES."""
    # R6 first: an attempt whose outcome nobody established is not a fresh
    # start. Checking it after R5 would let "consumed, outcome unknown" be
    # reported as a replay and quietly retried by a caller that treats replay
    # as a duplicate no-op.
    if attempt.prior_outcome == "unknown" and not attempt.reconciled:
        return Decision(False, "unreconciled", "R6")
    if approval.state == "consumed" or attempt.prior_outcome in ("done",):
        return Decision(False, "replay", "R5")
    if approval.state == "revoked":
        return Decision(False, "revoked", "R4")
    if approval.state == "superseded":
        return Decision(False, "superseded", "R1")
    if approval.state == "expired" or attempt.at > approval.expires_at:
        return Decision(False, "expired", "R3")
    if approval.state != EXECUTABLE_STATE:
        return Decision(False, "not-approved", "R1")
    if revision(attempt.parameters) != approval.action_revision:
        return Decision(False, "superseded", "R1")
    if attempt.execution_token != approval.execution_token:
        return Decision(False, "replay", "R5")
    if not _in_scope(approval.authority_scope, attempt.parameters):
        return Decision(False, "out-of-scope", "R2")
    return Decision(True, "executed", "")


# --- fixtures ------------------------------------------------------------
# One per negative criterion, plus the positive controls. The base approval is
# the one that executes; each negative case is that same approval with exactly
# one thing wrong, so a fixture cannot pass for a reason other than its rule.

PARAMS = {"action": "send", "amount": 120, "recipient": "acct-7781"}
NOW = 1_000
BASE = Approval(
    approval_id="AP-1",
    action_revision=revision(PARAMS),
    approver="duty ops reviewer",
    authority_scope={"action": "send", "max_amount": 500},
    issued_at=NOW - 100,
    expires_at=NOW + 900,
    state="approved",
    execution_token="tok-1",
)


def _replace(approval: Approval, **changes) -> Approval:
    values = {**approval.__dict__, **changes}
    return Approval(**values)


CASES = {
    "NAC-1": (BASE, Attempt({**PARAMS, "amount": 4_000}, "tok-1", NOW),
              False, "superseded"),
    "NAC-2": (_replace(BASE, authority_scope={"action": "send",
                                              "max_amount": 50}),
              Attempt(PARAMS, "tok-1", NOW), False, "out-of-scope"),
    "NAC-3": (BASE, Attempt(PARAMS, "tok-1", NOW + 1_000), False, "expired"),
    "NAC-4": (_replace(BASE, state="revoked"), Attempt(PARAMS, "tok-1", NOW),
              False, "revoked"),
    "NAC-5": (_replace(BASE, state="consumed"), Attempt(PARAMS, "tok-1", NOW,
              prior_outcome="done"), False, "replay"),
    "NAC-6": (_replace(BASE, state="consumed"), Attempt(PARAMS, "tok-1", NOW,
              prior_outcome="unknown"), False, "unreconciled"),
}

# The positive controls. Without them a decide() that refused everything would
# satisfy all six negative fixtures.
POSITIVE = {
    "clean": (BASE, Attempt(PARAMS, "tok-1", NOW), True, "executed"),
    # R6's other half: once the timed-out send has been reconciled and the
    # downstream system reports it never landed, the retry is allowed.
    "reconciled-retry": (BASE, Attempt(PARAMS, "tok-1", NOW,
                         prior_outcome="unknown", reconciled=True),
                         True, "executed"),
}


# --- document check ------------------------------------------------------
# Three ways to hollow the document out without touching a heading were found
# by review, so structure alone is not enough. HTML comments are stripped before
# any structural match, because a rules section wrapped in <!-- ... --> renders
# as nothing while its lines still satisfy a line-anchored regex. Each rule's
# sentence has to carry its own load-bearing terms, because a bold heading kept
# over a reversed sentence is not the rule. A phrase declaring the contract dead
# is refused on the raw text, comments included.
# What this does NOT do: it is a phrase and term list, not comprehension. A
# rewrite that keeps the terms and still says something wrong passes.

def _prose(text: str) -> str:
    """The document as it renders: HTML comments removed. Commenting section 5
    out leaves every numbered rule line intact for a line-anchored regex, so
    structural matching reads this and never the raw bytes."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def _rule_sentence(text: str, rule_id: str, name: str):
    """The sentence under the numbered, bolded definition in section 5, or None
    when the definition is gone. Not any mention of the id: a substring search
    for "R5" passes on the exit gate's "R1 to R6" and on section 6's rule
    column, so deleting the rule itself would not be caught. That version of
    this check was written first and is what the removal fixtures in
    test_tools_gates caught."""
    pattern = r"^\s*\d+\.\s+\*\*%s %s\.\*\*(.*)$" % (re.escape(rule_id),
                                                     re.escape(name))
    found = re.search(pattern, text, re.M)
    return found.group(1) if found else None


def _missing_terms(sentence: str, rule_id: str) -> list:
    """Which of the rule's load-bearing terms the sentence no longer carries."""
    return [TERM_NAMES.get(term, repr(term)) for term in RULE_TERMS[rule_id]
            if not re.search(term, sentence, re.I)]


def _criterion_row(text: str, criterion: str, rule_id: str) -> bool:
    """The row in section 6's table, bound to its rule. Same reason: "NAC-6"
    appears in "NAC-1 to NAC-6" whether or not the row survives."""
    pattern = r"^\|\s*%s\s*\|\s*%s\s*\|" % (re.escape(criterion),
                                             re.escape(rule_id))
    return re.search(pattern, text, re.M) is not None


def _field_row(text: str, name: str) -> bool:
    pattern = r"^\|\s*%s\s*\|" % re.escape(name)
    return re.search(pattern, text, re.M) is not None


def _section(text: str, number: int):
    """The body of "## <number>. ..." up to the next level-two heading, or None
    when that heading is gone. Every lookup below is scoped to the section that
    owns it: without that, a row deleted from the approval record still passes
    while a row of the same name sits in any other table, and a document that
    renamed section 4 away passes on rows found under whatever replaced it."""
    heading = re.search(r"^## %d\..*\n" % number, text, re.M)
    if heading is None:
        return None
    body = text[heading.end():]
    following = re.search(r"^## ", body, re.M)
    return body[:following.start()] if following else body


def _state_rows(text: str) -> list:
    """Every State row in section 4, which is where the vocabulary is declared.
    All of them, not the first: a decoy State row placed above a gutted real
    one is exactly how a first-match lookup is defeated, and a record with two
    State rows is malformed whichever one an executor reads."""
    return [found.group(1) for found in
            re.finditer(r"^\|\s*State\s*\|(.*)$", text, re.M)]


def _issues_for(root: Path, relative: str, states: bool) -> list:
    path = root / relative
    if not path.is_file():
        # Deleting the document is the cheapest way to pass a check that only
        # reads documents it finds, so the loss is the finding.
        return ["%s: missing" % relative]
    raw = path.read_text(encoding="utf-8")
    text = _prose(raw)
    issues = []
    for phrase in NULLIFIERS:
        found = re.search(phrase, raw, re.I)
        if found:
            issues.append("%s: the contract is marked dead by %r" %
                          (relative, found.group(0)))
    # 4 holds the approval record, 5 the rules, 6 the negative criteria. A
    # section whose heading is gone is reported, and its contents are then
    # looked for in an empty string rather than anywhere in the document: what
    # is not in the section is not in the section.
    sections = {}
    for number in (4, 5, 6):
        body = _section(text, number)
        if body is None:
            issues.append("%s: section %d is not there" % (relative, number))
        sections[number] = body or ""
    for rule_id, name, _reason, criterion in RULES:
        sentence = _rule_sentence(sections[5], rule_id, name)
        if sentence is None:
            issues.append("%s: rule %s (%s) is not stated" %
                          (relative, rule_id, name))
        else:
            missing = _missing_terms(sentence, rule_id)
            if missing:
                issues.append("%s: rule %s (%s) no longer says %s" %
                              (relative, rule_id, name, ", ".join(missing)))
        if not _criterion_row(sections[6], criterion, rule_id):
            issues.append("%s: negative criterion %s (%s) is not stated" %
                          (relative, criterion, rule_id))
    for field_name in RECORD_FIELDS:
        if not _field_row(sections[4], field_name):
            issues.append("%s: approval record field %r is not stated"
                          % (relative, field_name))
    if states:
        rows = _state_rows(sections[4])
        if not rows:
            issues.append("%s: the approval record has no State row" % relative)
        else:
            for state in STATES:
                if any(not re.search(r"\b%s\b" % re.escape(state), row)
                       for row in rows):
                    issues.append("%s: approval state %r is not in the State "
                                  "row" % (relative, state))
    return issues


def _examples(root: Path) -> list:
    """The named example, plus any other filled copy in examples/. The named
    one stays required: a repository that deleted it and kept another copy has
    still lost the document this template points readers at."""
    found = {str(path.relative_to(root)) for path in root.glob(EXAMPLE_GLOB)}
    return sorted(found | {EXAMPLE})


def check(root: Path = REPO) -> list:
    """Every document carries the rules, their negative criteria and all seven
    record fields; only the template declares the whole state vocabulary,
    because states a worked example never reaches are not required to appear in
    it. The record fields are checked in the examples too: closing a hole in
    the template and leaving it open in the filled copy closes nothing."""
    issues = _issues_for(root, TEMPLATE, states=True)
    for relative in _examples(root):
        issues += _issues_for(root, relative, states=False)
    return issues


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="fail when a document dropped part of the contract")
    parser.add_argument("--cases", action="store_true",
                        help="print each fixture's verdict")
    parser.add_argument("--root", default=str(REPO))
    args = parser.parse_args(argv)
    root = Path(args.root)
    status = 0
    if args.cases or not args.check:
        for name, (approval, attempt, _allowed, _reason) in (
                list(CASES.items()) + list(POSITIVE.items())):
            verdict = decide(approval, attempt)
            print("%-18s %-8s %s" % (name,
                                     "allow" if verdict.allowed else "refuse",
                                     verdict.reason))
    if args.check:
        issues = check(root)
        for issue in issues:
            print(issue, file=sys.stderr)
        if issues:
            print("approval-gate contract: %d problem(s)" % len(issues),
                  file=sys.stderr)
            status = 1
        else:
            print("approval-gate contract: ok (%d rules, %d fixtures)"
                  % (len(RULES), len(CASES) + len(POSITIVE)))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
