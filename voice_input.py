import speech_recognition as sr

def listen():
    """Mic నుండి voice వింటుంది, text గా return చేస్తుంది"""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("JARVIS: Listening... (మాట్లాడు bro)")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("JARVIS: No voice detected, try again.")
            return None

    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("JARVIS: Could not understand, please speak again.")
        return None
    except sr.RequestError:
        print("JARVIS: Internet connection needed for voice recognition.")
        return None
