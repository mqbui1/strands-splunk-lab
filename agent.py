import time
import os

from strands import Agent
from strands.telemetry import StrandsTelemetry

# ----------------------------
# REQUIRED: Service identity
# ----------------------------

os.environ["OTEL_SERVICE_NAME"] = "splunk-strands-agent"
os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "deployment.environment=demo,service.version=1.0"

# ----------------------------
# OTLP exporter configuration
# ----------------------------

os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://otel-collector:4317"
os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "grpc"
os.environ["OTEL_EXPORTER_OTLP_INSECURE"] = "true"

# Disable AWS / Bedrock completely (mandatory for local/mock)
os.environ["STRANDS_DISABLE_AWS"] = "true"
os.environ["STRANDS_DISABLE_BEDROCK"] = "true"

# Optional: increase debug visibility
os.environ["OTEL_LOG_LEVEL"] = "debug"

# ----------------------------
# Initialize telemetry
# ----------------------------

strands_telemetry = StrandsTelemetry()
strands_telemetry.setup_otlp_exporter()
strands_telemetry.setup_console_exporter()

# ----------------------------
# Create agent (mock model only)
# ----------------------------

agent = Agent(
    name="splunk-strands-agent",
    model="mock"
)

print("Strands agent initialized.")
print("Sending telemetry every 5 seconds...")

# ----------------------------
# Main loop
# ----------------------------

while True:
    try:
        prompt = "Hello from Strands agent telemetry demo"
        print("Invoking agent...")
        response = agent(prompt)
        print("Response:", response)

    except Exception as e:
        print("Agent error:", str(e))

    time.sleep(5)
