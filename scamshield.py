import json
import os
from typing import Dict, List

import openai
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# ------------- Config --------------------------------------------------------

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL            = "gpt-4o-mini"     # Pick any model you have access to
SYSTEM_PROMPT    = """
You are a Scam Detector AI designed to analyze voice call transcripts between two individuals and determine whether the exchange contains signs of a vishing (voice phishing) or scam attempt.

Thoroughly evaluate the entire conversation, paying close attention to common scam tactics such as:
	•	Requests for sensitive personal or financial information
	•	Creating urgency or pressure to act immediately
	•	Impersonating legitimate institutions or authority figures
	•	Promising rewards or threatening penalties
	•	Requesting unusual forms of payment (e.g., gift cards, wire transfers)

Your response must always be a valid JSON object with exactly three elements:
1.	"reason": A concise, objective explanation summarizing the specific language, patterns, or behaviors in the conversation that contributed to your decision. Do not speculate or use subjective language.
2.	"scam_level": An integer from 0 to 100 representing the likelihood that this conversation involves a scam or vishing attempt.
3.	"scam_indicators": A list of detected scam indicators found in the conversation. Valid values are:
	•	"Request for sensitive info"
	•	"Urgency"
	•	"Impersonation"
	•	"Promises of rewards"
	•	"Threats of penalties"
	•	"Payment requests"
If no indicators are found, return an empty list.

Do not return any text outside of the JSON object. Only output the JSON.
"""

# ------------- Data ---------------------------------------------------------

conversations: Dict[str, List[Dict[str, str]]] = {}  # callId ➜ [{role,content}, …]

# ------------- API layer ----------------------------------------------------

app = FastAPI(title="ScamShield", version="0.1.0")


class ClassificationRequest(BaseModel):
    callId: str
    text: str


@app.post("/classify")
async def classify(req: ClassificationRequest):
    # 1️⃣  keep running history per call
    history = conversations.setdefault(req.callId, [])
    history.append({"role": "user", "content": req.text})

    # 2️⃣  build message list for Chat API
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        response = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.2,
            response_format={"type": "json_object"},
        )
    except openai.OpenAIError as e:
        raise HTTPException(status_code=502, detail=str(e))

    # 3️⃣  return the JSON produced by the model (already validated server-side)
    raw = response.choices[0].message.content            # string
    try:
        data = json.loads(raw)                             # dict ✅
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="LLM did not return valid JSON",
        )

    return JSONResponse(content=data)                      # clean JSON out
    
