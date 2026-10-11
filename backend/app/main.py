from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.db.base import Base
from app.db.database import engine, SessionLocal

from app.models import (
    Customer,
    Merchant,
    Payment,
    Settlement,
    ExceptionRecord,
)

from app.services.reconciliation import reconcile_payment
from app.services.bulk_reconciliation import reconcile_all_payments
from app.ml.anomaly_detector import detect_anomalies
from app.agents.resolution_agent import resolve_exception
from app.api.dashboard import router as dashboard_router


app = FastAPI(
    title="FinOps Autopilot",
    description="Agentic Financial Reconciliation & Exception Resolution Platform",
    version="0.1.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Database
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# Dashboard Router
# --------------------------------------------------

app.include_router(dashboard_router)


# --------------------------------------------------
# Root
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "project": "FinOps Autopilot",
        "status": "running",
        "version": "0.1.0",
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }


# --------------------------------------------------
# Single Payment Reconciliation
# --------------------------------------------------

@app.post("/reconcile/{payment_id}")
def reconcile(payment_id: str):
    session = SessionLocal()

    try:
        exception = reconcile_payment(
            session,
            payment_id,
        )

        # Payment matched successfully
        if exception is None:
            return {
                "status": "matched",
                "payment_id": payment_id,
            }

        # Exception created or existing exception returned
        return {
            "status": "exception_created",
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
            "status_db": exception.status,
        }

    finally:
        session.close()


# --------------------------------------------------
# Bulk Reconciliation
# --------------------------------------------------

@app.post("/reconcile-all")
def reconcile_all():
    session = SessionLocal()

    try:
        return reconcile_all_payments(session)

    finally:
        session.close()


# --------------------------------------------------
# ML Anomaly Detection
# --------------------------------------------------

@app.get("/ml/anomalies")
def ml_anomalies():
    session = SessionLocal()

    try:
        return {
            "status": "success",
            "results": detect_anomalies(session),
        }

    finally:
        session.close()


# --------------------------------------------------
# Exception Resolution Agent
# --------------------------------------------------

@app.post("/exceptions/{exception_id}/resolve")
def resolve_exception_endpoint(exception_id: str):
    session = SessionLocal()

    try:
        return resolve_exception(
            session,
            exception_id,
        )

    except ValueError as e:
        return {
            "status": "error",
            "message": str(e),
        }

    finally:
        session.close()


@app.get("/payments")
def get_payments():
    session = SessionLocal()

    try:
        payments = (
            session.query(Payment)
            .order_by(Payment.created_at.desc())
            .all()
        )

        return [
            {
                "payment_id": payment.payment_id,
                "customer_id": payment.customer_id,
                "merchant_id": payment.merchant_id,
                "amount": float(payment.amount),
                "currency": payment.currency,
                "status": payment.status,
                "processor": payment.processor,
                "created_at": payment.created_at.isoformat()
                if payment.created_at
                else None,
            }
            for payment in payments
        ]

    finally:
        session.close()
