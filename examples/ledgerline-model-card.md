# Model Card: Ledgerline Expense Copilot

Fills [templates/ai/model-card.md](../templates/ai/model-card.md). Everything here is ILLUSTRATIVE and invented: Ledgerline, the Expense Copilot, its model vendor, its people, its customers, and every performance result are fiction carried from the [journey data sheet](ledgerline-journey.md) and the [coverage sheet](ledgerline-coverage-sheet.md) so the add-on's Gate 5 claims can be checked. See the [examples index](README.md).

**Owner:** Priya Nair, engineering lead · **Contact for questions:** launch-team channel · **Signed:** 2026-11-06 · **Last updated:** 2026-12-11

## 1. Intended use

- **Extract receipt fields:** The pinned document model extracts merchant, date, amount and currency from a single receipt image or forwarded receipt, leaving unknown fields blank and flagged rather than guessing.
- **Suggest a category:** The system suggests a category and shows the matching line from the customer account's own policy.
- **Assemble a draft:** The system assembles a draft expense line item and report for the filer to review, edit or reject.
- **Flag uncertainty:** Fields and category suggestions below the model confidence threshold are flagged for reviewer attention.
- **Who it serves:** Customer-account filers, finance reviewers and account administrators using Ledgerline Expenses.

**Model and version pinned:** Ledgerline's model vendor document model, `docmodel-2026-09-30`
**Card owner:** Priya Nair · **Contact for questions:** launch-team channel · **Last updated:** 2026-12-11

**Explicitly out of scope:**

- **Auto-submission:** The model must not submit a report. The filer remains responsible for reviewing and pressing submit.
- **Judging whether an expense is legitimate:** The model does not decide whether an expense is legitimate, compliant or fraudulent. It abstains from that judgment and leaves it to the filer and reviewer.
- **Multi-receipt photos:** The model is not trusted to process a photo containing multiple receipts. It abstains rather than producing a combined draft.
- **Non-English receipts:** The model is not trusted to extract non-English receipts. It abstains and flags the item for review. German-language receipts are specifically below the field-accuracy threshold.

## 2. Known limitations and failure modes

| Limitation or failure mode | How it shows up for the user | Source (path + section) |
|---|---|---|
| Accuracy varies by customer receipt mix | On the internal labeled receipt set, 86% of extracted fields were accepted without edit. On the customer add-on window, 87% were accepted without edit. | [ledgerline-journey.md](ledgerline-journey.md), data sheet N21 and N66 |
| Reviewer-caught extraction errors remain present | Reviewers caught 2.1 errors per 100 drafted reports internally and 2.4 errors per 100 drafted reports in the customer add-on window. | [ledgerline-journey.md](ledgerline-journey.md), data sheet N24 and N67 |
| German-language receipts perform below the eval threshold | Wrenfield Labs reached 61% approval on 33 drafted reports, mostly German-language receipts. The German-language eval set scored 71% field accuracy against the 90% threshold. | [ledgerline-journey.md](ledgerline-journey.md), data sheet N45 and N83, risk R3; [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md), LC20 and LC21 |
| German receipts with comma decimals can produce materially wrong amounts | The red-team test found an amount read a hundred times too large on 4 of 25 German receipt attempts. The issue was fixed and re-attacked, but German receipts remain out of scope because the eval result is below threshold. | [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md), LC28, RT-07 |
| Multi-receipt photos are not a supported input | The model abstains rather than attempting to separate, combine or assign multiple receipts in one image. | [ledgerline-journey.md](ledgerline-journey.md), shared story LEDGERLINE-S2 and PRD functional scope; [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md), AI overlay |
| Legitimacy judgments are not a model capability | The output is a draft and a policy match, not a decision that an expense is legitimate. The filer and reviewer must make that judgment. | [ledgerline-journey.md](ledgerline-journey.md), shared story LEDGERLINE-S3; [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md), AI overlay |
| The model must not be used to submit reports | Auto-submission is blocked by the human approval flow. A request to auto-submit was held in red-team testing, and no submit tool exists. | [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md), LC28, RT-05; human approval gate design in the coverage artifact map |
| A customer policy instruction can be adversarial input | An instruction planted in a customer's own policy document was followed on 3 of 20 attempts before the quoted-data fix. The fixed version was held on re-test, but policy text remains treated as untrusted data. | [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md), LC28, RT-02 |

## 3. Performance summary

- **Headline result:** EVAL-2, the customer-policy set of 360 English-language receipts, scored 92% field accuracy and 86% category match with the current policy-match prompt version. The category-match result clears the 85% threshold, and field accuracy clears the 90% threshold. [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md), LC19 and LC21.
- **Variance across segments:** Internal English-language receipts scored 86% of fields accepted without edit, compared with 87% in the customer add-on window. Reviewer-caught errors were 2.1 per 100 drafted reports internally and 2.4 per 100 drafted reports in the customer add-on window. Wrenfield Labs was at 61% approval on 33 drafted reports, mostly German-language receipts. The German-language eval set scored 71% field accuracy against the 90% threshold. [ledgerline-journey.md](ledgerline-journey.md), N21, N24, N45, N66 and N67; [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md), LC20 and LC21.
- **Segments not measured yet, stated plainly:** Multi-receipt photos are not measured as an in-scope capability because the model abstains. Legitimacy judgments are not measured as a model capability because they are out of scope. Non-English receipt performance beyond the German-language eval set is not measured.

## 4. Data provenance

The provider is not named in this story. Ledgerline pins the provider's document model as `docmodel-2026-09-30`; the available product record identifies the model and its prompt changes but does not disclose training or fine-tuning data beyond the provider's document-model description. At inference time, the customer receipt, extracted fields and the customer's own policy excerpt reach the model for drafting and policy matching. The accepted customer DPA terms include 30-day prompt retention and the existing no-training clause; approval-gate audit records are retained under the finance-records rule, with the customer-account confirmation still owned by the legal lead. [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md), LC16, LC17, LC25, LC27 and LC31.

## 5. Update policy

- **What triggers a card update:** A change to the pinned model, a prompt version change, a new eval result, a new red-team finding, a change to an abstention boundary, or a material change to what customer data reaches the model.
- **Who updates it:** Priya Nair · **Review cadence even without changes:** Review at each add-on Gate 5 review and whenever the launch team reopens model scope.
- **Where old versions live:** The signed card and later updates remain in the repository history. No separate version archive is specified; the date in this header identifies the current card.

## Exit gate

- [x] Every capability claim in section 1 has a matching evaluation or product evidence row. Extraction and category matching use EVAL-1 and EVAL-2, while drafting and confidence flags are part of the customer stories and overlay records.
- [x] The out-of-scope list exists and names at least the uses the team already declined. It names auto-submission, legitimacy judgment, multi-receipt photos and non-English receipts.
- [x] Every limitation row cites a source document by path.
- [x] Performance is reported with segment variance, including internal results, customer-window results, Wrenfield's German-language result and the German eval result.
- [x] The pinned version string matches the evaluation record exactly: `docmodel-2026-09-30`.
- [x] A contact is named that outsiders can actually reach: launch-team channel.

Signed at the add-on Gate 5, 2026-11-06: Priya Nair, engineering lead. Updated 2026-12-11 with EVAL-3 and the German-language result.
