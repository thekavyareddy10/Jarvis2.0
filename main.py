"""
JARVIS v2.0 - Iron Man AI Assistant
=====================================
- Wake word: "Jarvis"
- AI Brain: Ollama (llama3.2) - 100% Free
- PC Control: Jarvis API
- Voice: Windows PowerShell TTS (reliable)
"""

import time
import datetime
import webbrowser
import sys
import subprocess
import requests
import speech_recognition as sr

# ── Config ────────────────────────────────────────────────────────────────────
MIC_INDEX        = 1
API_BASE         = "http://127.0.0.1:8000"
OLLAMA_URL       = "http://localhost:11434/api/generate"
AI_MODEL         = "llama3.2"
ENERGY_THRESHOLD = 2500

# ── Speak (Windows PowerShell TTS) ───────────────────────────────────────────
jarvis_speaking = False

def speak(text: str):
    global jarvis_speaking
    jarvis_speaking = True
    print(f"JARVIS: {text}")
    # Clean text for PowerShell
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
    recognizer.pause_threshold = 0.6

    try:
        mic = sr.Microphone(device_index=MIC_INDEX)
        with mic as source:
            print("JARVIS: Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        text = recognizer.recognize_google(audio, language="en-IN")
        print(f"You said: {text}")
        return text.lower()
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

# ── Ollama AI Brain ───────────────────────────────────────────────────────────
PERSONALITY = """You are JARVIS, Tony Stark's AI assistant.
Be witty, helpful, slightly formal. Call user 'boss'.
Keep replies short - 1 to 2 sentences only.
Never break character."""

def ask_ai(question):
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": AI_MODEL,
            "prompt": f"{PERSONALITY}\n\nUser: {question}\nJARVIS:",
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 80},
        }, timeout=30)
        if res.status_code == 200:
            return res.json().get("response", "").strip()
        return "Having trouble thinking right now boss."
    except requests.exceptions.ConnectionError:
        return "Ollama is offline boss. Please start the Ollama app."
    except:
        return "AI error boss. Try again."

# ── Greeting ──────────────────────────────────────────────────────────────────
def greet():
    hour = datetime.datetime.now().hour
    g = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    speak(f"{g} boss! JARVIS v2.0 online and ready.")

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
}

APPS = {
    "notepad":      "notepad",
    "calculator":   "calculator",
    "explorer":     "explorer",
    "paint":        "paint",
    "cmd":          "cmd",
    "chrome":       "chrome",
    "firefox":      "firefox",
    "vs code":      "vscode",
    "task manager": "task manager",
    "word":         "word",
    "excel":        "excel",
}

# ── Think ─────────────────────────────────────────────────────────────────────
def think(user_input):
    t = user_input.lower().strip()

    if any(w in t for w in ["time", "what time"]):
        return f"Current time is {datetime.datetime.now().strftime('%I:%M %p')} boss."

    if any(w in t for w in ["date", "today"]):
        return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')} boss."

    if any(w in t for w in ["hello", "hi", "how are you"]):
        return "Fully operational boss! Ready to assist."

    if any(w in t for w in ["thanks", "thank you"]):
        return "Always here for you boss!"

    if any(w in t for w in ["system", "cpu", "ram", "performance"]):
        res = api("GET", "/system/info")
        if "error" not in res:
            return f"CPU at {res['cpu_percent']} percent, RAM at {res['ram']['percent']} percent boss."
        return "Jarvis API is offline boss."

    if any(w in t for w in ["open", "launch", "go to"]):
        for site, url in SITES.items():
            if site in t:
                webbrowser.open(url)
                return f"Opening {site} boss."
        for app, name in APPS.items():
            if app in t:
                api("POST", "/apps/open", {"name": name})
                return f"Opening {app} boss."
        return "Which app or site boss?"

    if t.startswith("search "):
        query = t.replace("search ", "")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query} boss."

    if "screenshot" in t:
        api("POST", "/keyboard/screenshot")
        return "Screenshot taken boss."

    if "volume up" in t or "louder" in t:
        for _ in range(5):
            api("POST", "/keyboard/press", {"key": "volumeup"})
        return "Volume up boss."

    if "volume down" in t or "quieter" in t:
        for _ in range(5):
            api("POST", "/keyboard/press", {"key": "volumedown"})
        return "Volume down boss."

    if "mute" in t:
        api("POST", "/keyboard/press", {"key": "volumemute"})
        return "Muted boss."

    if "lock" in t:
        api("POST", "/system/lock")
        return "Screen locked boss."

    if "shutdown" in t or "power off" in t:
        api("POST", "/system/shutdown")
        return "SHUTDOWN"

    if "restart" in t or "reboot" in t:
        api("POST", "/system/restart")
        return "Restarting boss."

    if any(w in t for w in ["bye", "stop", "exit", "goodbye"]):
        return "SHUTDOWN"

    return ask_ai(user_input)

# ── Voice Mode ────────────────────────────────────────────────────────────────
def voice_mode():
    speak("Voice mode active. Say Jarvis to wake me up boss.")
    print(f"\n Listening only for YOUR voice (threshold: {ENERGY_THRESHOLD})")
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
            speak("Didn't catch that boss. Try again.")
            continue

        response = think(command)

        if response == "SHUTDOWN":
            speak("Shutting down. Goodbye boss!")
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
    print("       J.A.R.V.I.S — ONLINE v2.0")
    print("=" * 45)

    greet()
    time.sleep(1)
    show_tasks()

    try:
        requests.get(f"{API_BASE}/", timeout=2)
        print("✅ Jarvis API connected")
    except:
        print("⚠️  Jarvis API offline — start run.py")

    try:
        requests.get("http://localhost:11434", timeout=2)
        print("✅ Ollama AI connected")
    except:
        print("⚠️  Ollama offline — start Ollama app")

    print()

    if check_mic():
        print("[Mic detected — Voice Mode ON]")
        voice_mode()
    else:
        print("[Mic not ready — Keyboard Mode]")
        type_mode()

if __name__ == "__main__":
    run_jarvis()
