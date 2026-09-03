---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["ERP", "erp", "enterprise resource planning", "finance and operations"]
---
# ERP and enterprise finance

The distinctive fact about this domain is that your product is the evidence. An ERP is not a system that reports the financial record, it is the financial record, which means an external auditor can refuse to sign accounts because of how your software stores a change. The second distinctive fact is that the famous failures were almost never software defects. Hershey, Nike, Lidl, Revlon and Birmingham City Council each shipped working software into an organisation that was not ready for it, on a date somebody chose badly, with data nobody had cleaned. A PM here spends more time on cutover, migration and process fit than on features, and the roadmap that ignores that is the roadmap that produces the case study.

## Questions a PM must ask

1. Does this feature touch the general ledger, a tax-relevant balance, or anything an auditor samples? If yes, immutability, retention and segregation of duties are requirements rather than hardening tasks.
2. Who signs off that the books produced by this system are correct, and what would they need to see to sign? The Controller is not a stakeholder to inform, they are the acceptance criterion.
3. What is the cutover plan, and what date does it land on? Hershey went live three months late into the run-up to Halloween. Go-live timing is an executive decision that a PM has to force into the open, not a scheduling detail.
4. What does the customer's data actually look like, as opposed to what their schema says? Migration defects surface at reconciliation, which is after cutover, which is after the fallback window closed.
5. Where does the customer's process genuinely differ from the standard model, and is that difference a competitive advantage or an accident? Lidl spent seven years and roughly EUR 500 million bending software to a purchase-price inventory valuation it could have changed.
6. Can a user initiate, approve and post the same transaction? If the answer is anything other than a system-enforced no, you have built a fraud path and an audit finding.
7. Which jurisdictions does the customer invoice in, and what does each mandate? Country e-invoicing regimes arrive on legislative calendars that outrank your roadmap.
8. What is the rollback, and has anyone run it? A cutover with no rehearsed reverse is a one-way door that the business does not know it is walking through.

## Gatekeepers

- **The external auditor.** Not a customer stakeholder at all, which is why teams forget them. They can qualify an opinion or refuse to rely on the system, and the usual triggers are mutable audit trails, unexplained manual journals, and access that nobody reviewed. Under Sarbanes-Oxley section 404 management and, for larger filers, the auditor must assess internal control over financial reporting, and your logs are the evidence.
- **The corporate controller.** Signs the balances. Will block go-live on a reconciliation they cannot explain, and is right to.
- **Internal audit and the SOX programme office.** Own the control matrix. A feature that creates a new segregation-of-duties conflict has to be remediated before it reaches production, not after the annual test finds it.
- **Tax.** Country e-invoicing and reporting mandates are dated obligations with legal consequence. They are the one part of the roadmap that cannot slip.
- **IT change management and the release board.** Own the window. Financial-period close, statutory reporting and peak trading all close the window, and the intersection can leave very few usable dates in a year.
- **The data migration owner.** Holds a veto in practice even without one on paper: if reconciliation does not tie, nothing proceeds.
- **Works councils and payroll, where the suite includes HR.** Payroll go-live carries same-day wage exposure, so a parallel run is the norm rather than a precaution. See [hr-tech](hr-tech.md).

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Days to close the period | Whether the finance process actually got faster | Improves by deferring hard variances into aging exception buckets that are never cleared. Pair it with the value and age of open items |
| Reconciliation match rate | Whether the two sides of the record agree | Tolerance thresholds are set locally, so a high rate can mean a generous tolerance rather than a clean ledger |
| Segregation-of-duties violations | Live fraud paths and audit exposure | Counts conflicts detected by the rules you configured. A shrinking number can mean the ruleset was narrowed, not that the risk fell |
| Manual journal entries | How much the system is being worked around | A low count can mean the workarounds moved into spreadsheets outside the system, where nobody logs them |
| Audit findings raised | Whether controls held | Lags by a year and reports the prior configuration. It tells you about the software you shipped last year |
| Data migration accuracy | Whether the record survived the move | Usually measured on record counts, which pass while values, dates and currencies are wrong. Reconcile balances, not rows |
| Customisations in the deployment | Distance from the standard model, and the cost of the next upgrade | Counting objects flatters you. One customisation in the valuation model, which is what stopped Lidl, outweighs a hundred cosmetic ones |
| Time to go-live | Implementation velocity | Improves by descoping quietly, migrating less history, or declaring a phase live before the business runs on it |
| Uptime | Availability | A monthly average absorbs a two-hour outage during period close, which is the only outage anyone will remember |

## Reading

- **Grant Thornton's public-interest report on Birmingham City Council's Oracle implementation**, February 2025. The most useful ERP failure document currently available because it is an auditor's account rather than journalism. Budget moved from roughly GBP 19 million to over GBP 90 million, the council operated without an adequate financial management system for over two years, and the report names the cause as governance rather than software: an "adopt not adapt" principle abandoned under pressure, external reliance that weakened control, and a culture in which, in the report's own framing, bad news was unwelcome. That last finding is a product risk, not an organisational aside.
- **The Hershey 1999 go-live.** A 48-month plan compressed to 30 to clear Y2K, delivered three months late into peak season, with testing cut to make the date. Over 100 million dollars of orders could not be processed while the stock sat in the warehouse. The lesson a PM should take is about the compression, not the software.
- **Lidl and the eLWIS programme, 2011 to 2018.** Roughly EUR 500 million written off because the company would not change a purchase-price inventory valuation to match the standard retail-price model. The clearest case anywhere of a process difference that nobody costed being allowed to define the architecture.
- **Revlon's S/4HANA cutover, 2018.** Manufacturing disrupted, roughly 64 million dollars of orders unfilled, expedited freight to recover, delayed results, and a shareholder suit. Read it for the second-order costs: the remediation spend and the disclosure consequences exceeded the direct miss.
- **SEC Rule 17a-4**, as amended in 2022. Worth reading even outside broker-dealer scope because the amendment accepted a complete time-stamped audit trail of modifications and deletions as an alternative to write-once storage. It is a precise statement of what regulators consider equivalent to immutability, which is a question ERP architecture keeps asking.

**Conductor overlay:** this domain sharpens DISCOVER-2 (the evidence is the customer's actual data, not their process documentation), DEFINE-3 (non-functional requirements are audit requirements, and they come from a framework rather than from a preference), DESIGN-4 (migration and cutover are design, not delivery), and DELIVER-2 (release readiness is dominated by the reconciliation, the rehearsed rollback, and the calendar).

**Templates this bends:** [nfr](../../templates/definition/nfr.md) (immutability, retention and segregation of duties become stated targets with a named framework behind each), [migration-cutover-plan](../../templates/delivery/migration-cutover-plan.md) (the central artifact of this domain rather than a delivery appendix), [release-readiness](../../templates/delivery/release-readiness.md) (gains a reconciliation sign-off and a rehearsed-rollback row), and [risk-register](../../templates/execution/risk-register.md) (go-live date and data quality are the two entries that keep appearing in the failures above).
