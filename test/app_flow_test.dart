import 'dart:convert';
import 'dart:typed_data';

import 'package:baidget/app.dart';
import 'package:baidget/core/auth/auth_providers.dart';
import 'package:baidget/core/auth/auth_service.dart';
import 'package:baidget/core/network/api_client.dart';
import 'package:baidget/core/network/mock_backend.dart';
import 'package:baidget/core/settings/api_base_url.dart';
import 'package:baidget/features/auth/presentation/sign_in_screen.dart';
import 'package:baidget/features/expenses/presentation/expense_detail_screen.dart';
import 'package:baidget/features/onboarding/presentation/onboarding_screen.dart';
import 'package:baidget/features/upload/data/receipt_image_picker.dart';
import 'package:baidget/features/upload/presentation/upload_screen.dart';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

class _FakePicker extends ReceiptImagePicker {
  @override
  Future<Uint8List?> pick() async => Uint8List.fromList([0xFF, 0xD8]);
}

/// Always fails the scan with the given error code.
class _FailingScanAdapter implements HttpClientAdapter {
  _FailingScanAdapter(this.inner, this.status, this.code);

  final HttpClientAdapter inner;
  final int status;
  final String code;
  int scanCalls = 0;
  final scanIds = <String>[];

  @override
  Future<ResponseBody> fetch(
    RequestOptions options,
    Stream<Uint8List>? requestStream,
    Future<void>? cancelFuture,
  ) {
    if (options.path != '/expenses/scan') {
      return inner.fetch(options, requestStream, cancelFuture);
    }
    scanCalls++;
    scanIds.add(
      (options.data as FormData).fields.firstWhere((f) => f.key == 'id').value,
    );
    return Future.value(
      ResponseBody.fromString(
        jsonEncode({
          'error': {'code': code, 'message': 'x', 'details': {}},
        }),
        status,
        headers: {
          Headers.contentTypeHeader: [Headers.jsonContentType],
        },
      ),
    );
  }

  @override
  void close({bool force = false}) {}
}

