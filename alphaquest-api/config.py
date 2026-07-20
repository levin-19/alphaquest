"""
config.py — Central configuration for AlphaQuest API.
All constants, paths, and environment values live here.
No hardcoded values anywhere else in the project.
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables or defaults."""

    # --- Project ---
    PROJECT_NAME: str = "AlphaQuest API"
    API_VERSION: str = "1.0.0"
    DEBUG_MODE: bool = False

    # --- Directories ---
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    MODELS_DIR: str = os.path.join(BASE_DIR, "models")
    LABELS_DIR: str = os.path.join(BASE_DIR, "labels")

    # --- Model Paths ---
    ALPHABET_MODEL_PATH: str = os.path.join(MODELS_DIR, "alphabet_model.h5")
    SPEECH_MODEL_PATH: str = os.path.join(MODELS_DIR, "speech_model.h5")

    # --- Label Paths ---
    ALPHABET_LABELS_PATH: str = os.path.join(LABELS_DIR, "alphabet_labels.json")
    SPEECH_LABELS_PATH: str = os.path.join(LABELS_DIR, "speech_labels.json")

    # --- Upload Constraints ---
    MAX_UPLOAD_SIZE_BYTES: int = 20 * 1024 * 1024  # 20 MB

    # --- Allowed File Extensions ---
    ALLOWED_IMAGE_EXTENSIONS: set = {".png", ".jpg", ".jpeg", ".webp"}
    ALLOWED_AUDIO_EXTENSIONS: set = {".wav", ".mp3"}

    # --- Model Input ---
    IMAGE_TARGET_SIZE: tuple = (224, 224)
    AUDIO_TARGET_SR: int = 16000
    AUDIO_MFCC_N: int = 13
    AUDIO_TARGET_LEN: int = 100

    model_config = {"case_sensitive": True}


# Singleton settings instance used across the app
settings = Settings()
