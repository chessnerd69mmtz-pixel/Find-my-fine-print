# Find My Fine Print — Local Edition

A local-first contract and rulebook analysis app. Upload PDF, DOCX, TXT, or Markdown files, ask a question, inspect exact-source-verified quotes, and review potential ambiguities.

## Free local use (recommended)

- **Ollama + `llama3.2` is the default.** It runs on your computer, requires no API key, and has no per-request hosted AI API fee.
- Install Ollama from https://ollama.com/download, then run `ollama pull llama3.2`.
- The practical limits are your computer's RAM/CPU/GPU, disk space, document size, and how long you are willing to wait. No app can promise infinite processing capacity.
- Choose **All sections** to send every extracted chunk through the selected model. This removes the former 30-section cap, but large documents can take a long time.
- The default file cap is 50 MiB and extracted-text cap is 1.2 million characters. Adjust `CLAUSELENS_MAX_UPLOAD_BYTES` and `CLAUSELENS_MAX_EXTRACTED_CHARS` in your environment if your machine can handle more.

Optional hosted providers:
- Gemini API key: https://aistudio.google.com/app/apikey
- Groq API key: https://console.groq.com/keys

Hosted providers send selected document sections to their service and remain subject to provider quotas, terms, privacy policies, and possible charges. API keys are submitted for the current request and are not saved by the app or committed to this repository.

## Run locally

1. Install Python 3.11+ from https://www.python.org/downloads/.
2. Install Ollama and run `ollama pull llama3.2` (once).
3. On Windows, run `run_windows.bat`. On macOS/Linux, run `chmod +x run_linux_mac.sh` and then `./run_linux_mac.sh`.
4. Open http://127.0.0.1:8000.

## Reliability and privacy notes

- TF-IDF retrieval preserves negations and legal operators rather than dropping them as generic English stop words.
- Quotation references and offsets are derived from extracted source markers. Potential loopholes must include a verbatim supporting quote; the backend checks it against the exact retrieved segment and marks missing or mismatched evidence unverified. A matching quote proves only that the text exists, not that the legal interpretation is correct.
- All-sections mode has no fixed section-count cap. Hosted Gemini/Groq analysis uses bounded concurrency (default 3, configurable with `CLAUSELENS_CLOUD_CONCURRENCY`, maximum 6); local Ollama analysis remains sequential by default to avoid overwhelming laptop memory and compute.
- DOCX extraction includes body paragraphs, tables with row-level markers, and section headers/footers when available. Footnotes, endnotes, textboxes, scanned images, and complex layouts may still be omitted by the underlying extraction libraries.
- Model interpretation is not independently proven correct. Review the original document, especially for consequential decisions; this is not legal advice.
- Local Ollama mode processes model requests on your computer. The app's default bind address is `127.0.0.1`; do not expose it publicly without authentication, HTTPS, rate limiting, and secure secret handling.
- Scanned PDFs need OCR before upload. PDF/DOCX extraction may not preserve all layout, images, footnotes, textboxes, or complex formatting.
- GitHub Pages cannot run this Python/FastAPI backend; run it locally or deploy the backend to a Python-capable host with appropriate security controls.

## Tests

```bash
python -m pip install -r requirements.txt
python -m pytest -q
node --check static/app.js
python -m py_compile app.py
```
