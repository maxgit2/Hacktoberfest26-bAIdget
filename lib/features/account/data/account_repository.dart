import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/auth/auth_providers.dart';
import '../../../core/network/api_client.dart';
import '../../../core/network/api_exception.dart';
import '../domain/user_profile.dart';

class AccountRepository {
  AccountRepository(this._dio);

  final Dio _dio;

  /// Creates the profile on the first call.
  Future<UserProfile> getMe() => apiCall(() async {
    final res = await _dio.get<Map<String, dynamic>>('/me');
    return UserProfile.fromJson(res.data!);
  });

  /// Creates missing recurring occurrences up to now. Idempotent.
  Future<void> syncRecurringRules() => apiCall(() async {
    // At most a few rounds, in case the server keeps saying has_more.
    for (var i = 0; i < 5; i++) {
      final res = await _dio.post<Map<String, dynamic>>(
        '/recurring-rules/sync',
      );
      if (res.data?['has_more'] != true) return;
    }
  });
}

final accountRepositoryProvider = Provider<AccountRepository>(
  (ref) => AccountRepository(ref.watch(dioProvider)),
);

/// Profile of the signed-in user. Reloaded when the user changes.
final meProvider = FutureProvider<UserProfile>((ref) async {
  final user = await ref.watch(authStateProvider.future);
  if (user == null) throw StateError('Not signed in');
  return ref.watch(accountRepositoryProvider).getMe();
});
