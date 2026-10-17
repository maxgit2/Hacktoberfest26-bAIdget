import 'dart:typed_data';

import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http_parser/http_parser.dart';

import '../../../core/network/api_client.dart';
import '../../../core/network/api_exception.dart';
import '../domain/expense.dart';

class ExpensesRepository {
  ExpensesRepository(this._dio);

  final Dio _dio;

  /// The scan takes ~3–10 s; the contract asks for a 45 s client timeout.
  static const scanTimeout = Duration(seconds: 45);

  /// Uploads a receipt or payment screenshot. The expense comes back already
  /// saved (201, or 200 if [id] was already used).
  ///
  /// [id] is a client UUIDv4: after a timeout, retry with the SAME id so the
  /// expense is never created twice.
  Future<Expense> scan(Uint8List jpeg, {required String id}) =>
      apiCall(() async {
        final form = FormData.fromMap({
          'id': id,
          'image': MultipartFile.fromBytes(
            jpeg,
            filename: 'receipt.jpg',
            contentType: MediaType('image', 'jpeg'),
          ),
        });
        final res = await _dio.post<Map<String, dynamic>>(
          '/expenses/scan',
          data: form,
          options: Options(receiveTimeout: scanTimeout),
        );
        return Expense.fromJson(res.data!);
      });
}

final expensesRepositoryProvider = Provider<ExpensesRepository>(
  (ref) => ExpensesRepository(ref.watch(dioProvider)),
);
