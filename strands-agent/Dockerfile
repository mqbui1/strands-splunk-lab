FROM python:3.11-slim

WORKDIR /app
COPY agent.py .

# Install strands and opentelemetry
RUN pip install --no-cache-dir strands opentelemetry-sdk opentelemetry-exporter-otlp

CMD ["python", "agent.py"]
