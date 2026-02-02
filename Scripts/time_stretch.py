# time_stretch.py
from __future__ import annotations
import numpy as np
from scipy.signal import stft, istft
from io_wav import peak_normalize_if_needed

def _stretch_mono(x: np.ndarray, stretch: float, sr: int,n_fft: int = 2048, hop: int = 512) -> np.ndarray:
    if stretch <= 0:
        raise ValueError("stretch must be > 0")

    f, t, Z = stft(x, fs=sr, nperseg=n_fft, noverlap=n_fft - hop, boundary=None, padded=False)
    mag = np.abs(Z)
    phase = np.angle(Z)

    n_frames = Z.shape[1]
    t_out = np.arange(0, n_frames, 1.0 / stretch)
    t_out = t_out[t_out < n_frames - 1]

    omega = 2 * np.pi * np.arange(Z.shape[0]) * hop / n_fft
    phase_acc = phase[:, 0].copy()
    Z_out = np.zeros((Z.shape[0], len(t_out)), dtype=np.complex64)

    for i, ti in enumerate(t_out):
        t0 = int(np.floor(ti))
        t1 = t0 + 1
        a = ti - t0

        mag_i = (1 - a) * mag[:, t0] + a * mag[:, t1]

        dphi = phase[:, t1] - phase[:, t0]
        dphi = np.mod(dphi - omega + np.pi, 2*np.pi) - np.pi
        phase_acc += omega + dphi

        Z_out[:, i] = mag_i * np.exp(1j * phase_acc)

    _, y = istft(Z_out, fs=sr, nperseg=n_fft, noverlap=n_fft - hop, input_onesided=True)
    return y.astype(np.float32)

def apply_time_stretch(x: np.ndarray, sr: int, stretch: float,
                    n_fft: int = 2048, hop: int = 512) -> np.ndarray:
    """
    stretch > 1.0 で遅く（長く）
    stretch < 1.0 で速く（短く）
    """
    x = x.astype(np.float32)
    if x.ndim == 1:
        y = _stretch_mono(x, stretch, sr, n_fft=n_fft, hop=hop)
        return peak_normalize_if_needed(y)
    else:
        ys = []
        for ch in range(x.shape[1]):
            ys.append(_stretch_mono(x[:, ch], stretch, sr, n_fft=n_fft, hop=hop))
        y = np.stack(ys, axis=1)
        return peak_normalize_if_needed(y)
