# config.py  -- all settings live here and are read from the .env file.

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Student CRUD API"
    API_PREFIX: str = "/api"

    # SQLite by default so nothing needs installing.
    # For Postgres use: postgresql+asyncpg://user:password@localhost:5432/dbname
    DATABASE_URL: str = "sqlite+aiosqlite:///./students.db"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
