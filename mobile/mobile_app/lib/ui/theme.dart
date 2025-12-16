import 'package:flutter/material.dart';

class AppTheme {
  static const _maroon = Color(0xFF800000);
  static const _red = Color(0xFFB00020);
  static const _yellow = Color(0xFFFFC400);
  static const _black = Color(0xFF0B0B0B);

  static ThemeData light() {
    final scheme = ColorScheme(
      brightness: Brightness.light,
      primary: _maroon,
      onPrimary: Colors.white,
      primaryContainer: const Color(0xFFFFE5E5),
      onPrimaryContainer: _black,
      secondary: _yellow,
      onSecondary: _black,
      secondaryContainer: const Color(0xFFFFF2B3),
      onSecondaryContainer: _black,
      tertiary: _red,
      onTertiary: Colors.white,
      tertiaryContainer: const Color(0xFFFFD6D6),
      onTertiaryContainer: _black,
      error: const Color(0xFFB3261E),
      onError: Colors.white,
      errorContainer: const Color(0xFFF9DEDC),
      onErrorContainer: const Color(0xFF410E0B),
      surface: Colors.white,
      onSurface: _black,
      surfaceContainerHighest: const Color(0xFFF4F4F4),
      onSurfaceVariant: const Color(0xFF3A3A3A),
      outline: const Color(0xFFB5B5B5),
      shadow: Colors.black,
      inverseSurface: _black,
      onInverseSurface: Colors.white,
      inversePrimary: _yellow,
      surfaceTint: _maroon,
      scrim: Colors.black,
    );
    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      brightness: Brightness.light,
      visualDensity: VisualDensity.adaptivePlatformDensity,
      appBarTheme: AppBarTheme(
        centerTitle: false,
        backgroundColor: scheme.surface,
        foregroundColor: scheme.onSurface,
      ),
      cardTheme: CardThemeData(
        elevation: 0,
        color: scheme.surface,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: scheme.outline.withOpacity(0.25)),
        ),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: scheme.primary,
          foregroundColor: scheme.onPrimary,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(14)),
      ),
    );
  }

  static ThemeData dark() {
    final scheme = ColorScheme(
      brightness: Brightness.dark,
      primary: _yellow,
      onPrimary: _black,
      primaryContainer: const Color(0xFF3A2F00),
      onPrimaryContainer: Colors.white,
      secondary: _maroon,
      onSecondary: Colors.white,
      secondaryContainer: const Color(0xFF3A0B0B),
      onSecondaryContainer: Colors.white,
      tertiary: _red,
      onTertiary: Colors.white,
      tertiaryContainer: const Color(0xFF4A0E10),
      onTertiaryContainer: Colors.white,
      error: const Color(0xFFF2B8B5),
      onError: const Color(0xFF601410),
      errorContainer: const Color(0xFF8C1D18),
      onErrorContainer: const Color(0xFFF9DEDC),
      surface: _black,
      onSurface: Colors.white,
      surfaceContainerHighest: const Color(0xFF151515),
      onSurfaceVariant: const Color(0xFFCACACA),
      outline: const Color(0xFF5C5C5C),
      shadow: Colors.black,
      inverseSurface: Colors.white,
      onInverseSurface: _black,
      inversePrimary: _maroon,
      surfaceTint: _yellow,
      scrim: Colors.black,
    );
    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      brightness: Brightness.dark,
      visualDensity: VisualDensity.adaptivePlatformDensity,
      scaffoldBackgroundColor: scheme.surface,
      cardTheme: CardThemeData(
        elevation: 0,
        color: const Color(0xFF121212),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: scheme.outline.withOpacity(0.35)),
        ),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: scheme.primary,
          foregroundColor: scheme.onPrimary,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        ),
      ),
    );
  }
}
