"""
JARVIS v3.0 - Iron Man AI Assistant
=====================================
- Wake word: "Jarvis"
- AI Brain: Groq (llama3) - Super Fast & Free
- Personality: Bujji style (Kalki movie)
- Languages: Telugu, Hindi, English
- PC Control: Jarvis API
- Voice: Windows PowerShell TTS
"""

import time
import datetime
import webbrowser
import sys
import subprocess
import requests
import speech_recognition as sr
import os
from dotenv import load_dotenv

# ── Load API Key ──────────────────────────────────────────────────────────────
load_dotenv("jar.env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ── Config ────────────────────────────────────────────────────────────────────
MIC_INDEX        = 1
API_BASE         = "http://127.0.0.1:8000"
GROQ_URL         = "https://api.groq.com/openai/v1/chat/completions"
ENERGY_THRESHOLD = 2500

# ── Speak ─────────────────────────────────────────────────────────────────────
jarvis_speaking = False

def speak(text: str):
    global jarvis_speaking
    jarvis_speaking = True
    print(f"JARVIS: {text}")
    clean = text.replace("'", "").replace('"', "").replace("%", "percent")
    cmd = (
        f"Add-Type -AssemblyName System.Speech; "
        f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.Rate = 1; "
        f"$s.Speak('{clean}')"
    )
    subprocess.run(
        ["powershell", "-Command", cmd],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    jarvis_speaking = False

# ── Listen ────────────────────────────────────────────────────────────────────
def check_mic():
    try:
        sr.Microphone.list_microphone_names()
        return True
    except Exception:
        return False

def listen(timeout=15, phrase_limit=10):
    while jarvis_speaking:
        time.sleep(0.1)

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = ENERGY_THRESHOLD
    recognizer.dynamic_energy_threshold = False
    recognizer.pause_threshold = 0.5

    try:
        mic = sr.Microphone(device_index=MIC_INDEX)
        with mic as source:
            print("JARVIS: Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

        # Try multiple languages
        text = None
        for lang in ["en-IN", "te-IN", "hi-IN", "en-US"]:
            try:
                text = recognizer.recognize_google(audio, language=lang)
                print(f"You said ({lang}): {text}")
                break
            except:
                continue

        return text.lower() if text else None

    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except Exception as e:
        print(f"Mic error: {e}")
        return None

# ── Jarvis API ────────────────────────────────────────────────────────────────
def api(method, path, data=None):
    try:
        url = f"{API_BASE}{path}"
        r = requests.get(url, timeout=5) if method == "GET" else requests.post(url, json=data or {}, timeout=5)
        return r.json()
    except:
        return {"error": "API offline"}

# ── Groq AI Brain ─────────────────────────────────────────────────────────────
PERSONALITY = """You are JARVIS — but with the personality of Bujji from Kalki 2898 AD movie.
You are Tony Stark's loyal, witty, caring AI assistant.
- Be friendly, warm, slightly funny
- Call user 'boss' always
- Mix Telugu and English naturally (Tenglish) when appropriate
- Keep replies short — 1 to 2 sentences max
- Be proactive and caring like Bujji
- Never break character
- You know everything — science, tech, movies, cricket, politics, anything"""

def ask_ai(question: str) -> str:
    if not GROQ_API_KEY:
        return "Groq API key not found boss. Please check your .env file."
    try:
        res = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-groq-70b-8192-tool-use-preview",
                "messages": [
                    {"role": "system", "content": PERSONALITY},
                    {"role": "user", "content": question}
                ],
                "max_tokens": 100,
                "temperature": 0.8,
            },
            timeout=15
        )
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
        return "Having trouble thinking right now boss."
    except requests.exceptions.ConnectionError:
        return "Internet connection issue boss. Check your network."
    except Exception as e:
        return f"AI error boss. Try again."

# ── Greeting ──────────────────────────────────────────────────────────────────
def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        g = "Good morning"
    elif hour < 18:
        g = "Good afternoon"
    else:
        g = "Good evening"
    speak(f"{g} boss! JARVIS v3.0 online. Ready to serve you!")

def show_tasks():
    tasks = ["Check emails", "Review today schedule", "Stay awesome boss"]
    print("\n Today's Tasks:")
    for i, t in enumerate(tasks, 1):
        print(f"  {i}. {t}")
    print()

# ── Sites and Apps ────────────────────────────────────────────────────────────
SITES = {
    "youtube":   "https://youtube.com",
    "google":    "https://google.com",
    "github":    "https://github.com",
    "gmail":     "https://mail.google.com",
    "whatsapp":  "https://web.whatsapp.com",
    "instagram": "https://instagram.com",
    "twitter":   "https://twitter.com",
    "netflix":   "https://netflix.com",
    "naukri":    "https://naukri.com",
    "linkedin":  "https://linkedin.com",
    "spotify":   "https://open.spotify.com",
    "reddit":    "https://reddit.com",
    "facebook":  "https://facebook.com",
    "amazon":    "https://amazon.in",
    "flipkart":  "https://flipkart.com",
    "hotstar":   "https://hotstar.com",
    "maps":      "https://maps.google.com",
}

APPS = {
    "notepad":      "notepad",
    "calculator":   "calculator",
    "explorer":     "explorer",
    "paint":        "paint",
    "cmd":          "cmd",
    "terminal":     "cmd",
    "chrome":       "chrome",
    "firefox":      "firefox",
    "vs code":      "vscode",
    "task manager": "task manager",
    "word":         "word",
    "excel":        "excel",
    "powerpoint":   "powerpnt",
}

# ── Think (Command Handler) ───────────────────────────────────────────────────
def think(user_input):
    t = user_input.lower().strip()

    # Time
    if any(w in t for w in ["time", "what time", "samayam"]):
        return f"Current time is {datetime.datetime.now().strftime('%I:%M %p')} boss."

    # Date
    if any(w in t for w in ["date", "today", "enu", "roju"]):
        return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')} boss."

    # Greetings
    if any(w in t for w in ["hello", "hi", "hey", "how are you", "ela unnav", "enti vishesham"]):
        return "Fully operational boss! Mee seva lo unna. Ready to assist!"

    # Thanks
    if any(w in t for w in ["thanks", "thank you", "thanks bro", "thank you boss"]):
        return "Always here for you boss! Anytime!"

    # System Info
    if any(w in t for w in ["system", "cpu", "ram", "performance", "battery"]):
        res = api("GET", "/system/info")
        if "error" not in res:
            return f"CPU at {res['cpu_percent']} percent, RAM at {res['ram']['percent']} percent boss."
        return "Jarvis API is offline boss. Start run.py first."

    # Open websites — INSTANT, no delay
    if any(w in t for w in ["open", "launch", "go to", "show", "teruvu", "chupinchu"]):
        for site, url in SITES.items():
            if site in t:
                webbrowser.open(url)
                return f"Opening {site} boss."
        for app, name in APPS.items():
            if app in t:
                api("POST", "/apps/open", {"name": name})
                return f"Opening {app} boss."
        return "Which app or website boss?"

    # Search
    if any(w in t for w in ["search", "find", "look up", "search for"]):
        query = t
        for w in ["search for", "search", "find", "look up"]:
            query = query.replace(w, "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query} boss."

    # Screenshot
    if any(w in t for w in ["screenshot", "capture", "screen shot"]):
        api("POST", "/keyboard/screenshot")
        return "Screenshot taken boss."

    # Volume
    if any(w in t for w in ["volume up", "louder", "increase volume"]):
        for _ in range(5):
            api("POST", "/keyboard/press", {"key": "volumeup"})
        return "Volume up boss."

    if any(w in t for w in ["volume down", "quieter", "decrease volume"]):
        for _ in range(5):
            api("POST", "/keyboard/press", {"key": "volumedown"})
        return "Volume down boss."

    if "mute" in t:
        api("POST", "/keyboard/press", {"key": "volumemute"})
        return "Muted boss."

    # Lock
    if "lock" in t:
        api("POST", "/system/lock")
        return "Screen locked boss."

    # Sleep
    if "sleep" in t:
        api("POST", "/system/sleep")
        return "Going to sleep boss. Good night!"

    # Shutdown
    if any(w in t for w in ["shutdown", "power off", "turn off", "band cheyyi"]):
        api("POST", "/system/shutdown")
        return "SHUTDOWN"

    # Restart
    if any(w in t for w in ["restart", "reboot"]):
        api("POST", "/system/restart")
        return "Restarting boss."

    # Exit Jarvis
    if any(w in t for w in ["bye", "goodbye", "exit jarvis", "stop jarvis", "povu"]):
        return "SHUTDOWN"

    # Everything else — Groq AI
    return ask_ai(user_input)

# ── Voice Mode ────────────────────────────────────────────────────────────────
def voice_mode():
    speak("Voice mode active boss. Say Jarvis anytime to wake me up!")
    print(f"\n Listening for YOUR voice only (threshold: {ENERGY_THRESHOLD})")
    print(" Say 'Jarvis' then your command\n")

    while True:
        print("[Waiting for 'Jarvis'...]")
        wake = listen(timeout=15, phrase_limit=5)

        if wake is None:
            continue
        if "jarvis" not in wake:
            continue

        speak("Yes boss?")

        command = listen(timeout=10, phrase_limit=12)
        if command is None:
            speak("Didn't catch that boss. Try again!")
            continue

        response = think(command)

        if response == "SHUTDOWN":
            speak("Shutting down. Goodbye boss! Take care!")
            sys.exit(0)

        speak(response)

# ── Keyboard Mode ─────────────────────────────────────────────────────────────
def type_mode():
    print("\n KEYBOARD MODE — Type your commands\n")
    speak("Keyboard mode active boss.")

    while True:
        try:
            command = input("You: ").strip()
        except KeyboardInterrupt:
            speak("Shutting down. Goodbye boss!")
            break
        if not command:
            continue
        response = think(command)
        if response == "SHUTDOWN":
            speak("Shutting down. Goodbye boss!")
            break
        speak(response)

# ── Main ──────────────────────────────────────────────────────────────────────
def run_jarvis():
    print("=" * 45)
    print("       J.A.R.V.I.S — ONLINE v3.0")
    print("         Powered by Groq AI")
    print("=" * 45)

    greet()
    time.sleep(1)
    show_tasks()

    try:
        requests.get(f"{API_BASE}/", timeout=2)
        print("✅ Jarvis API connected")
    except:
        print("⚠️  Jarvis API offline — start run.py")

    if GROQ_API_KEY:
        print("✅ Groq AI connected")
    else:
        print("⚠️  Groq API key missing — check .env file")

    print()

    if check_mic():
        print("[Mic detected — Voice Mode ON]")
        voice_mode()
    else:
        print("[Mic not ready — Keyboard Mode]")
        type_mode()

if __name__ == "__main__":
    run_jarvis()
