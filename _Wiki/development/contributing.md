---
title: Contributing and development setup
status: active
updated: 2026-10-17
---

# Contributing and development setup

Read [current state](../current-state.md), [scope](../product/scope.md), and [open questions](../open-questions.md). AI contributors also follow [AGENTS.md](../../AGENTS.md) and the shared [maintenance workflow](../maintenance.md).

## Repository structure after Flutter initialization

```text
/
  README.md                 Project entry point
  LICENSE                   Existing Apache License 2.0
  AGENTS.md                 Shared agent instructions
  CLAUDE.md                 Claude entry point to shared instructions
  pubspec.yaml              Flutter package and dependency constraints
  pubspec.lock              Committed dependency resolutions
  .metadata                 Flutter scaffold revision/channel metadata
  analysis_options.yaml     Flutter analyzer/lint configuration
  lib/main.dart             Generated counter demo
  test/widget_test.dart     Counter increment smoke test
  android/                  Gradle Kotlin DSL Android runner
  ios/                      Xcode iOS runner and placeholder native test
  web/                      Web shell, manifest, icons
  linux/                    Linux CMake runner
  macos/                    macOS Xcode runner and placeholder native test
  windows/                  Windows CMake runner
  _Wiki/
    index.md                Navigation
    current-state.md        Short current implementation/handoff snapshot
    maintenance.md          Wiki schema and contributor workflow
    log.md                  Append-only activity record
    open-questions.md       Unresolved coordination decisions
    product/                Scope and user flows
    engineering/            Architecture, domain, contracts, AI/data
    development/            Actual setup and collaboration guidance
    decisions/              Decision register and ADRs
    lessons/                Reproducible failures and verified solutions
    sources/                Source register and reference interpretation
    raw/                    Dated immutable English source records
    templates/              Small reusable document forms
    tools/                  Optional dependency-free wiki check
```

Evidence: commit `055275e513a6690489d8712e20011913f42ec555` (`Initialize Flutter project`, Francesca De Luca, 2026-10-17), [ADR-0003](../decisions/adr-0003-flutter-scaffold.md). The root is the client package; there is no backend directory/manifest or CI workflow. Generated runners do not change the Android-focused product scope.

## SDK and platform prerequisites

- [pubspec.yaml](../../pubspec.yaml) declares package `baidget`, app version `1.0.0+1`, Dart `^3.13.4`, and `publish_to: none`. Use a Flutter SDK that satisfies that Dart constraint; no exact Flutter release is pinned. The lockfile's Flutter lower bound is not an SDK pin. See the [technology registry](../engineering/architecture.md) for constraints, resolved dependencies, and the recorded scaffold revision.
- Android builds read `flutter.sdk` from ignored `android/local.properties` in [settings.gradle.kts](../../android/settings.gradle.kts). SDK paths and generated artifacts stay local; [Android ignore rules](../../android/.gitignore) also exclude Gradle wrapper launchers/JAR and local properties. A clean clone needs Flutter tooling to prepare local build files; that preparation has not been verified here.
- [Android app configuration](../../android/app/build.gradle.kts) targets Java/Kotlin 17, delegates Android SDK/NDK levels to Flutter, uses `com.example.baidget`, and signs release with the debug key. AGP `9.1.0`, Kotlin plugin `2.4.0`, and Gradle `9.3.1` are declared, not a proven compatible local toolchain. Provision the appropriate JDK/Android SDK and demo device before building; choose final IDs/signing before provider registration or distribution.
- The other platform runners require their platform toolchains. No additional platform build or support commitment has been verified.

## Setup and command registry

| Area | Current command status | Next contributor action |
| --- | --- | --- |
| Frontend SDK/environment | From root: `flutter --version`, `flutter doctor -v`, `flutter devices` | Not run: Flutter/Dart/Java not found by `Get-Command flutter,dart,java -ErrorAction SilentlyContinue` in this session; verify a compatible SDK and target toolchain |
| Frontend dependencies/run/build | From root: `flutter pub get`, `flutter run`, `flutter build apk --debug` | Commands documented for the existing package; not executed here; retain the lockfile unless intentionally changing dependencies |
| Backend setup/run | Unavailable: no FastAPI scaffold or manifest | Record actual path, Python version, environment/dependency commands, local start command |
| Auth/Firebase | No configuration or selected services | Record chosen services, safe setup steps and required environment variable names |
| AI/email services | No provider or credentials configured | Record provider setup, safe configuration names, mock mode, limits and failure behavior |
| Application tests/lint | From root: `flutter analyze`, `flutter test`; optionally `dart format --output=none --set-exit-if-changed lib test` | Not executed: tools unavailable in PATH; existing test covers only the counter, not expense features or platform integration |
| Deployment/CI | No target or workflow selected | Record build/run environment and observed deployment/CI evidence |
| Wiki structure | `python _Wiki/tools/check_wiki.py` with a working Python 3.9+ interpreter | Check local links, index coverage and metadata; review factual consistency separately |

