from typing import TYPE_CHECKING
from observer import LoggingSettings, Observer, SpanAttrsFilter, SpanFilterSampler
from sqlalchemy.ext.asyncio import AsyncEngine

from src.infra.config import OpentelemetrySettings

if TYPE_CHECKING:
    from fastapi import FastAPI


def setup_observability(engine: AsyncEngine, app: "FastAPI") -> None:
    """Настройка observability с помощью библиотеки observer"""
    observer_settings = OpentelemetrySettings()

    logging_settings = LoggingSettings()
    observer = Observer(logging_settings)

    # Настройка логирования
    observer.setup_logging(
        span_filter_sampler=SpanFilterSampler(
            SpanAttrsFilter(
                ("http.route", "/health"),
                ("db.statement", "SELECT 1"),
            ),
        )
    )

    observer.update_logger_config(
        "uvicorn",
        {
            "handlers": [],
            "level": observer.log_level,
        },
    )
    observer.update_logger_config(
        "uvicorn.error",
        {
            "handlers": ["console"],
            "level": observer.log_level,
        },
    )

    if observer_settings.instrument_fastapi:
        observer.setup_fastapi_instrumentor(app)
    if observer_settings.instrument_sqlalchemy:
        observer.setup_sqlalchemy_instrumentor(
            engine, span=observer_settings.instrument_sqlalchemy_span
        )
