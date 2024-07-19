import os
from azure.core.settings import settings
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Declare OpenTelemetry as enabled tracing plugin for Azure SDKs
settings.tracing_implementation = "opentelemetry"

class OpenTelemetryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        trace.set_tracer_provider(TracerProvider())
        self.tracer = trace.get_tracer(__name__)
        exporter = AzureMonitorTraceExporter(
            connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
        )
        trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(exporter))
       
    def __call__(self, request):
        try:
            # Start a new span for this request
            with self.tracer.start_as_current_span(name="MyApp") as span:
                print("Inside current_span context manager")
                span.set_attribute("http.method", request.method)
                span.set_attribute("http.url", request.path)
                response = self.get_response(request)
                span.set_attribute("http.status_code", response.status_code)
                return response
        except Exception as e:
            print(f"Error creating span in custom middleware:{str(e)}")
            return self.get_response(request)