No secret values belong in setup instructions. Once configuration is added, provide a sanitized environment example and identify required variables without exposing actual tokens or account data. A working interpreter used for wiki checks is not the chosen backend runtime.

On this Windows session, `C:/Users/Max/AppData/Local/Python/bin/python.exe --version` returned `Python 3.14.7`. The wiki command used this interpreter explicitly:

```powershell
& C:/Users/Max/AppData/Local/Python/bin/python.exe _Wiki/tools/check_wiki.py
```

This is an observed machine-specific path, not a portable installation requirement. Results are recorded in the [log](../log.md). Missing PATH entries do not prove the SDKs are absent from the whole machine; no SDK installation or dependency upgrade was performed.

## Integrating the uncommitted wiki with the remote scaffold

The integration on 2026-10-17 fetched `origin` and fast-forwarded `main` from `ec8a3b5` to `055275e`. The local files were untracked, so an ordinary pull would collide with the remote `README.md`; there was no divergent local commit requiring a merge commit. A safety stash saved all local files first. Agent entry points and `_Wiki` were restored from its untracked-files parent, and the README was combined manually, preserving project/wiki navigation and remote Flutter resource links.

Local recovery reference: stash commit `7ee1ae3c86968ed83948a515cef9af506c527df7`, message `Safety backup of local wiki before Flutter scaffold integration 2026-10-17`; the pre-integration files are under its `^3` tree. This is a **local** backup, not an object promised to exist on GitHub. Do not blindly apply it over the merged README. At the initial integration handoff, documentation was uncommitted and no push had been performed. The initiator subsequently requested committing and publishing all documentation to `origin/main`; that task is recorded in the [activity log](../log.md). The safety stash is retained.

## Working together during the hackathon

Current specification: [SRC-003](../raw/2026-10-17-updated-specification.md), [ADR-0004](../decisions/adr-0004-updated-product-baseline.md), and [scope/milestones](../product/scope.md). Device identity replaces Google sign-in; gallery OCR and manual input share a form; the supplied expense fields are documented but not implemented. Do not infer Firebase services, worker libraries, DeepSeek-OCR hosting, or AgentMail adoption from the named direction. Resolve the relevant [questions](../open-questions.md) before choosing shared identity/data/API contracts.

1. Agree on the outcome and relevant contracts for a bounded change; link a task/issue if one exists.
2. Check the current working tree and nearby changes. Coordinate overlapping files and shared integration contracts before incompatible implementations diverge.
3. Record consequential choices with a short [decision](../decisions/index.md). Use proposed status while an agreement is unresolved. Do not block routine reversible work on formal sign-off.
4. Implement and run checks appropriate to the change. State whether external providers, storage, identity, or the UI are mocked.
5. Update the affected wiki pages, current state/questions if needed, and append a [log](../log.md) entry. Include documentation with the same change/PR when possible.
6. At integration, verify the agreed flow across the actual client/backend boundary and record remaining gaps. Branch naming and PR policy remain team choices; no CI enforcement is claimed.

Human contributors may edit the wiki directly. Agents maintain the same files; there is no separate authoritative memory for each tool.

## Verification discipline

Git publication also requires an author name/email, independently of remote authentication. The first documentation commit attempt encountered missing identity; see the verified [Git author identity lesson](../lessons/git-author-identity.md). Use an identity verified for the acting user and deliberate configuration scope; do not infer it from an unrelated teammate's commit.

Use the candidate scenarios in [scope](../product/scope.md) and [AI/data](../engineering/ai-and-data.md) to choose meaningful checks. Once implemented, cover category ownership, money/date semantics, user-corrected drafts, duplicates, provider failures, and summary consistency.

Record exact commands, observed results, test fixture type, and any checks not run. A Markdown structural check does not verify API behavior, Firebase rules, AI accuracy, or a mobile build. Preserve useful error signatures and fixes as [lessons](../lessons/index.md), using redacted or synthetic evidence.
