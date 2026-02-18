# strands/telemetry.py
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import os

def setup_otlp_exporter():
    """
    Configures OpenTelemetry tracing to send spans to OTLP collector.
    """
    # Read OTEL endpoint from env or default to localhost
    otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")
    
    # Create OTLP exporter
    otlp_exporter = OTLPSpanExporter(endpoint=otel_endpoint, insecure=True)
    
    # Create a TracerProvider with a default resource
    resource = Resource.create(attributes={"service.name": "splunk-strands-agent"})
    provider = TracerProvider(resource=resource)
    
    # Attach the exporter to a BatchSpanProcessor
    span_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(span_processor)
    
    # Set global tracer provider
    trace.set_tracer_provider(provider)
    print(f"OTLP exporter configured, sending to {otel_endpoint}")
