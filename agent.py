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


# --- Strands Agent setup ---
agent = Agent(
    name="splunk-strands-demo-agent"
)

agent.start()

print("Strands agent started. Sending periodic telemetry...")


# --- Main loop ---
try:
    while True:
        with tracer.start_as_current_span("heartbeat"):
            print("Sending heartbeat span...")
        time.sleep(5)

except KeyboardInterrupt:
    print("Stopping agent...")
    agent.stop()
