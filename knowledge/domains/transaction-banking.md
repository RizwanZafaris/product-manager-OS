---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Transaction banking", "cash management", "corporate treasury banking", "transaction-banking"]
---
# Transaction banking

Your customer here is not a person, it is a corporate treasury function, and the treasurer, the accounts payable clerk who runs the actual payment file, and the auditor who needs an unbroken trail across every bank relationship are three different people who want three different things. The treasurer buys certainty and a cut-off time, not a feature list: a bulk payment file that fails at four in the afternoon is not a bug report, it is a client who missed payroll and remembers it. The distinctive fact is that corporates move money in files, not in single taps. A payroll or supplier run can carry thousands of line items in one file, built on ISO 20022 or an older proprietary format, and a single malformed row can fail the whole batch, or worse, half succeed it while the rest silently do not post. Liquidity management, cash pooling and sweeping across a group's accounts and currencies, is itself a regulated activity in some jurisdictions and a cross-border tax and FX question in every one of them. Trade finance, letters of credit, guarantees, supply chain finance, still runs substantially on paper and SWIFT message types even as legal frameworks slowly catch up to digital documents.

## Questions a PM must ask

1. Who is the buyer, who is the daily user, and who is the auditor, and do they actually want the same thing? A treasurer wants visibility, a clerk wants fewer clicks per run, an auditor wants a trail that cannot be edited after the fact.
2. What happens to the other several thousand rows in a bulk payment file when one row fails validation? Partial batch failure semantics decide whether this is a minor defect or a payroll incident.
3. Which rail carries this instruction, and what is its cut-off time, cost, and reversibility? A same-day domestic transfer and a cross-border wire have different risk and cost profiles, and treating them as interchangeable mis-prices both.
4. Is this a payment initiation feature, a cash visibility feature, or a liquidity movement feature? Dual authorisation rules and audit expectations differ sharply between the three.
5. Does maker-checker dual control apply here, and can it be evaded, for example by one person holding both roles, or by a batch under a threshold skipping review entirely?
6. Where does a reconciliation break get raised when the corporate's ERP and the bank's core disagree about a settled payment, and who owns closing it?
7. For a cross-border instruction, is the FX rate shown to the customer before they confirm, or only after the transfer has already been priced against them?
8. If a trade finance instrument, a guarantee or a letter of credit, is involved, does the product actually track the instrument's legal state under the applicable rulebook, rather than treating it as a generic document upload?

## Gatekeepers

- **Corporate treasury and its bank-relationship policy.** A treasurer will not move a payroll file through an unproven rail; multi-bank redundancy and a demonstrated fallback are commercial requirements, not nice-to-haves.
- **Maker-checker policy owners inside the corporate customer.** They set the authorisation matrix the product must enforce, and a workflow that lets one person quietly satisfy both roles voids their own control.
- **The bank's own treasury and liquidity risk desk.** Cash pooling and sweeping move real intraday liquidity positions, and this desk can block a feature that creates unhedged intraday exposure.
- **SWIFT, via its Customer Security Programme.** Not a regulator, but every institution sending or receiving SWIFT traffic self-attests annually against its controls framework, and a vendor touching that pipeline inherits the evidentiary burden.
- **National payment scheme operators and their file-format rulebooks**, Nacha for US ACH, the domestic bulk clearing and switching operator elsewhere (Pakistan's 1Link is a non-US example). A malformed file is judged against the scheme's rulebook, not the product's assumptions.
- **Sanctions and AML screening.** Every cross-border corporate payment is screened before release, and a product that lets a user simply resend a held payment without re-screening has built a control gap, not a convenience.
- **External auditors of the corporate customer.** Need an exportable, unbroken trail from initiation to bank confirmation for every material payment; a UI log the bank itself can edit is not evidence.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Straight through processing rate for bulk files | Processing efficiency | Rises when exception-prone payment types are filtered out of the measured population before the count is taken |
| Cut-off adherence for same-day payments | Reliability against the customer's real deadline | Measured against the bank's internal cut-off, not the treasurer's actual payroll deadline once approval time is subtracted |
| Partial batch failure rate | Bulk processing integrity | A low rate hides that one partial failure inside a payroll file is a relationship event no average can absorb |
| Reconciliation break aging, bank to ERP | Control health | A shrinking backlog can mean breaks are being written off rather than actually investigated |
| FX margin captured | Revenue on cross-border payments | A basis-point spread hides the absolute cost a high-volume corporate actually pays, which they experience in currency, not in basis points |
| Time to onboard a corporate account | Sales cycle health | Improves by deferring complex entity structures or trade finance products to a later phase that never actually closes |
| Payment file rejection rate at the scheme level | Format quality | A whole-file rejection scores the same as a one-row rejection, though the operational cost to the client is not the same |
| Maker-checker override or exception rate | Control robustness | Near zero often means overrides are pre-approved in bulk, not that the control is regularly and honestly tested |
| Client-reported statement lag | Trust in cash visibility | Bank-side settlement can post same day while the statement or reporting feed lags by a business day, and the two get conflated |

## Reading

- **The SWIFT Customer Security Programme.** The controls framework every SWIFT-connected institution self-attests against annually; read it before assuming a "SWIFT integration" is a purely technical project.
- **ISO 20022 corporate-to-bank messaging**, payment initiation and account statement message types, the standard progressively replacing older proprietary bank file formats and the SWIFT MT message series.
- **Nacha's Operating Rules for the US ACH network**, as the model bulk-payment rulebook; read your own jurisdiction's equivalent, for Pakistan that includes the rules operated through 1Link (verify current specifics before relying).
- **UCP 600 and the ICC's International Standard Banking Practice**, the baseline rules for documentary letters of credit even where the surrounding product is fully digital.
- **The UK's Electronic Trade Documents Act 2023.** Gives electronic bills of lading and similar instruments the same legal standing as paper, the clearest example of trade finance digitisation moving from technology into statute (verify the commencement date before relying).
- **Basel III's treatment of intraday liquidity and large exposures.** Shapes what a bank will actually let a pooling or sweeping product do across group entities, regardless of what the product spec assumes.

**Conductor overlay:** this domain sharpens DISCOVER-1 (name the person, since buyer, daily user, and auditor are three separate people here), DESIGN-2 (integrations, because every ERP and bank rail needs an owner and a failure behavior), DEFINE-5 (how requirements fail, since partial batch failure has to be a testable requirement, not prose), and OPERATE-3 (did the drivers move, since a working-capital or efficiency claim needs its mechanism traced, not assumed).

**Templates this bends:** [integrations](../../templates/architecture/integrations.md) (every bank rail and ERP connector gets an owner, SLA, and failure behavior), [failure-scenarios](../../templates/delivery/failure-scenarios.md) (partial batch failure is the canonical scenario to rehearse), [personas](../../templates/discovery/personas.md) (treasurer, clerk, and auditor as three distinct personas, not one composite), and [dashboard-spec](../../templates/operate/dashboard-spec.md) (straight-through processing and reconciliation breaks belong on the same dashboard so one cannot move without the other showing).
