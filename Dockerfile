FROM python:3.11-slim

WORKDIR /app

COPY agent.py .

# Install git and build tools
RUN apt-get update && apt-get install -y git build-essential && rm -rf /var/lib/apt/lists/*

# Install OTEL SDK and Strands SDK from GitHub
RUN pip install --no-cache-dir \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    git+https://github.com/strands-ai/strands-python-sdk.git
