from greeting import greet, speak
from tasks import show_tasks
import time

def check_mic():
    try:
        import speech_recognition as sr
        sr.Microphone.list_microphone_names()
        return True
    except Exception:
        return False

def listen():
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("JARVIS: Listening... (matladhu bro)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        text = recognizer.recognize_google(audio, language="en-IN")
        print(f"You said: {text}")
        return text.lower()
    except Exception:
        return None

def think(user_input):
    user_input = user_input.lower().strip()

    if any(w in user_input for w in ["time", "what time"]):
        import datetime
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"Current time is {now} boss."

    if any(w in user_input for w in ["date", "today"]):
        import datetime
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {today}."

    if any(w in user_input for w in ["hello", "hi", "hey"]):
        return "Hello boss! How can I help you today?"

    if any(w in user_input for w in ["how are you", "ela unnav"]):
        return "Fully operational boss. Ready to assist!"

    if "open youtube" in user_input:
        import webbrowser
        webbrowser.open("https://youtube.com")
        return "Opening YouTube boss."

    if "open google" in user_input:
        import webbrowser
        webbrowser.open("https://google.com")
        return "Opening Google boss."

    if "open github" in user_input:
        import webbrowser
        webbrowser.open("https://github.com")
        return "Opening GitHub boss."

    if "open naukri" in user_input:
        import webbrowser
        webbrowser.open("https://naukri.com")
        return "Opening Naukri for job search boss."

    if user_input.startswith("search "):
        query = user_input.replace("search ", "")
        import webbrowser
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query} boss."

    if any(w in user_input for w in ["thanks", "thank you", "thanks bro"]):
        return "Always here for you boss!"

    if any(w in user_input for w in ["bye", "stop", "exit", "shutdown"]):
        return "SHUTDOWN"

    return f"Got it boss. I heard: {user_input}. More skills coming soon!"

def type_mode():
    print("\n" + "="*45)
    print("  KEYBOARD MODE - Type your commands")
    print("  Type 'bye' to exit")
    print("="*45 + "\n")
    speak("Keyboard mode active boss. Type your commands.")

    while True:
        try:
            command = input("You: ").strip().lower()
        except KeyboardInterrupt:
            speak("Shutting down. Goodbye boss!")
            break

        if not command:
            continue

        response = think(command)

        if response == "SHUTDOWN":
            speak("Shutting down. Goodbye boss!")
            print("JARVIS: Offline.")
            break

        print(f"JARVIS: {response}")
        speak(response)

def voice_mode():
    speak("Voice mode active. Say Jarvis to wake me up boss.")
    print("\nJARVIS: Say 'Jarvis' to wake me. Say 'stop' to exit.\n")

    while True:
        print("[Waiting... say 'Jarvis']")
        wake = listen()

        if wake is None:
            continue

        if "jarvis" not in wake:
            continue

        speak("Yes boss, tell me.")
        print("JARVIS: Activated! Listening for command...")

        command = listen()

        if command is None:
            speak("Did not catch that. Try again.")
            continue

        response = think(command)

        if response == "SHUTDOWN":
            speak("Shutting down. Goodbye boss!")
            print("JARVIS: Offline.")
            break

        print(f"JARVIS: {response}")
        speak(response)

def run_jarvis():
    print("=" * 45)
    print("         JARVIS - ONLINE v2.0")
    print("=" * 45)

    greet()
    time.sleep(1)
    show_tasks()
    time.sleep(1)

    if check_mic():
        print("\n[Mic detected - Voice Mode ON]")
        voice_mode()
    else:
        print("\n[Mic not ready - switching to Keyboard Mode]")
        print("Fix: Run ->  python -m pip install pyaudio")
        type_mode()

if __name__ == "__main__":
    run_jarvis()
