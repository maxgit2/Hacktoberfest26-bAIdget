import 'dart:async';

class AppUser {
  const AppUser({required this.uid, this.email, this.displayName});

  final String uid;
  final String? email;
  final String? displayName;
}

/// The user closed the Google account picker.
class SignInCancelledException implements Exception {
  const SignInCancelledException();
}

/// Authentication only: the API is the single source of data.
abstract interface class AuthService {
  Stream<AppUser?> authStateChanges();

  AppUser? get currentUser;

  /// Throws [SignInCancelledException] if the user cancels.
  Future<void> signInWithGoogle();

  Future<void> signOut();

  /// Token for `Authorization: Bearer`. Null when signed out.
  Future<String?> getIdToken({bool forceRefresh = false});
}

/// Fake sign-in used until the Firebase config is available.
/// Works only with the mock backend: a real backend rejects its token.
class FakeAuthService implements AuthService {
  FakeAuthService({AppUser? initialUser}) : _user = initialUser;

  static const user = AppUser(
    uid: 'fake-uid',
    email: 'dev@baidget.test',
    displayName: 'Dev User',
  );

  AppUser? _user;
  final _controller = StreamController<AppUser?>.broadcast();

  @override
  Stream<AppUser?> authStateChanges() async* {
    yield _user;
    yield* _controller.stream;
  }

  @override
  AppUser? get currentUser => _user;

  @override
  Future<void> signInWithGoogle() async {
    _user = user;
    _controller.add(_user);
  }

  @override
  Future<void> signOut() async {
    _user = null;
    _controller.add(null);
  }

  @override
  Future<String?> getIdToken({bool forceRefresh = false}) async =>
      _user == null ? null : 'fake-token';
}
