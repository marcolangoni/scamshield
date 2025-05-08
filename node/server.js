// server.js - node js version of scamshield.py
import express from "express";
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY, // make sure this env var is set
});

const MODEL = "gpt-4o-mini";          // choose any model you have access to
const SYSTEM_PROMPT = `
You are a Scam Detector AI designed to analyze voice call transcripts between
two individuals and determine whether the exchange contains signs of a vishing
(voice phishing) or scam attempt.

Thoroughly evaluate the entire conversation, paying close attention to common
scam tactics such as:
 • Requests for sensitive personal or financial information
 • Creating urgency or pressure to act immediately
 • Impersonating legitimate institutions or authority figures
 • Promising rewards or threatening penalties
 • Requesting unusual forms of payment (e.g., gift cards, wire transfers)

Your response must always be a valid JSON object with exactly three elements:
1. "reason": A concise, objective explanation summarizing the specific language,
   patterns, or behaviors in the conversation that contributed to your decision.
2. "scam_level": An integer from 0 to 100 representing the likelihood that this
   conversation involves a scam or vishing attempt.
3. "scam_indicators": A list of detected scam indicators found in the conversation.
   Valid values are:
     • "Request for sensitive info"
     • "Urgency"
     • "Impersonation"
     • "Promises of rewards"
     • "Threats of penalties"
     • "Payment requests"
   If no indicators are found, return an empty list.

Do not return any text outside of the JSON object. Only output the JSON.
`;

// --- Data store (in-memory per process) ------------------------------------
/** @type {Map<string, Array<{role:"user"|"assistant"|"system", content:string}>>} */
const conversations = new Map();

// --- Express setup ----------------------------------------------------------
const app = express();
app.use(express.json());

// POST /classify  ------------------------------------------------------------
app.post("/classify", async (req, res) => {
  const { callId, text } = req.body ?? {};

  if (!callId || !text) {
    return res.status(400).json({ error: "`callId` and `text` are required" });
  }

  // 1️⃣  Append this chunk to that call's running history
  const history = conversations.get(callId) ?? [];
  history.push({ role: "user", content: text });
  conversations.set(callId, history);

  // 2️⃣  Build message array for Chat Completions
  const messages = [
    { role: "system", content: SYSTEM_PROMPT },
    ...history,
  ];

  try {
    const completion = await openai.chat.completions.create({
      model: MODEL,
      messages,
      temperature: 0.2,
      response_format: { type: "json_object" },
    });

    const content = completion.choices[0].message.content;

    // 3️⃣  The model already outputs valid JSON. Return it verbatim.
    //     (Optionally parse to validate: JSON.parse(content))
    res.type("application/json").send(content);
  } catch (err) {
    console.error(err);
    res.status(502).json({ error: String(err) });
  }
});

// --- Start server -----------------------------------------------------------
const PORT = process.env.PORT || 8000;
app.listen(PORT, () =>
  console.log(`ScamShield API listening on http://0.0.0.0:${PORT}`)
);
