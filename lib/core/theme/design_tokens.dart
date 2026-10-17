import 'package:flutter/material.dart';

/// bAIdget design tokens: colors and text styles.
///
/// Never hard-code hex values or font sizes in widgets: always go through
/// `context.colors` / `context.text` (or `Theme.of(context)`).

// ---------------------------------------------------------------------------
// Raw palette: hex values live ONLY here.
// ---------------------------------------------------------------------------

abstract final class AppPalette {
  // Brand
  static const teal700 = Color(0xFF0F766E);
  static const teal400 = Color(0xFF2DD4BF);
  static const teal100 = Color(0xFFCCFBF1);
  static const teal900 = Color(0xFF134E4A);
  static const teal950 = Color(0xFF042F2E);

  // Neutrals — light
  static const surfaceLight = Color(0xFFFCFCFB);
  static const pageLight = Color(0xFFF9F9F7);
  static const inkLight = Color(0xFF0B0B0B);
  static const inkSecondaryLight = Color(0xFF52514E);
  static const hairlineLight = Color(0xFFE1E0D9);
  static const borderLight = Color(0xFFC3C2B7);

  // Neutrals — dark
  static const surfaceDark = Color(0xFF1A1A19);
  static const pageDark = Color(0xFF0D0D0D);
  static const inkDark = Color(0xFFF0EFEC);
  static const inkSecondaryDark = Color(0xFFC3C2B7);
  static const hairlineDark = Color(0xFF2C2C2A);
  static const borderDark = Color(0xFF383835);

  static const inkMuted = Color(0xFF898781);

  // Status colors (fixed, same in both themes). Always pair with icon + text.
  static const good = Color(0xFF0CA30C);
  static const warning = Color(0xFFFAB219);
  static const serious = Color(0xFFEC835A);
  static const critical = Color(0xFFD03B3B);
  static const goodTextLight = Color(0xFF006300);
}

// ---------------------------------------------------------------------------
// Semantic colors (ThemeExtension, switch with light/dark).
// ---------------------------------------------------------------------------

@immutable
class AppColors extends ThemeExtension<AppColors> {
  const AppColors({
    required this.brand,
    required this.onBrand,
    required this.brandContainer,
    required this.onBrandContainer,
    required this.page,
    required this.surface,
    required this.textPrimary,
    required this.textSecondary,
    required this.textMuted,
    required this.divider,
    required this.border,
    required this.success,
    required this.successText,
    required this.warning,
    required this.serious,
    required this.error,
    required this.categories,
    required this.categoryOther,
  });

  final Color brand;
  final Color onBrand;
  final Color brandContainer;
  final Color onBrandContainer;

  /// Page background.
  final Color page;

  /// Background of cards, sheets and charts.
  final Color surface;

  final Color textPrimary;
  final Color textSecondary;
  final Color textMuted;

  /// Hairlines (dividers, chart grids).
  final Color divider;

  /// Input and card borders, chart axes.
  final Color border;

  final Color success;

  /// "Positive" text (e.g. savings, under budget).
  final Color successText;
  final Color warning;
  final Color serious;
  final Color error;

  /// Fallback expense-category colors, in a FIXED order: category N always
  /// uses `categories[N]`, never cycled. Past the eighth, use
  /// [categoryOther]. The order keeps neighbours distinguishable for
  /// colour-blind users: do not reorder.
  ///
  /// The colour marks identity on dots, bars and chips; the text next to it
  /// stays in [textPrimary]/[textSecondary].
  final List<Color> categories;
  final Color categoryOther;

  /// Stable colour for the category at [index].
  Color categoryAt(int index) => index >= 0 && index < categories.length
      ? categories[index]
      : categoryOther;

  static const light = AppColors(
    brand: AppPalette.teal700,
    onBrand: Colors.white,
    brandContainer: AppPalette.teal100,
    onBrandContainer: AppPalette.teal950,
    page: AppPalette.pageLight,
    surface: AppPalette.surfaceLight,
    textPrimary: AppPalette.inkLight,
    textSecondary: AppPalette.inkSecondaryLight,
    textMuted: AppPalette.inkMuted,
    divider: AppPalette.hairlineLight,
    border: AppPalette.borderLight,
    success: AppPalette.good,
    successText: AppPalette.goodTextLight,
    warning: AppPalette.warning,
    serious: AppPalette.serious,
    error: AppPalette.critical,
    categories: [
      Color(0xFF2A78D6), // blue
      Color(0xFFEB6834), // orange
      Color(0xFF1BAF7A), // aqua
      Color(0xFFEDA100), // yellow
      Color(0xFFE87BA4), // magenta
      Color(0xFF008300), // green
      Color(0xFF6250D6), // violet
      Color(0xFFE34948), // red
    ],
    categoryOther: AppPalette.inkMuted,
  );

