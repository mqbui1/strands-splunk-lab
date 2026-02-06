import time

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from strands import Agent


# --- OpenTelemetry setup ---
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(
    endpoint="otel-collector:4317",
    insecure=True,
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)


# --- Create Strands agent ---
agent = Agent(
    name="splunk-strands-demo-agent"
)

print("Strands agent initialized.")


# --- Main loop ---
while True:

    with tracer.start_as_current_span("heartbeat"):

        print("Sending heartbeat span...")

        # invoke agent
        result = agent.run(
            input="Generate a simple heartbeat response"
        )

        print("Agent response:", result)

    time.sleep(5)
