from unittest.mock import AsyncMock

import pytest

from src.application.task.task_service import TaskService
from src.domain.task.exception import TaskValidationError


@pytest.fixture
def mock_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def service(mock_repo: AsyncMock) -> TaskService:
    return TaskService(mock_repo)


@pytest.mark.asyncio
async def test_create_task_success(service: TaskService, mock_repo: AsyncMock) -> None:
    task_data = {"title": "Test", "description": "Test"}
    mock_repo.create = AsyncMock()

    result = await service.create(**task_data)

    assert result.title == task_data["title"]
    mock_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_task_validation_error(service: TaskService) -> None:
    with pytest.raises(TaskValidationError):
        await service.create("", "description")
