---
title: Integration contracts
status: active
updated: 2026-10-17
---

# Integration contracts

Requirement baseline: [SRC-004](../raw/2026-10-17-frontend-handoff.md)/[ADR-0005](../decisions/adr-0005-api-handoff-baseline.md). Current source baseline: main `b6d984e`, [backend handoff](../../backend/specs/frontend-handoff.md), [OpenAPI](../../backend/openapi.json), routers/models/services. All handoff operations now exist; the [audit](../development/repository-audit.md) statically matched all 21 registered operations to the snapshot. Runtime schema regeneration/full contract tests were not executed here.

## Transport, identity and retries

Backend handoff base: `https://baidget-api-voiguesqbq-ew.a.run.app/v1`; root health is `/health`. This audit observed500/503 service errors; see [infrastructure](infrastructure.md). [Frontend handoff](../../docs/frontend-handoff.md) still has TBD and adds English UI/gallery-only decisions. Flutter defaults to empty URL/mock; the production address must be supplied deliberately.

Every domain operation requires Firebase Bearer auth. UID comes only from the verified token; Firebase client SDK is Auth-only. No owner field is accepted in expense mutation models (`extra=forbid`). Verification uses `check_revoked=False`; it does not restrict sign-in provider to Google. Health/docs/schema are public in source. Client interceptor refreshes/retries once on401, clones multipart and signs out on repeated authentication failure; provider-operation exceptions are handled, but real Google integration is unverified.

JSON UTF-8 except multipart scan. API amount responses are numbers, null if absent; requests normalize through Decimal and currently also accept numeric strings (OpenAPI number|string|null). EUR default allows omitted currency on manual create, unlike handoff's contradictory required/default wording. Amount >0, <=1,000,000 and at most two decimals. Offset-aware requests normalize to UTC Z. Server reports default Rome periods; occurrence math hardcodes Rome. See [model](domain-model.md).

Manual/scan IDs are optional UUIDv4; clients must generate/reuse them for safe retry. Transactional create returns 201 new or200 existing per user. Existing-body differences do not overwrite the record, but manual create validates category before checking the ID. A deleted manual ID returns 404 after valid request/category processing. Scan checks an existing *live* ID early, before image/quota/provider work. Deleted IDs fall through extraction/quota before eventual404; they are not resurrected, but failures can occur earlier. Concurrent fresh scans can invoke Gemini more than once while persisting only one expense.

## Endpoint registry: source implemented

All paths below are full server paths. Flutter currently consumes me, catalog/onboarding/category list, scan and sync; the remaining operations have no client repository/UI. Request/response model definitions and snapshot are the exact schema; this table summarizes behavior, not a second schema.

| Method / path | Success and implemented behavior |
| --- | --- |
| GET /health | 200 static status; no auth/dependency readiness check |
| GET /v1/me | 200 get/create profile transaction; uid/email/display_name/onboarding_completed |
| GET /v1/categories/catalog | 200 static 11-item English catalog, Essential/Complete presets; authenticated |
| POST /v1/categories/onboarding | 201 categories; min 2 selected/custom, add Other, total active<=30, unique names, transactional completion;409 repeated |
| GET /v1/categories | 200 items, active only, no cursor |
| POST /v1/categories | 201 category, trimmed1–40-char name; unique active casefold name; max 30 |
| PATCH /v1/categories/{category_id} | 200 name/icon/color; at least one field; name cannot be null; Other rename allowed |
| DELETE /v1/categories/{category_id} | 204 archive;409 if Other, live expenses or active rule references |
| POST /v1/expenses | 201/200 single manual expense, optional UUID/amount/text/default EUR |
| POST /v1/expenses/scan | 201/200 persisted expense; multipart image and optional UUIDv4; JPEG/PNG/WebP decoded bytes,10,485,760-byte service limit |
| GET /v1/expenses | 200 items/next_cursor; from inclusive/to exclusive, category/type/needs_review filters, limit 1–100 default 50 |
| GET /v1/expenses/{expense_id} | 200 expense or404 for absent/deleted/foreign ID |
| PATCH /v1/expenses/{expense_id} | 200 allowed date/text/category/amount/currency/needs_review fields; empty/forbidden/null required fields422; one occurrence only |
| DELETE /v1/expenses/{expense_id} | 204 soft delete; repeated delete404, rule continues |
| POST /v1/expenses/{expense_id}/make-recurring | 201 rule/expense/created_occurrences; converts source to index 0 and performs one capped catch-up;409 already recurring |
| GET /v1/recurring-rules | 200 items including inactive, excluding deleted_at; no pagination |
| PATCH /v1/recurring-rules/{rule_id} | 200 editable template/end_date/active; no frequency/start/currency; affects unmaterialized occurrences |
| DELETE /v1/recurring-rules/{rule_id} | 204 active=false; rule stays listed, can be reactivated; expenses unchanged |
| POST /v1/recurring-rules/sync | 200 created/rules_processed/has_more;20 rules/50 indexes per rule per call; issues below |
| GET /v1/summary/monthly?month=YYYY-MM | 200 server period/total/count/uncounted/by_category |
| GET /v1/summary/yearly?year=YYYY | 200 same plus12 monthly entries including zeros |

