# io_wav.py
from __future__ import annotations
import numpy as np
import soundfile as sf

def read_wav(path: str) -> tuple[np.ndarray, int]:
    x, sr = sf.read(path, always_2d=False)
    return x.astype(np.float32), sr

def write_wav(path: str, x: np.ndarray, sr: int) -> None:
    sf.write(path, x, sr)

def peak_normalize_if_needed(x: np.ndarray, peak: float = 0.98) -> np.ndarray:
    m = float(np.max(np.abs(x))) + 1e-12
    if m > peak:
        x = x * (peak / m)
    return x.astype(np.float32)
