import 'package:flutter/foundation.dart';
import '../services/storage_service.dart';

class UserProvider extends ChangeNotifier {
  final StorageService _storageService = StorageService();
  
  int _stars = 0;
  int _dailyProgress = 0;
  final int dailyGoal = 5;

  int get stars => _stars;
  int get dailyProgress => _dailyProgress;

  Future<void> loadUserData() async {
    _stars = await _storageService.getStars();
    _dailyProgress = await _storageService.getDailyProgress();
    notifyListeners();
  }

  Future<void> addStars(int amount) async {
    _stars += amount;
    await _storageService.addStars(amount);
    
    if (_dailyProgress < dailyGoal) {
      _dailyProgress++;
      await _storageService.updateDailyProgress(_dailyProgress);
    }
    
    notifyListeners();
  }
}
