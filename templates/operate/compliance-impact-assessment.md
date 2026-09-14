---
layer: templates
stage: DEFINE
gate: 2
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Compliance Impact Assessment", "compliance-impact-assessment"]
---
# Compliance Impact Assessment: [product or feature name]

**Stage:** [DEFINE and DELIVER](../../os/STAGE-GATES.md) (feeds Gate 2 and Gate 5, regulated overlay)
**Knowledge:** [reg-gap-check](../../skills/reg-gap-check/SKILL.md)
**Skill:** [reg-gap-check](../../skills/reg-gap-check/SKILL.md)

<!-- This template asks the questions; it never supplies the answers. It is not legal
     advice, and a completed copy is not a compliance certification. Answers belong to
     your legal counsel, privacy officer, or second line, and their names go in the
     sign-off table.

     Products that contain an AI or machine-learning feature and have a financial
     regulator applying to them activate the regulated module: run the
     reg-gap-check skill linked above, which routes into the verbatim regulated
     material rather than paraphrasing regulator text. Both halves are required
     by ../../os/STAGE-GATES.md; a regulated product with no model still runs
     reg-gap-check for gap mapping, and its regulatory owner names what covers it. Never reword regulator text
     in this document; cite the instrument and section, and name who holds the copy. -->

**Owner:** [name] · **Legal or compliance counterpart:** [name]
**Status:** Draft / In review / Signed · **Date:** [YYYY-MM-DD]

## 1. Product and data summary

<!-- Say what the feature does and who the user, decider, and buyer are in two
     sentences; name every market and jurisdiction because later sections answer
     per market where rules differ. A trap: listing only the launch country and
     forgetting that data hosting or a payment rail drags in another
     jurisdiction. Do not write a marketing description of the feature. -->

- What the feature does and who uses it: [two sentences]
- Markets and jurisdictions in scope: [list; sections below are answered per market where they differ]
- Does the product contain an AI model making or influencing decisions about people? [yes / no; if yes, also complete the AI overlay in ../ai/, starting with human-approval-gates.md]

## 2. Applicable regulations and regimes

<!-- "Applies because" cites a scoping fact about your product, not a vibe.
     Evidence names a document, a clause, or written advice, and who holds it.
     A trap: copying a regulation name into the first column with "applies to
     our industry" as the reason, which a reviewer cannot distinguish from a
     guess. This fails when "evidence" names a webpage with no version or
     holder, or when a row is left without an owner. Do not write "we believe
     it is in scope"; either cite the scoping fact or mark it as a gap. -->

| Regulation or regime | Applies because | Obligations triggered | Evidence and holder | Owner |
|---|---|---|---|---|
| | | | | |

## 3. Data categories

<!-- Each row is one category of data the feature actually processes, not a
     system table list; special-category data needs a condition column filled by
     counsel or the DPO, not by the PM. This fails when you list "user data" as a
     single row and miss that date of birth for under-13s is special category in
     its own right. Do not leave the lawful-basis cell blank; a blank is a gap
     that blocks sign-off. -->

| Data category | Personal data? | Special or sensitive category? | Additional condition for special-category or criminal-offence data (entered by counsel or DPO) | Stored where | Retention period | Lawful basis or ground |
|---|---|---|---|---|---|---|
| | yes / no | yes / no | [condition, or N/A if not special] | | | |

## 4. DPIA flag

<!-- A data protection impact assessment is its own exercise; this section only
     decides whether one is required and who runs it. Answer each question
     honestly, because a false "no" here moves the risk into the DPIA you never
     run. This fails when the PM treats "significant effects" as obvious harm
     and misses that profiling which steers access to services can qualify. Do
     not leave a question blank; a blank is read as "no" in an audit. -->

Answer each honestly:

- Systematic profiling or automated decisions with significant effects? [yes / no]
- Large-scale processing of special category data? [yes / no]
- Systematic monitoring of a publicly accessible area? [yes / no]
- New technology applied to personal data in a novel way? [yes / no]

**DPIA required:** [yes / no] · If yes: run by [name], due [YYYY-MM-DD], filed at [location]

## 5. Cross-border transfers

<!-- A transfer is any time personal data leaves a jurisdiction, including remote
     support access from another country, not just a storage move; name the
     mechanism (adequacy decision, standard contractual clauses, binding corporate
     rules) and where the signed copy lives. A trap: assuming a vendor listed as
     "EU hosting" has no transfer when its support engineers sit in another
     region. Never write "N/A" without confirming where every processor's
     personnel can access the data from. -->

| Transfer (from, to) | Data involved | Mechanism relied on | Evidence |
|---|---|---|---|
| | | | |

## 6. Third parties and processors

<!-- Name every external party that touches the data, including sub-processors
     your processor engages without telling you, and cite the clause that binds
     them to this use, not just the contract name. This fails when the clause
     covers "services" generally but not the specific processing you are doing,
     or when a sub-processor change has not been flowed down. Do not list a party
     whose role you have not confirmed in writing. -->

| Party | Role (processor / sub-processor / controller) | Contract clause covering this use | Audit or information rights |
|---|---|---|---|
| | | | |

## 7. Retention and deletion

<!-- Retention belongs per category in section 3; here you confirm that schedule
     is complete and describe deletion as a mechanism that runs, not a policy
     that exists. A trap: writing "deleted on request" when the actual path is a
     ticket queued against a backlog, or when backups silently restore the
     record days later. Never assert a retention period of zero; backups and logs
     always survive for some window, so name it. -->

- Retention schedule per category is complete in section 3: [confirm]
- Deletion is implemented, not just promised: how a deletion request actually executes: [mechanism, owner]
- What survives deletion (backups, logs, aggregates) and for how long: [list]

## 8. Gaps

<!-- A gap is anything that blocks sign-off or safe shipment: missing evidence,
     an unsigned clause, an open DPIA action, a deletion path that does not
     execute yet. This fails when the PM softens a gap into "still deciding"
     or "to confirm", which hides a deferred decision from the sign-off
     table; write the concrete risk if the feature ships as is. Never close a
     gap by rewording it away; it closes when evidence lands or a control is
     built. -->

| # | Gap | Risk if shipped as is | Owner | Date |
|---|---|---|---|---|
| | | | | |

## 9. Sign-off

<!-- Legal counsel or DPO and second-line compliance must sign before the product
     owner accepts; a verdict is one of Pass, Conditional Pass, or Fail, with
     conditions stated as closeable actions, not as preferences. A trap: a
     forwarded email or a chat message standing in for a signed verdict, which
     leaves no auditable record. Do not sign on behalf of a role that has not
     reviewed the file. -->

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
