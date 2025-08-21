import os
from typing import Any

import pytest
from pytest_alembic.config import Config
from pytest_mock_resources import create_postgres_fixture

from src.infra.config import BASE_DIR


alembic_engine = create_postgres_fixture(async_=True)  # type: ignore


@pytest.fixture
def alembic_config() -> Any:
    """Override this fixture to configure the exact alembic context setup required."""
    script_location = os.path.join(BASE_DIR,  "infra", "db", "migrations")
    config_path = os.path.join(os.path.dirname(BASE_DIR), "alembic.ini")
    alembic_config = Config(
        config_options={
            "script_location": script_location,
            "file": config_path,
        }
    )
    return alembic_config
