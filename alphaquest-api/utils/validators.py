"""
utils/validators.py — File type and size validation helpers.
Import from here to avoid duplicated validation logic.
"""
import os
from config import settings


def validate_image_file(filename: str, content: bytes) -> None:
    """
    Validate an image upload by extension and size.

    Args:
        filename: Sanitized filename from the upload.
        content:  Raw file bytes.

    Raises:
        ValueError: If the extension is invalid or the file is too large.
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        allowed = ", ".join(sorted(settings.ALLOWED_IMAGE_EXTENSIONS))
        raise ValueError(f"Unsupported image type '{ext}'. Allowed: {allowed}.")

    _check_size(content, "image")


def validate_audio_file(filename: str, content: bytes) -> None:
    """
    Validate an audio upload by extension and size.

    Args:
        filename: Sanitized filename from the upload.
        content:  Raw file bytes.

    Raises:
        ValueError: If the extension is invalid or the file is too large.
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext not in settings.ALLOWED_AUDIO_EXTENSIONS:
        allowed = ", ".join(sorted(settings.ALLOWED_AUDIO_EXTENSIONS))
        raise ValueError(f"Unsupported audio type '{ext}'. Allowed: {allowed}.")

    _check_size(content, "audio")


def _check_size(content: bytes, label: str) -> None:
    """
    Internal helper to enforce MAX_UPLOAD_SIZE_BYTES.

    Args:
        content: Raw bytes to measure.
        label:   Human-readable name used in error messages.

    Raises:
        ValueError: If the content exceeds the configured limit.
    """
    limit = settings.MAX_UPLOAD_SIZE_BYTES
    if len(content) > limit:
        limit_mb = limit / (1024 * 1024)
        raise ValueError(f"The {label} exceeds the {limit_mb:.0f} MB upload limit.")
