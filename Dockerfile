# Use slim Python 3.11
FROM python:3.11-slim

WORKDIR /app

# Install git and build tools
RUN apt-get update && \
    apt-get install -y git build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy local agent code
COPY agent.py .

# Install OTEL + Strands SDK from GitHub
RUN pip install --no-cache-dir \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    git+https://github.com/strands-ai/strands-python-sdk.git
