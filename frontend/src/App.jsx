import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [summary, setSummary] = useState(null);
  const [exceptions, setExceptions] = useState([]);
  const [payments, setPayments] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const loadDashboard = async () => {
    try {
      const [summaryRes, exceptionsRes, paymentsRes] =
        await Promise.all([
          axios.get(`${API}/dashboard/summary`),
          axios.get(`${API}/dashboard/exceptions`),
          axios.get(`${API}/payments`),
        ]);

      setSummary(summaryRes.data);
      setExceptions(exceptionsRes.data);
      setPayments(paymentsRes.data);
    } catch (error) {
      console.error(error);
      setMessage("Unable to load dashboard.");
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const resolveException = async (exceptionId) => {
    setLoading(true);
    setMessage("");

    try {
      await axios.post(`${API}/exceptions/${exceptionId}/resolve`);

      setMessage(`${exceptionId} resolved successfully.`);

      await loadDashboard();
    } catch (error) {
      console.error(error);
      setMessage(`Failed to resolve ${exceptionId}.`);
    } finally {
      setLoading(false);
    }
  };

  const reconcileAll = async () => {
    setLoading(true);
    setMessage("");

    try {
      await axios.post(`${API}/reconcile-all`);

      setMessage("All payments reconciled successfully.");

      await loadDashboard();
    } catch (error) {
      console.error(error);
      setMessage("Bulk reconciliation failed.");
    } finally {
      setLoading(false);
    }
  };

  const runAnomalyDetection = async () => {
    setLoading(true);
    setMessage("");

    try {
      const response = await axios.get(`${API}/ml/anomalies`);

      const anomalies = response.data.results || [];

      const count = anomalies.filter(
        (item) => item.prediction === -1
      ).length;

      setMessage(`ML scan completed. ${count} anomalies detected.`);
    } catch (error) {
      console.error(error);
      setMessage("ML anomaly detection failed.");
    } finally {
      setLoading(false);
    }
  };

  if (!summary) {
    return (
      <div className="app">
        <h1>FinOps Autopilot</h1>
        <p>Loading dashboard...</p>
        {message && <p className="error">{message}</p>}
      </div>
    );
  }

  return (
    <div className="app">
      <header>
        <h1>FinOps Autopilot</h1>
        <p>Agentic Financial Reconciliation Platform</p>
        <span className="system-status">
          ● System Operational
        </span>
      </header>

      {message && <div className="message">{message}</div>}

      {/* SUMMARY */}

      <section className="cards">
        <div className="card">
          <h3>Total Payments</h3>
          <strong>{summary.total_payments}</strong>
        </div>

        <div className="card">
          <h3>Settlements</h3>
          <strong>{summary.settlements}</strong>
        </div>

        <div className="card">
          <h3>Exceptions</h3>
          <strong>{summary.exceptions}</strong>
        </div>

        <div className="card danger">
          <h3>Open Exceptions</h3>
          <strong>{summary.open_exceptions}</strong>
        </div>
      </section>

      {/* EXCEPTION OVERVIEW */}

      <section className="overview">
        <h2>Exception Overview</h2>

        <div className="overview-grid">
          <div>
            <span>Critical</span>
            <strong>{summary.critical}</strong>
          </div>

          <div>
            <span>High</span>
            <strong>{summary.high}</strong>
          </div>

          <div>
            <span>Medium</span>
            <strong>{summary.medium}</strong>
          </div>

          <div>
            <span>In Review</span>
            <strong>{summary.in_review}</strong>
          </div>
        </div>
      </section>

      {/* AUTOMATION */}

      <section className="actions">
        <h2>Automation Controls</h2>

        <button onClick={reconcileAll} disabled={loading}>
          {loading ? "Processing..." : "Run Reconciliation"}
        </button>

        <button
          onClick={runAnomalyDetection}
          disabled={loading}
        >
          Run ML Anomaly Detection
        </button>

        <button
          onClick={loadDashboard}
          disabled={loading}
        >
          Refresh Dashboard
        </button>
      </section>

      {/* EXCEPTIONS */}

      <section className="exceptions">
        <div className="section-header">
          <div>
            <h2>Exception Management</h2>
            <p>
              Review and resolve detected financial exceptions.
            </p>
          </div>

          <span className="live">LIVE</span>
        </div>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Exception ID</th>
                <th>Payment</th>
                <th>Type</th>
                <th>Severity</th>
                <th>Difference</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {exceptions.map((exception) => (
                <tr key={exception.exception_id}>
                  <td>{exception.exception_id}</td>

                  <td>{exception.payment_id}</td>

                  <td>{exception.exception_type}</td>

                  <td>
                    <span
                      className={`severity ${exception.severity.toLowerCase()}`}
                    >
                      {exception.severity}
                    </span>
                  </td>

                  <td>
                    {exception.difference !== null
                      ? exception.difference
                      : "-"}
                  </td>

                  <td>{exception.status}</td>

                  <td>
                    {exception.status === "OPEN" ? (
                      <button
                        className="resolve-btn"
                        onClick={() =>
                          resolveException(
                            exception.exception_id
                          )
                        }
                        disabled={loading}
                      >
                        Resolve
                      </button>
                    ) : (
                      <span className="resolved">
                        ✓ Resolved
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* PAYMENTS */}

      <section className="payments">
        <div className="section-header">
          <div>
            <h2>Payment Operations</h2>
            <p>
              Monitor processed financial transactions.
            </p>
          </div>
        </div>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Payment ID</th>
                <th>Customer</th>
                <th>Merchant</th>
                <th>Amount</th>
                <th>Currency</th>
                <th>Status</th>
                <th>Processor</th>
              </tr>
            </thead>

            <tbody>
              {payments.map((payment) => (
                <tr key={payment.payment_id}>
                  <td>{payment.payment_id}</td>
                  <td>{payment.customer_id}</td>
                  <td>{payment.merchant_id}</td>

                  <td>
                    {payment.amount.toFixed(2)}
                  </td>

                  <td>{payment.currency}</td>

                  <td>{payment.status}</td>

                  <td>{payment.processor}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <footer>
        FinOps Autopilot · Automated Financial Operations
      </footer>
    </div>
  );
}

export default App;