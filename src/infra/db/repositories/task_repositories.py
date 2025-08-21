from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.task.entity import TaskEntity
from src.domain.task.value_object import TaskStatus
from src.infra.db.models.task import Task


class TaskRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, title: str, description: str = "") -> TaskEntity:
        pass

    @abstractmethod
    async def get(self, task_id: UUID) -> TaskEntity:
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> List[TaskEntity]:
        pass

    @abstractmethod
    async def update(
        self, task_id: UUID, title: str, description: str, status: TaskStatus
    ) -> TaskEntity:
        pass

    @abstractmethod
    async def delete(self, task_id: UUID) -> None:
        pass


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, task_id: UUID) -> Optional[TaskEntity]:
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        return self._to_entity(task) if task else None

    async def list(self, skip: int = 0, limit: int = 100) -> List[TaskEntity]:
        result = await self.session.execute(select(Task).offset(skip).limit(limit))
        tasks = result.scalars().all()
        return [self._to_entity(task) for task in tasks]

    async def create(self, task: TaskEntity) -> None:
        db_task = self._to_model(task)
        self.session.add(db_task)
        await self.session.commit()

    async def update(self, task: TaskEntity) -> None:
        await self.session.execute(
            update(Task)
            .where(Task.id == task.id)
            .values(title=task.title, description=task.description, status=task.status)
        )
        await self.session.commit()

    async def delete(self, task_id: UUID) -> None:
        await self.session.execute(delete(Task).where(Task.id == task_id))
        await self.session.commit()

    def _to_entity(self, task: Task) -> TaskEntity:
        return TaskEntity(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            created_at=task.created_at,
        )

    def _to_model(self, task: TaskEntity) -> Task:
        return Task(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            created_at=task.created_at,
        )
