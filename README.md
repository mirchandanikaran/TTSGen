# Kokoro TTS GUI

A high-performance, offline Text-to-Speech (TTS) system with a modern graphical interface, designed for creating engaging voiceovers for YouTube Shorts and content creation. Powered by **Kokoro-82M** and **ONNX Runtime**.

## 🚀 Features

- **High-Quality Offline TTS**: Natural-sounding speech generated entirely locally.
- **Voice Modulation (Blending)**: Mix two different voices to create unique vocal characters.
- **Energetic Presets**: Pre-configured profiles (e.g., "Smart & Youthful", "Deep & Authoritative") optimized for engagement.
- **Custom Pauses**: Use the `<>` tag in your script for precise 1-second breaks.
- **Precise Speed Control**: Adjust speed from 0.2x to 3.0x via slider or direct text input.
- **Enhanced Punctuation**: Integrated with **Misaki G2P** for better prosody and natural flow.
- **Standalone Mac App**: Build a dedicated `.app` bundle for your Applications folder.

## 📦 Installation

This project uses `uv` for fast, reliable dependency management.

1. **Install uv** (if you haven't):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and Install**:
   ```bash
   cd kokoro_tts
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

3. **Models**:
   Ensure `kokoro-v1.0.onnx` and `voices-v1.0.bin` are in the project root.

## 🖥️ Usage

### Launch the GUI
```bash
uv run gui.py
```

### CLI Generation
```bash
uv run main.py "Hello world! <> Welcome to the show." --voice am_puck --speed 1.15
```

## 🛠️ Building the Standalone Mac App
To create a `KokoroTTS.app` for your Mac:
```bash
uv run python build.py
```
Check the `dist/` folder after completion.

## 📜 License
This project is for educational and creative use. The underlying Kokoro model is subject to its own license.
