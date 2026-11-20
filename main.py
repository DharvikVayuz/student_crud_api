# main.py  -- the starting point of the app. Run with:  uvicorn main:app --reload

from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from database.database import init_db
from middlewares.exception_handler import ExceptionHandlerMiddleware
from routes.book_routes import router as book_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once when the server starts: create the tables if they don't exist.
    await init_db()
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# Turns any error we raise into a clean JSON response.
app.add_middleware(ExceptionHandlerMiddleware)

# Every new module's router gets registered here.
app.include_router(book_router, prefix=settings.API_PREFIX)


@app.get("/health")
async def health():
    return {"status": "ok"}
