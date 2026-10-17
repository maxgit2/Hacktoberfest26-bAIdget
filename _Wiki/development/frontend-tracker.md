---
title: Frontend activity and milestone tracker
status: active
updated: 2026-10-17
owner: unassigned
---

# Frontend activity and milestone tracker

Current Flutter source at main `b6d984e` remains the partial auth/onboarding/upload/detail/settings client. Backend availability in source has advanced to every handoff operation, so absent API code is no longer its blocker. Mocks and test declarations do not close real configuration/runtime gates. Owners unassigned; [review](integration-review.md#post-merge-audit-at-b6d984e), [maintenance](../maintenance.md).

| Milestone | Gate | Current state |
| --- | --- | --- |
| FE-M0 | Root client/manifests/tests and baseline | Artifact gate done |
| FE-M1 | Real auth/API bootstrap, onboarding/category maintenance | Partial client, backend source exists; platform Firebase/real validation pending |
| FE-M2 | Expense CRUD and saved scan review | Gallery/upload/read-only detail exist; manual/PATCH/list/delete missing |
| FE-M3 | Recurrence and server summaries | Bounded lifecycle sync hook only; management/summary UI missing |
| FE-M4 | Android/runtime/integration/recovery | Toolchain/config unverified here; public backend unhealthy in audit probe |

| ID | Milestone | Status | Owner | Activity / completion gate | Evidence / dependency |
| --- | --- | --- | --- | --- | --- |
| FE-01 | FE-M0 | done | Unassigned | Root app/manifests/test-source artifact gate | lib/, pubspec/lock, test/api_test.dart and app_flow_test.dart present |
| FE-02 | FE-M1 | blocked | Unassigned | Complete schema, configured Firebase and real routing inputs | OpenAPI/address now supplied (BE-02); Android Firebase files/Google Services plugin absent and public probes500/503; INF-03/10 |
| FE-03 | FE-M1 | in-progress | Unassigned | Real Google/Firebase login and one-refresh retry integration | Adapter/interceptor present, USE_FIREBASE=false default; Firebase.initializeApp without supplied platform options/files, no live test |
| FE-04 | FE-M1 | in-progress | Unassigned | Catalog/presets/custom onboarding and category CRUD/errors | Onboarding/read implemented; editing/category CRUD repositories/UI missing; backend source now present BE-04; FE-15 |
| FE-05 | FE-M2 | todo | Unassigned | Manual/shared expense edit/create/PATCH/null form with retry key | No create/PATCH client; backend source exists, runtime and BE-13 compatibility needed |
| FE-06 | FE-M2 | in-progress | Unassigned | Detail/list/filter/pagination/delete and occurrence/series distinction | Uploaded-object read-only detail only, no fetch/list/delete repository; server endpoints now exist |
| FE-07 | FE-M2 | in-progress | Unassigned | Gallery/JPEG/same-ID45s upload and editable persisted review | Picker/repository/upload present; correction missing; mock not live extraction proof; BE-06/13/15, INF-06/10 |
| FE-08 | FE-M3 | todo | Unassigned | Conversion/edit/stop UI and lifecycle completion semantics | Server rules/sync exist; AccountRepository loops max 5, home swallows errors, overlaps possible; Q-21/26 |
| FE-09 | FE-M3 | todo | Unassigned | Server monthly/yearly/category summary UI and models | No summary client/repository/UI; server summary source present BE-08 |
| FE-10 | FE-M4 | in-progress | Unassigned | Loading/error/retry and online recovery | Status/error messages/mock flow tests exist; real configuration/error recovery pending |
| FE-11 | FE-M4 | blocked | Unassigned | Run analyze/tests/debug APK and Android real/synthetic acceptance | 25 test declarations, unrun in audit: Flutter absent in PATH; previous machine's setup notes are historical, not this host's result |
| FE-12 | Future | deferred | Unassigned | Email/budgets/family/bulk/voice/currencies/offline/weekly/chart extensions | English UI/gallery-only baseline; no camera requirement |
| FE-13 | FE-M4 | in-progress | Unassigned | Verify token acquisition/refresh/sign-out exceptions complete | Four bounded regressions and interceptor fix present; no Flutter execution here |
| FE-14 | FE-M4 | todo | Unassigned | Settings URL recovery before profile/onboarding succeeds | Settings reachable only from upload; persisted invalid URL strands earlier gates; source finding retained |
| FE-15 | FE-M1 | todo | Unassigned | Reconcile onboarding max/name/icon behavior with real backend | A-02: client/mock30 picks+Other vs server30 total; mock/icons differ; Q-10, test boundary with server |

The upload source detail consumes the scan response; later GET/list/PATCH support must account for BE-13 rather than assume identical nested scan shape. API URL Settings permits arbitrary HTTP/HTTPS and bearer tokens follow the selected host; treat the URL as trusted developer configuration. No totals should be computed from paginated lists. See [backend](backend-tracker.md), [infrastructure](infrastructure-tracker.md) and [log](../log.md).
