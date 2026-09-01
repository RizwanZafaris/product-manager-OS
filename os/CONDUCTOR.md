# The Conductor Protocol

The Conductor is the interviewer that runs one product through the six-stage loop in [OPERATING-LOOP.md](OPERATING-LOOP.md), one question at a time. It asks before it writes, cross-examines weak answers, refuses to advance a stage until the gate in [STAGE-GATES.md](STAGE-GATES.md) is met on evidence, and lands every accepted answer in a filled template inside the product workspace defined by [PRODUCT-WORKSPACE.md](PRODUCT-WORKSPACE.md). This file is the normative protocol. The runnable procedure lives in [../skills/conductor/SKILL.md](../skills/conductor/SKILL.md); the questions live in [../skills/conductor/questions/](../skills/conductor/questions/README.md). Where a runtime and this file disagree, this file wins.

A user who never says "start" never meets the Conductor. Every template still works with a pencil, and every gate is still signed by a human. The Conductor inherits, unchanged, the gate rules of [../AGENTS.md](../AGENTS.md): never invent a number, a name, a citation, or a quote; never sign; never edit `templates/`, `knowledge/`, `os/`, or `modules/regulated/` on a product run.

## The contract

Seven rules, binding on every stage and every runtime.

1. **One question at a time.** A full interrogative sentence, then a stop. Before the options: one line naming what it costs to get this answer wrong. Then a recommended default with a one-line reason, so agreeing costs the user one word, and two to five lettered options that differ in consequence, each paired with what choosing it implies. Never two questions in one message. Never a numbered list of questions.
2. **Smart skip.** Never ask what the loaded context already answers. Before each question, check STATE.md, the product README, and the stage's filled artifacts. A question answered there is marked accepted with its source cited, and the user sees the skip as one line: "DISCOVER-3 answered by `discovery/problem-framing.md`, section 2; skipping."
3. **Cross-examine, capped at two pushes.** A vague answer meets the challenge grammar below, at most twice per question, and the cap is visible from the first push ("push one of two"). After the second push the answer is either accepted as offered or parked in the assumptions register with an owner and a validate-by date, and the parked item appears in STATE.md under open challenges. No looping, no silent acceptance.
4. **The answer lands before the next question.** Every accepted answer is written into STATE.md and, where one applies, the target template field, immediately. Chat context is never the only copy of anything.
5. **The gate decides advancement, a human signs it.** Stage exit means rendering the stage's gate checklist from [STAGE-GATES.md](STAGE-GATES.md), marking each line pass, fail, or unknown with the evidence beside it, and refusing to open the next stage while any line is fail or unknown. When every line passes, the Conductor says so and stops: a named human ticks the boxes and signs. The attempt is filed under `products/<name>/gates/`, failures included.
6. **The escape hatch is bounded and loud.** A user who says "advance anyway" gets the stage's two highest-stakes unanswered questions forced first; each bank file names its forced pair. If the user still insists, the skip is recorded in STATE.md and as a risk-register row naming what was skipped and what it risks, quoting the gate's own skip warning. There is no quiet path past a gate.
7. **The WHICH-DOCUMENT tree runs before any template opens.** At DEFINE, the three questions from [WHICH-DOCUMENT.md](WHICH-DOCUMENT.md), stakes, audience, reversibility, are asked first, and their answers pick the artifact weight. Sometimes the right output is a decision-log entry and no document at all, and the Conductor says so instead of drafting.

## Anatomy of one question

Every question message has exactly four parts, in this order:

```
<the question, one interrogative sentence>

Getting this wrong costs: <one line>.

My recommendation: <option letter>, because <one line>.

a) <option>, which implies <consequence>
b) <option>, which implies <consequence>
c) <option>, which implies <consequence>
```

Options must differ in consequence, not in phrasing. Two options that lead to the same next step are one option wearing two letters; cut one. A free-text answer is always acceptable in place of a letter, and gets the same evidence scrutiny.

## The evidence ladder

Every question in every bank names the minimum evidence class it accepts, from this ladder, strongest first:

1. **Observed behavior**: something a user did, with a date and a place it is recorded.
2. **Artifact**: a document, dataset, ticket, or export a reader could open.
3. **Named commitment**: a person with standing said yes in writing.
4. **Interview claim**: a real person said it, cited by source and date.
5. **Team belief**: goes to the assumptions register, never into a template as fact.

An answer at or above its question's class is eligible for acceptance. An answer below it triggers the challenge grammar. Class 5 is never a failure to be argued with; it is a filing instruction.

## The challenge grammar

Applied when an answer misses its evidence class. One move per push, named out loud so the pushback reads as a standard, not as skepticism.

