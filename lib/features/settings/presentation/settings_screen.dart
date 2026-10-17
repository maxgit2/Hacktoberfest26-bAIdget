import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/auth/auth_providers.dart';
import '../../../core/config/app_config.dart';
import '../../../core/network/api_client.dart';
import '../../../core/settings/api_base_url.dart';
import '../../../core/theme/design_tokens.dart';

class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  final _formKey = GlobalKey<FormState>();
  late final _urlController = TextEditingController(
    text: ref.read(customApiBaseUrlProvider),
  );
  bool _saving = false;

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _saving = true);
    final notifier = ref.read(customApiBaseUrlProvider.notifier);
    await notifier.set(_urlController.text);
    if (!mounted) return;
    _urlController.text = ref.read(customApiBaseUrlProvider);
    setState(() => _saving = false);
    FocusScope.of(context).unfocus();
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(const SnackBar(content: Text('Settings saved')));
  }

  @override
  Widget build(BuildContext context) {
    final user = ref.watch(authStateProvider).value;
    final usingMock = ref.watch(usingMockBackendProvider);
    final baseUrl = ref.watch(apiBaseUrlProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text('Account', style: context.text.titleMedium),
            ListTile(
              contentPadding: EdgeInsets.zero,
              leading: const Icon(Icons.account_circle_outlined),
              title: Text(user?.displayName ?? 'Signed in'),
              subtitle: user?.email == null ? null : Text(user!.email!),
            ),
            OutlinedButton.icon(
              onPressed: () => ref.read(authServiceProvider).signOut(),
              icon: const Icon(Icons.logout),
              label: const Text('Sign out'),
            ),
            const SizedBox(height: 32),
            Text('Developer', style: context.text.titleMedium),
            const SizedBox(height: 12),
            TextFormField(
              controller: _urlController,
              decoration: InputDecoration(
                labelText: 'Backend URL',
                hintText: 'https://api.example.com/v1',
                helperText: AppConfig.apiBaseUrl.isEmpty
                    ? 'Include /v1. Leave empty to use the mock backend.'
                    : 'Include /v1. Leave empty to use ${AppConfig.apiBaseUrl}',
                helperMaxLines: 2,
                border: const OutlineInputBorder(),
                suffixIcon: IconButton(
                  tooltip: 'Clear',
                  icon: const Icon(Icons.clear),
                  onPressed: _urlController.clear,
                ),
              ),
              keyboardType: TextInputType.url,
              autocorrect: false,
              textInputAction: TextInputAction.done,
              validator: (value) =>
                  CustomApiBaseUrlNotifier.validate(value ?? ''),
              onFieldSubmitted: (_) => _save(),
            ),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: _saving ? null : _save,
              child: const Text('Save'),
            ),
            const SizedBox(height: 16),
            _StatusTile(
              ok: !usingMock,
              title: usingMock ? 'Mock backend active' : 'Backend in use',
              subtitle: usingMock
                  ? 'Uploads return sample data. Nothing leaves the device.'
                  : baseUrl,
            ),
            _StatusTile(
              ok: AppConfig.useFirebase,
              title: AppConfig.useFirebase
                  ? 'Google sign-in (Firebase)'
                  : 'Development sign-in',
              subtitle: AppConfig.useFirebase
                  ? null
                  : 'Works only with the mock backend.',
            ),
          ],
        ),
      ),
    );
  }
}

class _StatusTile extends StatelessWidget {
  const _StatusTile({required this.ok, required this.title, this.subtitle});

  final bool ok;
  final String title;
  final String? subtitle;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      leading: Icon(
        ok ? Icons.cloud_done_outlined : Icons.science_outlined,
        color: ok ? context.colors.success : context.colors.warning,
      ),
      title: Text(title),
      subtitle: subtitle == null ? null : Text(subtitle!),
    );
  }
}
