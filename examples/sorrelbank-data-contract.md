# Data Contract: Sorrelbank Market order lifecycle events

Fills [templates/architecture/data-contract.md](../templates/architecture/data-contract.md). Everything here is invented for this standalone example: Sorrelbank Market is a fictional online grocery delivery business, its teams and people are fictional, and every volume, percentage, target, name and date is ILLUSTRATIVE, not drawn from any real company or dataset. There is no journey or data sheet behind it. See the [examples index](README.md).

**Dataset or stream:** topic `orders.lifecycle.v2` on the company event bus, landed hourly to the warehouse table `events.order_lifecycle_v2` · **Producer team:** Orders · **Contract owner:** Tomasz Reyes, Product Manager, Orders
**Version:** 2.3 · **Status:** Approved at Gate 3 with two open items (sections 6 and 7) · **Date:** 2026-10-27
**Machine-readable contract:** `contracts/order-lifecycle/v2.yaml` in the orders service repository, not tracked in this repository

Why now: this contract went to the Gate 3 review of the Orders checkout rebuild, which changes what `order_total_minor` means and so needs a version 3 (section 7). Before it, the stream had four known consumers and no written promise. The September incident in section 8 is why it now has one.

## 1. Purpose and grain

- Business process this records: an order moving from placement to delivery, cancellation or refund
- Grain, one row or event is: one committed state change of one order in the order service. An order produces between two and seven events
- Primary or deduplication key: `event_id`. Events for one order share `order_id`, which is also the partition key
- Where it lives: topic `orders.lifecycle.v2`, 12 partitions keyed by `order_id`, events for one order in commit order; warehouse table `events.order_lifecycle_v2`, partitioned by the UTC hour of `event_time`
- Delivery guarantee (streams): at least once. Consumers of the topic deduplicate on `event_id`; the warehouse table is deduplicated at landing
- Deliberately excluded: staff test orders, orders from the wholesale channel (their own contract), and line items (contract `orders.lines.v1`)

## 2. Consumers

| Consumer team | Named contact | What they use it for | Fields depended on | Decision it feeds, and when | Notified through |
|---|---|---|---|---|---|
| Finance systems | Adaeze Lund, Finance Systems Lead | Daily revenue recognition and reconciliation with the payments ledger | `event_type`, `event_time`, `order_id`, `currency`, `order_total_minor`, `refund_amount_minor` | The daily close, from 05:00 UTC; the month-end close | `#data-orders-contract` and direct message |
| Demand forecasting | Priya Haldane, Data Scientist, Supply | Next-day purchase orders to suppliers, per store | `event_type`, `event_time`, `store_id`, `item_count`, `delivery_slot_start` | Purchase orders sent at 04:00 UTC daily | `#data-orders-contract` and direct message |
| Customer messaging | Ben Oyelaran, Engineering Manager, Messaging | Real-time "on its way" and "delivered" text messages | `event_type`, `event_time`, `order_id`, `customer_ref` | Each message, within a minute of the change | `#data-orders-contract`, and on-call to on-call for lag |
| Loyalty | Marta Quintero, Product Manager, Loyalty | Points awarded on delivered orders | `event_type`, `customer_ref`, `order_total_minor`, `currency` | The nightly points run at 02:00 UTC | `#data-orders-contract` and direct message |
| Marketing attribution, found by the access review of 2026-10-12 | Callum Ferreira, Analyst, Growth | Weekly attribution model, from the warehouse table | `event_type`, `event_time`, `customer_ref`, `order_total_minor`, `delivery_area_code` | The Monday channel budget review | `#data-orders-contract` and direct message, contact confirmed 2026-10-14 |

The fifth row is the reason section 2 is read against access logs and not against memory. Nobody on the Orders team knew the attribution notebook existed until the review found its service account reading the table every Sunday night.

## 3. Schema and semantics

