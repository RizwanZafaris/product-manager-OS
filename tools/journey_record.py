import sys
import os
import json
import hashlib
import tempfile
import io
import contextlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pmos.cli import main as pmos_main

def run_main(argv):
    """Run pmos_main with argv, capture stdout, return (returncode, stdout_text)."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = pmos_main(argv)
    return rc, out.getvalue()

def status(folder):
    rc, stdout = run_main(["--json", "status", "--path", str(folder), "--product-id", "checkout"])
    return json.loads(stdout)

def answer(folder, evidence, token, turn_id, question_id):
    argv = ["answer", "--path", str(folder), "--product-id", "checkout", "--question-id", question_id,
            "--answer", "A real outcome", "--evidence", json.dumps(evidence),
            "--expected-revision", token, "--turn-id", turn_id, "--json"]
    rc, stdout = run_main(argv)
    return json.loads(stdout)

def process_bank(folder, prefix):
    """Run the question bank loop, return (final_status, questions_answered, answers_accepted)."""
    questions_answered = 0
    answers_accepted = 0
    for _ in range(20):
        st = status(folder)
        if st["interview"] != "question":
            break
        qid = st["question"]["id"]
        evidence = {"class": "observed_behavior", "source": "interview-001", "date": "2026-09-04",
                    "location": "customer-call"}
        ans = answer(folder, evidence, st["revision_token"], prefix + "-" + qid, qid)
        questions_answered += 1
        if ans["outcome"]["status"] == "accepted":
            answers_accepted += 1
    else:
        raise RuntimeError(f"Bank {prefix} did not finish within 20 answers")
    return st, questions_answered, answers_accepted

def generate_record_text():
    """Run the full journey and return the markdown text."""
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp) / "workspace"
        folder.mkdir()
        run_main(["init", "--path", str(folder), "--product-id", "checkout"])

        bank_ids = ["discover", "define", "design", "build", "deliver", "operate"]

        # Four refusals, attempted before anything is answered, so the section below
        # reports what the runtime did rather than what the generator was told to say.
        # Deleting the branch that enforces any one of these now changes this file and
        # fails `tools/journey_record.py --check`, which is what that gate is for.
        refusals = {}
        probe_proof = b"probe"
        (folder / "gate-probe.txt").write_bytes(probe_proof)
        full_proof = {"source": "gate-probe.txt",
                      "source_sha256": hashlib.sha256(probe_proof).hexdigest(),
                      "actor_id": "local-reviewer", "requester_id": "local-operator",
                      "decision": "approved", "approved_at": "2026-09-04T00:00:00Z"}

        def attempt(name, bank_id, evidence, turn_id):
            token = status(folder)["revision_token"]
            _rc, out = run_main(["gate", "--path", str(folder), "--product-id", "checkout",
                                 "--bank-id", bank_id, "--evidence", json.dumps(evidence),
                                 "--expected-revision", token, "--turn-id", turn_id, "--json"])
            payload = json.loads(out)
            outcome = payload.get("outcome") or {}
            state = outcome.get("status", payload.get("error", "no outcome"))
            if state not in ("blocked", "refused"):
                # A probe that is allowed through has both destroyed the rest of this run
                # and disproved the line it exists to evidence. Say which, rather than
                # letting the next gate call fail on a missing key several steps later.
                raise SystemExit(
                    "the runtime allowed the %r gate probe, which this record states is "
                    "refused: outcome %r, message %r. Either an enforcement branch is gone "
                    "or this probe is aimed at the wrong rule."
                    % (name, state, outcome.get("message", "")))
            refusals[name] = {"status": state, "message": outcome.get("message", "")}

        # Only the first of these can be attempted before anything is answered: the
        # unanswered-questions check fires first and would mask the other three, which
        # is how a row can look like a demonstration and be one of something else.
        attempt("unanswered", "discover", full_proof, "probe-unanswered")

        gate_outcomes = []
        questions_per_bank = []
        accepted_per_bank = []

        for idx, bank_id in enumerate(bank_ids, 1):
            st, q_count, a_count = process_bank(folder, bank_id)
            if idx == 1:
                # discover is answered and not yet gated, so each of these three reaches
                # the rule it is named for instead of stopping at the one before it.
                attempt("skipped", "define", full_proof, "probe-skipped")
                attempt("incomplete", "discover",
                        {k: v for k, v in full_proof.items() if k != "actor_id"},
                        "probe-incomplete")
                attempt("unauthorized", "discover",
                        dict(full_proof, actor_id="someone-else"), "probe-unauthorized")
                st = status(folder)
            proof_name = f"gate-{bank_id}.txt"
            proof_bytes = bank_id.encode()
            (folder / proof_name).write_bytes(proof_bytes)
            evidence = {"source": proof_name,
                        "source_sha256": hashlib.sha256(proof_bytes).hexdigest(),
                        "actor_id": "local-reviewer",
                        "requester_id": "local-operator",
                        "decision": "approved",
                        "approved_at": "2026-09-04T00:00:00Z"}
            rc, stdout = run_main(["gate", "--path", str(folder), "--product-id", "checkout", "--bank-id", bank_id,
                                   "--evidence", json.dumps(evidence),
                                   "--expected-revision", st["revision_token"],
                                   "--turn-id", f"gate-{bank_id}", "--json"])
            gate_res = json.loads(stdout)
            outcome = gate_res["outcome"]["status"]
            gate_outcomes.append(outcome)
            questions_per_bank.append(q_count)
            accepted_per_bank.append(a_count)

        # Staleness demonstration
        # a) initial status after six gates
        st_a = status(folder)
        interview_a = st_a["interview"]
        stale_a = [b["bank_id"] if isinstance(b, dict) else str(b) for b in st_a["stale_banks"]]

        # b) overwrite discover proof
        (folder / "gate-discover.txt").write_bytes(b"discover, edited after approval")
        st_b = status(folder)
        interview_b = st_b["interview"]
        stale_b = [b["bank_id"] if isinstance(b, dict) else str(b) for b in st_b["stale_banks"]]

        # c) re-prove discover
        new_sha = hashlib.sha256(b"discover, edited after approval").hexdigest()
        evidence_c = {"source": "gate-discover.txt", "source_sha256": new_sha,
                      "actor_id": "local-reviewer", "requester_id": "local-operator",
                      "decision": "approved", "approved_at": "2026-09-04T00:00:00Z"}
        rc, stdout_c = run_main(["gate", "--path", str(folder), "--product-id", "checkout",
                                 "--bank-id", "discover",
                                 "--evidence", json.dumps(evidence_c),
                                 "--expected-revision", st_b["revision_token"],
                                 "--turn-id", "gate-discover-again", "--json"])
        gate_c = json.loads(stdout_c)
        outcome_c = gate_c["outcome"]["status"]
        st_c = status(folder)
        interview_c = st_c["interview"]
        stale_c = [b["bank_id"] if isinstance(b, dict) else str(b) for b in st_c["stale_banks"]]

        # Build markdown
        lines = []
        lines.append("# Journey run: six stage gates through the pmos runtime")
        lines.append("")
        lines.append("This file fills no template. It is generated by `tools/journey_record.py`, which drives the `pmos` command line through all six question banks the same way `tests/test_pmos_cli.py` does, on a fictional product called checkout. Every answer, name, date and proof file is FICTIONAL TEST DATA: it proves the runtime executes and enforces the loop, not anything about a real product, sponsor or reviewer. See the [examples index](README.md).")
        lines.append("")
        lines.append("**Generated by:** `python3 tools/journey_record.py` · **Verified by:** `python3 tools/journey_record.py --check`")
        lines.append("")
        lines.append("## What the runtime enforced")
        lines.append("")
        lines.append("Each line below was attempted against this run and refused. The status and the")
        lines.append("runtime's own message are reproduced, so deleting the code that enforces any one of")
        lines.append("them changes this file and fails `python3 tools/journey_record.py --check`.")
        lines.append("")
        lines.append("| Attempted | Outcome | What the runtime said |")
        lines.append("|---|---|---|")
        for label, key in (("gate a bank with unanswered questions", "unanswered"),
                           ("gate a later bank, skipping the current one", "skipped"),
                           ("prove a gate with no actor_id in the proof", "incomplete"),
                           ("approve as an actor outside the bank's pinned approvers", "unauthorized")):
            got = refusals[key]
            lines.append(f"| {label} | {got['status']} | {got['message']} |")
        lines.append("")
        lines.append("- when a proof's source file changes after approval the gate goes stale and nothing later completes until it is proved again, which the Staleness table below shows happening.")
        lines.append("")
        lines.append("## Gates")
        lines.append("")
        lines.append("| Gate | Bank | Questions answered | Answers accepted | Gate outcome |")
        lines.append("|------|------|--------------------|--------------------|--------------|")
        for i, (bank, q, a, o) in enumerate(zip(bank_ids, questions_per_bank, accepted_per_bank, gate_outcomes), 1):
            lines.append(f"| {i} | {bank} | {q} | {a} | {o} |")
        lines.append("")
        lines.append("## Staleness")
        lines.append("")
        lines.append("| Step | What happened | interview | stale banks |")
        lines.append("|------|---------------|-----------|-------------|")
        lines.append(f"| a) | initial status after six gates | {interview_a} | {', '.join(stale_a) if stale_a else ''} |")
        lines.append(f"| b) | overwrite gate-discover.txt | {interview_b} | {', '.join(stale_b) if stale_b else ''} |")
        lines.append(f"| c) re-prove outcome | gate outcome after re-prove | {outcome_c} | not a status call |")
        lines.append(f"| c) status after re-prove | status call | {interview_c} | {', '.join(stale_c) if stale_c else ''} |")
        lines.append("")
        lines.append("")
        lines.append("## Result")
        total_accepted = sum(accepted_per_bank)
        lines.append(f"The runtime ended in interview state `{interview_c}` with {total_accepted} answers accepted across all six banks.")
        lines.append("")
        return "\n".join(lines)

def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description="Run the pmos journey and write a markdown record.")
    parser.add_argument("--out", default="examples/journey-run.md", help="output markdown file")
    parser.add_argument("--check", action="store_true", help="verify existing record matches a fresh run")
    args = parser.parse_args(argv)

    fresh = generate_record_text()
    if args.check:
        try:
            existing = Path(args.out).read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"Error: {args.out} does not exist")
            return 1
        if existing == fresh:
            print("journey record matches a fresh run")
            return 0
        else:
            # print unified diff
            import difflib
            diff = difflib.unified_diff(
                existing.splitlines(keepends=True),
                fresh.splitlines(keepends=True),
                fromfile=args.out,
                tofile="<fresh>"
            )
            sys.stdout.writelines(diff)
            return 1
    else:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(fresh, encoding="utf-8")
        return 0

if __name__ == "__main__":
    raise SystemExit(main())
