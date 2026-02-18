import logging
logging.basicConfig(level=logging.DEBUG)

from strands.models.echo import EchoModel
import strands.telemetry as strands_telemetry

# Send traces to OTEL collector
strands_telemetry.setup_otlp_exporter()

# Use EchoModel (NO AWS REQUIRED)
model = EchoModel()

response = model.predict("Hello from Strands telemetry demo")

print("Response:", response)
