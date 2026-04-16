import speech_recognition as sr
from gtts import gTTS
from IPython.display import Audio, display, clear_output
import ipywidgets as widgets
from datetime import date, timedelta, datetime
import pyowm
import random
import webbrowser
import os
import tempfile
from pydub import AudioSegment

class Shane:
    def __init__(self):
        self.log_file = "conversation_log.txt"
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.start_log()
        print("✅ SHANE is ready with Music & Google Search!")

    def start_log(self):
        today = date.today().strftime("%Y-%m-%d %H:%M")
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"\n=== Conversation Started: {today} ===\n")
        except:
            pass

    def remember(self, command: str):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"User: {command}\n")
        except:
            pass

    def speak(self, text: str):
        """Very loud voice"""
        print(f"🗣️ SHANE: {text}")
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                temp_filename = tmp.name
                tts.save(temp_filename)
            
            audio = AudioSegment.from_mp3(temp_filename)
            louder_audio = audio + 18
            louder_audio = louder_audio.normalize()
            
            louder_filename = temp_filename.replace(".mp3", "_loud.mp3")
            louder_audio.export(louder_filename, format="mp3")
            
            display(Audio(louder_filename, autoplay=True))
        except Exception as e:
            print(f"Audio error: {e}")
            print(f"→ SHANE: {text}")

    def open_things(self, command: str):
        cmd = command.lower()
        
        if "youtube" in cmd:
            self.speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
        elif "facebook" in cmd:
print("• open twitter / open reddit")
