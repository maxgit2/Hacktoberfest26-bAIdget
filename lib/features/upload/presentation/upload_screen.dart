import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:uuid/uuid.dart';

import '../../../core/network/api_error_messages.dart';
import '../../../core/network/api_exception.dart';
import '../../../core/theme/design_tokens.dart';
import '../../expenses/data/expenses_repository.dart';
import '../../expenses/presentation/expense_detail_screen.dart';
import '../../settings/presentation/settings_screen.dart';
import '../data/receipt_image_picker.dart';

/// Home for now: pick a receipt / payment screenshot and upload it.
class UploadScreen extends ConsumerStatefulWidget {
  const UploadScreen({super.key});

  @override
  ConsumerState<UploadScreen> createState() => _UploadScreenState();
}

class _UploadScreenState extends ConsumerState<UploadScreen> {
  Uint8List? _image;

  /// Expense id for [_image], kept across retries (idempotent upload).
  String? _expenseId;
  bool _picking = false;
  bool _uploading = false;

  bool get _busy => _picking || _uploading;

  Future<void> _pick() async {
    setState(() => _picking = true);
    try {
      final jpeg = await ref.read(receiptImagePickerProvider).pick();
      if (jpeg != null && mounted) {
        setState(() {
          _image = jpeg;
          _expenseId = const Uuid().v4();
        });
      }
    } catch (_) {
      _showMessage("Couldn't open this image. Try another one.");
    } finally {
      if (mounted) setState(() => _picking = false);
    }
  }

  Future<void> _upload() async {
    final image = _image!;
    setState(() => _uploading = true);
    try {
      final expense = await ref
          .read(expensesRepositoryProvider)
          .scan(image, id: _expenseId!);
      if (!mounted) return;
      // Already saved on the server: start fresh for the next one.
      setState(() {
        _image = null;
        _expenseId = null;
        _uploading = false;
      });
      await Navigator.of(context).push(
        MaterialPageRoute<void>(
          builder: (_) =>
              ExpenseDetailScreen(expense: expense, justAdded: true),
        ),
      );
    } on ApiException catch (e) {
      _showMessage(
        describeApiError(e),
        // Same id: if the first attempt went through, nothing is duplicated.
        onRetry: e.isTransient && e.code != ApiErrorCode.rateLimited
            ? _upload
            : null,
      );
    } finally {
      if (mounted) setState(() => _uploading = false);
    }
  }

  void _showMessage(String message, {VoidCallback? onRetry}) {
    if (!mounted) return;
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(
        SnackBar(
          content: Text(message),
          action: onRetry == null
              ? null
              : SnackBarAction(label: 'Retry', onPressed: onRetry),
        ),
      );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add expense'),
        actions: [
          IconButton(
            tooltip: 'Settings',
            icon: const Icon(Icons.settings_outlined),
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute<void>(builder: (_) => const SettingsScreen()),
            ),
          ),
        ],
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Expanded(child: _buildPreview()),
              const SizedBox(height: 16),
              if (_uploading)
                Column(
                  children: [
                    const CircularProgressIndicator(),
                    const SizedBox(height: 12),
                    Text(
                      'Reading your receipt…',
                      style: context.text.bodyLarge,
                    ),
                    Text(
                      'This can take a few seconds.',
                      style: context.text.bodySmall,
                    ),
                  ],
                )
              else if (_image == null)
                FilledButton.icon(
                  onPressed: _busy ? null : _pick,
                  icon: const Icon(Icons.photo_library_outlined),
                  label: const Text('Choose from gallery'),
                )
              else ...[
                FilledButton.icon(
                  onPressed: _busy ? null : _upload,
                  icon: const Icon(Icons.cloud_upload_outlined),
                  label: const Text('Upload'),
                ),
                const SizedBox(height: 8),
                OutlinedButton(
                  onPressed: _busy ? null : _pick,
                  child: const Text('Choose another image'),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildPreview() {
    final image = _image;
    if (image == null) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              Icons.receipt_long_outlined,
              size: 96,
              color: context.colors.textMuted,
            ),
            const SizedBox(height: 12),
            Text(
              'Upload a photo of a receipt or a screenshot of a payment.',
              textAlign: TextAlign.center,
              style: context.text.bodyLarge,
            ),
          ],
        ),
      );
    }
    return ClipRRect(
      borderRadius: BorderRadius.circular(12),
      child: InteractiveViewer(
        maxScale: 5,
        child: Image.memory(
          image,
          fit: BoxFit.contain,
          errorBuilder: (_, _, _) => Center(
            child: Icon(
              Icons.broken_image_outlined,
              size: 64,
              color: context.colors.textMuted,
            ),
          ),
        ),
      ),
    );
  }
}
