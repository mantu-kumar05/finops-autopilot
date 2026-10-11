from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.exception import ExceptionRecord
from app.models.payment import Payment
from app.models.settlement import Settlement


MISMATCH_THRESHOLD = Decimal("1.00")


def get_existing_exception(
    session: Session,
    payment_id: str,
):
    return (
        session.query(ExceptionRecord)
        .filter(ExceptionRecord.payment_id == payment_id)
        .first()
    )


def reconcile_payment(
    session: Session,
    payment_id: str,
):
    # Find payment
    payment = (
        session.query(Payment)
        .filter(Payment.payment_id == payment_id)
        .first()
    )

    if not payment:
        raise ValueError(f"Payment {payment_id} not found")

    # Prevent duplicate exceptions
    existing_exception = get_existing_exception(
        session,
        payment_id,
    )

    if existing_exception:
        return existing_exception

    # Find settlement
    settlement = (
        session.query(Settlement)
        .filter(Settlement.payment_id == payment_id)
        .first()
    )

    # Missing settlement
    if not settlement:
        exception = ExceptionRecord(
            exception_id=f"EXC_{payment_id}",
            payment_id=payment_id,
            exception_type="MISSING_SETTLEMENT",
            severity="HIGH",
            expected_amount=payment.amount,
            actual_amount=None,
            difference=None,
            status="OPEN",
            created_at=datetime.utcnow(),
        )

        session.add(exception)
        session.commit()

        return exception

    # Calculate difference
    difference = abs(
        Decimal(str(settlement.expected_amount))
        - Decimal(str(settlement.received_amount))
    )

    # No meaningful mismatch
    if difference < MISMATCH_THRESHOLD:
        return None

    # Determine severity
    if difference >= Decimal("100"):
        severity = "CRITICAL"
    elif difference >= Decimal("10"):
        severity = "HIGH"
    else:
        severity = "MEDIUM"

    exception = ExceptionRecord(
        exception_id=f"EXC_{payment_id}",
        payment_id=payment_id,
        exception_type="SETTLEMENT_MISMATCH",
        severity=severity,
        expected_amount=settlement.expected_amount,
        actual_amount=settlement.received_amount,
        difference=difference,
        status="OPEN",
        created_at=datetime.utcnow(),
    )

    session.add(exception)
    session.commit()

    return exception
