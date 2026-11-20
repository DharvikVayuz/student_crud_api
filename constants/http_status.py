# constants/http_status.py  -- named status codes so we never type magic numbers.

from enum import IntEnum


class StatusCode(IntEnum):
    OK = 200
    CREATED = 201

    BAD_REQUEST = 400
    NOT_FOUND = 404
    UNPROCESSABLE_ENTITY = 422

    INTERNAL_SERVER_ERROR = 500
