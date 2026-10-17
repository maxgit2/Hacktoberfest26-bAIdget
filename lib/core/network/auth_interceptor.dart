import 'package:dio/dio.dart';

import '../auth/auth_service.dart';

/// Adds `Authorization: Bearer <token>` to every request (except /health).
/// On `401` it force-refreshes the token and retries ONCE; if that fails too,
/// it signs the user out.
class AuthInterceptor extends Interceptor {
  AuthInterceptor(this._auth, this._dio);

  final AuthService _auth;
  final Dio _dio;

  static const _retriedKey = 'auth_retried';

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // A retry already carries the force-refreshed token.
    if (options.path != '/health' && options.extra[_retriedKey] != true) {
      try {
        final token = await _auth.getIdToken();
        if (token != null) options.headers['Authorization'] = 'Bearer $token';
      } catch (error, stackTrace) {
        return handler.reject(
          DioException(
            requestOptions: options,
            error: error,
            stackTrace: stackTrace,
            message: 'Could not obtain an authentication token',
          ),
        );
      }
    }
    handler.next(options);
  }

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    final options = err.requestOptions;
    if (err.response?.statusCode != 401) return handler.next(err);

    if (options.extra[_retriedKey] == true) {
      await _signOutSafely();
      return handler.next(err);
    }

    final String? token;
    try {
      token = await _auth.getIdToken(forceRefresh: true);
    } catch (_) {
      await _signOutSafely();
      return handler.next(err);
    }
    if (token == null) {
      await _signOutSafely();
      return handler.next(err);
    }

    options
      ..extra[_retriedKey] = true
      ..headers['Authorization'] = 'Bearer $token';
    // A multipart body can be sent only once.
    if (options.data is FormData) {
      options.data = (options.data as FormData).clone();
    }

    try {
      handler.resolve(await _dio.fetch<dynamic>(options));
    } on DioException catch (e) {
      handler.next(e);
    }
  }

  Future<void> _signOutSafely() async {
    try {
      await _auth.signOut();
    } catch (_) {
      // Preserve the original 401 even if provider sign-out fails.
    }
  }
}
