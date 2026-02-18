import logging
logging.basicConfig(level=logging.DEBUG)

# 1️⃣ Initialize telemetry FIRST
from strands.telemetry import StrandsTelemetry
strands_telemetry = StrandsTelemetry()  # auto-instrumentation

# 2️⃣ Configure OTLP exporter to send traces to local OTEL collector
strands_telemetry.setup_otlp_exporter(
    endpoint="http://otel-collector:4317",  # HTTP OTLP endpoint in docker-compose network
    insecure=True  # local collector, no TLS
)

# 3️⃣ Import your model AFTER telemetry is initialized
from strands.models.echo import EchoModel

# 4️⃣ Create model and agent
model = EchoModel()
agent = model.agent(name="splunk-strands-agent")

# 5️⃣ Call the agent
response = agent("Hello from Strands telemetry demo")
print("Response:", response)
