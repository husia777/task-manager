from typing import List
from uuid import UUID

from src.domain.task.entity import TaskEntity
from src.domain.task.exception import TaskNotFoundError, TaskValidationError
from src.domain.task.value_object import TaskStatus
from src.infra.db.repositories.task_repositories import TaskRepository

MAX_TITLE_LENGTH = 100
MAX_LIMIT_VALUE = 1000


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create(self, title: str, description: str = "") -> TaskEntity:
        if not title or not title.strip():
            raise TaskValidationError("title", title, "Название не может быть пустым")

        if len(title) > MAX_TITLE_LENGTH:
            raise TaskValidationError(
                "title", title, "Название не может превышать 100 символов"
            )

        task = TaskEntity(title=title.strip(), description=description.strip())
        await self.repository.create(task)
        return task

    async def get(self, task_id: UUID) -> TaskEntity:
        task = await self.repository.get(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        return task

    async def list(self, skip: int = 0, limit: int = 100) -> List[TaskEntity]:
        if skip < 0:
            raise TaskValidationError("skip", skip, "Не может быть отрицательным")

        if limit <= 0 or limit > MAX_LIMIT_VALUE:
            raise TaskValidationError("limit", limit, "Должно быть между 1 и 1000")

        return await self.repository.list(skip, limit)

    async def update(
        self, task_id: UUID, title: str, description: str, status: TaskStatus
    ) -> TaskEntity:
        task = await self.get(task_id)

        if not title or not title.strip():
            raise TaskValidationError("title", title, "Название не может быть пустым")

        if len(title) > MAX_TITLE_LENGTH:
            raise TaskValidationError(
                "title", title, "Название не может превышать 100 символов"
            )

        task.title = title.strip()
        task.description = description.strip()
        task.status = status

        await self.repository.update(task)
        return task

    async def delete(self, task_id: UUID) -> None:
        await self.get(task_id)
        await self.repository.delete(task_id)
