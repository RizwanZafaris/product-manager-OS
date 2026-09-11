# Risk Register: Saltmarsh Prepaid programme operations

Fills [templates/execution/risk-register.md](../templates/execution/risk-register.md). Everything here is invented: Saltmarsh Prepaid is a fictional consumer prepaid card programme, its sponsor bank, vendors and people are fictional, and every number, date and regulatory statement is ILLUSTRATIVE and labelled as such, not drawn from any real company, BIN or filing; see the [examples index](README.md). Regulatory statements here are written "as of 2026-09-11", confirm with counsel, and are not legal advice.

**Owner:** Priya Nadkarni, Programme Manager, Saltmarsh Prepaid · **Date:** 2026-09-11 · **Register owner:** Priya Nadkarni · **Review cadence:** weekly, every Tuesday 10:00 ET programme operations stand-up
**Last reviewed:** 2026-09-08 · **Premortem run:** 2026-09-02

Standalone fictional context, all ILLUSTRATIVE: Saltmarsh Prepaid issues the "Saltmarsh Card," a consumer prepaid card on a BIN sponsored by a fictional sponsor bank, Cascade Trust Bank, N.A. Priya Nadkarni manages the programme; Marcus Feld is Cascade's compliance officer and holds final sign-off on any programme change; Lena Wu is Saltmarsh's Head of Disputes; and Tom Okafor owns platform engineering at the programme. The four-party issuing constraints that shape every row below are in the [card-issuing domain card](../knowledge/domains/card-issuing.md): the sponsor, the networks, the wallet providers and the sponsor's banking supervisor each gate the programme, and disputes and tokenisation are where the real operating cost hides.

## 1. Scoring

Likelihood and impact each score 1 to 3 (low, medium, high). Score = L x I, range 1 to 9; a medium-likelihood risk hitting a high-impact event scores 2 x 3 = 6, and a high-likelihood risk on a low-impact event scores 3 x 1 = 3. At 6 or above a row needs an active mitigation with a dated trigger, not a watching brief. The scale is coarse on purpose: the issuing facts that decide these rows are regulatory clocks and network rules, not probability forecasts, so precision past three points invents confidence the data does not have. Two rows in section 2, R4 and R5, hit the 6-or-above threshold, so both carry dated mitigation triggers.

## 2. The register

Response is mitigate, accept, transfer, or avoid; "monitor" is not a response, it is accept without a signature, so any row needing a watching brief appears as accept, signed in section 3. The row R9 below is the card's dispute-timeline row, carried unchanged from the [card-issuing domain card](../knowledge/domains/card-issuing.md): under Regulation E the error-resolution clock expects provisional credit within 10 business days, and the CFPB Prepaid Rule ties provisional credit to accounts with completed identification, so the deadline is only a clean deadline once CIP is done (verify with counsel; as of 2026-09-11, not legal advice). Owners are split between Priya Nadkarni, who owns Saltmarsh's product and operational run, and Marcus Feld, who owns anything that touches the sponsor's own licence risk. No risk is accepted without Marcus Feld's sign-off, because on a sponsor-sponsored BIN the sponsor bank carries the ultimate regulatory responsibility even where Saltmarsh built the product.

