from app.db.base import Base
from app.db.database import engine

# Import all models so SQLAlchemy knows about them
from app.models.customer import Customer
from app.models.merchant import Merchant
from app.models.payment import Payment
from app.models.settlement import Settlement
from app.models.exception import ExceptionRecord


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
