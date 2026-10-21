# Find My Fine Print — Local Edition

A local-first contract and rulebook analysis app. Upload PDF, DOCX, TXT, or Markdown files, ask a question, review exact-source-verified quotes, and inspect potential loopholes.

## AI providers

**Ollama is the default** and uses `llama3.2` locally. No hosted API key is required for local inference.

Optional hosted providers:
- **Gemini API key:** https://aistudio.google.com/app/apikey (default model `gemini-2.5-flash`)
- **Groq API key:** https://console.groq.com/keys (default model `openai/gpt-oss-120b`; check current models at https://console.groq.com/docs/models)

Enter your own key in the app's masked field. The local app does not save keys to a settings file, database, or browser storage. Hosted analysis sends selected document sections to that provider; usage limits, terms, privacy policies, and potential charges apply. Never commit API keys to this repository.

## Run locally

1. Install Python 3.11+ from https://www.python.org/downloads/.
2. For local inference, install Ollama from https://ollama.com/download and run `ollama pull llama3.2`.
3. Clone/download the repository and run `run_windows.bat` on Windows. On macOS/Linux, run `chmod +x run_linux_mac.sh` followed by `./run_linux_mac.sh`.
4. Open http://127.0.0.1:8000.
5. Choose Ollama (default), Gemini, or Groq in the provider selector.

## Privacy and deployment notes

- The app is designed for local use on `127.0.0.1`. Do not expose it to the internet without authentication, HTTPS, rate limiting, and secure secret handling.
- Gemini/Groq mode sends retrieved source segments to the chosen provider. Check provider terms before uploading confidential or privileged material.
- TF-IDF retrieval can miss clauses; quote validation does not guarantee complete coverage or correct legal interpretation. This is informational, not legal advice.
- GitHub Pages cannot run this Python/FastAPI backend. This repository is the source-code project; run locally or deploy the backend to a Python-capable host with proper security controls.

## Tests

Run `python -m pytest -q` from the project folder.
