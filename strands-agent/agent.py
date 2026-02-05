import asyncio
from strands import Agent
from strands.models import BedrockModel
from strands.telemetry import configure_tracing, configure_metrics

# --- Configure OpenTelemetry ---
configure_tracing(
    otlp_endpoint="http://splunk-otel-collector:4318",
    service_name="strands-agent"
)

configure_metrics(
    otlp_endpoint="http://splunk-otel-collector:4318",
    service_name="strands-agent"
)

# --- Use BedrockModel but override converse for local testing ---
class LocalMockModel(BedrockModel):
    async def converse_async(self, *args, **kwargs):
        return "Mock response (no AWS credentials needed)"

# --- Create agent ---
model = LocalMockModel()
agent = Agent(model=model)

async def main():
    response = await agent.async_call("Test OpenTelemetry instrumentation")
    print("Agent response:", response)

if __name__ == "__main__":
    asyncio.run(main())
