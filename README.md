# bAIdget

bAIdget is an Android-focused expense tracker being developed during a one-day hackathon. The updated direction uses automatic smartphone ID/fingerprint identity, category templates, gallery receipt import with OCR review, a shared manual-entry form, and weekly/monthly/yearly/category summaries with period comparisons. Later milestones add email import, budgets/threshold alerts, and chart variants; see [scope and milestones](_Wiki/product/scope.md).

The repository contains a Flutter scaffold whose UI is the generated counter demo. Expense features and the specified FastAPI/Firebase backend are not implemented. Identity mechanics, data/API details, Firebase services, and hosting remain open. See [current state](_Wiki/current-state.md) for evidence and verification limits.

## Start here

- [Project wiki](_Wiki/index.md): shared product and engineering knowledge.
- [Product scope](_Wiki/product/scope.md) and [open questions](_Wiki/open-questions.md): requirements and unresolved choices.
- [Contributing and setup](_Wiki/development/contributing.md): structure, SDK constraints, commands, and observed check results.
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

These commands have not been verified in the integration session because Flutter/Dart were not found in its PATH. The existing [widget test](test/widget_test.dart) checks only the demo counter. Android is the product target; the generated iOS, web, Linux, macOS, and Windows runners do not establish additional product commitments.

## Flutter resources

- [Learn Flutter](https://docs.flutter.dev/get-started/learn-flutter)
- [Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Flutter learning resources](https://docs.flutter.dev/reference/learning-resources)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.

## License

See [LICENSE](LICENSE) for the Apache License 2.0.
