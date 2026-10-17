/// Expense as returned by the API.
///
/// Money: the API sends a number with at most 2 decimals; here it is kept as
/// integer cents to avoid floating point errors.
library;

enum ExpenseType { single, recurring }

enum ExpenseSource { manual, scan }

enum DocumentType { receipt, invoice, paymentScreenshot, other }

int? _toCents(Object? amount) =>
    amount == null ? null : ((amount as num) * 100).round();

class ScanItem {
  const ScanItem({
    required this.description,
    this.quantity,
    this.unitPriceCents,
    this.totalCents,
  });

  final String? description;
  final double? quantity;
  final int? unitPriceCents;
  final int? totalCents;

  factory ScanItem.fromJson(Map<String, dynamic> json) => ScanItem(
    description: json['description'] as String?,
    quantity: (json['quantity'] as num?)?.toDouble(),
    unitPriceCents: _toCents(json['unit_price']),
    totalCents: _toCents(json['total']),
  );
}

class ScanDetails {
  const ScanDetails({
    this.documentType,
    this.items = const [],
    this.vatTotalCents,
    this.vatNumber,
    this.paymentMethod,
  });

  final DocumentType? documentType;
  final List<ScanItem> items;
  final int? vatTotalCents;
  final String? vatNumber;
  final String? paymentMethod;

  factory ScanDetails.fromJson(Map<String, dynamic> json) => ScanDetails(
    documentType: switch (json['document_type']) {
      'receipt' => DocumentType.receipt,
      'invoice' => DocumentType.invoice,
      'payment_screenshot' => DocumentType.paymentScreenshot,
      'other' => DocumentType.other,
      _ => null,
    },
    items: [
      for (final i in (json['items'] as List? ?? const []))
        ScanItem.fromJson(i as Map<String, dynamic>),
    ],
    vatTotalCents: _toCents(json['vat_total']),
    vatNumber: json['vat_number'] as String?,
    paymentMethod: json['payment_method'] as String?,
  );
}

class Expense {
  const Expense({
    required this.id,
    required this.date,
    required this.categoryId,
    required this.type,
    required this.source,
    required this.currency,
    required this.needsReview,
    this.seller,
    this.title,
    this.description,
    this.amountCents,
    this.recurrenceRuleId,
    this.scanDetails,
    this.createdAt,
    this.updatedAt,
  });

  final String id;

  /// UTC. Show it with `.toLocal()`.
  final DateTime date;
  final String? seller;
  final String? title;
  final String? description;
  final String categoryId;
  final ExpenseType type;
  final String? recurrenceRuleId;

  /// Null when the scan could not read it (not counted in totals).
  final int? amountCents;
  final String currency;
  final ExpenseSource source;
  final ScanDetails? scanDetails;

  /// Amount, date or items unreliable: ask the user to check.
  final bool needsReview;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  /// Best label for lists and headers.
  String get displayTitle => title ?? seller ?? 'Untitled expense';

  factory Expense.fromJson(Map<String, dynamic> json) {
    final recurrence = json['recurrence'] as Map<String, dynamic>?;
    final scan = json['scan_details'] as Map<String, dynamic>?;
    return Expense(
      id: json['id'] as String,
      date: DateTime.parse(json['date'] as String),
      seller: json['seller'] as String?,
      title: json['title'] as String?,
      description: json['description'] as String?,
      categoryId: json['category'] as String,
      type: json['type'] == 'recurring'
          ? ExpenseType.recurring
          : ExpenseType.single,
      recurrenceRuleId: recurrence?['rule_id'] as String?,
      amountCents: _toCents(json['amount']),
      currency: json['currency'] as String? ?? 'EUR',
      source: json['source'] == 'scan'
          ? ExpenseSource.scan
          : ExpenseSource.manual,
      scanDetails: scan == null ? null : ScanDetails.fromJson(scan),
      needsReview: json['needs_review'] as bool? ?? false,
      createdAt: DateTime.tryParse(json['created_at'] as String? ?? ''),
      updatedAt: DateTime.tryParse(json['updated_at'] as String? ?? ''),
    );
  }
}
