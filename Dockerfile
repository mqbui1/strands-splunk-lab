FROM python:3.11-slim

WORKDIR /app

# Install git and build tools
RUN apt-get update && \
    apt-get install -y git build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy app
COPY agent.py .

# Install OpenTelemetry
RUN pip install --no-cache-dir opentelemetry-sdk opentelemetry-exporter-otlp

# Install Strands SDK via HTTPS with token
# Replace YOUR_GITHUB_TOKEN with a token that has repo access
# Install Strands SDK from GitHub
ARG GITHUB_TOKEN
RUN git clone https://$GITHUB_TOKEN@github.com/strands-agents/sdk-python.git /tmp/strands && \
    pip install /tmp/strands && \
    rm -rf /tmp/strands
