import { useState, useEffect } from "react"; 

function App() {
  const [result, setResult] = useState(null);
  const [admin, setAdmin] = useState(false);
  const [logs, setLogs] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [showPopup, setShowPopup] = useState(null);

  const [form, setForm] = useState({
    amount: "",
    is_night: false,
    new_device: false,
    location_changed: false,
    transactions_today: 1,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm({ ...form, [name]: type === "checkbox" ? checked : value });
  };

  const predictFraud = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          amount: Number(form.amount) || 0,
          transactions_today: Number(form.transactions_today) || 1,
        }),
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      setResult({ prediction: "Error", fraud_probability: 0, reasons: ["Check backend connection"] });
    }
  };

  const loadLogs = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/admin/logs");
      const data = await res.json();
      setLogs(data);
    } catch (e) {
      setLogs([]);
    }
  };

  useEffect(() => {
    if (admin) loadLogs();
  }, [admin]);

  const filteredLogs = logs.filter(log =>
    !searchTerm || 
    (log.prediction && log.prediction.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (log.time && log.time.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const getColor = (p) => p?.includes("Fraud") ? "#ef4444" : p?.includes("Suspicious") ? "#facc15" : "#22c55e";

  const styles = {
    page: {
      minHeight: "100vh",
      width: "100vw",
      margin: 0,
      padding: "2rem",
      background: "linear-gradient(135deg, #1e3a8a 0%, #7c3aed 50%, #ec4899 100%)",
      color: "white",
      fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      overflowX: "hidden"
    },
    mainLayout: {
      maxWidth: "1400px",
      margin: "0 auto",
      minHeight: "100vh",
      position: "relative",
      padding: "2rem 0"
    },
    cornerCardsContainer: {
      position: "fixed",
      top: 0,
      left: 0,
      width: "100vw",
      height: "100vh",
      pointerEvents: "none",
      zIndex: 10
    },
    topLeftCard: {
      position: "absolute",
      top: "2rem",
      left: "2rem",
      width: "280px",
      background: "rgba(255,255,255,0.15)",
      backdropFilter: "blur(20px)",
      padding: "1.5rem",
      borderRadius: "16px",
      border: "1px solid rgba(255,255,255,0.3)",
      pointerEvents: "auto",
      cursor: "pointer"
    },
    topRightCard: {
      position: "absolute",
      top: "2rem",
      right: "2rem",
      width: "280px",
      background: "rgba(255,255,255,0.15)",
      backdropFilter: "blur(20px)",
      padding: "1.5rem",
      borderRadius: "16px",
      border: "1px solid rgba(255,255,255,0.3)",
      pointerEvents: "auto",
      cursor: "pointer"
    },
    bottomLeftCard: {
      position: "absolute",
      bottom: "2rem",
      left: "2rem",
      width: "280px",
      background: "rgba(255,255,255,0.15)",
      backdropFilter: "blur(20px)",
      padding: "1.5rem",
      borderRadius: "16px",
      border: "1px solid rgba(255,255,255,0.3)",
      pointerEvents: "auto",
      cursor: "pointer"
    },
    bottomRightCard: {
      position: "absolute",
      bottom: "2rem",
      right: "2rem",
      width: "280px",
      background: "rgba(255,255,255,0.15)",
      backdropFilter: "blur(20px)",
      padding: "1.5rem",
      borderRadius: "16px",
      border: "1px solid rgba(255,255,255,0.3)",
      pointerEvents: "auto",
      cursor: "pointer"
    },
    centerForm: {
      background: "rgba(255,255,255,0.15)",
      backdropFilter: "blur(30px)",
      border: "1px solid rgba(255,255,255,0.3)",
      borderRadius: "24px",
      padding: "3rem",
      boxShadow: "0 25px 50px -12px rgba(0,0,0,0.4)",
      maxWidth: "500px",
      width: "100%",
      margin: "4rem auto 4rem",
      textAlign: "center"
    },
    title: {
      fontSize: "2.5rem",
      fontWeight: "900",
      background: "linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6)",
      WebkitBackgroundClip: "text",
      backgroundClip: "text",
      WebkitTextFillColor: "transparent",
      marginBottom: "2rem",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      gap: "1rem"
    },
    input: {
      width: "100%",
      padding: "1rem 1.25rem",
      marginBottom: "1rem",
      background: "rgba(255,255,255,0.2)",
      border: "1px solid rgba(255,255,255,0.4)",
      borderRadius: "12px",
      color: "white",
      fontSize: "1.1rem",
      boxSizing: "border-box"
    },
    checkboxLabel: {
      display: "flex",
      alignItems: "center",
      gap: "1rem",
      padding: "1rem",
      background: "rgba(255,255,255,0.15)",
      borderRadius: "12px",
      border: "1px solid rgba(255,255,255,0.3)",
      cursor: "pointer",
      marginBottom: "0.5rem",
      justifyContent: "space-between"
    },
    button: {
      padding: "1.25rem 2rem",
      fontSize: "1.1rem",
      fontWeight: "700",
      borderRadius: "12px",
      border: "none",
      cursor: "pointer",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      gap: "0.75rem",
      margin: "0.5rem 0",
      width: "100%"
    },
    analyzeBtn: {
      background: "linear-gradient(135deg, #3b82f6, #1d4ed8)",
      color: "white",
      boxShadow: "0 10px 25px rgba(59,130,246,0.4)"
    },
    adminBtn: {
      background: "linear-gradient(135deg, #10b981, #059669)",
      color: "white",
      boxShadow: "0 10px 25px rgba(16,185,129,0.4)"
    },
    result: {
      marginTop: "2rem",
      padding: "2rem",
      borderRadius: "20px",
      boxShadow: "0 20px 40px rgba(0,0,0,0.3)"
    },
    popup: {
      position: "fixed",
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: "rgba(0,0,0,0.7)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 1000
    },
    popupContent: {
      background: "linear-gradient(135deg, rgba(30,58,138,0.95), rgba(124,58,237,0.95))",
      backdropFilter: "blur(20px)",
      padding: "2.5rem",
      borderRadius: "24px",
      maxWidth: "500px",
      width: "90%",
      maxHeight: "80vh",
      overflowY: "auto",
      border: "1px solid rgba(255,255,255,0.3)"
    }
  };

  const factorNotes = [
    { icon: "💰", title: "High Amount", note: "Fraudsters prefer median $79 charges (55% under $100) to evade limits." },
    { icon: "🌙", title: "Night Time", note: "Legitimate txns drop at night; fraud peaks ~2am with low oversight." },
    { icon: "📱", title: "New Device", note: "Account takeovers spike via new devices for unauthorized access." },
    { icon: "📍", title: "Location Change", note: "Sudden geo-mismatches flag high risk in fraud detection." }
  ];

  if (admin) {
    return (
      <div style={styles.page}>
        <style>{`* { margin: 0; padding: 0; box-sizing: border-box; }`}</style>
        <div style={{ maxWidth: "1400px", margin: "0 auto", padding: "2rem 0", minHeight: "100vh" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "2rem" }}>
            <h1 style={{ fontSize: "2rem", fontWeight: "900", color: "white" }}>🧑‍💼 Admin Dashboard</h1>
            <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
              <span style={{ fontSize: "1.1rem" }}>
                Total Logs: <strong>{logs.length}</strong>
              </span>
              <button style={{ ...styles.button, ...styles.analyzeBtn, padding: "1rem 1.5rem", width: "auto" }} onClick={() => setAdmin(false)}>
                ← Back to App
              </button>
            </div>
          </div>
          
          <div style={{ display: "flex", gap: "1rem", marginBottom: "1.5rem", flexWrap: "wrap" }}>
            <input 
              style={{ ...styles.input, flex: 1, minWidth: "300px" }} 
              placeholder="🔍 Search by prediction or time..." 
              value={searchTerm} 
              onChange={(e) => setSearchTerm(e.target.value)} 
            />
            <button style={{ ...styles.button, ...styles.adminBtn, padding: "1rem 1.5rem", whiteSpace: "nowrap" }} onClick={loadLogs}>
              🔄 Refresh
            </button>
          </div>

          <div style={{ 
            flex: 1, 
            overflow: "auto", 
            background: "rgba(255,255,255,0.1)", 
            borderRadius: "16px", 
            padding: "1.5rem",
            border: "1px solid rgba(255,255,255,0.3)",
            maxHeight: "70vh"
          }}>
            {filteredLogs.length === 0 ? (
              <div style={{ 
                textAlign: "center", 
                padding: "3rem", 
                color: "rgba(255,255,255,0.7)",
                fontSize: "1.1rem"
              }}>
                {logs.length === 0 ? 
                  "📭 No logs available. Make some predictions first!" : 
                  "🔍 No logs match your search. Try adjusting the search term."
                }
              </div>
            ) : (
              <div style={{ 
                display: "grid", 
                gridTemplateColumns: "repeat(auto-fill, minmax(400px, 1fr))", 
                gap: "1rem",
                minHeight: "100%"
              }}>
                {filteredLogs.map((log, index) => (
                  <div key={index} style={{
                    background: "rgba(255,255,255,0.15)",
                    borderRadius: "12px",
                    padding: "1.5rem",
                    borderLeft: `5px solid ${getColor(log.prediction)}`,
                    backdropFilter: "blur(10px)",
                    boxShadow: "0 4px 20px rgba(0,0,0,0.2)"
                  }}>
                    <div style={{ 
                      display: "flex", 
                      justifyContent: "space-between", 
                      alignItems: "flex-start", 
                      marginBottom: "1rem" 
                    }}>
                      <div style={{ 
                        fontSize: "1.3rem", 
                        fontWeight: "700", 
                        color: getColor(log.prediction),
                        display: "flex",
                        alignItems: "center",
                        gap: "0.5rem"
                      }}>
                        {log.prediction?.includes("Fraud") ? "⚠️" : log.prediction?.includes("Suspicious") ? "⚡" : "✅"}
                        {log.prediction || "Unknown"}
                      </div>
                      <div style={{ 
                        fontSize: "0.9rem", 
                        color: "rgba(255,255,255,0.8)",
                        textAlign: "right"
                      }}>
                        {log.time || "No timestamp"}
                      </div>
                    </div>
                    
                    {log.fraud_probability !== undefined && (
                      <div style={{ 
                        fontSize: "2rem", 
                        fontWeight: "900", 
                        color: getColor(log.prediction),
                        marginBottom: "1rem",
                        textAlign: "center"
                      }}>
                        {log.fraud_probability}%
                      </div>
                    )}
                    
                    {log.amount && (
                      <div style={{ marginBottom: "0.75rem" }}>
                        <strong>Amount:</strong> ₹{log.amount.toLocaleString()}
                      </div>
                    )}
                    
                    {log.reasons && log.reasons.length > 0 && (
                      <div>
                        <strong>Reasons:</strong>
                        <ul style={{ 
                          margin: "0.5rem 0 0 0", 
                          paddingLeft: "1.25rem",
                          fontSize: "0.9rem"
                        }}>
                          {log.reasons.map((reason, i) => (
                            <li key={i} style={{ marginBottom: "0.25rem", color: "rgba(255,255,255,0.9)" }}>
                              • {reason}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
          
          <div style={{ 
            marginTop: "1.5rem", 
            padding: "1rem", 
            background: "rgba(255,255,255,0.1)",
            borderRadius: "12px",
            textAlign: "center",
            fontSize: "0.9rem",
            color: "rgba(255,255,255,0.7)"
          }}>
            Showing {filteredLogs.length} of {logs.length} logs
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.page}>
      <style>{`* { margin: 0; padding: 0; box-sizing: border-box; }`}</style>
      
      {/* FIXED CORNER CARDS - Always visible */}
      <div style={styles.cornerCardsContainer}>
        <div style={styles.topLeftCard} onClick={() => setShowPopup("note-0")}>
          <div style={{ fontSize: "2rem", marginBottom: "1rem", textAlign: "center" }}>{factorNotes[0].icon}</div>
          <h4 style={{ fontWeight: "700", marginBottom: "0.5rem" }}>{factorNotes[0].title}</h4>
          <p style={{ fontSize: "0.85rem", lineHeight: 1.4 }}>{factorNotes[0].note}</p>
        </div>
        <div style={styles.topRightCard} onClick={() => setShowPopup("note-1")}>
          <div style={{ fontSize: "2rem", marginBottom: "1rem", textAlign: "center" }}>{factorNotes[1].icon}</div>
          <h4 style={{ fontWeight: "700", marginBottom: "0.5rem" }}>{factorNotes[1].title}</h4>
          <p style={{ fontSize: "0.85rem", lineHeight: 1.4 }}>{factorNotes[1].note}</p>
        </div>
        <div style={styles.bottomLeftCard} onClick={() => setShowPopup("note-2")}>
          <div style={{ fontSize: "2rem", marginBottom: "1rem", textAlign: "center" }}>{factorNotes[2].icon}</div>
          <h4 style={{ fontWeight: "700", marginBottom: "0.5rem" }}>{factorNotes[2].title}</h4>
          <p style={{ fontSize: "0.85rem", lineHeight: 1.4 }}>{factorNotes[2].note}</p>
        </div>
        <div style={styles.bottomRightCard} onClick={() => setShowPopup("note-3")}>
          <div style={{ fontSize: "2rem", marginBottom: "1rem", textAlign: "center" }}>{factorNotes[3].icon}</div>
          <h4 style={{ fontWeight: "700", marginBottom: "0.5rem" }}>{factorNotes[3].title}</h4>
          <p style={{ fontSize: "0.85rem", lineHeight: 1.4 }}>{factorNotes[3].note}</p>
        </div>
      </div>

      {/* SCROLLABLE CENTER CONTENT */}
      <div style={styles.mainLayout}>
        <div style={styles.centerForm}>
          <h1 style={styles.title}>Credit Card Fraud Detection</h1>

          <div style={{ marginBottom: "2rem" }}>
            <label style={{ display: "block", marginBottom: "0.75rem", fontWeight: "600" }}>💰 Amount (₹)</label>
            <input style={styles.input} name="amount" placeholder="e.g., 5000" value={form.amount} onChange={handleChange} />
            <label style={{ display: "block", marginBottom: "0.75rem", fontWeight: "600" }}>⏰ Transactions Today</label>
            <input style={styles.input} name="transactions_today" type="number" placeholder="1" value={form.transactions_today} onChange={handleChange} />
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem", marginBottom: "2rem" }}>
            <label style={styles.checkboxLabel}>
              🌙 Night Time
              <input type="checkbox" name="is_night" style={{ width: "1.25rem", height: "1.25rem" }} onChange={handleChange} />
            </label>
            <label style={styles.checkboxLabel}>
              📱 New Device
              <input type="checkbox" name="new_device" style={{ width: "1.25rem", height: "1.25rem" }} onChange={handleChange} />
            </label>
            <label style={styles.checkboxLabel}>
              📍 Location Changed
              <input type="checkbox" name="location_changed" style={{ width: "1.25rem", height: "1.25rem" }} onChange={handleChange} />
            </label>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "1rem", marginBottom: "2rem" }}>
            <button style={{ ...styles.button, ...styles.analyzeBtn }} onClick={predictFraud}>🔍 Analyze Transaction</button>
            <button style={{ ...styles.button, ...styles.adminBtn }} onClick={() => setAdmin(true)}>🛡️ Admin Dashboard</button>
          </div>

          {result && (
            <div style={{
              ...styles.result,
              border: `4px solid ${getColor(result.prediction)}`,
              backgroundColor: getColor(result.prediction) + "20",
              textAlign: "center"
            }}>
              <div style={{ fontSize: "2rem", marginBottom: "1rem", display: "flex", alignItems: "center", justifyContent: "center", gap: "1rem" }}>
                {result.prediction.includes("Fraud") ? "⚠️" : "✅"}
                <span style={{ fontSize: "1.5rem", fontWeight: "900" }}>{result.prediction}</span>
              </div>
              <div style={{ fontSize: "3rem", fontWeight: "900", marginBottom: "1rem", color: getColor(result.prediction) }}>
                {result.fraud_probability}%
              </div>
              <ul style={{ listStyle: "none", padding: 0 }}>
                {result.reasons.map((r, i) => (
                  <li key={i} style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "1rem",
                    padding: "1rem",
                    background: "rgba(255,255,255,0.2)",
                    marginBottom: "0.75rem",
                    borderRadius: "12px"
                  }}>
                    <div style={{ width: "10px", height: "10px", background: "#ef4444", borderRadius: "50%" }} />
                    {r}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {showPopup && (
        <div style={styles.popup} onClick={() => setShowPopup(null)}>
          <div style={styles.popupContent} onClick={(e) => e.stopPropagation()}>
            {showPopup.startsWith("note-") ? (
              <p style={{ fontSize: "1.1rem", lineHeight: 1.6 }}>
                {factorNotes[parseInt(showPopup.split("-")[1])].note}
              </p>
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
