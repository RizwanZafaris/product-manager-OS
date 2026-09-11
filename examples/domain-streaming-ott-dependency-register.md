# Dependency Register: Northlight Streaming Rel-2 Catalogue and Ad-Tier Launch

Fills [templates/execution/dependency-register.md](../templates/execution/dependency-register.md). Everything here is invented: Northlight Streaming is a fictional subscription video service, Studio Corvid is its fictional content licensor, the people are roles filled by invented names, and every number, name and date is ILLUSTRATIVE. See the [examples index](README.md).

**Owner:** Priya Anand, senior product manager (catalogue and experience) · **Date:** 2026-11-04 · **Status:** Live register, reviewed weekly at the Monday catalogue-and-launch stand-up; last reviewed 2026-11-03

## 1. The register

| # | Dependency (deliverable, not a team name) | Owning team | Their named contact | Needed by (our date) | Their committed date | Status | Escalation contact (their manager or ours) |
|---|---|---|---|---|---|---|---|
| DEP-4 | Renewed output-deal licence for Studio Corvid's catalogue, 300 titles, UK and Ireland territory only | Studio Corvid, rights licensing | Elena Voss (ILLUSTRATIVE) | 2026-12-01, 60 days before the current window expires | not yet committed, in renewal negotiation | at risk | Head of Content Partnerships |
| DEP-5 | Sports rights blackout feed: a machine-readable per-title, per-territory schedule of when each live fixture goes dark after broadcast, covering all fixtures on the rights calendar to end of season | Rights operations (internal), with the league's media-rights desk as source | Marcus Adeyemi (ILLUSTRATIVE) | 2026-12-08, first live fixture of the winter slate | 2026-12-05, feed schema agreed and test data delivered | committed | Director of Rights Operations |
| DEP-6 | Subtitle and dub delivery for the localisation batch gating the Nordic launch window: 40 new titles, subtitle files plus QC sign-off, in five languages | Lumen Subtitles Ltd (vendor) | Ines Kovač (ILLUSTRATIVE) | 2026-12-15, the launch window opens; nothing ships into a market without its localised assets | 2026-12-10, final batch and QC report | requested, vendor has signed an SOW but no dated delivery plan on their own production schedule | Account Director, Lumen Subtitles, escalate to Head of Vendor Management |
| DEP-7 | Age classification for the 40 new localisation-batch titles: BBFC certificates for UK distribution, and equivalent certification for Ireland through the Irish Film Classification Office (IFCO) (as of 2026-09-11; confirm with counsel, not legal advice) | Standards and Practices (internal compliance) | Rowan Ellis (ILLUSTRATIVE) | 2026-12-12, three days before the launch window so the storefront can carry correct age gates | 2026-12-08, all 40 titles classified and filed | in progress | Chief Content Officer |
| DEP-8 | DRM licence-server vendor certification: Widevine L1 and FairPlay streaming-certified attestation from Veridex Systems (fictional vendor), covering the licence-server update shipped in release 24.3 | Platform engineering (internal), with Veridex Systems as the certifying party | Tomás Ferreira (ILLUSTRATIVE) | 2026-12-10, before any title above HD resolution enters the new catalogue slice | 2026-12-07, certification letter received | committed | VP Engineering Platform |
| DEP-9 | Ad-tier measurement partner integration: IAB Tech Lab certified ad impression verification endpoint live in staging, covering both client-side and server-side ad insertion paths | Ad technology (internal), with Metrica Labs (fictional measurement vendor) as the external party | Sofia Lindgren (ILLUSTRATIVE) | 2026-12-18, ad-tier public beta opens; sold campaigns must report verified impressions from day one | 2026-12-14, sandbox integration tested and signed off | committed | Head of Ad Sales Technology |

## 2. Escalation ladder

This register's escalation path runs through content partnerships, not engineering. A rights window does not move because a sprint velocity changes; it moves because a commercial conversation happens or it does not happen. The ladder below reflects that reality.

