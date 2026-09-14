---
layer: templates
stage: PLANNING
gate: 1
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Partner Integration Brief", "partner-integration-brief"]
---
# Partner Integration Brief: [partner name]

**Stage:** PLANNING track (a one-pager weight decision; the go or no-go lands in [decision-log.md](../execution/decision-log.md))
**Knowledge:** [build, buy or partner](../../frameworks/strategy/build-buy-partner.md)
**Skill:** [drafting agent](../../agents/drafting-agent.md)

<!-- One lean file for one question: should we build on this partner, yes or no?
     It is not a BD suite, a contract, or an integration spec; when the answer is
     yes, the technical work gets its own api-contract.md and integrations.md rows
     under the architecture templates, and the commercial terms get lawyers.

     The trap this file exists to block: partnerships that are announced before they
     are reasoned about. A logo swap and a press release are outputs a partnership
     can produce without solving any user problem. Section 2 forces the user problem
     to come first; if it cannot be filled with evidence, the recommendation in
     section 6 writes itself. -->

**Brief owner:** [name] · **Partner contact:** [name, role] · **Date:** [YYYY-MM-DD]
**Decision needed by:** [YYYY-MM-DD, and what forces that date]

## 1. The exchange

<!-- State both sides of the trade in concrete nouns, not aspirations. A good
     entry names the capability, data set or distribution the partner supplies
     and the volume, integration or operating context we supply. Do not write
     "synergy" or "strategic alignment"; write what changes hands. -->

- What the partner provides: [capability, data, distribution, coverage, in concrete terms]
- What we provide: [same discipline]
- Why they want this, in their words if you have them: [their motive; a partner whose motive you cannot state is a partner you have not understood]

## 2. The user problem this solves

<!-- Evidence, not strategy prose. If the problem is real it already shows up in
     tickets, interviews, or lost deals, filed as evidence notes. A trap: writing
     "this partnership will improve UX" with no filed evidence. This fails when
     the problem is asserted from the partner's pitch rather than from our own
     support tickets or discovery notes. Never list a benefit that does not map
     to a filled evidence note or a ticket count. -->

- Problem statement: [who is blocked, on what, today]
- Evidence: [links to filled ../discovery/evidence-note.md entries, ticket counts, win-loss rows]
- What users do today without this partnership: [the workaround, and what it costs them]
- Why partnering beats building or buying: [one honest paragraph]

## 3. Integration surface and owners

<!-- Team Topologies, by Matthew Skelton and Manuel Pais, argues that a team should
     publish what it offers and how to interact with it the way a service publishes
     an API. That framing is restated here for a partner boundary: name the surface,
     the owner on each side, and the response expectation, so the first outage is
     not also the first conversation about who answers. A trap: writing "our team"
     or "their team" instead of a named person and role. This fails when the first
     outage is also the first time the two owners meet. Do not leave a support
     expectation cell blank; state "not specified in the filed evidence" if so. -->

| Surface (API, data feed, embed, SSO) | What crosses it | Our owner | Their owner | Support expectation (response time, channel) |
|---|---|---|---|---|
| | | | | |

## 4. Commercial shape and exit terms

<!-- State the commercial model and the exit terms you would need if the deal ends.
     A good entry names the revenue shape, the term length and notice period, and
     what happens to users, data and in-flight transactions on exit. A trap:
     leaving exit terms blank because the partnership feels positive. This fails
     when the deal renews and there is no written exit path. Never write exit
     terms after signing; the partnership you cannot leave is the one that
     renegotiates you. -->

- Commercial shape: [revenue share / referral / paid license / mutual, with the numbers proposed, each labeled ILLUSTRATIVE until agreed]
- Term and renewal: [length, notice period]
- Exit terms, written before signing: [what happens to users, data, and in-flight transactions if either side walks; the partnership you cannot leave is the one that renegotiates you]

## 5. Risks

<!-- Dependency and data-sharing risks are mandatory rows; a partnership is a
     dependency you chose. Material rows are copied into ../execution/risk-register.md
     with owners. A trap: treating the partner as more reliable than a service we
     would build, because we chose them. This fails when the partner deprioritizes
     the surface we depend on and there is no row for it. Do not copy only the
     positive rows; the dependency and data-sharing rows are the mandatory minimum. -->

| Risk | Likelihood | Impact if it lands | Mitigation or accepted |
|---|---|---|---|
| [partner deprioritizes or sunsets the surface we depend on] | | | |
| [user or usage data crosses the boundary; regulator or contract exposure] | | | |
| [partner becomes a competitor or is acquired by one] | | | |
| [add rows] | | | |

## 6. Recommendation

<!-- One of go, no-go, or go with named conditions, in three sentences the decision
     log can hold. A good entry states the recommendation, the strongest reason for
     it, and the condition or evidence that would reverse it. A trap: writing "go"
     with no condition and no review date. This fails when the evidence later
     weakens and nobody can find the reversal trigger. Do not recommend before
     sections 2 and 3 are filled; a blank evidence row makes the recommendation
     unreadable. -->

[Go / no-go / go with named conditions, in three sentences: the recommendation, the strongest reason for it, the condition or evidence that would reverse it. Log the decision in [decision-log.md](../execution/decision-log.md) with a review date.]

## Exit gate

- [ ] Both sides of the exchange are stated in concrete terms, including the partner's motive
- [ ] The user problem cites filed evidence, not strategy language
- [ ] Every integration surface has a named owner on each side
- [ ] Exit terms are written down before anything is signed
- [ ] Dependency and data-sharing risks have rows, and material ones are in the risk register
- [ ] The recommendation is one of go, no-go, or conditional go, and is logged in the decision log
