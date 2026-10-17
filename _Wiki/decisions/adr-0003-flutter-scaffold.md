---
title: ADR-0003 Flutter client scaffold
status: active
updated: 2026-10-17
---

# ADR-0003: Flutter client scaffold at the repository root

- Decision status: **accepted as an implementation choice in the committed scaffold**; separate team approval of the complete stack is not evidenced.
- Date: 2026-10-17.
- Authority/evidence: Francesca De Luca authored and committed `055275e513a6690489d8712e20011913f42ec555` (`Initialize Flutter project`) on `origin/main`. The project initiator authorized downloading and integrating it with the local wiki. This does not establish acceptance of every generated default.

## Choice and scope

Use the repository root as a Flutter application package, `baidget`, version `1.0.0+1`, with Dart constraint `^3.13.4`. Evidence: [pubspec.yaml](../../pubspec.yaml), [lockfile](../../pubspec.lock), and [main.dart](../../lib/main.dart). Android, iOS, web, Linux, macOS, and Windows runners are present. Android remains the product target from the brief.

The existing package uses Flutter's built-in state/widgets, the Cupertino icon package (constraint `^1.0.8`, locked `1.0.9`), SDK widget testing, and Flutter lints (constraint `^6.0.0`, locked `6.0.0`). These are scaffold defaults for icons/testing/analysis. No framework or dependency alternatives evaluation is recorded; do not invent one. No dependencies were added or upgraded during wiki integration.

## Consequences and limits

The current app is the generated counter demo. The widget test checks a single increment; no test/build execution was possible in the integration session because Flutter/Dart were not found in PATH. [Metadata](../../.metadata) records the stable channel and revision `6a19cca56475dbfba1478ee68d7bd0c2ef891da1`; it does not pin or verify an installed Flutter release.

The original integration left product/backend/service details open under ADR-0002, followed by ADR-0004. The latest [ADR-0005](adr-0005-api-handoff-baseline.md) records the supplied API handoff; unresolved inputs remain in [questions](../open-questions.md). This scaffold decision remains valid and establishes none of those features as implemented. Generated example IDs/debug release signing need review before provider integration/distribution. Record actual checks in [development setup](../development/contributing.md).
