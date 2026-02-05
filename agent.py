import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from strands import StrandsAgent  # assuming this is the SDK import

# --- OpenTelemetry Setup ---
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# --- Strands Agent Setup ---
agent = StrandsAgent()
agent.start()

print("Strands agent started. Sending periodic telemetry...")

# --- Main loop to keep container alive ---
try:
    while True:
        with tracer.start_as_current_span("heartbeat"):
            print("Sending heartbeat span...")
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopping agent...")
    agent.stop()
