---
title: Integration contracts
status: active
updated: 2026-10-17
---

# Integration contracts

Current declared baseline: [SRC-004](../raw/2026-10-17-frontend-handoff.md), [ADR-0005](../decisions/adr-0005-api-handoff-baseline.md). Backend dev 18c0d19 now supplies only GET /health and GET /v1/me. Runtime-generated /v1/openapi.json exposes those paths; the complete committed snapshot is planned in slice 07. Other endpoints below remain contract targets. See [integration review](../development/integration-review.md). The [frontend handoff](../../docs/frontend-handoff.md) additionally specifies English UI and gallery-only input; [ADR-0006](../decisions/adr-0006-integrated-client-and-backend.md) preserves those decisions.

## Transport, identity, and retry rules

- Production API base remains `https://<TBD>/v1`. Implemented unauthenticated health is host-root `/health`; profile is `/v1/me`. Firebase emulator ports Firestore 8080/Auth 9099 are not the FastAPI address or evidence of a deployed API.
- Firebase SDK on the client is **Auth only**. Google sign-in uses `firebase_auth` and `google_sign_in` in the same Firebase project as the backend. No direct client Firestore access; deployment/rules compliance is unverified.
- Obtain a Firebase ID token with `user.getIdToken()` before each request and send `Authorization: Bearer <token>`. On 401, force refresh once with `getIdToken(true)` and retry once; sign out if authentication still fails. Do not send `owner` or a user ID in mutation requests; the backend derives ownership.
- JSON UTF-8, except multipart scan. Optional response fields are present as null rather than omitted. Offset timestamps accepted in requests; responses UTC with `Z`. Server month/year boundaries use `Europe/Rome`.
- Client generates UUIDv4 before manual creation or scan and reuses it on timeout retries. API permits an omitted ID, but then safe client retries lack that key. Repeated ID for the same user returns the existing expense with 200 rather than 201, without creating another record.
- EUR only. Amount is a JSON number with at most two decimals, greater than zero and at most 1,000,000 when supplied; null values are possible. Totals come from summary endpoints, never client aggregation of expense pages.
- Expense pagination uses `limit` 1–100 (default 50) and opaque `cursor`, yielding `items` and nullable `next_cursor`. Do not assume other list endpoints paginate if their documented shape lacks a cursor.
- Online-only, no synchronization protocol for offline edits. Recurrence sync is a separate server operation, not offline data sync.

## Endpoint registry

Paths are recorded as supplied; apply the base URL once, after confirming health routing. Full request/response examples and detailed errors remain in SRC-004 to avoid a second competing schema.

| Method / path | Declared behavior / key condition |
| --- | --- |
| GET /health | No auth; route prefix unresolved |
| GET /me | Get/create profile on first call; uid/email/display_name/onboarding_completed |
| GET /categories/catalog | English catalog and essential_4/complete_6 preset shortcuts |
| POST /categories/onboarding | Catalog/custom selections, at least two input items; auto-add Other; 201 categories, mark onboarded; repeated onboarding 409 |
| GET /categories | Active categories only |
| POST /categories | Create category; 201; case-insensitive unique names/max limit |
| PATCH /categories/{category_id} | Change name/icon/color; Other may be renamed |
| DELETE /categories/{category_id} | 204; block non-deleted expense/active-rule references and deletion of Other |
| POST /expenses | Create single expense; optional amount/seller/title/description; ID retry behavior above |
| POST /expenses/scan | One image multipart, jpeg/png/webp, at most 10 MB; optional UUID; saved expense, 201/200; Other fallback; no image retention |
| GET /expenses | Date descending; from inclusive/to exclusive ISO datetimes, category ID, single/recurring type, needs_review, limit/cursor |
| GET /expenses/{expense_id} | Expense or 404, including foreign-owner resources |
| PATCH /expenses/{expense_id} | date/seller/title/description/category/amount/currency/needs_review; null clears optional field; occurrence only |
| DELETE /expenses/{expense_id} | 204 soft deletion; does not stop its recurrence rule |
| POST /expenses/{expense_id}/make-recurring | weekly/monthly/yearly, optional inclusive local end_date; existing expense becomes first occurrence; backfill through today; 201 rule/expense/created_occurrences |
| GET /recurring-rules | items of rules |
| PATCH /recurring-rules/{rule_id} | Template seller/title/description/category/amount, end_date, active; cannot change frequency/start; only future not-yet-created occurrences affected |
| DELETE /recurring-rules/{rule_id} | 204, set inactive; existing occurrences stay |
| POST /recurring-rules/sync | Idempotently create missing occurrences; created/rules_processed/has_more; repeat while has_more |
| GET /summary/monthly?month=YYYY-MM | Server period bounds, total/count/uncounted/by_category, EUR |
| GET /summary/yearly?year=YYYY | Same shape, plus 12 by_month entries including zeros |

## Categories, scan review, and recurrence

Catalog IDs: `groceries, dining_out, transport, housing, bills, health, entertainment, shopping, travel, education, subscriptions`. Essential selects groceries/transport/housing/entertainment; Complete adds dining_out/health. Onboarding has at least two chosen/custom categories and a maximum of 30 is declared; whether Other counts toward the maximum needs OpenAPI/owner confirmation. Other is distinguished by `is_other`, not its editable display name.

Compress images to long side at most 2048 pixels and approximately JPEG quality 85. Show a loader, use client timeout 45 seconds, and reuse the ID on retry. The source's approximately 3–10 seconds is an estimate, not measured performance. Scan **already saves** the expense: display/edit it via PATCH; clear `needs_review` after review. Unreliable date/amount or item/total mismatch triggers review; absence of both readable merchant and total is `extraction_failed`, with no created expense.

Rules use `single|recurring`, not the superseded `concurrent`. Editing an occurrence does not edit its series; changing/deleting a rule leaves created occurrences intact. Monthly 31st clamps to shorter-month end and returns to the original day afterward. Reactivation does not backfill the paused interval. App start/resume triggers sync, but UI refresh/error ordering and rule timezone/leap-year details still need agreement.

## Summary and errors

Null amounts are excluded from totals and exposed via `uncounted`; never treat them as zero-valued purchases. Categories are sorted by total descending, including archived categories with expenses. Percentage is informational and may not sum to 100. Soft-deleted expenses are absent from responses; `deleted_at` in returned expenses is null. Week summaries, budget endpoints, offline sync, and email import are not defined/current scope.

Errors use `{error: {code, message, details}}`; branch on code, not the English message. Codes: 401 `unauthenticated`; 404 `not_found`; 409 `already_onboarded`, `category_in_use`, `cannot_modify_other`, `category_name_taken`, `already_recurring`; 413 `image_too_large`; 415 `unsupported_image_type`; 422 `validation_error` (details.fields), `min_categories`, `max_categories`, `category_not_found`, `extraction_failed`; 429 `rate_limited` with Retry-After seconds (default 30 scans/hour/user); 503 `extraction_unavailable`; 504 `extraction_timeout`; 500 `internal_error`.

Implementation/verification remains in the [backend tracker](../development/backend-tracker.md); client behavior in [frontend](../development/frontend-tracker.md); addresses/provider setup in [infrastructure](../development/infrastructure-tracker.md). See [open questions](../open-questions.md) and [model](domain-model.md).
