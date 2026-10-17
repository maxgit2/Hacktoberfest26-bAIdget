import 'package:intl/intl.dart';

final _eur = NumberFormat.simpleCurrency(locale: 'en_US', name: 'EUR');
final _date = DateFormat.yMMMd('en_US');
final _dateTime = DateFormat.yMMMd('en_US').add_jm();

/// `2340` → `€23.40`. EUR only for now (see the API contract).
String formatMoney(int cents) => _eur.format(cents / 100);

/// `Oct 16, 2026`, in the device time zone.
String formatDate(DateTime date) => _date.format(date.toLocal());

/// `Oct 16, 2026 12:30 PM`, in the device time zone.
String formatDateTime(DateTime date) => _dateTime.format(date.toLocal());
