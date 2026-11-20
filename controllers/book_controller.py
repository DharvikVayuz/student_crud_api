# controllers/book_controller.py
# LAYER 2: the translator between HTTP and the service.
#   - calls the service
#   - turns service errors into HTTP errors
#   - wraps the result in the standard response format

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from constants.http_status import StatusCode
from middlewares.exceptions import BadRequest, ResourceNotFound
from middlewares.response import success_response
from schemas.book_schemas import BookCreate, BookUpdate
from services.book_service import BookService


class BookController:

    def __init__(self, db: AsyncSession):
        self.service = BookService(db)

    async def create_book(self, payload: BookCreate) -> dict:
        try:
            book = await self.service.create_book(payload)
            return success_response("Book created successfully", data=book, status_code=StatusCode.CREATED)
        except ValueError as e:
            raise BadRequest(str(e))

    async def get_book(self, book_id: int) -> dict:
        try:
            book = await self.service.get_book(book_id)
            return success_response("Book fetched successfully", data=book)
        except LookupError as e:
            raise ResourceNotFound(str(e))

    async def get_books(self, page: int = 1, limit: int = 10, search: Optional[str] = None) -> dict:
        try:
            result = await self.service.get_all_books(page=page, limit=limit, search=search)
            return success_response(
                "Books fetched successfully",
                data=result["data"],
                total=result["meta"]["total"],
                page=result["meta"]["page"],
                page_size=result["meta"]["limit"],
                total_pages=result["meta"]["total_pages"],
            )
        except ValueError as e:
            raise BadRequest(str(e))

    async def update_book(self, book_id: int, payload: BookUpdate) -> dict:
        try:
            book = await self.service.update_book(book_id, payload)
            return success_response("Book updated successfully", data=book)
        except LookupError as e:
            raise ResourceNotFound(str(e))
        except ValueError as e:
            raise BadRequest(str(e))

    async def delete_book(self, book_id: int) -> dict:
        try:
            await self.service.delete_book(book_id)
            return success_response("Book deleted successfully")
        except LookupError as e:
            raise ResourceNotFound(str(e))
