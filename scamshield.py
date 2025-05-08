import os
from typing import Dict, List

import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ------------- Config --------------------------------------------------------

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL            = "gpt-4o-mini"     # Pick any model you have access to
SYSTEM_PROMPT    = """
You are a Scam Detector AI. Your task is to analyze conversations between two
people and determine whether the exchange contains indicators of a vishing
(voice phishing) or scam attempt.

Evaluate the entire conversation carefully, looking for common scam tactics
such as:
 • Requests for personal or financial information
 • Urgency or pressure to act immediately
 • Impersonation of authority figures or institutions
 • Promises of rewards or threats of penalties
 • Unusual payment requests (e.g., gift cards, wire transfers)

Your response must always be a valid JSON object with exactly two elements:
 1. "reason": A clear, concise explanation summarizing the specific elements
    in the conversation that influenced your classification decision.
 2. "certainty_level": An integer between 0-100 indicating confidence.
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
    return response.choices[0].message.content
