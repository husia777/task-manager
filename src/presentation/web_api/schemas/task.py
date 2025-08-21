from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

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


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field("", max_length=1000)
