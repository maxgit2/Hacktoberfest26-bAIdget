---
title: ADR-0002 Initial stack direction
status: superseded
updated: 2026-10-17
---

# ADR-0002: Initial application stack direction

- Decision status: **superseded** by [ADR-0004](adr-0004-updated-product-baseline.md) on 2026-10-17. Previously proposed; the historical rationale below is preserved.
- Date: 2026-10-17.
- Evidence: [initial project brief](../raw/2026-10-17-project-brief.md). Flutter now has implementation evidence in [ADR-0003](adr-0003-flutter-scaffold.md); no formal acceptance of the complete stack or FastAPI/Firebase implementation is evidenced.

## Historical proposal

Target Android with a Flutter client and a FastAPI backend, using Firebase for services to be determined. Provide Google sign-in and backend AI-assisted receipt reading/classification as required by the product brief.

## Rationale and alternatives

The stack is supplied by the project initiator as an initial direction; detailed team rationale and alternatives have not been recorded. Do not invent a completed framework evaluation. Reassess only when a concrete project constraint warrants it.

## Unresolved choices and consequences at proposal time

Agree Firebase's role, authentication/token verification, persistence/file storage, backend runtime, deployment, and email/AI providers. The Flutter scaffold uses built-in `setState`, `flutter_test`, and `flutter_lints`; product state management, routing, and networking remain unselected. This proposal does not authorize treating Firestore, Firebase Authentication, or any hosting service as already chosen.

Resolve the remaining parts of [Q-02 and Q-03](../open-questions.md), then record authority and consequences here or in focused decisions. Actual Flutter manifests and source paths are linked from the [architecture registry](../engineering/architecture.md) and [development guide](../development/contributing.md). This broader proposal is retained; ADR-0003 records only the observed client scaffold choice. Acceptance and implementation are separate facts.
