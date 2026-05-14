# 🤖 JARVIS - Iron Man AI Assistant

100% Free, Offline AI Assistant with Voice Control!

## Setup (One Time Only)

### 1. Install Python libraries
```
python -m pip install SpeechRecognition pyttsx3 requests pyaudio
```

### 2. Make sure these are running:
- Ollama app (for AI brain)
- llama3.2 model: `ollama pull llama3.2`

## Start Jarvis

Just double-click **START_JARVIS.bat**!

Or manually:
```
# Terminal 1 - API
cd jarvis-api
python run.py

# Terminal 2 - Voice  
python jarvis.py
```

## Commands

| చెప్పేది | జరిగేది |
|---------|---------|
| Hey Jarvis, open YouTube | YouTube opens |
| Hey Jarvis, open Chrome | Chrome opens |
| Hey Jarvis, what time is it | Time చెప్తుంది |
| Hey Jarvis, system performance | CPU/RAM చెప్తుంది |
| Hey Jarvis, take a screenshot | Screenshot తీస్తుంది |
| Hey Jarvis, volume up/down | Volume control |
| Hey Jarvis, lock screen | Screen lock |
| Hey Jarvis, tell me a joke | AI joke చెప్తుంది |
| Hey Jarvis, explain black holes | AI explains |
| Hey Jarvis, how are you | Jarvis responds |
| Hey Jarvis, shutdown | PC shutdown |
| Hey Jarvis, goodbye | Jarvis offline |

## Project Structure
```
jarvis-api/          ← PC control API (run this first)
  run.py
  app/

jarvis-voice/        ← This folder
  jarvis.py          ← Main voice assistant
  START_JARVIS.bat   ← One-click start
  requirements.txt
```