| Field | Type | Nullable | Semantics: meaning, unit, time zone, how derived, what null means | Allowed values or range | PII class | Since version |
|---|---|---|---|---|---|---|
| `event_id` | string (UUID) | No | Id of this event, set when the state change commits. Repeated on redelivery, which is what makes it the deduplication key | UUID | none | 1.0 |
| `event_type` | string, enum | No | The state the order entered | `order_placed`, `order_paid`, `order_picked`, `out_for_delivery`, `delivered`, `cancelled`, `refunded` | none | 1.0; `refunded` since 2.1 |
| `event_time` | timestamp | No | When the state change committed in the order service, UTC. Not when the event was emitted or received | Equal to or earlier than `emitted_time` | none | 1.0 |
| `emitted_time` | timestamp | No | When the producer published the event, UTC | Equal to or later than `event_time` | none | 2.0 |
| `order_id` | string | No | The order's id in the order service, stable for the life of the order | `o_` followed by 12 digits | none | 1.0 |
| `customer_ref` | string | No | Pseudonymous customer key: a keyed hash of the account id, stable across one customer's orders, not reversible without the key the Orders team holds | 64 hexadecimal characters | indirect | 2.0 |
| `store_id` | string | No | The store that fulfils the order | An id in the stores reference table | none | 1.0 |
| `currency` | string | No | Currency of every amount in this event, as an ISO 4217 code | `EUR`, `SEK` | none | 1.0 |
| `order_total_minor` | integer | Yes | Gross order value in minor units: items after promotions plus the delivery fee, excluding tips, before any refund. Refunds arrive as separate `refunded` events and are never netted here. The value on `order_paid` is authoritative; the value on `order_placed` can change at payment. Null on `refunded` events | 0 to 5,000,000 | none | 1.0; meaning changes in 3.0 (section 7) |
| `refund_amount_minor` | integer | Yes | Amount refunded by this event, minor units, positive. Null on every event type except `refunded` | 1 to the order's authoritative `order_total_minor` | none | 2.1 |
| `delivery_slot_start` | timestamp | Yes | Start of the booked delivery window, UTC. Null for click-and-collect orders, which have no slot | Within 14 days after `event_time` | none | 1.0 |
| `delivery_area_code` | string | Yes | The delivery zone Sorrelbank assigns, covering a few thousand households, never an address. Null for click-and-collect | `Z` followed by three digits | indirect | 2.0 |
| `item_count` | integer | No | Item units in the order at the time of the event; a multipack counts once | 1 to 400 | none | 1.0 |
| `schema_version` | string | No | The contract version the producer wrote against | `2.0` to `2.3` | none | 2.0 |

Enumerations are declared: `event_type` is open, so a new value may arrive after 30 days' notice and a consumer must ignore an event type it does not recognise rather than fail. `currency` is closed, so a new currency is a breaking change.

## 4. Service levels

| Service level | Indicator, exactly | Target | Window | Measured by | Breach pages |
|---|---|---|---|---|---|
| Freshness | Minutes from the end of an hour to that hour's partition being queryable in the warehouse | 45 minutes or less for at least 99% of partitions | Rolling 28 days, 672 hourly partitions | Monitor `orders_lifecycle_freshness` | Orders data on-call |
| Completeness | Distinct `order_placed` events per UTC day, divided by orders created in the order service database that day, test orders excluded from both | At least 99.8% every day, and never above 100% | Daily | Check QC5 | Orders data on-call; Finance told before 05:00 UTC when missed |
| Stream lag (streams only) | 95th percentile, per five-minute window, of the time an event becomes readable minus its `event_time` | 60 seconds or less in at least 99.5% of windows | Calendar month | Monitor `orders_lifecycle_lag_p95` | Orders platform on-call |

The readings at this gate, all ILLUSTRATIVE:

- Freshness, 28 days to 2026-10-25: 667 of 672 partitions landed within 45 minutes, 99.3%. The target allows 1% of 672, which is 6.72, so at most 6 late partitions; 5 were late.
- Completeness, 2026-10-24: 18,391 distinct `order_placed` events against 18,412 source orders, 99.89%. The 21 missing events came from one producer restart; they were replayed and the partition restated on 2026-10-25.
- Stream lag, October to 2026-10-26: 7,461 of 7,488 five-minute windows at 60 seconds or less, 99.64%.

## 5. Quality checks

