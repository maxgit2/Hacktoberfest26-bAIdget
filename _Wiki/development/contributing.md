---
title: Contributing and development setup
status: active
updated: 2026-10-19
---

# Contributing and development setup

Read [current state](../current-state.md), [contracts](../engineering/contracts.md), [questions](../open-questions.md) and [AGENTS](../../AGENTS.md). Baseline b6d984e; [audit ledger](repository-audit.md) records what was actually checked. Scoped backend instructions supplement shared policy; specs are protected from executor edits and do not constitute current completion status.

## Repository layout

| Path | Current role |
| --- | --- |
| lib/main.dart, lib/app.dart | Conditional Firebase bootstrap, preferences/Riverpod, auth/profile/onboarding/home/lifecycle |
| lib/core | Fake/Firebase auth, token retry, Dio/mock adapter, API URL preferences, formatting/theme/status |
| lib/features | Account/categories/expense models/repositories; sign-in/onboarding/gallery upload/read-only detail/settings |
| test |18 API/model/mock and7 widget declarations, no real backend/platform integration |
| android and other platform folders | Android target plus generated iOS/web/Linux/macOS/Windows runners; generated presence is not supported-product proof |
| backend/app | Layered FastAPI core/models/routers/services/repositories plus imaging/llm; all handoff domains |
| backend/tests |72 functions before parametrization; emulator safety fixture; mocked Gemini; ten synthetic text eval cases |
| backend/environment.yml, pyproject.toml | Conda Python 3.12, unpinned pip packages, Ruff/pytest settings |
| backend/openapi.json, scripts/export_openapi.py | Committed machine-readable contract and runtime export script |
| backend/firebase.json, firestore.rules/indexes | Auth9099/Firestore8080 emulators; deny-all clients; four expense indexes |
| backend/Dockerfile, deploy/bootstrap-gcp.sh | Non-root runtime image and one-time GCP/WIF/secret-container/budget setup |
| .github/workflows | Backend lint/emulator CI plus Cloud Run/rules/indexes deployment and smoke probes |
| docs/frontend-handoff.md, backend/specs | Frontend copy has English/gallery decisions; backend copy now has URL/extra errors; copies/report differ |
| _Wiki | Canonical current synthesis, historical source/decisions/log, trackers and full audit inventory |

## Post-hackathon development

The merged README reports cloud shutdown on 2026-10-17; the supplied service URL is historical. Use backend local emulator instructions below and synthetic data. A real mobile integration needs an explicitly configured running API and Firebase project; a default mock run does not require a live backend. [SRC-007](../raw/2026-10-19-post-hackathon-update.md) records reported historical test results, not a rerun in this check. Root .gitignore now excludes specific Obsidian files; other vault files may still be tracked.

## Flutter checks and modes

Root manifest requires Dart ^3.13.4; lockfile Flutter >=3.47.0. Exact Flutter release not pinned. With a compatible installed SDK:

```powershell
flutter doctor -v
flutter pub get
flutter analyze
flutter test
flutter devices
flutter run -d <device-id>
flutter build apk --debug
```

These commands are instructions, **not executed successes in this audit**. Flutter was absent in the checked PATH. Android uses min API24, Java/Kotlin17, AGP9.1.0/Kotlin2.4.0/Gradle9.3.1. Example com.example.baidget and debug signing in release remain. No google-services.json/firebase_options.dart/Google Services plugin integration is committed. Provider/app/signing and SDK compatibility need real verification.

Synthetic demo: empty effective URL and USE_FIREBASE=false → fake Continue with Google, at least2 onboarding selections (Essential shortcut), upload a synthetic gallery image, view saved detail, Settings/sign-out. Every second mock scan has null amount/review. No OCR, durable expense storage, manual/edit/list/delete or summary/rule-management UI is demonstrated. Mock category-limit behavior differs from server; do not use it for upper-bound acceptance.

