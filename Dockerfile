# strands-agent Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy local code
COPY . /app

# Ensure Python can find your code
ENV PYTHONPATH=/app:$PYTHONPATH

# Default command
CMD ["python", "agent.py"]
