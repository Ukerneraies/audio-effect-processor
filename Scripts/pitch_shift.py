# pitch_shift.py
from __future__ import annotations
import numpy as np
from scipy.signal import stft, istft
from io_wav import peak_normalize_if_needed

def _phase_vocoder_time_stretch_mono(x: np.ndarray, stretch: float, sr: int,
                                     n_fft: int = 2048, hop: int = 512) -> np.ndarray:
    """
    位相ボコーダで time-stretch（ピッチは維持）
    stretch > 1.0: 長く（テンポ遅く）
    stretch < 1.0: 短く（テンポ速く）
    """
    if stretch <= 0:
        raise ValueError("stretch must be > 0")

    # STFT
    f, t, Z = stft(x, fs=sr, nperseg=n_fft, noverlap=n_fft - hop, boundary=None, padded=False)
    mag = np.abs(Z)
    phase = np.angle(Z)

    # time steps in analysis frames -> synthesis frames
    n_frames = Z.shape[1]
    t_out = np.arange(0, n_frames, 1.0 / stretch)
    t_out = t_out[t_out < n_frames - 1]

    # 位相の進み（期待値）
    omega = 2 * np.pi * np.arange(Z.shape[0]) * hop / n_fft

    phase_acc = phase[:, 0].copy()
    Z_out = np.zeros((Z.shape[0], len(t_out)), dtype=np.complex64)

    prev_phase = phase[:, 0].copy()

    for i, ti in enumerate(t_out):
        t0 = int(np.floor(ti))
        t1 = t0 + 1
        a = ti - t0

        # magnitude interpolate
        mag_i = (1 - a) * mag[:, t0] + a * mag[:, t1]

        # phase advance
        dphi = phase[:, t1] - phase[:, t0]
        dphi = np.mod(dphi - omega + np.pi, 2*np.pi) - np.pi  # wrap to [-pi, pi]
        phase_acc += omega + dphi

        Z_out[:, i] = mag_i * np.exp(1j * phase_acc)
        prev_phase = phase[:, t1]

    # ISTFT
    _, y = istft(Z_out, fs=sr, nperseg=n_fft, noverlap=n_fft - hop, input_onesided=True)
    return y.astype(np.float32)

def time_stretch(x: np.ndarray, stretch: float, sr: int,
                 n_fft: int = 2048, hop: int = 512) -> np.ndarray:
    """
    mono/stereo対応：チャンネルごとに処理
    """
    x = x.astype(np.float32)
    if x.ndim == 1:
        y = _phase_vocoder_time_stretch_mono(x, stretch, sr, n_fft=n_fft, hop=hop)
        return peak_normalize_if_needed(y)
    else:
        ys = []
        for ch in range(x.shape[1]):
            ys.append(_phase_vocoder_time_stretch_mono(x[:, ch], stretch, sr, n_fft=n_fft, hop=hop))
        y = np.stack(ys, axis=1)
        return peak_normalize_if_needed(y)

def pitch_shift(x: np.ndarray, semitones: float, sr: int,
                n_fft: int = 2048, hop: int = 512) -> np.ndarray:
    """
    ピッチ変更（長さは維持）：
    1) time-stretch で長さを変える
    2) resample（ここでは線形補間）で元の長さに戻す
    """
    if semitones == 0:
        return x.astype(np.float32)

    factor = 2 ** (semitones / 12.0)  # ピッチ倍率
    # ピッチを上げたい→一旦短くする（stretch < 1）
    stretched = time_stretch(x, 1.0 / factor, sr, n_fft=n_fft, hop=hop)

    # 元の長さに戻す（サンプル数合わせ）
    target_len = x.shape[0]
    y = _resample_to_length(stretched, target_len)

    return peak_normalize_if_needed(y)

def _resample_to_length(x: np.ndarray, target_len: int) -> np.ndarray:
    """
    目標サンプル数に合わせる簡易リサンプル（線形補間）。
    """
    if target_len <= 0:
        raise ValueError("target_len must be > 0")

    if x.ndim == 1:
        idx = np.linspace(0, len(x) - 1, target_len)
        y = np.interp(idx, np.arange(len(x)), x).astype(np.float32)
        return y

    # stereo / multi-channel
    ys = []
    for ch in range(x.shape[1]):
        idx = np.linspace(0, len(x) - 1, target_len)
        ys.append(np.interp(idx, np.arange(len(x)), x[:, ch]))
    y = np.stack(ys, axis=1).astype(np.float32)
    return y
