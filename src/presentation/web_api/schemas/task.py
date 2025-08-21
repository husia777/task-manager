from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from src.domain.task.value_object import TaskStatus


class TaskDTO(BaseModel):
    id: UUID
    title: str
    description: str
    status: TaskStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeleteResponse(BaseModel):
    message: str
