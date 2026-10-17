import 'dart:convert';
import 'dart:typed_data';

import 'package:baidget/core/auth/auth_service.dart';
import 'package:baidget/core/format/formatters.dart';
import 'package:baidget/core/network/api_client.dart';
import 'package:baidget/core/network/api_exception.dart';
import 'package:baidget/core/network/mock_backend.dart';
import 'package:baidget/core/settings/api_base_url.dart';
import 'package:baidget/features/categories/data/categories_repository.dart';
import 'package:baidget/features/categories/domain/category.dart';
import 'package:baidget/features/expenses/data/expenses_repository.dart';
import 'package:baidget/features/expenses/domain/expense.dart';
import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';

/// Answers with a scripted list of responses and records the requests.
class _ScriptedAdapter implements HttpClientAdapter {
  _ScriptedAdapter(this.responses);

  final List<(int, Object, Map<String, List<String>>)> responses;
  final requests = <RequestOptions>[];

  @override
  Future<ResponseBody> fetch(
    RequestOptions options,
    Stream<Uint8List>? requestStream,
    Future<void>? cancelFuture,
  ) async {
    requests.add(options);
    final (status, body, headers) = responses[requests.length - 1];
    return ResponseBody.fromString(
      jsonEncode(body),
      status,
      headers: {
        Headers.contentTypeHeader: [Headers.jsonContentType],
        ...headers,
      },
    );
  }

  @override
  void close({bool force = false}) {}
}

class _CountingAuth extends FakeAuthService {
  _CountingAuth() : super(initialUser: FakeAuthService.user);

  int refreshes = 0;
  int signOuts = 0;

  @override
  Future<String?> getIdToken({bool forceRefresh = false}) async {
    if (forceRefresh) refreshes++;
    return forceRefresh ? 'fresh-token' : 'old-token';
  }

  @override
  Future<void> signOut() async {
    signOuts++;
    await super.signOut();
  }
}

Map<String, Object> _err(String code) => {
  'error': {'code': code, 'message': 'msg', 'details': <String, Object>{}},
};

const _me = {
  'uid': 'u',
  'email': null,
  'display_name': null,
  'onboarding_completed': true,
};

