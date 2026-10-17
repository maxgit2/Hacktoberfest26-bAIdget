import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../config/app_config.dart';

/// Overridden in `main()` with the loaded instance.
final sharedPreferencesProvider = Provider<SharedPreferences>(
  (ref) => throw UnimplementedError('sharedPreferencesProvider not overridden'),
);

/// The URL typed in Settings ('' when not set).
final customApiBaseUrlProvider =
    NotifierProvider<CustomApiBaseUrlNotifier, String>(
      CustomApiBaseUrlNotifier.new,
    );

/// The URL actually used: Settings, then `--dart-define`, then '' (mock).
final apiBaseUrlProvider = Provider<String>((ref) {
  final custom = ref.watch(customApiBaseUrlProvider);
  return custom.isNotEmpty ? custom : AppConfig.apiBaseUrl;
});

class CustomApiBaseUrlNotifier extends Notifier<String> {
  static const _key = 'api_base_url';

  @override
  String build() => ref.read(sharedPreferencesProvider).getString(_key) ?? '';

  /// Saves the URL; an empty string goes back to the default.
  Future<void> set(String url) async {
    final prefs = ref.read(sharedPreferencesProvider);
    final normalized = normalizeUrl(url);
    if (normalized.isEmpty) {
      await prefs.remove(_key);
    } else {
      await prefs.setString(_key, normalized);
    }
    state = normalized;
  }

  static String normalizeUrl(String url) {
    var u = url.trim();
    while (u.endsWith('/')) {
      u = u.substring(0, u.length - 1);
    }
    return u;
  }

  /// Error message, or null if the URL is valid (or empty).
  static String? validate(String url) {
    final u = normalizeUrl(url);
    if (u.isEmpty) return null;
    final uri = Uri.tryParse(u);
    if (uri == null ||
        !(uri.scheme == 'http' || uri.scheme == 'https') ||
        uri.host.isEmpty) {
      return 'Enter a full URL, e.g. https://api.example.com/v1';
    }
    return null;
  }
}
