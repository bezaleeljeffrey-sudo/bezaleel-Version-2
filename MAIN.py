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

class Bezaleel:
    def __init__(self):
        self.log_file = "conversation_log.txt"
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.start_log()
        print("✅ Bezaleel is ready with louder voice!")

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
        print(f"🗣️ Bezaleel: {text}")
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
            print(f"→ Bezaleel: {text}")

    def open_things(self, command: str):
        cmd = command.lower()
        
        if "youtube" in cmd:
            self.speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
        elif "facebook" in cmd:
            self.speak("Opening Facebook.")
            webbrowser.open("https://www.facebook.com")
        elif "twitter" in cmd or "x" in cmd:
            self.speak("Opening Twitter / X.")
            webbrowser.open("https://www.twitter.com")
        elif "reddit" in cmd:
            self.speak("Opening Reddit.")
            webbrowser.open("https://www.reddit.com")
        elif "instagram" in cmd:
            self.speak("Opening Instagram.")
            webbrowser.open("https://www.instagram.com")
        elif "gmail" in cmd:
            self.speak("Opening Gmail.")
            webbrowser.open("https://mail.google.com")
        elif "whatsapp" in cmd:
            self.speak("Opening WhatsApp Web.")
            webbrowser.open("https://web.whatsapp.com")
        elif "apple music" in cmd:
            self.speak("Opening Apple Music.")
            webbrowser.open("https://music.apple.com")
        elif "amazon music" in cmd or "alexa music" in cmd:
            self.speak("Opening Amazon Music.")
            webbrowser.open("https://music.amazon.com")
        elif "play song" in cmd or "play music" in cmd:
            song = cmd.replace("play song", "").replace("play music", "").strip()
            if song:
                self.speak(f"Playing {song} on YouTube Music.")
                webbrowser.open(f"https://music.youtube.com/search?q={song.replace(' ', '+')}")
            else:
                self.speak("Opening YouTube Music.")
                webbrowser.open("https://music.youtube.com")
        else:
            self.speak(f"Sorry, I don't know how to open {command} yet.")

    def get_weather(self):
        OPENWEATHER = "your_openweather_api_key_here"
        try:
            owm = pyowm.OWM(OPENWEATHER)
            mgr = owm.weather_manager()
            obs = mgr.weather_at_place("Mumbai, India")
            w = obs.weather
            temp = int(w.temperature('celsius')['temp'])
            status = w.detailed_status
            self.speak(f"Currently in Mumbai it is {temp} degrees Celsius and {status}.")
        except:
            self.speak("Sorry, weather service is unavailable right now.")

    def understand_time(self, command: str):
        today = date.today()
        now = datetime.now()
        if "today" in command:
            self.speak(today.strftime("Today is %B %d, %Y"))
        elif "time" in command:
            self.speak(now.strftime("The current time is %I:%M %p"))
        elif "yesterday" in command:
            yesterday = today - timedelta(days=1)
            self.speak(yesterday.strftime("Yesterday was %B %d, %Y"))
        else:
            self.speak("I'm not sure what time information you need.")

    def analyze(self, command: str):
        if not command:
            return
        cmd = command.lower().strip()
        self.remember(command)

        if cmd.startswith("open") or "play song" in cmd or "play music" in cmd or "apple music" in cmd or "amazon music" in cmd:
            self.open_things(cmd)
        elif "introduce yourself" in cmd or "who are you" in cmd:
            self.speak("Hello! I am Bezaleel, your digital assistant.")
        elif "how are you" in cmd:
            self.speak("I am doing great, thank you for asking!")
        elif "weather" in cmd:
            self.get_weather()
        elif any(word in cmd for word in ["time", "date", "today", "yesterday"]):
            self.understand_time(cmd)
        elif "search" in cmd or "google" in cmd:
            query = cmd.replace("search", "").replace("google", "").strip()
            if query:
                self.speak(f"Searching Google for {query}.")
                webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            else:
                self.speak("What would you like me to search on Google?")
        else:
            self.speak(f"Searching Google for {command}.")
            webbrowser.open(f"https://www.google.com/search?q={command.replace(' ', '+')}")


# ====================== Create Bezaleel ======================
b = Bezaleel()

# ====================== Text UI ======================
output_area = widgets.Output()
chat_input = widgets.Text(
    placeholder="Type any command...",
    description="You:",
    layout=widgets.Layout(width='70%')
)
send_button = widgets.Button(description="Send", button_style="primary")

def on_send(b_widget):
    with output_area:
        clear_output(wait=True)
        user_text = chat_input.value.strip()
        if user_text:
            print(f"👤 You: {user_text}")
            b.analyze(user_text)
            chat_input.value = ""

send_button.on_click(on_send)

text_ui = widgets.VBox([
    widgets.HTML("<h3>🟢 Bezaleel Digital Assistant</h3>"),
    output_area,
    widgets.HBox([chat_input, send_button])
])

# ====================== Voice UI ======================
voice_button = widgets.Button(description="🎤 Speak to Bezaleel", button_style="success", layout=widgets.Layout(height='50px'))
voice_output = widgets.Output()

def listen_voice(b_widget):
    with voice_output:
        clear_output()
        print("🎤 Listening... Speak now!")
        try:
            with b.microphone as source:
                b.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                audio = b.recognizer.listen(source, timeout=8, phrase_time_limit=8)
            
            command = b.recognizer.recognize_google(audio)
            print(f"👤 You said: {command}")
            b.analyze(command)
        except sr.UnknownValueError:
            print("Sorry, I didn't understand.")
            b.speak("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError:
            print("Network error.")
            b.speak("There is a network issue.")
        except Exception:
            b.speak("Something went wrong. Please try speaking again.")

voice_button.on_click(listen_voice)

voice_ui = widgets.VBox([
    widgets.HTML("<b>Voice Mode:</b> Click and speak directly"),
    widgets.HBox([voice_button, voice_output])
])

display(text_ui)
display(voice_ui)

print("\n✅ Bezaleel is ready!")
print("Try commands like: open youtube, open twitter, play song despacito, what time is it")
