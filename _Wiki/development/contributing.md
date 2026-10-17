---
title: Contributing and development setup
status: active
updated: 2026-10-17
---

# Contributing and development setup

Read [current state](../current-state.md), [API contracts](../engineering/contracts.md), [scope](../product/scope.md), and [questions](../open-questions.md). Shared policy is [AGENTS.md](../../AGENTS.md); also read scoped backend instructions before editing backend files.

## Current repository layout

| Path | Actual content |
| --- | --- |
| lib/main.dart, lib/app.dart | App bootstrap and sign-in/profile/onboarding/upload gates |
| lib/core/ | Auth, network/mock adapter, API URL settings, formatting/theme/widgets |
| lib/features/ | Account/categories/expense models and repositories; onboarding, upload, read-only detail and settings screens |
| test/api_test.dart, test/app_flow_test.dart | API/model/scripted-adapter tests and mocked widget flows; old counter test removed |
| backend/app/ | FastAPI core, user models, repository/service and health/me routers |
| backend/tests/ | Auth, profile/idempotent creation/concurrency/isolation, errors and health tests |
| backend/environment.yml, backend/pyproject.toml | Conda Python 3.12 dependencies; Ruff/pytest configuration |
| backend/firebase.json, firestore.rules/indexes | Local emulators, client deny-all rules and current empty indexes |
| backend/Dockerfile, .github/workflows/ci.yml | Container and backend emulator CI definitions |
| docs/frontend-handoff.md, backend/specs/ | API handoff copies and backend target slices; frontend copy additionally specifies English UI/gallery-only |
| _Wiki/ | Shared synthesis, preserved raw sources, decisions/lessons, maintenance and work registers |

Actual integration refs are main 6d9baea and dev 18c0d19. No generated production Firebase platform configuration is committed; complete OpenAPI export arrives in planned backend slice 07.

## Testing quick start — working-tree correction, 2026-10-17

This section preserves and reconciles the concurrent testing-query notes with the merge review. The client has fake sign-in, onboarding, upload/detail/settings and mocked tests; the counter-only inventory is historical. Runtime success is not established without executing Flutter.

From repository root with a compatible Flutter SDK/device:

```powershell
flutter doctor -v
flutter pub get
flutter analyze
flutter test
flutter devices
flutter run -d <device-id>
```

For the synthetic demo, leave Settings backend URL empty and omit USE_FIREBASE=true. Tap Continue with Google (fake), select at least two categories or Essential, continue, choose a synthetic gallery receipt and upload. Every second mock scan requests review with no detected amount. Inspect detail, Settings and sign-out. Mock data is in memory and image content is not interpreted; review editing, manual input, summaries and recurrence are not delivered by this demo.

A nonempty URL enables real HTTP; it does not enable real auth. Real Google auth also needs USE_FIREBASE=true and Firebase platform configuration. Current real backend only supports /health and /v1/me, so category onboarding/scanning against it is incomplete. An invalid persisted URL can prevent access to Settings before onboarding; track FE-14 rather than repeatedly choosing an unusable URL.

## Backend setup and checks

From backend/, follow [backend README](../../backend/README.md). The declared toolchain is Conda env baidget from environment.yml, Python 3.12; dependencies are not pinned.

```sh
conda env create -f environment.yml
conda activate baidget
ruff check .
ruff format --check .
firebase emulators:exec --project demo-baidget --only firestore,auth "python -m pytest -q"
```

The Firebase CLI and Java are additional prerequisites. Both emulator host variables are mandatory for tests; plain pytest now fails before database client startup when either is absent. The guarded failure is intentional. Use demo-baidget and synthetic fixtures, never live Firebase/Gemini.

For a local API process, run the emulator exec wrapper with `uvicorn app.main:app --reload`, or explicitly configure emulator hosts. Settings do not automatically read .env; Uvicorn's --env-file option can load a local file. Health is at root /health; me/schema/docs use /v1. Production HTTPS and Android-emulator mapping are not supplied/tested.

