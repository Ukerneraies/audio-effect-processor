
# audio-effect-processor
WAV 音声ファイルに対して、音程変更（Pitch）、テンポ変更（Tempo）、エコー（Echo）などの加工を行い、加工後の音声を書き出すツールです。  
UI から直感的にパラメータを調整して出力できます（※UI実装がある場合）。

## Contents
- [🛠️ Usage](#Usage)
- [📜 License & Citation & Acknowledgments](#License)
<br><br>

## <a name="Usage"></a>🛠️ Usage

### Requirements

* Python 3.8 or later
* Recommended: OS Windows
<br>

### Repository Cloning and Dependency Installation

```bash
git clone https://github.com/Ukerneraies/audio-effect-processor
cd audio-effect-processor
conda create --name audio_effect python=3.8
conda activate audio_effect
pip install -r requirements.txt
```
### Using the UI：
Startup command
```bash
streamlit run Scripts/app.py
```
1.Upload a WAV file
2.Adjust the pitch, tempo, and echo
3.Output the processed audio (save/download)

### Using the CLI：
Pitch
```bash
python Scripts/pitch_shift.py --in input.wav --out output_pitch.wav --amount 0.0
```
Tempo
```bash
python Scripts/time_stretch.py --in input.wav --out output_tempo.wav --amount 0.0
```
Echo
```bash
python Scripts/echo.py --in input.wav --out output_echo.wav --amount 0.0

```
<br><br>
## <a name="License"></a>📜 License & Disclaimer & Citation

### Disclaimer

This project is provided **"AS IS"**, without warranty of any kind.

Despite best efforts to improve quality and reliability, **we do not guarantee** the accuracy, performance, or suitability of the output audio.  
Audio processing may cause artifacts (noise/distortion), unexpected changes in loudness, or degradation depending on parameters and input conditions.

The authors and contributors do not assume any legal responsibility for any damages, data loss, security issues, public opinion risks, or liabilities arising from the use, misuse, abuse, or improper utilization of this project.

### Citation
If you find our work helpful, please cite it!

```
@article{Ukerneraies,
  title={audio-effect-processor},
  author={Ukerneraies},
  year={2026}
}
```



