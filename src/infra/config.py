from typing import Dict, Literal

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    user: str = "postgres"
    password: str = "postgres"
    host: str = "postgres"
    port: int = 5432
    db: str = "postgres"
    driver: Literal["asyncpg", "psycopg", "psycopg2"] = "asyncpg"

    @computed_field  # type: ignore [prop-decorator]
    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme=f"postgresql+{self.driver}",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db,
        )

    model_config = SettingsConfigDict(env_prefix="postgres_")


class OpentelemetrySettings(BaseSettings):
    exporter_otlp_endpoint: str = (
        "http://collector.observability.svc.cluster.local:4317"
    )
    exporter_otlp_insecure: bool = True
    service_name: str = "task-service"
    resource_attributes: Dict[str, str] = {
        "service.namespace": "observability-demo",
        "service.version": "1.0",
    }
    instrument_fastapi: bool = True
    instrument_sqlalchemy: bool = True
    instrument_sqlalchemy_span: bool = False
