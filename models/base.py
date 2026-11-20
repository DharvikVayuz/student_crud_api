# models/base.py  -- every model (database table) inherits from Base.

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
