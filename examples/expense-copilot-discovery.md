# Discovery Document: Expense Copilot

Produced with [templates/discovery/discovery-document.md](../templates/discovery/discovery-document.md). Fictional product, fictional company, every number invented for illustration. See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Status:** Decided · **Date:** 2026-08-14

## Trigger

Support tickets tagged "expenses" at Fernwood Software (fictional, about 900 employees) tripled over two quarters after the company switched travel agencies. The finance lead asked engineering for "a better form". Before building a better form, we ran discovery to find out what problem the tickets actually describe.

## Target user

Individual contributors who travel one to four times a quarter and file their own expense reports. Secondary: the three finance reviewers who approve every report. Not in scope: executive assistants filing on behalf of others, a distinct workflow we deliberately parked.

## Pain

Filing a report takes real evening time and still bounces. From twelve interviews (eight filers, four finance reviewers, held 2026-07-20 to 2026-08-01):

- Filers re-type data that already exists on the receipt: merchant, date, amount, currency. Ten of twelve named re-typing as the worst part, unprompted.
- Roughly a third of reports bounce at review, and the top bounce reason is a category mismatch against a policy the filer has never read.
- Reviewers spend most of their pass on mechanical checks (totals, categories, receipt attached), not on judgment.

Cost of inaction, estimated with the finance lead from her own team's time logs: about 30 reviewer-hours a month on mechanical checks, plus filer frustration we heard in every single interview. Estimate, not a measurement; she signed it as good enough to justify discovery.

## Hypothesis

If the system reads the receipt and drafts the report (merchant, date, amount, currency, suggested category with the policy line it matched), filers will submit in one sitting and bounce rates will fall, because the two main bounce causes, typos and category mismatches, are exactly what a draft can get right. The filer stays the author: nothing is submitted without their review, which also keeps accountability where the policy puts it.

## Success signal

Two signals, agreed with the finance lead on 2026-08-12:

1. First-submission approval rate for reports drafted by the copilot rises from the current 62% baseline (her figure, from the finance system) toward 80%.
2. Filers choose it: at least half of eligible reports use the draft flow within two months of launch, without a mandate.

If drafts are heavily corrected but approval does not move, the hypothesis is wrong even if usage is high, and we will say so at the metrics review.

## Go or no-go

**GO.** Decided 2026-08-14 by Maya Chen (product) and Daniel Okafor (finance lead). Rationale: the pain is verbatim in ten of twelve interviews, the cost is signed by the budget owner, and the hypothesis is falsifiable with numbers the finance system already produces. Proceed to DEFINE; the PRD is [expense-copilot-prd.md](expense-copilot-prd.md).

Known risks carried forward: extraction quality on crumpled or foreign-language receipts is unproven, and the model vendor question (training on our data, retention) is unanswered. Both are opened as gaps in the PRD rather than resolved by optimism here.