| # | Risk (event, not a vague noun) | Category (value / usability / feasibility / viability / delivery / security) | L | I | Score | Response | Mitigation and its trigger | Owner | Review date |
|---|---|---|---|---|---|---|---|---|---|
| R1 | The card network issues a rule bulletin on a tokenisation change with a fixed compliance date (2027-03-31) that the programme's current provisioning cannot meet without a wallet re-integration | delivery | 2 | 3 | 6 | mitigate | Network rule bulletins are tracked with their effective dates in a standing watch item; a dated change plan with a named engineer is open 180 days before the compliance date (by 2026-10-02 for a 2027-03-31 date), and if no plan is open at that checkpoint the row escalates to Marcus Feld | Tom Okafor (engineering) with Marcus Feld (sponsor sign-off) | 2026-09-22 |
| R2 | A card-processor outage at Cascade's processing partner exceeds the contracted window (4 hours) during a peak cash-out period, so authorisations, ATM and app balance reads all fail at once | delivery | 2 | 2 | 4 | mitigate | The sponsor bank carries the processor outage in its own vendor-continuity register; the trigger that moves this above a watching brief is any single outage over 4 hours or any second outage inside a 30-day window, at which point the row escalates to Marcus Feld and the sponsor SLA clause is re-read against the contracted uptime | Priya Nadkarni (Saltmarsh run) with Marcus Feld (sponsor SLA) | 2026-09-22 |
| R3 | A token provisioning failure spike, a wallet provisioning success rate falling below the 95 percent threshold (from the illustrative baseline of about 98 percent), leaves cardholders' wallet payments silently broken after a physical card reissue | security | 2 | 3 | 6 | mitigate | Provisioning success is monitored against the 95 percent floor; the trigger is a sustained fall below it, at which point re-provisioning after reissue is forced before authorisation resumes, since a token and the reissued physical number diverging is the failure the [domain card](../knowledge/domains/card-issuing.md) names; root-cause with the wallet provider's provisioning contact inside 5 business days of the trigger firing | Tom Okafor (engineering) | 2026-09-22 |
| R4 | A sponsor-bank supervisory action by Cascade's own banking supervisor freezes all Saltmarsh programme changes (new features, BIN changes, limit increases) pending remediation | viability | 2 | 3 | 6 | mitigate | Severity, not the count of open findings, is watched weekly, since the domain card names a single severe finding as the trigger for suspension rather than a pile of small ones; the trigger is any open finding rated severe, which freezes the launch calendar and opens a dated remediation plan jointly signed by Priya Nadkarni and Marcus Feld before any feature ships | Marcus Feld (sponsor compliance) | 2026-09-22 |
| R5 | A Saltmarsh programme feature, say a transaction-velocity relaxation or a limit increase, ships or goes live before the sponsor's programme-risk and underwriting function has signed it off | viability | 2 | 3 | 6 | mitigate | Any velocity, limit or exposure change carries a dated sponsor sign-off as its own release-readiness line; the trigger is any such change lacking a dated Marcus Feld sign-off, which blocks the release (release-readiness carries this as its own line per the [domain card](../knowledge/domains/card-issuing.md)); the feature does not move to the release branch without it | Priya Nadkarni (with Marcus Feld as final approver) | 2026-09-22 |
| R9 | A cardholder's Regulation E dispute misses the 10-business-day provisional-credit deadline because the case queue backs up during a fraud spike | compliance | 2 | 3 | 6 | mitigate | Auto-escalate any open case to a second reviewer at business day 8; the sponsor bank's own dispute-SLA dashboard alerts at day 9; trigger is any case crossing day 8 with no provisional credit posted | Head of Disputes (Lena Wu, ILLUSTRATIVE) | 2026-09-22 |

The score column is the arithmetic L x I: R1 2 x 3 = 6, R2 2 x 2 = 4, R3 2 x 3 = 6, R4 2 x 3 = 6, R5 2 x 3 = 6, R9 2 x 3 = 6.

## 3. Accepted risks

Acceptance here is only ever Marcus Feld's to sign, since on Cascade's BIN the sponsor's risk appetite outranks Saltmarsh's backlog; a risk nobody in the sponsor's chair has signed is drift, not acceptance. The two rows below carry that signature and its revisit date.

| Register # | Accepted by (name, role) | Date | Rationale in one sentence | Revisit when |
|---|---|---|---|---|
| R2 | Marcus Feld, Cascade Trust Bank compliance officer | 2026-09-09 | We carry a single moderate processor outage inside the contracted window as sponsor risk, because the sponsor already holds the uptime SLA and duplicating a second failover at the programme layer is not funded this quarter. | Any single outage above 4 hours, a second outage inside 30 days, or the next sponsor SLA renewal |

