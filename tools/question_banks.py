#!/usr/bin/env python3
"""Generator for pmos/question_banks.json, the versioned Conductor contract.

    python3 tools/question_banks.py            # write pmos/question_banks.json
    python3 tools/question_banks.py --check    # exit 1 when the committed file is stale

The contract compiles the six Markdown banks in skills/conductor/questions/ into
one JSON object that ships inside the pmos package, which the Markdown does not:
the wheel carries pmos/ and nothing from skills/conductor/. Each bank stays the
authored source and the contract is a reading of it. A bank's version is a hash
of what it contracts, so only a change to the contract makes a new version; a
change to the header prose does not. The tool fails, and writes nothing, when a
bank breaks a rule of the format in skills/conductor/questions/README.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "skills" / "conductor" / "questions"
ORDER = ("discover", "define", "design", "build", "deliver", "operate")
OUTPUT = ROOT / "pmos" / "question_banks.json"
RUNG_CLASSES = {
    1: "observed_behavior",
    2: "artifact",
    3: "named_commitment",
    4: "interview_claim",
    5: "team_belief",
}
# The lines an entry may carry, and the key each one gets in the contract.
FIELDS = {
    "Ask:": "ask",
    "Wrong costs:": "wrong_costs",
    "Evidence class:": "evidence",
    "Cross-examine when:": "cross_examine",
    "Accept when:": "accept_when",
    "Lands in:": "lands_in",
    "Options:": "options",
}
REQUIRED = ("Ask:", "Evidence class:", "Accept when:", "Lands in:")
STAGE_RE = re.compile(r"^Stage:\s*([A-Z]+),\s*feeds\s+Gate\s+(\d+)")
HEADING_RE = re.compile(r"^### ([A-Z]+)-(\d+):\s*(.+?)\s*$")
# A leading rung: one digit from 1 to 5, or "N or M", which reads as the
# larger number, the weaker rung the entry accepts.
RUNG_RE = re.compile(r"^\s*([1-5])(?:\s+or\s+([1-5]))?\b")


class BankError(ValueError):
    pass


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def bank_version(bank: dict) -> str:
    """'c' plus 16 hex characters of the sha256 of a parsed bank's JSON."""
    return "c" + _sha256_hex(_canonical(bank).encode("utf-8"))[:16]


def _id_pattern(stage: str):
    """Entry IDs of the six stages, and of this bank's own stage."""
    stages = sorted({name.upper() for name in ORDER} | {stage})
    return re.compile(r"\b(?:%s)-\d+\b" % "|".join(stages))


def _entries(text: str) -> list:
    """(heading, body lines) per '### ' entry, which runs to the next heading."""
    entries, current = [], None
    for line in text.split("\n"):
        if line.startswith("### "):
            current = (line, [])
            entries.append(current)
        elif line.startswith("## "):
            current = None
        elif current is not None:
            current[1].append(line)
    return entries


def _sections(text: str) -> dict:
    """The '## ' sections of a bank, heading text to body lines."""
    sections, current = {}, None
    for line in text.split("\n"):
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif line.startswith("### "):
            current = None
        elif current is not None:
            sections[current].append(line)
    return sections


def _parse_question(stage: str, heading: str, body: list) -> tuple:
    match = HEADING_RE.match(heading)
    if not match or match.group(1) != stage:
        raise BankError("%s: entry heading %r is not '### %s-<n>: <handle>'"
                        % (stage, heading, stage))
    number = int(match.group(2))
    entry_id = "%s-%d" % (stage, number)
    values = {}
    for line in body:
        for prefix in FIELDS:
            if line.startswith(prefix):
                if prefix in values:
                    raise BankError("%s: repeats its %s line"
                                    % (entry_id, prefix))
                values[prefix] = line[len(prefix):].strip()
                break
    for prefix in REQUIRED:
        if not values.get(prefix):
            raise BankError("%s: has no %s line" % (entry_id, prefix))
    rung = RUNG_RE.match(values["Evidence class:"])
    if not rung:
        raise BankError("%s: its Evidence class line names no rung from 1 "
                        "to 5" % entry_id)
    evidence_rung = max(int(rung.group(1)), int(rung.group(2) or 0))
    question = {key: values.get(prefix) for prefix, key in FIELDS.items()}
    question.update(id=entry_id, handle=match.group(3),
                    evidence_rung=evidence_rung,
                    evidence_class=RUNG_CLASSES[evidence_rung])
    return number, question


