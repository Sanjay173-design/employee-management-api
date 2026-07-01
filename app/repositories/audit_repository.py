from sqlalchemy.orm import Session

from app.models.audit_log_model import AuditLog


class AuditRepository:

    @staticmethod
    def create_log(
        db: Session,
        log: AuditLog
    ):

        db.add(log)

        db.commit()

        db.refresh(log)

        return log