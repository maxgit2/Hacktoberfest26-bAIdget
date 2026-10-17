import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/network/api_error_messages.dart';
import '../../../core/network/api_exception.dart';
import '../../../core/theme/design_tokens.dart';
import '../../../core/widgets/status_views.dart';
import '../../account/data/account_repository.dart';
import '../../categories/data/categories_repository.dart';
import '../../categories/domain/category.dart';
import '../../categories/presentation/category_style.dart';

/// First launch: the user picks at least 2 categories.
class OnboardingScreen extends ConsumerStatefulWidget {
  const OnboardingScreen({super.key});

  @override
  ConsumerState<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends ConsumerState<OnboardingScreen> {
  final _selected = <String>{};
  final _custom = <NewCategory>[];
  bool _submitting = false;

  int get _count => _selected.length + _custom.length;
  bool get _canSubmit =>
      !_submitting &&
      _count >= CategoryLimits.minOnboarding &&
      _count <= CategoryLimits.max;

  void _applyPreset(CatalogPreset preset) => setState(() {
    _selected
      ..clear()
      ..addAll(preset.catalogIds);
  });

  Future<void> _addCustom(CategoryCatalog catalog) async {
    final taken = {
      'other',
      for (final i in catalog.items) i.name.toLowerCase(),
      for (final c in _custom) c.name.toLowerCase(),
    };
    final name = await showDialog<String>(
      context: context,
      builder: (_) => _CustomCategoryDialog(takenNames: taken),
    );
    if (name != null) setState(() => _custom.add(NewCategory(name: name)));
  }

  Future<void> _submit() async {
    setState(() => _submitting = true);
    try {
      await ref
          .read(categoriesRepositoryProvider)
          .completeOnboarding(catalogIds: _selected.toList(), custom: _custom);
      _finish();
    } on ApiException catch (e) {
      if (e.code == ApiErrorCode.alreadyOnboarded) return _finish();
      if (!mounted) return;
      setState(() => _submitting = false);
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(describeApiError(e))));
    }
  }

  /// The gate re-reads `/me` and moves on to the home screen.
  void _finish() {
    ref.invalidate(categoriesProvider);
    ref.invalidate(meProvider);
  }

  @override
  Widget build(BuildContext context) {
    final catalog = ref.watch(categoryCatalogProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Your categories')),
      body: catalog.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => ErrorView(
          error: e,
          onRetry: () => ref.invalidate(categoryCatalogProvider),
        ),
        data: _buildContent,
      ),
      bottomNavigationBar: catalog.hasValue
          ? SafeArea(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: FilledButton(
                  onPressed: _canSubmit ? _submit : null,
                  child: _submitting
                      ? const SizedBox.square(
                          dimension: 18,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : Text(
                          _count < CategoryLimits.minOnboarding
                              ? 'Pick at least ${CategoryLimits.minOnboarding}'
                              : 'Continue with $_count categories',
                        ),
                ),
              ),
            )
          : null,
    );
  }

  Widget _buildContent(CategoryCatalog catalog) {
    return ListView(
      padding: const EdgeInsets.symmetric(vertical: 16),
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: Text(
            'Pick the categories you want to track. You can change them '
            'later. An "Other" category is always added for you.',
            style: context.text.bodyMedium?.copyWith(
              color: context.colors.textSecondary,
            ),
          ),
        ),
        if (catalog.presets.isNotEmpty) ...[
          const SizedBox(height: 16),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Wrap(
              spacing: 8,
              children: [
                for (final p in catalog.presets)
                  ActionChip(
                    avatar: const Icon(Icons.auto_awesome_outlined, size: 18),
                    label: Text(p.name),
                    onPressed: _submitting ? null : () => _applyPreset(p),
                  ),
              ],
            ),
          ),
        ],
        const SizedBox(height: 8),
        for (final item in catalog.items)
          CheckboxListTile(
            value: _selected.contains(item.id),
            onChanged: _submitting
                ? null
                : (on) => setState(
                    () => on == true
                        ? _selected.add(item.id)
                        : _selected.remove(item.id),
                  ),
            secondary: Icon(categoryIcon(item.icon)),
            title: Text(item.name),
          ),
        const Divider(),
        for (final c in _custom)
          ListTile(
            leading: Icon(categoryIcon(c.icon)),
            title: Text(c.name),
            trailing: IconButton(
              tooltip: 'Remove',
              icon: const Icon(Icons.close),
              onPressed: _submitting
                  ? null
                  : () => setState(() => _custom.remove(c)),
            ),
          ),
        ListTile(
          leading: const Icon(Icons.add),
          title: const Text('Add a custom category'),
          enabled: !_submitting && _count < CategoryLimits.max,
          onTap: () => _addCustom(catalog),
        ),
      ],
    );
  }
}

class _CustomCategoryDialog extends StatefulWidget {
  const _CustomCategoryDialog({required this.takenNames});

  final Set<String> takenNames;

  @override
  State<_CustomCategoryDialog> createState() => _CustomCategoryDialogState();
}

class _CustomCategoryDialogState extends State<_CustomCategoryDialog> {
  final _formKey = GlobalKey<FormState>();
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _save() {
    if (_formKey.currentState!.validate()) {
      Navigator.of(context).pop(_controller.text.trim());
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('New category'),
      content: Form(
        key: _formKey,
        child: TextFormField(
          controller: _controller,
          autofocus: true,
          maxLength: 40,
          textCapitalization: TextCapitalization.sentences,
          decoration: const InputDecoration(labelText: 'Name'),
          validator: (value) {
            final name = value?.trim() ?? '';
            if (name.isEmpty) return 'Enter a name';
            if (widget.takenNames.contains(name.toLowerCase())) {
              return 'This category already exists';
            }
            return null;
          },
          onFieldSubmitted: (_) => _save(),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Cancel'),
        ),
        FilledButton(onPressed: _save, child: const Text('Add')),
      ],
    );
  }
}
