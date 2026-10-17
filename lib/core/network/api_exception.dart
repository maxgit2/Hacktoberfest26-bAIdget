import 'package:dio/dio.dart';

/// Error codes from the backend contract (`error.code`) plus client-only ones.
/// Always branch on the code, never on the message.
abstract final class ApiErrorCode {
  // Backend
  static const unauthenticated = 'unauthenticated';
  static const notFound = 'not_found';
  static const alreadyOnboarded = 'already_onboarded';
  static const categoryInUse = 'category_in_use';
  static const cannotModifyOther = 'cannot_modify_other';
  static const categoryNameTaken = 'category_name_taken';
  static const alreadyRecurring = 'already_recurring';
  static const imageTooLarge = 'image_too_large';
  static const unsupportedImageType = 'unsupported_image_type';
  static const validationError = 'validation_error';
  static const minCategories = 'min_categories';
  static const maxCategories = 'max_categories';
  static const categoryNotFound = 'category_not_found';
  static const extractionFailed = 'extraction_failed';
  static const rateLimited = 'rate_limited';
  static const extractionUnavailable = 'extraction_unavailable';
  static const extractionTimeout = 'extraction_timeout';
  static const internalError = 'internal_error';

  // Client only
  static const noConnection = 'no_connection';
  static const timeout = 'timeout';
  static const invalidResponse = 'invalid_response';
  static const unknown = 'unknown';
}

class ApiException implements Exception {
  const ApiException(
    this.code, {
    this.statusCode,
    this.message,
    this.details = const {},
    this.retryAfter,
  });

  final String code;
  final int? statusCode;

  /// English, for logs. Don't show it to the user as-is.
  final String? message;
  final Map<String, dynamic> details;

  /// From the `Retry-After` header (`429`).
  final Duration? retryAfter;

  /// Worth retrying the same request later (network or AI provider issues).
  bool get isTransient => const {
    ApiErrorCode.noConnection,
    ApiErrorCode.timeout,
    ApiErrorCode.extractionUnavailable,
    ApiErrorCode.extractionTimeout,
    ApiErrorCode.rateLimited,
  }.contains(code);

  factory ApiException.fromDio(DioException e) {
    switch (e.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return const ApiException(ApiErrorCode.timeout);
      case DioExceptionType.connectionError:
        return const ApiException(ApiErrorCode.noConnection);
      case DioExceptionType.badResponse:
        return ApiException.fromResponse(e.response!);
      default:
        if (e.error is ApiException) return e.error! as ApiException;
        return ApiException(ApiErrorCode.unknown, message: e.message);
    }
  }

  /// Parses `{"error": {"code", "message", "details"}}`.
  factory ApiException.fromResponse(Response<dynamic> response) {
    final status = response.statusCode;
    final data = response.data;
    final error = data is Map ? data['error'] : null;
    final retryAfterSeconds = int.tryParse(
      response.headers.value('retry-after') ?? '',
    );

    if (error is Map) {
      final details = error['details'];
      return ApiException(
        error['code'] as String? ?? ApiErrorCode.unknown,
        statusCode: status,
        message: error['message'] as String?,
        details: details is Map ? details.cast<String, dynamic>() : const {},
        retryAfter: retryAfterSeconds == null
            ? null
            : Duration(seconds: retryAfterSeconds),
      );
    }
    return ApiException(
      status == 401 ? ApiErrorCode.unauthenticated : ApiErrorCode.unknown,
      statusCode: status,
    );
  }

  @override
  String toString() => 'ApiException($code, status: $statusCode, $message)';
}

/// Runs a request, turning Dio and JSON parsing errors into [ApiException].
Future<T> apiCall<T>(Future<T> Function() request) async {
  try {
    return await request();
  } on DioException catch (e) {
    throw ApiException.fromDio(e);
  } on TypeError catch (e) {
    throw ApiException(ApiErrorCode.invalidResponse, message: '$e');
  } on FormatException catch (e) {
    throw ApiException(ApiErrorCode.invalidResponse, message: '$e');
  }
}
