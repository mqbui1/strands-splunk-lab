import time
import os
import logging
from strands.telemetry import StrandsTelemetry

# ----------------------------
# Environment / OTLP setup
# ----------------------------
os.environ["OTEL_SERVICE_NAME"] = "splunk-strands-agent"
os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "deployment.environment=demo,service.version=1.0"
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://otel-collector:4317"
os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "grpc"
os.environ["OTEL_EXPORTER_OTLP_INSECURE"] = "true"
os.environ["STRANDS_DISABLE_AWS"] = "true"
os.environ["STRANDS_DISABLE_BEDROCK"] = "true"
os.environ["OTEL_LOG_LEVEL"] = "debug"

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(
    level=logging.DEBUG,   # will capture debug/info/warning/error
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("splunk-strands-agent")

# ----------------------------
# Initialize telemetry
# ----------------------------
strands_telemetry = StrandsTelemetry()
strands_telemetry.setup_otlp_exporter()
strands_telemetry.setup_console_exporter()

# ----------------------------
# Mock agent
# ----------------------------
class MockAgent:
    def __init__(self, name="mock-agent"):
        self.name = name

    def __call__(self, prompt):
        return f"[MOCK RESPONSE] Received prompt: '{prompt}'"

agent = MockAgent(name="splunk-strands-agent")

logger.info("Strands agent (mock) initialized.")
logger.info("Sending telemetry every 5 seconds...")

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
