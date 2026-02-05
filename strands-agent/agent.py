import asyncio
from strands import Agent
from strands.models.mock import MockModel  # Use a local mock instead of AWS Bedrock
from strands.telemetry import configure_tracing, configure_metrics

# --- Configure OpenTelemetry ---
# These should match your collector
configure_tracing(
    otlp_endpoint="http://splunk-otel-collector:4318",
    service_name="strands-agent"
)

configure_metrics(
    otlp_endpoint="http://splunk-otel-collector:4318",
    service_name="strands-agent"
)

# --- Use Mock Model for testing ---
model = MockModel()

# --- Create agent ---
agent = Agent(model=model)

async def main():
    # Example request to the agent
    response = await agent.async_call("Test OpenTelemetry instrumentation")
    print("Agent response:", response)

if __name__ == "__main__":
    asyncio.run(main())
