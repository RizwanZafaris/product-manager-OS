---
name: product-analyst
description: Run a disciplined research pass as a single analyst with one chat model. Use when DISCOVER needs cited evidence behind a discovery template, when OPERATE needs metric evidence for Gate 6, or when any claim is about to enter a template and would not survive the question "says who". Takes a research question and returns evidence notes with verbatim quotes, named tensions, and committed positions with confidence labels.
---

# Product Analyst: research that survives cross-examination

This skill is a distillation of a staged research pipeline into something one person with one chat model can run in an afternoon. The full pipeline uses parallel agents; here every stage becomes a pass, run in order, by you. What survives the distillation is the discipline: decompose before searching, search for disagreement on purpose, quote sources verbatim, name conflicts before drafting, and attack your own draft before anyone else sees it. What is deliberately left out is the machinery.

The analyst gathers and weighs evidence. It does not decide, draft requirements, or recommend a build. Its findings are what the Conductor's cross-examination stands on at Gate 1 and Gate 6, so a wrong "fact" here propagates into every later stage.

## Files this skill drives

- [../../templates/discovery/evidence-note.md](../../templates/discovery/evidence-note.md), one note per source, the atomic output of every pass
- [../../templates/discovery/discovery-document.md](../../templates/discovery/discovery-document.md) and [../../templates/discovery/problem-framing.md](../../templates/discovery/problem-framing.md), the evidence fields
- [../../templates/operate/metrics-review.md](../../templates/operate/metrics-review.md), the measurement evidence at OPERATE
- [../../templates/definition/assumptions-register.md](../../templates/definition/assumptions-register.md), where everything unverified goes
- The product's STATE.md evidence ledger, which takes each note's ledger row directly; the note format and the ledger share columns by design

For agent runtimes, [../../agents/research-agent.md](../../agents/research-agent.md) executes this method under its own operating rules; the method is the same either way.

## When to use

- Before Gate 1, when the discovery set needs facts that are citable rather than plausible
- Before Gate 6, when the success signal needs a measured number with its source system named
- Whenever a persona, market claim, or competitor statement is about to be written down as fact
- When two sources in the workspace already disagree and nobody has said so in writing

## Inputs

The research question, and the decision it is meant to inform, because a question with no decision behind it produces a document rather than an answer. The workspace as it stands, so existing evidence notes are read before new searches are run and the same source is not re-litigated. Any claim already written down as fact that this pass is expected to verify, named explicitly. And the date by which the answer is needed, which decides the sizing in pass 3 rather than being discovered when the count is already past twelve.

Ask for the decision when it is missing. If nobody can say what result would change what they do, say so and stop: this method is expensive and it is the wrong instrument for curiosity.

## The method: six passes, in order

Run them in order. Each pass produces a written artifact before the next begins, because work that lives only in the chat is work that evaporates.

### Pass 1: decompose

Break the research question into sub-questions, each one answerable and falsifiable, numbered SQ1, SQ2, and so on. List the named entities involved: companies, products, regulations, people, systems. Then run the coverage check: read the original question once more and confirm every part of it maps to a sub-question. Anything unmapped becomes a new sub-question or a written note that it is out of scope and why. A research pass that skips decomposition answers the question it drifted into, not the one it was asked.

### Pass 2: plan the searches, three lenses

Write the search plan before running any search, a few lines per lens:

1. **Breadth.** What is the landscape? Surveys, comparisons, recent coverage, the obvious queries.
2. **Canonical primary sources.** Who owns the ground truth? Official documentation, filings, standards bodies, the original paper or announcement rather than commentary about it. For anything with a research literature, primary literature before secondary summaries.
3. **Adversarial.** A deliberate hunt for who disagrees. At least one search phrased to find the strongest case against the emerging answer: criticism of X, limitations of X, X failure, why not X. Research that only confirms is advocacy, and the adversarial lens is the difference.

A sub-question with no adversarial search planned is not yet planned.

### Pass 3: one evidence note per source

