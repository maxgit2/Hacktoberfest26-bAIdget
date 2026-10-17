# 02 — Categories
**Depends on:** 01 | **Executor:** Antigravity

## Endpoints
`GET /v1/categories/catalog`, `POST /v1/categories/onboarding`, `GET /v1/categories`, `POST /v1/categories`, `PATCH /v1/categories/{id}`, `DELETE /v1/categories/{id}`

## Files
`app/services/catalog.py` (static catalog: 11 ids + presets `essential_4`, `complete_6`, exactly as in the handoff), `app/repositories/categories.py`, `app/services/categories.py`, `app/routers/categories.py`, `app/models/category.py`, `tests/test_categories.py`.

## Acceptance
- Onboarding in **one transaction**: user not onboarded (else `409 already_onboarded`). Unknown catalog id → `422 validation_error`. Total of catalog + custom ≥ 2 (else `422 min_categories`). Total + Other ≤ 30 (`422 max_categories`, D-5). Names unique (`409 category_name_taken`). `Other` is added with `is_other=true`. Sets `onboarding_completed=true` → `201 {"categories":[...]}`.
- Create/rename: uniqueness by `name_key` among active categories (in a transaction); limit 30.
- `Other` can be renamed but not deleted (`409 cannot_modify_other`).
- Delete: if any expense with `deleted_at==null` or any rule with `active==true` uses the category → `409 category_in_use`, else archive (`archived_at`) → 204. (Q-1 pending.) Expenses and rules do not exist yet in this slice: the repo methods are written now; their tests land in slice 03/05.
- `GET /categories` excludes archived categories.

## Tests
catalog shape; onboarding happy path, already_onboarded, min, max, duplicate name (case-insensitive "groceries" vs "Groceries"); CRUD; rename Other OK / delete Other 409; archived category hidden; user B cannot PATCH or DELETE A's category (404).
