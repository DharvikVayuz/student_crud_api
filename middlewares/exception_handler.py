# middlewares/exception_handler.py
# Catches every error raised while handling a request and returns it as JSON.

import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from constants.http_status import StatusCode
from middlewares.exceptions import CustomException

logger = logging.getLogger("api")


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except CustomException as exc:
            # An error we raised on purpose (BadRequest, ResourceNotFound, ...)
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "status_code": exc.status_code,
                    "error_type": exc.error_type,
                    "message": exc.message,
                },
            )
        except Exception:
            # A bug we did not expect. Log it, but don't leak details to the client.
            logger.exception("Unhandled exception")
            return JSONResponse(
                status_code=StatusCode.INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "status_code": StatusCode.INTERNAL_SERVER_ERROR,
                    "error_type": "Internal Server Error",
                    "message": "Something went wrong",
                },
            )
