from sqlalchemy import Column, String, Numeric, DateTime
from app.db.base import Base


class Settlement(Base):
    __tablename__ = "settlements"

    settlement_id = Column(String, primary_key=True)
    payment_id = Column(String, nullable=False, index=True)

    expected_amount = Column(Numeric(18, 2), nullable=False)
    received_amount = Column(Numeric(18, 2), nullable=False)

    currency = Column(String(3), nullable=False)
    status = Column(String(30), nullable=False)

    settled_at = Column(DateTime, nullable=True)
