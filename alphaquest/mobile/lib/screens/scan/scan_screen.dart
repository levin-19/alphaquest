import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:image_picker/image_picker.dart';
import 'package:confetti/confetti.dart';
import 'package:provider/provider.dart';
import '../../config/colors.dart';
import '../../providers/user_provider.dart';
import '../../widgets/questy_mascot.dart';
import '../../services/api_service.dart';
import '../../widgets/custom_appbar.dart';

class ScanScreen extends StatefulWidget {
  final ImageSource source;
  
  const ScanScreen({super.key, required this.source});

  @override
  State<ScanScreen> createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> {
  final ApiService _apiService = ApiService();
  final ImagePicker _picker = ImagePicker();
  late ConfettiController _confettiController;
  
  bool _isLoading = false;
  Uint8List? _imageBytes;
  String? _prediction;
  double? _confidence;
  String? _errorMessage;
  
  @override
  void initState() {
    super.initState();
    _confettiController = ConfettiController(duration: const Duration(seconds: 3));
    // Immediately open camera/gallery when screen loads
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _pickImage();
    });
  }
  
  @override
  void dispose() {
    _confettiController.dispose();
    super.dispose();
  }

  Future<void> _pickImage() async {
    try {
      final XFile? image = await _picker.pickImage(
        source: widget.source,
        maxWidth: 800,
        maxHeight: 800,
      );
      
      if (image != null) {
        final bytes = await image.readAsBytes();
        setState(() {
          _imageBytes = bytes;
          _isLoading = true;
          _prediction = null;
        });
        
        // Add a slight delay for UX so kids see Questy "thinking"
        await Future.delayed(const Duration(seconds: 1));
        
        final result = await _apiService.predictLetter(bytes, image.name);
        
        setState(() {
          _isLoading = false;
          if (result != null) {
            if (result.containsKey('error')) {
              _prediction = "Error";
              _errorMessage = result['error'];
            } else {
              _prediction = result['prediction'];
              _confidence = (result['confidence'] as num).toDouble();
              
              if (_confidence! > 50) {
                _confettiController.play();
                // Award stars if we have a match
                if (mounted) {
                  context.read<UserProvider>().addStars(20);
                }
              }
            }
          } else {
            _prediction = "Error";
            _errorMessage = "Oops! I couldn't see it clearly.";
          }
        });
      } else {
        // User cancelled, go back
        if (mounted) Navigator.pop(context);
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
        _prediction = "Error";
        _errorMessage = "Something went wrong.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(title: 'Letter Scanner', showBackButton: true),
      body: Stack(
        alignment: Alignment.topCenter,
        children: [
          if (_imageBytes == null && !_isLoading)
            const Center(child: CircularProgressIndicator(color: AppColors.primary)),
            
          if (_imageBytes != null)
            SingleChildScrollView(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  // Image Preview
                  Container(
                    height: 250,
                    width: double.infinity,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(32),
                      border: Border.all(color: AppColors.primary, width: 4),
                      boxShadow: [
                        BoxShadow(
                          color: AppColors.primary.withOpacity(0.3),
                          blurRadius: 16,
                          offset: const Offset(0, 8),
                        )
                      ],
                    ),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(28),
                      child: Image.memory(
                        _imageBytes!,
                        fit: BoxFit.cover,
                      ),
                    ),
                  ).animate().scale(),
                  
                  const SizedBox(height: 48),
                  
                  // Loading State
                  if (_isLoading) ...[
                    const QuestyMascot(
                      size: 100, 
                      message: "Hmm... Let me think!",
                    ).animate().fadeIn(),
                    const SizedBox(height: 32),
                    const CircularProgressIndicator(
                      valueColor: AlwaysStoppedAnimation<Color>(AppColors.accent),
                      strokeWidth: 8,
                    ),
                  ],
                  
                  // Result State
                  if (!_isLoading && _prediction != null) ...[
                    if (_prediction == "Error")
                      QuestyMascot(
                        size: 100, 
                        isHappy: false,
                        message: _errorMessage ?? "Oops! I couldn't see it clearly.",
                      ).animate().shake()
                    else ...[
                      QuestyMascot(
                        size: 100, 
                        isHappy: _confidence! > 50,
                        message: _confidence! > 50 ? "You did it! Awesome!" : "Good try! Try again!",
                      ).animate().scale(delay: 200.ms, curve: Curves.elasticOut),
                      
                      const SizedBox(height: 32),
                      
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 48, vertical: 24),
                        decoration: BoxDecoration(
                          color: _confidence! > 50 ? AppColors.success : AppColors.accent,
                          borderRadius: BorderRadius.circular(40),
                          boxShadow: [
                            BoxShadow(
                              color: (_confidence! > 50 ? AppColors.success : AppColors.accent).withOpacity(0.4),
                              blurRadius: 20,
                              offset: const Offset(0, 10),
                            )
                          ]
                        ),
                        child: Column(
                          children: [
                            Text(
                              _prediction!,
                              style: const TextStyle(
                                fontSize: 80,
                                fontWeight: FontWeight.w900,
                                color: Colors.white,
                                height: 1.0,
                              ),
                            ).animate().scale(delay: 400.ms),
                            Text(
                              '${_confidence!.toStringAsFixed(0)}% Match',
                              style: const TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: Colors.white70,
                              ),
                            ),
                          ],
                        ),
                      ).animate().fadeIn(delay: 200.ms).slideY(begin: 0.5),
                    ],
                    
                    const SizedBox(height: 48),
                    
                    SizedBox(
                      width: double.infinity,
                      height: 64,
                      child: ElevatedButton(
                        onPressed: () => Navigator.pop(context),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.primary,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(32)),
                        ),
                        child: const Text('Play Again!', style: TextStyle(fontSize: 24)),
                      ),
                    ).animate().fadeIn(delay: 800.ms),
                  ],
                ],
              ),
            ),
            
          // Confetti!
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
}
