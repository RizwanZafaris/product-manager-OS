# Context Management: [feature name]

Stage: AI overlay, active whenever the product contains a model; feeds Gate 3 (architecture and risks reviewed)
Knowledge: ../../knowledge/INDEX.md
Skill: ../../skills/ai-prd/SKILL.md

<!-- Everything the model sees at inference time is a decision someone made, or a
     decision nobody made, which is worse. This document is the inventory of what goes
     into the window, in what order, what gets dropped first when space runs out, and
     what must be filtered before it ever arrives. -->

**Feature:** [one sentence]
**Context owner:** [name] · **Document date:** [YYYY-MM-DD]
**Model context window:** [n tokens] · **Working budget (leave headroom for output):** [n tokens]

## 1. Context sources

| Source | What it contributes | Freshness (live / cached, max age) | PII class (none / personal / sensitive) | Filter applied before inclusion |
|---|---|---|---|---|
| [e.g. system prompt] | [role, rails, output contract] | [versioned, see prompt-structure.md] | none | [n/a] |
| [e.g. retrieval index] | [top k passages] | [re-indexed weekly] | [personal] | [PII scrub, see section 4] |
| [e.g. conversation history] | [last n turns] | [live] | [personal] | [truncation + scrub] |
| [add] | | | | |

## 2. Token budget and priority order

<!-- When the window is tight, something gets dropped. Decide the order here, not in
     whatever the framework does by default. Priority 1 is never dropped. -->

| Slot | Budget (tokens) | Priority (1 = never dropped) | Drop behavior when over budget |
|---|---|---|---|
| System prompt | [n] | 1 | never dropped; if it alone exceeds budget, that is a build failure |
| [e.g. current user request] | [n] | 1 | never dropped |
| [e.g. retrieved passages] | [n] | 2 | [drop lowest-ranked first] |
| [e.g. history] | [n] | 3 | [oldest turns summarized, then dropped] |
| [add] | | | |

## 3. Staleness policy

- Max acceptable age per cached source: [source: age, per row in section 1]
- What happens when a source exceeds its age: [refresh synchronously / serve with a staleness notice / abstain]
- Who is alerted when a refresh pipeline fails: [name or rota]

## 4. PII filter

- What is stripped or masked before the model sees it: [classes: names, account identifiers, card data, addresses, add per your data classification]
- Where the filter runs (before the context is assembled, not after): [component]
- Test: [eval cases proving the filter catches each class; test IDs]
- What is logged about context contents, and how the log avoids re-collecting the PII the filter removed: [answer]
- For regulated products, residency and vendor-terms questions about this data belong to the overlay in ../../modules/regulated/README.md

## Worked micro-example

A support assistant with a 128k window ILLUSTRATIVE reserves 4k for the system prompt, 2k for the live request, 12k for retrieval, 8k for history, and holds the rest as output headroom. Under pressure, history summarizes before retrieval drops, because a wrong answer from missing policy text is worse than a curt one from missing chit-chat. That sentence, written down, is the whole value of this document.

## Exit gate

- [ ] Every context source has a row with freshness, PII class, and filter stated
- [ ] The budget table covers everything in section 1 and fits the working budget
- [ ] Drop order is explicit; nothing relies on framework defaults
- [ ] The PII filter has tests per class and runs before assembly
- [ ] Staleness has a behavior and an alerted owner, not just a number
