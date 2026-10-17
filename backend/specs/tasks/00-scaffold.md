# 00 — Scaffold
**Depends on:** — | **Executor:** Codex | **Branch:** slice/00-scaffold

## Goal
Runnable empty service with tooling, errors, logging, health and CI. No domain code.

## Endpoints
`GET /health` (no auth, at root) → `200 {"status":"ok"}`. All other routes live under the `/v1` prefix. (Q-12)

## Files
`environment.yml` (conda: python=3.12, pip: fastapi, uvicorn[standard], pydantic-settings, google-cloud-firestore, firebase-admin, google-genai, pillow, python-multipart, structlog or stdlib json logging, pytest, pytest-asyncio, httpx, ruff), `pyproject.toml` (ruff + pytest config only), `app/main.py`, `app/core/{config,errors,logging}.py`, `app/routers/health.py`, `Dockerfile` (python:3.12-slim, pip install, non-root user, `uvicorn` on `$PORT`), `.dockerignore`, `.env.example`, `.gitignore`, `firebase.json` (emulators firestore:8080, auth:9099), `firestore.rules` (deny all), `firestore.indexes.json` (empty), `.github/workflows/ci.yml` (setup-miniconda, firebase-tools, Java, `ruff check`, `ruff format --check`, `firebase emulators:exec "pytest"`), `tests/conftest.py`, `tests/test_health.py`, `tests/test_errors.py`.

## Acceptance
- `AppError(code, http_status, message, details)` + handlers: `HTTPException`, `RequestValidationError` → `422 validation_error` with `details.fields`, unhandled → `500 internal_error` (no stack trace in the body).
- JSON logs with a request id. Authorization header and bodies never logged.
- Settings via env: `GOOGLE_CLOUD_PROJECT`, `FIRESTORE_EMULATOR_HOST`, `FIREBASE_AUTH_EMULATOR_HOST`, `GEMINI_API_KEY`, `GEMINI_MODEL`, `SCAN_RATE_LIMIT_PER_HOUR=30`, `MAX_IMAGE_BYTES=10485760`, `TZ_NAME=Europe/Rome`.
- `docker build` succeeds. CI passes.

## Tests
health 200; unknown route → error shape; invalid query → `validation_error` shape; forced exception → `internal_error` shape.