Lists use descending date then descending document ID. Cursor is base64 JSON date/id, opaque to clients, validated before `start_after`; it is not signed or bound to original filters. Invalid cursor422. Query range order `from<to` is not explicitly enforced by the service. Response optional fields are explicit nulls; deleted expenses are excluded, so returned deleted_at is null.

## Categories and persisted scan review

Catalog IDs: groceries, dining_out, transport, housing, bills, health, entertainment, shopping, travel, education, subscriptions. Essential selects groceries/transport/housing/entertainment; Complete adds dining_out/health. Server adds Other and counts it in30. Duplicate catalog/custom names fail409; names trimmed/casefolded. Client/mock instead allow30 picks before Other; this is unresolved integration drift, not an alternative approved maximum. Backend icons `receipt_long` and `medical_services` fall back to the client's generic label icon.

Scan performs client/server JPEG preparation (long side<=2048, quality 85), default provider timeout 30s and client receive timeout 45s. Image type is decoded, not trusted from extension/MIME. Quota is transactional fixed UTC-hour (default 30 attempts/user), consumed before provider/extraction success.429 includes Retry-After. Successful response is already saved: no second confirmation/create. Missing/invalid date uses current UTC and review; naive extracted date uses TZ_NAME. Missing/invalid amount, item/total discrepancy >one cent per item, invalid item values or VAT set review. Neither merchant nor valid total yields422 without an expense. Unknown category maps to caller's Other. Extracted currency is currently ignored and stored EUR; see Q-29.

`scan_details` money conversion exists only in scan service response. Ordinary GET/list/PATCH and make-recurring responses call `_expense_response`, leaving stored `unit_price_cents`, `total_cents`, `vat_total_cents` inside the arbitrary dict. The Flutter parser expects `unit_price`, `total`, `vat_total`; reloaded records would lose displayed scan money. OpenAPI does not constrain this nested object. This source-verified discrepancy is not fixed by this audit.

## Recurrence and summaries

Rules anchor in Europe/Rome, inclusive local end_date, weekly/monthly/yearly arithmetic from original start; Jan31→Feb28→Mar31 and Feb29→Feb28/non-leap→Feb29/leap. Source expense retains its ID and original metadata at index 0. Generated UUIDv5 records use source=manual, scan_details=null, needs_review=false, internal recurrence.index. Existing records, including deleted occurrences, are skipped. Pause→resume sets resume_from=now and skips prior indexes, with a50-index processing cap. DELETE is deactivation, not tombstoning.

Sync prioritizes due rules, then other active rules, sorted by ID; no cursor. `has_more` is initialized true whenever active count>20, even if none due. Flutter makes at most five calls, swallows failure and does not refresh lists/summaries (which have no UI yet); overlapping lifecycle sync is not serialized. Conversion only performs one capped catch-up, so an old source can require later sync. Existing expenses never change when the rule template changes; overdue but not-yet-created occurrences use the current template.

Summaries stream all non-deleted records in [from,to), aggregate integer cents and fetch names including archived categories. `count` and category/month count include only non-null amounts; `uncounted` includes null amounts and excludes them from buckets/totals. Percentages use Decimal ROUND_HALF_UP to one decimal, categories sort by total descending; zero total branch returns 0.0, empty summary categories empty. Yearly always returns 12 months. No weekly, comparison, budget or email API exists.

## Errors and contract drift

Envelope `{error:{code,message,details}}`; branch on code.401 unauthenticated;404 not_found;409 already_onboarded/category_in_use/cannot_modify_other/category_name_taken/already_recurring;413 image_too_large;415 unsupported_image_type;422 validation_error/min_categories/max_categories/category_not_found/extraction_failed;429 rate_limited;503 extraction_unavailable;504 extraction_timeout;500 internal_error. Validation details list fields; request middleware adds X-Request-ID. Unsupported HTTP methods are mapped from 405 to 500 by the generic HTTP handler, a retained defect.

[CONTRACT-REPORT](../../backend/CONTRACT-REPORT.md) describes currency optionality, unconstrained scan_details and extra endpoint errors, but became partly stale when backend handoff documented deleted-ID/category errors. The frontend copy remains older. Snapshot permits number|string for Decimal input and generic nested scan_details; UUIDv4/precision rules are partly custom validators rather than complete schema constraints. Structural endpoint/error-code tests do not prove every runtime condition or nested response. Use [review](../development/integration-review.md#post-merge-audit-at-b6d984e), [questions](../open-questions.md) and [backend tracker](../development/backend-tracker.md) for remaining reconciliation and verification.