## Observed verification environment and limits

A temporary Python 3.12.14 environment was created from the bundled runtime and populated with the exact package names in environment.yml; it is a verification alternative, not a change from Conda as the declared workflow. Java 21.0.8 and bundled Node 24.19.0 support local emulator tooling; Firebase CLI 15.34.0 was cached. See [integration review](integration-review.md) for exact commands/results, package resolutions and limitations.

Flutter/Dart, Conda and Docker are not available in the task PATH. No Flutter test/build, container build, hosted CI, production Firebase/Cloud Run or live Google/Gemini flow is claimed. GitNexus initially failed with the session's default Node shim; the bundled Node plus an escalated local command could use the installed runner. Later shared instructions/index were preserved, and pre-commit graph checks are recorded separately in the review.

Wiki check:

```powershell
& C:/Users/Max/AppData/Local/Python/bin/python.exe _Wiki/tools/check_wiki.py
```

A prior session verified that interpreter as Python 3.14.7; this machine-specific path is not a backend runtime selection. Structural checks do not establish feature correctness.

## Collaboration and recovery

Update the [frontend](frontend-tracker.md), [backend](backend-tracker.md), and [infrastructure](infrastructure-tracker.md) registers with each meaningful source/check/status change; use [maintenance](../maintenance.md). Preserve concurrent policy/testing notes and append log entries, rather than overwriting previous results.

The pre-integration local wiki/tracker backup is stash 9046be8c1d830584d8a3fe4028cd5e5689011cb8 (new untracked wiki files in its ^3 tree). The older bootstrap stash 7ee1ae3c86968ed83948a515cef9af506c527df7 is also retained. Do not blindly apply either over the integrated files. Personal _Wiki/.obsidian state is ignored, not published; generated emulator debug logs are excluded.

Git author metadata is separate from remote authentication; see [identity lesson](../lessons/git-author-identity.md). Publication uses the already verified current user's command-local identity, without changing global settings. Root AGENTS.md is canonical shared policy; scoped backend executor rules are additional implementation guidance and do not turn a merge/review into an unsolicited feature slice.

## Local Android provisioning in progress (2026-10-17)

The user authorized inspection and installation of the Windows test environment. Direct checks found Git/Winget and Microsoft OpenJDK 21.0.8 at `C:/Program Files/Android/openjdk/jdk-21.0.8`; Flutter/Android tools were absent from PATH. The machine reports Windows 10 Home 22H2, Intel i7-3630QM, about 16 GB RAM and about 816 GB free disk space. CIM reports an active hypervisor but firmware virtualization false; actual emulator acceleration remains unresolved. Reading Windows optional-feature state requires an elevated administrator token, which the execution process did not have.

Flutter tag 3.47.7 was cloned from the official repository into `C:/Users/Max/develop/flutter`; the matching release manifest declares Dart 3.13.5, compatible with `^3.13.4`. Dart bootstrap and official Google command-line tools downloads are still running. User `ANDROID_HOME` and Flutter/platform-tools/emulator PATH entries were configured without replacing other entries. A resumed Android Studio installer did not match its official checksum and was not executed; do not treat the IDE as installed. Android command-line tools plus existing Java can provision the emulator without that IDE.

A user-authorized local PowerShell procedure at `C:/Users/Max/develop/baidget-setup.ps1` is running hidden. It waits for the verified tools, installs API 36/build tools/emulator/Google APIs x86_64 image, creates `baidget_api36`, checks acceleration, configures Flutter, runs dependency resolution/analyze/tests/debug APK build, and attempts to launch the app if acceleration and build succeed. Its status, stdout and stderr are in the same directory as `baidget-setup-status.txt`, `baidget-setup.log` and `baidget-setup-errors.log`. This is an active installation process, not a recurring automation. Keep the computer awake and online. No reboot or firmware change is performed. Nonzero checks and required manual virtualization steps must be read from the logs; no frontend test/build/emulator success is claimed yet.
