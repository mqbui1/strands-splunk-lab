# Use slim Python 3.11
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential git && \
    rm -rf /var/lib/apt/lists/*

# Copy the agent code
COPY agent.py .

# Install Python packages: OpenTelemetry + Strands SDK from GitHub
ARG GITHUB_TOKEN
RUN pip install --no-cache-dir \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp && \
    git clone https://$GITHUB_TOKEN@github.com/strands-agents/sdk-python.git /tmp/strands && \
    pip install /tmp/strands && \
    rm -rf /tmp/strands

CMD ["python", "agent.py"]
