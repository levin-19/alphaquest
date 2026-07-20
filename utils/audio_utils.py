"""
utils/audio_utils.py — Audio loading, silence trimming, normalization,
MFCC extraction, padding, and reshape for TensorFlow inference.
"""
import io

import librosa
import numpy as np
import soundfile as sf

from config import settings
from core.logger import get_logger

logger = get_logger("AudioUtils")


def load_audio_from_bytes(audio_bytes: bytes) -> tuple:
    """
    Load audio data from raw bytes using soundfile.

    Args:
        audio_bytes: Raw bytes of the audio file (wav or mp3).

    Returns:
        Tuple of (audio_array: np.ndarray, sample_rate: int).

    Raises:
        ValueError: If the bytes cannot be decoded as audio.
    """
    try:
        audio, sr = sf.read(io.BytesIO(audio_bytes))
        return audio, sr
    except Exception as exc:
        raise ValueError(f"Cannot decode audio: {exc}") from exc


def to_mono(audio: np.ndarray) -> np.ndarray:
    """
    Convert stereo (multi-channel) audio to mono by averaging channels.

    Args:
        audio: NumPy array. Shape (samples,) or (samples, channels).

    Returns:
        1-D mono NumPy array.
    """
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)
    return audio


def resample_audio(audio: np.ndarray, orig_sr: int) -> np.ndarray:
    """
    Resample audio to the project's target sample rate if needed.

    Args:
        audio:   Mono audio array.
        orig_sr: Original sample rate.

    Returns:
        Resampled audio array at settings.AUDIO_TARGET_SR.
    """
    if orig_sr != settings.AUDIO_TARGET_SR:
        audio = librosa.resample(
            y=audio.astype(np.float32),
            orig_sr=orig_sr,
            target_sr=settings.AUDIO_TARGET_SR,
        )
    return audio


def trim_silence(audio: np.ndarray) -> np.ndarray:
    """
    Trim leading and trailing silence from an audio array.

    Args:
        audio: Mono audio array.

    Returns:
        Trimmed audio array.
    """
    trimmed, _ = librosa.effects.trim(audio)
    return trimmed


def normalize_audio(audio: np.ndarray) -> np.ndarray:
    """
    Normalize audio amplitude to the range [-1.0, 1.0].

    Args:
        audio: Mono audio array.

    Returns:
        Normalized audio array.
    """
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val
    return audio


def extract_mfcc(audio: np.ndarray) -> np.ndarray:
    """
    Extract Mel Frequency Cepstral Coefficients (MFCC) from audio.

    Args:
        audio: Normalized mono audio array.

    Returns:
        2-D MFCC array of shape (n_mfcc, frames).
    """
    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=settings.AUDIO_TARGET_SR,
        n_mfcc=settings.AUDIO_MFCC_N,
    )
    return mfcc


def pad_mfcc(mfcc: np.ndarray) -> np.ndarray:
    """
    Pad or truncate MFCC to a fixed time-axis length for consistent model input.

    Args:
        mfcc: 2-D array of shape (n_mfcc, frames).

    Returns:
        2-D array of shape (n_mfcc, AUDIO_TARGET_LEN).
    """
    target = settings.AUDIO_TARGET_LEN
    if mfcc.shape[1] < target:
        pad_width = target - mfcc.shape[1]
        mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode="constant")
    else:
        mfcc = mfcc[:, :target]
    return mfcc


def reshape_for_model(mfcc: np.ndarray) -> np.ndarray:
    """
    Add batch and channel dimensions for CNN-style models.
    (n_mfcc, frames) → (1, n_mfcc, frames, 1)

    Args:
        mfcc: 2-D array of shape (n_mfcc, frames).

    Returns:
        4-D array ready for TensorFlow inference.
    """
    mfcc = np.expand_dims(mfcc, axis=0)   # batch dim
    mfcc = np.expand_dims(mfcc, axis=-1)  # channel dim
    return mfcc


def preprocess_audio(audio_bytes: bytes) -> np.ndarray:
    """
    Full audio preprocessing pipeline:
    load → mono → resample → trim → normalize → MFCC → pad → reshape.

    Args:
        audio_bytes: Raw bytes of the uploaded audio file.

    Returns:
        4-D float32 NumPy array ready for TensorFlow inference.

    Raises:
        ValueError: If any step in the pipeline fails.
    """
    try:
        audio, sr = load_audio_from_bytes(audio_bytes)
        audio = to_mono(audio).astype(np.float32)
        audio = resample_audio(audio, sr)
        audio = trim_silence(audio)
        audio = normalize_audio(audio)
        mfcc = extract_mfcc(audio)
        mfcc = pad_mfcc(mfcc)
        mfcc = reshape_for_model(mfcc)
        logger.info(f"Audio preprocessed to shape {mfcc.shape}.")
        return mfcc
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"Audio preprocessing failed: {exc}") from exc
