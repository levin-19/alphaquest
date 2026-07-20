import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../config/colors.dart';

class QuestyMascot extends StatelessWidget {
  final double size;
  final bool isHappy;
  final String? message;

  const QuestyMascot({
    super.key,
    this.size = 120,
    this.isHappy = true,
    this.message,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (message != null)
          Container(
            margin: const EdgeInsets.only(bottom: 16),
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(24),
              border: Border.all(color: AppColors.primary, width: 3),
              boxShadow: [
                BoxShadow(
                  color: AppColors.primary.withOpacity(0.3),
                  blurRadius: 8,
                  offset: const Offset(0, 4),
                )
              ],
            ),
            child: Text(
              message!,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: AppColors.textLight,
              ),
              textAlign: TextAlign.center,
            ),
          ).animate().scale(duration: 400.ms, curve: Curves.elasticOut),
          
        Stack(
          alignment: Alignment.center,
          children: [
            Container(
              width: size,
              height: size,
              decoration: BoxDecoration(
                color: AppColors.secondary,
                shape: BoxShape.circle,
                border: Border.all(color: AppColors.accent, width: 4),
                boxShadow: [
                  BoxShadow(
                    color: AppColors.accent.withOpacity(0.4),
                    blurRadius: 12,
                    offset: const Offset(0, 6),
                  )
                ],
              ),
            ),
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                _buildEye(isHappy),
                const SizedBox(width: 16),
                _buildEye(isHappy),
              ],
            ),
            Positioned(
              bottom: size * 0.25,
              child: Container(
                width: size * 0.15,
                height: size * 0.15,
                decoration: const BoxDecoration(
                  color: AppColors.accent,
                  shape: BoxShape.circle,
                ),
              ),
            ),
          ],
        ).animate(onPlay: (controller) => controller.repeat(reverse: true))
         .moveY(begin: -5, end: 5, duration: 1.seconds, curve: Curves.easeInOut),
      ],
    );
  }

  Widget _buildEye(bool isHappy) {
    return Container(
      width: size * 0.25,
      height: size * 0.25,
      decoration: const BoxDecoration(
        color: Colors.white,
        shape: BoxShape.circle,
      ),
      child: Center(
        child: Container(
          width: size * 0.1,
          height: isHappy ? size * 0.05 : size * 0.1,
          decoration: BoxDecoration(
            color: AppColors.textLight,
            borderRadius: BorderRadius.circular(size * 0.1),
          ),
        ),
      ),
    );
  }
}
