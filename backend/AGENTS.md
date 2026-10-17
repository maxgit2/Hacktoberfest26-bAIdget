# AGENTS.md — rules for executor agents (Codex, Antigravity)

First follow the shared repository policy in [../AGENTS.md](../AGENTS.md), read the common wiki's current state/maintenance, and update its relevant frontend/backend/infrastructure trackers and log with actual evidence. These scoped backend slice rules supplement that policy; backend specs describe targets and must not become a separate implementation-status history. A human-authorized merge/review task retains its explicitly requested scope.

You implement **one slice**: `specs/tasks/NN-*.md`, in your own worktree/branch `slice/NN-name`. Read the task file, `specs/frontend-handoff.md` (API contract), `specs/02-data-model.md` and `specs/03-architecture.md` before coding.

## Never
- Edit anything under `specs/`. If a spec looks wrong or ambiguous, **stop and report it**. Do not guess.
- Change the API contract or the data model on your own. Propose it in your report.
- Commit secrets, `.env`, or service-account keys. Log tokens, images, amounts, e-mails or other PII.
- Call real Gemini or real Firebase in tests.

## Environment & commands
```bash
conda env create -f environment.yml   # or: conda env update -f environment.yml --prune
conda activate baidget
firebase emulators:exec --only firestore,auth "pytest -q"   # tests run against emulators
ruff check . && ruff format --check .
```
New dependencies: add them to `environment.yml` (pip section if not on conda-forge) and say so in your report.

## Layering
- `routers/`: HTTP only (parse, `Depends(current_user)`, call the service, return a response model). No business logic.
- `services/`: business rules. No Firestore imports.
- `repositories/`: the **only** modules that import `google.cloud.firestore`. Use `AsyncClient`.
- No blocking calls in async paths: wrap sync SDK calls (`firebase_admin.auth.verify_id_token`, Pillow, a sync Gemini client) in `run_in_threadpool` / `asyncio.to_thread`.
- `uid` comes **only** from the verified token. Every path starts at `users/{uid}`.

## Money
- `Decimal(str(x))` then `.quantize(Decimal("0.01"), ROUND_HALF_UP)`. Never do arithmetic on floats.
- Validate ≤ 2 decimals, `0 < amount ≤ 1000000`. `amount` is nullable.
- Store integer cents (`amount_cents`). Serialize as a JSON number.
- LLM amounts arrive as **strings**: normalize the comma (`"1.234,56"` → `1234.56`, `"12,5"` → `12.50`) before `Decimal`.

## Firestore
- Write `deleted_at: None` (and `archived_at: None` for categories) explicitly on create. Every list query filters `deleted_at == None`.
- Any new query shape gets its composite index in `firestore.indexes.json`.
- Read-modify-write (get-or-create, idempotent create, name uniqueness, rate limit, recurring sync) goes inside a transaction.

## Errors
Only the format and codes in `frontend-handoff.md` §3: `{"error": {"code", "message", "details"}}`. No new codes.

## Tests (write them together with the code)
- pytest + emulators. Two-user fixture: **every endpoint has a test proving user B cannot read or modify user A's data** (404).
- Gemini is mocked in every test.
- Recurring sync runs twice in one test: the second run creates 0.

## Report when done
Files changed, commands run with results (ruff, pytest summary), any spec doubts, and any new dependency.

## Review checklist (the orchestrator rejects the slice if any item fails)
- [ ] Paths under `users/{uid}`, uid from the token; a two-user isolation test exists
- [ ] No logic in routers; only repositories import Firestore; no blocking calls in async code
- [ ] Money rules above; no float arithmetic
- [ ] Explicit `deleted_at: null`; lists filter on it; indexes present
- [ ] Recurring: date computed from `start` (not incrementally), deterministic ids, transaction per rule, soft-deleted occurrences never recreated, idempotency test
- [ ] Only documented error codes
- [ ] Scan: image never stored or logged; LLM output validated against the schema; category id validated against the user's categories; Gemini mocked; rate limit enforced
- [ ] No secrets or PII in the repo or logs
- [ ] OpenAPI snapshot updated and consistent with `frontend-handoff.md` (from slice 07 on, or whenever an endpoint changes)
