# 1. Install deps
npm install

# 2. Set your key
export OPENAI_API_KEY="sk-••••••••"

# 3. Fire it up
npm start



# test it

```bash
curl -X POST http://localhost:8000/classify \
     -H "Content-Type: application/json" \
     -d '{"callId":"test-1","text":"Hello, I am from the bank..."}'
```
