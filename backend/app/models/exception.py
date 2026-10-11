from sqlalchemy import Column, String, Numeric, DateTime
from app.db.base import Base


class ExceptionRecord(Base):
    __tablename__ = "exceptions"

    exception_id = Column(String, primary_key=True)
    payment_id = Column(String, nullable=False, index=True)

    exception_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)

    expected_amount = Column(Numeric(18, 2), nullable=True)
    actual_amount = Column(Numeric(18, 2), nullable=True)
    difference = Column(Numeric(18, 2), nullable=True)

    status = Column(String(30), nullable=False, default="OPEN")

    created_at = Column(DateTime, nullable=False)
