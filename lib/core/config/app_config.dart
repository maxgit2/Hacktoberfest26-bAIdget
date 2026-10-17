/// Build-time configuration:
///
/// ```
/// flutter run --dart-define=API_BASE_URL=https://api.example.com/v1 --dart-define=USE_FIREBASE=true
/// ```
abstract final class AppConfig {
  /// Default backend URL (including `/v1`). The URL saved in Settings wins.
  /// Empty = in-memory mock backend.
  static const apiBaseUrl = String.fromEnvironment('API_BASE_URL');

  /// Real Google sign-in through Firebase. Requires the Firebase config files
  /// (`flutterfire configure`). When false, a fake sign-in is used.
  static const useFirebase = bool.fromEnvironment('USE_FIREBASE');
}
