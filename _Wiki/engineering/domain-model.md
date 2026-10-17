---
title: Domain model
status: active
updated: 2026-10-17
---

# Domain model

Current source: main `b6d984e`, [Pydantic models](../../backend/app/models/expense.py), repositories/services and [OpenAPI](../../backend/openapi.json). The full persistence model is now present, extending [SRC-004](../raw/2026-10-17-frontend-handoff.md). [ADR-0007](../decisions/adr-0007-merged-backend-baseline.md) records observed choices without inventing independent approval. All business collections are below token-derived `users/{uid}`.

## Persistence map

| Document | Stored fields / behavior |
| --- | --- |
| users/{uid} | email/display_name from initial token, onboarding_completed=false initially, created_at/updated_at; transactionally provisioned by /me, existing token profile is not refreshed |
| categories/{category_id} | name/name_key/icon/color/catalog_id/is_other/archived_at/created_at/updated_at; IDs cat_ plus8 UUID hex chars; archive marker explicit null initially, no deleted_at field |
| expenses/{expense_id} | UTC date, nullable text, category ID, type, recurrence, amount_cents, EUR, source, scan_details, needs_review, timestamps, deleted_at=null initially; owner/id injected from UID/document on responses |
| recurring_rules/{rule_id} | frequency/start/anchor_tz/end_date/active/next_index/resume_from/template/source_expense_id/timestamps/deleted_at; IDs rule_ plus8 UUID hex chars |
| meta/scan_rate | UTC window_start and count, overwritten for next fixed hourly window |

The latter four paths are subcollections/documents under users/{uid}. UUID-prefix IDs are not guaranteed collision-free by a dedicated uniqueness reservation; expense create is transactional and returns existing records for reused IDs. No uploaded-image collection, inbox, budget, sharing membership, offline-operation log or user deletion endpoint exists.

## Expense API and mutation boundary

| Field | Implemented representation / rule |
| --- | --- |
| id | Client/server UUIDv4 for new manual/scan; generated recurring occurrences UUIDv5; response strings; immutable |
| owner | Token UID in response, not persisted as a mutation-supplied field |
| date | Required offset-aware timestamp, normalized UTC; patchable |
| seller/title/description | Nullable text; PATCH null clears; no explicit max text length in expense model |
| category | Active user category required on create/change; stored ID, not label |
| type/recurrence | single/null initially; conversion makes recurring/{rule_id}; internal occurrence index hidden from response |
| amount | Nullable positive <=1,000,000 with <=2 decimals; stored integer cents, response JSON number |
| currency | EUR literal/default, omitted create allowed; explicit null invalid |
| source | manual/scan; immutable through expense PATCH |
| scan_details | Structured stored cents metadata for scan, otherwise null; unconstrained dict in API model, serializer discrepancy below |
| needs_review | Manual=false; extraction-derived on scan; PATCH bool allows explicit clearing after user review, no automatic clearing when amount/date changes |
| created_at/updated_at/deleted_at | Server UTC dates; immutable through request; deleted records excluded so returned deleted_at=null |

Expense create/update and recurring request models forbid extra fields. PATCH requires at least one field; date/category/currency/needs_review cannot explicitly be null, while amount/text can. No scan_details edit API exists. Client model intentionally omits owner/deleted_at and keeps money as cents; default enum handling can tolerate unknown values but does not validate a full server response contract.

## Money and scan metadata

[Money helper](../../backend/app/core/money.py) parses Decimal from input, normalizes comma/dot separator styles, quantizes ROUND_HALF_UP to 0.01 and rejects original precision beyond2 decimals, non-finite/bool/zero/negative/over-limit values. Exact integer cents are summed; JSON response serialization converts to number. Request OpenAPI allows numeric strings as well as numbers/null; schema does not fully express custom bounds/precision.

Stored scan_details: document_type, items[{description,quantity,unit_price_cents,total_cents}], vat_total_cents, vat_number, payment_method. Scan response maps cents to unit_price/total/vat_total. Ordinary expense read/list/update/conversion currently leaves stored cents keys inside scan_details; this violates the handoff shape and the client parser expectation. See [contracts](contracts.md) and Q-25. Quantity currently reuses positive two-decimal money parsing, so weighted quantities with finer precision become null/review. Zero VAT likewise becomes null/review. Extracted non-EUR currency is ignored rather than rejected/converted (Q-29).

Extraction schema requires declared nullable fields and document_type enum, but now ignores additional fields after the Gemini schema fix in b6d984e (extra=forbid removed). Category IDs are rechecked against the user's active list; unknown goes to Other. Missing/invalid date uses now+review, naive extracted dates get TZ_NAME; missing merchant alone does not force review if amount/date/items are reliable. No provider confidence threshold is stored.

## Categories and summaries

Trimmed names1–40 chars, casefold uniqueness among active categories; icons/colors arbitrary nullable strings. At least two selected/custom items before Other, maximum 30 active including Other. Other is identified by is_other, renameable/non-deletable. Archive blocked by live expense or active-rule category reference; the rule usage query does not filter deleted_at. Category validation and later expense/rule writes are separate operations, so concurrent archive/write integrity needs targeted verification.

Summaries default to TZ_NAME=Europe/Rome local boundaries and return UTC periods. Integer cents totals exclude nulls; count/category count/month count exclude null amounts; uncounted reports them separately. Percentages rounded to one decimal HALF_UP; zero-total branch0.0; only populated counted categories returned, total-descending. Historical names use get_any (including archived), current names rather than name snapshots; missing category document causes a server error. Yearly always returns 12 zero-inclusive buckets. No persisted rollup or pagination of summaries.

## Recurring lifecycle

Rule response: id/frequency/start/end_date/active/template(text/category/amount/currency). Internal anchor_tz always Europe/Rome, start stored UTC, end_date local YYYY-MM-DD string. Source expense becomes index 0 unchanged ID; next_index starts1. Occurrence n derives from original local start (not previous date), clamps month/leap-day then returns UTC; UUIDv5 from fixed namespace plus rule ID/index. Generated records have manual source and no scan metadata/review flag. Original scanned index 0 keeps its scan data.

Rule PATCH modifies template/end_date/active for records not yet created; frequency/start/currency immutable. DELETE sets active=false without deleted_at, so inactive rules remain listed and reactivatable. Resume stores now and skips earlier indexes, not just a recorded pause interval. Existing expenses/edits/deletes remain untouched by sync; even deleted occurrence docs prevent regeneration. One transaction per rule, at most50 indexes/20 active rules per call; due rules prioritized. The cap has_more behavior is incomplete and client only runs five rounds: see [review](../development/integration-review.md#post-merge-audit-at-b6d984e).

See [flows](../product/user-flows.md), [questions](../open-questions.md) and the [backend register](../development/backend-tracker.md) for acceptance gaps; source schemas alone do not prove runtime or live owner isolation.
