/// A user category (`GET /categories`).
class Category {
  const Category({
    required this.id,
    required this.name,
    this.icon,
    this.color,
    this.catalogId,
    this.isOther = false,
  });

  final String id;
  final String name;

  /// Material icon name, e.g. `shopping_cart`. Free string, optional.
  final String? icon;

  /// Hex color, e.g. `#4CAF50`. Free string, optional.
  final String? color;
  final String? catalogId;

  /// The automatic `Other` category: can be renamed, never deleted.
  final bool isOther;

  factory Category.fromJson(Map<String, dynamic> json) => Category(
    id: json['id'] as String,
    name: json['name'] as String,
    icon: json['icon'] as String?,
    color: json['color'] as String?,
    catalogId: json['catalog_id'] as String?,
    isOther: json['is_other'] as bool? ?? false,
  );

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'icon': icon,
    'color': color,
    'catalog_id': catalogId,
    'is_other': isOther,
  };
}

/// An entry of the static catalog (`GET /categories/catalog`).
class CatalogItem {
  const CatalogItem({required this.id, required this.name, this.icon});

  final String id;
  final String name;
  final String? icon;

  factory CatalogItem.fromJson(Map<String, dynamic> json) => CatalogItem(
    id: json['id'] as String,
    name: json['name'] as String,
    icon: json['icon'] as String?,
  );
}

/// A shortcut that preselects some catalog items.
class CatalogPreset {
  const CatalogPreset({
    required this.id,
    required this.name,
    required this.catalogIds,
  });

  final String id;
  final String name;
  final List<String> catalogIds;

  factory CatalogPreset.fromJson(Map<String, dynamic> json) => CatalogPreset(
    id: json['id'] as String,
    name: json['name'] as String,
    catalogIds: (json['catalog_ids'] as List).cast<String>(),
  );
}

class CategoryCatalog {
  const CategoryCatalog({required this.items, required this.presets});

  final List<CatalogItem> items;
  final List<CatalogPreset> presets;

  factory CategoryCatalog.fromJson(Map<String, dynamic> json) =>
      CategoryCatalog(
        items: [
          for (final i in json['items'] as List)
            CatalogItem.fromJson(i as Map<String, dynamic>),
        ],
        presets: [
          for (final p in json['presets'] as List)
            CatalogPreset.fromJson(p as Map<String, dynamic>),
        ],
      );
}

/// A custom category in the onboarding body.
class NewCategory {
  const NewCategory({required this.name, this.icon, this.color});

  final String name;
  final String? icon;
  final String? color;

  Map<String, dynamic> toJson() => {
    'name': name,
    if (icon != null) 'icon': icon,
    if (color != null) 'color': color,
  };
}

/// Limits from the contract. `Other` is added by the server and not counted.
abstract final class CategoryLimits {
  static const minOnboarding = 2;
  static const max = 30;
}
