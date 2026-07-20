"""
api/routes.py — All API route definitions for AlphaQuest.

Endpoints:
    GET  /                 — service info
    GET  /health           — health check
    GET  /version          — API version
    POST /predict-image    — alphabet prediction from image
    POST /predict-speech   — label prediction from audio
    POST /predict-both     — combined prediction from image + audio
"""
import time
from typing import Annotated

import numpy as np
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from config import settings
from core.logger import get_logger
from core.model_loader import model_manager
from core.security import sanitize_filename
from schemas.response_models import (
    CombinedPredictionResponse,
    HealthResponse,
    PredictionResponse,
    RootResponse,
    VersionResponse,
)
from utils.preprocessing import run_audio_pipeline, run_image_pipeline
from utils.validators import validate_audio_file, validate_image_file

logger = get_logger("Routes")

router = APIRouter()


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _run_model(model, input_array: np.ndarray) -> tuple[int, float]:
    """
    Run TensorFlow inference and return (class_index, confidence_percent).

    Args:
        model:       Loaded Keras model.
        input_array: Preprocessed NumPy array.

    Returns:
        Tuple of (predicted_class_index, confidence_percentage).
    """
    preds = model.predict(input_array, verbose=0)
    idx = int(np.argmax(preds, axis=1)[0])
    conf = float(np.max(preds, axis=1)[0]) * 100.0
    return idx, conf


# ---------------------------------------------------------------------------
# Simple GET endpoints
# ---------------------------------------------------------------------------

@router.get("/", response_model=RootResponse, tags=["General"])
async def root() -> RootResponse:
    """Return the service name and running status."""
    return RootResponse(service=settings.PROJECT_NAME, status="running")


@router.get("/health", response_model=HealthResponse, tags=["General"])
async def health() -> HealthResponse:
    """Lightweight health check for Render uptime monitoring."""
    return HealthResponse(healthy=True)


@router.get("/version", response_model=VersionResponse, tags=["General"])
async def version() -> VersionResponse:
    """Return the current API version string."""
    return VersionResponse(version=settings.API_VERSION)


# ---------------------------------------------------------------------------
# POST /predict-image
# ---------------------------------------------------------------------------

@router.post(
    "/predict-image",
    response_model=PredictionResponse,
    responses={400: {"model": None}, 503: {"model": None}},
    tags=["Prediction"],
)
async def predict_image(
    file: Annotated[UploadFile, File(description="PNG, JPG, JPEG, or WEBP image file.")]
) -> PredictionResponse:
    """
    Accept an image upload and return the predicted alphabet letter.

    **Pipeline:** Upload → Validate → Resize → Normalize → Tensor → Model → Confidence → JSON
    """
    model = model_manager.get_alphabet_model()
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Alphabet model is not available.",
        )

    filename = sanitize_filename(file.filename or "upload")
    content = await file.read()

    try:
        validate_image_file(filename, content)
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})

    try:
        t0 = time.perf_counter()
        img_array = run_image_pipeline(content)
        idx, conf = _run_model(model, img_array)
        elapsed = (time.perf_counter() - t0) * 1000
        label = model_manager.get_label("alphabet", idx)
        logger.info(f"Image prediction: '{label}' ({conf:.1f}%) in {elapsed:.1f}ms")
        return PredictionResponse(prediction=label, confidence=round(conf, 2))
    except ValueError as exc:
        logger.warning(f"Image preprocessing error: {exc}")
        return JSONResponse(status_code=400, content={"error": str(exc)})
    except Exception as exc:
        logger.error(f"Unexpected error in predict_image: {exc}")
        return JSONResponse(
            status_code=500, content={"error": "Image prediction failed."}
        )


# ---------------------------------------------------------------------------
# POST /predict-speech
# ---------------------------------------------------------------------------

@router.post(
    "/predict-speech",
    response_model=PredictionResponse,
    responses={400: {"model": None}, 503: {"model": None}},
    tags=["Prediction"],
)
async def predict_speech(
    file: Annotated[UploadFile, File(description="WAV or MP3 audio file.")]
) -> PredictionResponse:
    """
    Accept an audio upload and return the predicted speech label.

    **Pipeline:** Upload → Validate → MFCC → Normalize → Tensor → Model → Confidence → JSON
    """
    model = model_manager.get_speech_model()
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Speech model is not available.",
        )

    filename = sanitize_filename(file.filename or "upload")
    content = await file.read()

    try:
        validate_audio_file(filename, content)
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})

    try:
        t0 = time.perf_counter()
        audio_array = run_audio_pipeline(content)
        idx, conf = _run_model(model, audio_array)
        elapsed = (time.perf_counter() - t0) * 1000
        label = model_manager.get_label("speech", idx)
        logger.info(f"Speech prediction: '{label}' ({conf:.1f}%) in {elapsed:.1f}ms")
        return PredictionResponse(prediction=label, confidence=round(conf, 2))
    except ValueError as exc:
        logger.warning(f"Audio preprocessing error: {exc}")
        return JSONResponse(status_code=400, content={"error": str(exc)})
    except Exception as exc:
        logger.error(f"Unexpected error in predict_speech: {exc}")
        return JSONResponse(
            status_code=500, content={"error": "Speech prediction failed."}
        )


# ---------------------------------------------------------------------------
# POST /predict-both
# ---------------------------------------------------------------------------

@router.post(
    "/predict-both",
    response_model=CombinedPredictionResponse,
    responses={400: {"model": None}, 503: {"model": None}},
    tags=["Prediction"],
)
async def predict_both(
    image: Annotated[UploadFile, File(description="PNG, JPG, JPEG, or WEBP image.")],
    audio: Annotated[UploadFile, File(description="WAV or MP3 audio file.")],
) -> CombinedPredictionResponse:
    """
    Accept an image and an audio file simultaneously.
    Runs both models and indicates whether their predictions match.

    **Pipeline:** Upload Both → Validate → Preprocess → Run Both Models → Compare → JSON
    """
    img_model = model_manager.get_alphabet_model()
    aud_model = model_manager.get_speech_model()

    if img_model is None or aud_model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="One or more models are not available.",
        )

    img_filename = sanitize_filename(image.filename or "image")
    aud_filename = sanitize_filename(audio.filename or "audio")

    img_content = await image.read()
    aud_content = await audio.read()

    try:
        validate_image_file(img_filename, img_content)
        validate_audio_file(aud_filename, aud_content)
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})

    try:
        img_array = run_image_pipeline(img_content)
        aud_array = run_audio_pipeline(aud_content)

        img_idx, img_conf = _run_model(img_model, img_array)
        aud_idx, aud_conf = _run_model(aud_model, aud_array)

        img_label = model_manager.get_label("alphabet", img_idx)
        aud_label = model_manager.get_label("speech", aud_idx)

        avg_conf = round((img_conf + aud_conf) / 2.0, 2)
        match = img_label.upper() == aud_label.upper()

        logger.info(
            f"Combined: image='{img_label}' speech='{aud_label}' "
            f"match={match} avg_conf={avg_conf:.1f}%"
        )

        return CombinedPredictionResponse(
            alphabet=img_label,
            speech=aud_label,
            match=match,
            confidence=avg_conf,
        )
    except ValueError as exc:
        logger.warning(f"Preprocessing error in predict_both: {exc}")
        return JSONResponse(status_code=400, content={"error": str(exc)})
    except Exception as exc:
        logger.error(f"Unexpected error in predict_both: {exc}")
        return JSONResponse(
            status_code=500, content={"error": "Combined prediction failed."}
        )
