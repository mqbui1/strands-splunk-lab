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

# OTLP exporter to send spans to local OTEL collector
otlp_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4318",  # matches docker-compose service name
    insecure=True
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# -----------------------------
# Start Strands Client
# -----------------------------
client = Client()  # initialize Strands client
client.start()     # start the client (SDK may handle background tasks)

# -----------------------------
# Main loop: generate telemetry
# -----------------------------
print("Agent is running. Press Ctrl+C to stop.")
try:
    while True:
        with tracer.start_as_current_span("heartbeat"):
            print("Sending heartbeat span...")
            time.sleep(10)  # send a span every 10 seconds
except KeyboardInterrupt:
    print("Agent stopped manually.")
    client.stop()  # gracefully stop Strands client
