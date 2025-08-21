from datetime import datetime
import uuid
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func
from sqlalchemy import String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from src.infra.db.connection import Base
from src.domain.task.value_object import TaskStatus


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.CREATED)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
