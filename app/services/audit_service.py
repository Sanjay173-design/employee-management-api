from datetime import datetime

from app.models.audit_log_model import AuditLog
from app.repositories.audit_repository import (
    AuditRepository
)


class AuditService:

    @staticmethod
    def log_action(
        db,
        user_email,
        action,
        entity,
        entity_id
    ):

        log = AuditLog(
            user_email=user_email,
            action=action,
            entity=entity,
            entity_id=str(entity_id),
            created_at=datetime.now()
        )

        return AuditRepository.create_log(
            db,
            log
        )