# Release Readiness: Emberfall Tactics v4.2.1

Fills [templates/delivery/release-readiness.md](../templates/delivery/release-readiness.md). Everything here is invented for this standalone example: Emberfall Tactics is a fictional mobile tactics game, Kindlewick Games its fictional publisher, the Tactician Crate is its fictional paid loot mechanic, and every number, name and date is ILLUSTRATIVE, not drawn from any real studio or market. There is no external gaming-domain journey or data sheet. See the [examples index](README.md).

**Owner:** Noor Bashir, Release Manager · **Date:** 2026-11-05 · **Status:** Gate 5 held 2026-11-05; decision GO WITH CONDITIONS recorded below; launch target held at 2026-11-14 pending Google Play resubmission pass on 2026-11-10

**Release:** v4.2.1 "Ashen Depths" update · **Target date:** 2026-11-14
**Decider:** Noor Bashir, Release Manager · **Decision:** GO WITH CONDITIONS
**Decision date:** 2026-11-05 · **Held before any production rollout:** yes

## 1. Features

- [x] Everything in the PRD's launch scope is built, and nothing extra shipped unreviewed
- [x] Scope cuts since sign-off are listed here: The "Guild Wars" PvP mode was cut to post-launch v4.3 due to server load testing failures in October (see [growth-plan](../templates/planning/growth-plan.md) for the original bet); the cosmetic-only "Shadow Cloak" bundle was deferred to ensure it did not interfere with the Tactician Crate odds disclosure UI changes required by Google Play policy. Both cuts were reviewed against the core loop retention targets (D7/D30) and deemed non-blocking for the monetization gate.
- [x] Acceptance criteria all pass (Gate 4 evidence: `qa-report-v4.2.1.pdf` in the release workspace, not tracked in this repository, signed off 2026-10-28)

## 2. Tests

