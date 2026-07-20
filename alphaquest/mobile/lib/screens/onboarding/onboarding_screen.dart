import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../config/colors.dart';
import '../../routes/app_routes.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final PageController _pageController = PageController();
  int _currentPage = 0;

  final List<Map<String, dynamic>> _onboardingData = [
    {
      'title': 'Learn the ABCs!',
      'description': 'Join Questy on a magical adventure to learn all the English letters.',
      'color': AppColors.primary,
      'icon': Icons.school_rounded,
    },
    {
      'title': 'Draw & Capture',
      'description': 'Write a letter on paper, take a picture, and let Questy guess it!',
      'color': AppColors.accent,
      'icon': Icons.camera_alt_rounded,
    },
    {
      'title': 'Earn Stars!',
      'description': 'Collect shiny stars, unlock badges, and become an Alphabet Master!',
      'color': AppColors.secondary,
      'icon': Icons.star_rounded,
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundLight,
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: PageView.builder(
                controller: _pageController,
                onPageChanged: (index) => setState(() => _currentPage = index),
                itemCount: _onboardingData.length,
                itemBuilder: (context, index) {
                  return Padding(
                    padding: const EdgeInsets.all(32.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          width: 200,
                          height: 200,
                          decoration: BoxDecoration(
                            color: _onboardingData[index]['color'].withOpacity(0.2),
                            shape: BoxShape.circle,
                          ),
                          child: Center(
                            child: Icon(
                              _onboardingData[index]['icon'],
                              size: 100,
                              color: _onboardingData[index]['color'],
                            ),
                          ),
                        ).animate().scale(duration: 600.ms, curve: Curves.elasticOut),
                        
                        const SizedBox(height: 48),
                        
                        Text(
                          _onboardingData[index]['title'],
                          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                            fontWeight: FontWeight.w900,
                            color: _onboardingData[index]['color'],
                            fontSize: 32,
                          ),
                          textAlign: TextAlign.center,
                        ).animate().fadeIn(delay: 200.ms).slideY(begin: 0.2),
                        
                        const SizedBox(height: 16),
                        
                        Text(
                          _onboardingData[index]['description'],
                          style: const TextStyle(
                            fontSize: 20,
                            color: AppColors.textLight,
                            fontWeight: FontWeight.w600,
                          ),
                          textAlign: TextAlign.center,
                        ).animate().fadeIn(delay: 400.ms),
                      ],
                    ),
                  );
                },
              ),
            ),
            
            // Bottom Controls
            Padding(
              padding: const EdgeInsets.all(32.0),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: List.generate(
                      _onboardingData.length,
                      (index) => AnimatedContainer(
                        duration: const Duration(milliseconds: 300),
                        margin: const EdgeInsets.symmetric(horizontal: 6),
                        height: 12,
                        width: _currentPage == index ? 32 : 12,
                        decoration: BoxDecoration(
                          color: _currentPage == index
                              ? _onboardingData[_currentPage]['color']
                              : Colors.grey.shade300,
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 32),
                  SizedBox(
                    width: double.infinity,
                    height: 64,
                    child: ElevatedButton(
                      onPressed: () {
                        if (_currentPage < _onboardingData.length - 1) {
                          _pageController.nextPage(
                            duration: const Duration(milliseconds: 400),
                            curve: Curves.easeInOut,
                          );
                        } else {
                          // No login screen for kids app, go straight to home!
                          Navigator.pushReplacementNamed(context, AppRoutes.home);
                        }
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: _onboardingData[_currentPage]['color'],
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(32),
                        ),
                      ),
                      child: Text(
                        _currentPage == _onboardingData.length - 1 ? "Let's Play!" : "Next",
                        style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ).animate().scale(duration: 400.ms),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
