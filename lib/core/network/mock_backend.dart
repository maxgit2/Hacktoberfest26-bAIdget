import 'dart:convert';
import 'dart:typed_data';

import 'package:dio/dio.dart';

/// In-memory backend that follows `docs/frontend-handoff.md`, used while no
/// backend URL is set. It plugs into Dio as an adapter, so the app runs the
/// exact same repository code it will use against the real API.
///
/// Phase 1 endpoints only; the rest answer `404 not_found`.
class MockBackend {
  bool onboardingCompleted = false;
  final List<Map<String, dynamic>> categories = [];
  final Map<String, Map<String, dynamic>> expenses = {};
  int _scanCount = 0;
  int _categorySeq = 0;

  static const catalogItems = [
    {'id': 'groceries', 'name': 'Groceries', 'icon': 'shopping_cart'},
    {'id': 'dining_out', 'name': 'Dining out', 'icon': 'restaurant'},
    {'id': 'transport', 'name': 'Transport', 'icon': 'directions_car'},
    {'id': 'housing', 'name': 'Housing', 'icon': 'home'},
    {'id': 'bills', 'name': 'Bills', 'icon': 'receipt'},
    {'id': 'health', 'name': 'Health', 'icon': 'local_hospital'},
    {'id': 'entertainment', 'name': 'Entertainment', 'icon': 'movie'},
    {'id': 'shopping', 'name': 'Shopping', 'icon': 'shopping_bag'},
    {'id': 'travel', 'name': 'Travel', 'icon': 'flight'},
    {'id': 'education', 'name': 'Education', 'icon': 'school'},
    {'id': 'subscriptions', 'name': 'Subscriptions', 'icon': 'subscriptions'},
  ];

  static const presets = [
    {
      'id': 'essential_4',
      'name': 'Essential',
      'catalog_ids': ['groceries', 'transport', 'housing', 'entertainment'],
    },
    {
      'id': 'complete_6',
      'name': 'Complete',
      'catalog_ids': [
        'groceries',
        'transport',
        'housing',
        'entertainment',
        'dining_out',
        'health',
      ],
    },
  ];

  MockResponse handle(RequestOptions o) {
    final route = '${o.method} ${o.path}';
    return switch (route) {
      'GET /health' => _ok({'status': 'ok'}),
      'GET /me' => _ok({
        'uid': 'fake-uid',
        'email': 'dev@baidget.test',
        'display_name': 'Dev User',
        'onboarding_completed': onboardingCompleted,
      }),
      'GET /categories/catalog' => _ok({
        'items': catalogItems,
        'presets': presets,
      }),
      'POST /categories/onboarding' => _onboarding(o.data as Map),
      'GET /categories' => _ok({'items': categories}),
      'POST /expenses/scan' => _scan(o.data as FormData),
      'POST /recurring-rules/sync' => _ok({
        'created': 0,
        'rules_processed': 0,
        'has_more': false,
      }),
      _ => _error(404, 'not_found', 'Not implemented in the mock: $route'),
    };
  }

  MockResponse _onboarding(Map body) {
    if (onboardingCompleted) {
      return _error(409, 'already_onboarded', 'Onboarding already completed');
    }
    final ids = (body['catalog_ids'] as List? ?? const []).cast<String>();
    final custom = (body['custom'] as List? ?? const []).cast<Map>();
    final total = ids.length + custom.length;
    if (total < 2) {
      return _error(422, 'min_categories', 'At least 2 categories required');
    }
    if (total > 30) {
      return _error(422, 'max_categories', 'At most 30 categories');
    }

    final created = <Map<String, dynamic>>[];
    for (final id in ids) {
      final item = catalogItems.firstWhere(
        (i) => i['id'] == id,
        orElse: () => const {},
      );
      if (item.isEmpty) {
        return _error(422, 'validation_error', 'Unknown catalog id: $id');
      }
      created.add(_category(item['name']!, icon: item['icon'], catalogId: id));
    }
    for (final c in custom) {
      created.add(
        _category(
          c['name'] as String,
          icon: c['icon'] as String?,
          color: c['color'] as String?,
        ),
      );
    }
    created.add(_category('Other', icon: 'more_horiz', isOther: true));

    final names = created.map((c) => (c['name'] as String).toLowerCase());
    if (names.toSet().length != names.length) {
      return _error(409, 'category_name_taken', 'Duplicate category name');
    }

    categories
      ..clear()
      ..addAll(created);
    onboardingCompleted = true;
    return MockResponse(201, {'categories': created});
  }

