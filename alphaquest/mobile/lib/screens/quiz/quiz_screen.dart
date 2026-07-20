import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:provider/provider.dart';
import 'package:confetti/confetti.dart';
import '../../config/colors.dart';
import '../../providers/user_provider.dart';
import '../../widgets/questy_mascot.dart';
import '../../widgets/custom_appbar.dart';

class QuizScreen extends StatefulWidget {
  const QuizScreen({super.key});

  @override
  State<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  late ConfettiController _confettiController;
  
  final List<String> _letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'];
  late String _targetLetter;
  late List<String> _options;
  
  bool _answered = false;
  bool _isCorrect = false;
  
  @override
  void initState() {
    super.initState();
    _confettiController = ConfettiController(duration: const Duration(seconds: 2));
    _generateQuiz();
  }
  
  void _generateQuiz() {
    final random = Random();
    _targetLetter = _letters[random.nextInt(_letters.length)];
    
    _options = [_targetLetter];
    while (_options.length < 4) {
      final randomLetter = _letters[random.nextInt(_letters.length)];
      if (!_options.contains(randomLetter)) {
        _options.add(randomLetter);
      }
    }
    _options.shuffle();
    
    setState(() {
      _answered = false;
      _isCorrect = false;
    });
  }

  void _checkAnswer(String selected) {
    if (_answered) return; 
    
    setState(() {
      _answered = true;
      _isCorrect = (selected == _targetLetter);
    });
    
    if (_isCorrect) {
      _confettiController.play();
      context.read<UserProvider>().addStars(10);
    }
  }

  @override
  void dispose() {
    _confettiController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(title: 'Quiz Time!', showBackButton: true),
      body: Stack(
        alignment: Alignment.topCenter,
        children: [
          Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              children: [
                QuestyMascot(
                  size: 100,
                  isHappy: _answered ? _isCorrect : true,
                  message: _answered 
                      ? (_isCorrect ? "Correct! +10 Stars ⭐" : "Oops! The correct answer was $_targetLetter.")
                      : "Find the letter: $_targetLetter",
                ).animate().scale(),
                
                const SizedBox(height: 48),
                
                Expanded(
                  child: GridView.count(
                    crossAxisCount: 2,
                    mainAxisSpacing: 24,
                    crossAxisSpacing: 24,
                    children: _options.map((letter) => _buildOptionCard(letter)).toList(),
                  ),
                ),
                
                if (_answered)
                  SizedBox(
                    width: double.infinity,
                    height: 64,
                    child: ElevatedButton(
                      onPressed: _generateQuiz,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primary,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(32)),
                      ),
                      child: const Text('Next Question', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                    ),
                  ).animate().fadeIn(delay: 600.ms),
              ],
            ),
          ),
          
          Align(
            alignment: Alignment.topCenter,
            child: ConfettiWidget(
              confettiController: _confettiController,
              blastDirectionality: BlastDirectionality.explosive,
              shouldLoop: false,
              colors: const [AppColors.primary, AppColors.secondary, AppColors.accent, AppColors.success],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildOptionCard(String letter) {
    Color cardColor = Colors.white;
    if (_answered) {
      if (letter == _targetLetter) {
        cardColor = AppColors.success;
      } else if (!_isCorrect && letter != _targetLetter) {
        cardColor = AppColors.error;
      }
    }
    
    return GestureDetector(
      onTap: () => _checkAnswer(letter),
      child: Container(
        decoration: BoxDecoration(
          color: cardColor,
          borderRadius: BorderRadius.circular(32),
          border: Border.all(color: AppColors.primary.withOpacity(0.3), width: 4),
          boxShadow: [
            BoxShadow(
              color: AppColors.primary.withOpacity(0.2),
              blurRadius: 16,
              offset: const Offset(0, 8),
            )
          ],
        ),
        child: Center(
          child: Text(
            letter,
            style: TextStyle(
              fontSize: 64,
              fontWeight: FontWeight.w900,
              color: _answered && letter == _targetLetter ? Colors.white : AppColors.textLight,
            ),
          ),
        ),
      ),
    ).animate().scale();
  }
}
