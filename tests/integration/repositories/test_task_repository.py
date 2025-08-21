import pytest
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.db.repositories.task_repositories import TaskRepository
from src.domain.task.entity import TaskEntity


@pytest.mark.asyncio
async def test_create_and_get_task(db_session: AsyncSession):
    repo = TaskRepository(db_session)
    task = TaskEntity(title="Test Task")

    await repo.create(task)
    result = await repo.get(task.id)

    assert result.title == task.title
    assert result.id == task.id
