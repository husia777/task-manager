from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from src.domain.task.value_object import TaskStatus


@dataclass
class TaskEntity:
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
