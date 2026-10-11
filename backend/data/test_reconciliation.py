from app.db.database import SessionLocal
from app.services.reconciliation import reconcile_payment


def main():
    session = SessionLocal()

    try:
        exception = reconcile_payment(
            session,
            "PAY_000001",
        )

        if exception:
            print("Exception detected!")
            print(f"Exception ID: {exception.exception_id}")
            print(f"Type: {exception.exception_type}")
            print(f"Severity: {exception.severity}")
            print(f"Difference: {exception.difference}")
        else:
            print("No exception detected.")

    finally:
        session.close()


if __name__ == "__main__":
    main()
