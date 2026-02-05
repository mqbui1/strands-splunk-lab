# agent.py
import time
from strands import Client

# Initialize Strands client
client = Client()

print("Strands agent started and connected...")

# Example telemetry or task loop
try:
    while True:
        # TODO: replace this with actual telemetry sending if needed
        print("Agent running, sending telemetry...")
        # Example: client.send_metric(...)  # uncomment if you have real metrics

        # Sleep for 10 seconds before next loop iteration
        time.sleep(10)

except KeyboardInterrupt:
    print("Agent stopping gracefully...")
