---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Legaltech", "legal tech", "legal technology", "law firm software"]
---
# Legaltech

The product sits between two duties older than software: the confidentiality a lawyer owes a client, and the rule, in most jurisdictions, that only a licensed lawyer may practice law. Both survive automation only if the product is built to respect them, and neither shows up in a normal user story. The distinctive fact that follows is that privilege is a property of the communication, not of the tool, and it can be waived by an act as small as routing privileged material through a channel a court later decides was not confidential enough, or by feeding it to a third-party model without informed client consent. One architecture decision, made once, can retroactively strip protection from years of a client's documents. "Who may practice law" is also answered differently outside the US bar-by-state model: England and Wales route conduct regulation through the Solicitors Regulation Authority and the Bar Standards Board, each with its own rules on outsourcing and technology, and a compliance design copied from the US Model Rules will miss both.

## Questions a PM must ask

1. Does this feature draft, predict an outcome, or recommend a course of action a reasonable client would rely on as legal advice? If yes, unauthorized-practice exposure attaches regardless of the marketing, and a licensed reviewer in the loop is a requirement.
2. Where does privileged material live once it enters the product, and who else, a subprocessor, a model vendor, a backup system, can technically reach it? An access path you did not design for is still a path a court can find when deciding whether privilege survived.
3. If a model is involved, is client data used to train it, and did the client agree in terms they would recognize as covering that? Standard terms are not the same as informed consent for privilege purposes.
4. Who is the client of record in the data model, and does that match who is actually being served? A conflict check run against the wrong entity is the failure mode that gets a lawyer disqualified from a matter.
5. What is the retention and litigation-hold story? A document the firm was obligated to preserve, and your product silently expired, is a spoliation problem on the firm's malpractice carrier and on your contract with them.
6. For e-discovery: can the process demonstrate defensibility, a documented, repeatable method, if challenged? Courts sanction discovery-process failures more often than the underlying dispute, and "the tool did it" is not a defense.
7. What happens when the tool is confidently wrong, a hallucinated citation, a missed deadline, a misclassified privileged document? Courts have already sanctioned lawyers for filing fabricated citations from generative tools.
8. Which bar's technology-competence and outsourcing rules apply, and has the firm's own risk or general counsel signed off, separately from IT security? Most Model Rules jurisdictions now read competence to include understanding the tool.

## Gatekeepers

- **State bar associations and their ethics rules (the ABA Model Rules, adopted state by state in the US).** Rule 5.5 restricts unauthorized practice; Rules 1.1 and 1.6 extend competence and confidentiality to technology choices. A bar ethics opinion, not a terms-of-service clause, decides whether a feature crosses the line.
- **The Solicitors Regulation Authority and the Bar Standards Board (England and Wales)**, or the equivalent conduct regulator in a civil-law jurisdiction. Non-US regulators draw confidentiality and outsourcing lines differently than the ABA framework.
- **Courts, through discovery sanctions and admissibility rulings.** Do not review a product before launch but will sanction a filing that used it badly; a documented, defensible e-discovery process is the only evidence that survives a challenge.
- **The client, through privilege itself.** Privilege belongs to the client, not the firm and not the vendor; the client can waive it by accident through your design, and no vendor contract restores it afterward.
- **General counsel and risk, internally at the firm.** The buyer of legaltech rarely feels a UPL or confidentiality failure first; risk and GC sign-off on data handling is frequently the real gate, separate from and slower than IT security review.
- **Malpractice insurers.** Increasingly ask specific questions about AI-tool use, citation verification, and data handling before renewing a policy; their questionnaire is a de facto requirements document nobody sent you.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Document review throughput | E-discovery or contract-review efficiency | Says nothing about precision and recall; moving fast through irrelevant documents inflates this while missing the ones that mattered |
| Citation or clause accuracy rate | Whether generated legal text can be trusted | Measured against a generic benchmark, not the specific jurisdiction in front of a real user; a strong score has coexisted with fabricated citations in filed briefs |
| Time to first draft | Drafting-tool value | A fast draft a lawyer must substantially rewrite before filing has not saved time, only moved it downstream and off the dashboard |
| Conflict-check turnaround | Whether new-matter intake is fast | A shallow entity-matching rule produces false clears that surface as a disqualification motion months later |
| Privilege-log accuracy | Discovery defensibility | A complete-looking log can still misclassify documents; sampling audit is the only real check, and few teams budget time for it |
| Billable-hour impact | Whether the firm's business model tolerates the gain | A tool that makes work faster can cut revenue in a business that bills by the hour; efficiency and adoption can point opposite ways for the buyer |
| Access-log completeness | Confidentiality control health | A complete log proves access happened, not that it was authorized; firms rarely review it until a breach is already suspected |
| Unauthorized-practice complaint rate | UPL exposure | Near zero early in a product's life is not evidence of safety; enforcement is slow, complaint-driven, and lags growth by years |
| E-discovery defensibility challenge rate | Whether the process survives a court challenge | Low rates in early matters do not predict behavior in a high-stakes matter where opposing counsel has an incentive to look hard |

