import time
from strands import Client
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# -----------------------------
# Configure OpenTelemetry
# -----------------------------
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4318",  # matches docker-compose service name
    insecure=True
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# -----------------------------
# Start Strands Client
# -----------------------------
client = Client()
client.start()

# -----------------------------
# Main loop: keep container alive
# -----------------------------
print("Agent is running. Press Ctrl+C to stop.")
try:
    while True:
        with tracer.start_as_current_span("heartbeat"):
            print("Sending heartbeat span...")
        time.sleep(10)  # send a span every 10 seconds
except KeyboardInterrupt:
    print("Stopping agent...")
    client.stop()
