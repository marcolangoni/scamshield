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

---

## 🐳 Run in Docker

The image is fully self-contained; just inject your OpenAI key at runtime.


```bash
# 1. Build locally

docker buildx build \
  --platform linux/amd64 \
  -t scamshield:latest .

# 2. Or pull the published image
docker pull ghcr.io/marcolangoni/scamshield:latest

# 3. Run

docker run -d \
  -e OPENAI_API_KEY=sk-•••••••• \
  -p 8000:8000 \
  --name scamshield \
  scamshield:latest

```
---

## 🔌 REST API

| Method | Path        | Payload (body)                                    | Response (example) |
|--------|-------------|---------------------------------------------------|--------------------|
| POST   | `/classify` | ```json\n{ "callId": "abc-123", "text": "chunk of speech" }\n``` | ```json\n{\n  "reason": "Caller impersonates bank and pressures victim for PIN.",\n  "certainty_level": 87\n}\n``` |


```json
{
“reason”: “Caller impersonates bank and pressures victim for PIN.”,
“certainty_level”: 87
}
```
---
## 🛠 Requirements

* Python ≥ 3.10  
* `openai` ≥ 1.33.0 (new `httpx` stack)  
* FastAPI 0.111 / Uvicorn 0.29

All pinned in **requirements.txt**.

---

## 📦 Project layout


scamshield/
├── scamshield.py      # FastAPI app
├── requirements.txt   # frozen deps
└── Dockerfile         # multi-arch container recipe
