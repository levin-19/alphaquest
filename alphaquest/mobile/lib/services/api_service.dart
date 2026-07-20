import 'dart:typed_data';
import 'package:dio/dio.dart';

class ApiService {
  // Hugging Face Space Direct URL (from the backend we just deployed!)
  static const String baseUrl = 'https://radwanhossan18-alphaquest-api.hf.space';
  
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
    )
  );

  Future<Map<String, dynamic>?> predictLetter(Uint8List imageBytes, String filename) async {
    try {
      // Create MultipartFile from bytes
      final multipartFile = MultipartFile.fromBytes(
        imageBytes,
        filename: filename,
      );

      final formData = FormData.fromMap({
        'file': multipartFile,
      });

      // Hit the /predict endpoint using the default model
      final response = await _dio.post(
        '/predict',
        data: formData,
      );

      if (response.statusCode == 200) {
        return response.data;
      }
      return {'error': 'Server returned ${response.statusCode}'};
    } catch (e) {
      print('API Error: $e');
      if (e is DioException) {
        if (e.response?.statusCode == 503) {
          return {'error': 'Server is offline (503). Check HuggingFace.'};
        }
        return {'error': 'Server error: ${e.response?.statusCode ?? e.message}'};
      }
      return {'error': 'Failed to connect to server.'};
    }
  }
}
