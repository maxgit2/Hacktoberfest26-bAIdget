import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/format/formatters.dart';
import '../../../core/theme/design_tokens.dart';
import '../../categories/data/categories_repository.dart';
import '../../categories/presentation/category_style.dart';
import '../domain/expense.dart';

/// Read-only for now; editing (PATCH) comes in the next phase.
class ExpenseDetailScreen extends ConsumerWidget {
  const ExpenseDetailScreen({
    super.key,
    required this.expense,
    this.justAdded = false,
  });

  final Expense expense;

  /// Shows the "saved" confirmation after an upload.
  final bool justAdded;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final categories = ref.watch(categoriesProvider).value ?? const [];
    final category = categories
        .where((c) => c.id == expense.categoryId)
        .firstOrNull;
    final scan = expense.scanDetails;
    final amount = expense.amountCents;

    return Scaffold(
      appBar: AppBar(title: const Text('Expense')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (justAdded)
            _Notice(
              icon: Icons.check_circle_outline,
              color: context.colors.success,
              title: 'Saved to your expenses',
            ),
          if (expense.needsReview)
            _Notice(
              icon: Icons.warning_amber_rounded,
              color: context.colors.warning,
              title: 'Please review this expense',
              body:
                  "Some details couldn't be read reliably. "
                  'Check the amount, date and items.',
            ),
          Text(expense.displayTitle, style: context.text.headlineMedium),
          if (expense.seller != null && expense.seller != expense.title)
            Text(expense.seller!, style: context.text.titleMedium),
          Text(
            formatDateTime(expense.date),
            style: context.text.bodyMedium?.copyWith(
              color: context.colors.textSecondary,
            ),
          ),
          const SizedBox(height: 16),
          if (amount != null)
            Text(
              formatMoney(amount),
              style: AppTextStyles.amountLarge.copyWith(
                color: context.colors.textPrimary,
              ),
            )
          else
            Text(
              'Amount not detected',
              style: context.text.titleLarge?.copyWith(
                color: context.colors.textSecondary,
              ),
            ),
          if (category != null) ...[
            const SizedBox(height: 8),
            Align(
              alignment: Alignment.centerLeft,
              child: Chip(
                avatar: CategoryDot(
                  color: categoryColor(category, categories, context.colors),
                ),
                label: Text(category.name),
              ),
            ),
          ],
          if (expense.description != null) ...[
            const SizedBox(height: 16),
            Text(expense.description!, style: context.text.bodyLarge),
          ],
          if (scan != null) ..._scanSection(context, scan),
        ],
      ),
    );
  }

  List<Widget> _scanSection(BuildContext context, ScanDetails scan) {
    final rows = <(String, String)>[
      if (scan.documentType != null)
        ('Document', _documentLabel(scan.documentType!)),
      if (scan.paymentMethod != null) ('Payment', scan.paymentMethod!),
      if (scan.vatTotalCents != null) ('VAT', formatMoney(scan.vatTotalCents!)),
      if (scan.vatNumber != null) ('VAT number', scan.vatNumber!),
    ];
    return [
      if (rows.isNotEmpty) ...[
        const SizedBox(height: 24),
        Text('Details', style: context.text.titleMedium),
        const Divider(),
        for (final (label, value) in rows)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 4),
            child: Row(
              children: [
                Expanded(
                  child: Text(
                    label,
                    style: context.text.bodyMedium?.copyWith(
                      color: context.colors.textSecondary,
                    ),
                  ),
                ),
                Text(value, style: context.text.bodyMedium),
              ],
            ),
          ),
      ],
      if (scan.items.isNotEmpty) ...[
        const SizedBox(height: 24),
        Text('Items', style: context.text.titleMedium),
        const Divider(),
        for (final item in scan.items)
          ListTile(
            contentPadding: EdgeInsets.zero,
            title: Text(item.description ?? 'Item'),
            subtitle: item.quantity == null || item.quantity == 1
                ? null
                : Text(
                    '${_quantity(item.quantity!)} × '
                    '${item.unitPriceCents == null ? '?' : formatMoney(item.unitPriceCents!)}',
                  ),
            trailing: item.totalCents == null
                ? null
                : Text(
                    formatMoney(item.totalCents!),
                    style: AppTextStyles.amount.copyWith(
                      color: context.colors.textPrimary,
                    ),
                  ),
          ),
      ],
    ];
  }

  static String _quantity(double q) =>
      q == q.roundToDouble() ? q.toInt().toString() : q.toString();

  static String _documentLabel(DocumentType t) => switch (t) {
    DocumentType.receipt => 'Receipt',
    DocumentType.invoice => 'Invoice',
    DocumentType.paymentScreenshot => 'Payment screenshot',
    DocumentType.other => 'Other',
  };
}

class _Notice extends StatelessWidget {
  const _Notice({
    required this.icon,
    required this.color,
    required this.title,
    this.body,
  });

  final IconData icon;
  final Color color;
  final String title;
  final String? body;

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: ListTile(
        leading: Icon(icon, color: color),
        title: Text(title),
        subtitle: body == null ? null : Text(body!),
      ),
    );
  }
}
