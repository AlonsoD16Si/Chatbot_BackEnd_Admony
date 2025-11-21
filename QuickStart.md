# 🚀 Inicio Rápido

## 1. Configurar entorno

```bash
# Activar entorno virtual
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias base
pip install -r requirements.txt

# (Opcional) Instalar extras locales como pandas o Celery
pip install -r requirements-optional.txt
```

## 2. Configurar API Key de Gemini

Crea un archivo `.env` en la raíz del proyecto:

```env
GEMINI_API_KEY=tu_api_key_aqui
PORT=8000
```

> **Obtener API Key:** https://makersuite.google.com/app/apikey

## 3. Iniciar el servidor

```bash
uvicorn app.main:app --reload --port 8000
```

El servidor estará disponible en: http://localhost:8000

## 4. Probar (sin Node.js)

### Opción A: Script de prueba completo

```bash
# En otra terminal
python test_chatbot.py
```

### Opción B: Prueba simple

```bash
python test_simple.py
```

### Opción C: Verificar salud

Abre en el navegador: http://localhost:8000/health

## 5. Probar desde Postman/Insomnia

**Endpoint:** `POST http://localhost:8000/api/chat`

**Body (JSON):**

```json
{
  "question": "¿Cómo puedo ahorrar más?",
  "financial_data": {
    "user": {
      "id": 1,
      "name": "Carlos",
      "city": "Mexico",
      "job": "Developer"
    },
    "finances": {
      "income": {
        "salary": 15000,
        "other": 2000,
        "total_income": 17000
      },
      "expenses": {
        "categories": {
          "food": { "total": 2000, "breakdown": {} }
        },
        "total_expenses": 3300
      },
      "subscriptions": [],
      "budget": {
        "planned": 5000,
        "spent": 3300,
        "remaining": 1700
      },
      "savings": {
        "goal": 3000,
        "current": 1200,
        "progress_percent": 40
      }
    }
  }
}
```

## ✅ ¡Listo!

Ahora puedes integrar este módulo con tu backend Node.js o seguir probándolo de forma independiente.