  Map<String, dynamic> _category(
    String name, {
    String? icon,
    String? color,
    String? catalogId,
    bool isOther = false,
  }) => {
    'id': 'cat_${++_categorySeq}',
    'name': name,
    'icon': icon,
    'color': color,
    'catalog_id': catalogId,
    'is_other': isOther,
  };

  MockResponse _scan(FormData form) {
    if (form.files.where((f) => f.key == 'image').isEmpty) {
      return _error(422, 'validation_error', 'Missing image');
    }
    final id = form.fields
        .where((f) => f.key == 'id')
        .map((f) => f.value)
        .firstOrNull;
    if (id != null && expenses.containsKey(id)) {
      return _ok(expenses[id]!);
    }

    // Every second scan comes back with needs_review, to exercise the UI.
    final needsReview = _scanCount++ % 2 == 1;
    final category =
        categories.where((c) => c['catalog_id'] == 'groceries').firstOrNull ??
        categories.where((c) => c['is_other'] == true).firstOrNull;
    final now = DateTime.now().toUtc().toIso8601String();
    final expense = <String, dynamic>{
      'id': id ?? 'mock-${DateTime.now().microsecondsSinceEpoch}',
      'owner': 'fake-uid',
      'date': now,
      'seller': 'Esselunga',
      'title': 'Esselunga',
      'description': null,
      'category': category?['id'] ?? 'cat_other',
      'type': 'single',
      'recurrence': null,
      'amount': needsReview ? null : 23.4,
      'currency': 'EUR',
      'source': 'scan',
      'scan_details': {
        'document_type': 'receipt',
        'items': [
          {
            'description': 'Milk',
            'quantity': 2,
            'unit_price': 1.2,
            'total': 2.4,
          },
          {
            'description': 'Bread',
            'quantity': 1,
            'unit_price': 2.5,
            'total': 2.5,
          },
          {
            'description': 'Dish soap',
            'quantity': 1,
            'unit_price': 18.5,
            'total': 18.5,
          },
        ],
        'vat_total': 2.1,
        'vat_number': 'IT01234567890',
        'payment_method': 'card',
      },
      'needs_review': needsReview,
      'created_at': now,
      'updated_at': now,
      'deleted_at': null,
    };
    expenses[expense['id'] as String] = expense;
    return MockResponse(201, expense);
  }

  static MockResponse _ok(Object body) => MockResponse(200, body);

  static MockResponse _error(int status, String code, String message) =>
      MockResponse(status, {
        'error': {'code': code, 'message': message, 'details': {}},
      });
}

class MockResponse {
  const MockResponse(this.status, this.body);

  final int status;
  final Object body;
}

class MockBackendAdapter implements HttpClientAdapter {
  MockBackendAdapter(
    this.backend, {
    this.latency = const Duration(milliseconds: 300),
    this.scanLatency = const Duration(seconds: 3),
  });

  final MockBackend backend;
  final Duration latency;
  final Duration scanLatency;

  @override
  Future<ResponseBody> fetch(
    RequestOptions options,
    Stream<Uint8List>? requestStream,
    Future<void>? cancelFuture,
  ) async {
    await Future<void>.delayed(
      options.path == '/expenses/scan' ? scanLatency : latency,
    );
    final response = backend.handle(options);
    return ResponseBody.fromString(
      jsonEncode(response.body),
      response.status,
      headers: {
        Headers.contentTypeHeader: [Headers.jsonContentType],
      },
    );
  }

  @override
  void close({bool force = false}) {}
}
