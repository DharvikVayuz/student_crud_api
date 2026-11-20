# middlewares/exceptions.py  -- our own error types. Raise one and the client gets a clean JSON error.

from constants.http_status import StatusCode


class CustomException(Exception):
    def __init__(self, message, status_code=StatusCode.INTERNAL_SERVER_ERROR, error_type="Internal Server Error"):
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        super().__init__(self.message)


class BadRequest(CustomException):
    def __init__(self, msg="Bad request"):
        super().__init__(msg, StatusCode.BAD_REQUEST, "Bad Request")


class ResourceNotFound(CustomException):
    def __init__(self, msg="Resource not found"):
        super().__init__(msg, StatusCode.NOT_FOUND, "Not Found")
