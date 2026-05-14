@echo off
title JARVIS
color 0b
echo.
echo  =============================================
echo    J.A.R.V.I.S - Starting Up...
echo  =============================================
echo.

:: 1. Start Ollama (if not running)
echo  [1/3] Starting Ollama AI...
start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Ollama\ollama.exe" serve
timeout /t 3 /nobreak > nul

:: 2. Start Jarvis API
echo  [2/3] Starting Jarvis API...
start "Jarvis API" /min cmd /k "cd /d C:\Users\%USERNAME%\OneDrive\Desktop\jarvis-api && python run.py"
timeout /t 4 /nobreak > nul

:: 3. Start Voice Assistant
echo  [3/3] Starting Voice Assistant...
start "Jarvis Voice" /min cmd /k "cd /d %~dp0 && python jarvis.py"

echo.
echo  =============================================
echo    JARVIS is ONLINE! Say 'Hey Jarvis'!
echo  =============================================
echo.
timeout /t 3 /nobreak > nul
exit
