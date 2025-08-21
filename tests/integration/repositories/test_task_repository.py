import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.task.entity import TaskEntity
from src.infra.db.repositories.task_repositories import TaskRepository


@pytest.mark.asyncio
async def test_create_and_get_task(db_session: AsyncSession) -> None:
    repo = TaskRepository(db_session)
    task = TaskEntity(title="Test Task")

    await repo.create(task)
    result = await repo.get(task.id)

    assert result is not None
    assert result.title == task.title
    assert result.id == task.id
