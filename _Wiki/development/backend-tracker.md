---
title: Backend activity and milestone tracker
status: active
updated: 2026-10-17
owner: unassigned
---

# Backend activity and milestone tracker

Canonical FastAPI register. Integration of dev 18c0d19 delivers slices 00/01; the earlier source-absent inventory/testing-query correction is now reconciled. [Backend tasks](../../backend/specs/tasks/00-scaffold.md) describe future work, not completed features. Owners are unassigned; executor labels in source plans do not assign a human owner. Use [maintenance](../maintenance.md), [review](integration-review.md), [contracts](../engineering/contracts.md).

| Milestone | Gate | Current state |
| --- | --- | --- |
| BE-M0 | Handoff plus runnable source and complete schema | Source/manifests/partial generated schema present; complete export missing |
| BE-M1 | Firebase ownership and profile/categories | Auth/profile source present; categories absent |
| BE-M2 | Expense CRUD/idempotency/extraction | Not implemented (slices 03/06) |
| BE-M3 | Recurrence/summary accounting | Not implemented (slices 04/05) |
| BE-M4 | Complete reproducible acceptance and delivery | Local partial checks; full API/container/deployment still open |

| ID | Milestone | Status | Owner | Activity / completion gate | Evidence / dependency |
| --- | --- | --- | --- | --- | --- |
| BE-01 | BE-M0 | done | Unassigned | Preserve handoff and canonical documentation | [SRC-004](../raw/2026-10-17-frontend-handoff.md), ADR-0005, current contract/trackers |
| BE-02 | BE-M0 | in-progress | Unassigned | Source/runtime/start commands and complete matching OpenAPI delivered | backend/ now present; Conda Python 3.12 manifest, README, /v1/openapi.json partial runtime schema; complete snapshot planned slice 07, host/config missing |
| BE-03 | BE-M1 | done | Unassigned | Verify current Firebase-token/profile ownership, repeat/concurrent provisioning and two-user isolation; future domains tested in their own gates | Local emulator suite: 14 passed, independently repeated; bounded contention repair and two new regressions verified. [Review](integration-review.md); categories remain BE-04 |
| BE-04 | BE-M1 | todo | Unassigned | Catalog/presets/onboarding/category CRUD/constraints/Other and ownership tests | Slice 02 is a plan only; no category router/repository/model/tests |
| BE-05 | BE-M2 | todo | Unassigned | Expense schema/UUID retries, cents/precision, time/nulls/filter/cursor/delete and owner tests | Slice 03 planned; no expense code; internal storage proposals not implemented |
| BE-06 | BE-M2 | todo | Unassigned | Image validation/rate/error/provider handling, saved review and no-retention tests | Slice 06 planned; google-genai/Pillow/env declarations only, no extraction code |
| BE-07 | BE-M3 | todo | Unassigned | Rule conversion/occurrences/sync/idempotency/pause/month-end and isolation | Slice 05 planned; deterministic IDs/Rome/caps are documented proposals, not code |
| BE-08 | BE-M3 | todo | Unassigned | Server summary counts/nulls/currency/Rome DST/archived category/12-month behavior | Slice 04 planned; no summary code; rounding/count proposals need evidence |
| BE-09 | BE-M4 | in-progress | Unassigned | Health/auth errors/schema metadata plus future pagination/rate headers | /health and /v1/me exist; stable normal error envelope tested/probed, unsupported-method mapping issue BE-12; no complete OpenAPI export |
| BE-10 | BE-M4 | in-progress | Unassigned | Reproducible full backend test/handoff evidence, covering each implemented slice and future endpoint acceptance | Existing auth/profile/error/health tests and local Ruff; full feature tests, Docker/hosted CI/deploy unverified; details in review |
| BE-11 | Future | deferred | Unassigned | Email/budgets/family/bulk/voice/currencies/offline and unsupported weekly/chart extensions | Contract excludes current scope |
| BE-12 | BE-M4 | todo | Unassigned | Agree/fix unsupported-method error mapping without inventing contract codes | Reproduced POST /health and POST /v1/me as 500 internal_error due HTTPException mapping; source handoff lacks 405 code, record contract decision before changing |

Finish slice 02 next; preserve source specs and surface ambiguities rather than guessing. Runtime evidence closes only the corresponding implemented slice, never categories/OCR by implication. Cross-register dependencies: [frontend](frontend-tracker.md), [infrastructure](infrastructure-tracker.md); append status changes to [log](../log.md).
