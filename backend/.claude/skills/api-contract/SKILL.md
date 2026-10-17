---
name: api-contract
description: Procedure when any endpoint, field, status code or error code changes in bAIdget — get user approval, update frontend-handoff.md in same branch, regenerate OpenAPI snapshot. Use whenever a diff touches routers/ or models/.
---
1. Contract change proposed? → stop, ask the user (frontend dev depends on it).
2. Approved → edit `specs/frontend-handoff.md` in the SAME branch (object shapes, endpoint section, error table).
3. `python scripts/export_openapi.py` → commit `openapi.json`; `pytest tests/test_openapi_snapshot.py tests/test_contract.py`.
4. Call it out in the slice status under "deviations from spec".
Review: `git diff main -- app/routers app/models` non-empty and `openapi.json` unchanged → reject.
