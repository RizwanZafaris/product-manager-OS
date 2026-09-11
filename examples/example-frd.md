# Functional Requirements Document: Orchard Desk Intake

Fills [templates/definition/frd.md](../templates/definition/frd.md). Everything here is invented: Orchard Desk is an ILLUSTRATIVE fictional product from fictional company Juniper Works, and Mira Sen, Omar Bell and Nia Cole are fictional people. All numbers, dates and identifiers are ILLUSTRATIVE and internally consistent.

**Owner:** Mira Sen · **Date:** 2026-04-14 · **Status:** Approved · **Version:** 1
**Parent PRD:** Standalone DEFINE set. The PRD seed and its F-row capabilities are included in the context below.

Juniper Works is an ILLUSTRATIVE fictional company. Orchard Desk is an ILLUSTRATIVE fictional web product for small repair businesses. A customer sends a service request through a public form, the dispatcher reviews it, and the dispatcher assigns it to a technician. Mira Sen is the product manager, Omar Bell is the engineering lead, and Nia Cole is the service-operations lead.

The PRD seed contains three functional capabilities:

| PRD F-row | Capability | Story |
|---|---|---|
| F1 | A customer can submit a repair request with contact details, address, issue description and optional photo | ORCHARD-S1 |
| F2 | A dispatcher can review submitted requests and assign one to an available technician | ORCHARD-S2 |
| F3 | The system sends the customer a confirmation and assignment update | ORCHARD-S3 |

This standalone Orchard Desk FRD has no business-rules register of its own: Orchard Desk is a separate fictional universe from Harbourgate, and the Harbourgate business-rules register's rules (payment authorisation, refunds, reconciliation) do not apply to a repair-intake product. The coverage sheet lists this file as using nothing on the Harbourgate sheet.

## 1. Functional requirements

| ID | Requirement (testable statement) | Parent capability (PRD F-row) | Priority (must / should / later) | Acceptance criteria ID | Notes |
|---|---|---|---|---|---|
| FR-001 | When a customer submits a request with a name, email address, service address and issue description, the system shall validate each required field, create one request record, and display a confirmation containing the request reference | F1 | must | AC-001 | A submission with a missing required field is not created |
| FR-002 | When a customer attaches a photo in an accepted image format no larger than 5 MB, the system shall store the photo with the request and show the photo status as attached | F1 | should | AC-002 | If the file fails validation, the request may still be submitted without the photo |
| FR-003 | When a dispatcher opens the intake queue, the system shall show each unassigned request with its reference, submission time, customer name, service address, issue description and assignment status | F2 | must | AC-003 | Queue results are ordered newest first |
| FR-004 | When a dispatcher selects an unassigned request and an available technician, the system shall assign the request once, record the technician and assignment time, and change the request status to assigned | F2 | must | AC-004 | A second assignment attempt on the same request shall leave the original assignment unchanged |
| FR-005 | After a request is created, the system shall send the customer one confirmation email containing the request reference and a summary of the submitted details | F3 | must | AC-005 | The email send attempt and delivery status are recorded |
| FR-006 | After a request changes from unassigned to assigned, the system shall send the customer one assignment email containing the request reference and the assigned technician's name | F3 | must | AC-006 | No assignment email is sent when an assignment attempt is rejected |
| FR-007 | The dispatcher interface shall display a request's validation, notification and assignment errors without exposing internal error details to the customer | F2 | should | AC-007 | Internal details remain in the operations log |
| FR-008 | The system shall prevent a duplicate request created with the same submission key from creating more than one request record | F1 | must | AC-008 | A repeated submission returns the original request reference |

## 2. Data flows

### Flow: customer request submission

- **Trigger:** A customer submits the Orchard Desk public request form.
- **Steps:**
  1. The customer enters a name, email address, service address and issue description, and optionally selects a photo.
  2. Orchard Desk validates the required fields and the optional photo format and size.
  3. Orchard Desk checks the submission key for a prior completed submission.
  4. Orchard Desk creates one request record and stores the accepted photo, if present.
  5. Orchard Desk returns the request reference and queues a confirmation email.
- **Data in:** Name, email address, service address, issue description, optional photo, submission key, from the customer web form.
- **Data out:** Request reference and submission status to the customer; request record and photo to the Orchard Desk data store; email job to the notification service.
- **Failure behavior:** The customer sees field-level validation messages for invalid input and can correct the form. A rejected photo does not block submission when the other fields are valid. If the data store fails, the customer sees that the request was not submitted and the system creates no partial request record. If the same submission key is repeated after creation, the system returns the original request reference and creates no second record.
- **Requirements covered:** FR-001, FR-002, FR-005, FR-008

### Flow: dispatcher assignment

- **Trigger:** A dispatcher opens an unassigned request and selects an available technician.
- **Steps:**
  1. The dispatcher interface requests the current request and available-technician data.
  2. Orchard Desk verifies that the request is unassigned and that the selected technician is available.
  3. Orchard Desk writes the assignment, assignment time and assigned status as one operation.
  4. Orchard Desk queues one assignment email for the customer.
  5. The dispatcher interface displays the assigned status and technician.
