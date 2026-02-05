# agent.py
from strands.agent import Agent  # GitHub SDK
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure OTEL
resource = Resource.create({"service.name": "strands-agent"})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://splunk-otel-collector:4317", insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# Create Strands Agent
agent = Agent()

with tracer.start_as_current_span("strands-operation"):
    response = agent.send("Hello from Strands Agent!")
    print("Response from Strands:", response)
