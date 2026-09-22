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
bank breaks a rule of the format in skills/conductor/questions/README.md, or
when its gate rendering table has more or fewer rows than its gate has
checklist lines in os/STAGE-GATES.md.
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
STAGE_GATES = ROOT / "os" / "STAGE-GATES.md"
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
GATE_HEADING_RE = re.compile(r"^## Gate (\d+):")
# A checklist line is any box lint.py's CHECKBOX_RE accepts: '-' or '*', indented
# or not, ticked or not. Matching '- [ ] ' alone let a line written '* [ ] ' or
# '- [x] ' join a gate without the count noticing.
CHECKLIST_BOX_RE = re.compile(r"^\s*[-*]\s*\[[ xX]\]\s*")
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


def parse_signoffs(text: str) -> dict:
    """Map gate number to the role names in its sign-off table."""

    lines = text.split("\n")

    def _split_cells(row: str) -> list:
        return [cell.strip() for cell in row.strip().strip("|").split("|")]

    def _is_separator(cell: str) -> bool:
        return set(cell) <= set("-: ")

    signoffs = {}
    for gate in range(1, 7):
        heading = "## Gate %d:" % gate
        start = None
        for index, line in enumerate(lines):
            if line.startswith(heading):
                start = index + 1
                break
        if start is None:
            raise BankError("os/STAGE-GATES.md: Gate %d has no sign-off table"
                            % gate)
        end = len(lines)
        for index in range(start, len(lines)):
            if index >= start and lines[index].startswith("## "):
                end = index
                break
        section = lines[start:end]

        found = False
        line = 0
        roles = []
        while line < len(section):
            if not section[line].startswith("|"):
                line += 1
                continue

            table = []
            while line < len(section) and section[line].startswith("|"):
                table.append(section[line])
                line += 1

            header = _split_cells(table[0])
            if header and header[0] == "Sign-off":
                found = True
                for body in table[1:]:
                    cells = _split_cells(body)
                    if not cells:
                        continue
                    first = cells[0]
                    if not first or _is_separator(first):
                        continue
                    roles.append(first)
                break

        if not found or not roles:
            raise BankError("os/STAGE-GATES.md: Gate %d has no sign-off table"
                            % gate)
        signoffs[str(gate)] = roles
    return signoffs


def parse_checklists(text: str) -> dict:
    """Map gate number to the checklist lines of its section, box stripped, in order.

    A gate's section runs from its '## Gate N:' heading to the next line that
    starts with '## ', whatever that heading names, not to the next gate: the
    file closes with sections that are not gates, and a box in one of those
    would otherwise be counted as the last gate's line.
    """
    checklists, current = {}, None
    for line in text.split("\n"):
        heading = GATE_HEADING_RE.match(line)
        if heading:
            current = checklists.setdefault(int(heading.group(1)), [])
        elif line.startswith("## "):
            current = None
        elif current is not None:
            box = CHECKLIST_BOX_RE.match(line)
            if box:
                current.append(line[box.end():].strip())
    return checklists


def check_checklist_coverage(bank: dict, checklists: dict) -> None:
    """Refuse a bank whose gate rendering has a row count unlike its gate's checklist.

    Rows against checklist lines, not against questions: one question can
    evidence several lines and a line can need a signature no question asks
    for, so those two counts differ in shipped banks and are meant to. Counts,
    not text: every row paraphrases its line on purpose, so comparing wording
    would reject each faithful paraphrase. What a count catches is the drift
    that happened, a line added to the gate with no row added to the bank, and
    it has to be caught here because the runtime never reads these rows when
    it records a gate approval. A row paired with the wrong line has the right
    count, so it passes this check.
    """
    gate, source = bank["gate"], "skills/conductor/questions/%s.md" % bank["id"]
    lines = checklists.get(gate)
    if lines is None:
        raise BankError("%s feeds Gate %d, and os/STAGE-GATES.md has no Gate %d "
                        "checklist" % (source, gate, gate))
    rows = bank["gate_rendering"]
    if len(rows) != len(lines):
        raise BankError(
            "Gate %d in os/STAGE-GATES.md has %d checklist lines but the Gate %d "
            "rendering table in %s has %d rows; add or remove rows until each "
            "checklist line has one" % (gate, len(lines), gate, source, len(rows)))


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
    try:
        stage_gates_text = STAGE_GATES.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise BankError("cannot read %s: %s" % (STAGE_GATES, error))
    signoffs = parse_signoffs(stage_gates_text)
    checklists = parse_checklists(stage_gates_text)

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
        check_checklist_coverage(bank, checklists)
        version = bank_version(bank)
        bank.update(source="skills/conductor/questions/%s.md" % stage,
                    source_sha256=_sha256_hex(raw), version=version)
        banks.append(bank)

    # Every question id a gate_rendering row cites, against the ids the contract defines.
    # Checked here rather than in parse_bank because only compile_contract sees all six
    # banks: a row may legitimately cite an earlier stage's question, and one shipped row
    # does. Two ways for that to be wrong, and neither was caught before. A citation no
    # bank defines renders a row that can never be met, sits in the report forever and
    # fails no gate. A citation owned by a LATER bank asks a stage to prove itself with an
    # answer that does not exist yet. Keyed on the contract's own id map rather than on the
    # shape of an id, so a dotted id such as discover.person is checked the same way.
    owner_of = {}
    for position, bank in enumerate(banks):
        for question in bank.get("questions", []):
            owner_of[question["id"]] = (bank["id"], position)
    for position, bank in enumerate(banks):
        for row in bank.get("gate_rendering", []):
            for question_id in row.get("questions", []):
                owner = owner_of.get(question_id)
                if owner is None:
                    raise BankError(
                        "%s: the gate line %r cites %s, which no bank in this contract "
                        "defines" % (bank["id"].upper(), row.get("line"), question_id))
                if owner[1] > position:
                    raise BankError(
                        "%s: the gate line %r cites %s, which belongs to %s, a later stage; "
                        "a gate cannot be proved by an answer that does not exist yet"
                        % (bank["id"].upper(), row.get("line"), question_id, owner[0].upper()))

    return {"schema": 1, "generated_by": "tools/question_banks.py",
            "banks": banks, "signoffs": signoffs}


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
