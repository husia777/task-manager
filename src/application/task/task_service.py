from typing import List
from uuid import UUID

from observer import get_custom_logger as get_logger

from src.domain.task.entity import TaskEntity
from src.domain.task.exception import TaskNotFoundError, TaskValidationError
from src.domain.task.value_object import TaskStatus

MAX_TITLE_LENGTH = 100
MAX_LIMIT_VALUE = 1000

logger = get_logger(__name__)


class TaskService:
    def __init__(self, repository):
        self.repository = repository

    async def create(self, title: str, description: str = "") -> TaskEntity:
        logger.info(
            "Creating new task", extra={"title": title, "description": description}
        )

        if not title or not title.strip():
            error_msg = "Название не может быть пустым"
            logger.error(
                "Task validation error", extra={"error": error_msg, "title": title}
            )
            raise TaskValidationError("title", title, error_msg)

        if len(title) > MAX_TITLE_LENGTH:
            error_msg = "Название не может превышать 100 символов"
            logger.error(
                "Task validation error",
                extra={
                    "error": error_msg,
                    "title": title,
                    "title_length": len(title),
                    "max_length": MAX_TITLE_LENGTH,
                },
            )
            raise TaskValidationError("title", title, error_msg)

        task = TaskEntity(title=title.strip(), description=description.strip())
        await self.repository.create(task)

        logger.info(
            "Task created successfully",
            extra={"task_id": str(task.id), "title": task.title},
        )
        return task

    async def get(self, task_id: UUID) -> TaskEntity:
        logger.debug("Getting task by ID", extra={"task_id": str(task_id)})

        task = await self.repository.get(task_id)
        if not task:
            logger.warning("Task not found", extra={"task_id": str(task_id)})
            raise TaskNotFoundError(task_id)

        logger.debug("Task found", extra={"task_id": str(task_id)})
        return task

    async def list(self, skip: int = 0, limit: int = 100) -> List[TaskEntity]:
        logger.debug("Listing tasks", extra={"skip": skip, "limit": limit})

        if skip < 0:
            error_msg = "Не может быть отрицательным"
            logger.error("Validation error", extra={"error": error_msg, "skip": skip})
            raise TaskValidationError("skip", skip, error_msg)

        if limit <= 0 or limit > MAX_LIMIT_VALUE:
            error_msg = "Должно быть между 1 и 1000"
            logger.error(
                "Validation error",
                extra={
                    "error": error_msg,
                    "limit": limit,
                    "max_limit": MAX_LIMIT_VALUE,
                },
            )
            raise TaskValidationError("limit", limit, error_msg)

        tasks = await self.repository.list(skip, limit)

        logger.info(
            "Tasks listed", extra={"count": len(tasks), "skip": skip, "limit": limit}
        )
        return tasks

    async def update(
        self, task_id: UUID, title: str, description: str, status: TaskStatus
    ) -> TaskEntity:
        logger.info(
            "Updating task",
            extra={
                "task_id": str(task_id),
                "title": title,
                "description": description,
                "status": status.value,
            },
        )

        task = await self.get(task_id)

        if not title or not title.strip():
            error_msg = "Название не может быть пустым"
            logger.error(
                "Task validation error", extra={"error": error_msg, "title": title}
            )
            raise TaskValidationError("title", title, error_msg)

        if len(title) > MAX_TITLE_LENGTH:
            error_msg = "Название не может превышать 100 символов"
            logger.error(
                "Task validation error",
                extra={
                    "error": error_msg,
                    "title": title,
                    "title_length": len(title),
                    "max_length": MAX_TITLE_LENGTH,
                },
            )
            raise TaskValidationError("title", title, error_msg)

        task.title = title.strip()
        task.description = description.strip()
        task.status = status

        await self.repository.update(task)

        logger.info("Task updated successfully", extra={"task_id": str(task_id)})
        return task

    async def delete(self, task_id: UUID) -> None:
        logger.info("Deleting task", extra={"task_id": str(task_id)})

        await self.get(task_id)
        await self.repository.delete(task_id)

        logger.info("Task deleted successfully", extra={"task_id": str(task_id)})
