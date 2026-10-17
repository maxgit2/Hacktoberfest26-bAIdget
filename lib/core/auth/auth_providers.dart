import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../config/app_config.dart';
import 'auth_service.dart';
import 'firebase_auth_service.dart';

final authServiceProvider = Provider<AuthService>(
  (ref) => AppConfig.useFirebase ? FirebaseAuthService() : FakeAuthService(),
);

final authStateProvider = StreamProvider<AppUser?>(
  (ref) => ref.watch(authServiceProvider).authStateChanges(),
);
