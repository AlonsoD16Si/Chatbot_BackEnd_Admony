# 🤖 Admony - Chatbot Financiero Backend

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**API inteligente para análisis financiero personal con IA**

[Características](#características) •
[Instalación](#instalación) •
[Uso](#uso) •
[API](#documentación-api) •
[Contribuir](#contribución)

</div>

---

## 📋 Descripción

**Admony** es un backend robusto y escalable para un chatbot financiero inteligente. Construido con FastAPI y potenciado por Google Gemini AI, proporciona análisis financiero personalizado, recomendaciones inteligentes y respuestas en lenguaje natural basadas en los datos financieros del usuario.

### ✨ Características

- 🚀 **API REST Rápida**: Construida con FastAPI para alto rendimiento
- 🤖 **IA Generativa**: Integración con Google Gemini AI para respuestas inteligentes
- 💰 **Análisis Financiero**: Procesamiento completo de ingresos, gastos, ahorros y presupuestos
- 📊 **Insights Personalizados**: Recomendaciones basadas en el perfil financiero del usuario
- 🔒 **Validación Robusta**: Validación exhaustiva de datos con Pydantic
- 📝 **Logging Avanzado**: Sistema de logs estructurado con Loguru
- 🌐 **CORS Habilitado**: Listo para integración con frontend
- ⚡ **Respuestas Optimizadas**: Respuestas concisas y accionables

---

## 🏗️ Arquitectura

```
Chatbot_BackEnd_Admony/
├── app/
│   ├── __init__.py
│   ├── main.py              # Endpoint principal FastAPI
│   ├── gemini_client.py     # Cliente Google Gemini AI
│   ├── prompt_builder.py    # Constructor de prompts inteligentes
│   ├── data_handler.py      # Validación y procesamiento de datos
│   └── utils.py             # Utilidades comunes
├── logs/
│   └── chatbot.log          # Logs del sistema
├── tests/
│   ├── test_chatbot.py
│   ├── test_simple.py
│   └── test_data.json
├── requirements.txt         # Dependencias base
├── requirements-optional.txt # Dependencias opcionales (solo local)
├── .env                     # Variables de entorno (no incluido)
└── README.md
```

### 🔄 Flujo de Trabajo

```
Usuario → Pregunta + Datos Financieros
    ↓
FastAPI (main.py) → Validación (data_handler.py)
    ↓
Construcción de Prompt (prompt_builder.py)
    ↓
Google Gemini AI (gemini_client.py)
    ↓
Respuesta Inteligente → Usuario
```

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- API Key de Google Gemini AI

### Pasos de Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/Chatbot_BackEnd_Admony.git
cd Chatbot_BackEnd_Admony
```

2. **Crear entorno virtual**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt

# Opcional: instala extras locales (pandas, Celery, embeddings)
pip install -r requirements-optional.txt
```

4. **Configurar variables de entorno**

```bash
# Crear archivo .env en la raíz del proyecto
echo "GEMINI_API_KEY=tu_api_key_aqui" > .env
echo "PORT=8000" >> .env
```

5. **Ejecutar el servidor**

```bash
# Modo desarrollo
python -m app.main

# O con uvicorn directamente
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: `http://localhost:8000`

---

## 📖 Uso

### Endpoints Disponibles

#### 1. Health Check

```bash
GET /
GET /health
```

**Respuesta:**

```json
{
  "status": "healthy",
  "gemini_configured": true,
  "data_handler_configured": true
}
```

#### 2. Chat con el Asistente Financiero

```bash
POST /api/chat
Content-Type: application/json
```

**Request Body:**

```json
{
  "question": "¿Cómo puedo ahorrar más dinero este mes?",
  "financial_data": {
    "user": {
      "name": "Juan Pérez",
      "job": "Desarrollador",
      "city": "Ciudad de México"
    },
    "finances": {
      "income": {
        "total_income": 50000,
        "salary": 45000,
        "other": 5000,
        "period": "mensual"
      },
      "expenses": {
        "total_expenses": 35000,
        "categories": {
          "alimentacion": { "total": 8000 },
          "transporte": { "total": 5000 },
          "entretenimiento": { "total": 3000 },
          "servicios": { "total": 4000 },
          "otros": { "total": 15000 }
        }
      },
      "budget": {
        "planned": 40000,
        "spent": 35000,
        "remaining": 5000
      },
      "savings": {
        "current": 20000,
        "goal": 50000,
        "progress_percent": 40
      },
      "subscriptions": [
        {
          "name": "Netflix",
          "amount": 199,
          "next_charge_date": "2025-11-15"
        }
      ]
    }
  }
}
```

**Response:**

```json
{
  "response": "Con un ingreso de $50,000 y gastos de $35,000, tienes $15,000 disponibles. Te recomiendo destinar $10,000 a tu ahorro (alcanzarías tu meta en 3 meses) y reducir gastos en 'otros' ($15,000 es alto). Revisa tus suscripciones para optimizar.",
  "success": true
}
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno

| Variable         | Descripción              | Ejemplo     |
| ---------------- | ------------------------ | ----------- |
| `GEMINI_API_KEY` | API Key de Google Gemini | `AIzaSy...` |
| `PORT`           | Puerto del servidor      | `8000`      |
| `LOG_LEVEL`      | Nivel de logging         | `INFO`      |

### Personalización de Respuestas

Puedes ajustar el comportamiento del chatbot en `app/prompt_builder.py`:

```python
SYSTEM_PROMPT = """Eres un asistente financiero experto..."""
```

### Ajuste de Parámetros del Modelo

En `app/main.py`, puedes modificar:

- `max_tokens`: Longitud de respuesta (default: 300)
- `temperature`: Creatividad (0.0 - 1.0, default: 0.7)

---

## 🧪 Testing

```bash
# Ejecutar tests
python test_simple.py

# Test con datos específicos
python test_chatbot.py
```

---

## 📊 Documentación API

FastAPI genera documentación interactiva automáticamente:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 🛠️ Stack Tecnológico

| Tecnología            | Versión | Propósito                                      |
| --------------------- | ------- | ---------------------------------------------- |
| **FastAPI**           | 0.115.0 | Framework web                                  |
| **Uvicorn**           | 0.30.0  | Servidor ASGI                                  |
| **Google Gemini AI**  | Latest  | Motor de IA                                    |
| **Pydantic**          | 2.8.2   | Validación de datos                            |
| **Loguru**            | 0.7.2   | Sistema de logging                             |
| **Python**            | 3.12+   | Lenguaje base                                  |
| **Extras opcionales** | -       | Pandas/Celery/Sentence Transformers solo local |

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Sigue estos pasos:

1. **Fork** el proyecto
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### Guías de Contribución

- Sigue PEP 8 para el estilo de código
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario
- Mantén los commits limpios y descriptivos

---

## 📝 Roadmap

- [ ] Implementar autenticación JWT
- [ ] Agregar soporte multiidioma
- [ ] Implementar caché de respuestas con Redis
- [ ] Crear dashboard de métricas
- [ ] Integrar análisis predictivo con ML
- [ ] Agregar exportación de reportes PDF
- [ ] Implementar webhooks para notificaciones
- [ ] Soporte para múltiples modelos de IA

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

**Proyecto Admony**

- 📧 Email: alonso_dlsilva@outlook.com
- 🌐 Website: [alonso.com](alonsodev.vercel.app/Work)

---

## 🙏 Agradecimientos

- Google Gemini AI por proporcionar la infraestructura de IA
- La comunidad de FastAPI por el excelente framework
- Todos los contribuidores que hacen posible este proyecto

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella ⭐**

Hecho con ❤️ para mejorar la salud financiera de todos

</div>
