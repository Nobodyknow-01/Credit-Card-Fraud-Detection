import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# -------------------------------
# 1. CREATE SYNTHETIC DATASET
# -------------------------------

np.random.seed(42)
rows = 8000

data = {
    "amount": np.random.exponential(scale=4000, size=rows),
    "is_night": np.random.binomial(1, 0.3, rows),
    "new_device": np.random.binomial(1, 0.25, rows),
    "location_changed": np.random.binomial(1, 0.2, rows),
    "transactions_today": np.random.randint(1, 10, rows),
}

df = pd.DataFrame(data)

# -------------------------------
# 2. FRAUD LOGIC (GROUND TRUTH)
# -------------------------------

def label_fraud(row):
    score = 0

    if row["amount"] > 10000:
        score += 2
    if row["is_night"] == 1:
        score += 1
    if row["new_device"] == 1:
        score += 2
    if row["location_changed"] == 1:
        score += 2
    if row["transactions_today"] >= 5:
        score += 2

    return 1 if score >= 4 else 0

df["fraud"] = df.apply(label_fraud, axis=1)

print("Fraud rate:", df["fraud"].mean())

# -------------------------------
# 3. SPLIT DATA
# -------------------------------

X = df.drop("fraud", axis=1)
y = df["fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# -------------------------------
# 4. PIPELINE (SCALER + MODEL)
# -------------------------------

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(
        class_weight="balanced",
        max_iter=2000,
        random_state=42
    ))
])

# -------------------------------
# 5. TRAIN MODEL
# -------------------------------

pipeline.fit(X_train, y_train)

# -------------------------------
# 6. EVALUATION
# -------------------------------

y_pred = pipeline.predict(X_test)

print("\nCONFUSION MATRIX")
print(confusion_matrix(y_test, y_pred))

print("\nCLASSIFICATION REPORT")
print(classification_report(y_test, y_pred))

# -------------------------------
# 7. SAVE MODEL
# -------------------------------

joblib.dump(pipeline, "new-fraud_model.pkl")
print("\n✅ Model saved as new-fraud_model.pkl")
