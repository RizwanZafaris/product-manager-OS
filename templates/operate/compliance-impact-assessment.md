# Compliance Impact Assessment: [product or feature name]

**Stage:** DEFINE and DELIVER (feeds [Gate 2 and Gate 5](../../os/STAGE-GATES.md), regulated overlay)
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [reg-gap-check](../../skills/reg-gap-check/SKILL.md)

<!-- This template asks the questions; it never supplies the answers. It is not legal
     advice, and a completed copy is not a compliance certification. Answers belong to
     your legal counsel, privacy officer, or second line, and their names go in the
     sign-off table.

     Products under a financial regulator activate the regulated module: run the
     reg-gap-check skill linked above, which routes into the verbatim regulated
     material rather than paraphrasing regulator text. Never reword regulator text
     in this document; cite the instrument and section, and name who holds the copy. -->

**Owner:** [name] · **Legal or compliance counterpart:** [name]
**Status:** Draft / In review / Signed · **Date:** [YYYY-MM-DD]

## 1. Product and data summary

- What the feature does and who uses it: [two sentences]
- Markets and jurisdictions in scope: [list; sections below are answered per market where they differ]
- Does the product contain an AI model making or influencing decisions about people? [yes / no; if yes, also complete the AI overlay in ../ai/, starting with human-approval-gates.md]

## 2. Applicable regulations and regimes

<!-- "Applies because" cites a scoping fact about your product, not a vibe.
     Evidence names a document, a clause, or written advice, and who holds it. -->

| Regulation or regime | Applies because | Obligations triggered | Evidence and holder | Owner |
|---|---|---|---|---|
| | | | | |

## 3. Data categories

| Data category | Personal data? | Special or sensitive category? | Stored where | Retention period | Lawful basis or ground |
|---|---|---|---|---|---|
| | yes / no | yes / no | | | |

## 4. DPIA flag

<!-- A data protection impact assessment is its own exercise; this section only
     decides whether one is required and who runs it. -->

Answer each honestly:

- Systematic profiling or automated decisions with significant effects? [yes / no]
- Large-scale processing of special category data? [yes / no]
- Systematic monitoring of a publicly accessible area? [yes / no]
- New technology applied to personal data in a novel way? [yes / no]

**DPIA required:** [yes / no] · If yes: run by [name], due [YYYY-MM-DD], filed at [location]

## 5. Cross-border transfers

| Transfer (from, to) | Data involved | Mechanism relied on | Evidence |
|---|---|---|---|
| | | | |

## 6. Third parties and processors

| Party | Role (processor / sub-processor / controller) | Contract clause covering this use | Audit or information rights |
|---|---|---|---|
| | | | |

## 7. Retention and deletion

- Retention schedule per category is complete in section 3: [confirm]
- Deletion is implemented, not just promised: how a deletion request actually executes: [mechanism, owner]
- What survives deletion (backups, logs, aggregates) and for how long: [list]

## 8. Gaps

| # | Gap | Risk if shipped as is | Owner | Date |
|---|---|---|---|---|
| | | | | |

## 9. Sign-off

| Name | Role | Verdict | Conditions | Date |
|---|---|---|---|---|
| | Legal counsel or DPO | | | |
| | Second line / compliance (regulated products) | | | |
| | Product owner | | | |

## Exit gate

This document passes when:

- [ ] Every regulation row cites evidence and names its holder, no "we believe it is fine" rows
- [ ] Every data category has a stated retention period and lawful ground
- [ ] The DPIA decision is recorded either way, with a named runner if yes
- [ ] Deletion is described as a mechanism that executes, not a policy that exists
- [ ] For financially regulated products, the reg-gap-check skill was run and its output is attached
- [ ] Legal sign-off is a name and a date, not a forwarded email

Signed: [name], [role], [YYYY-MM-DD]
