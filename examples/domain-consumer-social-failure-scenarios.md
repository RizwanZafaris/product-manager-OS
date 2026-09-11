# Failure Scenarios: Driftcast moderation, age assurance and recommendation surfaces

Fills [templates/delivery/failure-scenarios.md](../templates/delivery/failure-scenarios.md). Everything here is invented: Driftcast is a fictional photo and short-video sharing app, the people are roles filled by invented names, and every number, date and identifier is ILLUSTRATIVE, drawn from the consumer-social domain card and the shared journey data sheet rather than from any real app or incident. See the [examples index](README.md). Regulatory statements are as of 2026-09-11, confirm with counsel, and are not legal advice.

**Owner:** Chiara Lombardi, Head of Trust and Safety · **Reviewed with:** Marco Oyelaran, on-call lead · **Date:** 2026-09-11

## 1. Scenario table

<!-- Detection means "how we know within minutes, without a customer telling us".
     If the honest answer is "a customer tells us", write that, and open a monitoring
     gap in section 2. Recovery names steps, an owner, and a time estimate. -->

| ID | Scenario | Blast radius | Detection | Recovery | Data loss risk |
|---|---|---|---|---|---|
| FS-1 | Coordinated harassment raid backs up the report queue, the moderation-overload row carried from [the domain card](../knowledge/domains/consumer-social.md) | Every reported user, including the person being targeted, sees no visible action for hours; worst case is a targeted creator leaving the platform | Open-report-queue depth alert crosses 500 cases, plus a per-account report-velocity alert at 10 times normal inside 30 minutes | Auto-throttle the reported account's reply rate once reports cross 200; page the on-call trust and safety lead, not only engineering on-call; owner: Chiara Lombardi; expected under 6 hours to clear the backlog | None; reports are durable and rejected cases are logged with reason codes |
| FS-2 | Age-assurance vendor fails closed for new sign-ups (ILLUSTRATIVE vendor name: Vellum Verify) | No new user under the age-assurance threshold can complete sign-up in the affected market; existing users unaffected | Vendor health-check alert plus a sign-up completion-rate drop alert at 20 percent below the trailing 7-day median | Fail open only for the 18-and-over self-declaration path where counsel confirms it is permitted; hold under-18 sign-ups in a queue and re-verify on recovery; owner: Marco Oyelaran; expected under 2 hours to restore vendor path, queue cleared within 24 hours | Possible: age-assurance session tokens for sign-ups attempted during the outage; no content or profile data lost |
| FS-3 | Hash-matching pipeline breaks and the legal reporting duty is not met (US reporting to NCMEC) | Reported content may not reach NCMEC within the statutory window; worst case is both a legal exposure and continued exposure of harmful content | Pipeline heartbeat alert plus a mismatch between upload-hash volume and hash-match call volume over a 15-minute window | Fail closed for uploads that require hash matching; page the trust and safety lead and legal counsel immediately; owner: Chiara Lombardi with legal counsel; expected under 1 hour to restore the pipeline, reporting catch-up within the same day | Possible: hash-match results for content processed during the outage window; content itself is retained |
| FS-4 | Recommendation-surface outage (the feed and the "For you" surface return errors or stale content) | All users see a degraded or empty feed; worst case is a contribution-rate dip while creators cannot reach an audience | Feed error-rate alert at 5 percent over 5 minutes, plus a feed render-time alert at the 99th percentile | Serve the last-known-good feed snapshot, disable personalized ranking, and page the platform on-call; owner: Marco Oyelaran; expected under 30 minutes to restore | None; feed ranking state is recomputed, not stored as the source of truth |

FS-0, the template's own completed sample row (receipt-storage service unavailable), is not reproduced here; the rows above are the consumer-social set the [domain card](../knowledge/domains/consumer-social.md) asks this template to extend with abuse and moderation-overload scenarios.

## 2. Monitoring gaps found while writing this

<!-- Every "we would not know" discovered above becomes a row here and a change
     request against ../architecture/observability.md. -->

| Gap | Fix | Owner | Date |
|---|---|---|---|
| Queue age by harm category was never measured; the queue-depth alert in FS-1 measures volume, not how long a report of a given harm category has been waiting | Add a queue-age-by-harm-category instrument, with separate alert thresholds for categories the [domain card](../knowledge/domains/consumer-social.md) lists (harassment, spam, CSAM, scams, coordinated manipulation), and route it to the trust and safety dashboard | Chiara Lombardi | 2026-10-09 |
| Age-assurance vendor outages are not distinguished from ordinary sign-up errors in the current alerting, so FS-2 would be detected as a generic drop | Add a vendor-scoped health check and a separate sign-up completion-rate alert per market | Marco Oyelaran | 2026-10-09 |
| Hash-match call volume is not reconciled against upload-hash volume, so a silent pipeline break would not surface | Add the reconciliation job and route its failures to the trust and safety lead, not only to engineering | Marco Oyelaran | 2026-10-09 |

## 3. Rehearsal

- Scenarios rehearsed (game day or tabletop), with dates: FS-1 was rehearsed as a tabletop exercise on 2026-08-28, led by Chiara Lombardi, trust and safety lead, with Marco Oyelaran and one moderator on call. FS-2 and FS-3 are scheduled for a joint tabletop on 2026-10-16, with legal counsel present for the FS-3 NCMEC reporting walk.
- The scenario we most doubt our recovery steps for: FS-1. The auto-throttle step assumes the per-account report-velocity alert fires before the queue-depth alert, and the exercise on 2026-08-28 did not confirm that ordering; if the queue-depth alert fires first, the backlog has already started and the 6-hour recovery estimate may not hold.

## Exit gate

This document passes when:

- [x] Every external dependency has at least one scenario row. Vellum Verify is covered by FS-2; the hash-matching pipeline and its NCMEC reporting duty by FS-3; the recommendation ranking surface by FS-4.
- [x] Every row states detection, and "customer report" answers created a section 2 gap. FS-1 detects by queue-depth and per-account velocity alerts, not a customer report; the queue-age-by-harm-category gap is filed in section 2 because that measure was never built.
- [x] Every recovery names an owner and a time estimate, not just steps. FS-1: Chiara Lombardi, under 6 hours; FS-2: Marco Oyelaran, under 2 hours; FS-3: Chiara Lombardi with legal counsel, under 1 hour; FS-4: Marco Oyelaran, under 30 minutes.
- [x] Data loss risk is stated per row, including "none". FS-1 and FS-4 are "none"; FS-2 and FS-3 name the specific data at risk.
- [x] At least the highest blast-radius scenario has a rehearsal date. FS-1, the highest blast-radius row (every reported user, including the targeted person), was rehearsed 2026-08-28.

Signed: Chiara Lombardi, Head of Trust and Safety, 2026-09-11
