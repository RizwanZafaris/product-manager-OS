---
layer: templates
stage: DISCOVER
gate: 1
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Evidence Note", "evidence-note"]
---
# Evidence Note: [source short name]

Stage: DISCOVER and OPERATE, feeds Gate 1 and Gate 6
Knowledge: [Knowledge index](../../knowledge/INDEX.md)
Skill: [product-analyst](../../skills/product-analyst/SKILL.md)

<!-- One note per source. Not per claim, not per topic: per source. If one
     source supports three claims, write three claim blocks in one note; if one
     claim needs three sources, that is three notes that cite each other.

     The verbatim quote is the point of this file. A paraphrase drifts a little
     with every retelling, and six weeks later nobody can check it without
     re-reading the source. A quote is checkable in ten seconds. If no single
     sentence in the source carries your claim, your claim is not in the source.

     The ledger row at the bottom is copied unchanged into the product's
     STATE.md evidence ledger. Keep it to one line; the note above it holds
     everything that does not fit. -->

**Note ID:** E[number, unique within the product workspace]
**Author:** [name or runtime] · **Retrieved:** [YYYY-MM-DD]

## Source

- **Name:** [publication, document, system, or person]
- **Locator:** [URL, file path, ticket ID, or interview reference a reader could open]
- **Source date:** [YYYY-MM-DD, when the source was published or the interview held]
- **Type:** [interview / ticket / metric export / document / public page / dataset / observation]

## Claim

[One sentence, your words, stating what this source supports. If the source supports several distinct claims, repeat this section and the two below it per claim.]

**Verbatim quote:**

> "[The load-bearing sentence, unchanged, in quotation marks. Ellipses only for true omissions, never to bend meaning.]"

**Evidence class:** [observed behavior / artifact / named commitment / interview claim / team belief]

<!-- Strongest first: observed behavior (something a user did, recorded, dated),
     artifact (a document or export a reader could open), named commitment (a
     person with standing said yes in writing), interview claim (a real person
     said it, cited by source and date), team belief (goes to the assumptions
     register, never into a template as fact). -->

## Weight

- **Confidence:** [verified / single-source / contested / unverified]
- **Agrees with:** [note IDs, or "none found"]
- **Disagrees with:** [note IDs plus one line on the conflict, or "none found"]
- **What this note cannot support:** [the nearby, bigger claim someone will be tempted to hang on it; name it so they do not]

<!-- Confidence definitions: verified means two or more independent sources
     agree (name them in Agrees with); single-source means this note stands
     alone; contested means a listed note disagrees and the tension is carried,
     not resolved; unverified means belief, and the claim goes to
     ../definition/assumptions-register.md instead of into any template. -->

## Ledger row

Copy this row, filled, into the evidence ledger in the product's STATE.md:

| E# | Claim | Verbatim quote | Source | Source date | Retrieved | Confidence |
|---|---|---|---|---|---|---|
| E[n] | [claim, short] | "[quote]" | [locator] | [YYYY-MM-DD] | [YYYY-MM-DD] | [confidence] |

## How an evidence note fails

<!-- This is the smallest artifact in the tree and the one everything else
     rests on. A gate decision traces back through synthesis, through a
     persona, to a note like this one, so a defect here is invisible and load
     bearing at the same time. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Paraphrase presented as a quote | Quotation marks around a tidied version of what was said | Quotation marks are reserved for verbatim text. Paraphrase goes outside them, always |
| No source or no date | "Research shows", with nothing attached | Author or speaker, document or session, and the date. A note without them cannot be checked |
| Only what we already believed | Sources selected because they agreed, and the disagreement went unrecorded | Record what contradicts the position too. Finding no counter-evidence is itself a finding |
| Context stripped | A sentence lifted from a paragraph that qualifies or reverses it | Carry enough surrounding text that the meaning survives the extraction |
| Confidence asserted | "A reliable source", with nothing behind the adjective | Use the classes in Weight above: verified, single-source, contested, unverified |

### Worked micro-example (ILLUSTRATIVE, invented)

<!-- Shows the one thing this template exists to protect: the boundary between
     what was said and what we concluded. Delete once real notes exist. -->

| E# | Claim | Verbatim quote | Source | Source date | Retrieved | Confidence |
|---|---|---|---|---|---|---|
| *E7* | *Rural postcodes are rejected by validation, and reps abandon rather than retry* | *"I put the postcode in three times, then I just gave up and did it at home"* | *Interview, field rep, session 4* | *2026-03-11* | *2026-03-12* | *single-source* |

*Note what is outside the quotation marks. The rep did not say validation was the cause, and did not say others do the same. Both are our inference, and both are why the confidence is single-source rather than verified.*

## Exit gate

<!-- Checkable by someone who was not in the session. -->

- [ ] The quote is verbatim, and everything outside the quotation marks is marked as inference
- [ ] Source, source date and retrieval date are all present and locatable by someone else
- [ ] The confidence class is one of the four in Weight, and the reason for it is stated
- [ ] Contradicting evidence was looked for, and either recorded or explicitly reported as absent
- [ ] The ledger row is filled and ready to copy into the product's STATE.md
- [ ] The worked example above has been removed
