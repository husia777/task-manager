from typing import Any, Dict
from uuid import UUID


class DomainError(Exception):
    """Базовый класс для всех доменных ошибок"""

    @property
    def message(self) -> str:
        return "Произошла ошибка"

    def body(self) -> Dict[str, Any]:
        return {}

    def name(self) -> str:
        return self.__class__.__name__


class TaskNotFoundError(DomainError):
    """Ошибка: задача не найдена"""

    def __init__(self, task_id: UUID):
        self.task_id = task_id
        super().__init__()

    @property
    def message(self) -> str:
        return f"Задача с ID {self.task_id} не найдена"

    def body(self) -> Dict[str, Any]:
        return {"task_id": str(self.task_id)}


class TaskValidationError(DomainError):
    """Ошибка валидации задачи"""

    def __init__(self, field: str, value: Any, reason: str):
        self.field = field
        self.value = value
        self.reason = reason
        super().__init__()

    @property
    def message(self) -> str:
        return f"Некорректное значение для поля {self.field}: {self.reason}"

    def body(self) -> Dict[str, Any]:
        return {"field": self.field, "value": str(self.value), "reason": self.reason}
