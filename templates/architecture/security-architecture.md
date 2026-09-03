---
layer: templates
stage: DESIGN
gate: 3
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Security Architecture Checklist", "security-architecture"]
---
# Security Architecture Checklist: `<system name>`

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md)
Knowledge: [knowledge index](../../knowledge/INDEX.md)
Skill: [red-team-agent](../../agents/red-team-agent.md)

<!-- Threat modeling by STRIDE, the classification introduced at Microsoft by Loren
     Kohnfelder and Praerit Garg: Spoofing, Tampering, Repudiation, Information
     disclosure, Denial of service, Elevation of privilege. This checklist is encoded
     in this repo's own words; read a full treatment before running your first
     session. The walk is done per component against the system design document, in
     one sitting, with an engineer and someone adversarial in the room. If the
     product contains a model, run the AI red-team review as well; this checklist
     covers the system, not prompt-level attacks. -->

**System:** `<name>` · **Session date:** `<YYYY-MM-DD>` · **Participants:** `<names>`
**Design reviewed:** `<link to the filled system-design.md>` · **Status:** Draft / Reviewed / Signed off

## 1. Trust boundaries

<!-- A trust boundary is any line where the level of trust changes: internet to
     gateway, service to database, our platform to a vendor, user content into a
     model prompt. List each; the STRIDE walk in section 2 runs per boundary. -->

| # | Boundary | What crosses it | Trust change |
|---|---|---|---|
| 1 | | | |

## 2. STRIDE walk

<!-- One table per component from the system design document. For each threat class,
     either name the threat and mitigation, or write "not applicable because
     <reason>". A blank cell means the walk was not done, not that the threat is
     absent. Risk score: likelihood (1 to 3) times impact (1 to 3), so 1 to 9;
     anything 6 or above must also appear in the risk register. -->

### Component: `<name>`

| Threat class | Concrete threat here (or "not applicable because ...") | Risk score (L x I) | Mitigation | Mitigation owner | Verified by (test, review, or control) |
|---|---|---|---|---|---|
| Spoofing | | | | | |
| Tampering | | | | | |
| Repudiation | | | | | |
| Information disclosure | | | | | |
| Denial of service | | | | | |
| Elevation of privilege | | | | | |

## 3. Standing checks

<!-- Answer each with a value or an owner, never a bare yes. -->

- Secrets management: `<where secrets live, how they rotate, who can read them>`
- Least privilege: `<how service and human access is scoped and reviewed, and cadence>`
- Encryption in transit and at rest: `<protocols and key management>`
- Audit logging: `<which security-relevant events are logged, and where alerts route>`
- Dependency and image scanning: `<tool, gate it blocks, owner>`
- Data classified per the data model: `<link to the filled data-model.md section 5>`

## 4. Findings routed onward

| Finding | Risk score | Routed to (risk register row / backlog item) | Owner | Date |
|---|---|---|---|---|
| | | | | |

## Exit gate

- [ ] Every component in the system design document has a completed STRIDE table
- [ ] No blank cells: every threat class has a threat or a reasoned "not applicable"
- [ ] Every mitigation has a named owner and a verification method that can fail
- [ ] Every score of 6 or higher is a row in the risk register
- [ ] Standing checks in section 3 all carry values and owners
- [ ] Someone adversarial attended the session and is named above
