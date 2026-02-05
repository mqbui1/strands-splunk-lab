import asyncio
from strands import Agent
from strands.models import BedrockModel
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# --- Configure tracing ---
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({"service.name": "strands-agent"}))
)
tracer = trace.get_tracer(__name__)
otlp_span_exporter = OTLPSpanExporter(endpoint="http://splunk-otel-collector:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_span_exporter))
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

# --- Configure metrics ---
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://splunk-otel-collector:4318", insecure=True),
    export_interval_millis=1000
)
metrics.set_meter_provider(MeterProvider(resource=Resource.create({"service.name": "strands-agent"}), metric_readers=[metric_reader]))
meter = metrics.get_meter(__name__)

# --- Local mock model ---
class LocalMockModel(BedrockModel):
    async def converse_async(self, *args, **kwargs):
        return "Mock response (no AWS credentials needed)"

# --- Create agent ---
model = LocalMockModel()
agent = Agent(model=model)

async def main():
    with tracer.start_as_current_span("agent-call"):
        response = await agent.async_call("Test OpenTelemetry instrumentation")
    print("Agent response:", response)

if __name__ == "__main__":
    asyncio.run(main())
