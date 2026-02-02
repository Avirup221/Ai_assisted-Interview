import asyncio
import os
import wave
import keyboard
import pyaudio
import pyttsx3
import numpy as np
import tkinter as tk
from tkinter import filedialog
from faster_whisper import WhisperModel

# Local imports
from groq_llm import InterviewManager
from resume_parser import extract_text_from_resume

# --- Configuration ---
TEMP_AUDIO_FILE = "temp_recording.wav"
WHISPER_MODEL_SIZE = "base.en"

class AudioHandler:
    def __init__(self):
        print(f"⏳ Loading Whisper model ({WHISPER_MODEL_SIZE})...")
        self.stt_model = WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type="float32")
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 165)

    def record_audio(self, filename):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000 
        p = pyaudio.PyAudio()
        
        try:
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        except OSError:
            print("❌ Error: Check microphone.")
            return False

        print("\n" + "="*40)
        print("   🔴 RECORDING... (Press 'q' to stop)")
        print("="*40 + "\n")

        frames = []
        # Clear buffer to avoid accidental triggers
        while keyboard.is_pressed('q'): pass

        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            if keyboard.is_pressed('q'):
                print("⏹️  Stopped.")
                break

        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        return True

    def transcribe(self, filename):
        print("📝 Transcribing...")
        try:
            segments, _ = self.stt_model.transcribe(filename, beam_size=5, language="en")
            text = " ".join([s.text for s in segments]).strip()
            return text
        except Exception:
            return ""

    def speak(self, text):
        print(f"\n🗣️  Interviewer: {text}")
        try:
            clean = text.replace("*", "").replace("#", "")
            self.tts_engine.say(clean)
            self.tts_engine.runAndWait()
        except Exception:
            pass

def select_file_dialog():
    """Opens a system window to select the resume file."""
    print("📂 Opening file picker...")
    
    # Create a hidden root window so the full TK GUI doesn't show up
    root = tk.Tk()
    root.withdraw() 
    root.attributes('-topmost', True) # Bring to front
    
    file_path = filedialog.askopenfilename(
        title="Select your Resume",
        filetypes=[("PDF & Text Files", "*.pdf *.txt"), ("All Files", "*.*")]
    )
    
    root.destroy()
    return file_path

async def main():
    # 1. Setup Phase
    audio = AudioHandler()
    
    # Open File Dialog
    print("\n" + "="*50)
    print("   PLEASE SELECT YOUR RESUME FILE")
    print("="*50)
    
    resume_path = select_file_dialog()
    
    if not resume_path:
        print("⚠️ No file selected. Starting in generic mode.")
        resume_text = "No resume context provided. Ask standard behavioral questions."
    else:
        print(f"✅ Selected: {resume_path}")
        resume_text = extract_text_from_resume(resume_path)
        if not resume_text:
            print("❌ Could not read text from file. Using generic mode.")
            resume_text = "No resume context."

    # Initialize AI Interviewer
    interviewer = InterviewManager(resume_text)
    
    # 2. Start the Interview
    print("\n🚀 Starting Interview... (AI is reading your resume...)")
    
    # Send "start" trigger
    first_question = await interviewer.get_next_question("The interview is starting now.")
    audio.speak(first_question)

    # 3. Main Loop
    while True:
        print("\n" + "-"*50)
        print("Options: 'r' = Record Answer | 'x' = End & Feedback")
        print("-" * 50)
        
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'r':
                    # --- Recording Phase ---
                    audio.record_audio(TEMP_AUDIO_FILE)
                    user_text = await asyncio.to_thread(audio.transcribe, TEMP_AUDIO_FILE)
                    
                    if not user_text or len(user_text) < 2:
                        print("⚠️  Didn't catch that. Press 'r' to try again.")
                        break

                    print(f"\n🔹 You: {user_text}")
                    
                    # --- AI Generation Phase ---
                    print("\n🧠 AI is thinking...")
                    next_question = await interviewer.get_next_question(user_text)
                    audio.speak(next_question)
                    break 

                elif event.name == 'x':
                    # --- Feedback Phase ---
                    print("\n🛑 Ending Interview. Generating Feedback...")
                    feedback = await interviewer.get_final_feedback()
                    
                    print("\n" + "="*60)
                    print("FINAL FEEDBACK REPORT")
                    print("="*60)
                    print(feedback)
                    
                    audio.speak("Interview complete. I have printed your feedback on the screen.")
                    
                    if os.path.exists(TEMP_AUDIO_FILE):
                        os.remove(TEMP_AUDIO_FILE)
                    return

            await asyncio.sleep(0.05)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")