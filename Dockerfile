FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends procps && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /home/appuser/.local

COPY app/ ./app/
COPY tests/ ./tests/
COPY .env.example .env

RUN useradd -m -u 1000 appuser
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]