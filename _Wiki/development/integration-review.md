---
title: Dev integration review and verification evidence
status: active
updated: 2026-10-17
---

# Dev integration review and verification evidence

Review target: dev 18c0d1946136db94a30983eb91e5f377b3a07678 and incoming frontend main 6d9baea8e66ca2eb4f49e8c6b22d2bfa30d2a185, integrating over shared ancestor ec8a3b5. User authorized merge plus commit/push. Source/code review covered backend app/tests/config/specs/CI/container and all 43 incoming frontend/test/platform/config paths; generated icons/plugin files are mechanical artifacts, not executed platform evidence.

## Delivered scope and compatibility

Actual backend application routes: GET /health and GET /v1/me. The /me response matches the client UserProfile parser; no owner is accepted from client input. Firebase verification runs in a threadpool and user access is scoped to token uid. Backend repository uses async Firestore transactions.

Frontend has real adapters but defaults to fake auth and memory mocks; onboarding/category/scan/sync mocks exceed actual server coverage. English UI/gallery-only decisions in docs/frontend-handoff.md are retained. No real category onboarding, scan/OCR, manual expense CRUD, summaries or recurrence is established by this merge.

## Repairs and findings

- **Repaired in source, Flutter validation pending:** token acquisition/refresh/sign-out exceptions previously bypassed Dio handler completion. AuthInterceptor now rejects/completes with the relevant error; four bounded regression tests were added. Tests are not claimed executed.
- **Verified guard repair:** backend tests now reject missing emulator variables before database initialization; README uses emulator exec/export rather than relying on .env auto-loading.
- **Verified profile contention repair:** initial full emulator run failed concurrent first-login (11 passed/1 failed). Commit-phase Aborted exhausted the SDK's five attempts; one fresh transaction round after 50–250 ms jitter now handles that specific exhaustion, with at most ten SDK commit attempts. Unrelated ValueError propagates. Two regression tests and real five-way concurrency pass; [diagnosis and limits](../lessons/firestore-profile-contention.md) preserve the evidence.
- **Known P2 follow-up:** POST /health and POST /v1/me return 500 internal_error because HTTPException mapping only preserves 401/404. Reproduced with local ASGI transport. Changing the error contract requires an explicit code/status choice; no new code was invented here.
- **Known P2 recovery gap:** persisted invalid API URL can strand profile/onboarding screens without Settings access; Settings currently lives on upload screen. Source-derived, not Flutter-runtime reproduced.
- Removed generated tracked firestore-debug.log from publication and ignore future debug logs. Root Obsidian state remains ignored; source history/backups are retained.

## Actual checks

| Check | Observed result |
| --- | --- |
| Isolated environment | Python 3.12.14 venv populated from environment.yml package names; no manifest dependency changes |
| Ruff | python -m ruff check . passed; python -m ruff format --check . passed, from backend/ |
| Generated OpenAPI | create_app().openapi() contains only /health and /v1/me |
| Missing-emulator safety probe | Health test setup exits 1 with explicit two-host requirement, before database client; expected result |
| Initial full emulator suite | Firebase CLI15.34.0, Java21.0.8, demo-baidget, Auth9099/Firestore8080: 11 passed, one concurrent-profile failure |
| Repaired full emulator suite | 14 passed in 12.42s; root independent repeat: 14 passed in 5.77s. Additional real five-way concurrency check: one passed in 2.50s |
| Regression sensitivity | Exhaustion regression fails against original get_or_create with 500 and passes the repair; unrelated ValueError is propagated without retry |
| Client tests | 25 declarations (18 API/model/mock, seven widget); flutter test test/api_test.dart could not start because Flutter is unavailable |
| ASGI method probe | GET /health 200; POST /health and POST /v1/me 500 internal_error, recorded follow-up |
| Wiki/merge final checks | 37 pages, three entry points, valid local links and metadata; staged diff whitespace passes; no unmerged paths; all 81 changed text files pass UTF-8/conflict-marker/whitespace/final-newline checks |
| Final graph change check | 86 files / 334 changed symbols / two affected flows, medium risk; structured result partial=false and truncated=false; all 334 symbols returned |

Backend test environment resolutions include FastAPI0.143.3, Starlette1.8.0, Firebase Admin7.7.0, Firestore2.34.1, pytest9.1.1, pytest-asyncio1.4.0, Ruff0.17.1, httpx0.28.1, pydantic2.14.1 and google-genai2.31.0. These are observed temporary installations, not new manifest pins. Declared CI uses Python3.12/Java21/Node22; local CLI used bundled Node24.19.0.

Reproducible local full-suite command: from backend with the declared environment active, `firebase emulators:exec --project demo-baidget --only firestore,auth "python -m pytest -q"`. No real Firebase/Gemini calls are permitted. Emulator CLI/Java and dependencies were prepared in local temporary/cache locations; no service was deployed.

## Graph and review limitations

GitNexus tools were initially absent from the callable MCP surface. A concurrently available local GitNexus1.6.12 runner/index was subsequently inspected and rebuilt with --index-only --pdg. AuthInterceptor impact was LOW (direct createDio/API-client dependents); profile get_or_create impact LOW via get_or_create_user/read_me. Fixture clear_firestore returned UNKNOWN because pytest autouse invocation is dynamic; source fixture inspection and the actual safety/suite checks supplement it, not a false unused verdict.

Final PDG rebuild succeeded: 2,974 nodes, 4,838 edges, 38 clusters and 22 flows. detect-changes --scope all returned medium risk for 86 files/334 symbols, affecting profile creation and auth sign-out. The CLI formatter prints only 15 symbols even with --limit 1000; inspecting the same installed LocalBackend structured result confirmed all 334 symbols with partial=false/truncated=false. These flows have backend emulator/regression coverage or explicitly unrun client regressions as recorded above.

FTS/BM25 is unavailable, and CLI does not support explain despite the PDG build. No complete taint-tool review is claimed. Structural context/impact and manual source/trust-boundary review are distinct evidence; no complete security audit or production validation is implied.

Flutter/Dart, Conda and Docker were unavailable; no Android/iOS/desktop build, real Google auth, deployed Firestore rules/Cloud Run, live OCR, or hosted CI success is claimed. Backends slices 02–07 remain planned. See [frontend](frontend-tracker.md), [backend](backend-tracker.md), [infrastructure](infrastructure-tracker.md), [questions](../open-questions.md), [log](../log.md).
