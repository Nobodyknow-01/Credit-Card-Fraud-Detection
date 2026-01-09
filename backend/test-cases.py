import requests
import json

URL = "http://127.0.0.1:8000/predict"

test_cases = [

    # =======================
    # 🟢 LOW RISK (1–10)
    # =======================
    {
        "name": "Low Risk 1 – Small amount daytime",
        "data": {"amount": 300, "is_night": False, "new_device": False, "location_changed": False, "transactions_today": 1}
    },
    {
        "name": "Low Risk 2 – Trusted device",
        "data": {"amount": 800, "is_night": False, "new_device": False, "location_changed": False, "transactions_today": 2}
    },
    {
        "name": "Low Risk 3 – Normal shopping",
        "data": {"amount": 1500, "is_night": False, "new_device": False, "location_changed": False, "transactions_today": 3}
    },
    {
        "name": "Low Risk 4 – Grocery purchase",
        "data": {"amount": 600, "is_night": False, "new_device": False, "location_changed": False, "transactions_today": 1}
    },
    {
        "name": "Low Risk 5 – Regular user",
        "data": {"amount": 2000, "is_night": False, "new_device": False, "location_changed": False, "transactions_today": 2}
    },
    {
        "name": "Low Risk 6 – Low frequency",
        "data": {"amount": 900, "is_night": False, "new_device": False, "location_changed": False, "transactions_today": 1}
    },
    {
        "name": "Low Risk 7 – Afternoon transaction",
        "data": {"amount": 1200, "is_night": False, "new_device": False, "location_changed": False, "transactions_today": 2}
    },
    {
        "name": "Low Risk 8 – Known device",
        "data": {"amount": 1800, "is_night": False, "new_device": False, "location_changed": False, "transactions_today": 3}
    },
    {
        "name": "Low Risk 9 – Regular bill payment",
        "data": {"amount": 2500, "is_night": False, "new_device": False, "location_changed": False, "transactions_today": 2}
    },
    {
        "name": "Low Risk 10 – Monthly expense",
        "data": {"amount": 3000, "is_night": False, "new_device": False, "location_changed": False, "transactions_today": 3}
    },

    # =======================
    # 🟡 MEDIUM RISK (11–20)
    # =======================
    {
        "name": "Medium Risk 11 – New device",
        "data": {"amount": 2500, "is_night": False, "new_device": True, "location_changed": False, "transactions_today": 2}
    },
    {
        "name": "Medium Risk 12 – Night transaction",
        "data": {"amount": 3500, "is_night": True, "new_device": False, "location_changed": False, "transactions_today": 2}
    },
    {
        "name": "Medium Risk 13 – Location change",
        "data": {"amount": 4000, "is_night": False, "new_device": False, "location_changed": True, "transactions_today": 2}
    },
    {
        "name": "Medium Risk 14 – Slightly high amount",
        "data": {"amount": 6000, "is_night": False, "new_device": False, "location_changed": False, "transactions_today": 4}
    },
    {
        "name": "Medium Risk 15 – New device + normal time",
        "data": {"amount": 5000, "is_night": False, "new_device": True, "location_changed": False, "transactions_today": 3}
    },
    {
        "name": "Medium Risk 16 – Night + regular device",
        "data": {"amount": 4500, "is_night": True, "new_device": False, "location_changed": False, "transactions_today": 3}
    },
    {
        "name": "Medium Risk 17 – Multiple transactions",
        "data": {"amount": 3500, "is_night": False, "new_device": False, "location_changed": False, "transactions_today": 5}
    },
    {
        "name": "Medium Risk 18 – New location",
        "data": {"amount": 5500, "is_night": False, "new_device": False, "location_changed": True, "transactions_today": 3}
    },
    {
        "name": "Medium Risk 19 – Night + medium amount",
        "data": {"amount": 7000, "is_night": True, "new_device": False, "location_changed": False, "transactions_today": 4}
    },
    {
        "name": "Medium Risk 20 – Device + location change",
        "data": {"amount": 6500, "is_night": False, "new_device": True, "location_changed": True, "transactions_today": 3}
    },

    # =======================
    # 🔴 HIGH RISK (21–30)
    # =======================
    {
        "name": "High Risk 21 – New device + night",
        "data": {"amount": 12000, "is_night": True, "new_device": True, "location_changed": False, "transactions_today": 3}
    },
    {
        "name": "High Risk 22 – Location change + night",
        "data": {"amount": 14000, "is_night": True, "new_device": False, "location_changed": True, "transactions_today": 3}
    },
    {
        "name": "High Risk 23 – Burst transactions",
        "data": {"amount": 8000, "is_night": False, "new_device": False, "location_changed": True, "transactions_today": 7}
    },
    {
        "name": "High Risk 24 – Very high amount",
        "data": {"amount": 25000, "is_night": False, "new_device": False, "location_changed": False, "transactions_today": 2}
    },
    {
        "name": "High Risk 25 – All risk factors",
        "data": {"amount": 30000, "is_night": True, "new_device": True, "location_changed": True, "transactions_today": 6}
    },
    {
        "name": "High Risk 26 – Night + burst",
        "data": {"amount": 18000, "is_night": True, "new_device": False, "location_changed": True, "transactions_today": 8}
    },
    {
        "name": "High Risk 27 – New device + high amount",
        "data": {"amount": 22000, "is_night": False, "new_device": True, "location_changed": False, "transactions_today": 4}
    },
    {
        "name": "High Risk 28 – Sudden location shift",
        "data": {"amount": 16000, "is_night": False, "new_device": False, "location_changed": True, "transactions_today": 5}
    },
    {
        "name": "High Risk 29 – Night shopping spree",
        "data": {"amount": 19000, "is_night": True, "new_device": False, "location_changed": False, "transactions_today": 6}
    },
    {
        "name": "High Risk 30 – Maximum risk",
        "data": {"amount": 50000, "is_night": True, "new_device": True, "location_changed": True, "transactions_today": 10}
    },
]

print("\n🔍 FRAUD MODEL TEST RESULTS\n" + "=" * 50)

for case in test_cases:
    response = requests.post(URL, json=case["data"])
    result = response.json()

    print(f"\n🧪 {case['name']}")
    print("Input:", json.dumps(case["data"], indent=2))
    print("Prediction:", result["prediction"])
    print("Fraud Probability:", f"{result['fraud_probability']}%")
    print("Reasons:")
    for r in result["reasons"]:
        print(" -", r)

print("\n✅ Testing complete")
