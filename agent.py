import os
import time
import logging
from strands.telemetry import StrandsTelemetry
from strands.agents import ChatCompletion  # real agent

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("splunk-strands-agent")

# ----------------------------
# Telemetry setup
# ----------------------------
os.environ["OTEL_SERVICE_NAME"] = "splunk-strands-agent"
os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "deployment.environment=demo,service.version=1.0"
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://otel-collector:4317"
os.environ["OTEL_EXPORTER_OTLP_INSECURE"] = "true"
os.environ["OTEL_LOG_LEVEL"] = "debug"

strands_telemetry = StrandsTelemetry()
strands_telemetry.setup_otlp_exporter()      # Send traces to OTLP endpoint
strands_telemetry.setup_console_exporter()   # Optional console debug logs

# ----------------------------
# Real agent setup
# ----------------------------
agent = ChatCompletion(model="mock")  # or "openai:gpt-4o" if you have credentials

logger.info("Strands agent initialized and ready.")

# ----------------------------
# Main loop
# ----------------------------
while True:
    try:
        prompt = "Hello from Strands agent telemetry demo"
        logger.debug("Invoking agent...")
        response = agent(prompt)
        logger.debug("Response: %s", response)

    except Exception as e:
        logger.error("Agent error: %s", str(e))

    time.sleep(5)
