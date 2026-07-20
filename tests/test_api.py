"""
tests/test_api.py — Pytest test suite for AlphaQuest API.

Tests cover:
  - Health endpoint
  - Version endpoint
  - Root endpoint
  - 404 handling
  - Missing file (422 validation error)
  - Unsupported image format (400)
  - Unsupported audio format (400)
"""
import io
import pytest
from fastapi.testclient import TestClient

from app import app
from config import settings

client = TestClient(app)


# ---------------------------------------------------------------------------
# Basic GET endpoints
# ---------------------------------------------------------------------------

class TestRootEndpoints:
    def test_root_returns_service_name(self):
        res = client.get("/")
        assert res.status_code == 200
        body = res.json()
        assert body["service"] == settings.PROJECT_NAME
        assert body["status"] == "running"

    def test_health_returns_true(self):
        res = client.get("/health")
        assert res.status_code == 200
        assert res.json() == {"healthy": True}

    def test_version_returns_string(self):
        res = client.get("/version")
        assert res.status_code == 200
        assert res.json()["version"] == settings.API_VERSION

    def test_unknown_route_returns_json_404(self):
        res = client.get("/does-not-exist")
        assert res.status_code == 404
        body = res.json()
        assert "error" in body


# ---------------------------------------------------------------------------
# POST /predict-image validation
# ---------------------------------------------------------------------------

class TestPredictImage:
    def test_missing_file_returns_422(self):
        """FastAPI raises 422 Unprocessable Entity when required field is absent."""
        res = client.post("/predict-image")
        assert res.status_code == 422

    def test_unsupported_extension_returns_400(self):
        fake_file = io.BytesIO(b"fake content")
        res = client.post(
            "/predict-image",
            files={"file": ("malware.exe", fake_file, "application/octet-stream")},
        )
        assert res.status_code == 400
        assert "error" in res.json()

    def test_txt_file_rejected(self):
        fake_file = io.BytesIO(b"this is text")
        res = client.post(
            "/predict-image",
            files={"file": ("readme.txt", fake_file, "text/plain")},
        )
        assert res.status_code == 400
        assert "error" in res.json()

    def test_pdf_rejected(self):
        fake_file = io.BytesIO(b"%PDF-content")
        res = client.post(
            "/predict-image",
            files={"file": ("document.pdf", fake_file, "application/pdf")},
        )
        assert res.status_code == 400
        assert "error" in res.json()


# ---------------------------------------------------------------------------
# POST /predict-speech validation
# ---------------------------------------------------------------------------

class TestPredictSpeech:
    def test_missing_file_returns_422(self):
        res = client.post("/predict-speech")
        assert res.status_code == 422

    def test_unsupported_extension_returns_400(self):
        fake_file = io.BytesIO(b"fake audio")
        res = client.post(
            "/predict-speech",
            files={"file": ("audio.ogg", fake_file, "audio/ogg")},
        )
        assert res.status_code == 400
        assert "error" in res.json()

    def test_image_file_rejected_for_speech(self):
        fake_file = io.BytesIO(b"\xff\xd8\xff\xe0")  # JPEG magic bytes
        res = client.post(
            "/predict-speech",
            files={"file": ("photo.jpg", fake_file, "image/jpeg")},
        )
        assert res.status_code == 400
        assert "error" in res.json()


# ---------------------------------------------------------------------------
# POST /predict-both validation
# ---------------------------------------------------------------------------

class TestPredictBoth:
    def test_missing_both_files_returns_422(self):
        res = client.post("/predict-both")
        assert res.status_code == 422

    def test_invalid_image_type_returns_400(self):
        bad_img = io.BytesIO(b"not an image")
        good_audio = io.BytesIO(b"RIFF....WAVEfmt ")
        res = client.post(
            "/predict-both",
            files={
                "image": ("file.bmp", bad_img, "image/bmp"),
                "audio": ("clip.wav", good_audio, "audio/wav"),
            },
        )
        assert res.status_code == 400
        assert "error" in res.json()
