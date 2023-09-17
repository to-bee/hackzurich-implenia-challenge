from http import HTTPStatus
from typing import Any


class GenericAPIException(Exception):
    status_code = HTTPStatus.BAD_REQUEST
    # Default value set on a class level
    default_detail = None
    # Default value set on a class level
    default_code = "api.unknown_error"

    # Explicitly set over constructor
    detail = None
    # Explicitly set over constructor
    code = None

    headers = None

    def __init__(
        self,
        detail: str | None = None,
        status: int | None = None,
        code: str | None = None,
        headers: dict[str, Any] | None = None,
    ):
        self.detail = detail or self.default_detail
        self.code = code or self.default_code

        if status:
            self.status_code = status

        if headers:
            self.headers = headers

    def __str__(self):
        return " | ".join(filter(None, map(str, [self.code, self.status_code, self.detail])))

