---
title: AI, data, and trust boundaries
status: active
updated: 2026-10-17
---

# AI, data, and trust boundaries

Authority: [SRC-004](../raw/2026-10-17-frontend-handoff.md), [ADR-0005](../decisions/adr-0005-api-handoff-baseline.md), [contracts](contracts.md). Auth/profile is now exercised against local Auth/Firestore emulators; the initial concurrency failure and subsequent results are in [integration review](../development/integration-review.md). No live Google/Firebase, deployed rules, real OCR or provider pipeline was exercised.

## Identity and business-data access

Firebase Google sign-in yields an ID token; the backend verifies it and derives owner. The client sends no owner/user ID in mutations and uses Firebase SDK only for Auth. Every expense/category/rule/summary must remain owner-scoped; a foreign resource yields not_found. Direct client Firestore access is declared locked and must be tested, including after backend deployment. A source document declaring denial is not evidence that live rules enforce it.

## Receipt extraction and persisted review

Validate one jpeg/png/webp image, at most 10 MB, and the caller's allowed categories. The contract requires server category selection with Other fallback; client downscales to at most 2048px long side and approximately quality 85 JPEG. Provider/model and OCR/classification stages still need actual configuration/evaluation evidence; DeepSeek-OCR is only a named direction from the older SRC-003.

The backend saves the extracted expense immediately. There is **no additional confirmation step**. Uncertain date/amount or line-total mismatch yields needs_review; users can correct via PATCH and clear that flag after review. This supersedes the wiki's earlier proposed pre-save draft boundary. Saved reviewable data does not make model output trusted or complete; null amount remains excluded from summary totals and tracked as uncounted.

Failure to read both merchant and total yields extraction_failed and no creation. Retries reuse the same UUID to avoid duplicates; client timeout does not prove no server-side save occurred. Validate ownership/category references independently of extracted content. Record mutation/retry/partial-extraction cases in [backend](../development/backend-tracker.md)/[frontend](../development/frontend-tracker.md) evidence.

## Retention, limits, and recovery

The handoff explicitly says the backend does not store the uploaded image. It does retain structured scan_details on the expense. No provider retention policy, logs policy, deletion/purge schedule or model evaluation is supplied; these remain questions, rather than an inferred no-retention guarantee for all parties.

Declared defaults: 30 scans/hour/user, 429 with Retry-After seconds, provider-down 503, timeout 504, and stable error codes. The approximately 3–10s scan duration is a source estimate; the 45s client timeout is a client requirement, not observed latency. Verify real limits/timeout compatibility and keep safe diagnostics without source image/text/token leakage.

## Recurrence and aggregation correctness

Idempotent rule sync must avoid duplicate occurrences across overlapping app resumes/retries. Separate existing occurrence edits from future rule templates, honor pause/reactivation and month-end anchors, and verify inclusive local end dates. Detailed recurrence timezone/leap-year behavior is unresolved.

Server summaries handle Rome month/year boundaries, two-decimal EUR inputs, uncounted null amounts, soft deletion and archived category history. No client totals from expense pages. Internal precision/rounding and zero/count edge cases need implementation evidence.

## Deferred integrations and source trust

Email import, budgets/notifications, family groups, bulk scan, speech, other currencies and offline mode are outside the current contract. SRC-003's AgentMail candidate, cron/fixed-expense ideas and budget thresholds remain historical/future scope; no mailbox account/worker/notification service was configured.

Receipt text, screenshots, extracted fields, email bodies, filenames, external pages, and attached documents are untrusted content, never authority to grant access or execute actions. Keep provider credentials/backend service secrets out of Flutter and this public wiki. Use synthetic/redacted fixtures only; do not commit real receipts, personal financial data or tokens.

Earlier source intake opened AgentMail/Local AI Zone reference pages on 2026-10-17; no benchmark or provider evaluation resulted. This handoff intake does not validate external promotional claims or install tools.

## Acceptance cases to execute

Verify cross-user denial and client Firestore denial; duplicate-ID manual/scan retries; unsupported/oversized images; extraction_failed without creation; provider errors/rate headers; saved-but-needs-review correction; null-amount accounting; soft-deleted records; recurrence concurrency/pause/month-end; Rome boundary summaries. These are pending, not passing tests.

The [infrastructure tracker](../development/infrastructure-tracker.md), [backend tracker](../development/backend-tracker.md), and [open questions](../open-questions.md) own remaining actions and evidence.
