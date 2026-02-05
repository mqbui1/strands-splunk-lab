import os
from strands.agent import Agent  # Use Agent class

# OpenTelemetry imports
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# --- Configure Tracing ---
resource = Resource.create(attributes={
    "service.name": "strands-agent",
    "service.instance.id": os.getenv("HOSTNAME", "local")
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# OTEL endpoints (use Docker Compose service name)
OTEL_TRACES_ENDPOINT = os.getenv(
    "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", "http://splunk-otel-collector:4317"
)
OTEL_METRICS_ENDPOINT = os.getenv(
    "OTEL_EXPORTER_OTLP_METRICS_ENDPOINT", "http://splunk-otel-collector:4318"
)

# Configure OTLP exporter for traces
otlp_trace_exporter = OTLPSpanExporter(endpoint=OTEL_TRACES_ENDPOINT, insecure=True)
span_processor = BatchSpanProcessor(otlp_trace_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# --- Configure Metrics ---
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint=OTEL_METRICS_ENDPOINT, insecure=True)
)
metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[metric_reader]))
meter = metrics.get_meter(__name__)

# Example metric
request_counter = meter.create_counter(
    name="strands_requests_total",
    description="Number of requests sent to Strands",
    unit="1"
)

# --- Strands Agent ---
agent = Agent()

# --- Main Application Logic ---
if __name__ == "__main__":
    with tracer.start_as_current_span("strands_request"):
        # Send a message to Strands
        response = agent.complete("Hello from Strands Agent!")
        print("Agent response:", response)

        # Record metric
        request_counter.add(1)