  static const dark = AppColors(
    brand: AppPalette.teal400,
    onBrand: AppPalette.teal950,
    brandContainer: AppPalette.teal900,
    onBrandContainer: AppPalette.teal100,
    page: AppPalette.pageDark,
    surface: AppPalette.surfaceDark,
    textPrimary: AppPalette.inkDark,
    textSecondary: AppPalette.inkSecondaryDark,
    textMuted: AppPalette.inkMuted,
    divider: AppPalette.hairlineDark,
    border: AppPalette.borderDark,
    success: AppPalette.good,
    successText: AppPalette.good,
    warning: AppPalette.warning,
    serious: AppPalette.serious,
    error: AppPalette.critical,
    categories: [
      Color(0xFF3987E5), // blue
      Color(0xFFD95926), // orange
      Color(0xFF199E70), // aqua
      Color(0xFFC98500), // yellow
      Color(0xFFD55181), // magenta
      Color(0xFF008300), // green
      Color(0xFF9085E9), // violet
      Color(0xFFE66767), // red
    ],
    categoryOther: AppPalette.inkMuted,
  );

  @override
  AppColors copyWith({
    Color? brand,
    Color? onBrand,
    Color? brandContainer,
    Color? onBrandContainer,
    Color? page,
    Color? surface,
    Color? textPrimary,
    Color? textSecondary,
    Color? textMuted,
    Color? divider,
    Color? border,
    Color? success,
    Color? successText,
    Color? warning,
    Color? serious,
    Color? error,
    List<Color>? categories,
    Color? categoryOther,
  }) {
    return AppColors(
      brand: brand ?? this.brand,
      onBrand: onBrand ?? this.onBrand,
      brandContainer: brandContainer ?? this.brandContainer,
      onBrandContainer: onBrandContainer ?? this.onBrandContainer,
      page: page ?? this.page,
      surface: surface ?? this.surface,
      textPrimary: textPrimary ?? this.textPrimary,
      textSecondary: textSecondary ?? this.textSecondary,
      textMuted: textMuted ?? this.textMuted,
      divider: divider ?? this.divider,
      border: border ?? this.border,
      success: success ?? this.success,
      successText: successText ?? this.successText,
      warning: warning ?? this.warning,
      serious: serious ?? this.serious,
      error: error ?? this.error,
      categories: categories ?? this.categories,
      categoryOther: categoryOther ?? this.categoryOther,
    );
  }

  @override
  AppColors lerp(AppColors? other, double t) {
    if (other == null) return this;
    Color l(Color a, Color b) => Color.lerp(a, b, t)!;
    return AppColors(
      brand: l(brand, other.brand),
      onBrand: l(onBrand, other.onBrand),
      brandContainer: l(brandContainer, other.brandContainer),
      onBrandContainer: l(onBrandContainer, other.onBrandContainer),
      page: l(page, other.page),
      surface: l(surface, other.surface),
      textPrimary: l(textPrimary, other.textPrimary),
      textSecondary: l(textSecondary, other.textSecondary),
      textMuted: l(textMuted, other.textMuted),
      divider: l(divider, other.divider),
      border: l(border, other.border),
      success: l(success, other.success),
      successText: l(successText, other.successText),
      warning: l(warning, other.warning),
      serious: l(serious, other.serious),
      error: l(error, other.error),
      categories: [
        for (var i = 0; i < categories.length; i++)
          l(categories[i], other.categories[i]),
      ],
      categoryOther: l(categoryOther, other.categoryOther),
    );
  }
}

// ---------------------------------------------------------------------------
// Text styles. No colour: the theme applies it (textPrimary).
// System font (Roboto / SF Pro).
// ---------------------------------------------------------------------------

abstract final class AppTextStyles {
  static const _tabular = [FontFeature.tabularFigures()];

  /// Hero figure (monthly total on the dashboard).
  static const display = TextStyle(
    fontSize: 40,
    height: 1.1,
    fontWeight: FontWeight.w700,
    letterSpacing: -0.5,
  );

