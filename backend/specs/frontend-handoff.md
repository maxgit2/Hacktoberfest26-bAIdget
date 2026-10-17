# bAIdget — Backend API handoff for the Flutter app

Audience: the Flutter developer and their coding agent. This document is the **contract**. If something here conflicts with your assumptions, this document wins. If something is missing or ambiguous, ask the backend owner instead of guessing.

The machine-readable contract is `openapi.json` (exported from FastAPI). This file explains behaviour that the schema cannot.

---

## 1. Overview

bAIdget is a personal expense tracker. The user signs in with Google, picks expense categories, and adds expenses manually or by scanning a receipt / a screenshot of a payment. Expenses can be marked as recurring. The app shows monthly / yearly summaries and per-category totals. Each user only sees their own data.

- Base URL: `https://<TBD>/v1` (provided by the backend owner; a local emulator URL is available for development)
- Health check: `GET /health` (no auth)
- Currency: **EUR only** for now. The `currency` field exists and must be `"EUR"`.
- Online-only: the app needs a connection. There is no sync protocol.

### Hard rules for the app

1. Use the Firebase SDK **only for Auth**. Never read or write Firestore directly (it is locked for clients). Everything goes through this API.
2. Never send `owner` / user id. The backend takes it from the token.
3. Generate the expense `id` (UUIDv4) on the client when creating (see Idempotency).
4. Money is a JSON number with at most 2 decimals. Don't compute totals on the client from lists: use the summary endpoints.

---

## 2. Authentication

1. Sign in with Google through `firebase_auth` + `google_sign_in` (same Firebase project as the backend).
2. For every request send: `Authorization: Bearer <Firebase ID token>`. Get it with `await user.getIdToken()` before each call (the SDK caches and refreshes it).
3. On `401`, force-refresh the token (`getIdToken(true)`) and retry **once**. If it fails again, sign the user out.

---

## 3. Conventions

| Topic | Rule |
|---|---|
| Format | JSON, UTF-8. Exception: `POST /expenses/scan` is `multipart/form-data` |
| Timestamps | ISO 8601. Requests: any offset accepted (e.g. `2026-10-16T12:30:00+02:00`). Responses: always UTC with `Z` |
| Month/year boundaries | Computed by the server in `Europe/Rome` |
| IDs | Strings. Expense id = client UUIDv4. Categories / rules ids = server generated |
| Money | `amount`: number, ≤ 2 decimals, `> 0`, `<= 1000000`. Can be `null` in responses (scan could not read it) |
| Nulls | Optional fields are returned as `null`, never omitted |
| Soft delete | Deleted items disappear from all responses. `deleted_at` is always `null` in responses |
| Idempotency | `POST /expenses` and `POST /expenses/scan` accept a client `id`. If that id already exists for the user, the existing expense is returned with **200** (instead of **201**) and nothing is created twice. Safe to retry after a timeout |
| Pagination | `limit` (1–100, default 50) + opaque `cursor`. Response: `{ "items": [...], "next_cursor": "..." \| null }` |

### Error format

Every error has this shape:

```json
{ "error": { "code": "category_in_use", "message": "Human readable, English", "details": { } } }
```

Branch on `code`, never on `message`.

| HTTP | code | When |
|---|---|---|
| 401 | `unauthenticated` | Missing/invalid/expired token |
| 404 | `not_found` | Resource doesn't exist (or isn't yours) |
| 409 | `already_onboarded` | Onboarding already completed |
| 409 | `category_in_use` | Deleting a category used by expenses or active recurring rules |
| 409 | `cannot_modify_other` | Deleting the `Other` category |
| 409 | `category_name_taken` | Duplicate category name (case-insensitive) |
| 409 | `already_recurring` | `make-recurring` on an expense that is already recurring |
| 413 | `image_too_large` | Scan image over the limit (10 MB) |
| 415 | `unsupported_image_type` | Not jpeg / png / webp |
| 422 | `validation_error` | Bad body/query. `details.fields` lists problems |
| 422 | `min_categories` | Onboarding with fewer than 2 categories |
| 422 | `max_categories` | More than 30 categories |
| 422 | `category_not_found` | `category` id doesn't exist or is archived |
| 422 | `extraction_failed` | Scan could not read merchant nor total. Nothing was created |
| 429 | `rate_limited` | Too many scans. Header `Retry-After` (seconds) |
| 503 | `extraction_unavailable` | AI provider down. Retry later |
| 504 | `extraction_timeout` | AI provider too slow. Retry |
| 500 | `internal_error` | Bug. Report it |

---

## 4. Typical flows

**First launch**
1. Google sign-in → `GET /me`.
2. If `onboarding_completed == false` → `GET /categories/catalog` → user selects ≥ 2 (presets are shortcuts that preselect items) and may add custom ones → `POST /categories/onboarding`.

