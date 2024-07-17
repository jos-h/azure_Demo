import os

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

"""
An example to show an application using Opentelemetry tracing api and sdk. Custom dependencies are
tracked via spans and telemetry is exported to application insights with the AzureMonitorTraceExporter.
"""


class OpenTelemetryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        tracer_provider = TracerProvider()
        trace.set_tracer_provider(tracer_provider)
        self.tracer = trace.get_tracer(__name__)
        span_processor = BatchSpanProcessor(
            AzureMonitorTraceExporter(
                connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
            )
        )
        tracer_provider.add_span_processor(span_processor)

    def __call__(self, request):
        try:
            # Start a new span for this request
            with self.tracer.start_as_current_span(
                "django_request",
                attributes={
                    "http.method": request.method,
                    "http.url": request.path_info,
                },
            ) as span:
                response = self.get_response(request)
                span.set_attribute("http.status_code", response.status_code)
                return response
        except Exception as e:
            print(f"Error creating span in custom middleware:{str(e)}")
            return self.get_response(request)
