# 05 — Recurring
**Depends on:** 03 | **Executor:** Codex | **Risk:** high (concurrency) | **Parallel with:** 04, 06

## Endpoints
`POST /v1/expenses/{id}/make-recurring`, `GET /v1/recurring-rules`, `PATCH /v1/recurring-rules/{id}`, `DELETE /v1/recurring-rules/{id}`, `POST /v1/recurring-rules/sync`

## Files
`app/services/recurrence.py` (pure date math: `occurrence_date(start_local, freq, n)` with month-end clamp), `app/repositories/rules.py`, `app/services/recurring.py`, `app/routers/recurring.py`, `app/models/recurring.py`, `tests/test_recurrence_math.py`, `tests/test_recurring.py`.

## Acceptance
- Occurrence n is computed **from start** (Jan 31 → Feb 28 → Mar 31, never drifting). Leap years: Feb 29 yearly → Feb 28 in non-leap years.
- `make-recurring`: in a transaction, the expense becomes `type=recurring`, `recurrence={rule_id, index:0}`; the rule is created with `next_index=1`; then the sync of that rule runs → `201 {rule, expense, created_occurrences}`. Already recurring → `409 already_recurring`. Missing or deleted → 404.
- Sync: ≤ 20 active rules per call, one transaction per rule, ≤ 50 occurrences per rule; occurrence id = `uuid5(NS, f"{rule_id}:{n}")`; existing doc (even soft-deleted) → skip, never recreate; stop at `end_date` (inclusive, local) or now; `has_more` when a cap is hit.
- PATCH rule: template fields + `end_date` + `active`; `frequency`/`start` → `422 validation_error`. `active` false→true sets `resume_from=now`; occurrences dated before it are skipped and `next_index` advances past them (no backfill).
- DELETE rule → `active=false`, 204. Existing occurrences remain.

## Tests
math table (weekly, monthly 31st, yearly Feb 29); **sync twice → second created=0**; soft-delete one occurrence then sync → not recreated; pause 3 months, reactivate → no occurrences for the paused period; caps → has_more; end_date respected; concurrent sync calls (gather ×3) → no duplicates; category delete blocked by an active rule; user B cannot touch A's rules (404) and B's sync does not create A's expenses.
