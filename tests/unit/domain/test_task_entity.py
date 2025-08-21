import uuid
from datetime import datetime

from src.domain.task.entity import TaskEntity
from src.domain.task.value_object import TaskStatus


def test_task_entity_creation() -> None:
    task = TaskEntity(
        title="Test Task", description="Test Description", status=TaskStatus.IN_PROGRESS
    )

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == TaskStatus.IN_PROGRESS
    assert isinstance(task.id, uuid.UUID)
    assert isinstance(task.created_at, datetime)


def test_task_entity_default_values() -> None:
    task = TaskEntity()

    assert task.title == ""
    assert task.description == ""
    assert task.status == TaskStatus.CREATED
