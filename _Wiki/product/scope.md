---
title: Product scope
status: active
updated: 2026-10-19
---

# Product scope

Current client/API scope: [SRC-004](../raw/2026-10-17-frontend-handoff.md), [ADR-0005](../decisions/adr-0005-api-handoff-baseline.md). Current main `b6d984e` contains the full backend handoff route set and a partial Flutter client. [ADR-0007](../decisions/adr-0007-merged-backend-baseline.md) and the [current review](../development/integration-review.md#post-merge-audit-at-b6d984e) distinguish source delivery, missing client features, unrun checks and observed service errors. Earlier raw sources/scaffold decisions remain history.

## Post-hackathon status

[Hackathon submission on MLH](https://www.mlh.com/events/hacktoberfest-hack-day-milano-x-coding-bunker/submissions/01a14a07-ec0b-8893-8b60-eca85e30fdd3), supplied by the project initiator on 2026-10-19 and linked from the root README.

The merged README reports the hackathon finished and cloud hosting shut down on 2026-10-17; see [SRC-007](../raw/2026-10-19-post-hackathon-update.md). This changes the operational baseline, not feature acceptance. Its feature overview describes backend capabilities and does not establish missing Flutter screens. Local development remains possible through the documented emulator setup; hosted acceptance needs deliberately configured hosting if resumed.

## Current integration scope

Personal Android expense tracking, online-only and EUR-only, with English UI and gallery-only input under frontend handoff decisions. Firebase SDK use is Auth-only, and verified tokens establish backend ownership. Current default client mode is fake auth/in-memory data; family sharing remains excluded.

| ID | Current requirement | Evidence / implementation boundary |
| --- | --- | --- |
| REQ-01 | Firebase Google auth and one-refresh Bearer retry | Client SDK/adapter and backend auth present; fake default, real project configuration unverified |
| REQ-02 | Catalog/presets/custom onboarding, bounds, CRUD and Other protections | Backend categories/onboarding/CRUD code and tests present; Flutter only onboarding/read; server30 includes Other, client/mock30 excludes it |
| REQ-03 | One gallery receipt/payment image; immediate save and review correction | Backend Gemini scan/PATCH source and tests present; Flutter upload/read-only detail, no correction form; historical live scan reported, independent extraction acceptance unverified |
| REQ-04 | Manual single-expense create/edit/delete; optional amount; EUR; UUID retry key | Backend CRUD source and tests present; Flutter manual/edit/delete/list absent; owner/type/source/timestamps immutable |
| REQ-05 | Email import | Explicitly outside current scope; retain as deferred roadmap |
| REQ-06 | Monthly/yearly and category summaries, uncounted values, yearly 12 month buckets | Server summary source/tests present; client absent; weekly/previous-period extension not specified |
| REQ-07 | Navigate onboarding/categories, expenses, input/review, recurrence, summaries | Current home is upload only; complete feature navigation not implemented |
| REQ-08 | Expense/category/rule fields and error/idempotency/pagination conventions | [Domain model](../engineering/domain-model.md) and committed OpenAPI now exist; nested scan shape and textual drift remain |
| REQ-09 | Budgets/alerts | Explicitly outside current scope; no budget schema/endpoints |
| REQ-10 | Recurring rule conversion/edit/stop and idempotent sync on start/resume | Backend rules/sync present; client bounded lifecycle hook only, no management UI; has_more completion defect |

## Milestones and maintained work registers

The latest handoff does not assign release numbers or deadlines. The workstream milestones below are **proposed execution groupings** derived from it; no person/date is assigned without evidence. Task status, dependency, owner, and completion proof live in one canonical register per workstream:

- [Frontend tracker](../development/frontend-tracker.md): scaffold, auth/categories, expense/scan UI, recurrence/summaries, verification.
- [Backend tracker](../development/backend-tracker.md): source/OpenAPI delivery, identity/categories, expenses/extraction, recurrence/aggregation, verification.
- [Infrastructure tracker](../development/infrastructure-tracker.md): repo baseline, SDK/Firebase/environment, backend/data/OCR deployment, operational checks.

The [maintenance workflow](../maintenance.md) defines status updates. A contract claim is not a done implementation; tasks with unavailable implementation evidence remain unverified or blocked.

## Earlier numbered roadmap: historical/future scope

SRC-003 supplied 0.1 backend infrastructure; 1.0 device identity/templates/input; 2.0 deployment/categories/summaries; 3.0 email; 4.0 budgets and 25/50/75/100% alerts; 5.0 chart variants. Those labels are preserved in the immutable source, **not current delivery commitments**. Device identity is replaced; recurrence and category CRUD now belong to the declared integration contract. Do not defer them merely because an old version list was vague.

Email, budgets, family, bulk scan, speech-to-text, other currencies, and offline mode are explicitly out of scope now. Weekly summaries, period-comparison presentation, optional category hierarchy, camera capture, and chart-selection timing require clarification/extension. DeepSeek-OCR and AgentMail names from SRC-003 do not prove current provider adoption; the handoff does not name its extraction model.

## Acceptance gate

Verify on real configured client/backend: Google login and first/returning onboarding; category constraints/Other; owner isolation and error codes; UUID retries without duplicates; manual CRUD; scan saved-on-return/review correction/failure recovery; recurrence sync and separate occurrence/series edits; server summary totals/null handling/Rome boundaries; client Firestore denial. Source presence, mocked tests and historical auth/profile checks do not satisfy the complete product gate. Historical 2026-10-17 probes failed500/503; hosting is now reported shut down; see infrastructure evidence.

See [flows](user-flows.md), [contracts](../engineering/contracts.md), [questions](../open-questions.md), and the three registers for the exact remaining work.
