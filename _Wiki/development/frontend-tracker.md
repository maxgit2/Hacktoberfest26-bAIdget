---
title: Frontend activity and milestone tracker
status: active
updated: 2026-10-17
owner: unassigned
---

# Frontend activity and milestone tracker

Canonical Flutter register, reconciled with main 6d9baea plus merge hardening. Earlier testing-query notes correctly identified partial client source; the table now records it explicitly. Owners remain unassigned. Milestones are proposed gates, not releases/deadlines. See [maintenance](../maintenance.md), [integration review](integration-review.md), [contracts](../engineering/contracts.md).

| Milestone | Gate | Current state |
| --- | --- | --- |
| FE-M0 | Root client and documented baseline exist | Source gate done; counter replaced |
| FE-M1 | Auth/API bootstrap and category onboarding/CRUD | Partial mock/client source; real configuration and category API absent |
| FE-M2 | Expense CRUD and saved scan review | Gallery/upload/detail present; manual/edit/delete/list missing |
| FE-M3 | Recurrence and server summaries | Repository/mock sync hook only; feature/API missing |
| FE-M4 | Android/runtime/integration and recovery checks | Blocked by Flutter/config/incomplete backend |

| ID | Milestone | Status | Owner | Activity / completion gate | Evidence / dependency |
| --- | --- | --- | --- | --- | --- |
| FE-01 | FE-M0 | done | Unassigned | Root Flutter client/manifests/test sources exist; artifact gate only | 6d9baea: [app](../../lib/app.dart), [API tests](../../test/api_test.dart), [flow tests](../../test/app_flow_test.dart); old widget_test.dart removed |
| FE-02 | FE-M1 | blocked | Unassigned | Supply complete versioned OpenAPI, real Firebase/platform config and deploy/emulator routing inputs | Backend source/partial generated schema now present; complete snapshot/config/host still absent; BE-02, INF-03/04 |
| FE-03 | FE-M1 | in-progress | Unassigned | Complete Google/Firebase auth and one-refresh API behavior with real configuration | Auth adapter/interceptor/packages present; default fake auth; token-exception repair and tests in FE-13; real flow unverified |
| FE-04 | FE-M1 | in-progress | Unassigned | Profile/catalog/presets/custom onboarding and category CRUD/errors | Profile gate and onboarding/read source/mock routes present; category editing and backend category endpoints missing; BE-04 |
| FE-05 | FE-M2 | todo | Unassigned | Manual/shared editable expense form, create/PATCH/null validation and UUID retries | No manual/create/PATCH implementation; BE-05; read-only scan detail is not this gate |
| FE-06 | FE-M2 | in-progress | Unassigned | Expense detail/list/filter/pagination/delete and series distinction | Read-only detail exists; list/edit/delete/filter UI absent; BE-05 |
| FE-07 | FE-M2 | in-progress | Unassigned | Gallery/JPEG upload, same UUID retry/45s receive timeout, saved record correction and limits | Picker/scan repository/upload/detail exist; mock extraction only; PATCH review correction absent; BE-06, INF-06 |
| FE-08 | FE-M3 | todo | Unassigned | Rule conversion/edit/stop UI and complete lifecycle sync semantics | Account repository/mock sync hook present, not rule management or delivered server sync; BE-07, Q-21 |
| FE-09 | FE-M3 | todo | Unassigned | Server monthly/yearly/category summaries with uncounted and 12 months | No summary client/UI/server; BE-08 |
| FE-10 | FE-M4 | in-progress | Unassigned | Error/loading/retry and online-state recovery | Error mapping/status views and mock flow tests exist; FE-13/14 and real integration remain open |
| FE-11 | FE-M4 | blocked | Unassigned | Execute analyze/tests/Android acceptance with recorded toolchain/config/server evidence | 25 test declarations now present (18 API/model/mock, 7 widget); no Flutter/Dart executable available, all unrun here |
| FE-12 | Future | deferred | Unassigned | Email/budgets/family/bulk/voice/other currencies/offline and unsupported weekly/chart hierarchy extensions | Current contract excludes these; UI is English and gallery-only, not a camera TODO |
| FE-13 | FE-M4 | in-progress | Unassigned | Verify token acquisition/refresh/sign-out exceptions complete requests rather than hang | AuthInterceptor repaired; four two-second regression tests added; source/diff reviewed, Flutter execution blocked |
| FE-14 | FE-M4 | todo | Unassigned | Expose API URL recovery before profile/onboarding completes | Settings currently reachable from upload only; persisted invalid URL can strand startup; source finding in [review](integration-review.md) |

No milestone is promoted by mocks or test declarations. Next: backend categories to unblock real onboarding, Firebase config, Flutter checks, and FE-13/14 validation. Update rows/gates/evidence and shared [log](../log.md) with each delivery. Related: [backend](backend-tracker.md), [infrastructure](infrastructure-tracker.md).
