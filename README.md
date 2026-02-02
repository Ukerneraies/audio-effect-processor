# audio-effect-processor

WAV 音声ファイルに対して、音程変更（Pitch）、テンポ変更（Tempo）、エコー（Echo）などの加工を行い、加工後の音声を書き出すツールです。  
UI から直感的にパラメータを調整して出力できます（※UI実装がある場合）。

---

## 特徴

- WAV の読み込み → 加工 → WAV 書き出し
- 主な加工
  - Pitch（音の高さ）
  - Tempo（テンポ）
  - Echo（エコー）
- UI で調整できる（対応している場合）
- **スライダーの中心が 0**（基準）で、左右に動かすと増減する設計

---

## デモ（スクリーンショット）

- `<img width="781" height="865" alt="image" src="https://github.com/user-attachments/assets/d454d5c6-9aaa-496c-8acf-ba3e8347ce2a" />
`

---

## 動作環境

- Python 3.10+（推奨）
- OS: Windows / macOS / Linux（想定）

---

## インストール

### 1) リポジトリの取得

```bash
git clone https://github.com/<YOUR_NAME>/audio-effect-processor.git
cd audio-effect-processor
