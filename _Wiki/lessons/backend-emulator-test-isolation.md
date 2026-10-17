---
title: Backend tests must fail before cloud initialization without emulators
status: active
updated: 2026-10-17
---

# Backend tests must fail before cloud initialization without emulators

## Observed issue

At dev 18c0d19, the autouse clear_firestore fixture silently continued when FIRESTORE_EMULATOR_HOST was absent. The client fixture then started Firebase/Firestore lifespan. With a configured real project/ADC that could use the non-emulator client path. The original README also started emulators separately before plain pytest, without exporting hosts; Settings does not automatically load .env.

No live cloud access was attempted to demonstrate this risk. Source control flow establishes the missing guard; actual negative validation uses no emulator hosts and stops before client startup.

## Fix and verification

The [fixture](../../backend/tests/conftest.py) now requires both FIRESTORE_EMULATOR_HOST and FIREBASE_AUTH_EMULATOR_HOST, failing clearly when either is missing. [Backend README](../../backend/README.md) runs tests/local API through firebase emulators:exec with demo-baidget, which exports emulator variables to the child.

The command `python -m pytest -q tests/test_health.py` without the two variables produced the expected setup error and exit 1 in 0.12s, before a client starts. This is a passing safety probe, not a passing application test. Full emulator outcomes and the separate profile-contention issue are in [integration review](../development/integration-review.md).

Use synthetic fixtures and local emulator hosts only. Do not “fix” the guard by pointing tests at a real project or by weakening it to make an unconfigured test command pass. Neither .env.example nor a running emulator alone supplies Python process environment variables.
