# Kokoro TTS - YouTube Shorts Pro 🎙️

A high-performance, offline Text-to-Speech (TTS) system with a premium graphical interface, specifically optimized for creating engaging, professional voiceovers for YouTube Shorts and social media content. Powered by **Kokoro-82M** and **ONNX Runtime**.

## 🌟 Premium Features

- **High-Quality Offline TTS**: Natural-sounding speech generated entirely locally—no cloud costs, no latency.
- **Voice Modulation (Blending)**: Mix any two voices from the library to create your own unique vocal signature.
- **Pitch Control**: Deepen or brighten your voice (0.5x to 1.5x) with precise spinbox and arrow controls.
- **Pro Voice Presets**: One-click access to curated vocal profiles:
    - **Deep Narrator (Engaging)**: Our signature default for storytelling.
    - **Excited Pro Artist**: High-energy broadcast style.
    - **Smart & Youthful**: Perfect for fast-paced educational shorts.
- **Granular Pacing Controls**:
    - `<`: 0.5-second natural pause.
    - `<>`: 1.0-second dramatic break.
    - `,,`: Subtle conversational pause.
- **Gender Swap (M/F)**: Instant toggle between top-tier male and female voices.
- **Precise Speed Input**: Adjust speed (0.2x to 3.0x) via slider or direct numerical input with arrows.
- **Misaki G2P Integration**: Enhanced phoneme processing for superior punctuation and natural prosody.

## 📦 Installation

This project uses `uv` for lightning-fast dependency management.

1. **Install uv**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Setup Project**:
   ```bash
   cd kokoro_tts
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

3. **Required Assets**:
   Download and place `kokoro-v1.0.onnx` and `voices-v1.0.bin` in the project root.

## 🖥️ Usage

### Launch the GUI
```bash
uv run gui.py
```

### CLI Support
```bash
uv run main.py "Welcome to the show! < Get ready for the truth." --voice am_michael --speed 0.85 --pitch 1.15
```

## 🛠️ Standalone Mac App
Create a dedicated **KokoroTTS.app** for your Applications folder:
```bash
uv run python build.py
```
*Note: The app is self-contained and runs completely offline.*

## 📜 License
This tool is built for creators. The underlying Kokoro model is subject to its own licensing terms.
