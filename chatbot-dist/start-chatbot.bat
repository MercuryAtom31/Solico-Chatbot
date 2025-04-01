@echo off
REM Start Ollama (this opens it in a separate window)
start "" "ollama.exe" serve --model mistral:7b-instruct

REM Wait for a few seconds to let Ollama start
timeout /t 5

REM Start the Flask app
python app.py

REM When finished, close the windows to stop the chatbot.
