import os
import logging
from strands.telemetry import StrandsTelemetry
from strands.agents import ChatCompletion

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
strands_telemetry = StrandsTelemetry()
strands_telemetry.setup_otlp_exporter()   # automatically sends spans to OTLP
strands_telemetry.setup_console_exporter() # optional console logs

# ----------------------------
# Real agent setup
# ----------------------------
agent = ChatCompletion(model="mock")  # or "openai:gpt-4o" if you have credentials

logger.info("Strands agent initialized and ready.")

# ----------------------------
# Main loop
# ----------------------------
import time

while True:
    try:
        prompt = "Hello from Strands agent telemetry demo"
        logger.debug("Invoking agent...")
        response = agent(prompt)
        logger.debug("Response: %s", response)

    except Exception as e:
        logger.error("Agent error: %s", str(e))

    time.sleep(5)
