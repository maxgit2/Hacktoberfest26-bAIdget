---
title: Open questions
status: active
updated: 2026-10-17
---

# Open questions

Baseline `b6d984e`; [SRC-006](raw/2026-10-17-post-merge-audit.md), [contracts](engineering/contracts.md), [review](development/integration-review.md#post-merge-audit-at-b6d984e). IDs preserved. Owners unassigned. **Observed in code** resolves what source does, not independent product acceptance or runtime verification. Backend's internal ADOPTED AS PROPOSED statement is preserved in specs but is not corroborated human approval here. P0 blocks the affected integration/demo; P1 precedes the affected feature/operation.

| ID | State / priority | Current answer and remaining question |
| --- | --- | --- |
| Q-01 | Partial / P0 | MVP scope documented; milestones remain proposed gates with no assigned owners/deadlines. Confirm demo acceptance coverage and responsibility. |
| Q-02 | Source resolved; runtime P0 | Flutter/FastAPI/Firebase Auth/backend-only Firestore implemented in source; Cloud Run deploy/bootstrap/URL now exist. Service probes500/503, same-project mobile setup/live isolation unverified; Q-20/27. |
| Q-03 | Contract/source resolved | Firebase tokens, one forced client refresh and verified backend UID; check_revoked=false and no Google-only provider enforcement. Real provider/app/signing/denial checks remain INF-03/05. |
| Q-04 | Core resolved; extension P1 | One category ID per expense; scan items metadata, not split allocations. No category hierarchy implemented. |
| Q-05 | Source resolved; acceptance P0 | Async google-genai/Pillow pipeline implemented; gemini-flash-latest alias configured. Need healthy runtime, secret/model/version/region/retention and measured image extraction quality; no live eval result supplied. |
| Q-06 | Deferred | Email/AgentMail/mailbox provisioning have no endpoint/source implementation and remain outside MVP. |
| Q-07 | Source resolved; client P0 | Expense POST/PATCH/conversion/rules schemas and nullable validation present in OpenAPI/models. Shared manual/review form missing in Flutter. Text/schema drift Q-22/25. |
| Q-08 | Observed resolution | Backend stores integer cents via Decimal; nullable amounts excluded from counted summaries, EUR-only API. Amount request strings also accepted; extraction currency handling Q-29. |
| Q-09 | Observed resolution; consistency P1 | Offset requests→UTC Z; reports/scan TZ_NAME default Rome. Recurrence hardcodes Rome independently; should configurable TZ affect it or remain fixed? |
| Q-10 | Source answer; interoperability P0 | Server maximum 30 includes Other, names trimmed/casefolded and duplicates rejected. Client/mock maximum 30 excludes Other (31 total); reconcile and test upper bound. |
| Q-11 | Open / P1 | No durable image write in app; temporary UploadFile spooling not excluded. Provider region/retention/logs/purge/account deletion undefined; structured scan data persists. |
| Q-12 | Source resolved; tooling P1 | Riverpod/Dio and Conda Python 3.12/FastAPI/async Firestore/CI/container/deploy exist. Audit host lacks Flutter and Python app/test packages; no current full suite/build/hosted success claimed. Historical tools/results are not portable. |
| Q-13 | Resolved source | English UI with en_US/EUR formatting and device-local display times; localization/time-boundary edge tests remain. |
| Q-14 | Open / P0 for real Android demo | Need device/API level, Firebase app registration/Google Services integration, application ID/signing/SHA and demonstrated Google login/real API flow. |
| Q-15 | Resolved source | Gallery-only/no camera; ReceiptImagePicker uses gallery. Other platform runners are not verified support. |
| Q-16 | Resolved baseline | Personal owner-scoped app, no family/sharing implementation. |
| Q-17 | Core source resolved; extension P1 | Monthly/yearly/by-category server summaries implemented. Weekly/comparison/chart/hierarchy extensions unspecified; summary client absent. |
| Q-18 | Deferred | Budgets/alerts absent, no endpoints/notification worker. Bootstrap billing budget is infrastructure alerting, unrelated to expense budgets. |
| Q-19 | Source resolved; retention P1 | Soft deletion/UUID idempotency implemented; manual deleted ID→404, scan only returns 404 after possible image/quota/provider work. No restore/purge. Q-11 and Q-28. |
| Q-20 | Artifacts resolved; availability P0 | Full backend/OpenAPI/start/CI/deploy/rules/indexes and production handoff URL present. Mobile config missing; public service probe failed; source owner/run/revision success evidence absent. |
| Q-21 | Partial / P0 for lifecycle integration | Client loops at most5 and swallows sync errors; no overlap guard/completion refresh. Decide UI completion/retry behavior and truthful backlog signaling; Q-26. |
| Q-22 | Partial / P0 for typed integration | Snapshot now exists. currency omitted→EUR despite required/default prose; amount requests number|string; scan_details arbitrary; custom amount/UUIDv4 constraints incompletely encoded. Backend handoff vs frontend copy/report drift persists; reconcile approved contract and typed clients. |
| Q-23 | Observed source resolution | Rome anchor, monthly/leap-day clamp from start, inclusive local end, generated UUIDv5, caps20 rules/50 indexes, paused skip via resume_from, inactive listed/reactivatable. Runtime cap/concurrency/DST acceptance pending; Q-26. |
| Q-24 | Observed source resolution | count/category/month counts exclude nulls; uncounted separate; integer-cent aggregation, one-decimal HALF_UP percentages; empty categories empty, zero-total percentage branch0.0. Full current tests unrun. |
| Q-25 | Open / P0 for expense reload | Scan response converts cents metadata; general read/list/PATCH/conversion returns stored *_cents keys. Unify serializers/typed schema and test reload after scan; BE-13. |
| Q-26 | Open / P0 for sync completion | >20 active rules forces has_more=true even if none due. Due-first ordering helps catch-up but does not signal completion; client abandons after 5 rounds. Agree completion/pagination semantics; BE-14/FE-08. |
| Q-27 | Open / P0 | What causes current public health500/profile-schema503? Inspect Cloud Run revision/deploy/runtime logs and verify healthy probes without exposing secrets; INF-10. |
| Q-28 | Open / P1 | Concurrent fresh/deleted-ID scans may spend quota/provider work before deduplication/tombstone decision. Agree concurrency/retry reservation and error-order guarantees; BE-16. |
| Q-29 | Open / P0 for financial correctness | Extracted currency ignored, all results labeled EUR. Agree rejection/review behavior for non-EUR documents; do not claim conversion or other-currency support. BE-15. |
| Q-30 | Open / P1 | Quantities share positive two-decimal money validator; zero VAT becomes null/review. Define weighted quantity precision, zero money metadata and mismatch handling; BE-15. |
| Q-31 | Open / P1 | Validate deployed indexes for combined filters/rule category references and cross-domain category archive/write races. Source has four indexes and separate validation/write transactions; emulator success alone insufficient. |
| Q-32 | Open / P1 | Repository-only WIF condition/manual dispatch bypass of CI predicate need ref/environment protection review; live IAM/branch controls unverified. INF-12. |

Answers belong in canonical product/engineering pages with evidence, work status in [frontend](development/frontend-tracker.md), [backend](development/backend-tracker.md), [infrastructure](development/infrastructure-tracker.md). No external messages or approvals are fabricated by this audit.
