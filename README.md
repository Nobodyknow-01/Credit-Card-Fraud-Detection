**# 💳 Credit Card Fraud Detection System**

A full-stack machine learning web application that predicts whether a credit card transaction is **Safe, Suspicious, or Fraudulent** in real time. The system includes a modern, mobile-responsive user interface and an admin dashboard to monitor transaction logs.

This project is built to demonstrate end-to-end ML deployment using **React (Vite)** for the frontend and **FastAPI** for the backend.

---

## 🚀 Key Features
• Real-time fraud prediction  
• Fraud probability percentage  
• Reason-based explanations  
• Admin dashboard with logs  
• Mobile-friendly responsive UI  
• Modern glassmorphism design  
• FastAPI + React integration  

---

## 🧠 Machine Learning Overview
A pre-trained fraud detection model is used to analyze transaction patterns and generate:
• Prediction label (Safe / Suspicious / Fraud)  
• Fraud probability score  
• Logical risk explanations  

The model is integrated with the backend using a REST API.

---

## 🛠️ Tech Stack
Frontend: React (Vite), JavaScript, HTML, CSS  
Backend: FastAPI, Python  
ML & Data: Pandas, NumPy, Scikit-learn / XGBoost  
Database: SQLite (for logs)  

---

## 📁 Project Structure
```

credit-card-fraud-detection/
├── backend/
│   ├── main.py
│   ├── model/
│   │   └── fraud_model.pkl
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .env
│   └── package.json
└── README.md

```

---

## ⚙️ Environment Variable
Create a `.env` file inside the `frontend` folder:

```

VITE_API_URL=[http://localhost:8000](http://localhost:8000)

````

---

## ▶️ Run the Project Locally

Backend (FastAPI):
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
````

Frontend (React):

```bash
cd frontend
npm install
npm run dev
```

---

## 🔗 API Endpoints

POST `/predict`

```json
{
  "amount": 5000,
  "transactions_today": 3,
  "is_night": true,
  "new_device": false,
  "location_changed": true
}
```

GET `/admin/logs`
Returns recent transaction predictions for the admin dashboard.

---

## 🧑‍💼 Admin Dashboard

The admin panel displays:
• Total transaction logs
• Fraud probability and prediction
• Transaction reasons
• Search and refresh functionality

---

## 📱 Mobile Support

The UI is fully responsive and optimized for mobile devices with adaptive layouts and touch-friendly controls.

---

## 📌 Use Cases

• Banking and FinTech security
• Fraud risk analysis
• Machine learning portfolio
• Academic and final-year projects

---

## 🚧 Future Enhancements

• Admin authentication
• Advanced analytics and charts
• Cloud database integration
• Model retraining pipeline
• Scalable deployment

---

## 👨‍💻 Author

**Shubham Kumavat**
Data Science & Machine Learning Enthusiast

---

## 📜 License

This project is created for educational and demonstration purposes.

```

---

If you want, I can now:
- Make it **even shorter (recruiter-style)**  
- Add **screenshots section**
- Add **Vercel + Render deployment steps**
- Optimize it for **GitHub stars & visibility**

Just say the word 👍
```
