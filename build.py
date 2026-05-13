import subprocess
import os
import sys

def build_app():
    print("Starting build process for Kokoro TTS...")
    
    # Base command
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--windowed", # Create a .app bundle on Mac
        "--name=KokoroTTS",
        # Include data files (models)
        "--add-data=kokoro-v1.0.onnx:.",
        "--add-data=voices-v1.0.bin:.",
    ]
    
    # Add customtkinter data (essential for themes to work in bundle)
    try:
        import customtkinter
        ctk_path = os.path.dirname(customtkinter.__file__)
        cmd.append(f"--add-data={ctk_path}:customtkinter")
    except ImportError:
        print("Error: customtkinter not found. Please install it first.")
        return

    # Add misaki/spacy data if possible, but it's often easier to let it download on first run
    # However, to be truly standalone, we should bundle it.
    # For now, we'll stick to the basics and ensure the app can download it if missing.

    # Entry point
    cmd.append("gui.py")
    
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd)
    
    print("\nBuild complete!")
    print("Check the 'dist' folder for 'KokoroTTS.app'.")
    print("Note: The first time you run it, it might take a moment to initialize.")

if __name__ == "__main__":
    build_app()