| Check id | Type (schema, uniqueness, null, range, ordering, reconciliation, distribution) | Rule | Runs when | Blocks publication or alerts | Reader or owner |
|---|---|---|---|---|---|
| QC1 | Schema | Every event validates against the registered v2 schema | On write | Blocks: a failing event goes to the dead-letter topic and never reaches a consumer | Orders platform on-call |
| QC2 | Uniqueness | `event_id` unique within 7 days. Duplicates are dropped at landing; more than 0.5% of an hour's events being duplicates alerts | Hourly | Alerts | Orders data on-call |
| QC3 | Null | No nulls in a non-nullable field. `refund_amount_minor` is present on `refunded` events and null on every other type | Hourly, on landing | Blocks: the partition is withheld from the certified view | Orders data on-call |
| QC4 | Ordering | Per order, `event_time` never decreases from placed to paid to picked to out for delivery to delivered. More than 0.1% of a day's orders in violation alerts | Daily, 03:00 UTC | Alerts | Tomasz Reyes reads the daily summary |
| QC5 | Reconciliation, count | Completeness as defined in section 4 | Daily, 04:15 UTC | Blocks the day's certified flag | Orders data on-call |
| QC6 | Reconciliation, value | Sum of `order_total_minor` on `order_paid` events per day and currency, against the payments ledger's captured total, within 0.1% | Daily, 04:15 UTC | Blocks the day's certified flag | Adaeze Lund and Orders data on-call |
| QC7 | Distribution | Hourly `order_placed` count outside 60% to 140% of the same hour's average over the previous four weeks | Hourly | Alerts | Orders data on-call |

Demand forecasting reads uncertified hourly partitions by choice: its 04:00 UTC run comes before QC5 and QC6 finish at 04:15. It accepted that in its sign-off below, and it is the only consumer that does.

## 6. Personal data and access

- Fields classed direct or sensitive: none. `customer_ref` and `delivery_area_code` are indirect: joined with `event_time` they can single out a household, so neither may be joined to a dataset holding names or addresses outside the Orders team
- Lawful basis or policy reference: the Orders privacy impact assessment, PIA-2026-07, in the product workspace, not tracked in this repository
- Retention: topic 7 days; warehouse table 25 months, set by the finance audit requirement; consumer copies no longer than the warehouse table
- Access: the warehouse table through the `orders-lifecycle-readers` group, granted by the contract owner on a ticket that names the use. Reads are logged and the group is reviewed quarterly; the 2026-10-12 review found the fifth consumer
- Consumer obligations: no attempt to reverse `customer_ref`; no sharing outside Sorrelbank; rows deleted from consumer copies within 30 days of a deletion notice
- Erasure path: on an erasure request the order service deletes the customer's key mapping and publishes a deletion notice to every consumer in section 2. [OPEN: whether deleting the mapping while `customer_ref` rows stay in place satisfies erasure for this dataset; Ruth Mensah-Kerr, privacy counsel, owns the answer, due 2026-11-30]

## 7. Versioning and change policy

- Version scheme: MAJOR for breaking, MINOR for additive. Current: 2.3
- Breaking changes, as this contract defines them: removing or renaming a field; changing a type; making a non-nullable field nullable; changing a field's meaning, unit or time zone under the same name; changing the grain or the deduplication key; adding a value to a closed enum or removing a value from any enum; lowering a target in section 4; weakening the delivery guarantee
- Notice period for a breaking change: 90 days from announcement to removal of the old version
- Dual publication: yes, the old and new topics and tables are both live for the whole notice period
- Notice for additive changes: 14 days · for a new value in an open enum: 30 days
- How notice is given: a dated entry in the contract changelog in the orders service repository, plus a direct message to each named contact in section 2, with acknowledgement recorded below
- Who approves a breaking change: Tomasz Reyes; any change that shortens a notice period also needs Nnamdi Calloway, Head of Data
- Emergency exception (security or legal): Nnamdi Calloway may shorten the notice, never below two working days, except to stop an active leak of personal data, when notice is same-day

| Change | Version | Announced | Old version available until | Consumers acknowledged (k of n) |
|---|---|---|---|---|
| `refund_amount_minor` added, and `refunded` added to `event_type` | 2.1 | 2026-03-02 | Not applicable, additive | 4 of 4 |
| `order_total_minor` changes meaning: the delivery fee moves to a new field, `delivery_fee_minor`, so the total becomes items after promotions only | 3.0 | 2026-10-15 | v2 removed no earlier than 2027-01-13, 90 days after the announcement; v3 published alongside it from 2026-11-16 | 4 of 5 |

The 3.0 row is a breaking change although no field is renamed and no type changes. A consumer still reading the old meaning would compute every figure without error and be wrong by the delivery fee on every order.

