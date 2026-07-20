"""
core/logger.py — Centralized logging configuration for AlphaQuest API.
All modules should import get_logger() from here.
"""
import logging
import sys
import time
from functools import wraps
from typing import Callable


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a named logger with consistent formatting.

    Args:
        name: The module/component name for the logger.

    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(name)

    # Only add handlers if they don't exist (prevents duplicate log lines)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    return logger


def log_prediction_time(logger: logging.Logger) -> Callable:
    """
    Decorator that logs the inference time of a prediction function.

    Args:
        logger: The logger to use for timing output.

    Returns:
        A decorator function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            logger.info(f"{func.__name__} completed in {elapsed:.2f}ms")
            return result
        return wrapper
    return decorator
