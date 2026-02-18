import time
import os

from strands import Agent
from strands.telemetry import StrandsTelemetry

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


# ----------------------------
# OpenTelemetry setup
# ----------------------------

os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://otel-collector:4317"
strands_telemetry = StrandsTelemetry()
strands_telemetry.setup_otlp_exporter()      # Send traces to OTLP endpoint
strands_telemetry.setup_console_exporter()

# resource = Resource.create({
#     "service.name": "strands-agent",
#     "service.version": "1.0.0",
#     "deployment.environment": "demo"
# })

# provider = TracerProvider(resource=resource)

# otlp_exporter = OTLPSpanExporter(
#     endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317"),
#     insecure=True,
# )

# processor = BatchSpanProcessor(otlp_exporter)
# provider.add_span_processor(processor)

# trace.set_tracer_provider(provider)

# tracer = trace.get_tracer("strands-agent-demo")


# ----------------------------
# Create agent WITHOUT specifying model
# ----------------------------

agent = Agent(
    name="splunk-strands-agent"
)

print("Strands agent initialized.")
print("Sending telemetry every 5 seconds...")

# ----------------------------
# Main loop
# ----------------------------

while True:

    # with tracer.start_as_current_span(
    #     "gen_ai.request",
    #     attributes={
    #         "gen_ai.system": "strands",
    #         "gen_ai.operation.name": "invoke",
    #         "gen_ai.request.model": "default",
    #         "gen_ai.request.type": "completion"
    #     }
    # ) as span:

        try:

            prompt = "Hello from Strands agent telemetry demo"

            print("Invoking agent...")

            # Call agent safely
            response = agent(prompt)
            print(response)
            
            # span.set_attribute("gen_ai.response.success", True)

        except Exception as e:

            print("Agent error (expected in demo mode):", str(e))

            # span.set_attribute("gen_ai.response.success", False)
            # span.record_exception(e)

    time.sleep(5)
