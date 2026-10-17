import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/auth/auth_providers.dart';
import '../../../core/auth/auth_service.dart';
import '../../../core/config/app_config.dart';
import '../../../core/theme/design_tokens.dart';

class SignInScreen extends ConsumerStatefulWidget {
  const SignInScreen({super.key});

  @override
  ConsumerState<SignInScreen> createState() => _SignInScreenState();
}

class _SignInScreenState extends ConsumerState<SignInScreen> {
  bool _busy = false;

  Future<void> _signIn() async {
    setState(() => _busy = true);
    try {
      await ref.read(authServiceProvider).signInWithGoogle();
    } on SignInCancelledException {
      // The user closed the picker: nothing to say.
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Sign-in failed. Please try again.')),
        );
      }
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Spacer(),
              Icon(
                Icons.receipt_long_outlined,
                size: 72,
                color: context.colors.brand,
              ),
              const SizedBox(height: 16),
              Text(
                'bAIdget',
                textAlign: TextAlign.center,
                style: context.text.displayMedium,
              ),
              const SizedBox(height: 8),
              Text(
                'Upload your receipts, we sort your expenses.',
                textAlign: TextAlign.center,
                style: context.text.bodyLarge?.copyWith(
                  color: context.colors.textSecondary,
                ),
              ),
              const Spacer(),
              FilledButton.icon(
                onPressed: _busy ? null : _signIn,
                icon: _busy
                    ? const SizedBox.square(
                        dimension: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.login),
                label: const Text('Continue with Google'),
              ),
              if (!AppConfig.useFirebase) ...[
                const SizedBox(height: 8),
                Text(
                  'Development sign-in: Firebase is not configured.',
                  textAlign: TextAlign.center,
                  style: context.text.bodySmall,
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
