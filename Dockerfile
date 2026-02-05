FROM python:3.11-slim

WORKDIR /app

# Need git for pip install from GitHub
RUN apt-get update && \
    apt-get install -y git build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY agent.py .

RUN pip install --no-cache-dir \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    git+https://github.com/strands-ai/strands-python-sdk.git
