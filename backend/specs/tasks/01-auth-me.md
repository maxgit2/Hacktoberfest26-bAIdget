# 01 — Auth + GET /me
**Depends on:** 00 | **Executor:** Codex | **Risk:** high (auth), reviewed with extra care

## Endpoints
`GET /v1/me`

## Files
`app/core/auth.py` (`current_user` dependency), `app/repositories/{client,users}.py`, `app/services/users.py`, `app/routers/me.py`, `app/models/user.py`, `tests/test_auth.py`, `tests/test_me.py`, two-user fixture in `conftest.py` (tokens minted by the Auth emulator).

## Acceptance
- Bearer token required. `verify_id_token(check_revoked=False)` runs in the threadpool. Any failure → `401 unauthenticated`, and the token is never logged.
- `uid`, `email`, `name` come from the decoded token only.
- `GET /me`: get-or-create `users/{uid}` in a transaction. Response `{uid,email,display_name,onboarding_completed}`.
- A single Firestore `AsyncClient` per process (lifespan).

## Tests
no header / malformed / expired or invalid token → 401 shape; first call creates the doc, second call returns the same doc and does not overwrite `created_at`; concurrent first calls (asyncio.gather ×5) → one doc; user A and user B get different profiles.
