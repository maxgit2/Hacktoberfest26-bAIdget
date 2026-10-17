---
title: Integration review and verification evidence
status: active
updated: 2026-10-17
---

# Integration review and verification evidence

The earlier integration below is historical. For current main source, findings and actual checks see [post-merge audit](#post-merge-audit-at-b6d984e) and the [file ledger](repository-audit.md).

## Historical integration at 18c0d19

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

## Post-merge audit at b6d984e

Requested by the initiator after the large backend dev merge; initial working tree clean. All307 baseline tracked files are accounted for in the [audit ledger](repository-audit.md): application and test text inspected, platform scaffolding/configuration reviewed by role, binary icons inventoried, old raw records preserved. No application symbol was edited. [SRC-006](../raw/2026-10-17-post-merge-audit.md)/[ADR-0007](../decisions/adr-0007-merged-backend-baseline.md) separate observed implementation choices from product approval.

### Current delivery

Backend slices00–07 now contain models, repositories, services, routers and tests;21 operations across15 paths, all 20 handoff operations plus root health. Gemini/Pillow/image validation, transactional quotas, summaries and recurrence are source-present. CI, bootstrap, keyless Cloud Run deployment, secret injection, four indexes and OpenAPI snapshot exist. Flutter still defaults to fake auth/memory data and exposes only sign-in/profile/onboarding/upload/read-only detail/settings plus bounded sync. Remaining manual/edit/list/delete/category-maintenance/rules/summary UI is absent, not missing server source.

### Findings requiring follow-up

Priorities below are audit recommendations, not assigned release commitments. “Source” means directly inspected; isolated probes name their stubs and do not imply ASGI/emulator validation.

| ID | Priority / evidence | Finding and practical consequence | Follow-up |
| --- | --- | --- | --- |
| A-01 | P1; source + isolated serializer-body probe | [General expense serializer](../../backend/app/services/expenses.py) preserves stored scan_details *_cents keys; [scan serializer](../../backend/app/services/scan.py) maps them to unit_price/total/vat_total. Reload/list/PATCH/conversion differ from upload; Flutter expects the latter. | BE-13, Q-25: centralize conversion, type nested schema, test scan→GET/list/PATCH/conversion |
| A-02 | P1; source | [Client limit](../../lib/features/categories/domain/category.dart)/mock count 30 picks excluding Other; [server](../../backend/app/services/categories.py) counts Other in30. Mock success can become server422. Client also lacks receipt_long/medical_services icons (generic fallback). | FE-15, Q-10: align limits and server-backed boundary cases |
| A-03 | P1; source + isolated sync-body probe | [sync_recurring_rules](../../backend/app/services/recurring.py) sets has_more if active count>20 even with no due rules. [AccountRepository](../../lib/features/account/data/account_repository.dart) stops after 5 calls, home suppresses errors/has no completion refresh or overlap guard. | BE-14/FE-08, Q-21/26: meaningful backlog/completion and refresh/retry protocol |
| A-04 | P1; source | [Android Gradle](../../android/app/build.gradle.kts) lacks Google Services plugin/config; no google-services.json/GoogleService-Info.plist/firebase_options.dart tracked. Example ID/debug release signing remain; real mode calls Firebase.initializeApp. | INF-03, FE-02/03/11: registered same-project Firebase/signing and actual device test |
| A-05 | P1; live public read-only probe | Handoff Cloud Run URL returned /health500, /v1/me503, /v1/openapi.json503 (HTML service responses), not expected200/401/schema. Root health itself is only static OK when app starts. | INF-10, Q-27: investigate revision/deploy/runtime logs, verify availability; cause unknown |
| A-06 | P1 financial currency / P2 metadata; source | [Extraction mapper](../../backend/app/services/scan.py) ignores extracted currency and labels EUR, without conversion/review based on currency. Quantity uses positive two-decimal money parser; weighted precision/zero VAT can become null/review. | BE-15, Q-29/30: agree validation/review rules, synthetic non-EUR/weighted/zero cases |
| A-07 | P2; source | Deleted-ID scan lookup hides tombstone, so image/quota/provider work can occur before eventual404. Concurrent fresh same-ID requests can both call Gemini before idempotent persistence. | BE-16, Q-28: clarify retry/error-order/billing guarantees and concurrency tests |
| A-08 | P2; source + historical ASGI probe | [HTTP error handler](../../backend/app/core/errors.py) maps unsupported methods405 to 500. | BE-12: approved status/code behavior and regression |
| A-09 | P2; source | [Settings](../../lib/features/settings/presentation/settings_screen.dart) only reachable after profile/onboarding. Bad persisted URL can strand earlier gates. URL accepts HTTP/HTTPS; selected host receives Firebase bearer tokens. | FE-14: startup recovery; treat override as trusted developer configuration |
| A-10 | P2 operational verification gap | [Four indexes](../../backend/firestore.indexes.json) do not establish all multi-filter/active-rule category-usage queries in deployed Firestore. Category validation/archive vs expense/rule creation are separate operations; concurrent integrity needs verification. | INF-11, Q-31: validate target queries/indexes and race cases; no reproduced live index failure claimed |
| A-11 | P2 deployment trust verification gap | [WIF bootstrap](../../backend/deploy/bootstrap-gcp.sh) conditions on repository, not ref; [deploy](../../.github/workflows/deploy.yml) manual entry bypasses CI success and has no explicit triggering-event/manual-main guard. Actual branch/environment/IAM restrictions unknown. | INF-12, Q-32: review entry-point/ref protection, no exploit or failed IAM test claimed |
| A-12 | P2 evidence/contract drift | Backend handoff URL and extra errors changed; frontend copy still TBD/older errors, CONTRACT-REPORT partly stale. Snapshot is generic for scan_details and allows Decimal strings; endpoint coverage tests are shallow. Offline eval has text cases, skips missing results and no quality threshold. | BE-02/09/10, Q-22: reconcile handoffs/report/schema and collect meaningful current validation/evaluation |

### Checks actually executed in this audit

| Check | Result / limit |
| --- | --- |
| Baseline | git status --short initially empty; git log pins b6d984e;307 git ls-files paths inventoried |
| Python syntax | Python 3.13.0 ast.parse on all 57 tracked Python files passed; no imports/services/emulators exercised |
| Static API comparison | Parsed committed JSON;21 router method/path pairs equal snapshot; all 20 handoff method/path pairs present; no runtime export/model-equivalence claim |
| Money | Direct import of stdlib-only core/money.py: exact 0.10+0.20 cents, both separator styles and invalid precision/zero/max/nan/bool rejection passed |
| Recurrence arithmetic | Isolated actual occurrence_date/occurrence_id function bodies with stdlib globals: UTC month/leap clamps and deterministic UUID passed; no Rome DST (tzdata unavailable) |
| Serializer discrepancy | Actual serializer bodies with identity ExpenseResponse.model_validate stub: generic output retains *_cents keys, scan output maps12.34; source defect reproduced in this bounded context |
| Sync discrepancy | Actual async sync body with fake repository returning21 active non-due rules: created0/rules_processed20/has_more=true reproduced; no Firestore transactions exercised |
| Public service | Python urllib HTTPS GET, no token/receipt/mutations;500/503 results above. Initial sandbox socket-denied attempt followed by permitted read-only network execution; no provider call |
| Runtime prerequisites | Python 3.13.0 present; pytest/FastAPI/Firebase/Firestore/Pillow/tzdata absent in selected interpreter; Flutter/Java/Firebase/Conda/Ruff not found in checked PATH |
| Test inventory |72 backend test functions before parametrization,25 Flutter declarations; tests are not reported passing |

Full pytest/Ruff/schema regeneration/Flutter/Android/container/hosted workflow/live Firebase/Gemini and deployed IAM/rules/index checks remain unrun. The earlier14 passing tests remain scoped to 18c0d19-era health/profile, not all current domains. Source contains test coverage for normal domain/isolation/concurrency cases, but lacks demonstrated current runtime evidence and targeted regressions for findings above. No test bypass of the emulator safety fixture was performed.

### Current graph evidence

At first the MCP registry lacked this repo and local runner/metadata were absent. The user created the index during the audit. Bound explicitly to Hacktoberfest26-bAIdget at commit b6d984e; context reports250 indexed files/2,004 nodes/4,037 relationships/115 processes, no declared incomplete reasons. Generated policy block counts differ slightly because it was emitted earlier in that run; preserve the user's generated edits.

Concept queries returned empty with **FTS indexes missing / keyword search degraded**; these are not proof of absent features. Named context corroborated scan→prepare_image/extract/quota/idempotent persistence and sync→planner/repository links, plus the generic serializer's six callers. Read the named process Scan → Consume_in_transaction: router→scan_expense→consume→transaction. The process-ID URI did not resolve; the process-name URI did. current_user has no incoming call edges despite explicit Depends(current_user) in routers; source registration establishes framework usage and an empty graph result is not an unused verdict.

Documentation impact: current-state/README/root AGENTS are MEDIUM with 44 reachable linked files; trackers/questions/review are HIGH (18–21 direct document references), no application processes attributed to File nodes. This HIGH warning was reported before those edits; IDs/paths are preserved and linked pages reconciled. No application-symbol blast-radius or complete taint audit is claimed. Final graph/diff/wiki results are in the [ledger](repository-audit.md) and [log](../log.md).