Real mode requires same-project Firebase platform/Google provider configuration plus `--dart-define=USE_FIREBASE=true` and `--dart-define=API_BASE_URL=<host>/v1`. Backend handoff host is documented in [infrastructure](../engineering/infrastructure.md); the old cloud deployment is reported shut down, so use a configured local API or deliberately restored hosting. A nonempty URL alone enables real HTTP while keeping fake auth by default. Settings URL overrides build default; clearing returns to build default, not necessarily mock. Settings is unavailable before home, so recover a bad persisted URL through app data/preferences or a deliberate recovery fix (FE-14).

Client/gallery paths are Android-focused; other generated runners are not validated. Debug Android allows cleartext local HTTP; release does not explicitly enable it. Local emulator host mapping (e.g.10.0.2.2) needs actual device/network validation, not a promise of working routing. No CORS middleware is configured for a browser frontend.

## Backend local setup

Use [backend README](../../backend/README.md) and Python 3.12/Conda manifest; Firebase CLI and Java 21 are additional emulator prerequisites.

```sh
cd backend
conda env create -f environment.yml
conda activate baidget
ruff check .
ruff format --check .
firebase emulators:exec --project demo-baidget --only firestore,auth "python -m pytest -q"
python scripts/export_openapi.py
```

Regeneration writes the snapshot; inspect its diff and run test_openapi_snapshot/test_contract through the emulator wrapper. Tests use an autouse fixture requiring both emulator host variables, even for nominally pure tests, and clear the emulator database. Never point them at a live project/provider or weaken the guard to get a green result. Gemini is mocked. The eval comparator is a separate manual tool, not a CI/quality gate or captured image benchmark.

For local API use the same emulator exec wrapper around `uvicorn app.main:app --reload` (port8000 by default). Emulator8080 is Firestore, not API. Environment Settings does not read .env automatically; use Uvicorn `--env-file .env` if needed, never commit secrets. GET /health at host root; docs/schema/domain routes under/v1. Health does not test downstream readiness.

Full backend pytest/Ruff/export/container checks were not run here because required packages/tools are absent. Python 3.13 AST parsing/direct money and isolated-function probes are limited checks, not Python 3.12 application acceptance. Earlier14-test emulator results belong to the earlier auth/profile integration in [review](integration-review.md). No install/SDK provisioning was performed in this audit.

## Infrastructure and secrets

Use [infrastructure](../engineering/infrastructure.md) for GitHub variables, WIF, service accounts, Secret Manager, image/runtime limits, Firestore rules/indexes and trust gaps. Do not run bootstrap/deploy just to inspect state: these mutate cloud resources and require task authorization. This audit only read definitions and probed public health/auth/schema without tokens.

## Documentation and graph checks

```powershell
python _Wiki/tools/check_wiki.py
git diff --check
node .gitnexus/run.cjs detect-changes --scope all --repo .
```

Use a real Python 3.9+ interpreter; audit uses `C:/Program Files/Python313/python.exe` (3.13.0). GitNexus became available after the user indexed this checkout. Explicitly bind Hacktoberfest26-bAIdget in MCP; named context/impact works, concept queries warned missing FTS and are not authoritative negative results. Graph framework/DI omissions need source confirmation. The checker validates local paths/metadata/index coverage, not URL uptime, heading anchors or behavior.

Keep shared IDs, preserve raw notes and append-only history, update the three trackers and current state in the same change. Retained historical stash hashes are recorded in the earlier [log](../log.md); they were not inspected/restored by this audit. Do not blindly apply old snapshots over current work. No commit or push is implied by a documentation request.

<a id="local-android-provisioning-in-progress-2026-10-17"></a>

## Historical local Android provisioning (2026-10-17)

A previous session on a different user profile reported Java 21.0.8, Flutter3.47.7 source at C:/Users/Max/develop/flutter, official Dart/Android downloads and a setup procedure at C:/Users/Max/develop/baidget-setup.ps1. Its status/log/error files were recorded beside it. A resumed Studio installer checksum failed and was not executed; acceleration and frontend checks were pending at that report. The audit host uses MaxAdmin and did not observe that old process or its final outcome. This is historical evidence, not an installation or successful build on the present host. See the unchanged provisioning entry in [log](../log.md).
