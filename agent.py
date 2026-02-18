import time
import logging

from strands import Agent
from strands.telemetry import StrandsTelemetry

# ----------------------------
# Logging (console debug)
# ----------------------------

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

logger = logging.getLogger("strands-demo")

# ----------------------------
# Telemetry setup
# ----------------------------

telemetry = StrandsTelemetry()

# sends traces to OTLP collector
telemetry.setup_otlp_exporter()

# prints spans to console
telemetry.setup_console_exporter()

logger.info("Telemetry initialized")

# ----------------------------
# Create real agent (mock model)
# ----------------------------

agent = Agent(
    name="splunk-strands-agent",
    model="mock"   # works without AWS / OpenAI
)

logger.info("Agent initialized")

# ----------------------------
# Main loop
# ----------------------------

while True:

    try:

        logger.debug("Invoking agent")

        response = agent.invoke(
            "Hello from Strands telemetry demo"
        )

        logger.debug("Agent response: %s", response)

    except Exception as e:

        logger.exception("Agent invocation failed")

    time.sleep(5)
