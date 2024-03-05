from typing import Dict
from typing import NoReturn

from flask import jsonify
from werkzeug.exceptions import HTTPException


class APIException(Exception):
    status_code = 400

    def __init__(
        self, error: str, status_code: int | None = None, message: str | None = "", payload: Dict | None = None
    ):
        self.error = error
        self.status_code = status_code or self.status_code
        self.message = message
        self.payload = payload

    def to_dict(self):
        return dict(error=self.error, message=self.message, data=self.payload or {})

    def to_response(self):
        return jsonify(self.to_dict()), self.status_code

    @classmethod
    def from_http_exception(cls, exception: HTTPException):
        return cls(error="", status_code=exception.code, message=exception.description)

    @classmethod
    def from_exception(cls, exception: Exception):
        return APIException(error="", status_code=500, message=str(exception))


def abort(error: str, status_code: int, message: str = "", payload: Dict | None = None) -> NoReturn:
    raise APIException(error, status_code, message, payload)
