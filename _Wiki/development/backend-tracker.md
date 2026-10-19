---
title: Backend activity and milestone tracker
status: active
updated: 2026-10-19
owner: unassigned
---

# Backend activity and milestone tracker

Freshness checked at `3b4cee3` on 2026-10-19: backend source/tests unchanged. [SRC-007](../raw/2026-10-19-post-hackathon-update.md) records teammate-reported 90 tests, green CI and live scan success before shutdown; no run logs/results were independently collected or tests rerun here. These reports supplement the earlier evidence without closing unverified gates or source findings. The latest README log's claim that this tracker only covered slices 00-01 is incorrect; `9482e3c` already covered 00-07.

Reconciled at main `b6d984e`; slices00–07 now have source and tests. `unverified` below means implementation exists but the complete completion gate was not executed/proven by this audit, not that the feature is absent. Earlier14-test success covered auth/profile only. Owners unassigned; source executor labels are not current assignments. [Review](integration-review.md#post-merge-audit-at-b6d984e), [maintenance](../maintenance.md), [contracts](../engineering/contracts.md).

| Milestone | Gate | Current state |
| --- | --- | --- |
| BE-M0 | Handoff plus runnable source and complete matching schema | Source, commands and snapshot present; static route match passed; runtime regeneration pending |
| BE-M1 | Firebase ownership and profile/categories | Auth/profile earlier emulator evidence; categories code/tests present, full current validation pending |
| BE-M2 | Expense CRUD/idempotency/extraction | Code/tests present, serializer/currency/retry issues recorded, runtime/provider acceptance pending |
| BE-M3 | Recurrence/summary accounting | Code/tests present; sync completion issue and full-suite acceptance open |
| BE-M4 | Complete reproducible acceptance and delivery | CI/deploy artifacts present; hosting reported shut down, reproducible acceptance gates open |

| ID | Milestone | Status | Owner | Activity / completion gate | Evidence / dependency |
| --- | --- | --- | --- | --- | --- |
| BE-01 | BE-M0 | done | Unassigned | Preserve handoff and canonical documentation | SRC-004/ADR-0005 preserved; SRC-006 reconciles later source |
| BE-02 | BE-M0 | in-progress | Unassigned | Source/start/schema/address delivery and matching runtime schema | backend/openapi.json:15 paths/21 operations, all 20 handoff operations present; router static match passed; runtime export/snapshot test unrun, INF-10 |
| BE-03 | BE-M1 | done | Unassigned | Earlier Firebase-token/profile provisioning, concurrency and two-user isolation gate | Historical14 passing emulator tests in earlier review; no claim full current suite passed |
| BE-04 | BE-M1 | unverified | Unassigned | Categories/catalog/onboarding/CRUD/Other/ownership acceptance | Models/router/services/repository and test_categories.py now exist; min 2, total 30 incl Other; current emulator suite unrun; client limit FE-15 |
| BE-05 | BE-M2 | unverified | Unassigned | Expense CRUD/UUID/money/time/nulls/filter/cursor/delete/isolation acceptance | Full code/test_expenses.py; cents probes passed, test suite unrun; BE-13 serialization remains |
| BE-06 | BE-M2 | unverified | Unassigned | Image validation/quota/provider/errors/review/privacy acceptance | imaging/llm/scan/rate_limit code, mocked test_scan/test_imaging/schema; ten text-only eval cases; historical live scan reported in SRC-007, no independent accuracy benchmark; BE-15/16 |
| BE-07 | BE-M3 | unverified | Unassigned | Conversion/sync/idempotency/pause/month-end/isolation acceptance | recurrence/recurring/rules code and tests; isolated UTC date/ID probes passed; Rome emulator tests unrun; BE-14 |
| BE-08 | BE-M3 | unverified | Unassigned | Exact summaries/null/count/DST/history/12-month acceptance | summary service/models/router and test_summary.py now present; count excludes nulls; full checks unrun |
| BE-09 | BE-M4 | in-progress | Unassigned | Health/errors/OpenAPI/pagination/rate metadata accepted | operation IDs, responses/examples and snapshot exist; AST route match passed; BE-12/13, INF-10 |
| BE-10 | BE-M4 | in-progress | Unassigned | Full reproducible lint/emulator/contract/container/handoff evidence | 72 backend test functions before parametrization; CI definition exists, dependencies absent in prior audit; README now reports 90 tests/green CI, hosted run evidence not collected |
| BE-11 | Future | deferred | Unassigned | Email/budgets/family/bulk/voice/currencies/offline/weekly extensions | No implemented routes; outside current contract |
| BE-12 | BE-M4 | todo | Unassigned | Resolve unsupported-method error mapping | HTTP handler still converts405 to 500; earlier reproduction retained; agree code/status and add regression |
| BE-13 | BE-M2 | todo | Unassigned | Unify scan_details shape across upload/read/list/PATCH/conversion | A-01: _scan_response converts cents, _expense_response does not; isolated function-body probe reproduced drift; test reloads |
| BE-14 | BE-M3 | todo | Unassigned | Make sync has_more express actionable remaining work | A-03:21 non-due fake rules →0 created/20 processed/has_more=true using actual sync body; coordinate client cap/refresh Q-21/26 |
| BE-15 | BE-M2 | todo | Unassigned | Agree and enforce extracted currency/quantity/VAT semantics | A-06: currency ignored→EUR, quantities reuse money precision, zero VAT invalid; Q-29/30 |
| BE-16 | BE-M2 | todo | Unassigned | Verify concurrent/deleted-ID scan retry costs and failure order | A-07: deleted get returnsNone before paid extraction, final tombstone404; concurrent fresh IDs can invoke provider twice; no runtime reproduction claimed |

No feature milestone is done merely because route/source/tests exist. For resumed development, prioritize configured local/runtime evidence, response compatibility and current full suite, then client integration. Append transitions to [log](../log.md); dependent [frontend](frontend-tracker.md) and [infrastructure](infrastructure-tracker.md) gates are reconciled.
