import os

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

"""
An example to show an application using Opentelemetry tracing api and sdk. Custom dependencies are
tracked via spans and telemetry is exported to application insights with the AzureMonitorTraceExporter.
"""


def setup_tracing():
    tracer_provider = TracerProvider()
    trace.set_tracer_provider(tracer_provider)
    try:
        # This is the exporter that sends data to Application Insights
        exporter = AzureMonitorTraceExporter(
            connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
        )
        span_processor = BatchSpanProcessor(exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)
    except Exception as e:
        print(f"Error setting up the trace:{str(e)}")


class OpenTelemetryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tracer = trace.get_tracer(__name__)
        # Start a new span for this request
        with tracer.start_as_current_span(
            "django_request",
            attributes={"http.method": request.method, "http.url": request.path_info},
        ) as span:
            response = self.get_response(request)
            span.set_attribute("http.status_code", response.status_code)
            return response


setup_tracing()
