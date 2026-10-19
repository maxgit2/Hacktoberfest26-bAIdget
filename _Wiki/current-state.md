---
title: Current state
status: active
updated: 2026-10-19
---

# Current state

## Inspected baseline

Freshness checked at local main `3b4cee3` on 2026-10-19. Since wiki publication/setup fix `4fa9754`, only README, the wiki log and Obsidian ignore entries changed; application/configuration/test source is unchanged. [SRC-007](raw/2026-10-19-post-hackathon-update.md) records the post-hackathon report and evidence limits.

Reconciled against main `b6d984e` on 2026-10-17, after merge `65d4bec` and deployment/schema fixes. The earlier integration report described `18c0d19` and is historical. The [audit inventory](development/repository-audit.md) accounts for the tracked files; [SRC-006](raw/2026-10-17-post-merge-audit.md) and [ADR-0007](decisions/adr-0007-merged-backend-baseline.md) record provenance and observed choices.

## What exists now

- **Backend source:** all 20 handoff operations plus root `GET /health` are registered, with categories/onboarding, expense CRUD/filtering/cursors, Gemini scan, monthly/yearly summaries and recurring conversion/rules/sync. [OpenAPI](../backend/openapi.json) has 15 paths/21 operations. Models, repositories, services and tests exist for all slices 00–07; this does not mean every acceptance gate passes.
- **Flutter source:** English sign-in/profile/onboarding, gallery/JPEG upload, saved read-only detail, Settings and bounded lifecycle sync. Empty API URL and `USE_FIREBASE=false` still default to fake auth/in-memory data. Manual input, correction/PATCH, list/filter/delete, category maintenance, recurring management and summary UI/repositories remain missing. Firebase platform files and Google Services Gradle integration are absent from tracked source.
- **Infrastructure:** backend CI, non-root Docker image definition, four Firestore indexes, deny-all client rules, GCP bootstrap and keyless GitHub→Cloud Run deploy workflow exist. The handoff retains a historical HTTPS URL. The merged README reports the hackathon finished and cloud deployment shut down on 2026-10-17; do not treat that address as a maintained service. See [infrastructure](engineering/infrastructure.md) for settings, IAM, secrets and evidence limits.

## Verification and active problems

This audit parsed all 57 tracked Python files, matched router methods/paths to OpenAPI and all 20 handoff operations, and directly checked exact-money helpers. There are 72 backend test functions before parametrization and 25 Flutter test declarations. Full suites, schema regeneration, Ruff, Android/container builds and hosted CI were **not rerun** here: this Python 3.13 environment has no application/test dependencies and Flutter is unavailable. Earlier 14-test emulator success applies only to the earlier auth/profile slice, not the expanded backend.

Read-only HTTPS probes of the handoff service during this audit returned **500 for /health and 503 for /v1/me and /v1/openapi.json**, with HTML service errors. These are historical 2026-10-17 observations, not a current incident diagnosis. The later shutdown report does not establish their cause; no authenticated business or live Gemini operation was attempted. The existence of a deploy workflow is not a successful deployment result.

Source review found important remaining mismatches: frontend max excludes Other while backend includes it; general expense responses expose stored scan cents keys rather than the upload response's money keys; recurrence `has_more` stays true whenever more than 20 rules are active; lifecycle client stops after five rounds and suppresses errors. Unsupported methods still map to 500, Settings recovery is unavailable before onboarding, and scan currency is relabeled EUR without validating extracted currency. See the [current review](development/integration-review.md#post-merge-audit-at-b6d984e) for evidence and priorities.

## Next work

For any resumed integration, provision/configure a backend and collect fresh runtime evidence; supply and test Android Firebase configuration; reconcile the recorded API/client mismatches; implement editable scan review and remaining UI. Validate indexes for actual combined queries and run the full emulator/Flutter suites. Work owners remain unassigned in the [frontend](development/frontend-tracker.md), [backend](development/backend-tracker.md) and [infrastructure](development/infrastructure-tracker.md) registers. [Open questions](open-questions.md) now distinguish answers observed in code from remaining acceptance/operational decisions. The README additionally reports 90 automated tests, green CI on every merge and a successful live scan before shutdown; these historical results were not independently reproduced here and do not close the remaining gates. No code fix, cloud mutation, commit or publication is part of this documentation check.
