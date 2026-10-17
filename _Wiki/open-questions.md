---
title: Open questions
status: active
updated: 2026-10-17
---

# Open questions

Current sources: [SRC-004](raw/2026-10-17-frontend-handoff.md), [ADR-0005](decisions/adr-0005-api-handoff-baseline.md), and [integrated source evidence](development/integration-review.md). “Resolved in contract” does not mean implemented/tested. IDs are retained; owners are unassigned. P0 blocks affected integration; P1 precedes the affected feature. Backend specs record additional proposed resolutions; their internal adoption label is not independent evidence of human acceptance here. No external messages are sent by this task.

| ID | State / priority | Current answer and remaining question |
| --- | --- | --- |
| Q-01 | Partial / P0 | Latest handoff defines current scope without numeric deadlines. Workstream milestones are proposed in the three trackers; which are the demo gates/assigned owners/dates? Older 0.1–5.0 list is historical/future. |
| Q-02 | Source direction verified; deployment P0 | Flutter/FastAPI/Firebase Auth and backend-only Firestore are present. Backend health/profile pass local emulator tests; deny-all client rules and CI/container are source artifacts. Production Firebase/config/addresses/deployment remain unverified; Q-20. |
| Q-03 | Resolved in contract | Google through Firebase Auth supersedes device fingerprint. Firebase ID token per call; forced refresh/retry once then sign-out on repeated auth failure; backend derives owner. SDK/provider configuration and isolation tests remain tracked work. |
| Q-04 | Resolved core; extension P1 | Expense category is a category ID; one category per expense. Scan line items are metadata, not an agreed split-allocation schema. Optional hierarchy/granularity remains unsupported. |
| Q-05 | Partial / P0 | Scan format/limits/saved review/errors are specified. Backend specs now target Gemini/Cloud Run and declare google-genai plus a model placeholder; extraction code and provider/model evaluation are absent. Older DeepSeek-OCR wording is historical. Confirm actual model/region/retention and provide acceptance evidence before claiming OCR integration. |
| Q-06 | Deferred | Email/AgentMail/address provisioning are outside current scope. Retain older requirements as future work; no current email endpoint or provider decision. |
| Q-07 | Resolved core; schema P0 | Shared manual/edit form uses POST single, PATCH edits, conversion/rules for recurrence. recurring replaces concurrent. Exact schema/nullable validation awaits OpenAPI (Q-22). |
| Q-08 | Partial / P0 | EUR-only JSON number, >0, <=1,000,000, <=2 decimals; amount may be null and uncounted. Internal rounding/storage and detailed summary counts remain Q-24. |
| Q-09 | Partial / P1 | Offset ISO requests, UTC Z responses, Europe/Rome month/year boundaries. Recurrence timezone/end/leap rules and comparison definitions remain Q-23/17. |
| Q-10 | Partial / P0 | Catalog/preset contents, min two selected/custom, max 30, Other auto-add/rename/no-delete, uniqueness and in-use checks supplied. Does max include Other, and how are duplicate catalog/custom names counted? |
| Q-11 | Partial / P1 | Backend does not store uploaded images; structured scan_details persists. Provider/log retention, purge policy and sensitive diagnostics handling are not supplied. |
| Q-12 | Source/tooling partial; runtime P1 | Riverpod/Dio client, layered async FastAPI/Conda Python 3.12 manifest, backend CI/container are present. Local temporary Python/Java/Node tools and 14 passing emulator tests are verified. Flutter/Dart/Conda/Docker and platform/deployed checks remain unavailable/unrun; exact evidence in review. No worker/cron is selected for current recurrence. |
| Q-13 | Resolved in current frontend source | docs/frontend-handoff.md explicitly specifies English UI; source screens are English. Product locale/format edge cases still require tests. |
| Q-14 | Open / P1 | Which Android demo device/API level, Firebase app registration, final application ID/signing and service-failure fallback will be verified? |
| Q-15 | Resolved in current frontend source | docs/frontend-handoff.md explicitly specifies gallery-only/no camera. ReceiptImagePicker uses ImageSource.gallery; no camera task is required by this baseline. |
| Q-16 | Resolved in contract | Personal owner-scoped app; family/sharing explicitly excluded for now. |
| Q-17 | Partial / P1 | Monthly/yearly/category endpoints supplied; weekly endpoint, current/previous comparison presentation, category hierarchy and selectable chart variants are not defined. Confirm extension scope; no totals from expense lists. |
| Q-18 | Deferred | Budget/alerts excluded; older 25/50/75/100% concept retained in SRC-003 without current endpoints/notification infrastructure. |
| Q-19 | Resolved core; future P1 | UUID create retry semantics and soft deletion supplied; owner/type/source/timestamps immutable. Deleted records excluded, returned deleted_at null; no restore/purge endpoint specified. Future retention policy remains Q-11. |
| Q-20 | Partial / P0 | Backend dev18c0d19 now supplies source/manifests/start/CI/emulators and partial runtime /v1/openapi.json; /health is at root and /v1/me exists. Complete committed snapshot (slice07), real Firebase platform config, production host/routing and named owner remain missing. |
| Q-21 | Open / P0 for lifecycle integration | Start/resume sync is called fire-and-forget but has_more requires follow-up calls. Agree completion refresh, errors/retries and overlapping resume handling so visible summaries do not imply finished generation. |
| Q-22 | Open / P0 for typed client | Resolve text/schema details: currency listed required with default; id optional at API but required client retry policy; precise nullability and recurrence/scan schemas. Validate all endpoints/errors against supplied OpenAPI when available. |
| Q-23 | Open / P1 | Recurrence declares weekly/monthly/yearly, inclusive local end, 31st clamp, future-only changes, no pause backfill. Which timezone, leap-day behavior and limits apply? Which inactive rules are listed? |
| Q-24 | Open / P1 | Summary total excludes nulls; uncounted is defined, but count/by-category count semantics, zero-total percentages and internal rounding are not. Confirm with schema/tests rather than guessing. |

## Keeping answers and tasks separate

Answers belong in [contracts](engineering/contracts.md), [model](engineering/domain-model.md), [flows](product/user-flows.md) or [scope](product/scope.md), with source/authority/date. Action/implementation status belongs in [frontend](development/frontend-tracker.md), [backend](development/backend-tracker.md), and [infrastructure](development/infrastructure-tracker.md). Update both when a blocker is resolved, preserving IDs and appending [log](log.md).
