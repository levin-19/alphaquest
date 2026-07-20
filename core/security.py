"""
core/security.py — Security middleware, file validation, and sanitization.
"""
import os
import re
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings
from core.logger import get_logger

logger = get_logger("Security")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that injects essential security headers into every HTTP response.
    Prevents XSS, clickjacking, and MIME sniffing attacks.
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


def sanitize_filename(filename: str) -> str:
    """
    Remove potentially dangerous characters from a filename.
    Prevents path traversal attacks (e.g., ../../etc/passwd).

    Args:
        filename: The raw filename from the upload.

    Returns:
        A sanitized, safe filename string.
    """
    # Strip directory components
    filename = os.path.basename(filename)
    # Keep only safe characters: alphanumeric, dashes, underscores, dots
    filename = re.sub(r"[^\w\.\-]", "_", filename)
    return filename


def validate_image_extension(filename: str) -> None:
    """
    Validate that the file extension is in the allowed image list.

    Args:
        filename: The sanitized filename.

    Raises:
        ValueError: If the extension is not allowed.
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        allowed = ", ".join(settings.ALLOWED_IMAGE_EXTENSIONS)
        raise ValueError(f"Unsupported image format '{ext}'. Allowed: {allowed}")


def validate_audio_extension(filename: str) -> None:
    """
    Validate that the file extension is in the allowed audio list.

    Args:
        filename: The sanitized filename.

    Raises:
        ValueError: If the extension is not allowed.
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext not in settings.ALLOWED_AUDIO_EXTENSIONS:
        allowed = ", ".join(settings.ALLOWED_AUDIO_EXTENSIONS)
        raise ValueError(f"Unsupported audio format '{ext}'. Allowed: {allowed}")


def validate_upload_size(content: bytes, label: str = "file") -> None:
    """
    Validate that the uploaded file content does not exceed the size limit.

    Args:
        content: The raw bytes of the uploaded file.
        label: Human-readable label for error messages.

    Raises:
        ValueError: If the file size exceeds the limit.
    """
    max_mb = settings.MAX_UPLOAD_SIZE_BYTES / (1024 * 1024)
    if len(content) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise ValueError(f"The {label} exceeds the {max_mb:.0f}MB upload limit.")
