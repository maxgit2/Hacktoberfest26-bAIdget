---
title: Current state
status: active
updated: 2026-10-17
---

# Current state

## Integrated source and verified boundaries

The integration combines frontend main commit `6d9baea8e66ca2eb4f49e8c6b22d2bfa30d2a185` with backend dev commit `18c0d1946136db94a30983eb91e5f377b3a07678`. The merge applies without textual conflicts. Pre-existing API-handoff/wiki/tracker work was preserved in local safety stash `9046be8c1d830584d8a3fe4028cd5e5689011cb8` and restored for this integration. Personal Obsidian state remains local/ignored.

The frontend is no longer a counter demo: [app.dart](../lib/app.dart) gates sign-in/profile/onboarding/upload, with gallery input, read-only expense detail and settings. Empty API URL and `USE_FIREBASE=false` default to fake auth and synthetic in-memory data. Auth adapters and API repositories are present; production Firebase configuration and real end-to-end behavior are unverified. UI is English and gallery-only under [frontend handoff decisions](../docs/frontend-handoff.md).

The backend now exists under [backend/](../backend/README.md), with Python 3.12/Conda dependency manifest, layered FastAPI source, async Firestore profile transactions, Firebase token verification, JSON errors/logging, emulator config, deny-all Firestore client rules, Dockerfile and [backend CI](../.github/workflows/ci.yml). Implemented business routes are only `GET /health` and `GET /v1/me`; generated docs/schema are under /v1. No complete committed OpenAPI snapshot exists.

Categories, expenses, scan/OCR, summaries and recurrence are **not implemented in the backend**. Frontend onboarding/scan mocks do not establish those API capabilities. Manual expense input, correction/PATCH, lists, summaries, category maintenance and recurrence UI remain incomplete. A real first-login flow stops at missing category endpoints.

## Specification and remaining issues

[ADR-0005](decisions/adr-0005-api-handoff-baseline.md) remains the API baseline; [ADR-0006](decisions/adr-0006-integrated-client-and-backend.md) records observed implementation/tooling and the limits of backend proposals. [Contracts](engineering/contracts.md), [model](engineering/domain-model.md), and [architecture](engineering/architecture.md) separate intended endpoints from actual source.

The integration repairs token-operation exception completion and adds four client regression tests; these are unrun without Flutter. Backend tests now require both emulator hosts. A bounded retry fixes observed Firestore profile-contention exhaustion; the full local emulator suite passes all 14 tests, independently repeated. Known follow-ups include inaccessible URL settings before profile/onboarding recovery and unsupported HTTP methods mapped to 500. Exact observed checks, versions and residual risks are in [integration review](development/integration-review.md); do not infer a passing Android build, deployed Firebase/Cloud Run, complete API or live OCR.

## Work registers and next actions

- [Frontend](development/frontend-tracker.md): auth/onboarding/upload/detail/settings source is partial; runtime and real integration gates remain open.
- [Backend](development/backend-tracker.md): scaffold/auth/profile present; slices 02–07 remain planned; implementation and checks are recorded per gate.
- [Infrastructure](development/infrastructure-tracker.md): local Python/Java/Node verification tooling and CI/config artifacts exist; production configuration/deployment and Flutter are unresolved.

Complete backend categories next to unblock real onboarding, supply Firebase platform configuration and deployment inputs, and resolve the [remaining questions](open-questions.md). Follow [maintenance](maintenance.md) for tracker updates. History/results live in [log](log.md); the earlier incomplete external reference review remains independent.

Local Android provisioning is now in progress with user authorization: Flutter 3.47.7 source is installed, Java 21.0.8 verified and user SDK paths configured; Dart/Android downloads and subsequent SDK/AVD/analyze/test/build checks are still pending in a logged local process. See [setup status](development/contributing.md#local-android-provisioning-in-progress-2026-10-17). This does not close frontend verification gates.
