from strands import Client
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Configure OTEL
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export traces to local OTEL collector
otlp_exporter = OTLPSpanExporter(endpoint="http://splunk-otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Initialize Strands Agent
agent = Agent()

# Example usage
with tracer.start_as_current_span("strands-demo"):
    response = agent.send("Hello from Strands Agent!")
    print("Strands response:", response)
