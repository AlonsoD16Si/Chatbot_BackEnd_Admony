

import json
import requests

API_URL = "http://127.0.0.1:8000"

financial_data = {
    "user": {
        "id": 1,
        "name": "Carlos",
        "city": "Mexico",
        "job": "Software Developer"
    },
    "finances": {
        "income": {
            "salary": 15000,
            "other": 2000,
            "total_income": 17000,
            "period": "2025-09-16 to 2025-09-30"
        },
        "expenses": {
            "categories": {
                "food": {"total": 2000, "breakdown": {}},
                "transport": {"total": 800, "breakdown": {}},
                "entertainment": {"total": 500, "breakdown": {}}
            },
            "total_expenses": 3300
        },
        "subscriptions": [
            {
                "name": "Netflix",
                "amount": 199,
                "next_charge_date": "2025-09-27",
                "frequency": "biweekly"
            }
        ],
        "budget": {
            "period": "2025-09-23 to 2025-09-29",
            "planned": 5000,
            "spent": 3300,
            "remaining": 1700
        },
        "savings": {
            "goal": 3000,
            "current": 1200,
            "progress_percent": 40
        }
    },
    "insights": {
        "weekly_saving_potential": 1000,
        "recommendations": []
    }
}

# Tu pregunta aquí
question = "¿Cuantos perros puedo meter en un fiat?"

print(f"Pregunta: {question}\n")

try:
    response = requests.post(
        f"{API_URL}/api/chat",
        json={
            "question": question,
            "financial_data": financial_data
        },
        timeout=30
    )
    response.raise_for_status()
    
    result = response.json()
    print("Respuesta del chatbot:")
    print("-" * 60)
    print(result["response"])
    print("-" * 60)
    
except Exception as e:
    print(f"Error: {e}")

