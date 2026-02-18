import time
import logging

from strands import Agent
from strands.telemetry import StrandsTelemetry
from strands.models.mock import MockModel

logging.basicConfig(level=logging.DEBUG)

telemetry = StrandsTelemetry()
telemetry.setup_otlp_exporter()
telemetry.setup_console_exporter()

agent = Agent(
    name="splunk-strands-agent",
    model=MockModel()
)

while True:
    response = agent("Hello from Strands telemetry demo")
    print(response)
    time.sleep(5)
