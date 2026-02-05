# Use Python 3.11 slim
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    strands

# Copy your agent code
COPY agent.py .

# Run the agent
CMD ["python", "agent.py"]
