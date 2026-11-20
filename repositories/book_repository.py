# repositories/book_repository.py
# LAYER 4 (bottom): talks to the database. Nothing else is allowed to run queries.
# No business rules here -- only "get / insert / change / remove rows".

from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.book_models import Book


class BookRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, book_id: int) -> Optional[Book]:
        result = await self.db.execute(select(Book).where(Book.id == book_id))
        return result.scalar_one_or_none()

    async def get_by_title(self, title: str) -> Optional[Book]:
        result = await self.db.execute(select(Book).where(func.lower(Book.title) == title.lower()))
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int = 1,
        limit: int = 10,
        search: Optional[str] = None,
    ) -> tuple[list[Book], int]:
        query = select(Book)
        count_query = select(func.count()).select_from(Book)

        if search:
            search_filter = Book.title.ilike(f"%{search.strip()}%")
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)

        query = query.order_by(Book.created_at.desc()).offset((page - 1) * limit).limit(limit)

        books = list((await self.db.execute(query)).scalars().all())
        total = (await self.db.execute(count_query)).scalar()
        return books, total

    async def create(self, data: dict) -> Book:
        book = Book(**data)
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)
        return book

    async def update(self, book: Book, data: dict) -> Book:
        for field, value in data.items():
            setattr(book, field, value)
        await self.db.commit()
        await self.db.refresh(book)
        return book

    async def delete(self, book: Book) -> None:
        await self.db.delete(book)
        await self.db.commit()
