---
title: ADR-0006 Integrated client and backend implementation choices
status: active
updated: 2026-10-17
---

# ADR-0006: Integrated client and backend implementation choices

- Decision status: **accepted for the committed implementation/tooling now integrated**; future backend proposals are not independently approved by this record.
- Date: 2026-10-17.
- Authority/evidence: initiator authorized downloading/reviewing dev, merging to main, then committing/pushing all changes. Main frontend is 6d9baea; dev backend is 18c0d19. [Integration source record](../raw/2026-10-17-integration-source-record.md) pins the evidence.
- Later evidence: [ADR-0007](adr-0007-merged-backend-baseline.md) extends this historical inventory to the full merged backend, domain persistence, extraction and deployment artifacts at b6d984e. Future-at-this-merge statements below are not the current feature inventory.
- Relationship: [ADR-0005](adr-0005-api-handoff-baseline.md) remains the target API contract; [ADR-0003](adr-0003-flutter-scaffold.md) is historical scaffold evidence, not current feature inventory.

## Observed choices and consequences at the initial integration

The client now uses Riverpod, Dio, preferences, Google/Firebase Auth adapters, UUID scan retry keys and gallery compression. Empty API URL/fake auth are deliberate development defaults. The [frontend handoff](../../docs/frontend-handoff.md) explicitly adds English UI and gallery-only input; backend handoff remains otherwise aligned. No camera implementation is required by the current frontend decision.

The backend uses FastAPI, Python 3.12 with Conda environment.yml, async Firestore repositories, threadpool token verification, transactional profile get-or-create, JSON error/request logging, local Auth/Firestore emulators, Ruff/pytest configuration, a non-root Dockerfile and CI. Dependency versions are unpinned; temporary venv validation is not a switch away from the declared Conda workflow. Only /health and /v1/me application endpoints are delivered.

Backend specs target Cloud Run EU and Gemini, and propose cents/Decimal money storage, category ID/name limits, Rome recurrence anchors/caps and other gap resolutions. They label adoption internally and cite a prior conversation not supplied here. Preserve those as documented backend proposals/targets; do not invent separate human acceptance, implemented future slices, validated Gemini model, deployed IAM/rules, or Cloud Run service.

## Merge hardening within existing behavior

Retain the protected local wiki/tracker work and all incoming frontend/backend commits. Exclude personal Obsidian state and generated emulator debug logs. Fix token-operation exception completion and require local emulator variables before tests; these preserve existing API behavior and do not add endpoints/schema fields.

Concurrency validation exposed profile transaction contention exhaustion. Retry once with a fresh transaction and 50–250 ms jitter only for SDK exhaustion caused by Aborted; unrelated errors propagate. This bounds attempts without changing the profile contract. Its verified diagnosis and limits are in the [contention lesson](../lessons/firestore-profile-contention.md) and [integration review](../development/integration-review.md). Unsupported-method mapping and pre-onboarding Settings recovery remain explicit follow-ups rather than silent contract changes.

## Verification and remaining scope

Source presence, mocks, emulator tests, declared schemas, CI files and deployed services are separate evidence levels. Use the [frontend](../development/frontend-tracker.md), [backend](../development/backend-tracker.md), and [infrastructure](../development/infrastructure-tracker.md) registers. No Flutter/container/hosted CI/production provider success is implied by this merge.
