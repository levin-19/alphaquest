# AlphaQuest API

**Production-ready FastAPI backend** for the AlphaQuest AI-powered educational app for children. Deployed on **Render** with zero configuration after model placement.

---

## Features

| Feature | Details |
|---|---|
| Framework | FastAPI (async, Swagger, ReDoc) |
| AI Runtime | TensorFlow 2.15 |
| Image Processing | Pillow + OpenCV |
| Audio Processing | Librosa + SoundFile (MFCC) |
| Deployment | Render (free tier compatible) |
| Security | File validation, size limits, security headers |
| Architecture | Singleton model loader, decoupled utils, Pydantic schemas |

---

## Project Structure

```text
alphaquest-api/
├── app.py                  ← FastAPI app + middleware + global handlers
├── config.py               ← All constants and paths (no hardcoded values)
├── startup.py              ← Local Uvicorn entry point
├── requirements.txt        ← Pinned dependencies
├── render.yaml             ← Render Blueprint (1-click deploy)
├── runtime.txt             ← Render Python version
├── .gitignore
├── api/
│   └── routes.py           ← GET /, /health, /version | POST /predict-*
├── core/
│   ├── logger.py           ← Centralized logging
│   ├── model_loader.py     ← Singleton TF model + label manager
│   └── security.py         ← File validation, sanitization, headers
├── utils/
│   ├── image_utils.py      ← Load, RGB, resize, normalize, expand dims
│   ├── audio_utils.py      ← Load, mono, MFCC, pad, reshape
│   ├── preprocessing.py    ← Pipeline wrappers
│   └── validators.py       ← Extension + size validation
├── schemas/
│   └── response_models.py  ← Pydantic response types
├── labels/
│   ├── alphabet_labels.json
│   └── speech_labels.json
├── models/                 ← ⚠️ Place your .h5 files here
├── tests/
│   └── test_api.py
└── docs/
    └── api_examples.md
```

---

## Local Installation

```bash
cd alphaquest-api
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Place your models:
```
models/alphabet_model.h5
models/speech_model.h5
```

Run locally:
```bash
python startup.py
# or
uvicorn app:app --reload --port 8080
```

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

---

## Run Tests

```bash
pytest tests/ -v
```

---

## Render Deployment (5 Steps)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USER/alphaquest-api.git
   git push -u origin main
   ```

2. **Create Render Account** at [render.com](https://render.com)

3. **New → Blueprint** → Select your GitHub repository.  
   Render reads `render.yaml` automatically.

4. **Click Apply** — Render installs dependencies and starts the server.

5. **Live URL**: `https://alphaquest-api.onrender.com`
   Verify: visit `/docs` to see the Swagger UI.

### Updating the backend
```bash
git add .
git commit -m "Update"
git push
```
Render auto-deploys on every push (autoDeploy: true in render.yaml).

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Service name and status |
| GET | `/health` | Uptime check (used by Render) |
| GET | `/version` | API version |
| POST | `/predict-image` | Predict alphabet from image |
| POST | `/predict-speech` | Predict label from audio |
| POST | `/predict-both` | Run both models and compare |

---

## Flutter Integration

Update your Flutter `api_service.dart`:
```dart
static const String baseUrl = 'https://alphaquest-api.onrender.com';
```

See `docs/api_examples.md` for complete Flutter `http` package examples.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| 503 on predict endpoints | Your `.h5` model file is missing from `models/`. Check Render build logs. |
| Out of Memory crash | Upgrade Render to Starter ($7/mo) for more than 512MB RAM. |
| Audio 400 error | Only `.wav` and `.mp3` are accepted. |
| Image 400 error | Only `.png`, `.jpg`, `.jpeg`, `.webp` are accepted. |
| Cold start delay | Free Render tier spins down after 15 min of inactivity. First request takes ~30s. |

---

## Security

- File extensions strictly validated before reading bytes.
- File size capped at 20 MB.
- Filenames sanitized (path traversal prevented).
- Security headers (`X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`) injected on every response.
- No internal stack traces exposed to clients.
