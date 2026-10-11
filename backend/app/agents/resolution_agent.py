from sqlalchemy.orm import Session

from app.models.exception import ExceptionRecord


def resolve_exception(
    session: Session,
    exception_id: str,
):
    exception = (
        session.query(ExceptionRecord)
        .filter(ExceptionRecord.exception_id == exception_id)
        .first()
    )

    if not exception:
        raise ValueError(f"Exception {exception_id} not found")

    if exception.status != "OPEN":
        return {
            "status": "already_processed",
            "exception_id": exception.exception_id,
            "current_status": exception.status,
        }

    if exception.exception_type == "SETTLEMENT_MISMATCH":
        if exception.severity == "CRITICAL":
            action = "ESCALATE_TO_FINANCE"
        elif exception.severity == "HIGH":
            action = "REVIEW_SETTLEMENT"
        else:
            action = "AUTO_ADJUSTMENT_REVIEW"

    elif exception.exception_type == "MISSING_SETTLEMENT":
        action = "REQUEST_SETTLEMENT"

    else:
        action = "MANUAL_REVIEW"

    exception.status = "IN_REVIEW"
    session.commit()

    return {
        "status": "resolution_started",
        "exception_id": exception.exception_id,
        "exception_type": exception.exception_type,
        "severity": exception.severity,
        "recommended_action": action,
    }
