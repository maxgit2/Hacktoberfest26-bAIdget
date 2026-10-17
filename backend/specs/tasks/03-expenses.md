# 03 — Expenses
**Depends on:** 02 | **Executor:** Codex

## Endpoints
`POST /v1/expenses`, `GET /v1/expenses`, `GET /v1/expenses/{id}`, `PATCH /v1/expenses/{id}`, `DELETE /v1/expenses/{id}`

## Files
`app/core/money.py` (Decimal helpers, cents conversion), `app/core/time.py` (parse any offset → UTC, serialize with `Z`), `app/repositories/expenses.py`, `app/services/expenses.py`, `app/routers/expenses.py`, `app/models/expense.py`, `firestore.indexes.json` (4 indexes from 02-data-model), `tests/test_expenses.py`, `tests/test_money.py`, plus the category_in_use test for slice 02.

## Acceptance
- Create: `id` UUIDv4 optional. Idempotent in a transaction: existing → **200** existing doc; new → **201**. (Q-2, Q-3 pending.) `type=single`, `source=manual`, `needs_review=false`, `deleted_at=None` written explicitly.
- `category` must be an active category of the user → else `422 category_not_found`.
- `currency` must be `"EUR"`. `amount`: >0, ≤1e6, ≤2 decimals, nullable.
- List: filters `from` (incl), `to` (excl), `category`, `type`, `needs_review`; `limit` 1–100 (default 50); opaque cursor; ordered by `date desc, id desc`; `next_cursor` null at the end. Invalid cursor → `422 validation_error`.
- PATCH: only the allowed fields; `null` clears optional fields; `category` is re-validated; `updated_at` refreshed. Forbidden fields → `422 validation_error`.
- DELETE: soft delete → 204. The item then 404s on GET and disappears from lists.
- Responses: every field present, `amount` as a number, timestamps UTC `Z`, `deleted_at: null`.

## Tests
create 201 then the same id → 200 with no duplicate; amount 0.001 / 0 / 1000000.01 → 422; amount null OK; float edge (0.1+0.2 style: 0.10 and 0.20 sum to exactly 0.30 in cents); `+02:00` input → `Z` output; pagination across 3 pages with no dups or gaps; each filter; soft delete hides the item; category delete blocked by an expense (slice 02 rule); **user B: GET/PATCH/DELETE A's expense → 404, B's list excludes A's**.
