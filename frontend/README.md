FinOps Autopilot
Agentic Financial Reconciliation & Exception Resolution Platform

FinOps Autopilot is an intelligent financial operations platform that automates payment reconciliation, detects settlement exceptions, identifies anomalies using machine learning, and assists with exception resolution.

System Architecture
                    ┌─────────────────────┐
                    │    React Dashboard  │
                    │    localhost:5173   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │    Backend API      │
                    │    localhost:8000   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       Reconciliation     ML Detection    Resolution Agent
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │     PostgreSQL      │
                    │       finops        │
                    └─────────────────────┘

Core Features
Payment reconciliation
Settlement matching
Missing settlement detection
Settlement mismatch detection
Exception severity classification
Bulk reconciliation
ML-based anomaly detection
Agent-assisted exception resolution
Real-time dashboard
Exception management
PostgreSQL persistence
Current Demo Data

The development environment contains:

20 payments
1 settlement
20 detected exceptions
Settlement mismatch for PAY_000001
Missing settlements for the remaining payments
Multiple exceptions processed by the Resolution Agent
ML anomaly detection results
Backend

The backend is built with:

Python
FastAPI
SQLAlchemy
PostgreSQL
Psycopg2
Run the Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload


Backend:

http://127.0.0.1:8000


API documentation:

http://127.0.0.1:8000/docs


Health check:

http://127.0.0.1:8000/health

Frontend

The frontend is built with:

React
Vite
Axios
Run the Frontend
cd frontend
npm run dev


Frontend:

http://localhost:5173

API Endpoints
Health
GET /health


Checks database connectivity.

Dashboard Summary
GET /dashboard/summary


Returns payment, settlement, exception and status statistics.

Exceptions
GET /dashboard/exceptions


Returns detected financial exceptions.

Payments
GET /payments


Returns processed payment records used by the Payment Operations dashboard.

Reconcile Payment
POST /reconcile/{payment_id}


Reconciles an individual payment against its settlement.

Reconcile All
POST /reconcile-all


Runs reconciliation across all payments.

ML Anomalies
GET /ml/anomalies


Runs anomaly detection against payment data.

Resolve Exception
POST /exceptions/{exception_id}/resolve


Processes an exception through the Resolution Agent.

End-to-End Workflow
Payment Data
     │
     ▼
Reconciliation
     │
     ├── Match ───────────────► Successful
     │
     └── Mismatch/Missing
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

Project Structure
finops-autopilot/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── db/
│   │   ├── ml/
│   │   ├── models/
│   │   └── services/
│   │
│   ├── data/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
└── README.md

Project Status
MVP Complete
 PostgreSQL database
 SQLAlchemy models
 Synthetic financial data
 Payment reconciliation
 Exception detection
 Bulk reconciliation
 ML anomaly detection
 Resolution Agent
 FastAPI APIs
 React dashboard
 Exception management
 Payment Operations dashboard
 Automated dashboard refresh
Demo

Start the backend first:

cd backend
venv\Scripts\activate
uvicorn app.main:app --reload


Then start the frontend in a second terminal:

cd frontend
npm run dev


Open:

http://localhost:5173


The dashboard displays the current reconciliation and exception state and allows OPEN exceptions to be processed through the Resolution Agent.

Technology Stack
Layer	Technology
Frontend	React + Vite
API	FastAPI
ORM	SQLAlchemy
Database	PostgreSQL
Database Driver	Psycopg2
HTTP Client	Axios
ML	Scikit-learn
Runtime	Python + Node.js
Purpose

FinOps Autopilot is designed as an internal financial operations platform for teams that need to monitor payment transactions, reconcile settlements, identify exceptions, detect anomalous activity, and streamline exception handling.

