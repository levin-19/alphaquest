import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../config/colors.dart';
import '../../routes/app_routes.dart';
import '../../widgets/questy_mascot.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _navigateToNext();
  }

  void _navigateToNext() async {
    await Future.delayed(const Duration(seconds: 4));
    if (mounted) {
      Navigator.pushReplacementNamed(context, AppRoutes.onboarding);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.primary,
      body: Stack(
        children: [
          // Clouds background
          Positioned(
            top: 100,
            left: 20,
            child: const Icon(Icons.cloud_rounded, color: Colors.white70, size: 80)
                .animate(onPlay: (controller) => controller.repeat(reverse: true))
                .moveX(begin: -10, end: 10, duration: 3.seconds),
          ),
          Positioned(
            top: 250,
            right: -20,
            child: const Icon(Icons.cloud_rounded, color: Colors.white70, size: 120)
                .animate(onPlay: (controller) => controller.repeat(reverse: true))
                .moveX(begin: 10, end: -10, duration: 4.seconds),
          ),
          
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const QuestyMascot(
                  size: 150,
                  message: 'Welcome to AlphaQuest!',
                ).animate().scale(duration: 800.ms, curve: Curves.elasticOut),
                
                const SizedBox(height: 48),
                
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(40),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.1),
                        blurRadius: 10,
                        offset: const Offset(0, 5),
                      )
                    ],
                  ),
                  child: const Text(
                    'Learn • Capture • Recognize',
                    style: TextStyle(
                      color: AppColors.primary,
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ).animate().slideY(begin: 1, end: 0, duration: 600.ms, curve: Curves.easeOutBack),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
