from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import random
import sqlite3
from datetime import datetime

app = FastAPI(title="Credit Card Fraud Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- LOAD MODEL ----------------
model = joblib.load(r"C:\Users\Dhanvantri\Desktop\credit-card-fraud\fraud_model.pkl")


# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect("fraud_logs.db")
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

# ---------------- FEATURE GENERATION ----------------
def generate_features(data: UserTransaction):
    features = [random.uniform(-1, 1) for _ in range(28)]

    if data.new_device:
        features[random.randint(0, 27)] = random.uniform(-5, -3)

    if data.location_changed:
        features[random.randint(0, 27)] = random.uniform(3, 6)

    if data.transactions_today > 5:
        features[random.randint(0, 27)] = random.uniform(-4, -2)

    if data.is_night:
        features[random.randint(0, 27)] += random.uniform(1, 2)

    time = random.uniform(0, 100000)
    amount = data.amount

    return [time] + features + [amount]

# ---------------- REASONS ----------------
def generate_reasons(data):
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
    conn = sqlite3.connect("fraud_logs.db")
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
    # Convert input to dict
    input_data = {
        "amount": data.amount,
        "is_night": int(data.is_night),
        "new_device": int(data.new_device),
        "location_changed": int(data.location_changed),
        "transactions_today": data.transactions_today,
    }

    # Create DataFrame (IMPORTANT)
    X = pd.DataFrame([input_data])

    # Predict probability (pipeline handles scaling)
    prob = model.predict_proba(X)[0][1]

    # Decision logic
    if prob > 0.8:
        prediction = "Fraud 🚨"
    elif prob > 0.4:
        prediction = "Suspicious ⚠️"
    else:
        prediction = "Safe ✅"

    return {
        "prediction": prediction,
        "fraud_probability": round(prob * 100, 2),
        "reasons": generate_reasons(data)
    }


# ---------------- ADMIN LOGS API ----------------
@app.get("/admin/logs")
def get_logs():
    conn = sqlite3.connect("fraud_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT amount, prediction, fraud_probability, reasons, created_at
        FROM fraud_logs
        ORDER BY created_at DESC
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
print("CLASSES ORDER:", model.classes_)
