# routes/book_routes.py
# LAYER 1 (top): only defines the URLs. No logic -- it hands everything to the controller.

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.book_controller import BookController
from database.database import get_db
from schemas.book_schemas import BookCreate, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


def get_controller(db: AsyncSession = Depends(get_db)) -> BookController:
    return BookController(db)


@router.post("", status_code=201)
async def create_book(payload: BookCreate, controller: BookController = Depends(get_controller)):
    return await controller.create_book(payload)


@router.get("")
async def get_books(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: Optional[str] = Query(default=None),
    controller: BookController = Depends(get_controller),
):
    return await controller.get_books(page=page, limit=limit, search=search)


@router.get("/{book_id}")
async def get_book(book_id: int, controller: BookController = Depends(get_controller)):
    return await controller.get_book(book_id)


@router.put("/{book_id}")
async def update_book(book_id: int, payload: BookUpdate, controller: BookController = Depends(get_controller)):
    return await controller.update_book(book_id, payload)


@router.delete("/{book_id}")
async def delete_book(book_id: int, controller: BookController = Depends(get_controller)):
    return await controller.delete_book(book_id)
