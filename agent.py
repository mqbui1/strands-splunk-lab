# agent.py
from strands import Client  # PyPI SDK
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Configure OTEL
resource = Resource.create({"service.name": "strands-demo-agent"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# OTLP Exporter (Docker service name for OTEL Collector)
otlp_exporter = OTLPSpanExporter(
    endpoint="http://splunk-otel-collector:4317",
    insecure=True
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Strands SDK
client = Client()
with tracer.start_as_current_span("strands-demo-span"):
    response = client.send("Hello from Strands Agent!")
    print("Strands response:", response)
