import time
import logging
import random

from strands import Agent
from strands.telemetry import StrandsTelemetry

#
# Setup Python logging
#
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

logger = logging.getLogger("strands-lab")


#
# Initialize OpenTelemetry via Strands
#
telemetry = StrandsTelemetry()

# enable OTLP trace exporter
telemetry.setup_otlp_exporter()

# enable metrics exporter
telemetry.setup_meter(enable_otlp_exporter=True)


#
# Create a simple local Strands agent
#
agent = Agent(
    name="test-strands-agent",
    system_prompt="You are a helpful assistant for OpenTelemetry testing.",
    model="mock"  # uses built-in mock model, no external dependency
)


logger.info("Strands agent started successfully")


#
# Generate telemetry continuously
#
request_count = 0

while True:

    try:

        request_count += 1

        logger.info("Sending request #%s", request_count)

        #
        # This generates a TRACE automatically
        #
        response = agent(
            f"Explain OpenTelemetry in one sentence. Request #{request_count}"
        )

        #
        # This generates LOG telemetry
        #
        logger.info("Received response: %s", response)

        #
        # Generate some additional telemetry variation
        #
        if random.random() > 0.7:
            logger.warning("Simulated warning condition occurred")

        time.sleep(5)

    except Exception as e:

        logger.exception("Error during agent execution: %s", e)

        time.sleep(5)
