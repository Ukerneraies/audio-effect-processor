
# audio-effect-processor
This tool processes WAV audio files, changing their pitch, tempo, echo, etc., and exports the processed audio.
You can intuitively adjust parameters from the UI and output the audio (if the UI is implemented).

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
1.Upload a WAV file.
2.Adjust the pitch, tempo, and echo.
3.Output the processed audio (save/download).

### Using the CLI：
Pitch
```bash
python Scripts/process_one.py input.wav out_pitchup.wav --pitch 5
```
Tempo
```bash
python Scripts/process_one.py input.wav out_slow.wav --tempo 1.2
```
Echo
```bash
python Scripts/process_one.py input.wav out_echo.wav --echo --delay 0.22 --decay 0.30

```
<br><br>
## <a name="License"></a>📜 License & Disclaimer & Citation

### Disclaimer

This project is provided **"AS IS"**, without warranty of any kind.

Despite best efforts to improve quality and reliability, **we do not guarantee** the accuracy, performance, or suitability of the output audio.  
Audio processing may cause artifacts (noise/distortion), unexpected changes in loudness, or degradation depending on parameters and input conditions.

The authors and contributors do not assume any legal responsibility for any damages, data loss, security issues, public opinion risks, or liabilities arising from the use, misuse, abuse, or improper utilization of this project.

This project may include code generated or assisted by AI tools (including ChatGPT); users are responsible for validating outputs and results.

### Citation
If you find our work helpful, please cite it!

```
@article{Ukerneraies,
  title={audio-effect-processor},
  author={Ukerneraies},
  year={2026}
}
```



