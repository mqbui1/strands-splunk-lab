import logging
logging.basicConfig(level=logging.DEBUG)

from strands import Agent
from strands.models.echo import EchoModel

import strands.telemetry as strands_telemetry

# Send traces to OTEL collector
strands_telemetry.setup_otlp_exporter()

# Use EchoModel (NO AWS REQUIRED)
model = EchoModel()

agent = Agent(
    name="splunk-strands-agent",
    model=model
)

response = agent("Hello from Strands telemetry demo")

print("Response:", response)
