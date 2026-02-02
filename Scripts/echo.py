# echo.py
from __future__ import annotations
import numpy as np
from io_wav import peak_normalize_if_needed

def apply_echo(x: np.ndarray, sr: int, delay_sec: float = 0.25, decay: float = 0.35) -> np.ndarray:
    """
    単発ディレイによる簡易エコー
    mono: (N,)
    stereo: (N, C)
    """
    x = x.astype(np.float32)
    delay = int(sr * delay_sec)
    if delay <= 0:
        return x

    y = np.copy(x)

    if x.ndim == 1:
        y[delay:] += decay * x[:-delay]
    else:
        y[delay:, :] += decay * x[:-delay, :]

    return peak_normalize_if_needed(y)