**Every app start / resume**
1. `POST /recurring-rules/sync` (fire and forget; creates missing recurring expenses up to today).
2. Load categories, expenses, summary.

**Add manually**: `POST /expenses` (generate `id` first).

**Scan**: compress the image (long side ≤ 2048 px, JPEG ~85) → `POST /expenses/scan` → show the returned expense. The call takes ~3–10 s: show a loader, client timeout 45 s. If it times out, retry with the **same** `id`. There is no confirmation step: the expense is already saved. If `needs_review` is `true`, highlight it so the user can fix it with `PATCH`, and send `needs_review: false` once reviewed.

**Make an expense recurring**: the user edits an existing expense and turns on "recurring" → `POST /expenses/{id}/make-recurring`. The edit screen of any recurring occurrence only changes that occurrence. To change the series use the recurring-rules endpoints.

**Delete a category**: if the server answers `category_in_use`, tell the user to move or delete those expenses first.

---

## 5. Endpoints

### Objects

**Expense**
```json
{
  "id": "6f1c1c0e-3b0a-4a64-9f0e-2d1f2f6d9a11",
  "owner": "firebase-uid",
  "date": "2026-10-16T10:30:00Z",
  "seller": "Esselunga",
  "title": "Esselunga",
  "description": null,
  "category": "cat_8f2a",
  "type": "single",
  "recurrence": null,
  "amount": 23.4,
  "currency": "EUR",
  "source": "scan",
  "scan_details": {
    "document_type": "receipt",
    "items": [
      { "description": "Latte", "quantity": 2, "unit_price": 1.2, "total": 2.4 }
    ],
    "vat_total": 2.1,
    "vat_number": "IT01234567890",
    "payment_method": "card"
  },
  "needs_review": false,
  "created_at": "2026-10-16T10:31:02Z",
  "updated_at": "2026-10-16T10:31:02Z",
  "deleted_at": null
}
```
- `type`: `"single"` | `"recurring"`. When `recurring`, `recurrence` is `{ "rule_id": "rule_x1" }`.
- `source`: `"manual"` | `"scan"`. `scan_details` is `null` for manual expenses; its fields may be `null`.
- `document_type`: `"receipt"` | `"invoice"` | `"payment_screenshot"` | `"other"`.

**Category**
```json
{ "id": "cat_8f2a", "name": "Groceries", "icon": "shopping_cart", "color": "#4CAF50",
  "catalog_id": "groceries", "is_other": false }
```
`icon` / `color` are free strings for the UI (optional). Archived categories are not returned by `GET /categories`.

**RecurringRule**
```json
{
  "id": "rule_x1",
  "frequency": "monthly",
  "start": "2026-08-05T09:00:00Z",
  "end_date": null,
  "active": true,
  "template": { "seller": "Netflix", "title": "Netflix", "description": null,
                "category": "cat_sub", "amount": 12.99, "currency": "EUR" }
}
```

---

### `GET /me`
Returns the user profile; creates it on first call.
```json
{ "uid": "firebase-uid", "email": "a@b.com", "display_name": "Ana", "onboarding_completed": false }
```

### `GET /categories/catalog`
Static catalog (English names; users can rename after onboarding).
```json
{
  "items": [ { "id": "groceries", "name": "Groceries", "icon": "shopping_cart" }, ... ],
  "presets": [
    { "id": "essential_4", "name": "Essential", "catalog_ids": ["groceries","transport","housing","entertainment"] },
    { "id": "complete_6",  "name": "Complete",  "catalog_ids": ["groceries","transport","housing","entertainment","dining_out","health"] }
  ]
}
```
Catalog ids: `groceries, dining_out, transport, housing, bills, health, entertainment, shopping, travel, education, subscriptions`.

### `POST /categories/onboarding`
Body (≥ 2 items in total between both lists):
```json
{ "catalog_ids": ["groceries", "transport"], "custom": [ { "name": "Pets", "icon": "pets", "color": "#FF9800" } ] }
```
→ `201` `{ "categories": [Category, ...] }`. An `Other` category (`is_other: true`) is always added automatically. Sets `onboarding_completed = true`.
Errors: `409 already_onboarded`, `422 min_categories`, `422 max_categories`, `409 category_name_taken`.

### `GET /categories`
→ `200` `{ "items": [Category, ...] }` (active categories only).

### `POST /categories`
Body: `{ "name": "Gym", "icon": "fitness_center", "color": "#2196F3" }` → `201` Category.
Errors: `409 category_name_taken`, `422 max_categories`.

### `PATCH /categories/{category_id}`
Body: any of `name`, `icon`, `color`. → `200` Category. `Other` can be renamed.

### `DELETE /categories/{category_id}`
→ `204`. Blocked if any non-deleted expense or active recurring rule uses it: `409 category_in_use`. `Other` can't be deleted: `409 cannot_modify_other`.

