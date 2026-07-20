"""
utils/preprocessing.py — Shared preprocessing entry points.
Import `run_image_pipeline` and `run_audio_pipeline` from here across the app.
"""
import numpy as np

from utils.image_utils import preprocess_image
from utils.audio_utils import preprocess_audio


def run_image_pipeline(image_bytes: bytes) -> np.ndarray:
    """
    Execute the full image preprocessing pipeline.

    Args:
        image_bytes: Raw bytes from the uploaded image file.

    Returns:
        4-D float32 NumPy array ready for model inference.
    """
    return preprocess_image(image_bytes)


def run_audio_pipeline(audio_bytes: bytes) -> np.ndarray:
    """
    Execute the full audio preprocessing pipeline.

    Args:
        audio_bytes: Raw bytes from the uploaded audio file.

    Returns:
        4-D float32 NumPy array ready for model inference.
    """
    return preprocess_audio(audio_bytes)
