---
title: Current state
status: active
updated: 2026-10-17
---

# Current state

## Verified repository state

On 2026-10-17, fetched `origin` and fast-forwarded local `main` from `ec8a3b5` to `055275e513a6690489d8712e20011913f42ec555` (`Initialize Flutter project`, Francesca De Luca). Restored the uncommitted local wiki and agent entry points, and combined the local project/wiki README with the remote Flutter resources. See the [activity log](log.md) for integration and verification evidence.

The repository root is now the Flutter package: [manifest](../pubspec.yaml), [lockfile](../pubspec.lock), [application](../lib/main.dart), [widget test](../test/widget_test.dart), and [analyzer configuration](../analysis_options.yaml). Generated runners exist for Android, iOS, web, Linux, macOS, and Windows. Android remains the requested product platform; runner presence is not a scope expansion.

Source inspection shows only the generated counter demo: `MyApp` opens `MyHomePage`; tapping `+` increments in-memory state with `setState`. The existing test asserts `0` becomes `1`. No expense features, backend, auth/Firebase integration, persistence, camera/AI/email integration, deployment, or CI workflow are present. App tests/builds have not run in this session: Flutter, Dart, and Java were not found in PATH. See [setup and checks](development/contributing.md).

The wiki structural check passed after integration; exact results are in the log. The earlier exhaustive reference-comment review remains incomplete; coverage and follow-up remain in the [source register](sources/index.md).

## Product direction

bAIdget's [updated specification](raw/2026-10-17-updated-specification.md) replaces Google sign-in with automatic smartphone ID/fingerprint identity. Receipt extraction starts from gallery selection; manual entry shares the review form. Summaries include weekly/monthly/yearly/category views and previous-period comparison. The supplied model includes optional float amount, default euro, timestamps, and `concurrent {info}`; wire/validation/accounting details remain open. Personal use is the working scope, explicitly questioned in the source. See [scope/milestones](product/scope.md), [flows](product/user-flows.md), and [model](engineering/domain-model.md).

The [updated baseline ADR-0004](decisions/adr-0004-updated-product-baseline.md) records Android/Flutter/FastAPI/Firebase as the human-supplied direction, DeepSeek-OCR as the named OCR direction, AgentMail as a candidate, and workers as tentative. Only Flutter is present in code. Milestones are 0.1 backend infrastructure; 1.0 auth/templates/input; 2.0 deployment/categories/summaries; 3.0 email; 4.0 budgets/alerts; 5.0 chart variants. None is claimed complete. SDK/dependency evidence remains in [architecture](engineering/architecture.md); Firebase services, OCR variant/host, backend credentials, and deployment target are undefined.

## Suggested next coordination steps

These are coordination recommendations, not assigned tasks or delivery commitments.

1. Select which source milestones fit the demo and clarify camera/gallery, category-edit timing, and chart scope tensions.
2. Resolve the [blocking questions](open-questions.md): device auth/proof/recovery, optional float precision/null handling, timestamp boundaries, category references, `concurrent` info, record IDs/deletion, and extraction contract.
3. Agree on the [contract checklist](engineering/contracts.md) before parallel client/backend work; document mocks explicitly.
4. Verify the existing Flutter scaffold with a compatible SDK and agree the backend location/runtime; see the [development guide](development/contributing.md).
5. Implement and verify an agreed vertical slice; resolve application IDs, Android demo target, and external-service setup before claiming integration.

## Handoff convention

At the end of a task, briefly record delivered behavior, changed contracts, verification, blockers, and the next useful action. Named task owners and GitHub issue/PR links are currently unassigned. Keep detailed history in [log.md](log.md); keep this page short and current.
