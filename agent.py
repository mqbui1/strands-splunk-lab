import os
import time
import logging
from strands.telemetry import StrandsTelemetry
from strands.agents import ChatCompletion  # real instrumented agent

# ----------------------------
# Environment / OTLP setup
# ----------------------------
os.environ["OTEL_SERVICE_NAME"] = "splunk-strands-agent"
os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "deployment.environment=demo,service.version=1.0"
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://otel-collector:4317"
os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "grpc"
os.environ["OTEL_EXPORTER_OTLP_INSECURE"] = "true"

# Optional: disable AWS/Bedrock if running local/demo
os.environ["STRANDS_DISABLE_AWS"] = "true"
os.environ["STRANDS_DISABLE_BEDROCK"] = "true"

# Enable debug logging for OTEL SDK
os.environ["OTEL_LOG_LEVEL"] = "debug"

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("splunk-strands-agent")

# ----------------------------
# Initialize telemetry
# ----------------------------
strands_telemetry = StrandsTelemetry()
strands_telemetry.setup_otlp_exporter()      # send spans to OTLP endpoint
strands_telemetry.setup_console_exporter()   # optional: print spans locally

logger.info("Strands telemetry initialized.")

# ----------------------------
# Use real ChatCompletion agent
# ----------------------------
agent = ChatCompletion(model="gpt-4")  # real Strands agent, auto-instrumented

logger.info("ChatCompletion agent initialized.")
logger.info("Sending requests every 5 seconds...")

# ----------------------------
# Main loop
# ----------------------------
while True:
    try:
        prompt = "Hello from Strands demo"
        response = agent(prompt)  # auto-instrumented — spans generated automatically
        logger.info("Agent response: %s", response)

    except Exception as e:
        logger.error("Agent error: %s", str(e))

    time.sleep(5)
