from http import HTTPStatus
from typing import Any

from fastapi import Response
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, ConfigDict

from src.domain.task.exception import DomainError


class HTTPErrorDetail(BaseModel):
    msg: str
    body: dict[str, Any]


class HTTPErrorModel(BaseModel):
    detail: list[HTTPErrorDetail]


class BadRequest(HTTPErrorModel):
    """
    Response модель для HTTPBadRequest статус кодов
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": [
                    {
                        "msg": "Something goes wrong",
                        "body": {"field": "value"},
                        "type": "ErrorType",
                    }
                ]
            }
        }
    )


class NotFound(HTTPErrorModel):
    """
    Response модель для статус кода HTTPNotFound
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": [
                    {
                        "msg": "Entity not found",
                        "body": {"field": "value"},
                        "type": "ErrorType",
                    }
                ]
            }
        }
    )


def to_error_detail_dict(error: DomainError) -> dict[str, Any]:
    return {
        "detail": [
            {
                "msg": error.message,
                "body": error.body(),
                "type": error.name(),
            }
        ]
    }


def to_error_detail(error: DomainError, status_code: HTTPStatus) -> Response:
    return ORJSONResponse(status_code=status_code, content=to_error_detail_dict(error))
