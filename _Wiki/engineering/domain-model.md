---
title: Domain model
status: draft
updated: 2026-10-17
---

# Domain model

Authority: [updated specification, SRC-003](../raw/2026-10-17-updated-specification.md), [ADR-0004](../decisions/adr-0004-updated-product-baseline.md). This records the supplied model faithfully, not an implemented database schema/final API contract. At `055275e`, [main.dart](../../lib/main.dart) contains only widgets and an integer counter.

## Supplied expense fields

| Field | Source type | Required/default | Remaining detail |
| --- | --- | --- | --- |
| `owner` | Text | Required | Stable authenticated owner mapping; backend derives/checks ownership |
| `date` | Timestamp | Required | Purchase timestamp format, timezone/offset, date-only input conversion |
| `seller` | Text | Optional | Missing/null/empty and validation |
| `title` | Text | Optional | Missing/null/empty and validation |
| `category` | Text | Required | Stable category ID versus label, ownership, rename/delete |
| `type` | `single` or `concurrent` with `{info}` | Requiredness/default unspecified | Literal/union encoding, `info` structure, mapping to recurrence |
| `description` | Text | Optional | Missing/null/empty and validation |
| `amount` | Float | Optional | Precision/rounding, refunds/range, null/save/aggregation policy |
| `currency` | Text | Required; default euro | Literal `euro` versus `EUR` or another convention; supported currencies |
| `created_at` | Timestamp | Default `now()`; requiredness unspecified | Assigning component/clock, timezone, immutability, serialization |
| `deleted_at` | Timestamp | Optional | Deletion meaning, visibility, restore/purge, summary behavior |

The source supplies no expense record ID; agree its creation/representation before edit/delete APIs (Q-19). Do not silently rename `concurrent` to `recurring` in shared payloads. The `info` placeholder defines neither a recurrence schema nor a scheduler.

## Money, time, and deletion tensions

The updated requirement explicitly says optional **float** `amount`. The bootstrap wiki recommended exact decimal/integer-minor-unit representation; that was engineering advice, not an approved schema. Retain the supplied type. **Open Q-08:** agree wire/storage/aggregation representation and precision/rounding; do not silently substitute another type. Missing amount is not zero; its budget/chart/summary contribution is undefined.

`date` is explicitly a timestamp, settling the old date-versus-timestamp question at source-type level. Format, timezone, week starts, period boundaries, and partial-period comparison remain open (Q-09). Default `now()` does not establish server-side assignment; server-owned creation metadata is a recommendation to confirm.

`deleted_at` suggests soft deletion, but its behavior is not defined. Excluding deleted records from views/totals, restoration, retention, and recurrence/alert effects remain proposals (Q-19).

## Other concepts

| Concept | Current direction | Open details |
| --- | --- | --- |
| User/device identity | Stable smartphone ID/fingerprint replaces Google sign-in | Generation/storage, backend proof/session, reinstall/device change, multiple devices |
| Category template | Four/six-category starting sets or from scratch | Labels/versioning, customization milestone |
| User category | Required expense category text; editable setup | ID/label, ownership, hierarchy/granularity, historical rename/delete |
| Import draft | Reviewable OCR values; shared manual form | Transient/persisted state, confirmation boundary, email review |
| Receipt attachment | Gallery image for backend extraction | Formats/limits, retention/access, additional camera route |
| Email delivery | System-generated address; periodic sync in 3.0 | Provisioning timing, provider/deduplication, retry/retention |
| Recurrence | `single` / `concurrent {info}`; recurring input in narrative | Mapping, frequency/start/end, definitions versus occurrences, optional cron |
| Budget | Budget creation/threshold alerts in 4.0; category alerts optional | No fields supplied; owner, currency, period, threshold/notification semantics |

## Proposed invariants to agree and verify

- Derive ownership from a verified backend identity/session. A device ID or `owner` string alone is not proof.
- Verify ownership of categories, expenses, imports, files, and budgets. Prefer stable references for renamed categories.
- Preserve missing values and distinguish drafts from saved expenses; user corrections take precedence over extracted suggestions.
- Define deduplication separately for uploads, saves, forwarded emails, and generated recurrence occurrences.
- Make summary/budget totals reproducible under agreed null amount, rounding, currency, timestamp, deletion, and recurrence rules. Additional currencies are optional; conversion is unspecified.

These are recommendations, not implemented safeguards. See [contracts](contracts.md), [flows](../product/user-flows.md), [questions](../open-questions.md), and [AI/data](ai-and-data.md).
