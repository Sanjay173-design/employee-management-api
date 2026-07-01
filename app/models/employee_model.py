from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime
)

from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Employee(Base):

    __tablename__ = "employees"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True
    )

    name = Column(
        String,
        nullable=False,
        index=True
    )

    age = Column(
        Integer,
        nullable=False
    )

    department = Column(
        String,
        nullable=False,
        index=True
    )

    salary = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False,
        index=True
    )