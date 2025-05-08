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

# Containerize

```dockerfile
# Dockerfile
FROM node:20-slim

WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY server.js .

ENV PORT=8000
EXPOSE 8000

CMD ["node", "server.js"]
```

# Build for x86-64 and run

```bash
docker buildx build --platform linux/amd64 -t scamshield-node:latest .
docker run -d -e OPENAI_API_KEY=sk-••• -p 8000:8000 scamshield-node:latest
```