def _forced_pair(stage: str, lines: list, entry_ids: set) -> list:
    found = []
    for entry_id in _id_pattern(stage).findall("\n".join(lines)):
        if entry_id not in found:
            found.append(entry_id)
    pair = found[:2]
    if len(pair) != 2 or not set(pair) <= entry_ids:
        raise BankError("%s: the Forced pair section must name two of this "
                        "bank's entries" % stage)
    return pair


def _gate_rendering(stage: str, gate: int, lines: list) -> list:
    pattern = _id_pattern(stage)
    table = [line.strip() for line in lines if line.strip().startswith("|")]
    rows = []
    for line in table[1:]:  # the first table line is the header
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2 or not cells[0] or set(cells[0]) <= set("-: "):
            continue  # the separator row
        rows.append({"line": cells[0], "evidenced_by": cells[1],
                     "questions": pattern.findall(cells[1])})
    if not rows:
        raise BankError("%s: the Gate %d rendering table has no rows"
                        % (stage, gate))
    return rows


def parse_bank(stage: str, text: str) -> dict:
    """One bank's contract, raising BankError on any broken format rule."""
    upper = stage.upper()
    header = next((line for line in text.split("\n")
                   if line.startswith("Stage:")), "")
    match = STAGE_RE.match(header)
    if not match or match.group(1) != upper:
        raise BankError("%s: needs a header line 'Stage: %s, feeds Gate N'"
                        % (upper, upper))
    gate = int(match.group(2))
    questions, previous = [], 0
    for heading, body in _entries(text):
        number, question = _parse_question(upper, heading, body)
        if number <= previous:
            raise BankError("%s: entry numbers must increase, and %s follows "
                            "%s-%d" % (upper, question["id"], upper, previous))
        previous = number
        questions.append(question)
    if not questions:
        raise BankError("%s: has no entries" % upper)
    sections = _sections(text)
    rendering = "Gate %d rendering" % gate
    if "Forced pair" not in sections or rendering not in sections:
        raise BankError("%s: needs a Forced pair and a %s section"
                        % (upper, rendering))
    return {
        "id": stage,
        "stage": upper,
        "gate": gate,
        "questions": questions,
        "forced_pair": _forced_pair(
            upper, sections["Forced pair"], {q["id"] for q in questions}),
        "gate_rendering": _gate_rendering(upper, gate, sections[rendering]),
    }


def compile_contract() -> dict:
    """The six banks in loop order, each with its source hash and version."""
    banks = []
    for stage in ORDER:
        path = SOURCE_DIR / ("%s.md" % stage)
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
        except (OSError, UnicodeDecodeError) as error:
            raise BankError("%s: cannot read %s: %s" % (stage.upper(), path,
                                                        error))
        bank = parse_bank(stage, text)
        version = bank_version(bank)
        bank.update(source="skills/conductor/questions/%s.md" % stage,
                    source_sha256=_sha256_hex(raw), version=version)
        banks.append(bank)
    return {"schema": 1, "generated_by": "tools/question_banks.py",
            "banks": banks}


def render(contract: dict) -> str:
    return json.dumps(contract, indent=1, sort_keys=True,
                      ensure_ascii=False) + "\n"


def _shown(path) -> str:
    """A path as the messages show it: repo-relative when it is in the repo."""
    try:
        return Path(path).relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--check", action="store_true",
        help="regenerate in memory and fail when the committed "
             "pmos/question_banks.json is stale")
    args = parser.parse_args(argv)

    try:
        contract = compile_contract()
    except BankError as error:
        print("question banks: %s" % error, file=sys.stderr)
        return 1
    payload = render(contract).encode("utf-8")  # explicit LF, never translated
    shown = _shown(OUTPUT)

    if args.check:
        try:
            current = OUTPUT.read_bytes()
        except OSError:
            print("%s is missing. Run: python3 tools/question_banks.py"
                  % shown, file=sys.stderr)
            return 1
        if current != payload:
            print("%s is stale: it does not match what "
                  "tools/question_banks.py generates from the banks (byte "
                  "comparison, so a stray CRLF counts as stale too). Run: "
                  "python3 tools/question_banks.py, then commit the result."
                  % shown, file=sys.stderr)
            return 1
        print("%s: ok (up to date)" % shown)
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(payload)
    print("%s: written" % shown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
