from strands.agent import Agent
from strands.telemetry import configure_tracing, configure_metrics

# Configure OpenTelemetry to send traces/metrics to OTEL Collector
configure_tracing()
configure_metrics()

# Initialize the agent
agent = Agent()

# Example: send a test request
if __name__ == "__main__":
    response = agent("Test OpenTelemetry instrumentation")
    print("Agent response:", response)
