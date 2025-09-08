from typing import List
from uuid import UUID

from observer import get_custom_logger as get_logger

from src.domain.task.entity import TaskEntity
from src.domain.task.exception import TaskNotFoundError, TaskValidationError
from src.domain.task.value_object import TaskStatus
from src.infra.db.repositories.task_repositories import TaskRepository

MAX_TITLE_LENGTH = 100
MAX_LIMIT_VALUE = 1000

logger = get_logger(__name__)


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    async def create(self, title: str, description: str = "") -> TaskEntity:
        logger.info(
            "Creating new task: title='%s', description='%s'",
            title,
            description,
            extra={
                "title": title,
                "description": description,
                "action": "task_creation_started",
            },
        )

        if not title or not title.strip():
            error_msg = "Название не может быть пустым"
            logger.error(
                "Task validation failed: %s",
                error_msg,
                extra={
                    "error": error_msg,
                    "title": title,
                    "action": "validation_failed",
                },
            )
            raise TaskValidationError("title", title, error_msg)

        if len(title) > MAX_TITLE_LENGTH:
            error_msg = "Название не может превышать 100 символов"
            logger.error(
                "Task validation failed: %s, title_length=%d, max_allowed=%d",
                error_msg,
                len(title),
                MAX_TITLE_LENGTH,
                extra={
                    "error": error_msg,
                    "title": title,
                    "title_length": len(title),
                    "max_length": MAX_TITLE_LENGTH,
                    "action": "validation_failed",
                },
            )
            raise TaskValidationError("title", title, error_msg)

        logger.debug(
            "Validation passed, creating task entity",
            extra={
                "title": title,
                "description": description,
                "action": "validation_passed",
            },
        )

        task = TaskEntity(title=title.strip(), description=description.strip())

        logger.debug(
            "Saving task to repository: task_id=%s",
            str(task.id),
            extra={
                "task_id": str(task.id),
                "title": task.title,
                "action": "saving_to_repository",
            },
        )

        await self.repository.create(task)

        logger.info(
            "Task created successfully: task_id=%s, title='%s'",
            str(task.id),
            task.title,
            extra={
                "task_id": str(task.id),
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "action": "task_created",
            },
        )
        return task

    async def get(self, task_id: UUID) -> TaskEntity:
        logger.debug(
            "Getting task by ID: task_id=%s",
            str(task_id),
            extra={"task_id": str(task_id), "action": "get_task_started"},
        )

        task = await self.repository.get(task_id)
        if not task:
            logger.warning(
                "Task not found: task_id=%s",
                str(task_id),
                extra={"task_id": str(task_id), "action": "task_not_found"},
            )
            raise TaskNotFoundError(task_id)

        logger.debug(
            "Task found: task_id=%s, title='%s'",
            str(task_id),
            task.title,
            extra={
                "task_id": str(task_id),
                "title": task.title,
                "status": task.status.value,
                "action": "task_found",
            },
        )
        return task

    async def list(self, skip: int = 0, limit: int = 100) -> List[TaskEntity]:
        logger.debug(
            "Listing tasks: skip=%d, limit=%d",
            skip,
            limit,
            extra={"skip": skip, "limit": limit, "action": "list_tasks_started"},
        )

        if skip < 0:
            error_msg = "Не может быть отрицательным"
            logger.error(
                "Validation error: %s, skip=%d",
                error_msg,
                skip,
                extra={"error": error_msg, "skip": skip, "action": "validation_failed"},
            )
            raise TaskValidationError("skip", skip, error_msg)

        if limit <= 0 or limit > MAX_LIMIT_VALUE:
            error_msg = "Должно быть между 1 и 1000"
            logger.error(
                "Validation error: %s, limit=%d, max_limit=%d",
                error_msg,
                limit,
                MAX_LIMIT_VALUE,
                extra={
                    "error": error_msg,
                    "limit": limit,
                    "max_limit": MAX_LIMIT_VALUE,
                    "action": "validation_failed",
                },
            )
            raise TaskValidationError("limit", limit, error_msg)

        tasks = await self.repository.list(skip, limit)

        logger.info(
            "Tasks listed: count=%d, skip=%d, limit=%d",
            len(tasks),
            skip,
            limit,
            extra={
                "count": len(tasks),
                "skip": skip,
                "limit": limit,
                "task_ids": [str(task.id) for task in tasks],
                "action": "tasks_listed",
            },
        )
        return tasks

    async def update(
        self, task_id: UUID, title: str, description: str, status: TaskStatus
    ) -> TaskEntity:
        logger.info(
            "Updating task: task_id=%s, title='%s', description='%s', status=%s",
            str(task_id),
            title,
            description,
            status.value,
            extra={
                "task_id": str(task_id),
                "title": title,
                "description": description,
                "status": status.value,
                "action": "task_update_started",
            },
        )

        task = await self.get(task_id)

        if not title or not title.strip():
            error_msg = "Название не может быть пустым"
            logger.error(
                "Task validation failed: %s",
                error_msg,
                extra={
                    "error": error_msg,
                    "title": title,
                    "action": "validation_failed",
                },
            )
            raise TaskValidationError("title", title, error_msg)

        if len(title) > MAX_TITLE_LENGTH:
            error_msg = "Название не может превышать 100 символов"
            logger.error(
                "Task validation failed: %s, title_length=%d, max_allowed=%d",
                error_msg,
                len(title),
                MAX_TITLE_LENGTH,
                extra={
                    "error": error_msg,
                    "title": title,
                    "title_length": len(title),
                    "max_length": MAX_TITLE_LENGTH,
                    "action": "validation_failed",
                },
            )
            raise TaskValidationError("title", title, error_msg)

        logger.debug(
            "Validation passed, updating task: task_id=%s",
            str(task_id),
            extra={"task_id": str(task_id), "action": "validation_passed"},
        )

        task.title = title.strip()
        task.description = description.strip()
        task.status = status

        logger.debug(
            "Saving updated task to repository: task_id=%s",
            str(task_id),
            extra={"task_id": str(task_id), "action": "saving_to_repository"},
        )

        await self.repository.update(task)

        logger.info(
            "Task updated successfully: task_id=%s, title='%s'",
            str(task_id),
            task.title,
            extra={
                "task_id": str(task_id),
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "action": "task_updated",
            },
        )
        return task

    async def delete(self, task_id: UUID) -> None:
        logger.info(
            "Deleting task: task_id=%s",
            str(task_id),
            extra={"task_id": str(task_id), "action": "task_deletion_started"},
        )

        task = await self.get(task_id)

        logger.debug(
            "Task found for deletion: task_id=%s, title='%s'",
            str(task_id),
            task.title,
            extra={
                "task_id": str(task_id),
                "title": task.title,
                "action": "task_found_for_deletion",
            },
        )

        await self.repository.delete(task_id)

        logger.info(
            "Task deleted successfully: task_id=%s",
            str(task_id),
            extra={"task_id": str(task_id), "action": "task_deleted"},
        )
