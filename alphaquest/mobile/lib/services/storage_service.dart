import 'package:shared_preferences/shared_preferences.dart';

class StorageService {
  static const String _starsKey = 'user_stars';
  static const String _progressKey = 'daily_progress';

  Future<int> getStars() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getInt(_starsKey) ?? 0;
  }

  Future<void> addStars(int amount) async {
    final prefs = await SharedPreferences.getInstance();
    final current = await getStars();
    await prefs.setInt(_starsKey, current + amount);
  }

  Future<int> getDailyProgress() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getInt(_progressKey) ?? 0;
  }

  Future<void> updateDailyProgress(int progress) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(_progressKey, progress);
  }
}
