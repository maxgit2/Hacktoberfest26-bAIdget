# 02 — Firestore data model

> `01-stack.md` was not provided, so this file is **derived from `frontend-handoff.md`**. Every choice the handoff does not dictate is tagged **[D-n]** and listed in `open-questions.md` for approval.

## Global rules
- Everything lives under `users/{uid}`. `uid` comes only from the verified Firebase ID token.
- Timestamps are stored as Firestore `Timestamp` (UTC). Local dates (`end_date`) are stored as `"YYYY-MM-DD"` strings.
- Money is stored as **integer cents** `amount_cents` (`int | null`), e.g. 23.40 € → `2340`. The API exposes `amount` as a number with ≤ 2 decimals. Conversion goes through `Decimal(str(x)).quantize(Decimal("0.01"), ROUND_HALF_UP)`. **[D-1]**
- Soft delete: `deleted_at` is **written explicitly as `null` on create** and set to a Timestamp on delete. Every list query filters `deleted_at == null`.
- Clients are locked out: `firestore.rules` = deny all. Only the backend (Admin SDK) reads and writes.

## Collections

### `users/{uid}`
| field | type | notes |
|---|---|---|
| email | string\|null | from token |
| display_name | string\|null | from token |
| onboarding_completed | bool | default false |
| created_at, updated_at | Timestamp | |

Created with get-or-create inside a transaction on the first `GET /me`.

### `users/{uid}/categories/{category_id}`
`category_id` = `cat_` + short random id (server-generated). **[D-2]**
| field | type | notes |
|---|---|---|
| name | string | 1–40 chars, trimmed **[D-3]** |
| name_key | string | `casefold()` of the trimmed name, used for case-insensitive uniqueness |
| icon, color | string\|null | free strings |
| catalog_id | string\|null | null for custom categories |
| is_other | bool | exactly one per user; cannot be deleted |
| archived_at | Timestamp\|null | explicit null on create |
| created_at, updated_at | Timestamp | |

- Uniqueness: checked in a transaction against active (non-archived) categories via `name_key`. **[D-4]**
- Max 30 **active** categories, including `Other`. **[D-5]**
- Delete: blocked with `409 category_in_use` if any non-deleted expense or active rule uses the category; otherwise archived (`archived_at` set). See open question Q-1.

### `users/{uid}/expenses/{expense_id}`
`expense_id` = client UUIDv4 (or server `uuid4` if omitted). Recurring occurrences use `uuid5(NAMESPACE, f"{rule_id}:{n}")`, so retries produce the same id. **[D-6]**
| field | type | notes |
|---|---|---|
| date | Timestamp | stored as UTC |
| seller, title, description | string\|null | |
| category | string | category id, validated against the user's active categories |
| type | `"single"` \| `"recurring"` | |
| recurrence | map\|null | `{rule_id, index}`; `index` is internal and not exposed in the API **[D-7]** |
| amount_cents | int\|null | |
| currency | `"EUR"` | |
| source | `"manual"` \| `"scan"` | |
| scan_details | map\|null | `{document_type, items[{description, quantity, unit_price_cents, total_cents}], vat_total_cents, vat_number, payment_method}` |
| needs_review | bool | |
| created_at, updated_at | Timestamp | |
| deleted_at | Timestamp\|null | explicit null on create |

Idempotent create: `transaction.get(doc)` → if it exists, return it with **200** (even if soft-deleted? → Q-2), else `create` and return **201**.

### `users/{uid}/recurring_rules/{rule_id}`
`rule_id` = `rule_` + short random id.
| field | type | notes |
|---|---|---|
| frequency | `weekly`\|`monthly`\|`yearly` | immutable |
| start | Timestamp | date of the source expense, immutable |
| anchor_tz | `"Europe/Rome"` | occurrence n = local(start) + n·period, with day clamped to the end of the month (Jan 31 → Feb 28) **[D-8]** |
| end_date | string\|null | local date, inclusive |
| active | bool | |
| next_index | int | next occurrence to materialize (index 0 = source expense) |
| resume_from | Timestamp\|null | set on reactivation; occurrences dated before it are skipped, never backfilled **[D-9]** |
| template | map | `{seller, title, description, category, amount_cents, currency}` |
| source_expense_id | string | |
| created_at, updated_at | Timestamp | |
| deleted_at | Timestamp\|null | explicit null on create. `DELETE` sets `active=false` only (per handoff) |

Sync, one transaction per rule: read rule → for n from `next_index` while the occurrence date ≤ now and n < cap → `get` the deterministic expense doc; if absent, create it (a soft-deleted doc **exists**, so it is never recreated) → advance `next_index`. Caps: ≤ 50 occurrences per rule per call and ≤ 20 rules per call, then `has_more=true`. **[D-10]**

### `users/{uid}/meta/scan_rate`
`{window_start: Timestamp, count: int}`. Fixed 1-hour window, incremented in a transaction. Default limit 30/hour (configurable). **[D-11]**

## Indexes (`firestore.indexes.json`)
Collection group `expenses`, all with `deleted_at ASC`:
1. `deleted_at ASC, date DESC, __name__ DESC` (base list, summaries)
2. `deleted_at, category ASC, date DESC`
3. `deleted_at, type ASC, date DESC`
4. `deleted_at, needs_review ASC, date DESC`

Queries that combine several equality filters (for example category + type) can use index merging. If the emulator or production asks for a combined index, add it explicitly. Pagination cursor = opaque base64 of `{date, id}` + `start_after`.

Summaries read every non-deleted expense in the period range (`deleted_at == null`, `from ≤ date < to`) and sum `amount_cents` as integers. That is exact, with no float math. **[D-12]** Firestore `sum()` aggregation is not used because it cannot group by category.
