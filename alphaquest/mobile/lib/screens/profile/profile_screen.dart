import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:provider/provider.dart';
import '../../config/colors.dart';
import '../../providers/user_provider.dart';
import '../../widgets/custom_appbar.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final userProvider = context.watch<UserProvider>();
    
    return Scaffold(
      appBar: const CustomAppBar(title: 'My Profile'),
      body: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(24, 24, 24, 120),
        child: Column(
          children: [
            // Avatar
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: AppColors.primary.withOpacity(0.2),
                shape: BoxShape.circle,
              ),
              child: const CircleAvatar(
                radius: 60,
                backgroundColor: AppColors.primary,
                child: Icon(Icons.face_rounded, size: 80, color: Colors.white),
              ),
            ).animate().scale(duration: 400.ms, curve: Curves.easeOutBack),
            
            const SizedBox(height: 16),
            
            const Text(
              'Super Learner',
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.w900,
                color: AppColors.textLight,
              ),
            ).animate().fadeIn(delay: 200.ms),
            
            const SizedBox(height: 32),
            
            // Stats Row
            Row(
              children: [
                Expanded(
                  child: _buildStatCard(
                    'Stars', 
                    userProvider.stars.toString(), 
                    Icons.star_rounded, 
                    AppColors.secondary
                  ).animate().fadeIn(delay: 300.ms).slideY(begin: 0.2),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: _buildStatCard(
                    'Level', 
                    (userProvider.stars ~/ 50 + 1).toString(), 
                    Icons.military_tech_rounded, 
                    AppColors.accent
                  ).animate().fadeIn(delay: 400.ms).slideY(begin: 0.2),
                ),
              ],
            ),
            
            const SizedBox(height: 32),
            
            // Badges Section
            Align(
              alignment: Alignment.centerLeft,
              child: const Text(
                'My Badges',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.w900,
                  color: AppColors.textLight,
                ),
              ).animate().fadeIn(delay: 500.ms),
            ),
            
            const SizedBox(height: 16),
            
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(32),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.05),
                    blurRadius: 20,
                    offset: const Offset(0, 10),
                  )
                ],
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _buildBadge(Icons.local_fire_department_rounded, 'Streak', true, AppColors.accent),
                  _buildBadge(Icons.school_rounded, 'Scholar', userProvider.stars >= 50, AppColors.primary),
                  _buildBadge(Icons.diamond_rounded, 'Master', userProvider.stars >= 200, AppColors.secondary),
                ],
              ),
            ).animate().fadeIn(delay: 600.ms).slideY(begin: 0.2),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: color.withOpacity(0.15),
        borderRadius: BorderRadius.circular(32),
        border: Border.all(color: color, width: 2),
      ),
      child: Column(
        children: [
          Icon(icon, size: 48, color: color),
          const SizedBox(height: 8),
          Text(
            value,
            style: TextStyle(
              fontSize: 32,
              fontWeight: FontWeight.w900,
              color: color,
            ),
          ),
          Text(
            title,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: AppColors.textLight,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBadge(IconData icon, String title, bool isUnlocked, Color color) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: isUnlocked ? color.withOpacity(0.2) : Colors.grey.shade200,
            shape: BoxShape.circle,
            border: Border.all(
              color: isUnlocked ? color : Colors.grey.shade400,
              width: 3,
            ),
          ),
          child: Icon(
            icon,
            size: 36,
            color: isUnlocked ? color : Colors.grey.shade400,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          title,
          style: TextStyle(
            fontWeight: FontWeight.bold,
            color: isUnlocked ? AppColors.textLight : Colors.grey.shade500,
          ),
        ),
      ],
    );
  }
}