void main() {
  Future<MockBackend> pumpApp(
    WidgetTester tester, {
    bool signedIn = true,
    bool onboarded = true,
    HttpClientAdapter Function(HttpClientAdapter mock)? adapter,
  }) async {
    SharedPreferences.setMockInitialValues({});
    final prefs = await SharedPreferences.getInstance();
    final backend = MockBackend();
    if (onboarded) {
      backend
        ..onboardingCompleted = true
        ..categories.add({
          'id': 'cat_1',
          'name': 'Groceries',
          'icon': 'shopping_cart',
          'color': null,
          'catalog_id': 'groceries',
          'is_other': false,
        });
    }
    final mockAdapter = MockBackendAdapter(
      backend,
      latency: Duration.zero,
      scanLatency: Duration.zero,
    );

    await tester.pumpWidget(
      ProviderScope(
        retry: (_, _) => null,
        overrides: [
          sharedPreferencesProvider.overrideWithValue(prefs),
          authServiceProvider.overrideWithValue(
            FakeAuthService(
              initialUser: signedIn ? FakeAuthService.user : null,
            ),
          ),
          mockBackendProvider.overrideWithValue(backend),
          mockBackendAdapterProvider.overrideWithValue(
            adapter?.call(mockAdapter) ?? mockAdapter,
          ),
          receiptImagePickerProvider.overrideWithValue(_FakePicker()),
        ],
        child: const BaidgetApp(),
      ),
    );
    await tester.pumpAndSettle();
    return backend;
  }

  Future<void> upload(WidgetTester tester) async {
    await tester.tap(find.text('Choose from gallery'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Upload'));
    await tester.pumpAndSettle();
  }

  testWidgets('sign-in → onboarding → home', (tester) async {
    final backend = await pumpApp(tester, signedIn: false, onboarded: false);
    expect(find.byType(SignInScreen), findsOneWidget);

    await tester.tap(find.text('Continue with Google'));
    await tester.pumpAndSettle();
    expect(find.byType(OnboardingScreen), findsOneWidget);
    expect(find.text('Pick at least 2'), findsOneWidget);

    await tester.tap(find.text('Essential'));
    await tester.pump();
    await tester.tap(find.text('Continue with 4 categories'));
    await tester.pumpAndSettle();

    expect(find.byType(UploadScreen), findsOneWidget);
    expect(backend.categories.map((c) => c['name']), [
      'Groceries',
      'Transport',
      'Housing',
      'Entertainment',
      'Other',
    ]);
  });

  testWidgets('onboarding with a custom category', (tester) async {
    final backend = await pumpApp(tester, onboarded: false);

    await tester.tap(find.text('Groceries'));
    await tester.scrollUntilVisible(find.text('Add a custom category'), 200);
    await tester.tap(find.text('Add a custom category'));
    await tester.pumpAndSettle();
    await tester.enterText(find.byType(TextFormField), 'groceries');
    await tester.tap(find.text('Add'));
    await tester.pump();
    expect(find.text('This category already exists'), findsOneWidget);

    await tester.enterText(find.byType(TextFormField), 'Pets');
    await tester.tap(find.text('Add'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Continue with 2 categories'));
    await tester.pumpAndSettle();

    expect(find.byType(UploadScreen), findsOneWidget);
    expect(backend.categories.map((c) => c['name']), [
      'Groceries',
      'Pets',
      'Other',
    ]);
  });

  testWidgets('upload shows the saved expense', (tester) async {
    final backend = await pumpApp(tester);

    await upload(tester);

    expect(find.byType(ExpenseDetailScreen), findsOneWidget);
    expect(find.text('Saved to your expenses'), findsOneWidget);
    expect(find.text('€23.40'), findsOneWidget);
    expect(find.text('Groceries'), findsOneWidget);
    expect(find.text('Please review this expense'), findsNothing);
    expect(backend.expenses, hasLength(1));

    // The mock flags every second scan for review.
    await tester.pageBack();
    await tester.pumpAndSettle();
    expect(find.text('Choose from gallery'), findsOneWidget);
    await upload(tester);

    expect(find.text('Please review this expense'), findsOneWidget);
    expect(find.text('Amount not detected'), findsOneWidget);
    expect(backend.expenses, hasLength(2));
  });

  testWidgets('a transient error offers a retry with the same id', (
    tester,
  ) async {
    late _FailingScanAdapter failing;
    await pumpApp(
      tester,
      adapter: (mock) =>
          failing = _FailingScanAdapter(mock, 503, 'extraction_unavailable'),
    );

    await upload(tester);
    expect(find.textContaining('temporarily unavailable'), findsOneWidget);
    expect(find.byType(ExpenseDetailScreen), findsNothing);

    await tester.tap(find.text('Retry'));
    await tester.pumpAndSettle();

    expect(failing.scanCalls, 2);
    expect(failing.scanIds[0], failing.scanIds[1]);
  });

  testWidgets('extraction_failed explains it and offers no retry', (
    tester,
  ) async {
    await pumpApp(
      tester,
      adapter: (mock) => _FailingScanAdapter(mock, 422, 'extraction_failed'),
    );

    await upload(tester);

    expect(find.textContaining("couldn't read this image"), findsOneWidget);
    expect(find.text('Retry'), findsNothing);
    expect(find.text('Choose another image'), findsOneWidget);
  });

  testWidgets('sign out from settings goes back to sign-in', (tester) async {
    await pumpApp(tester);

    await tester.tap(find.byTooltip('Settings'));
    await tester.pumpAndSettle();
    expect(find.text('Mock backend active'), findsOneWidget);

    await tester.tap(find.text('Sign out'));
    await tester.pumpAndSettle();

    expect(find.byType(SignInScreen), findsOneWidget);
  });

  testWidgets('settings saves a valid backend URL', (tester) async {
    await pumpApp(tester);
    await tester.tap(find.byTooltip('Settings'));
    await tester.pumpAndSettle();

    await tester.enterText(find.byType(TextFormField), 'not a url');
    await tester.tap(find.text('Save'));
    await tester.pumpAndSettle();
    expect(find.textContaining('Enter a full URL'), findsOneWidget);

    await tester.enterText(find.byType(TextFormField), 'https://api.test/v1/');
    await tester.tap(find.text('Save'));
    await tester.pumpAndSettle();

    expect(find.text('Settings saved'), findsOneWidget);
    expect(find.text('Backend in use'), findsOneWidget);
    // Shown both in the field and in the status tile.
    expect(find.text('https://api.test/v1'), findsNWidgets(2));
  });
}
