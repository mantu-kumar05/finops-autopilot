import random
from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.database import DATABASE_URL
from app.models.customer import Customer
from app.models.merchant import Merchant
from app.models.payment import Payment


# Reproducible data
random.seed(42)

CUSTOMER_COUNT = 10
MERCHANT_COUNT = 5
PAYMENT_COUNT = 20

CURRENCIES = ["USD", "EUR", "GBP", "INR"]
PROCESSORS = ["processor_a", "processor_b", "processor_c"]
PAYMENT_STATUSES = ["SETTLED", "SUCCESS", "FAILED", "REFUNDED"]


def generate_customers(session: Session):
    customers = []

    for i in range(1, CUSTOMER_COUNT + 1):
        customer = Customer(
            customer_id=f"CUS_{i:05d}",
            name=f"Customer {i}",
            email=f"customer{i}@example.com",
        )

        customers.append(customer)

    session.add_all(customers)
    session.flush()

    return customers


def generate_merchants(session: Session):
    merchants = []

    countries = ["US", "GB", "DE", "IN", "SG"]

    for i in range(1, MERCHANT_COUNT + 1):
        merchant = Merchant(
            merchant_id=f"MER_{i:05d}",
            name=f"Merchant {i}",
            country=countries[(i - 1) % len(countries)],
        )

        merchants.append(merchant)

    session.add_all(merchants)
    session.flush()

    return merchants


def generate_payments(
    session: Session,
    customers: list[Customer],
    merchants: list[Merchant],
):
    payments = []

    start_date = datetime.utcnow() - timedelta(days=30)

    for i in range(1, PAYMENT_COUNT + 1):
        customer = random.choice(customers)
        merchant = random.choice(merchants)

        payment = Payment(
            payment_id=f"PAY_{i:06d}",
            customer_id=customer.customer_id,
            merchant_id=merchant.merchant_id,
            amount=Decimal(str(round(random.uniform(10, 5000), 2))),
            currency=random.choice(CURRENCIES),
            status=random.choice(PAYMENT_STATUSES),
            processor=random.choice(PROCESSORS),
            created_at=start_date + timedelta(
                minutes=random.randint(0, 30 * 24 * 60)
            ),
        )

        payments.append(payment)

    session.add_all(payments)


def main():
    engine = create_engine(DATABASE_URL)

    with Session(engine) as session:
        try:
            customers = generate_customers(session)
            merchants = generate_merchants(session)

            generate_payments(
                session,
                customers,
                merchants,
            )

            session.commit()

            print("Synthetic data generated successfully.")
            print(f"Customers: {len(customers)}")
            print(f"Merchants: {len(merchants)}")
            print(f"Payments: {PAYMENT_COUNT}")

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()


if __name__ == "__main__":
    main()
