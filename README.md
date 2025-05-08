# ScamShield
A lightweight FastAPI micro-service that streams call-transcript chunks to the OpenAI API and returns a real-time judgment on whether the conversation is a vishing (voice-phishing) attempt, plus a confidence score. Stateless, multi-call-aware, and deploys in seconds with Docker or serverless containers

* 🌱 **Lightweight** – ~70 lines of Python.  
* 🧠 **LLM-powered** – feeds the full running transcript into GPT and returns a JSON verdict.  
* 🪄 **Multi-call aware** – keeps transcripts separated by `callId`.  
* 🚀 **Instant deploy** – one `Dockerfile`, ready for x86/amd64 or ARM.

---

## ⏱ Quick start (local)

```bash
# 1. Clone
git clone https://github.com/your-org/scamshield.git
cd scamshield

# 2. Create a virtual-env & install deps
python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Export your OpenAI key
export OPENAI_API_KEY=sk-••••••••

# 4. Launch the API
uvicorn scamshield:app --host 0.0.0.0 --port 8000
```

