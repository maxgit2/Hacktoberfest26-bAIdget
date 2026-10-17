# bAIdget

bAIdget is an Android-focused personal expense tracker being developed during a one-day hackathon. The latest API handoff specifies Google sign-in via Firebase Auth, category onboarding, manual/scan expenses, recurring rules, and server monthly/yearly/category summaries. The current scope is online-only and EUR-only; email, budgets and other extensions are deferred. See [scope and milestones](_Wiki/product/scope.md).

The repository contains a partial Flutter client (auth/onboarding/gallery upload/read-only detail/settings) and a FastAPI backend with health/auth/profile slices. The default app uses fake auth and an in-memory mock; backend categories, expenses, OCR, summaries and recurrence remain planned. Real Firebase configuration, complete committed OpenAPI and deployment are not available. See [current state](_Wiki/current-state.md) and [integration review](_Wiki/development/integration-review.md) for actual evidence and checks.

## Start here

- [Project wiki](_Wiki/index.md): shared product and engineering knowledge.
- [Product scope](_Wiki/product/scope.md) and [open questions](_Wiki/open-questions.md): requirements and unresolved choices.
- [Contributing and setup](_Wiki/development/contributing.md): structure, SDK constraints, commands, and observed check results.
- Work registers: [frontend](_Wiki/development/frontend-tracker.md), [backend](_Wiki/development/backend-tracker.md), [infrastructure](_Wiki/development/infrastructure-tracker.md), with owners, status, dependencies and completion evidence.
- [Agent instructions](AGENTS.md) and [Claude entry point](CLAUDE.md): shared contribution policy.

All project documentation and code comments must be written in English. Product localization is a separate decision.

## Running the scaffold

The Flutter package is at the repository root. Use a Flutter SDK compatible with the Dart constraint `^3.13.4` in [pubspec.yaml](pubspec.yaml); an exact Flutter release is not pinned. With Flutter and the target platform tools available, run from this directory:

```sh
flutter pub get
flutter analyze
flutter test
flutter run
```

Flutter commands have not been executed in this session because Flutter/Dart are unavailable. Current [API/model tests](test/api_test.dart) and [widget flows](test/app_flow_test.dart) use mocks; they do not establish real backend integration. Android is the target; other generated runners do not establish product support. See [backend setup](backend/README.md) for emulator-only Python checks and [contributing](_Wiki/development/contributing.md) for the synthetic demo and toolchain limits.

## Flutter resources

- [Learn Flutter](https://docs.flutter.dev/get-started/learn-flutter)
- [Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Flutter learning resources](https://docs.flutter.dev/reference/learning-resources)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.

## License

See [LICENSE](LICENSE) for the Apache License 2.0.