## 4. Closed risks

Closed rows stay in this table rather than being deleted, because the same risk closing repeatedly is the pattern that shows it was survived, not addressed. Two illustrative rows are recorded here.

| Register # | Closed on | How it resolved (did not occur / occurred, impact was ... / mitigated away) |
|---|---|---|
| R0 (earlier run) | 2026-07-31 | Did not occur; the pre-launch token-verification step caught a mis-provisioning defect before wallets went live |
| R0b (earlier run) | 2026-08-25 | Occurred, impact was a 90-minute authorisation latency spike on one BIN range; mitigated by a queued retry with no customer-facing failures and no provisional-credit impact |

## 5. How this register fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| No owner | A row with a score and a date and no human attached | Every row has one named owner. Orphans go to the top of the review, not the bottom |
| Scored once, never revisited | Probability and impact unchanged for quarters while the world moved | Re-score at every review, and flag any row not touched in a month |
| Mitigation restates the risk | "Risk: outage. Mitigation: prevent the outage." | A mitigation names an action, an owner and a date, or it is not one |
| Everything is medium | A long list of identical amber rows and no triage | Force a spread. If most rows are medium, nobody has ranked them |
| Closed risks deleted | The history disappears, and the same risk returns next quarter unrecognised | Closed rows are archived, not removed, and reviewed for repeats |
| The register replaces escalation | A serious risk is logged, never raised, and leadership is surprised | Above an agreed threshold, logging is not enough: the row names who was told and when |

## Exit gate

- [x] Every risk is written as an event that could happen, not a topic heading. R1 is a rule bulletin with a fixed date, R4 is a supervisory action that freezes changes, R5 is a feature shipping without sponsor sign-off; none is a noun
- [x] Every open risk has a score, an owner, and a review date in the future. R1 to R5 and R9 each carry L, I, score, a named owner and a 2026-09-22 review date, future to the 2026-09-11 last review
- [x] Every score of 6 or higher has an active mitigation with a trigger, not "monitor". R1, R3, R4, R5 and R9 all score 6 and each names its trigger and its date, not a watching brief
- [x] Every accepted risk is signed by name in section 3. Only R2 is accepted, signed by Marcus Feld on 2026-09-09 (date as recorded in section 3), with a revisit condition
- [x] Findings from the security architecture checklist and dependency register appear here. The wallet-provider dependency (R3) and the sponsor-processor dependency (R2) are named, consistent with the programme integrations and the [domain card](../knowledge/domains/card-issuing.md)'s gatekeeper list
- [x] A premortem has been run before Gate 3, and its findings are rows above. The 2026-09-02 premortem produced R1 to R5 (R9 carried from the domain card's worked example)
- [x] The example row has been deleted. The template's counterparty-sandbox row does not appear; R1 is the network-bulletin row that replaces it

Exit-gate walk, 2026-09-11: I checked this register against its own exit gate. Section 1 carries the 1-to-3 scoring and the threshold of 6 as the decision rule. Section 2's R9 is the dispute-timeline row carried unchanged from the [card-issuing domain card](../knowledge/domains/card-issuing.md), and I confirmed it names the 10-business-day provisional-credit clock and flags the Prepaid Rule's completed-identification condition as one to verify with counsel. Every score column matches L x I by hand: the only row scoring below the threshold is R2 at 2 x 2 = 4, and the rest land on 6 or above, so all of them carry dated triggers rather than watching briefs. Owners are genuinely split between Priya Nadkarni and Marcus Feld, and the only accepted risk, R2, is signed by the sponsor's compliance officer, because on Cascade's BIN no risk is Saltmarsh's alone to accept. The template's example sandbox row is gone, replaced by the network-bulletin row R1. One note a non-owner reviewer should see: every score, owner and date here is ILLUSTRATIVE, so the arithmetic and the clock logic are the transferable part, not the specific ratings.

Signed: Marcus Feld, compliance officer, Cascade Trust Bank, 2026-09-11
