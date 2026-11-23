from datetime import datetime

from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

engine = create_engine(settings.sqlalchemy_url)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    # Store every datetime with its time zone, so timer math is never off by hours.
    type_annotation_map = {datetime: DateTime(timezone=True)}  # noqa: RUF012