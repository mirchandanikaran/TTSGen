import sys
import os
import argparse
from kokoro_onnx import Kokoro
import soundfile as sf
import numpy as np

class TTSManager:
    def __init__(self, model_path="kokoro-v1.0.onnx", voices_path="voices-v1.0.bin"):
        # Handle PyInstaller paths
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(base_path, model_path)
        self.voices_path = os.path.join(base_path, voices_path)
        self.kokoro = None
        self.g2p = None
        
        if not os.path.exists(self.model_path) or not os.path.exists(self.voices_path):
            raise FileNotFoundError(f"Model files not found: {self.model_path} or {self.voices_path}")

    def load_model(self):
        if self.kokoro is None:
            print("Initializing Kokoro TTS...")
            self.kokoro = Kokoro(self.model_path, self.voices_path)
        return self.kokoro

    def load_g2p(self):
        if self.g2p is None:
            try:
                print("Initializing Misaki G2P for enhanced punctuation...")
                from misaki import en
                # We use trf=False for speed, but Misaki still handles punctuation better than basic split
                self.g2p = en.G2P(trf=False, british=False)
            except ImportError:
                print("Misaki not found, falling back to basic G2P.")
                self.g2p = None
        return self.g2p

    def generate(self, text, voice="af_sky", speed=1.1, output_file="output.wav", blend_voice=None, blend_ratio=0.5):
        kokoro = self.load_model()
        g2p = self.load_g2p()
        
        print(f"Generating audio with voice: {voice}, speed: {speed}")
        if blend_voice:
            print(f"Blending with {blend_voice} at ratio {blend_ratio}")
        
        # Prepare voice (handle blending)
        if blend_voice:
            style1 = kokoro.get_voice_style(voice)
            style2 = kokoro.get_voice_style(blend_voice)
            # Linear interpolation between the two style embeddings
            voice_data = (style1 * (1 - blend_ratio)) + (style2 * blend_ratio)
        else:
            voice_data = voice

        # Handle custom breaks '<>'
        segments = text.split("<>")
        full_audio = []
        sample_rate = 24000 # Default for Kokoro

        for i, segment in enumerate(segments):
            segment = segment.strip()
            if segment:
                if g2p:
                    phonemes, _ = g2p(segment)
                    samples, sr = kokoro.create(
                        phonemes, 
                        voice=voice_data, 
                        speed=speed, 
                        lang="en-us",
                        is_phonemes=True
                    )
                else:
                    samples, sr = kokoro.create(
                        segment, 
                        voice=voice_data, 
                        speed=speed, 
                        lang="en-us"
                    )
                
                sample_rate = sr
                full_audio.append(samples)
            
            # Add 1 second of silence if not the last segment (where a '<>' was detected)
            if i < len(segments) - 1:
                silence = np.zeros(int(sample_rate * 1.0)) # 1 second of silence
                full_audio.append(silence)

        if not full_audio:
            return None

        # Concatenate all audio segments
        final_samples = np.concatenate(full_audio)
        sf.write(output_file, final_samples, sample_rate)
        return output_file

def main():
    parser = argparse.ArgumentParser(description="Kokoro TTS Generator")
    parser.add_argument("text", nargs="?", help="Text to convert to speech")
    parser.add_argument("--voice", default="af_sky", help="Voice to use (default: af_sky)")
    parser.add_argument("--speed", type=float, default=1.1, help="Speed of speech (default: 1.1)")
    parser.add_argument("--output", default="output.wav", help="Output filename")
    
    args = parser.parse_args()

    try:
        manager = TTSManager()
        text = args.text
        if not text:
            text = "Welcome to the channel! Today, we're diving deep into the world of finance. Let's get started!"
        
        manager.generate(text, voice=args.voice, speed=args.speed, output_file=args.output)
        print(f"Success! Audio saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
