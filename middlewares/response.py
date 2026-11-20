# middlewares/response.py  -- every successful response uses this same format.

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(message: str, data=None, status_code: int = 200, **kwargs):
    """
    Example output:
        {
          "status_code": 200,
          "message": "Books fetched successfully",
          "total": 25, "page": 1, "page_size": 10, "total_pages": 3,   <- only for lists
          "data": [...]
        }
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "message": message,
            **kwargs,
            "data": jsonable_encoder(data),
        },
    )
