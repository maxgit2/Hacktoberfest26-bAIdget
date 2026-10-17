---
title: User flows
status: active
updated: 2026-10-17
---

# User flows

Authority: [SRC-004](../raw/2026-10-17-frontend-handoff.md), [ADR-0005](../decisions/adr-0005-api-handoff-baseline.md). These target flows have partial implementation: frontend 6d9baea supplies auth/profile/onboarding/upload/detail/settings and mocks; backend 18c0d19 supplies health/auth/profile only. The synthetic demo is not a complete real backend flow. See [setup](../development/contributing.md) and [integration review](../development/integration-review.md). The frontend handoff establishes English UI and gallery-only input.

## Google authentication and onboarding

1. Sign in with Google via Firebase Auth and Google Sign-In in the backend's Firebase project.
2. GET /me creates/returns the profile. If onboarding_completed is false, load GET /categories/catalog.
3. Presets preselect catalog items; user selects at least two catalog/custom categories and submits POST /categories/onboarding. Backend adds Other and marks onboarded.
4. Use category CRUD after onboarding; identify Other by is_other rather than editable name. On category_in_use, tell the user to move/delete referenced expenses first; active rules can also block deletion.

For API requests fetch the Firebase ID token, send Bearer auth, force refresh/retry once on 401, then sign out if still unauthenticated. The SDK is Auth-only; never access Firestore directly or send owner. Device fingerprint identity from SRC-003 is superseded.

## Start/resume and online state

The handoff triggers POST /recurring-rules/sync at every app start/resume, described as fire-and-forget, then loads categories/expenses/summary. Follow has_more with further idempotent sync calls. Ordering of initial display, completion refresh, failure/retry and overlapping resume calls needs clarification; do not assume fire-and-forget makes newly generated records immediately visible.

The app is online-only. Show request/loading/error states rather than implying an offline editing/sync protocol.

## Manual expense and shared edit form

Generate UUIDv4 before POST /expenses and retain it across retries. Supply date/category/EUR plus optional amount/seller/title/description. The API creates a single expense, returning 201 or 200 for a repeated expense ID belonging to that user. Do not send owner or read-only type/source/timestamps. Missing currency behavior is an OpenAPI question despite the stated EUR default.

The earlier shared manual/post-scan form design remains useful; use current field/validation rules. Manual submission creates the record; editing a saved record uses PATCH. Null clears optional fields. Keep local form edits during recoverable errors; no endpoint for changing a saved expense's ID/type/source exists.

## Scan: save first, review afterward

Select a receipt/payment screenshot from the gallery; current frontend decisions exclude camera capture. Client code prepares JPEG at most 2048px long side/quality85 and retains a UUID for scan retry. Only the mock currently responds; real backend scan/PATCH correction is still planned.

Show a loader and use client timeout 45 seconds; the handoff's 3–10 seconds is an estimate. Retry timeouts with the same ID. The response is **already saved**, so there is no confirmation/create step afterward. Display the expense and allow PATCH correction; highlight needs_review and send false after review. Other is classification fallback. If neither merchant nor total is extracted, the API reports extraction_failed and creates nothing. Backend image storage is explicitly excluded by the contract.

This supersedes the earlier proposed pre-save draft workflow; a saved uncertain record still requires validation/correction. Cancellation after upload is not a guarantee of no saved expense. Recover by retrying the same operation ID or retrieving the result under the agreed client flow.

## Expense list and deletion

Use server filters (inclusive from, exclusive to, category ID, type, needs_review), date-descending order, and opaque pagination cursor. Display optional fields/null amount honestly; use server summaries for totals. PATCH an occurrence changes only it. DELETE soft-deletes; hide deleted records and do not infer that deleting an occurrence stops its series.

## Recurring series

Convert an existing expense with make-recurring (weekly/monthly/yearly; optional inclusive local end_date). It becomes the first occurrence and the backend catches up missing ones through today.

Use rules endpoints for future series changes; frequency/start cannot change. Rule deletion stops future generation but leaves created expenses. Reactivation does not backfill a paused interval. Monthly 31st clamps to shorter-month end and returns to the original day later. App lifecycle sync is required; no cron dependency is declared.

## Summaries and later scope

Use monthly/yearly summary endpoints: server Europe/Rome boundaries, EUR totals/category shares, uncounted amount-less records, and 12 yearly month buckets including zero months. Archived categories with expenses remain visible in summaries. Percentages may not sum to exactly 100.

Weekly summaries and current/previous comparison presentation from SRC-003 are not specified by this handoff; keep them as integration gaps rather than computing totals from expense lists. Family, email import, bulk scan, voice, other currencies, offline mode, and budgets are explicitly out of scope for now.

See [scope](scope.md), [contracts](../engineering/contracts.md), and [frontend tracker](../development/frontend-tracker.md) for acceptance gates and implementation status.