1. Slip detected at weekly review: register owner contacts the named contact within one working day. For DEP-4 this means Priya Anand calls Elena Voss directly; for internal rows (DEP-5, DEP-7, DEP-8, DEP-9) the same rule applies to the internal contact.
2. No recovery plan within two working days: escalate to the escalation contact on the row. For DEP-4, DEP-5 and DEP-6 this is the Head of Content Partnerships or the Director of Rights Operations, never the VP Engineering. For DEP-7 the escalation is to the Chief Content Officer. For DEP-8 and DEP-9 the escalation may go through engineering leadership since those are technical certifications, but the business consequence still routes back to content partnerships.
3. Still unresolved and the needed-by date is inside three weeks: raise at the Wednesday Content Partnerships steering call (Priya Anand, Head of Content Partnerships, CFO delegate, General Counsel delegate), and the dependency becomes a risk register row with a mitigation. For DEP-4 specifically, "mitigation" at this stage means beginning the process of removing affected titles from the storefront ahead of expiry, because the window will expire regardless of who is escalated.

## 3. Reverse dependencies

| Deliverable we owe | To team | Their needed-by | Our committed date | Status |
|---|---|---|---|---|
| Final title list with confirmed availability windows for Q1 2027 ad-sales packages, including which of the 300 Studio Corvid titles remain licensed past 2026-12-01 | Ad Sales | 2026-11-20, sales teams build Q1 packages against this list | 2026-11-18, pending DEP-4 outcome; if DEP-4 slips past 2026-11-15 the list ships marked "provisional, subject to licence renewal" | requested, blocked by DEP-4 |
| Blackout schedule integrated into the sports discovery rail so live fixtures do not appear as on-demand until the hold-back expires | Experience squad (discovery) | 2026-12-05, before the winter slate begins | 2026-12-03, contingent on DEP-5 delivering the feed by 2026-12-05 | committed |
| Age-gate configuration for the 40 new titles pushed to the storefront and parental-controls layer | Storefront and platform squad | 2026-12-13, two days before the launch window | 2026-12-11, contingent on DEP-7 completing classification by 2026-12-08 | committed |
| Verified impression reporting for the first 14 days of ad-tier beta, formatted to Metrica Labs' specification | Ad Sales and finance | 2027-01-05, first billing cycle closes | 2026-12-18 onward, contingent on DEP-9 | committed |

The first row is the one that earns sleepless nights: if DEP-4 is not resolved by 2026-11-15, Ad Sales cannot sell Q1 packages against titles that may leave the catalogue on 2026-12-01, and any campaign sold against a departing title becomes a refund liability. This is the reverse-dependency pressure that makes the escalation ladder in section 2 non-negotiable.

## 4. Weekly review notes

| Date | Rows that changed status | Escalations opened or closed |
|---|---|---|
| 2026-11-03 | DEP-4 remains at risk: Studio Corvid's renewal counter-proposal received 2026-10-30, requesting a 15% uplift on the annual fee and a 12-month term instead of 24 months; our legal team is reviewing. No change to status vocabulary, still at risk. DEP-6 moved from committed to requested: Lumen Subtitles confirmed the SOW was countersigned but their production scheduler has not placed the 40-title batch on their own timeline, so there is no dated delivery plan on their side, only ours. Per the rule, this is requested, not committed. | DEP-4: Priya Anand called Elena Voss on 2026-11-03 (one working day after the counter-proposal landed); no escalation yet, the two-working-day clock started 2026-11-04. DEP-6: Priya Anand emailed Lumen's Account Director on 2026-11-03 asking for the dated production schedule; no escalation yet. |
| 2026-10-27 | Title "Corvid Originals: Season Three Finale" left the catalogue on 2026-10-27, its window expiry date, as scheduled. This is the proof-of-concept failure mode: the title departed whether or not anyone escalated anything, because the contract said 2026-10-27 and 2026-10-27 arrived. No other row changed status. | None opened. This event is logged not as an escalation but as evidence for the Wednesday steering call that DEP-4 carries real consequences: the next such departure is 300 titles, not one. |
| 2026-10-20 | DEP-8 moved from requested to committed: Veridex Systems placed the certification audit on their own schedule for the week of 2026-12-01, with the letter due 2026-12-07. DEP-9 moved from requested to committed: Metrica Labs confirmed their staging endpoint would be available from 2026-12-01 with integration testing complete by 2026-12-14. | None. Both rows now show the owning party's own dated commitment, satisfying the "committed" definition. |
| 2026-10-13 | DEP-5 created: Rights Operations confirmed the league's media-rights desk would deliver the blackout schedule feed by 2026-12-05, and Marcus Adeyemi accepted the dependency on behalf of his team. DEP-7 created: Standards and Practices accepted the 40-title classification workload and committed to delivery by 2026-12-08. | None. New rows entered as committed because both internal teams have the work on their own plans with dates. |

