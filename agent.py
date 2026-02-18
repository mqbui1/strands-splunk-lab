import time
import os

from strands import Agent
from strands.telemetry import StrandsTelemetry
from strands.models.mock import MockModel

# ----------------------------
# REQUIRED: Service identity
# ----------------------------

os.environ["OTEL_SERVICE_NAME"] = "splunk-strands-agent"

os.environ["OTEL_RESOURCE_ATTRIBUTES"] = (
    "deployment.environment=demo,"
    "service.version=1.0"
)

# ----------------------------
# OTLP exporter configuration
# ----------------------------

# Your Splunk OTel Collector (gRPC)
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://otel-collector:4317"
os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "grpc"
os.environ["OTEL_EXPORTER_OTLP_INSECURE"] = "true"

# Disable AWS / Bedrock completely
os.environ["STRANDS_DISABLE_AWS"] = "true"
os.environ["STRANDS_DISABLE_BEDROCK"] = "true"

# Optional: increase debug visibility
os.environ["OTEL_LOG_LEVEL"] = "debug"

# ----------------------------
# Initialize telemetry
# ----------------------------

strands_telemetry = StrandsTelemetry()

# Send to collector → Splunk Observability Cloud
strands_telemetry.setup_otlp_exporter()

# Print spans locally (VERY useful for debugging)
strands_telemetry.setup_console_exporter()

# ----------------------------
# Create agent (FIXED)
# ----------------------------

agent = Agent(
    name="splunk-strands-agent",
    model=MockModel()   # ✅ THIS FIXES AWS CREDENTIAL ERRORS
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
