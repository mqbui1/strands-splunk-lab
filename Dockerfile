# strands-agent Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code into container
COPY . /app

# Ensure Python can find your code
ENV PYTHONPATH=/app:$PYTHONPATH

# Default command
CMD ["python", "agent.py"]
