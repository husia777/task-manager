import logging
from src.presentation.web_api.providers.abstract.task import task_service_provider
from src.infra.db.connection import get_session
from src.infra.db.repositories.task_repositories import TaskRepository
from src.application.task.task_service import TaskService
from src.presentation.web_api.endpoints.task import task_router
from fastapi import FastAPI, Depends

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
app = FastAPI()

app.include_router(task_router)


def get_task_repository(session=Depends(get_session)):
    return TaskRepository(session)


def get_task_service(task_repository=Depends(get_task_repository)):
    return TaskService(task_repository)


app.dependency_overrides[task_service_provider] = get_task_service
