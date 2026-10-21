@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python 3.11 or newer is required. Install it from https://www.python.org/downloads/
  pause
  exit /b 1
)
py -3 -m venv .venv 2>nul
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo For local Ollama, install it from https://ollama.com/download
echo Then run: ollama pull llama3.2
echo You can alternatively select Gemini or Groq in the app and enter your own API key.
echo Gemini key: https://aistudio.google.com/app/apikey
echo Groq key: https://console.groq.com/keys
echo.
set OLLAMA_MODEL=llama3.2
python app.py
pause
