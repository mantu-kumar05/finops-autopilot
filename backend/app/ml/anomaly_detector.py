from decimal import Decimal

import pandas as pd
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.settlement import Settlement


def detect_anomalies(session: Session):
    payments = session.query(Payment).all()

    rows = []

    for payment in payments:
        settlement = (
            session.query(Settlement)
            .filter(Settlement.payment_id == payment.payment_id)
            .first()
        )

        if settlement:
            expected = Decimal(str(settlement.expected_amount))
            received = Decimal(str(settlement.received_amount))

            difference = abs(expected - received)
            has_settlement = 1
        else:
            difference = Decimal("0")
            has_settlement = 0

        rows.append(
            {
                "payment_id": payment.payment_id,
                "amount": float(payment.amount),
                "settlement_difference": float(difference),
                "has_settlement": has_settlement,
            }
        )

    df = pd.DataFrame(rows)

    if len(df) < 2:
        return []

    features = [
        "amount",
        "settlement_difference",
        "has_settlement",
    ]

    model = IsolationForest(
        n_estimators=200,
        contamination=0.10,
        random_state=42,
    )

    model.fit(df[features])

    df["raw_score"] = model.decision_function(df[features])
    df["prediction"] = model.predict(df[features])

    # Convert Isolation Forest score into a simple 0-1 anomaly score.
    min_score = df["raw_score"].min()
    max_score = df["raw_score"].max()

    if max_score == min_score:
        df["anomaly_score"] = 0.0
    else:
        df["anomaly_score"] = (
            (max_score - df["raw_score"])
            / (max_score - min_score)
        )

    df["anomaly_score"] = df["anomaly_score"].round(4)

    return df[
        [
            "payment_id",
            "amount",
            "settlement_difference",
            "has_settlement",
            "anomaly_score",
            "prediction",
        ]
    ].to_dict(orient="records")
