import customtkinter as ctk
import threading
import os
import queue
from main import TTSManager

# Configuration
VOICES = [
    "--- American English ---",
    "am_puck (Andrew-style Young/Energetic Male)",
    "af_sky (Energetic Female)",
    "af_nicole (Dynamic Female)",
    "af_heart (Warm Female)",
    "af_bella (Passionate Female)",
    "af_sarah (Soft Female)",
    "af_nova (Neutral Female)",
    "am_michael (Deep Male)",
    "am_adam (Neutral Male)",
    "am_fenrir (Strong Male)",
    "am_liam (Youthful Male)",
    "am_echo (Crisp Male)",
    "--- British English ---",
    "bf_emma (Clear Female)",
    "bf_isabella (Gentle Female)",
    "bm_george (Proper Male)",
    "bm_fable (Deep Male)",
    "bm_lewis (Soft Male)",
]

class KokoroGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Kokoro TTS - YouTube Shorts Generator")
        self.geometry("700x550")
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.manager = None
        self.msg_queue = queue.Queue()
        
        # Configure layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header_label = ctk.CTkLabel(self, text="Kokoro TTS Generator", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Main Text Area
        self.text_frame = ctk.CTkFrame(self)
        self.text_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)

        self.text_input = ctk.CTkTextbox(self.text_frame, font=ctk.CTkFont(size=14))
        self.text_input.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.text_input.insert("1.0", "YO! What is up everyone! \n\nStop throwing your money away on things that don't matter. \n\nIf you want to build REAL wealth, you need to start TODAY. \n\nI'm talking about high-yield savings, consistent investing, and cutting the fluff. \n\nLet's get after it!")

        # Controls Frame
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Voice Selection
        self.voice_label = ctk.CTkLabel(self.controls_frame, text="Voice:")
        self.voice_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.voice_dropdown = ctk.CTkComboBox(self.controls_frame, values=VOICES, width=200)
        self.voice_dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.voice_dropdown.set(VOICES[1]) # Default to af_sky

        # --- Second Row: Speed and Modulation ---
        self.row2_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.row2_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        # Speed Label and Entry/Slider
        self.speed_label = ctk.CTkLabel(self.row2_frame, text="Speed:")
        self.speed_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.speed_slider = ctk.CTkSlider(self.row2_frame, from_=0.2, to=3.0, number_of_steps=28, command=self.sync_speed_entry)
        self.speed_slider.grid(row=0, column=1, padx=10, pady=10)
        self.speed_slider.set(1.15)

        self.speed_entry = ctk.CTkEntry(self.row2_frame, width=60)
        self.speed_entry.grid(row=0, column=2, padx=10, pady=10)
        self.speed_entry.insert(0, "1.15")
        self.speed_entry.bind("<Return>", self.sync_speed_slider)

        # Modulation (Blend) Control
        self.blend_label = ctk.CTkLabel(self.row2_frame, text="Modulation (Blend):")
        self.blend_label.grid(row=0, column=3, padx=10, pady=10)

        self.blend_dropdown = ctk.CTkComboBox(self.row2_frame, values=["None"] + VOICES, width=180)
        self.blend_dropdown.grid(row=0, column=4, padx=10, pady=10)
        self.blend_dropdown.set("None")

        self.blend_slider = ctk.CTkSlider(self.row2_frame, from_=0, to=1, number_of_steps=20, width=100)
        self.blend_slider.grid(row=0, column=5, padx=10, pady=10)
        self.blend_slider.set(0.5)

        # Modulation Presets
        self.preset_label = ctk.CTkLabel(self.row2_frame, text="Quick Presets:")
        self.preset_label.grid(row=0, column=6, padx=10, pady=10)

        self.mod_presets = {
            "Custom": None,
            "Deep & Authoritative": ("am_michael", "am_adam", 0.6, 1.0),
            "Smart & Youthful": ("am_puck", "am_liam", 0.7, 1.1),
            "Crisp & Clear": ("am_echo", "af_nova", 0.8, 1.15),
            "Professional Soft": ("af_sky", "af_sarah", 0.5, 1.0)
        }

        self.mod_preset_dropdown = ctk.CTkComboBox(self.row2_frame, values=list(self.mod_presets.keys()), 
                                                 width=150, command=self.apply_mod_preset)
        self.mod_preset_dropdown.grid(row=0, column=7, padx=10, pady=10)
        self.mod_preset_dropdown.set("Custom")

        # Progress and Status
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self, text="Ready | Misaki G2P Active", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=4, column=0, padx=20, pady=(0, 5))

        # Tips Label
        self.tips_label = ctk.CTkLabel(self, text="Tip: Use '<>' for a 1-second break, or ',,' for a short pause!", 
                                     font=ctk.CTkFont(size=11, slant="italic"), text_color="gray")
        self.tips_label.grid(row=5, column=0, padx=20, pady=(0, 10))

        # Generate Buttons Frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        self.generate_button = ctk.CTkButton(self.button_frame, text="Generate Speech", font=ctk.CTkFont(size=16, weight="bold"), 
                                            height=40, command=self.start_generation)
        self.generate_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        # Liam Preset Button
        self.liam_button = ctk.CTkButton(self.button_frame, text="Liam (Relaxed) Preset", font=ctk.CTkFont(size=16), 
                                        fg_color="#2c3e50", hover_color="#34495e", height=40, 
                                        command=self.apply_liam_preset)
        self.liam_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        # Start checking the message queue
        self.check_queue()

    def check_queue(self):
        """Check for messages from the background thread."""
        try:
            while True:
                msg_type, data = self.msg_queue.get_nowait()
                if msg_type == "SUCCESS":
                    self.finish_generation(data)
                elif msg_type == "ERROR":
                    self.finish_generation(data, "red")
                self.msg_queue.task_done()
        except queue.Empty:
            pass
        finally:
            self.after(100, self.check_queue)

    def apply_liam_preset(self):
        # Apply the specific settings requested
        target_voice = "am_liam (Youthful Male)"
        # Check if the voice exists in our list (it might be named slightly differently)
        for v in VOICES:
            if v.startswith("am_liam"):
                target_voice = v
                break
        
        self.voice_dropdown.set(target_voice)
        self.speed_slider.set(0.7)
        self.speed_entry.delete(0, "end")
        self.speed_entry.insert(0, "0.7")
        self.start_generation()

    def sync_speed_entry(self, value):
        self.speed_entry.delete(0, "end")
        self.speed_entry.insert(0, f"{value:.2f}")

    def sync_speed_slider(self, event):
        try:
            val = float(self.speed_entry.get())
            self.speed_slider.set(val)
        except ValueError:
            pass

    def apply_mod_preset(self, preset_name):
        settings = self.mod_presets.get(preset_name)
        if not settings:
            return
            
        v1, v2, ratio, speed = settings
        
        # Find full names in VOICES
        v1_full = next((v for v in VOICES if v.startswith(v1)), v1)
        v2_full = next((v for v in VOICES if v.startswith(v2)), v2)
        
        self.voice_dropdown.set(v1_full)
        self.blend_dropdown.set(v2_full)
        self.blend_slider.set(ratio)
        self.speed_slider.set(speed)
        self.speed_entry.delete(0, "end")
        self.speed_entry.insert(0, f"{speed:.2f}")

    def start_generation(self):
        text = self.text_input.get("1.0", "end-1c").strip()
        if not text:
            self.update_status("Error: Please enter some text", "red")
            return

        voice_full = self.voice_dropdown.get()
        if voice_full.startswith("---"):
            self.update_status("Error: Please select a valid voice", "red")
            return
            
        voice_id = voice_full.split(" ")[0]
        
        # Handling Speed
        try:
            speed = float(self.speed_entry.get())
        except ValueError:
            speed = self.speed_slider.get()

        # Handling Modulation (Blending)
        blend_full = self.blend_dropdown.get()
        blend_voice = None
        blend_ratio = 0
        if blend_full != "None" and not blend_full.startswith("---"):
            blend_voice = blend_full.split(" ")[0]
            blend_ratio = self.blend_slider.get()

        self.generate_button.configure(state="disabled")
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        self.update_status("Generating audio...", "white")

        # Run generation in a separate thread to keep UI responsive
        thread = threading.Thread(target=self.generate_audio, args=(text, voice_id, speed, blend_voice, blend_ratio))
        thread.start()

    def generate_audio(self, text, voice_id, speed, blend_voice=None, blend_ratio=0):
        try:
            if self.manager is None:
                self.manager = TTSManager()
            
            output_file = "output.wav"
            self.manager.generate(text, voice=voice_id, speed=speed, output_file=output_file, 
                                 blend_voice=blend_voice, blend_ratio=blend_ratio)
            
            self.msg_queue.put(("SUCCESS", f"Success! Saved to {output_file}"))
        except Exception as e:
            self.msg_queue.put(("ERROR", f"Error: {str(e)}"))

    def finish_generation(self, message, color="white"):
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(1)
        self.update_status(message, color)
        self.generate_button.configure(state="normal")

    def update_status(self, text, color="white"):
        self.status_label.configure(text=text, text_color=color)

if __name__ == "__main__":
    app = KokoroGUI()
    app.mainloop()
