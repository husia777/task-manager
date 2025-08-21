import logging

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.task.task_service import TaskService
from src.infra.db.connection import get_session
from src.infra.db.repositories.task_repositories import TaskRepository
from src.presentation.web_api.endpoints.task import task_router
from src.presentation.web_api.providers.abstract.task import task_service_provider

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
app = FastAPI()

app.include_router(task_router)


def get_task_repository(session: AsyncSession = Depends(get_session)) -> TaskRepository:
    return TaskRepository(session)


def get_task_service(
    task_repository: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(task_repository)


app.dependency_overrides[task_service_provider] = get_task_service