void main() {
  final image = Uint8List.fromList([0xFF, 0xD8]);

  group('ApiException', () {
    test('parses the error envelope and Retry-After', () async {
      final dio = Dio(BaseOptions(baseUrl: 'https://api.test'))
        ..httpClientAdapter = _ScriptedAdapter([
          (
            429,
            _err('rate_limited'),
            {
              'retry-after': ['120'],
            },
          ),
        ]);

      final e = await apiCall(() => dio.get<dynamic>('/x')).then<ApiException>(
        (_) => fail('no error'),
        onError: (Object e) => e as ApiException,
      );

      expect(e.code, ApiErrorCode.rateLimited);
      expect(e.statusCode, 429);
      expect(e.retryAfter, const Duration(minutes: 2));
      expect(e.isTransient, isTrue);
    });

    test('unexpected JSON becomes invalid_response', () async {
      final dio = Dio(BaseOptions(baseUrl: 'https://api.test'))
        ..httpClientAdapter = _ScriptedAdapter([
          (200, {'foo': 1}, {}),
        ]);
      final repo = CategoriesRepository(dio);

      expect(
        repo.getCategories(),
        throwsA(
          isA<ApiException>().having(
            (e) => e.code,
            'code',
            ApiErrorCode.invalidResponse,
          ),
        ),
      );
    });
  });

  group('AuthInterceptor', () {
    test('sends the Bearer token', () async {
      final adapter = _ScriptedAdapter([(200, _me, {})]);
      final dio = createDio(baseUrl: 'https://api.test', auth: _CountingAuth())
        ..httpClientAdapter = adapter;

      await dio.get<dynamic>('/me');

      expect(
        adapter.requests.single.headers['Authorization'],
        'Bearer old-token',
      );
    });

    test('on 401 refreshes the token and retries once', () async {
      final auth = _CountingAuth();
      final adapter = _ScriptedAdapter([
        (401, _err('unauthenticated'), {}),
        (200, _me, {}),
      ]);
      final dio = createDio(baseUrl: 'https://api.test', auth: auth)
        ..httpClientAdapter = adapter;

      final res = await dio.get<dynamic>('/me');

      expect(res.statusCode, 200);
      expect(auth.refreshes, 1);
      expect(auth.signOuts, 0);
      expect(
        adapter.requests[1].headers['Authorization'],
        'Bearer fresh-token',
      );
    });

    test('a second 401 signs the user out', () async {
      final auth = _CountingAuth();
      final dio = createDio(baseUrl: 'https://api.test', auth: auth)
        ..httpClientAdapter = _ScriptedAdapter([
          (401, _err('unauthenticated'), {}),
          (401, _err('unauthenticated'), {}),
        ]);

      await expectLater(
        apiCall(() => dio.get<dynamic>('/me')),
        throwsA(isA<ApiException>()),
      );
      expect(auth.refreshes, 1);
      expect(auth.signOuts, 1);
    });

    test('retries a multipart upload after 401', () async {
      final adapter = _ScriptedAdapter([
        (401, _err('unauthenticated'), {}),
        (201, _scanJson, {}),
      ]);
      final dio = createDio(baseUrl: 'https://api.test', auth: _CountingAuth())
        ..httpClientAdapter = adapter;

      final expense = await ExpensesRepository(dio).scan(image, id: 'abc');

      expect(expense.id, 'abc');
      expect(adapter.requests, hasLength(2));
    });
  });

  test('scan sends image + id as multipart with a 45 s timeout', () async {
    final adapter = _ScriptedAdapter([(201, _scanJson, {})]);
    final dio = createDio(baseUrl: 'https://api.test/v1', auth: _CountingAuth())
      ..httpClientAdapter = adapter;

    await ExpensesRepository(dio).scan(image, id: 'abc');

    final req = adapter.requests.single;
    expect(req.method, 'POST');
    expect(req.uri.toString(), 'https://api.test/v1/expenses/scan');
    expect(req.receiveTimeout, const Duration(seconds: 45));
    final form = req.data as FormData;
    expect(form.fields.single.key, 'id');
    expect(form.fields.single.value, 'abc');
    expect(form.files.single.key, 'image');
    expect(form.files.single.value.contentType.toString(), 'image/jpeg');
  });

  group('Expense.fromJson', () {
    test('reads the contract example', () {
      final e = Expense.fromJson(_scanJson);

      expect(e.amountCents, 2340);
      expect(e.date, DateTime.utc(2026, 10, 16, 10, 30));
      expect(e.source, ExpenseSource.scan);
      expect(e.type, ExpenseType.single);
      expect(e.scanDetails!.documentType, DocumentType.receipt);
      expect(e.scanDetails!.items.single.totalCents, 240);
      expect(e.scanDetails!.vatTotalCents, 210);
    });

    test('handles a missing amount and a recurring expense', () {
      final e = Expense.fromJson({
        ..._scanJson,
        'amount': null,
        'type': 'recurring',
        'recurrence': {'rule_id': 'rule_x1'},
        'scan_details': null,
      });

      expect(e.amountCents, isNull);
      expect(e.type, ExpenseType.recurring);
      expect(e.recurrenceRuleId, 'rule_x1');
      expect(e.scanDetails, isNull);
    });

    test('avoids floating point drift', () {
      expect(Expense.fromJson({..._scanJson, 'amount': 0.29}).amountCents, 29);
      expect(
        Expense.fromJson({..._scanJson, 'amount': 19.99}).amountCents,
        1999,
      );
    });
  });

  group('MockBackend', () {
    late MockBackend backend;
    late Dio dio;

    setUp(() {
      backend = MockBackend();
      dio = createDio(baseUrl: 'https://mock/v1', auth: _CountingAuth())
        ..httpClientAdapter = MockBackendAdapter(
          backend,
          latency: Duration.zero,
          scanLatency: Duration.zero,
        );
    });

    test('onboarding needs 2 categories and adds Other', () async {
      final repo = CategoriesRepository(dio);

      await expectLater(
        repo.completeOnboarding(catalogIds: ['groceries'], custom: []),
        throwsA(
          isA<ApiException>().having((e) => e.code, 'code', 'min_categories'),
        ),
      );

      final created = await repo.completeOnboarding(
        catalogIds: ['groceries'],
        custom: [const NewCategory(name: 'Pets')],
      );
      expect(created.map((c) => c.name), ['Groceries', 'Pets', 'Other']);
      expect(created.last.isOther, isTrue);

      await expectLater(
        repo.completeOnboarding(
          catalogIds: ['groceries', 'travel'],
          custom: [],
        ),
        throwsA(
          isA<ApiException>().having(
            (e) => e.code,
            'code',
            'already_onboarded',
          ),
        ),
      );
    });

    test('scan is idempotent on the client id', () async {
      final repo = ExpensesRepository(dio);

      final first = await repo.scan(image, id: 'same-id');
      final again = await repo.scan(image, id: 'same-id');

      expect(again.id, first.id);
      expect(backend.expenses, hasLength(1));
    });
  });

  test('formatMoney', () {
    expect(formatMoney(2340), '€23.40');
    expect(formatMoney(123456789), '€1,234,567.89');
  });

  test('backend URL validation', () {
    expect(CustomApiBaseUrlNotifier.validate(''), isNull);
    expect(CustomApiBaseUrlNotifier.validate('https://api.test/v1'), isNull);
    expect(
      CustomApiBaseUrlNotifier.validate('http://10.0.2.2:8000/v1'),
      isNull,
    );
    expect(CustomApiBaseUrlNotifier.validate('api.test'), isNotNull);
    expect(
      CustomApiBaseUrlNotifier.normalizeUrl(' https://a.b/v1/ '),
      'https://a.b/v1',
    );
  });
}

const _scanJson = <String, Object?>{
  'id': 'abc',
  'owner': 'firebase-uid',
  'date': '2026-10-16T10:30:00Z',
  'seller': 'Esselunga',
  'title': 'Esselunga',
  'description': null,
  'category': 'cat_8f2a',
  'type': 'single',
  'recurrence': null,
  'amount': 23.4,
  'currency': 'EUR',
  'source': 'scan',
  'scan_details': {
    'document_type': 'receipt',
    'items': [
      {'description': 'Latte', 'quantity': 2, 'unit_price': 1.2, 'total': 2.4},
    ],
    'vat_total': 2.1,
    'vat_number': 'IT01234567890',
    'payment_method': 'card',
  },
  'needs_review': false,
  'created_at': '2026-10-16T10:31:02Z',
  'updated_at': '2026-10-16T10:31:02Z',
  'deleted_at': null,
};
