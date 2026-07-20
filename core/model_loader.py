"""
core/model_loader.py — Singleton TensorFlow model and label manager.
Models and labels are loaded exactly once at startup. Every call to
get_alphabet_model() / get_speech_model() returns the cached object.
"""
import json
import os
from typing import Any, Dict, Optional

import tensorflow as tf

from config import settings
from core.logger import get_logger

logger = get_logger("ModelLoader")


class _ModelLoader:
    """
    Private singleton class that manages TensorFlow model and label loading.
    Do not instantiate directly — use the module-level `model_manager` instance.
    """

    _instance: Optional["_ModelLoader"] = None

    def __new__(cls) -> "_ModelLoader":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._models: Dict[str, Any] = {}
            cls._instance._labels: Dict[str, Dict[str, str]] = {}
            cls._instance._loaded = False
        return cls._instance

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def load_all(self) -> None:
        """
        Load all models and labels into memory.
        Safe to call multiple times — subsequent calls are no-ops.
        """
        if self._loaded:
            logger.info("Models already loaded, skipping.")
            return

        logger.info("Loading AlphaQuest models and labels…")

        self._load_labels("alphabet", settings.ALPHABET_LABELS_PATH)
        self._load_labels("speech", settings.SPEECH_LABELS_PATH)
        self._load_model("alphabet", settings.ALPHABET_MODEL_PATH)
        self._load_model("speech", settings.SPEECH_MODEL_PATH)

        self._loaded = True
        logger.info("Models loaded successfully.")
        logger.info("API Ready.")

    def get_alphabet_model(self) -> Any:
        """
        Return the loaded alphabet model.

        Returns:
            The Keras model instance, or None if not loaded.
        """
        return self._models.get("alphabet")

    def get_speech_model(self) -> Any:
        """
        Return the loaded speech model.

        Returns:
            The Keras model instance, or None if not loaded.
        """
        return self._models.get("speech")

    def get_label(self, key: str, index: int) -> str:
        """
        Resolve a predicted class index to its human-readable label.

        Args:
            key:   Either "alphabet" or "speech".
            index: The integer class index output by the model.

        Returns:
            A label string. Falls back to the raw index if not found.
        """
        return self._labels.get(key, {}).get(str(index), str(index))

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_model(self, key: str, path: str) -> None:
        """Load a single .h5 model from disk."""
        if not os.path.exists(path):
            logger.warning(f"Model file not found: {path}. Endpoint will return 503.")
            return
        try:
            self._models[key] = tf.keras.models.load_model(path)
            logger.info(f"Loaded {key} model from {path}.")
        except Exception as exc:
            logger.error(f"Failed to load {key} model: {exc}")

    def _load_labels(self, key: str, path: str) -> None:
        """Load a JSON label file from disk."""
        if not os.path.exists(path):
            logger.warning(f"Label file not found: {path}.")
            return
        try:
            with open(path, "r", encoding="utf-8") as fh:
                self._labels[key] = json.load(fh)
            logger.info(f"Loaded {key} labels ({len(self._labels[key])} classes).")
        except Exception as exc:
            logger.error(f"Failed to load {key} labels: {exc}")


# Module-level singleton — import and use this everywhere
model_manager = _ModelLoader()
