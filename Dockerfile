# Use slim Python 3.11
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential git && \
    rm -rf /var/lib/apt/lists/*

# Copy the agent code
COPY agent.py .

# Install Python packages: OpenTelemetry + Strands SDK (release with real agents)
RUN pip install --no-cache-dir \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    strands-agents==1.26.0

# Run the agent
CMD ["python", "agent.py"]
