from http import HTTPStatus
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.application.task.task_service import TaskService
from src.domain.task.entity import TaskEntity
from src.domain.task.exception import TaskNotFoundError, TaskValidationError
from src.domain.task.value_object import TaskStatus
from src.presentation.errors import BadRequest, NotFound, to_error_detail
from src.presentation.web_api.providers.abstract.task import task_service_provider
from src.presentation.web_api.schemas.task import (
    DeleteResponse,
    TaskCreateRequest,
    TaskDTO,
)

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.post(
    path="/",
    response_model=TaskDTO,
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.BAD_REQUEST.value: {"model": BadRequest},
    },
    name="Создание задачи",
    operation_id="create_task",
)
async def create_task(
    task_data: TaskCreateRequest,
    service: TaskService = Depends(task_service_provider),
) -> TaskEntity | Any:
    try:
        task = await service.create(
            title=task_data.title, description=task_data.description
        )
        return task
    except TaskValidationError as e:
        return to_error_detail(e, HTTPStatus.BAD_REQUEST)


@task_router.get(
    path="/",
    response_model=list[TaskDTO],
    responses={
        HTTPStatus.BAD_REQUEST.value: {"model": BadRequest},
    },
    name="Список задач",
    operation_id="list_tasks",
)
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    service: TaskService = Depends(task_service_provider),
) -> List[TaskEntity] | Any:
    try:
        tasks = await service.list(skip, limit)
        return tasks
    except TaskValidationError as e:
        return to_error_detail(e, HTTPStatus.BAD_REQUEST)


@task_router.get(
    path="/{id}",
    response_model=TaskDTO,
    responses={
        HTTPStatus.NOT_FOUND.value: {"model": NotFound},
    },
    name="Получение задачи по id",
    operation_id="get_task_by_id",
)
async def get_task(
    id: UUID, service: TaskService = Depends(task_service_provider)
) -> TaskEntity | Any:
    try:
        task = await service.get(id)
        return task
    except TaskNotFoundError as e:
        return to_error_detail(e, HTTPStatus.NOT_FOUND)


@task_router.put(
    path="/{id}",
    response_model=TaskDTO,
    responses={
        HTTPStatus.NOT_FOUND.value: {"model": NotFound},
        HTTPStatus.BAD_REQUEST.value: {"model": BadRequest},
    },
    name="Изменение данных задачи по id",
)
async def update_task(
    id: UUID,
    title: str,
    description: str,
    status: TaskStatus,
    service: TaskService = Depends(task_service_provider),
) -> TaskEntity | Any:
    try:
        task = await service.update(id, title, description, status)
        return task
    except TaskNotFoundError as e:
        return to_error_detail(e, HTTPStatus.NOT_FOUND)
    except TaskValidationError as e:
        return to_error_detail(e, HTTPStatus.BAD_REQUEST)


@task_router.delete(
    path="/{id}",
    status_code=HTTPStatus.OK,
    response_model=DeleteResponse,
    responses={
        HTTPStatus.NOT_FOUND.value: {"model": NotFound},
    },
    name="Удаление задачи по id",
)
async def delete_task(
    id: UUID, service: TaskService = Depends(task_service_provider)
) -> DeleteResponse | Any:
    try:
        await service.delete(id)
        return DeleteResponse(message=f"Задача с ID {id} была успешно удалена")
    except TaskNotFoundError as e:
        return to_error_detail(e, HTTPStatus.NOT_FOUND)
