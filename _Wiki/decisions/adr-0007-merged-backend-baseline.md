---
title: ADR-0007 Merged backend MVP baseline
status: active
updated: 2026-10-17
---

# ADR-0007: Record the merged backend MVP baseline

- Decision status: **accepted for documentation reconciliation**, explicitly requested by the initiator in [SRC-006](../raw/2026-10-17-post-merge-audit.md). The merged technical choices below are observed implementation, not newly inferred human approval of every backend contract extension.
- Date: 2026-10-17.
- Evidence: main `b6d984e`, merge `65d4bec`, [backend source](../../backend/app/main.py), [OpenAPI](../../backend/openapi.json), [deployment](../../.github/workflows/deploy.yml).
- Relationship: extends the implementation inventory in [ADR-0006](adr-0006-integrated-client-and-backend.md). [ADR-0005](adr-0005-api-handoff-baseline.md) remains the supplied product/API baseline; earlier decisions and raw records remain historical.

## Context and choice

Code added after the initial integration implemented slices02–07 without corresponding wiki updates. Maintain source-grounded canonical pages that distinguish source presence, local checks, hosted checks, deployed availability and client integration. Keep the requested [audit ledger](../development/repository-audit.md) as the resumable file inventory.

## Observed choices and alternatives

Merged source uses integer cents plus Decimal validation rather than float arithmetic, trimmed/casefold active category names (1–40 chars), 30 active categories including Other, soft archives/deletes, deterministic UUIDv5 generated occurrences and per-rule Firestore transactions. Recurrence anchors are Europe/Rome with month-end/leap-day clamp and caps50/20; summaries stream documents and aggregate in Python rather than rollups. Scan uses Pillow plus async google-genai structured extraction, category allowlist fallback and persisted review flags. [Backend proposals](../../backend/specs/open-questions.md) supply rationale but their internal adoption label is not independent evidence of full human agreement.

Cloud Run delivery uses GitHub OIDC/WIF, Secret Manager runtime injection and a non-root image rather than a committed service-account key. These alternatives describe the source design; no new framework/provider benchmark or selection was performed. Backend dependencies remain unpinned and Gemini uses a mutable model alias. Flutter still defaults to mocks and lacks the full feature UI and platform Firebase setup.

## Consequences and follow-up

Backend features must no longer be marked absent, while full product milestones stay open pending [verification and mismatches](../development/integration-review.md#post-merge-audit-at-b6d984e). Do not silently bless differences such as currency coercion, category-limit drift, scan-details serialization or sync completion. Record them in [questions](../open-questions.md) and trackers. Current public service probes returned500/503; deployment artifacts do not establish healthy availability. No API/feature implementation was altered by this decision record.