- **Data in:** Request reference, technician identifier and current assignment state, from the dispatcher interface and Orchard Desk data store.
- **Data out:** Assignment record and status to the data store; assignment email job to the notification service; updated request state to the dispatcher.
- **Failure behavior:** If the request is already assigned, the dispatcher sees the existing assignment and the system leaves it unchanged. If the technician is unavailable, the dispatcher sees an assignment error and no assignment is written. If the notification service fails after the assignment is written, the request remains assigned, the failed email is recorded, and the notification job is retryable.
- **Requirements covered:** FR-003, FR-004, FR-006, FR-007

### Flow: confirmation and assignment notification

- **Trigger:** A request-created or request-assigned event is accepted by the notification service.
- **Steps:**
  1. Orchard Desk sends the event with the request reference and permitted customer-facing fields.
  2. The notification service renders the appropriate email template.
  3. The notification service sends the email to the stored customer email address.
  4. Orchard Desk records the notification status and provider response.
- **Data in:** Event type, request reference, customer email address, customer name, submitted summary, and assigned technician name when applicable.
- **Data out:** Email delivery attempt to the email provider; notification status and provider response to the Orchard Desk data store.
- **Failure behavior:** The customer sees no internal provider detail. The system records a failed or delayed notification and retries the job according to the notification contract. A retry uses the event identifier so one event does not create more than one logical notification.
- **Requirements covered:** FR-005, FR-006, FR-007

## 3. Interfaces

| Interface | Direction (in / out / both) | Counterpart system | Data exchanged | Contract detail lives in |
|---|---|---|---|---|
| Public request form | in | Customer browser | Customer details, issue description, optional photo, submission key | Out of scope for this standalone excerpt; no architecture set exists for Orchard Desk |
| Dispatcher queue interface | both | Dispatcher browser | Request list, request details, technician availability, assignment command and result | Out of scope for this standalone excerpt; no architecture set exists for Orchard Desk |
| Request data store | both | Orchard Desk persistence service | Request, photo metadata, assignment, submission key and status records | Out of scope for this standalone excerpt; no architecture set exists for Orchard Desk |
| Notification event interface | out | Orchard Desk notification service | Request-created and request-assigned events, customer-facing fields and event identifier | Out of scope for this standalone excerpt; no architecture set exists for Orchard Desk |
| Email provider | out | External email delivery service | Recipient, template data, message identifier and delivery response | Out of scope for this standalone excerpt; no architecture set exists for Orchard Desk |

## 4. Business rule references

Orchard Desk carries no business-rules register in this standalone excerpt: the PRD seed names no payment, refund or reconciliation constraints for a repair-intake product, and none of these FRs is constrained by a rule outside this document. The closest thing to a business constraint here is procedural, not rule-governed: FR-004's one-time assignment and FR-008's duplicate-submission guard are expressed directly as testable behavior in Section 1, not traced to a separate rule ID.

## 5. Traceability matrix

| FR ID | PRD capability | Story | Acceptance criteria | Test case (filled at BUILD) |
|---|---|---|---|---|
| FR-001 | F1 | ORCHARD-S1 | AC-001 | [To be assigned at BUILD] |
| FR-002 | F1 | ORCHARD-S1 | AC-002 | [To be assigned at BUILD] |
| FR-003 | F2 | ORCHARD-S2 | AC-003 | [To be assigned at BUILD] |
| FR-004 | F2 | ORCHARD-S2 | AC-004 | [To be assigned at BUILD] |
| FR-005 | F3 | ORCHARD-S3 | AC-005 | [To be assigned at BUILD] |
| FR-006 | F3 | ORCHARD-S3 | AC-006 | [To be assigned at BUILD] |
| FR-007 | F2 | ORCHARD-S2 | AC-007 | [To be assigned at BUILD] |
| FR-008 | F1 | ORCHARD-S1 | AC-008 | [To be assigned at BUILD] |

**PRD capabilities with zero FRs:** none
**FRs with zero acceptance criteria:** none

---

### Worked micro-example (illustrative, invented)

> **FR-001:** When a customer submits a request with a name, email address, service address and issue description, Orchard Desk validates the fields, creates one request record and returns a request reference. Parent: F1. Priority: must. AC: AC-001.
>
> **Flow "customer request submission", failure behavior:** if a required field is invalid, the customer sees a field-level message and no request is created. If the data store fails, the customer sees that the request was not submitted and the system creates no partial record. If the same submission key is sent again, Orchard Desk returns the original request reference and creates no duplicate record.

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every FR is testable by a stranger: observable behavior and measurable bounds are stated in each requirement. Photo size, accepted image format, one-record behavior, status changes and notification outcomes are explicit.
- [x] Every FR traces to a PRD capability; both zero-lists in section 5 say "none" or carry an owner and date. All eight FRs trace to F1, F2 or F3, and both zero-lists say "none".
- [x] Every must FR has an acceptance criteria ID. FR-001, FR-003, FR-004, FR-005, FR-006 and FR-008 are must requirements and each has an acceptance criteria ID.
- [x] Every flow states its failure behavior. The customer submission, dispatcher assignment and notification flows each state user-visible and system behavior on failure.
- [x] Every interface row names its counterpart and its contract location. All five rows name a counterpart and link to an API or integration contract.
- [x] No business-rules register applies to this standalone excerpt (see Section 4); this gate item is not applicable. Orchard Desk names no payment, refund or reconciliation constraints, and no FR is traced to a rule ID outside this document.

Signed at Gate 2, 2026-04-14: Mira Sen, product manager; Omar Bell, engineering lead; Nia Cole, service-operations lead.
