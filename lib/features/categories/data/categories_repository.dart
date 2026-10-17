import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/auth/auth_providers.dart';
import '../../../core/network/api_client.dart';
import '../../../core/network/api_exception.dart';
import '../domain/category.dart';

class CategoriesRepository {
  CategoriesRepository(this._dio);

  final Dio _dio;

  Future<CategoryCatalog> getCatalog() => apiCall(() async {
    final res = await _dio.get<Map<String, dynamic>>('/categories/catalog');
    return CategoryCatalog.fromJson(res.data!);
  });

  /// Active categories only.
  Future<List<Category>> getCategories() => apiCall(() async {
    final res = await _dio.get<Map<String, dynamic>>('/categories');
    return [
      for (final c in res.data!['items'] as List)
        Category.fromJson(c as Map<String, dynamic>),
    ];
  });

  /// The server adds `Other` automatically.
  Future<List<Category>> completeOnboarding({
    required List<String> catalogIds,
    required List<NewCategory> custom,
  }) => apiCall(() async {
    final res = await _dio.post<Map<String, dynamic>>(
      '/categories/onboarding',
      data: {
        'catalog_ids': catalogIds,
        'custom': [for (final c in custom) c.toJson()],
      },
    );
    return [
      for (final c in res.data!['categories'] as List)
        Category.fromJson(c as Map<String, dynamic>),
    ];
  });
}

final categoriesRepositoryProvider = Provider<CategoriesRepository>(
  (ref) => CategoriesRepository(ref.watch(dioProvider)),
);

final categoryCatalogProvider = FutureProvider<CategoryCatalog>(
  (ref) => ref.watch(categoriesRepositoryProvider).getCatalog(),
);

/// Reloaded when the user changes.
final categoriesProvider = FutureProvider<List<Category>>((ref) async {
  final user = await ref.watch(authStateProvider.future);
  if (user == null) return const [];
  return ref.watch(categoriesRepositoryProvider).getCategories();
});
