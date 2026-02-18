import logging
import time

from strands.telemetry import StrandsTelemetry
from strands import Agent

# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("strands-demo")

# Telemetry
strands_telemetry = StrandsTelemetry()
strands_telemetry.setup_otlp_exporter()
strands_telemetry.setup_console_exporter()

# Real agent
agent = Agent(model="mock")

logger.info("Strands agent initialized.")

while True:
    try:
        logger.debug("Invoking agent...")
        response = agent.invoke("Hello from Strands telemetry demo")
        logger.debug("Response: %s", response)

    except Exception as e:
        logger.error("Agent error: %s", str(e))

    time.sleep(5)