---

### `POST /expenses`
Creates a **single** expense.
```json
{
  "id": "6f1c1c0e-3b0a-4a64-9f0e-2d1f2f6d9a11",
  "date": "2026-10-16T10:30:00+02:00",
  "category": "cat_8f2a",
  "amount": 23.4,
  "currency": "EUR",
  "seller": "Esselunga",
  "title": "Weekly groceries",
  "description": null
}
```
Required: `date`, `category`, `currency` (default `"EUR"`). Optional: `id`, `amount`, `seller`, `title`, `description`. If `id` is omitted the server generates one.
→ `201` Expense (`200` if the `id` already existed).
Errors: `422 category_not_found`, `422 validation_error`.

### `POST /expenses/scan`
`multipart/form-data`: `image` (file: jpeg/png/webp, ≤ 10 MB) and optional `id` (UUIDv4). Works for receipts and for screenshots of a payment (bank app, wallet, e-mail confirmation). **One image per request.**
→ `201` Expense with `source: "scan"` (`200` on repeated `id`). Already saved, no confirmation step. The server picks a category from the user's categories (falls back to `Other`).
`needs_review: true` when the amount or date could not be read reliably or the items don't add up to the total.
Errors: `413`, `415`, `422 extraction_failed`, `429 rate_limited` (default 30 scans/hour/user), `503`, `504`.
The image is **not** stored by the backend.

### `GET /expenses`
Query: `from` (inclusive), `to` (exclusive) as ISO datetimes; `category` (id); `type` (`single|recurring`); `needs_review` (bool); `limit`; `cursor`.
→ `200` `{ "items": [Expense, ...], "next_cursor": "..." | null }`, ordered by `date` descending.

### `GET /expenses/{expense_id}`
→ `200` Expense, or `404`.

### `PATCH /expenses/{expense_id}`
Body: any of `date`, `seller`, `title`, `description`, `category`, `amount`, `currency`, `needs_review`. Send `null` to clear an optional field. Cannot change `id`, `owner`, `type`, `source`, timestamps. → `200` Expense.
On a recurring occurrence this only changes that occurrence.

### `DELETE /expenses/{expense_id}`
Soft delete. → `204`. Deleting one occurrence of a series does not stop the series (use the rules endpoints for that).

### `POST /expenses/{expense_id}/make-recurring`
```json
{ "frequency": "monthly", "end_date": "2027-06-30" }
```
`frequency`: `weekly` | `monthly` | `yearly`. `end_date` optional (local date, inclusive). The expense becomes the first occurrence; missing occurrences up to today are created right away.
→ `201`
```json
{ "rule": RecurringRule, "expense": Expense, "created_occurrences": 2 }
```
Errors: `409 already_recurring`, `404`.
Monthly note: an expense on the 31st recurs on the last day of shorter months (Jan 31 → Feb 28 → Mar 31).

---

### `GET /recurring-rules`
→ `200` `{ "items": [RecurringRule, ...] }`.

### `PATCH /recurring-rules/{rule_id}`
Body: any of `seller`, `title`, `description`, `category`, `amount`, `end_date`, `active`. **`frequency` and `start` can't be changed** (delete the rule and make a new one from an expense). Changes apply only to occurrences **not yet created**; existing ones stay untouched. Re-activating (`active: true`) does not backfill the paused period. → `200` RecurringRule.

### `DELETE /recurring-rules/{rule_id}`
Stops the series (`active=false`). Existing occurrences remain. → `204`.

### `POST /recurring-rules/sync`
Creates any missing occurrences up to now. Idempotent: safe to call as often as you like.
→ `200` `{ "created": 3, "rules_processed": 2, "has_more": false }`. If `has_more` is `true`, call again.

---

### `GET /summary/monthly?month=2026-10`
```json
{
  "period": { "type": "month", "value": "2026-10", "from": "2026-09-30T22:00:00Z", "to": "2026-10-31T23:00:00Z" },
  "currency": "EUR",
  "total": 842.3,
  "count": 41,
  "uncounted": 2,
  "by_category": [
    { "category": "cat_8f2a", "name": "Groceries", "total": 310.5, "count": 12, "percentage": 36.9 }
  ]
}
```
`uncounted` = expenses without amount (not included in totals). `by_category` is sorted by total descending and includes archived categories that still have expenses. `percentage` is informational (may not add up to exactly 100).

### `GET /summary/yearly?year=2026`
Same shape with `"type": "year"` plus:
```json
"by_month": [ { "month": "2026-01", "total": 701.2, "count": 33 }, ... ]
```
`by_month` always has 12 entries (zeros included).

---

## 6. Out of scope for now (don't build UI against these)

Family groups, importing e-mails, bulk scan, speech-to-text, other currencies, offline mode, budgets.
