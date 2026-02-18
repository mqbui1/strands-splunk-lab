import time
import logging

from strands import Agent
from strands.telemetry import StrandsTelemetry

logging.basicConfig(level=logging.DEBUG)

telemetry = StrandsTelemetry()
telemetry.setup_otlp_exporter()
telemetry.setup_console_exporter()

agent = Agent(
    name="splunk-strands-agent",
    model="echo"   # ← THIS WORKS in your installed version
)

print("Agent initialized using echo model")

while True:
    response = agent("Hello from Strands telemetry demo")
    print("Response:", response)
    time.sleep(5)
