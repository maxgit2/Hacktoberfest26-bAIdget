import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/auth/auth_providers.dart';
import 'core/theme/design_tokens.dart';
import 'core/widgets/status_views.dart';
import 'features/account/data/account_repository.dart';
import 'features/auth/presentation/sign_in_screen.dart';
import 'features/onboarding/presentation/onboarding_screen.dart';
import 'features/upload/presentation/upload_screen.dart';

class BaidgetApp extends ConsumerStatefulWidget {
  const BaidgetApp({super.key});

  @override
  ConsumerState<BaidgetApp> createState() => _BaidgetAppState();
}

class _BaidgetAppState extends ConsumerState<BaidgetApp> {
  final _navigatorKey = GlobalKey<NavigatorState>();

  @override
  Widget build(BuildContext context) {
    // On sign-out (also when forced after a 401) drop any pushed screens.
    ref.listen(authStateProvider, (previous, next) {
      if (previous?.value != null && next.value == null) {
        _navigatorKey.currentState?.popUntil((route) => route.isFirst);
      }
    });

    return MaterialApp(
      title: 'bAIdget',
      navigatorKey: _navigatorKey,
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      home: const _AuthGate(),
    );
  }
}

/// Signed out → sign-in. Signed in → `/me` → onboarding or home.
class _AuthGate extends ConsumerWidget {
  const _AuthGate();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final auth = ref.watch(authStateProvider);
    return switch (auth) {
      AsyncData(value: null) || AsyncError() => const SignInScreen(),
      AsyncData() => const _ProfileGate(),
      _ => const LoadingView(),
    };
  }
}

class _ProfileGate extends ConsumerWidget {
  const _ProfileGate();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final me = ref.watch(meProvider);
    return me.when(
      loading: () => const LoadingView(),
      error: (e, _) => Scaffold(
        body: ErrorView(
          error: e,
          onRetry: () => ref.invalidate(meProvider),
          secondaryAction: TextButton(
            onPressed: () => ref.read(authServiceProvider).signOut(),
            child: const Text('Sign out'),
          ),
        ),
      ),
      data: (profile) => profile.onboardingCompleted
          ? const _Home()
          : const OnboardingScreen(),
    );
  }
}

/// Signed in and onboarded. Syncs recurring expenses on start and resume.
class _Home extends ConsumerStatefulWidget {
  const _Home();

  @override
  ConsumerState<_Home> createState() => _HomeState();
}

class _HomeState extends ConsumerState<_Home> with WidgetsBindingObserver {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _sync();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) _sync();
  }

  /// Fire and forget: a failure here must not block the app.
  void _sync() {
    ref
        .read(accountRepositoryProvider)
        .syncRecurringRules()
        .catchError((Object _) {});
  }

  @override
  Widget build(BuildContext context) => const UploadScreen();
}
