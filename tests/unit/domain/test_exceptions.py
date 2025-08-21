import uuid
from src.domain.task.exception import TaskNotFoundError, TaskValidationError


def test_task_not_found_error():
    task_id = uuid.uuid4()
    error = TaskNotFoundError(task_id)

    assert error.message == f"Задача с ID {task_id} не найдена"
    assert error.body() == {"task_id": str(task_id)}


def test_task_validation_error():
    error = TaskValidationError("title", "", "Не может быть пустым")

    assert "title" in error.message
    assert error.body()["field"] == "title"