[OPEN: Loyalty has not acknowledged the 3.0 notice. Points are computed from `order_total_minor`, so if Loyalty does not migrate, every delivered order's points drop by the delivery fee once v2 is removed, and nothing fails. Tomasz Reyes owns chasing Marta Quintero; acknowledgement is needed by 2026-11-16, when v3 starts publishing.]

## 8. Incident path

- Detected by: QC1, QC3, QC5 and QC6, which block; QC2, QC4 and QC7, which alert; the freshness and lag monitors
- Producer on call: the Orders data on-call rotation, paged within 5 minutes of a blocking check failing
- Consumers told within: 30 minutes of detection, in `#data-orders-contract` and by direct message to each named contact. Customer messaging is also paged on-call to on-call when stream lag breaches, because its impact reaches customers first
- What consumers should do meanwhile: Finance holds the daily close until the certified flag appears and escalates at 07:00 UTC; Demand forecasting uses the previous day's certified volumes with its own adjustment; Customer messaging drops any "on its way" message more than 15 minutes old rather than sending it late; Loyalty delays the nightly points run by up to 24 hours
- Restatement: corrected partitions are republished with `restated = true`, and a row in `events.order_lifecycle_corrections` names the partition, the reason and the change in row count. The channel post names the restated partitions
- Review: a postmortem in [incident-postmortem](../templates/operate/incident-postmortem.md) form within 5 working days for any breach of section 4

The incident that produced this contract, ILLUSTRATIVE: on 2026-09-03 a producer release began writing the emission time into `event_time` for `out_for_delivery` events. No check failed, because the field kept its type and its nullability. Customer messaging noticed six hours later, when "delivered" messages began arriving before "on its way". The postmortem's first action was the meaning column in section 3; its second was QC4.

## 9. What this contract does not promise

- Exactly-once delivery on the topic. Delivery is at least once; deduplicate on `event_id`
- Line items, per-item prices, or any address
- History beyond 25 months in the warehouse, or beyond 7 days on the topic
- A final total on `order_placed`. The authoritative total is on `order_paid`
- Wholesale channel orders

## 10. How this contract passes while consumers still get hurt

Three rows of the template's table applied to this contract; the others were checked at the review on 2026-10-27 and did not.

| Failure | The tell | What happened here |
|---|---|---|
| Silent change of meaning | A definition changes while the field name and the MAJOR version stay | The 2026-09-03 incident, and the reason version 3.0 is a MAJOR bump with a 90-day window although no field is renamed |
| Unlisted consumers | Access logs show readers who are not in section 2 | Marketing attribution, found 2026-10-12 and added before the 3.0 notice went out |
| Notice nobody received | Consumers learn of a change from a broken job | Not yet, and the Loyalty acknowledgement in section 7 is the open risk of it |

## Consumer sign-off

| Consumer team | Name | Reviewed version | Verdict and conditions | Date |
|---|---|---|---|---|
| Finance systems | Adaeze Lund | 2.3, and the 3.0 draft | Accepted, on condition that QC6 stays blocking | 2026-10-22 |
| Demand forecasting | Priya Haldane | 2.3 | Accepted; reads uncertified hourly partitions by choice (section 5) | 2026-10-23 |
| Customer messaging | Ben Oyelaran | 2.3 | Accepted | 2026-10-21 |
| Marketing attribution | Callum Ferreira | 2.3 | Accepted, and agreed not to join `delivery_area_code` to the customer database | 2026-10-24 |
| Loyalty | Marta Quintero | Not reviewed | [OPEN: see section 7] | |

## Exit gate

- [x] Grain and the deduplication key are each stated in one sentence
- [x] Every consumer row names a person, the fields they depend on, and the decision the data feeds (five rows, one found by access review)
- [x] Every field has a type, a nullability, a meaning that is more than its name, and a PII class that matches the data model (the Orders data model, in the product workspace)
- [x] Freshness and completeness each have an indicator, a numeric target, a window, and the query or monitor that measures them
- [x] Every quality check says whether it blocks publication or alerts, and who reads the alert
- [x] The breaking-change list includes changes of meaning, and the notice period is a number of days (90)
- [x] The incident path names who is paged, how soon consumers hear, what they do meanwhile, and how restated data is flagged
- [x] Section 9 lists at least one thing the contract does not promise
- [x] At least one consumer has signed, and every open item carries an owner and a date (four of five signed; the erasure question and the Loyalty acknowledgement are open with owners and dates)
- [x] Freshness and completeness alerts appear in the Orders observability spec, and each consumer appears in the integrations register (both in the product workspace)

Signed: Tomasz Reyes, Product Manager, Orders, 2026-10-27
