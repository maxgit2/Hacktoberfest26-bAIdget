---
title: ADR-0005 API handoff integration baseline
status: active
updated: 2026-10-17
---

# ADR-0005: API handoff as the current integration baseline

- Decision status: **accepted as the supplied documentation/integration baseline**, not a claim of implemented or tested services.
- Date: 2026-10-17.
- Authority: initiator supplied [SRC-004](../raw/2026-10-17-frontend-handoff.md) as updated specifications and requested wiki reconciliation plus three maintained work trackers. The backend author/owner is unnamed; no separate team approval is inferred.
- Supersedes: [ADR-0004](adr-0004-updated-product-baseline.md) for current integration scope. Its broader roadmap is preserved as deferred/unsupported work, rather than silently treated as delivered. [ADR-0003](adr-0003-flutter-scaffold.md) still establishes only the Flutter scaffold.

## Declared changes

| Area | Earlier baseline | Current handoff |
| --- | --- | --- |
| Identity | Smartphone ID/fingerprint | Google sign-in through Firebase Auth; Firebase ID token verified by backend |
| Access | Firebase services/ownership boundary open | Client uses Firebase only for Auth; all business data via API; Firestore locked to clients is a requirement to verify |
| Expense identity/type | No ID; `concurrent {info}` undefined | Client UUIDv4 recommended for retry safety; server may generate omitted IDs; `single\|recurring` with rule reference |
| Money/time | Optional float, euro encoding/timezone open | EUR only; optional amount, positive bounded number with at most two decimals; UTC responses, server Rome month/year boundaries |
| OCR save/review | Proposed draft/confirmation before save | Scan creates a saved expense immediately; user edits with PATCH and clears `needs_review`; no extra confirmation endpoint |
| Categories | Template content/limits/deletion open | Catalog/presets, 2–30 categories and auto-added Other; onboarding, CRUD and in-use protections declared |
| Recurrence | Unspecified info/optional cron | Rules plus idempotent sync at app start/resume; occurrence edits and series edits differ; no cron dependency is specified |
| Summaries | Weekly/monthly/yearly/comparisons | Monthly/yearly server endpoints; weekly and comparison presentation are not specified |
| Scope | Later email/budget milestones | Personal, online-only, EUR; email, budgets, family, bulk scan, voice, other currencies/offline excluded for now |

See [contracts](../engineering/contracts.md), [model](../engineering/domain-model.md), and [flows](../product/user-flows.md) for details. DeepSeek-OCR remains a name from SRC-003, not a provider/version reaffirmed by SRC-004; deployment/model selection still needs evidence.

## Historical intake limits and remaining reconciliation

At SRC-004 intake, no `openapi.json`, API host, emulator address, backend source, Firebase configuration/rules, or service tests were available. Current main supplies full backend/OpenAPI/deploy/URL artifacts; see [ADR-0007](adr-0007-merged-backend-baseline.md) and [current contracts](../engineering/contracts.md). Mobile platform configuration, runtime verification and explicit drift resolution remain open. Resolve schema/text differences and underspecified cases with the backend owner through the team's normal channel; this task does not authorize sending messages. Code now answers category maximum counting and recurrence timezone/leap dates; client-limit mismatch and lifecycle completion remain open. Preserve historical questions while updating their current evidence.

SRC-004's broad “no confirmation” rule supersedes the wiki's proposed pre-save boundary, while backend validation and human correction remain required trust boundaries. A saved record with uncertain extraction is reviewable data, not trusted model authority.

## Tracking choice and consequences

The user explicitly requested separate maintained [frontend](../development/frontend-tracker.md), [backend](../development/backend-tracker.md), and [infrastructure](../development/infrastructure-tracker.md) registers. Their milestone labels are proposed work breakdowns, not the source's release numbers or deadlines. Use stable task IDs, explicit owners/statuses, dependencies and completion evidence under [maintenance](../maintenance.md). Source-defined behavior alone cannot make an implementation task done.
