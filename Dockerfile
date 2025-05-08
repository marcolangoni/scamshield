# ---------- Build stage (tiny) ----------
FROM --platform=$BUILDPLATFORM python:3.10-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # uvicorn listens on :8000 by default
    PORT=8000

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scamshield.py .

# ---------- Runtime image ----------
FROM base AS runtime

EXPOSE 8000

CMD ["uvicorn", "scamshield:app", "--host", "0.0.0.0", "--port", "8000"]
