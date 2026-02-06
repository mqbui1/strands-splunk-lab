import time
import os

from strands import Agent
from strands.models.mock import MockModel

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


# ----------------------------
# OpenTelemetry setup
# ----------------------------

resource = Resource.create({
    "service.name": "strands-agent",
    "service.version": "1.0.0",
    "deployment.environment": "demo"
})

provider = TracerProvider(resource=resource)

otlp_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317"),
    insecure=True,
)

processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(processor)

trace.set_tracer_provider(provider)

tracer = trace.get_tracer("strands-agent-demo")


# ----------------------------
# Create Strands agent with MockModel
# ----------------------------

agent = Agent(
    name="splunk-strands-agent",
    model=MockModel()
)

print("Strands agent initialized with MockModel.")
print("Sending GenAI telemetry every 5 seconds...")


# ----------------------------
# Main loop
# ----------------------------

while True:

    # Create parent GenAI span (Splunk semantic conventions)
    with tracer.start_as_current_span(
        "gen_ai.request",
        attributes={
            "gen_ai.system": "strands",
            "gen_ai.operation.name": "invoke",
            "gen_ai.request.model": "mock-model",
            "gen_ai.request.type": "completion"
        }
    ) as span:

        print("Invoking agent...")

        try:
            response = agent(
                "Explain OpenTelemetry in one sentence."
            )

            print("Response:", response)

            span.set_attribute("gen_ai.response.success", True)

        except Exception as e:

            print("Error:", str(e))

            span.set_attribute("gen_ai.response.success", False)
            span.record_exception(e)

    time.sleep(5)