For each source consulted, fill one [evidence note](../../templates/discovery/evidence-note.md). The load-bearing rule: every note carries the source's key sentence verbatim, in quotation marks, because paraphrase drifts and a quote is checkable later. If no single sentence in the source carries the claim, the claim is not in the source, and the note says what the source actually supports. Sources read and found irrelevant get a one-line note too: what was checked and why it did not apply. Silence about a dead end is how the next reader repeats it.

Typical sizing: three to five sources for a narrow factual question, eight to twelve for a Gate 1 problem worth funding. When the count wants to grow past that, the question is too big; go back to pass 1 and split it.

### Pass 4: name the tensions before drafting

Read the notes against each other and write down every pair that disagrees: note IDs, the claim in dispute, and which way each source points. Then classify each tension: one source is stronger (say why), the sources measure different things (say what), or the disagreement is real and unresolved (mark both notes contested). This pass exists because per-source findings, however well cited individually, do not force their tensions into the open on their own. A findings list with zero tensions across five or more sources is a warning sign, not a clean bill; say explicitly that agreement was checked for and found.

### Pass 5: commit a position per sub-question

For each SQ, write three lines:

- **Position.** The answer, one or two sentences, plain.
- **Confidence.** One of: verified (two or more independent sources agree), single-source, contested (sources disagree, and the position picks a side with reasons), unverified (belief, not evidence; route it to the assumptions register).
- **What would change my mind.** A specific, observable finding that would flip the position. "More data" is not an answer; name the datum.

Hedged non-positions ("it depends", "both views have merit") are returned to sender. The reader needs a position to argue with, and the confidence label plus the flip condition are what keep a committed position honest.

### Pass 6: adversarial pass against your own draft

Before handoff, re-read the whole output as a hostile reviewer whose job is to find the weakest claim. Check, in order: every claim traces to a note ID; every quote is verbatim against its source; every quantifier (most, many, growing) has a number behind it or is cut; every absence is reported as "not found where I looked", never as "does not exist"; every tension from pass 4 is either resolved or visibly carried as contested; nothing the model generated has been promoted to evidence. Fix what fails, then write one line naming the weakest remaining claim and why it was kept anyway. A handoff without that line has skipped this pass.

## Rules that bind every pass

1. Every claim carries a source a reader could open. "It is well known" is not a source.
2. Never assert beyond the source. Three complaints is three, not "widespread frustration".
3. Model output is not evidence. Summaries, inferences, and this skill's own drafts are labeled as such and never enter an evidence note as the source.
4. Date everything: source date and retrieved date, both, every note.
5. Never fabricate a statistic, quote, interviewee, or citation, under any pressure of completeness. A gap marked "unknown, here is the cheapest way to find out" is a valid deliverable.
6. Quotation marks are reserved for verbatim text.

## Output shape

The handoff is: the decomposition with its coverage check, the search plan, the evidence notes, the tension list, one committed position per sub-question, and the pass 6 weakest-claim line. Unverified items go to the assumptions register with a suggested validation method, not into any template as fact.

## Failure modes this skill guards against

- **Research that only confirms.** Every source agrees, no adversarial search was planned, and the conclusion is the one the requester arrived with. The adversarial lens in pass 2 exists because this is the default outcome, not the unusual one.
- **Paraphrase inside quotation marks.** A tidied sentence presented as the source's own words. It reads better, it is unfalsifiable later, and it is the single defect that makes an evidence ledger worthless.
- **Tensions never surfaced.** Notes are individually well cited and never read against each other, so a real disagreement between two sources survives into a persona as though it were settled.
- **Dead ends left unrecorded.** A source checked and found irrelevant, with nothing written, so the next person spends the same hour discovering the same nothing.
- **A position committed with no confidence class.** The answer is stated flatly, the reader assumes it is verified, and the single source it rested on is never visible again.

## Exit gate

Do not report the research done until every sub-question has a committed position with a confidence label and a flip condition, every position traces to at least one evidence note, and the adversarial pass has run against the draft that will actually be handed off, not an earlier version of it.
