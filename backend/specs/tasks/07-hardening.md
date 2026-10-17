# 07 — Hardening & OpenAPI
**Depends on:** all | **Executor:** Codex. **Deploy is out of scope (DevOps owns it).**

## Files
explicit `operation_id` + `response_model` + `responses` (error examples) on every route; `scripts/export_openapi.py` → `openapi.json`; `tests/test_openapi_snapshot.py` (fails if stale); `tests/test_contract.py` (every handoff endpoint + error code exists in OpenAPI); README updated (setup, env vars, emulators, architecture diagram, handoff notes for DevOps: Dockerfile, required env/secrets, `firestore.rules` + `firestore.indexes.json` to deploy, EU region).

## Acceptance
- `openapi.json` committed, matches app; `frontend-handoff.md` consistent with it (diff report attached; any mismatch → user).
- Final report: summary, deviations, open questions, future work.
