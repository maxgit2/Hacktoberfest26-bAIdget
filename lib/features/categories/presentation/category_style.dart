import 'package:flutter/material.dart';

import '../../../core/theme/design_tokens.dart';
import '../domain/category.dart';

/// Icons for the names the backend uses (`icon` field). Unknown → label.
const _icons = <String, IconData>{
  'shopping_cart': Icons.shopping_cart_outlined,
  'restaurant': Icons.restaurant_outlined,
  'directions_car': Icons.directions_car_outlined,
  'home': Icons.home_outlined,
  'receipt': Icons.receipt_outlined,
  'local_hospital': Icons.local_hospital_outlined,
  'movie': Icons.movie_outlined,
  'shopping_bag': Icons.shopping_bag_outlined,
  'flight': Icons.flight_outlined,
  'school': Icons.school_outlined,
  'subscriptions': Icons.subscriptions_outlined,
  'pets': Icons.pets_outlined,
  'fitness_center': Icons.fitness_center_outlined,
  'more_horiz': Icons.more_horiz,
};

IconData categoryIcon(String? name) => _icons[name] ?? Icons.label_outline;

/// The category's own `color` if set, otherwise a stable palette slot based
/// on its position in [all] (`Other` is always grey).
Color categoryColor(Category category, List<Category> all, AppColors colors) {
  final hex = category.color;
  if (hex != null && RegExp(r'^#[0-9a-fA-F]{6}$').hasMatch(hex)) {
    return Color(int.parse('FF${hex.substring(1)}', radix: 16));
  }
  if (category.isOther) return colors.categoryOther;
  final regular = all.where((c) => !c.isOther).toList();
  return colors.categoryAt(regular.indexWhere((c) => c.id == category.id));
}

class CategoryDot extends StatelessWidget {
  const CategoryDot({super.key, required this.color, this.size = 12});

  final Color color;
  final double size;

  @override
  Widget build(BuildContext context) => Container(
    width: size,
    height: size,
    decoration: BoxDecoration(color: color, shape: BoxShape.circle),
  );
}
