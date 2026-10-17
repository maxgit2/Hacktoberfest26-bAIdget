---
title: Infrastructure activity and milestone tracker
status: active
updated: 2026-10-17
owner: unassigned
---

# Infrastructure activity and milestone tracker

Canonical tools/config/deployment register. The prior testing query correctly observed new backend/CI artifacts and default Node/Flutter limits; merge verification now adds an isolated Python 3.12 environment, Java/Node paths and local check evidence. No cloud deployment is implied. Owners remain unassigned. Gates are proposed work breakdowns; [maintenance](../maintenance.md) and [integration review](integration-review.md) govern evidence.

| Milestone | Gate | Current state |
| --- | --- | --- |
| INF-M0 | Traceable repository/wiki baseline | Source/history preserved; merge publication authorized |
| INF-M1 | Frontend/backend tools and real shared Firebase config | Backend verification tools available; Flutter/Conda/config missing |
| INF-M2 | Deployed API/data/extraction runtime | Local scaffold/emulator config/CI/container exist; cloud/OCR absent |
| INF-M3 | Reproducible full access/health/limits/operational handoff | Partial local checks; complete API/Android/deployment gates open |

| ID | Milestone | Status | Owner | Activity / completion gate | Evidence / dependency |
| --- | --- | --- | --- | --- | --- |
| INF-01 | INF-M0 | done | Unassigned | Repo/wiki/checker tracked and local wiki preserved during merge | Main 6d9baea + dev 18c0d19; safety stash 9046be8 retained; personal Obsidian/editor state ignored |
| INF-02 | INF-M1 | in-progress | Unassigned | Compatible tools plus actual Flutter/device/backend checks | Python 3.12.14 venv, Java 21.0.8, Node 24.19.0, Firebase CLI 15.34.0 available; local Ruff passes; Flutter/Dart/Conda/Docker unavailable |
| INF-03 | INF-M1 | blocked | Unassigned | Real Firebase project/Google platform registration/token setup | Emulator project demo-baidget is configured; real platform credentials/config not supplied; FE-03 remains unverified live |
| INF-04 | INF-M2 | in-progress | Unassigned | Source/start/container/CI/schema/address delivery | backend/README, Dockerfile, CI and emulator ports 8080/9099 supplied; /health root and /v1/me confirmed; complete OpenAPI and production host/deployment missing |
| INF-05 | INF-M2 | unverified | Unassigned | Prove client Firestore denial/backend scoped access in target environment | deny-all firestore.rules source exists; emulator profile tests cover backend paths, not production client-rule deployment |
| INF-06 | INF-M2 | blocked | Unassigned | Actual extraction provider/runtime/secrets, image/rate/time limits and retention evidence | Gemini/Cloud Run named as backend targets; env template is not a validated model/runtime; slice 06 absent |
| INF-07 | INF-M3 | in-progress | Unassigned | Reproducible health/auth/ownership/Firestore/retry/provider/recurrence checks | Partial service checks in review; most API endpoints/Android integration missing; coordinate BE-10/FE-11 |
| INF-08 | INF-M3 | in-progress | Unassigned | Safe secrets/diagnostics, CI commands and repeatable deployment checks | Env example, non-root Dockerfile and emulator CI supplied; generated debug log removed/ignored; test guard rejects missing emulator hosts; hosted CI/container/cloud unrun |
| INF-09 | Future | deferred | Unassigned | Inbox/workers, budget notifications, offline sync and optional cron | No current contract or implementation; recurrence planned through API sync |

Local test tooling was installed only in temporary/cache locations; no dependency was added/upgraded in project manifests. Exact observed versions and checks are in the review. See [frontend](frontend-tracker.md), [backend](backend-tracker.md), [setup](contributing.md); update gates/evidence in the shared [log](../log.md), including explicit failures/unrun checks.

2026-10-17 local provisioning update: INF-02 remains in-progress. Flutter 3.47.7 source installed; Dart and Android tools downloads pending. Java 21.0.8 verified, user PATH/ANDROID_HOME configured. A logged local setup process continues SDK/AVD/build/test provisioning; Android acceleration and all frontend runtime gates remain unverified. See [setup](contributing.md#local-android-provisioning-in-progress-2026-10-17).