  /// Page titles.
  static const headlineLarge = TextStyle(
    fontSize: 28,
    height: 1.2,
    fontWeight: FontWeight.w700,
    letterSpacing: -0.25,
  );

  /// Large section titles.
  static const headline = TextStyle(
    fontSize: 24,
    height: 1.25,
    fontWeight: FontWeight.w600,
  );

  /// App bar, card titles.
  static const title = TextStyle(
    fontSize: 20,
    height: 1.3,
    fontWeight: FontWeight.w600,
  );

  /// List rows (seller name), subtitles.
  static const titleSmall = TextStyle(
    fontSize: 16,
    height: 1.35,
    fontWeight: FontWeight.w600,
  );

  /// Body text.
  static const body = TextStyle(
    fontSize: 16,
    height: 1.5,
    fontWeight: FontWeight.w400,
  );

  /// Secondary text, descriptions.
  static const bodySmall = TextStyle(
    fontSize: 14,
    height: 1.45,
    fontWeight: FontWeight.w400,
  );

  /// Buttons, chips, tabs.
  static const label = TextStyle(
    fontSize: 14,
    height: 1.3,
    fontWeight: FontWeight.w600,
    letterSpacing: 0.1,
  );

  /// Captions, dates, chart labels.
  static const caption = TextStyle(
    fontSize: 12,
    height: 1.35,
    fontWeight: FontWeight.w500,
    letterSpacing: 0.2,
  );

  // Amounts: tabular figures so columns stay aligned.

  /// Amount in list rows and details.
  static const amount = TextStyle(
    fontSize: 16,
    height: 1.35,
    fontWeight: FontWeight.w600,
    fontFeatures: _tabular,
  );

  /// Large amount (receipt total).
  static const amountLarge = TextStyle(
    fontSize: 28,
    height: 1.2,
    fontWeight: FontWeight.w700,
    fontFeatures: _tabular,
  );

  /// Small amounts (receipt lines, chart axes).
  static const amountSmall = TextStyle(
    fontSize: 14,
    height: 1.3,
    fontWeight: FontWeight.w500,
    fontFeatures: _tabular,
  );

  /// Mapped onto Material's TextTheme so standard widgets
  /// (AppBar, ListTile, buttons...) already use these styles.
  static TextTheme textTheme(AppColors c) {
    TextStyle p(TextStyle s) => s.copyWith(color: c.textPrimary);
    TextStyle s2(TextStyle s) => s.copyWith(color: c.textSecondary);
    return TextTheme(
      displayLarge: p(display),
      displayMedium: p(display),
      displaySmall: p(headlineLarge),
      headlineLarge: p(headlineLarge),
      headlineMedium: p(headline),
      headlineSmall: p(title),
      titleLarge: p(title),
      titleMedium: p(titleSmall),
      titleSmall: p(label),
      bodyLarge: p(body),
      bodyMedium: p(bodySmall),
      bodySmall: s2(caption),
      labelLarge: p(label),
      labelMedium: p(caption),
      labelSmall: s2(caption),
    );
  }
}

// ---------------------------------------------------------------------------
// ThemeData built from the tokens.
// ---------------------------------------------------------------------------

abstract final class AppTheme {
  static ThemeData get light => _build(AppColors.light, Brightness.light);
  static ThemeData get dark => _build(AppColors.dark, Brightness.dark);

  static ThemeData _build(AppColors c, Brightness brightness) {
    final scheme =
        ColorScheme.fromSeed(
          seedColor: AppPalette.teal700,
          brightness: brightness,
        ).copyWith(
          primary: c.brand,
          onPrimary: c.onBrand,
          primaryContainer: c.brandContainer,
          onPrimaryContainer: c.onBrandContainer,
          surface: c.surface,
          onSurface: c.textPrimary,
          onSurfaceVariant: c.textSecondary,
          outline: c.border,
          outlineVariant: c.divider,
          error: c.error,
        );

    return ThemeData(
      useMaterial3: true,
      brightness: brightness,
      colorScheme: scheme,
      scaffoldBackgroundColor: c.page,
      textTheme: AppTextStyles.textTheme(c),
      dividerColor: c.divider,
      extensions: [c],
    );
  }
}

// ---------------------------------------------------------------------------
// Shortcuts: context.colors.brand, context.text.titleLarge
// ---------------------------------------------------------------------------

extension DesignTokensContext on BuildContext {
  AppColors get colors => Theme.of(this).extension<AppColors>()!;
  TextTheme get text => Theme.of(this).textTheme;
}
