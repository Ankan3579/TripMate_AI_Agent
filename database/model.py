from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime
)

from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from database.postgress import engine


Base = declarative_base()


class TripMemory(Base):

    __tablename__ = "trip_memory"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    origin = Column(
        Text,
        nullable=False
    )

    destination = Column(
        Text,
        nullable=False
    )

    start_date = Column(Text)

    end_date = Column(Text)

    budget = Column(Text)

    travelers = Column(Integer)

    user_query = Column(Text)

    final_response = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


Base.metadata.create_all(engine)