import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# -------------------- LOAD DATA --------------------

df = pd.read_csv("creditcard.csv")

print("Dataset shape:", df.shape)
print("Fraud cases:\n", df["Class"].value_counts())

# -------------------- FEATURES & TARGET --------------------

X = df.drop("Class", axis=1)
y = df["Class"]

# -------------------- SCALING --------------------

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -------------------- TRAIN TEST SPLIT --------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------- MODEL --------------------

model = LogisticRegression(
    class_weight="balanced",
    max_iter=1000,
    n_jobs=-1
)

model.fit(X_train, y_train)

# -------------------- EVALUATION --------------------

y_pred = model.predict(X_test)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))

# -------------------- SAVE MODEL & SCALER --------------------

joblib.dump(model, "model/fraud_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")

print("\n✅ Model and scaler saved successfully")
