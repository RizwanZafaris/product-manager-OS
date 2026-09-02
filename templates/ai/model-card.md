# Model Card: [feature or model name]

Stage: AI overlay, active whenever the product contains a model; feeds Gate 5 (release readiness)
Knowledge: ../../knowledge/INDEX.md
Skill: ../../skills/ai-prd/SKILL.md

<!-- The eval spec answers "is it good enough to ship?" for the team. This card
     answers "what is this, what is it for, and where does it break?" for everyone
     else: support, sales, legal, integrating teams, and in some markets an auditor.
     The format restates, in this repository's own words, the reporting practice
     Mitchell and coauthors proposed in "Model Cards for Model Reporting": pair every
     capability claim with its intended use, its known limits, and how performance
     varies across the people it serves.

     Write it at Gate 5 and update it on every model or prompt version change; a
     card describing last quarter's model is worse than no card, because it is
     believed. For products under a financial or data regulator, the disclosure
     requirements in ../../modules/regulated/README.md win on overlap, same rule as
     the eval spec. -->

**Model and version pinned:** [provider, model, exact version string, same string as eval-spec.md]
**Card owner:** [name] · **Contact for questions:** [name or channel] · **Last updated:** [YYYY-MM-DD]

## 1. Intended use

- What the model does in this product, one sentence per capability: [list]
- Who it serves: [user types]
- Explicitly out of scope: [uses the model will be asked for and must not be trusted with, e.g. legal or medical judgment, decisions about individual people without review]

<!-- The out-of-scope list is the load-bearing part. Every support ticket that starts
     "I used it to X and it was wrong" where X is on this list is a closed ticket;
     where X is missing from this list, it is your incident. -->

## 2. Known limitations and failure modes

<!-- Nothing new is discovered here; this section cites what the team already proved.
     Each row names its source document by path, so a reader can check the evidence
     rather than trust the summary. -->

| Limitation or failure mode | How it shows up for the user | Source (path + section) |
|---|---|---|
| [e.g. degrades on inputs over n pages] | [truncated or generic answers] | [eval-spec.md section 1, scenario #] |
| [e.g. can be steered by instructions inside pasted content] | [wrong or unsafe output] | [red-team-review.md finding #] |
| [add rows for every known limit] | | |

## 3. Performance summary

<!-- Copy from the filled eval-spec.md; compute nothing fresh here. Report variance
     across segments, not just the headline: an average that hides a weak segment is
     how a model that "works" fails a specific group of users. Every number is
     labeled ILLUSTRATIVE or cites the eval run that produced it, with a date. -->

- Headline result: [metric, value, label or citation]
- Variance across segments (language, region, input type, user group): [where it is weakest, with numbers]
- Segments not measured yet, stated plainly: [list, or "none"]

## 4. Data provenance

One or two sentences: what data the model was trained or fine-tuned on to the extent the provider discloses it, what product data reaches the model at inference time, and what is retained where. Link the vendor terms rather than paraphrasing them: [provenance statement, link]

## 5. Update policy

- What triggers a card update: [model or prompt version change, new eval results, new red-team findings]
- Who updates it: [name] · Review cadence even without changes: [cadence]
- Where old versions live: [location, so past claims stay checkable]

## Exit gate

- [ ] Every capability claim in section 1 has a matching row in the eval spec
- [ ] The out-of-scope list exists and names at least the uses the team already declined
- [ ] Every limitation row cites a source document by path
- [ ] Performance is reported with segment variance, or unmeasured segments are named
- [ ] The pinned version string matches eval-spec.md exactly
- [ ] A contact is named that outsiders can actually reach
