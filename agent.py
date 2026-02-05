# agent.py
from strands.agent import Agent
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure OpenTelemetry
resource = Resource.create({"service.name": "strands-agent"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Export traces to OTEL Collector (Docker service name)
otlp_exporter = OTLPSpanExporter(endpoint="http://splunk-otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

# Create Strands agent
agent = Agent()

with tracer.start_as_current_span("strands-operation"):
    response = agent.send("Hello from Strands Agent!")
    print("Strands response:", response)
