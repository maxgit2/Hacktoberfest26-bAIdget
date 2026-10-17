---
title: Recover bounded Firestore profile contention exhaustion
status: active
updated: 2026-10-17
---

# Recover bounded Firestore profile contention exhaustion

## Symptom and verified cause

The original dev 18c0d19 backend intermittently returned 500 when five first-login requests concurrently provisioned the same users/{uid} profile. The initial full emulator suite had 11 passes and one failure; a later reproduction returned one 200 and four 500 responses. This is independent of client auth mocks.

Instrumentation of installed google-cloud-firestore 2.34.1 showed repeated commit-phase Aborted exceptions exhausting the SDK's default five transaction attempts. The SDK then raises ValueError chained from the final Aborted. An initial read-phase hypothesis was not corroborated by the observed failure. The [SDK transaction reference](https://docs.cloud.google.com/python/docs/reference/firestore/latest/google.cloud.firestore_v1.async_transaction.AsyncTransaction) and [transaction guidance](https://docs.cloud.google.com/firestore/native/docs/manage-data/transactions) describe retry behavior; the exact wrapper behavior was verified against the installed SDK source.

## Bounded repair

[UsersRepository.get_or_create](../../backend/app/repositories/users.py) retries one additional SDK transaction round only when ValueError has an Aborted cause. It waits a random 50–250 ms and uses a fresh transaction. Other errors propagate unchanged; ownership and atomic creation remain enforced by the original transaction. No process-local lock registry, dependency, API field or protected specification changed.

This allows at most ten SDK commit attempts with the observed default configuration. It does not promise a fixed total HTTP deadline: SDK RPC deadlines still apply. Sustained contention may still exhaust the bounded retry and surface through existing error handling.

## Actual verification

[Profile tests](../../backend/tests/test_me.py) include deterministic exhausted-contention recovery and unrelated-ValueError propagation. The recovery regression fails against the original method (500 instead of 200) and passes the repair. Injecting pre-RPC commit errors was discarded because it kept emulator locks alive; the final simulation injects the SDK exhaustion wrapper before opening a transaction, then delegates the retry to the actual SDK.

With synthetic demo-baidget users and local Auth/Firestore emulators, the full suite passed 14 tests in 12.42 seconds; a separate real five-way concurrency check passed in 2.50 seconds. Root independently reran the complete suite: 14 passed in 5.77 seconds. Backend Ruff check and format check passed. This validates the implemented health/auth/profile slice locally, not future categories/OCR, production latency or deployment. See [integration review](../development/integration-review.md) for versions, commands and remaining limits.
