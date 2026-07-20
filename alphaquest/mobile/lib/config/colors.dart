import 'package:flutter/material.dart';

class AppColors {
  // Kids Edition Palette
  static const Color primary = Color(0xFF38BDF8); // Sky Blue
  static const Color secondary = Color(0xFFFDE047); // Sunny Yellow
  static const Color accent = Color(0xFFFB923C); // Orange
  
  // Feedback
  static const Color success = Color(0xFF4ADE80); // Green
  static const Color error = Color(0xFFF87171); // Soft Red
  
  // Backgrounds
  static const Color backgroundLight = Color(0xFFF0F9FF); // Very Light Blue
  static const Color backgroundDark = Color(0xFF0F172A);
  
  // Cards & Buttons
  static const Color surfaceLight = Colors.white;
  static const Color textLight = Color(0xFF334155); // Slate
  
  // Gradients for Buttons
  static const LinearGradient primaryGradient = LinearGradient(
    colors: [Color(0xFF7DD3FC), Color(0xFF0EA5E9)],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );
  
  static const LinearGradient accentGradient = LinearGradient(
    colors: [Color(0xFFFDBA74), Color(0xFFF97316)],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );
  
  static const LinearGradient successGradient = LinearGradient(
    colors: [Color(0xFF86EFAC), Color(0xFF22C55E)],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );
}
