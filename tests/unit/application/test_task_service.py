import pytest
import uuid
from unittest.mock import AsyncMock
from src.application.task.task_service import TaskService
from src.domain.task.exception import TaskNotFoundError, TaskValidationError


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def service(mock_repo):
    return TaskService(mock_repo)


@pytest.mark.asyncio
async def test_create_task_success(service, mock_repo):
    task_data = {"title": "Test", "description": "Test"}
    mock_repo.create = AsyncMock()

    result = await service.create(**task_data)

    assert result.title == task_data["title"]
    mock_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_task_validation_error(service):
    with pytest.raises(TaskValidationError):
        await service.create("", "description")
