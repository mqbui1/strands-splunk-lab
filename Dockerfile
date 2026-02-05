# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY agent.py .

RUN pip install --no-cache-dir \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    strands  # install from PyPI

CMD ["python", "agent.py"]
