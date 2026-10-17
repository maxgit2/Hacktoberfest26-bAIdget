# 04 — Summaries
**Depends on:** 03 | **Executor:** Antigravity | **Parallel with:** 05, 06

## Endpoints
`GET /v1/summary/monthly?month=YYYY-MM`, `GET /v1/summary/yearly?year=YYYY`

## Files
`app/services/summary.py`, `app/routers/summary.py`, `app/models/summary.py`, repo method `expenses.list_in_range(uid, from, to)` (streams non-deleted docs), `tests/test_summary.py`.

## Acceptance
- Period boundaries are computed in `Europe/Rome` (`zoneinfo`) and returned in UTC (`2026-10` → from `2026-09-30T22:00:00Z`, to `2026-10-31T23:00:00Z`).
- Sums use integer cents and are converted to a Decimal number. `uncounted` = docs with null amount (not in total or by_category totals; `count` = counted docs only? → see Q-13 below).
- `by_category`: sorted by total desc, includes archived categories (name read from the archived doc), `percentage` = round(cat/total*100, 1), 0 when total = 0.
- Yearly: `by_month` always has 12 entries.
- Bad month/year → `422 validation_error`.

## Tests
DST boundaries (March and October); an expense at 23:30 local on the last day is in that month; null amounts → uncounted; archived category appears; empty month → zeros; yearly has 12 entries; user B sees nothing of A.

> Q-13 (to open-questions): does `count` include uncounted expenses? Proposal: `count` = expenses with an amount; `uncounted` separate.
