from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.reconciliation import reconcile_payment


router = APIRouter(
    prefix="/reconciliation",
    tags=["Reconciliation"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/{payment_id}")
def reconcile(
    payment_id: str,
    db: Session = Depends(get_db),
):
    try:
        exception = reconcile_payment(
            db,
            payment_id,
        )

        if exception is None:
            return {
                "payment_id": payment_id,
                "status": "MATCHED",
                "message": "No reconciliation exception detected.",
            }

        return {
            "payment_id": payment_id,
            "exception_id": exception.exception_id,
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

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
