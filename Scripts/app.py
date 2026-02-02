# app.py
from __future__ import annotations
import io
import numpy as np
import soundfile as sf
import streamlit as st

from echo import apply_echo
from time_stretch import apply_time_stretch
from pitch_shift import pitch_shift

st.set_page_config(page_title="WAV Audio Processor", layout="centered")
st.title("WAV 音声加工ツール")
st.caption("中央=0（変化なし）で調整できるUI")

def read_wav_from_bytes(wav_bytes: bytes) -> tuple[np.ndarray, int]:
    bio = io.BytesIO(wav_bytes)
    x, sr = sf.read(bio, always_2d=False)
    return x.astype(np.float32), sr

def write_wav_to_bytes(x: np.ndarray, sr: int) -> bytes:
    bio = io.BytesIO()
    sf.write(bio, x, sr, format="WAV")
    return bio.getvalue()

def bipolar_to_unit(k: float) -> float:
    """[-1,1] -> [0,1]"""
    return (k + 1.0) / 2.0

uploaded = st.file_uploader("WAVファイルを選択", type=["wav"])
if uploaded is None:
    st.info("WAVをアップロードすると設定UIが出ます。")
    st.stop()

x, sr = read_wav_from_bytes(uploaded.getvalue())
st.success(f"読み込み成功: sample rate = {sr} Hz, shape = {x.shape}")

st.subheader("加工の設定（中央=0）")

col1, col2 = st.columns(2)

with col1:
    use_echo = st.checkbox("エコー", value=False)
    echo_k = st.slider("エコー量（-1〜+1）", -1.0, 1.0, 0.0, 0.01, disabled=not use_echo)

    # echo_k を delay/decay に変換
    # delay: 0.08〜0.50秒（負側でも動く）
    delay_sec = 0.08 + 0.42 * bipolar_to_unit(echo_k)
    # decay: 正側だけ有効（0〜0.7）
    decay = max(0.0, echo_k) * 0.70

    st.caption(f"内部パラメータ: delay={delay_sec:.3f}s, decay={decay:.2f}")

with col2:
    use_tempo = st.checkbox("テンポ（ピッチ維持）", value=False)
    tempo_k = st.slider("テンポ量（-1〜+1）", -1.0, 1.0, 0.0, 0.01, disabled=not use_tempo)
    stretch = 2 ** tempo_k
    st.caption(f"内部パラメータ: stretch={stretch:.3f}（>1で遅く、<1で速く）")

    use_pitch = st.checkbox("ピッチ（長さ維持）", value=False)
    pitch_k = st.slider("ピッチ量（-1〜+1）", -1.0, 1.0, 0.0, 0.01, disabled=not use_pitch)
    semitones = 12.0 * pitch_k
    st.caption(f"内部パラメータ: semitones={semitones:+.2f}")

st.subheader("適用順")
order = st.multiselect(
    "順番（おすすめ：Echo → Tempo → Pitch）",
    options=["Echo", "Tempo", "Pitch"],
    default=["Echo", "Tempo", "Pitch"],
)

if st.button("加工してプレビュー生成", type="primary"):
    y = x

    for name in order:
        if name == "Echo" and use_echo:
            # echo_k が0付近だと decay=0 で実質OFFになる
            y = apply_echo(y, sr, delay_sec=delay_sec, decay=decay)
        elif name == "Tempo" and use_tempo:
            y = apply_time_stretch(y, sr, stretch=stretch)
        elif name == "Pitch" and use_pitch:
            y = pitch_shift(y, semitones=semitones, sr=sr)

    out_bytes = write_wav_to_bytes(y, sr)

    st.subheader("プレビュー")
    st.audio(out_bytes, format="audio/wav")

    st.download_button(
        label="加工後WAVをダウンロード",
        data=out_bytes,
        file_name="processed.wav",
        mime="audio/wav",
    )

    st.write("出力情報:", {"sr": sr, "shape": tuple(y.shape), "seconds": float(len(y) / sr)})
