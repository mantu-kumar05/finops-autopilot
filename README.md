# FinOps Autopilot

**Agentic Financial Reconciliation & Exception Resolution Platform**

FinOps Autopilot is an intelligent financial operations platform that automates payment reconciliation, detects settlement exceptions, identifies anomalous transactions using machine learning, and assists with exception resolution.

## 🚀 Features

- Payment reconciliation and settlement matching
- Missing settlement and settlement mismatch detection
- Exception severity classification (CRITICAL / HIGH / MEDIUM)
- Bulk reconciliation
- ML-based anomaly detection
- Agent-assisted exception resolution
- Real-time operational dashboard with automated refresh
- Exception management and Payment Operations monitoring
- PostgreSQL persistence

## 🏗️ System Architecture

```
┌──────────────────────────┐
│     React Dashboard      │
│      Vite + Axios        │
│     localhost:5173       │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│         FastAPI          │
│       Backend API        │
│     localhost:8000       │
└────────────┬─────────────┘
             │
      ┌──────┼───────────────┐
      │      │               │
      ▼      ▼               ▼
┌──────────┐ ┌─────────────┐ ┌─────────────────┐
│Reconcil- │ │ML Detection │ │Resolution Agent │
│iation    │ │Scikit-learn │ │Workflow         │
│Service   │ │             │ │                 │
└────┬─────┘ └──────┬──────┘ └────────┬────────┘
     │              │                 │
     └──────────────┼─────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │      PostgreSQL      │
         │       finops DB      │
         └──────────────────────┘
```

## 🔄 How It Works

```
Payment Data
     │
     ▼
Payment Reconciliation
     │
     ├──────── Match ──────────────► Successful
     │
     └──────── Mismatch / Missing
                    │
                    ▼
            Exception Detection
                    │
                    ▼
           Severity Classification
                    │
                    ▼
            ML Anomaly Detection
                    │
                    ▼
              Resolution Agent
                    │
                    ▼
             Dashboard Update
```

## 🧠 Core Components

### Payment Reconciliation
Compares payment records against settlement records and identifies whether transactions are successfully reconciled.

### Exception Detection
Detects financial exceptions including:
- Missing settlements
- Settlement mismatches
- Amount differences
- High-value discrepancies

### Severity Classification
Exceptions are automatically classified as `CRITICAL`, `HIGH` or `MEDIUM`.

### ML Anomaly Detection
Uses Scikit-learn to identify unusual payment activity based on transaction and settlement-related features. The ML service produces an anomaly score and a prediction for each payment (`-1` = anomaly, `1` = normal).

### Resolution Agent
Processes detected exceptions and updates their operational status. Users can trigger exception resolution directly from the dashboard.

## 📊 Demo Data

The synthetic development data contains:

| Metric | Value |
|---|---|
| Payments | 20 |
| Settlements | 1 |
| Exceptions | 20 |
| Settlement Mismatch | PAY_000001 |
| Missing Settlements | 19 |

Example exception:

| Field | Value |
|---|---|
| Payment ID | PAY_000001 |
| Expected Amount | 3710.34 EUR |
| Received Amount | 3690.34 EUR |
| Difference | 20.00 EUR |
| Exception Type | SETTLEMENT_MISMATCH |
| Severity | HIGH |

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Axios |
| Backend | FastAPI (Python) |
| ORM | SQLAlchemy |
| Database | PostgreSQL (Psycopg2) |
| Machine Learning | Scikit-learn |
| Runtime | Python + Node.js |

## 📁 Project Structure

```
finops-autopilot/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   └── resolution_agent.py
│   │   ├── api/
│   │   │   ├── dashboard.py
│   │   │   └── reconciliation.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── database.py
│   │   │   └── init_db.py
│   │   ├── ml/
│   │   │   └── anomaly_detector.py
│   │   ├── models/
│   │   │   ├── customer.py
│   │   │   ├── merchant.py
│   │   │   ├── payment.py
│   │   │   ├── settlement.py
│   │   │   └── exception.py
│   │   ├── services/
│   │   │   ├── reconciliation.py
│   │   │   └── bulk_reconciliation.py
│   │   └── main.py
│   ├── data/
│   │   ├── generate_data.py
│   │   └── test_reconciliation.py
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## ⚙️ Backend Setup

**Prerequisites:** Python 3.13, Node.js, and PostgreSQL.

1. Create the database:

```
createdb finops
```

2. Create a virtual environment and install dependencies:

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure your environment:

```
copy .env.example .env
```

Open `.env` and set `DATABASE_URL` to your PostgreSQL credentials.

4. Create the tables and load the synthetic data:

```
python -m app.db.init_db
python -m data.generate_data
```

5. Start the API:

```
uvicorn app.main:app --reload
```

- Backend: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## 💻 Frontend Setup

Open a second terminal:

```
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks database connectivity |
| GET | `/dashboard/summary` | Payment, settlement, exception and status statistics |
| GET | `/dashboard/exceptions` | Detected financial exceptions |
| GET | `/payments` | Processed payment records for the Payment Operations dashboard |
| POST | `/reconcile/{payment_id}` | Reconciles one payment against its settlement |
| POST | `/reconcile-all` | Runs reconciliation across all payments |
| GET | `/ml/anomalies` | Runs anomaly detection against payment data |
| POST | `/exceptions/{exception_id}/resolve` | Processes an exception through the Resolution Agent |

## 📈 Dashboard

The React dashboard provides:

- Payment, settlement and exception counts
- Open, critical, high, medium and in-review exception counts
- Exception management table and Payment Operations table
- Reconciliation controls and ML anomaly detection control
- Exception resolution actions
- Automated dashboard refresh

## 🧪 Example ML Output

```json
{
  "payment_id": "PAY_000019",
  "amount": 566.65,
  "settlement_difference": 0,
  "has_settlement": 0,
  "anomaly_score": 0.434,
  "prediction": -1
}
```

| Prediction | Meaning |
|---|---|
| -1 | Anomaly |
| 1 | Normal |

## 📌 Project Status

**MVP complete**

- [x] PostgreSQL database and SQLAlchemy models
- [x] Synthetic financial data
- [x] Payment reconciliation and settlement matching
- [x] Exception detection and severity classification
- [x] Bulk reconciliation
- [x] ML anomaly detection
- [x] Resolution Agent
- [x] FastAPI APIs
- [x] React dashboard with exception management and Payment Operations
- [x] Automated dashboard refresh

## 🎯 Purpose

FinOps Autopilot is designed as an internal financial operations platform for teams that need to monitor payments, reconcile payment and settlement records, identify missing settlements and mismatches, detect anomalous activity, prioritize exceptions, and automate exception handling from a central dashboard.

## 🔐 Development Note

This project uses synthetic financial data and is intended for demonstration, development and portfolio purposes. It is not intended for processing real production financial transactions without additional security, compliance, authentication, authorization, monitoring and infrastructure controls.

## 📄 License

This project is intended for educational, demonstration and portfolio use.