import pyttsx3
import datetime

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)      # speed
    engine.setProperty('volume', 1.0)    # volume max
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female
    engine.say(text)
    engine.runAndWait()

def greet():
    hour = datetime.datetime.now().hour

    if 5 <= hour < 12:
        time_greeting = "Good morning"
    elif 12 <= hour < 17:
        time_greeting = "Good afternoon"
    elif 17 <= hour < 21:
        time_greeting = "Good evening"
    else:
        time_greeting = "Good night"

    message = f"{time_greeting} boss! JARVIS online. Ready to work!"
    print(f"JARVIS: {message}")
    speak(message)

if __name__ == "__main__":
    greet()