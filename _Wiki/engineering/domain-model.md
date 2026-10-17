---
title: Domain model
status: active
updated: 2026-10-17
---

# Domain model

Current declared model: [SRC-004](../raw/2026-10-17-frontend-handoff.md), [ADR-0005](../decisions/adr-0005-api-handoff-baseline.md). Frontend expense/category/profile parsers now exist under lib/features; backend UserResponse and the users/{uid} repository are implemented. Category/expense/rule persistence is still planned. [Backend data specs](../../backend/specs/02-data-model.md) propose cents/Decimal storage, names/IDs, Rome recurrence anchors and caps; separate human acceptance of those internally adopted proposals is not evidenced here. See [ADR-0006](../decisions/adr-0006-integrated-client-and-backend.md). The fields below remain the target API model, not a claim all backend models exist.

## Expense

| Field | Current declared meaning / mutation boundary |
| --- | --- |
| id | UUIDv4; client generates/reuses for create/scan retries; server can generate if omitted; immutable |
| owner | Firebase UID in responses, derived by backend from verified token; never sent by client |
| date | Purchase ISO timestamp; offsets accepted, UTC Z returned; patchable |
| seller, title, description | Optional text, response null when absent; PATCH null clears |
| category | User category ID, not a display label; must exist and not be archived; patchable |
| type | single or recurring; creation produces single; conversion uses make-recurring, never PATCH type |
| recurrence | Null for single; recurring refers to rule via rule_id |
| amount | Optional/null; when supplied positive, at most 1,000,000, at most two decimals; patchable |
| currency | EUR only; source lists create currency as required with default EUR; omission behavior needs missing OpenAPI |
| source | manual or scan; immutable; no email value in current contract |
| scan_details | Null for manual; scan metadata described below, not a retained image |
| needs_review | Review flag; PATCH false after human review; saved does not mean fully reviewed |
| created_at, updated_at | Server response UTC timestamps; not client-editable |
| deleted_at | Soft-delete metadata; always null on returned expenses because deleted items are excluded |

Response optional fields are returned as null, not omitted. PATCH cannot change id/owner/type/source/timestamps. Never infer backend ownership from a payload field or model text.

`scan_details` includes document_type (receipt/invoice/payment_screenshot/other), items (description, quantity, unit_price, total), vat_total, vat_number, and payment_method; metadata fields can be null. The source example illustrates shape, not proven extraction quality. Images are declared not stored by the backend; provider retention remains unknown.

## Money and summaries

The wire type is a JSON number with the stated precision/range; no database arithmetic/storage type is provided. Exact internal arithmetic/rounding is a verification concern, not permission to alter the wire contract. Missing amount is not zero; summaries exclude it from totals and expose uncounted.

Monthly/yearly endpoints compute periods in Europe/Rome and return UTC from/to, total/count/uncounted/by_category; yearly includes 12 by_month entries with zeros. Category percentages are informational and need not sum to 100. Do not compute totals from paginated lists. Count interpretation, zero-total percentages, and detailed rounding remain questions.

## Category and catalog

Category: id, name, optional icon/color free strings, catalog_id, is_other. IDs are server generated. Active categories appear in category lists; historical archived categories can still appear in summaries when they have expenses.

Catalog IDs: groceries, dining_out, transport, housing, bills, health, entertainment, shopping, travel, education, subscriptions. Presets essential_4 and complete_6 are onboarding shortcuts; source lists their content in [contracts](contracts.md).

Choose at least two catalog/custom items; Other is added automatically. Maximum 30 and case-insensitive name uniqueness are declared; max counting with Other needs confirmation. Other may be renamed, cannot be deleted, and is fallback for scan classification. Deleting a referenced category is blocked by non-deleted expenses or active recurring rules.

## RecurringRule and occurrence lifecycle

Rule response: id, frequency (weekly/monthly/yearly), start timestamp, optional inclusive local-date end_date, active, and template (seller/title/description/category/amount/currency). IDs are server generated. Conversion makes the existing expense the first recurring occurrence and creates missed occurrences through today.

- PATCH of an expense affects that occurrence only.
- PATCH of a rule changes seller/title/description/category/amount/end_date/active for occurrences not yet created; frequency/start are immutable.
- Deleting a rule sets active false; existing expenses remain. Deleting an occurrence does not stop a rule.
- Reactivation skips the paused period. Monthly 31st clamps to month end without shifting the original anchor permanently.
- Idempotent sync creates missing occurrences, returns created/rules_processed/has_more; call again while has_more.
- Timezone, leap-year behavior, inactive-rule listing, and edge cases are not invented here.

## User, future concepts, and evidence

GET /me returns/creates uid/email/display_name/onboarding_completed from Firebase-authenticated identity. No device fingerprint, forwarding address, shared family ownership, budget schema, offline sync object, or email source is defined in the current API. Earlier email/budget milestones remain [deferred roadmap](../product/scope.md), not removed source history.

See [contracts](contracts.md), [flows](../product/user-flows.md), [questions](../open-questions.md), and the [backend tracker](../development/backend-tracker.md) for implementation evidence and remaining work.
