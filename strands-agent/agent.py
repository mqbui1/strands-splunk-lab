import time
import logging

from strands import Agent
from strands.telemetry import StrandsTelemetry

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("strands-lab")

# Setup telemetry
telemetry = StrandsTelemetry()

telemetry.setup_otlp_exporter()
telemetry.setup_meter(enable_otlp_exporter=True)

# Create agent
agent = Agent(
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",
    system_prompt="You are a helpful assistant",
)

logger.info("Strands agent starting")

# Generate telemetry continuously
while True:

    logger.info("Sending request")

    response = agent("Explain OpenTelemetry in one sentence")

    logger.info("Response received: %s", response)

    time.sleep(10)
