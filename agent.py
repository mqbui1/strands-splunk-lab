# agent.py
from strands import strands  # strands() function is the main entrypoint
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Configure OpenTelemetry
resource = Resource.create({"service.name": "strands-demo-agent"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Configure OTLP exporter to Splunk OTEL Collector
otlp_exporter = OTLPSpanExporter(endpoint="http://splunk-otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Send a test trace using the Strands SDK
with tracer.start_as_current_span("strands-demo-span"):
    response = strands("Hello from Strands Agent!")  # returns response from Strands service
    print("Strands response:", response)
