# AlphaQuest API — Example Requests & Responses

Base URL (local): `http://localhost:8080`  
Base URL (Render): `https://alphaquest-api.onrender.com`

---

## 1. Health Check

### cURL
```bash
curl -X GET "https://alphaquest-api.onrender.com/health"
```

### Response
```json
{"healthy": true}
```

---

## 2. Predict Image (Alphabet)

### cURL
```bash
curl -X POST "https://alphaquest-api.onrender.com/predict-image" \
  -H "Accept: application/json" \
  -F "file=@/path/to/letter_A.jpg"
```

### Postman
- Method: POST  
- URL: `https://alphaquest-api.onrender.com/predict-image`  
- Body: `form-data` → Key: `file` (File type) → Select image file

### Flutter (`http` package)
```dart
import 'dart:io';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>> predictImage(File imageFile) async {
  final uri = Uri.parse('https://alphaquest-api.onrender.com/predict-image');
  final request = http.MultipartRequest('POST', uri);
  request.files.add(await http.MultipartFile.fromPath('file', imageFile.path));
  final streamedResponse = await request.send();
  final response = await http.Response.fromStream(streamedResponse);
  return jsonDecode(response.body);
}
```

### Response
```json
{
  "prediction": "A",
  "confidence": 99.82
}
```

---

## 3. Predict Speech

### cURL
```bash
curl -X POST "https://alphaquest-api.onrender.com/predict-speech" \
  -H "Accept: application/json" \
  -F "file=@/path/to/recording.wav"
```

### Flutter
```dart
Future<Map<String, dynamic>> predictSpeech(File audioFile) async {
  final uri = Uri.parse('https://alphaquest-api.onrender.com/predict-speech');
  final request = http.MultipartRequest('POST', uri);
  request.files.add(await http.MultipartFile.fromPath('file', audioFile.path));
  final streamedResponse = await request.send();
  final response = await http.Response.fromStream(streamedResponse);
  return jsonDecode(response.body);
}
```

### Response
```json
{
  "prediction": "What is this alphabet?",
  "confidence": 98.5
}
```

---

## 4. Predict Both (Image + Audio)

### cURL
```bash
curl -X POST "https://alphaquest-api.onrender.com/predict-both" \
  -F "image=@/path/to/letter_A.jpg" \
  -F "audio=@/path/to/recording.wav"
```

### Flutter
```dart
Future<Map<String, dynamic>> predictBoth(File imageFile, File audioFile) async {
  final uri = Uri.parse('https://alphaquest-api.onrender.com/predict-both');
  final request = http.MultipartRequest('POST', uri);
  request.files.add(await http.MultipartFile.fromPath('image', imageFile.path));
  request.files.add(await http.MultipartFile.fromPath('audio', audioFile.path));
  final streamedResponse = await request.send();
  final response = await http.Response.fromStream(streamedResponse);
  return jsonDecode(response.body);
}
```

### Response
```json
{
  "alphabet": "A",
  "speech": "A",
  "match": true,
  "confidence": 99.1
}
```

---

## 5. Error Responses

### Unsupported file type (400)
```json
{"error": "Unsupported image type '.bmp'. Allowed: .jpeg, .jpg, .png, .webp."}
```

### File too large (400)
```json
{"error": "The image exceeds the 20 MB upload limit."}
```

### Model not loaded (503)
```json
{"detail": "Alphabet model is not available."}
```

### Endpoint not found (404)
```json
{"error": "Endpoint '/wrong-path' not found."}
```