## Reading

- **The ABA Model Rules of Professional Conduct**, Rules 1.1, 1.6, and 5.5. Read the rule text and at least one state ethics opinion applying it to a specific tool category.
- **The SRA Standards and Regulations (England and Wales).** Read for contrast with the ABA framework on outsourcing and technology competence.
- **Mata v. Avianca, Inc.** (S.D.N.Y., sanctions order 2023). The canonical case of fabricated citations from a generative tool reaching a real filing; read how the sanction was reasoned, not just the headline.
- **The Sedona Conference's principles on e-discovery.** The closest thing this field has to an agreed defensibility standard for process, proportionality, and technology-assisted review.
- **The US Federal Rules of Civil Procedure, Rule 26 and Rule 37(e)** on spoliation sanctions for lost electronically stored information. Read Rule 37(e) before finalizing any retention or auto-deletion default.
- **A bar association's published guidance on generative AI in legal practice**, where one exists in your market (verify current status, since this guidance is being issued and revised quickly).

**Conductor overlay:** this domain sharpens DISCOVER-1 (name the person: the client holds the privilege and bears the UPL risk, not the firm administrator who bought the seat), DEFINE-6 (out of scope: the line between drafting assistance and legal advice has to be written down and read by the sponsor, because the unwritten version is where UPL exposure hides), DESIGN-2 (integrations: e-discovery, document-management, and court e-filing systems are third-party dependencies with their own defensibility and outage behavior), and DESIGN-3 (where privileged material lives, which subprocessors can reach it, and what retention default might destroy something under a litigation hold).

**Templates this bends:** [personas](../../templates/discovery/personas.md) (the client, the lawyer, and the firm's risk function are three people with different exposure), [data-model](../../templates/architecture/data-model.md) (classify privileged material as its own data class with its own access and retention rules), [integrations](../../templates/architecture/integrations.md) (e-discovery, DMS, and court-filing systems carry defensibility and outage behavior as first-class rows), and [business-rules](../../templates/definition/business-rules.md) (the UPL boundary is a business rule with a bar-complaint consequence, not a copy-editing choice).

**Filled in this repo:** [domain-legaltech-data-model.md](../../examples/domain-legaltech-data-model.md) fills the [data-model](../../templates/architecture/data-model.md) template directly for this domain and is the only standalone data-model example in the repository, for Statute & Sage: matter, client, document, privilege tag, per-matter consent for model-vendor access, litigation hold, retention policy and ethical wall entities, with a rule that a document cannot reach the inference endpoint without the matter's consent flag, a hold overriding retention deletion, and privilege classified on its own axis separate from PII, citing ABA Model Rule 1.6 and ABA Formal Opinion 512. For the other three bent templates, [sahulat-personas.md](../../examples/sahulat-personas.md), [harbourgate-integrations.md](../../examples/harbourgate-integrations.md) and [harbourgate-business-rules.md](../../examples/harbourgate-business-rules.md) remain the nearest reading for the persona, boundary-register, and rule-ownership shapes, though none carries a client, a court-filing system, or a UPL boundary.

**Worked example (ILLUSTRATIVE):** a data-model row for a fictional contract-review tool's privileged-material class, in the register-with-columns shape [harbourgate-integrations.md](../../examples/harbourgate-integrations.md) uses for integration boundaries.

| Field | Value |
|---|---|
| Data class | Privileged client communication (attorney work product) |
| Where it lives | Document store, tagged at ingestion by matter ID; never routed through the drafting model's third-party inference endpoint without the per-matter consent flag set |
| Who can reach it | Assigned matter team only, role-checked per request, not per session; the firm's own IT admins are logged separately and excluded from the default access list |
| Subprocessor exposure | Model vendor: none by default. A matter-level consent flag, set by the responsible partner, is required before any document in this class reaches the vendor, and the flag is itself logged as a decision |
| Retention | Governed by the matter's litigation-hold status, not a product-wide default; a hold flag on the matter suspends the class's normal deletion schedule automatically |
| Access-log requirement | Every read logged with requester, matter ID and timestamp; sampling audit run quarterly per the card's own metric on log completeness |
| Business rule | BR-LT-02: WHEN a matter's litigation-hold flag is set THEN block automatic deletion for every document in this class tied to that matter, with no override short of partner sign-off |
