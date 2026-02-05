FROM python:3.11-slim

WORKDIR /app

COPY agent.py .

# Install OTEL and Strands SDK directly from GitHub
RUN pip install --no-cache-dir \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    git+https://github.com/strands-ai/strands-python-sdk.git