## How this register fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| A verbal yes recorded as committed | "Elena said the renewal is basically done", entered as committed with no date | Committed means on their plan with their date. Anything else is requested. A studio executive saying "we are in good faith discussions" is not a commitment; it is a lead |
| No named human | The owning team is named and no person is | Teams do not answer messages. Name the contact and the escalation contact. For DEP-4, "Studio Corvid" is not a phone number; Elena Voss is |
| At risk is felt, not computed | The status column reflects mood rather than arithmetic | At risk means their date is after your needed-by. Compare the columns weekly. For DEP-4, "not yet committed" against a needed-by of 2026-12-01, itself 60 days ahead of the window's own expiry, is at risk by definition: every week without a committed renewal is a week closer to a titles-leave-the-catalogue date that does not move for negotiation status |
| Escalation avoided | A row sits at risk for weeks because raising it feels aggressive | The ladder is agreed in advance, so escalating is procedural rather than personal. For content-partnership escalations, the Head of Content Partnerships expects these conversations; they are part of the job description, not a complaint |
| Reverse dependencies blank | Only what you need from others is tracked | Fill what you owe. Here, the ad-sales Q1 package deadline is the goodwill that keeps the Wednesday steering call listening to the DEP-4 escalation. If we owe them nothing, they owe us no attention |
| Treating a rights expiry as an engineering problem | Someone suggests "can we just keep serving the title and sort out the licence later?" | The escalation ladder routes through content partnerships precisely because no engineering effort moves a licence date. A title leaves on its expiry date. The product response is graceful removal from the storefront, not a workaround |

## Exit gate

- [x] Every dependency names a deliverable, a human contact, and an escalation contact. All six rows carry a specific deliverable (not "the rights team"), a named individual, and an escalation contact whose role matches the nature of the dependency
- [x] Every row shows both our needed-by date and their committed date. DEP-4 shows "not yet committed" explicitly, which is honest; the other five rows carry dates
- [x] No row claims "committed" without the work on the owning team's own plan. DEP-6 was downgraded from committed to requested on 2026-11-03 when Lumen's scheduler had not placed the batch on their own timeline. DEP-4 has never been marked committed
- [x] Every at-risk or blocked row has a corresponding risk register entry. DEP-4 maps to risk R-07 ("Studio Corvid output deal lapses, 300 titles removed from UK/Ireland catalogue"); the reverse dependency on Ad Sales maps to R-08 ("Q1 ad packages sold against departing titles create refund liability")
- [x] Reverse dependencies are filled in, not left as a courtesy blank. Four rows, including the one that creates commercial pressure to resolve DEP-4
- [x] The weekly review has an entry from the current or previous week. Entry dated 2026-11-03, the most recent Monday stand-up
- [x] The example row has been deleted. The template's payments-webhook example row does not appear; DEP-4 replaces it as the first row, carried unchanged from the domain card

Signed at Gate 3 review, 2026-11-04: Priya Anand, senior product manager (register owner); David Chen, Head of Content Partnerships (escalation authority for DEP-4, DEP-5, DEP-6); Amara Osei, VP Engineering Platform (technical certification owner for DEP-8, DEP-9); Lena Marchetti, Chief Content Officer (regulatory classification owner for DEP-7).
