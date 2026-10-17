import 'api_exception.dart';

/// User-facing message for an API error.
String describeApiError(Object error) {
  if (error is! ApiException) return 'Something went wrong. Please try again.';
  return switch (error.code) {
    ApiErrorCode.noConnection =>
      'No connection. Check your internet and try again.',
    ApiErrorCode.timeout => 'The server is taking too long. Please try again.',
    ApiErrorCode.unauthenticated =>
      'Your session has expired. Please sign in again.',
    ApiErrorCode.imageTooLarge => 'This image is too large (max 10 MB).',
    ApiErrorCode.unsupportedImageType =>
      'Unsupported image type. Use JPEG, PNG or WebP.',
    ApiErrorCode.extractionFailed =>
      "We couldn't read this image. Try a clearer photo of the receipt.",
    ApiErrorCode.rateLimited => _rateLimited(error.retryAfter),
    ApiErrorCode.extractionUnavailable =>
      'Receipt reading is temporarily unavailable. Please try again later.',
    ApiErrorCode.extractionTimeout =>
      'Reading the receipt took too long. Please try again.',
    ApiErrorCode.categoryNameTaken =>
      'A category with this name already exists.',
    ApiErrorCode.minCategories => 'Pick at least 2 categories.',
    ApiErrorCode.maxCategories => 'You can have at most 30 categories.',
    _ => 'Something went wrong. Please try again.',
  };
}

String _rateLimited(Duration? retryAfter) {
  if (retryAfter == null) return 'Too many uploads. Please try again later.';
  final minutes = (retryAfter.inSeconds / 60).ceil();
  return minutes <= 1
      ? 'Too many uploads. Try again in a minute.'
      : 'Too many uploads. Try again in $minutes minutes.';
}
