# services/book_service.py
# LAYER 3: the business rules ("a title must be unique", "a book must exist before
# we update it"). Uses the repository for data. Knows nothing about HTTP.
#
# It raises plain Python errors; the controller turns them into HTTP errors:
#   LookupError -> 404 Not Found      ValueError -> 400 Bad Request

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.book_repository import BookRepository
from schemas.book_schemas import BookCreate, BookResponse, BookUpdate


class BookService:

    def __init__(self, db: AsyncSession):
        self.repo = BookRepository(db)

    async def create_book(self, payload: BookCreate) -> BookResponse:
        if await self.repo.get_by_title(payload.title):
            raise ValueError(f"A book titled '{payload.title}' already exists")
        book = await self.repo.create(payload.model_dump())
        return BookResponse.model_validate(book)

    async def get_book(self, book_id: int) -> BookResponse:
        book = await self.repo.get_by_id(book_id)
        if not book:
            raise LookupError(f"Book with id '{book_id}' not found")
        return BookResponse.model_validate(book)

    async def get_all_books(self, page: int = 1, limit: int = 10, search: Optional[str] = None) -> dict:
        if page < 1:
            raise ValueError("page must be greater than 0")
        if limit < 1:
            raise ValueError("limit must be greater than 0")

        books, total = await self.repo.get_all(page=page, limit=limit, search=search)
        return {
            "data": [BookResponse.model_validate(b) for b in books],
            "meta": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": (total + limit - 1) // limit,
            },
        }

    async def update_book(self, book_id: int, payload: BookUpdate) -> BookResponse:
        book = await self.repo.get_by_id(book_id)
        if not book:
            raise LookupError(f"Book with id '{book_id}' not found")

        changes = payload.model_dump(exclude_unset=True)  # only the fields the client sent

        new_title = changes.get("title")
        if new_title and new_title.lower() != book.title.lower() and await self.repo.get_by_title(new_title):
            raise ValueError(f"A book titled '{new_title}' already exists")

        book = await self.repo.update(book, changes)
        return BookResponse.model_validate(book)

    async def delete_book(self, book_id: int) -> None:
        book = await self.repo.get_by_id(book_id)
        if not book:
            raise LookupError(f"Book with id '{book_id}' not found")
        await self.repo.delete(book)