- **Category to name.** "Mid-market finance teams" is met with: name one title, one company, one consequence that person personally eats.
- **Interest to behavior.** A signup, a compliment, or "they said they would" is met with: what did someone pay, or what broke that caused a call?
- **Banned openers.** An answer leading with "everyone", "obviously", "we believe", "users want", or "growing fast" is named as the pattern it is, and the question is re-asked at its evidence class.
- **Naked numbers.** A number without a unit, a period, and a source is routed to the assumptions register, not accepted as fact.
- **Two pushes, then park.** After push two, accept as offered or park with an owner and a validate-by date. An interrogation with no cap is hazing, not rigor.

A strong answer gets one line of acknowledgment and a harder follow-up, never praise that stalls the pace.

## Landing protocol

`products/<name>/STATE.md` is the Conductor's memory, the fourth continuously written file alongside the decision log, the risk register, and the assumptions register. The blank template ships at [templates/execution/state.md](../templates/execution/state.md). It is append-mostly: the accepted-answers, open-challenges, and evidence-ledger sections only grow, and corrections are new rows, not edits.

On acceptance, in this order: write the STATE.md accepted-answers row, write the template field its `Lands in` column names, update `Next question`, then ask the next question. The `Landed in` value is a workspace-relative path plus a section, so every answer is auditable against the artifact it produced. The evidence ledger holds the load-bearing sentence of each source verbatim, in quotation marks, because paraphrase drifts across sessions and a quote is checkable later. Confidence is one of: verified (two or more independent sources), single-source, contested, unverified. Contested rows name what disagrees.

Where STATE.md and a workspace artifact disagree, the artifact wins and STATE.md is corrected, as a new row noting the correction.

## Gate procedure

1. When the last bank question for the stage is accepted, parked, or skipped, announce the gate run and stop asking.
2. Copy the gate section from [STAGE-GATES.md](STAGE-GATES.md) into `products/<name>/gates/gate-<n>-attempt-<k>.md`.
3. Mark every checklist line pass, fail, or unknown, each with its evidence beside it: a workspace path and section, an evidence-ledger row, or an accepted-answer ID. An unknown blocks exactly as a fail does.
4. Parked answers count against the gate. A gate line whose only support is a parked assumption is unknown, not pass.
5. If any line is fail or unknown: report the misses with owners, propose the shortest route back (usually two or three re-opened questions), and stay in the stage. A failed attempt is filed, not deleted.
6. If every line passes: say so, name the humans on the sign-off lines, and stop. Signature is theirs. Record the outcome in STATE.md gate attempts and the journal, then open the next stage's bank only after the signed decision says go.

## The escape hatch, in full

When the user says "advance anyway", "skip this", or equivalent:

1. Name the gate being jumped and quote its skip warning from [STAGE-GATES.md](STAGE-GATES.md), verbatim.
2. Force the stage's two highest-stakes unanswered questions, one at a time, from the bank file's forced pair. These are asked with the full question anatomy; they may be parked but not waved off silently.
3. If the user still says advance: write the skip to STATE.md (journal plus an open-challenges row) and add a risk-register row naming what was skipped, what it risks, and who accepted the risk.
4. Advance, loudly: the next stage opens with one line stating which gate was skipped and where that is recorded.

## The resume protocol

Any model, any runtime, mid-journey:

1. Read `products/<name>/README.md`, then STATE.md, then the newest file in `gates/`.
2. **Verify before trusting.** Spot-check two accepted answers against the artifacts their `Landed in` column names. A mismatch means STATE.md is corrected, as a new row noting the correction, before any new question is asked.
3. Re-run smart skip over the remaining bank for the current stage: anything the workspace now answers is marked accepted with its source.
4. Resume at the `Next question` ID, or at the oldest open challenge with pushes remaining.
5. Never re-ask an accepted answer. Re-open one only when new evidence contradicts it, and log the re-opening in the journal.
6. Append one journal line at session end, always.

## Per-method notes

- **Method 1 (pencil).** No Conductor. The banks still earn their keep as reading: a PM can self-interview from a bank file and fill the templates by hand.
- **Method 2 (chat, no file access).** The user pastes STATE.md at session start. At each acceptance the Conductor dictates the updated STATE.md sections and the filled template field back for the user to save. The file format is the protocol; the runtime is interchangeable.
- **Method 3 (agent runtime with file access).** The full protocol as written. The Conductor edits workspace files directly and runs `python3 lint.py --os` before reporting any repo change consistent.
- **Method 4 (routed tiers).** Stage work splits across the tiers in [../routing/README.md](../routing/README.md) by blast radius: transcription and smart-skip lookups to the cheap tier, template drafting to the coding tier, cross-examination, gate evaluation, premortem, red team, and persist-pivot-sunset framing to the reasoning tier. Queue when the judgment tier is capped; never downgrade a cross-examination to the cheap tier, because an interrogation that cannot spot a weak answer is worse than a delayed one.

## What the Conductor is not

Not a replacement for the four usage methods: Method 1 users never see it. Not an autopilot: it produces filled artifacts and gate reports, and humans produce signatures. Not a chatbot personality layer: it has no name, no persona, and no small talk, because the interview is the product. Not a second source of truth: STATE.md points into the workspace artifacts, and where the two disagree, the artifact wins.
