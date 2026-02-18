import time
import os

from strands import Agent
from strands.telemetry import StrandsTelemetry

from opentelemetry.sdk.resources import Resource

# ----------------------------
# REQUIRED: Service identity
# ----------------------------

os.environ["OTEL_SERVICE_NAME"] = "splunk-strands-agent"
os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "deployment.environment=demo,service.version=1.0"

# OTLP endpoint (your collector)
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://otel-collector:4317"
os.environ["OTEL_EXPORTER_OTLP_INSECURE"] = "true"
os.environ["STRANDS_DISABLE_AWS"] = "true"
os.environ["STRANDS_DISABLE_BEDROCK"] = "true"

# ----------------------------
# Initialize Strands telemetry
# ----------------------------

strands_telemetry = StrandsTelemetry()

# Sends telemetry to collector
strands_telemetry.setup_otlp_exporter()

# Shows telemetry locally in console
strands_telemetry.setup_console_exporter()

# ----------------------------
# Create agent
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

        print(response)

    except Exception as e:

        print("Agent error:", str(e))

    time.sleep(5)
