from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import sqlite3
from datetime import datetime
import os

# ---------------- APP INIT ----------------
app = FastAPI(title="Credit Card Fraud Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "fraud_model.pkl")
DB_PATH = os.path.join(BASE_DIR, "fraud_logs.db")

# ---------------- LOAD MODEL ----------------
model = joblib.load(MODEL_PATH)
print("CLASSES ORDER:", model.classes_)

# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fraud_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            prediction TEXT,
            fraud_probability REAL,
            reasons TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- INPUT SCHEMA ----------------
class UserTransaction(BaseModel):
    amount: float
    is_night: bool
    new_device: bool
    location_changed: bool
    transactions_today: int

# ---------------- REASONS ----------------
def generate_reasons(data: UserTransaction):
    reasons = []

    if data.amount > 50000:
        reasons.append("Very high transaction amount")
    if data.is_night:
        reasons.append("Transaction at unusual night time")
    if data.new_device:
        reasons.append("New device used for transaction")
    if data.location_changed:
        reasons.append("Transaction location suddenly changed")
    if data.transactions_today > 5:
        reasons.append("Unusually high number of transactions today")

    if not reasons:
        reasons.append("Transaction behavior looks normal")

    return reasons

# ---------------- SAVE LOG ----------------
def save_log(amount, prediction, prob, reasons):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fraud_logs (amount, prediction, fraud_probability, reasons, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        amount,
        prediction,
        prob,
        ", ".join(reasons),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

# ---------------- PREDICTION API ----------------
@app.post("/predict")
def predict(data: UserTransaction):

    # Prepare input exactly as model expects
    X = pd.DataFrame([{
        "amount": data.amount,
        "is_night": int(data.is_night),
        "new_device": int(data.new_device),
        "location_changed": int(data.location_changed),
        "transactions_today": data.transactions_today,
    }])

    prob = model.predict_proba(X)[0][1]

    if prob > 0.8:
        prediction = "Fraud 🚨"
    elif prob > 0.4:
        prediction = "Suspicious ⚠️"
    else:
        prediction = "Safe ✅"

    reasons = generate_reasons(data)

    # 🔥 CRITICAL FIX — SAVE TO DB
    save_log(
        amount=data.amount,
        prediction=prediction,
        prob=round(prob * 100, 2),
        reasons=reasons
    )

    return {
        "prediction": prediction,
        "fraud_probability": round(prob * 100, 2),
        "reasons": reasons
    }

# ---------------- ADMIN LOGS API ----------------
@app.get("/admin/logs")
def get_logs():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT amount, prediction, fraud_probability, reasons, created_at
        FROM fraud_logs
        ORDER BY id DESC
        LIMIT 50
    """)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "amount": r[0],
            "prediction": r[1],
            "fraud_probability": r[2],
            "reasons": r[3].split(", "),
            "time": r[4]
        }
        for r in rows
    ]