- [x] Every blocking level in the [testing strategy](../templates/delivery/testing-strategy.md) ran and passed
- [ ] The [edge-case register](../templates/delivery/edge-cases.md) has no open rows (Exception: Row #42, "Crate opening animation stutters on Android 12 devices with low RAM," moved to Known Issues table with severity Low and owner J. Chen)
- [x] [UAT](../templates/delivery/uat-plan.md) is signed off, conditions listed below if any (Condition: UAT sign-off includes a caveat that the new odds disclosure text must be verified in German and Japanese localizations before store submission; verification completed 2026-11-04)
- [x] For AI features: eval thresholds met per the [eval spec](../templates/ai/eval-spec.md), and the [red-team review](../templates/ai/red-team-review.md) is closed (Note: v4.2.1 contains no generative AI features; the matchmaking algorithm update was tested against fairness metrics but does not require red-team review under current internal policy as it is deterministic based on player skill rating)

## 3. Known issues shipping with this release

| # | Issue | Severity | Why it is acceptable to ship | Fix owner | Fix date |
|---|---|---|---|---|---|
| 1 | Platform certification: build 4.2.1 passes Apple App Store review and Google Play policy review, including the drop-rate disclosure for the Tactician Crate paid loot mechanic. Apple accepted 2026-11-03; Google's review flagged the crate's odds disclosure as not visible pre-purchase on the storefront listing (not the in-app screen, which already discloses it); resubmission queued for 2026-11-10, launch date held 2026-11-14 pending that pass, with a same-week resubmission slot reserved | High | This is a condition, not an issue that may ship open. The release cannot proceed until Google Play accepts the updated storefront metadata. Launch is held until 2026-11-14 to accommodate the resubmission queue. If Google rejects again, launch slips to 2026-11-21. | Noor Bashir, Release Manager | 2026-11-10 |
| 2 | Crate opening animation stutters on Android 12 devices with <4GB RAM | Low | The stutter is visual only and does not affect the random outcome or the transaction. It affects approximately 3% of the active device base. A fix is scheduled for v4.2.2. | J. Chen, Client Lead | 2026-11-20 |
| 3 | Localized string for "Tactician Crate" in French is 12 characters longer than the button width allows, causing truncation on iPhone SE | Medium | Truncation renders as "Tactic..." which is still recognizable to users who have seen the English version. A hotfix for string length adjustment is ready but requires a separate binary upload, delaying the iOS build slightly. We will ship with truncation and patch in v4.2.2 to avoid holding the entire release for one locale. | M. Dubois, Localization Lead | 2026-11-20 |

## 4. Rollback

- [x] Rollback procedure exists and was tested on [Staging Environment B], on [2026-11-02]
- Rollback trigger, agreed in advance:
    1. Server-side error rate for `crate_open` transactions exceeds 2% for 15 minutes.
    2. Any gambling regulator inquiry or cease-and-desist letter received regarding the Tactician Crate mechanics in any launch market.
    3. Critical crash rate on launch day exceeds 5% of daily active users.
- Rollback owner: Noor Bashir, Release Manager · Time to roll back: 10 minutes (via feature flag disablement)
- Data written between release and rollback:
    - Purchases made during the faulty window are retained and fulfilled manually by support.
    - Unopened crates purchased during the faulty window remain in inventory.
    - Odds calculations are logged server-side for audit; logs are preserved even after rollback.

## 5. Operations and monitoring

- [x] Dashboards and alerts for this release are live (see [observability](../templates/architecture/observability.md)). Specific dashboards created for:
    - Tactician Crate purchase conversion rate vs baseline.
    - Payer concentration metric (top 1% payer share of revenue) to detect anomalous spending patterns.
    - Regional loot-box opt-out rates (for markets where disabling is possible).
- [x] [Failure scenarios](../templates/delivery/failure-scenarios.md) reviewed with the on-call owner (Scenario: "Odds disclosure mismatch between client and server" walked through; mitigation is server-authoritative result generation regardless of client display bug)
- [x] The [operational readiness review](../templates/operate/operational-readiness-review.md) is complete

## 6. Communications

| Audience | What they get | Owner | Sent |
|---|---|---|---|
| Support team | Briefing on Tactician Crate odds disclosure changes, known Android stutter, and escalation path for refund requests related to "unfair odds" complaints. Script provided for handling COPPA/GDPR-K data deletion requests involving minors who opened crates. | Sarah Jenkins, Head of Support | 2026-11-04 |
| Internal stakeholders | Release note highlighting the Google Play resubmission status, the launch hold date, and the server-side kill switch capability for crate odds. | Noor Bashir, Release Manager | 2026-11-05 |
| Customers | Announcement of "Ashen Depths" content update. No specific mention of the delay unless launch slips beyond 2026-11-14. If slipped, a "coming soon" banner update on social channels. | Marketing Team | N/A (silent release until launch) |

## 7. Regulated overlay

- [x] Does this release touch a product that contains an AI or machine-learning feature and has a financial or data regulator applying to it?
    - **Answer:** No. The matchmaking-algorithm update is deterministic, not a machine-learning feature, so the AI-overlay condition in the router is not met and this section does not tick that overlay gate line. The regulated module still applies here for two other, unrelated reasons: the Tactician Crate's paid randomized rewards fall under consumer-protection and, in some jurisdictions, gambling regulation, and data collection from under-13 users triggers COPPA (US) and GDPR-K (EU) obligations. Both are named below with what was brought instead of the AI-overlay checklist.
    - **Action Taken:** The regulated module was run via the [reg-gap-check skill](../skills/reg-gap-check/SKILL.md). The [compliance impact assessment](../templates/operate/compliance-impact-assessment.md) is signed by Legal Counsel (A. Rossi) on 2026-11-01.
    - **Loot-Box Posture by Market (as of 2026-09-11, confirm with counsel; Legal Counsel A. Rossi confirms no change to this posture as of the 2026-11-05 decision date):**
        - **Belgium:** Paid random rewards treated as gambling. Tactician Crate disabled. Users see fixed-price bundles instead.
        - **Netherlands:** Kansspelautoriteit scrutiny high. Odds disclosed prominently. Crate enabled but monitored.
        - **South Korea:** Self-regulatory guidelines require probability disclosure. Disclosed in-game and on store listing. Enabled.
        - **USA:** FTC scrutiny ongoing. No federal ban. State laws vary. Enabled with full disclosure. COPPA compliance ensures under-13 accounts cannot purchase crates without parental consent flow.
        - **EU General:** GDPR applies to data processing. Odds disclosure required by consumer law directives. Enabled.
    - **Under-13 Posture:** Accounts identified as under-13 (via birthdate entry and age assurance checks) are excluded from Tactician Crate purchases entirely. They can only access fixed-reward events. Chat is restricted to pre-set phrases for all under-18 accounts.
    - **Payer-Concentration Telemetry:** Implemented to monitor if top 0.1% of payers account for >50% of crate revenue. Alert threshold set at 60%. If breached, marketing spend for whale-targeting campaigns is paused pending review.
    - **Server-Side Flag:** `crate_odds_override` flag implemented. Allows immediate rollback of crate odds to previous values or disabling of the mechanic globally without a client update. Tested on Staging 2026-11-02.

## 8. Sign-offs per function

| Function | Name | Verdict | Conditions | Date |
|---|---|---|---|---|
| Product | Elena Vance, Product Director | GO WITH CONDITIONS | Launch held until Google Play acceptance on 2026-11-10. If rejected, slip to 2026-11-21. | 2026-11-05 |
| Engineering | Raj Patel, Eng Lead | GO | None. | 2026-11-05 |
| QA | Chris O'Malley, QA Manager | GO | Known issue #2 (Android stutter) accepted as Low severity. | 2026-11-05 |
| Design | Yuki Tanaka, Design Lead | GO | Verified odds disclosure UI meets accessibility contrast standards. | 2026-11-05 |
| Support | Sarah Jenkins, Head of Support | GO | Scripts for refund and complaint handling briefed to team. | 2026-11-05 |
| Data | Priya Singh, Data Scientist | GO | Payer concentration dashboard live and alerting configured. | 2026-11-05 |
| Legal / Compliance | Antonio Rossi, Counsel | GO WITH CONDITIONS | Belgium crate disabled confirmed. All other markets require annual re-review of loot-box status. COPPA age-gate logic verified. | 2026-11-05 |

## 9. How this gate fails while looking like it passed

| Failure mode | What it looks like in the room | The rule that stops it |
|---|---|---|
| Rubber-stamp under date pressure | "We are fine, ship it", five times in five minutes, and nobody opens the runbook | Go criterion by criterion, pass or fail, recorded live rather than written up later |
| Empty known-issues table | A blank table presented as a clean result, with the real risks in direct messages | Do not accept the gate until the table is populated with severity, owner and mitigation |
| Rollback nobody tested | "We have a rollback plan" on a slide, no rehearsal, no timing | Require a rehearsal in a real environment, recently, with the elapsed time recorded |
| Sign-off by team, not person | "Engineering approves", written by whoever had the document open | Named sign-offs with role and date. A team cannot be paged or asked what it meant |
| Conditions agreed aloud | Everyone nods at "we will fix X first", and nothing is written | Conditions go in the sign-off row before the meeting ends, or the verdict is not conditional |
| Green dashboard, wrong metric | Every tile green while latency has tripled and the error budget is spent | Name the indicators tied to this release's user-visible behaviour, not only system uptime |
| Decider owns the ship date | The person holding the vote also owns the revenue number it affects | Declare it. Split the role for this gate, or record that the conflict was accepted and by whom |
| Gate held after the release | The meeting is on Friday, the flag was flipped on Tuesday, notes to be backfilled | The gate is held before any production rollout. There is no retroactive sign-off |

### Worked micro-example (ILLUSTRATIVE, invented)

<!-- A conditional go, which is the verdict people find hardest to write down properly. Delete it once this file holds a real release. -->

**Release:** *v2.4, receipt auto-extraction* · **Decision:** *GO WITH CONDITIONS* · **Decider:** *R. Ali, product lead*

| # | Issue | Severity | Why it is acceptable to ship | Fix owner | Fix date |
|---|---|---|---|---|---|
| *1* | *Extraction fails on receipts photographed in low light, and falls back to manual entry without telling the user why* | *medium* | *The fallback is correct and loses no data. The silence is confusing, not harmful, and affects a minority of submissions* | *S. Kaur* | *2026-06-12* |
| *2* | *Support runbook does not cover the fallback path* | *high* | *Not acceptable to ship. This is a condition, not a known issue* | *Support lead* | *before rollout* |

*Conditions recorded in the sign-off row: support runbook published and the support team briefed, both before the flag is enabled for any customer. Rollback trigger agreed in advance: manual-entry fallback rate above the pre-launch baseline for two consecutive hours, called by the on-call engineer without further discussion.*

The second row is the point. It was raised as a known issue and it is not one: nothing about it is acceptable to ship, so it became a written condition with a deadline before rollout. Known issues and conditions get confused constantly, and the difference is whether the release may proceed while it is open.

## Exit gate

Gate 5 is green when:

- [x] Every checklist box above is checked, or its exception sits in the known-issues table with an owner and a date (Edge-case register row #42 is in Known Issues #2)
- [x] The known-issues table is not empty, or the emptiness is explained (Populated with 3 items)
- [x] Every known issue distinguishes itself from a condition: an issue may ship open, a condition may not (Issue #1 is explicitly marked as a condition blocking launch; Issues #2 and #3 are shippable defects)
- [x] The rollback trigger is a condition a dashboard can show, not a feeling, and the procedure was executed on a dated environment (Triggers defined as % error rate and regulator inquiry; tested 2026-11-02)
- [x] Every sign-off row has a name and a date, and every conditional verdict has its condition written in the row (Product and Legal have conditions written)
- [x] The decider recorded GO, NO-GO, or GO WITH CONDITIONS, with conditions in writing (GO WITH CONDITIONS recorded in header and section 1)
- [x] This gate was held before any production rollout, and the header says so (Header states "Held before any production rollout: yes")
- [x] Section 7 is answered even where the answer is no, with the reason written (AI-overlay condition answered No with the reason; regulated module still run for the two unrelated triggers, with detailed market posture)

Signed: Noor Bashir, Release Manager, 2026-11-05
