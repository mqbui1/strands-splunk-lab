FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential git && \
    rm -rf /var/lib/apt/lists/*

COPY agent.py .

# Install Python packages: OpenTelemetry + Strands SDK from GitHub
ARG GITHUB_TOKEN
RUN pip install --no-cache-dir \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    "strands-agents @ git+https://${GITHUB_TOKEN}@github.com/strands-agents/sdk-python.git"

CMD ["python", "agent.py"]
