from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    DateTime
)

from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    user_email = Column(
        String,
        nullable=False
    )

    action = Column(
        String,
        nullable=False
    )

    entity = Column(
        String,
        nullable=False
    )

    entity_id = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False
    )