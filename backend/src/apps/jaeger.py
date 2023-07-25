from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider, export

from core.config import CONFIG


def configure_tracer(host: str, port: int):
    """Функция для конфигурации трейсера.

    Args:
        host: Хост
        port: Порт
    """
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: CONFIG.flask.project_name}),
        ),
    )
    trace.get_tracer_provider().add_span_processor(  # type: ignore[attr-defined]
        export.BatchSpanProcessor(
            span_exporter=JaegerExporter(agent_host_name=host, agent_port=port),
        ),
    )
    trace.get_tracer_provider().add_span_processor(  # type: ignore[attr-defined]
        export.BatchSpanProcessor(
            span_exporter=export.ConsoleSpanExporter(),
        ),
    )


def install(app):
    """Установка компонента Flask для мониторинга с помощью распределённой трассировкой запросов.

    Args:
        app: Flask
    """
    if CONFIG.jaeger.enabled:
        configure_tracer(host=CONFIG.jaeger.host, port=CONFIG.jaeger.port)
        FlaskInstrumentor().instrument_app(app)
