"""
JARVIS - Iron Man Style AI Assistant
=====================================
- Wake word: "Hey Jarvis"
- AI Brain: Ollama (llama3.2) - 100% Free & Offline
- Voice: Windows TTS
- PC Control: Jarvis API
"""

import speech_recognition as sr
import pyttsx3
import requests
import time
import sys
import os
import webbrowser
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
MIC_INDEX  = 1                      # Your working mic (Intel Smart)
API_BASE   = "http://127.0.0.1:8000"
OLLAMA_URL = "http://localhost:11434/api/generate"
AI_MODEL   = "llama3.2"
WAKE_WORDS = ["hey jarvis", "jarvis", "ok jarvis", "hi jarvis"]

# ── Voice Engine ──────────────────────────────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)

# Pick best male voice
for v in engine.getProperty("voices"):
    if any(name in v.name.lower() for name in ["david", "mark", "george", "zira"]):
        engine.setProperty("voice", v.id)
        break

def speak(text: str):
    print(f"  🤖 JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

# ── Ollama AI Brain ───────────────────────────────────────────────────────────

JARVIS_PERSONALITY = """You are JARVIS, Tony Stark's personal AI assistant. 
You are helpful, witty, and slightly formal. Always address the user as 'sir'.
Keep responses short and conversational (2-3 sentences max).
You can talk about anything - science, jokes, advice, news, etc.
Never break character. You are JARVIS, not an AI assistant."""

def ask_ai(question: str) -> str:
    """Ask Ollama AI and get response."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": AI_MODEL,
                "prompt": f"{JARVIS_PERSONALITY}\n\nUser: {question}\nJARVIS:",
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 100,  # Short responses for faster reply
                }
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        return "I'm having trouble processing that, sir."
    except requests.exceptions.ConnectionError:
        return "Ollama is not running, sir. Please start it."
    except Exception as e:
        return f"AI error, sir: {str(e)[:50]}"

# ── Jarvis API ────────────────────────────────────────────────────────────────

def api(method: str, path: str, data: dict = None):
    try:
        url = f"{API_BASE}{path}"
        r = requests.get(url, timeout=5) if method == "GET" else requests.post(url, json=data or {}, timeout=5)
        return r.json()
    except:
        return {"error": "API not connected"}

# ── Command Handler ───────────────────────────────────────────────────────────

SITES = {
    "youtube":   "https://youtube.com",
    "google":    "https://google.com",
    "github":    "https://github.com",
    "gmail":     "https://mail.google.com",
    "whatsapp":  "https://web.whatsapp.com",
    "instagram": "https://instagram.com",
    "twitter":   "https://twitter.com",
    "netflix":   "https://netflix.com",
    "spotify":   "https://open.spotify.com",
    "facebook":  "https://facebook.com",
    "reddit":    "https://reddit.com",
    "linkedin":  "https://linkedin.com",
}

APPS = {
    "notepad":        "notepad",
    "calculator":     "calculator",
    "explorer":       "explorer",
    "file explorer":  "explorer",
    "paint":          "paint",
    "cmd":            "cmd",
    "terminal":       "cmd",
    "powershell":     "powershell",
    "chrome":         "chrome",
    "firefox":        "firefox",
    "vs code":        "vscode",
    "visual studio":  "vscode",
    "word":           "word",
    "excel":          "excel",
    "task manager":   "task manager",
}

def handle_command(text: str):
    text = text.lower().strip()
    print(f"  🎤 You said: {text}")

    # ── Time & Date ────────────────────────────────────────────────────────
    if "time" in text:
        speak(f"The time is {datetime.now().strftime('%I:%M %p')}, sir.")
        return

    if "date" in text:
        speak(f"Today is {datetime.now().strftime('%A, %B %d %Y')}, sir.")
        return

    # ── System Info ────────────────────────────────────────────────────────
    if any(w in text for w in ["system", "cpu", "ram", "memory", "performance", "battery"]):
        res = api("GET", "/system/info")
        if "error" not in res:
            speak(f"CPU at {res['cpu_percent']}%, RAM at {res['ram']['percent']}%, Disk at {res['disk']['percent']}%.")
        else:
            speak("Jarvis API is offline, sir. Please start run.py.")
        return

    # ── Open Websites ──────────────────────────────────────────────────────
    if any(w in text for w in ["open", "launch", "go to", "show"]):
        for site, url in SITES.items():
            if site in text:
                speak(f"Opening {site}, sir.")
                api("POST", "/apps/open-url", {"url": url})
                return

        for app, name in APPS.items():
            if app in text:
                speak(f"Opening {app}, sir.")
                api("POST", "/apps/open", {"name": name})
                return

        speak("I'm not sure what to open, sir. Could you be more specific?")
        return

    # ── Close Apps ─────────────────────────────────────────────────────────
    if any(w in text for w in ["close", "kill", "stop"]):
        kill_map = {
            "chrome":  "chrome.exe",
            "firefox": "firefox.exe",
            "notepad": "notepad.exe",
            "spotify": "Spotify.exe",
        }
        for keyword, proc in kill_map.items():
            if keyword in text:
                speak(f"Closing {keyword}, sir.")
                api("POST", "/apps/kill", {"name": proc})
                return
        speak("Which application, sir?")
        return

    # ── Screenshot ─────────────────────────────────────────────────────────
    if "screenshot" in text or "capture" in text:
        speak("Screenshot taken, sir.")
        api("POST", "/keyboard/screenshot")
        return

    # ── Volume ─────────────────────────────────────────────────────────────
    if "volume up" in text or "increase volume" in text or "louder" in text:
        for _ in range(5): api("POST", "/keyboard/press", {"key": "volumeup"})
        speak("Volume increased, sir.")
        return

    if "volume down" in text or "decrease volume" in text or "quieter" in text:
        for _ in range(5): api("POST", "/keyboard/press", {"key": "volumedown"})
        speak("Volume decreased, sir.")
        return

    if "mute" in text:
        api("POST", "/keyboard/press", {"key": "volumemute"})
        speak("Muted, sir.")
        return

    # ── Power ──────────────────────────────────────────────────────────────
    if "lock" in text:
        speak("Locking screen, sir.")
        api("POST", "/system/lock")
        return

    if "sleep" in text:
        speak("Going to sleep, sir. Goodnight.")
        time.sleep(2)
        api("POST", "/system/sleep")
        return

    if "shutdown" in text or "turn off" in text or "power off" in text:
        speak("Shutting down in 5 seconds, sir. Goodbye.")
        time.sleep(2)
        api("POST", "/system/shutdown")
        return

    if "restart" in text or "reboot" in text:
        speak("Restarting now, sir.")
        time.sleep(2)
        api("POST", "/system/restart")
        return

    # ── Goodbye ────────────────────────────────────────────────────────────
    if any(w in text for w in ["goodbye", "bye", "stop", "shutdown jarvis", "sleep jarvis"]):
        speak("Goodbye sir. Always a pleasure.")
        sys.exit(0)

    # ── Greetings ──────────────────────────────────────────────────────────
    if any(w in text for w in ["hello", "hi", "hey", "how are you", "what's up"]):
        hour = datetime.now().hour
        g = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
        speak(f"{g} sir. All systems are fully operational.")
        return

    # ── AI Brain (everything else) ─────────────────────────────────────────
    speak("Let me think about that, sir.")
    reply = ask_ai(text)
    speak(reply)


# ── Main Listener ─────────────────────────────────────────────────────────────

def main():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = False
    recognizer.pause_threshold = 0.6

    mic = sr.Microphone(device_index=MIC_INDEX)

    # Calibrate
    print("  🎚️  Calibrating mic...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
    print(f"  ✅ Ready! (threshold: {int(recognizer.energy_threshold)})")

    # Check connections
    try:
        requests.get(f"{API_BASE}/", timeout=2)
        print("  ✅ Jarvis API connected")
    except:
        print("  ⚠️  Jarvis API offline — start run.py in jarvis-api folder")

    try:
        requests.get("http://localhost:11434", timeout=2)
        print("  ✅ Ollama AI connected")
    except:
        print("  ⚠️  Ollama offline — start Ollama app")

    print("\n" + "="*50)
    print("  🤖 JARVIS - Online and Ready")
    print(f"  Say one of: {WAKE_WORDS}")
    print("="*50 + "\n")

    speak("Jarvis online and ready, sir. How can I assist you?")

    while True:
        try:
            with mic as source:
                print("  👂 Listening...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=6)

            text = recognizer.recognize_google(audio, language="en-IN").lower()
            print(f"  [heard]: {text}")

            if any(w in text for w in WAKE_WORDS):
                speak("Yes sir?")
                with mic as source:
                    print("  🎙️  Command...")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=12)
                command = recognizer.recognize_google(audio, language="en-IN")
                handle_command(command)

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"  ❌ Speech error: {e}")
            time.sleep(2)
        except KeyboardInterrupt:
            speak("Jarvis shutting down. Goodbye sir.")
            sys.exit(0)
        except Exception as e:
            print(f"  ⚠️ Error: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
