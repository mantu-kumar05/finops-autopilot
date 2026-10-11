from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.services.reconciliation import reconcile_payment


def reconcile_all_payments(session: Session):
    payments = session.query(Payment).all()

    total = len(payments)
    matched = 0
    exceptions = 0
    errors = 0

    results = []

    for payment in payments:
        try:
            result = reconcile_payment(
                session,
                payment.payment_id,
            )

            if result is None:
                matched += 1

                results.append(
                    {
                        "payment_id": payment.payment_id,
                        "status": "matched",
                    }
                )

            else:
                exceptions += 1

                results.append(
                    {
                        "payment_id": payment.payment_id,
                        "status": "exception",
                        "exception_id": result.exception_id,
                        "exception_type": result.exception_type,
                        "severity": result.severity,
                    }
                )

        except Exception as e:
            errors += 1

            session.rollback()

            results.append(
                {
                    "payment_id": payment.payment_id,
                    "status": "error",
                    "error": str(e),
                }
            )

    return {
        "total_payments": total,
        "matched": matched,
        "exceptions": exceptions,
        "errors": errors,
        "results": results,
    }
