"""
utils/image_utils.py — Image loading, RGB conversion, resize, normalize,
expand dimensions, and tensor conversion.
"""
import io
from typing import Tuple

import numpy as np
from PIL import Image

from config import settings
from core.logger import get_logger

logger = get_logger("ImageUtils")


def load_image_from_bytes(image_bytes: bytes) -> Image.Image:
    """
    Open an image from raw bytes using Pillow.

    Args:
        image_bytes: Raw bytes of the image file.

    Returns:
        A PIL Image object.

    Raises:
        ValueError: If the bytes cannot be decoded as an image.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()                       # Detect truncated or invalid images early
        img = Image.open(io.BytesIO(image_bytes))  # Re-open after verify() (it consumes the stream)
        return img
    except Exception as exc:
        raise ValueError(f"Cannot decode image: {exc}") from exc


def convert_to_rgb(img: Image.Image) -> Image.Image:
    """
    Convert any PIL image mode (RGBA, L, P, CMYK …) to RGB.

    Args:
        img: Input PIL Image.

    Returns:
        A new RGB PIL Image.
    """
    if img.mode != "RGB":
        img = img.convert("RGB")
    return img


def resize_image(img: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
    """
    Resize a PIL image to the given (width, height) target using LANCZOS resampling.

    Args:
        img:         Input PIL Image.
        target_size: (width, height) tuple.

    Returns:
        Resized PIL Image.
    """
    return img.resize(target_size, Image.LANCZOS)


def normalize_image(img_array: np.ndarray) -> np.ndarray:
    """
    Normalize pixel values from [0, 255] to [0.0, 1.0].

    Args:
        img_array: NumPy array of dtype float32 in range [0, 255].

    Returns:
        Normalized NumPy array in range [0.0, 1.0].
    """
    return img_array / 255.0


def expand_image_dims(img_array: np.ndarray) -> np.ndarray:
    """
    Add a batch dimension to make the array model-compatible.
    (H, W, C) → (1, H, W, C)

    Args:
        img_array: 3-D NumPy array.

    Returns:
        4-D NumPy array with batch dimension at axis 0.
    """
    return np.expand_dims(img_array, axis=0)


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Full image preprocessing pipeline:
    load → RGB → resize → float32 → normalize → expand dims.

    Args:
        image_bytes: Raw bytes of the uploaded image.

    Returns:
        4-D float32 NumPy array ready for TensorFlow inference.

    Raises:
        ValueError: If any step in the pipeline fails.
    """
    try:
        img = load_image_from_bytes(image_bytes)
        img = convert_to_rgb(img)
        img = resize_image(img, settings.IMAGE_TARGET_SIZE)
        img_array = np.array(img, dtype=np.float32)
        img_array = normalize_image(img_array)
        img_array = expand_image_dims(img_array)
        logger.info(f"Image preprocessed to shape {img_array.shape}.")
        return img_array
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"Image preprocessing failed: {exc}") from exc
