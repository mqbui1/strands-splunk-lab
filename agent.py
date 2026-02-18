import time
import logging

from strands import Agent
from strands.telemetry import StrandsTelemetry

# ----------------------------
# Logging
# ----------------------------

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

logger = logging.getLogger("strands-demo")

# ----------------------------
# Telemetry
# ----------------------------

telemetry = StrandsTelemetry()

telemetry.setup_otlp_exporter()
telemetry.setup_console_exporter()

logger.info("Telemetry initialized")

# ----------------------------
# Create agent
# ----------------------------

agent = Agent(
    name="splunk-strands-agent",
    model="mock"
)

logger.info("Agent initialized")

# ----------------------------
# Main loop
# ----------------------------

while True:

    try:

        logger.debug("Invoking agent")

        response = agent(
            "Hello from Strands telemetry demo"
        )

        logger.debug("Agent response: %s", response)

    except Exception:

        logger.exception("Agent invocation failed")

    time.sleep(5)
