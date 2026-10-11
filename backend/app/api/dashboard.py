from fastapi import APIRouter
from sqlalchemy import func

from app.db.database import SessionLocal
from app.models import Payment, Settlement, ExceptionRecord


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/summary")
def dashboard_summary():
    session = SessionLocal()

    try:
        total_payments = session.query(func.count(Payment.payment_id)).scalar() or 0

        total_settlements = (
            session.query(func.count(Settlement.settlement_id)).scalar() or 0
        )

        total_exceptions = (
            session.query(func.count(ExceptionRecord.exception_id)).scalar() or 0
        )

        open_exceptions = (
            session.query(ExceptionRecord)
            .filter(ExceptionRecord.status == "OPEN")
            .count()
        )

        critical = (
            session.query(ExceptionRecord)
            .filter(ExceptionRecord.severity == "CRITICAL")
            .count()
        )

        high = (
            session.query(ExceptionRecord)
            .filter(ExceptionRecord.severity == "HIGH")
            .count()
        )

        medium = (
            session.query(ExceptionRecord)
            .filter(ExceptionRecord.severity == "MEDIUM")
            .count()
        )

        in_review = (
            session.query(ExceptionRecord)
            .filter(ExceptionRecord.status == "IN_REVIEW")
            .count()
        )

        return {
            "total_payments": total_payments,
            "settlements": total_settlements,
            "exceptions": total_exceptions,
            "open_exceptions": open_exceptions,
            "critical": critical,
            "high": high,
            "medium": medium,
            "in_review": in_review,
        }

    finally:
        session.close()


@router.get("/exceptions")
def dashboard_exceptions():
    session = SessionLocal()

    try:
        exceptions = (
            session.query(ExceptionRecord)
            .order_by(ExceptionRecord.created_at.desc())
            .all()
        )

        return [
            {
                "exception_id": exception.exception_id,
                "payment_id": exception.payment_id,
                "exception_type": exception.exception_type,
                "severity": exception.severity,
                "expected_amount": (
                    float(exception.expected_amount)
                    if exception.expected_amount is not None
                    else None
                ),
                "actual_amount": (
                    float(exception.actual_amount)
                    if exception.actual_amount is not None
                    else None
                ),
                "difference": (
                    float(exception.difference)
                    if exception.difference is not None
                    else None
                ),
                "status": exception.status,
            }
            for exception in exceptions
        ]

    finally:
        session.close()
