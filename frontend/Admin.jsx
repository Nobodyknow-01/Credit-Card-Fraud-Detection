import { useEffect, useState } from "react";

function Admin() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/admin/logs")
      .then(res => res.json())
      .then(data => setLogs(data));
  }, []);

  return (
    <div style={{ padding: 30 }}>
      <h1>🛡 Fraud Logs</h1>

      {logs.map(log => (
        <div key={log.id} style={{
          border: "1px solid #ddd",
          padding: 15,
          marginBottom: 10,
          borderRadius: 10
        }}>
          <p><strong>Amount:</strong> ₹{log.amount}</p>
          <p><strong>Prediction:</strong> {log.prediction}</p>
          <p><strong>Probability:</strong> {log.probability}%</p>
          <p><strong>Reasons:</strong> {log.reasons}</p>
          <p><small>{log.time}</small></p>
        </div>
      ))}
    </div>
  );
}

export default Admin;
