import time
import logging

from strands import Agent
from strands.telemetry import StrandsTelemetry


#
# logging
#
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("strands-lab")


#
# telemetry setup
#
telemetry = StrandsTelemetry()

telemetry.setup_otlp_exporter()
telemetry.setup_meter(enable_otlp_exporter=True)


#
# CRITICAL: force mock model
#
agent = Agent(
    name="otel-test-agent",
    model="mock",  # prevents Bedrock usage
)


logger.info("Agent initialized successfully")


#
# generate telemetry
#
counter = 0

while True:

    counter += 1

    logger.info(f"Sending request #{counter}")

    response = agent("Test OpenTelemetry instrumentation")

    logger.info(f"Response: {response}")

    time.sleep(5)
