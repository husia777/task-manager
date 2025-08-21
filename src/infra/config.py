import os
from typing import Literal

from pydantic import (
    PostgresDsn,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5433
    db: str = "postgres"
    driver: Literal["asyncpg", "psycopg", "psycopg2"] = "asyncpg"

    @computed_field  # type: ignore [prop-decorator]
    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(  # pyright: ignore[reportAttributeAccessIssue]
            scheme=f"postgresql+{self.driver}",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db,
        )

    model_config = SettingsConfigDict(env_prefix="postgres_")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
