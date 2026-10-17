import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../auth/auth_providers.dart';
import '../auth/auth_service.dart';
import '../settings/api_base_url.dart';
import 'auth_interceptor.dart';
import 'mock_backend.dart';

const _mockBaseUrl = 'https://mock.baidget.local/v1';

/// Shared across Dio rebuilds so the mock data survives a URL change.
final mockBackendProvider = Provider<MockBackend>((ref) => MockBackend());

final mockBackendAdapterProvider = Provider<HttpClientAdapter>(
  (ref) => MockBackendAdapter(ref.watch(mockBackendProvider)),
);

/// HTTP client for the backend. Rebuilt when the URL in Settings changes.
final dioProvider = Provider<Dio>((ref) {
  final baseUrl = ref.watch(apiBaseUrlProvider);
  final dio = createDio(
    baseUrl: baseUrl.isEmpty ? _mockBaseUrl : baseUrl,
    auth: ref.watch(authServiceProvider),
  );
  if (baseUrl.isEmpty) {
    dio.httpClientAdapter = ref.watch(mockBackendAdapterProvider);
  }
  ref.onDispose(dio.close);
  return dio;
});

/// True while no backend URL is set.
final usingMockBackendProvider = Provider<bool>(
  (ref) => ref.watch(apiBaseUrlProvider).isEmpty,
);

Dio createDio({required String baseUrl, required AuthService auth}) {
  final dio = Dio(
    BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 15),
      sendTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 20),
      headers: {'Accept': 'application/json'},
    ),
  );
  dio.interceptors.add(AuthInterceptor(auth, dio));
  return dio;
}
