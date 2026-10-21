#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
: "${OLLAMA_MODEL:=llama3.2}"
export OLLAMA_MODEL
printf '\nFor local Ollama, install https://ollama.com/download and run: ollama pull llama3.2\n'
printf 'Alternatively, choose Gemini or Groq in the app and enter your own API key.\n'
python app.py
