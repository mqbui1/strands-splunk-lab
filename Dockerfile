# Dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install dependencies for building and git
RUN apt-get update && \
    apt-get install -y git build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy local app
COPY agent.py .

# Install OTEL SDK
RUN pip install --no-cache-dir opentelemetry-sdk opentelemetry-exporter-otlp

# Install Strands SDK from GitHub via SSH
RUN git clone git@github.com:strands-ai/strands-python-sdk.git /tmp/strands && \
    pip install /tmp/strands && \
    rm -rf /tmp/strands
