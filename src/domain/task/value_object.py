from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TaskStatus(str, Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
