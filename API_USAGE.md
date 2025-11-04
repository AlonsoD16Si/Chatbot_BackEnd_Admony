# Guía de Uso - API del Chatbot Financiero

## Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```bash
# API Key de Google Gemini (REQUERIDA)
GEMINI_API_KEY=tu_api_key_aqui

# Puerto del servidor (opcional, default: 8000)
PORT=8000

# URL base de la API financiera backend (opcional, default: http://localhost:3000)
FINANCIAL_API_BASE_URL=http://localhost:3000
```

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

## Endpoints Disponibles

### 1. `/api/chat` - Endpoint Original

Envía los datos financieros directamente en el body de la petición.

**Request:**

```http
POST http://localhost:8000/api/chat
Content-Type: application/json

{
    "question": "¿Cómo está mi salud financiera?",
    "financial_data": {
        "success": true,
        "data": {
            "usuario": {...},
            "resumen": {...},
            ...
        }
    }
}
```

**Response:**

```json
{
  "response": "Tu salud financiera se ve bien...",
  "success": true
}
```

### 2. `/api/chat/auto` - Endpoint con Auto-Fetch (NUEVO) ⭐

Obtiene automáticamente los datos financieros desde tu API backend usando el bearer token.

**Request:**

```http
POST http://localhost:8000/api/chat/auto
Content-Type: application/json

{
    "question": "¿Cómo puedo ahorrar más este mes?",
    "bearer_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**

```json
{
  "response": "Para ahorrar más este mes te recomiendo...",
  "success": true
}
```

### 3. `/health` - Health Check

Verifica que el servidor esté funcionando correctamente.

**Request:**

```http
GET http://localhost:8000/health
```

**Response:**

```json
{
  "status": "healthy",
  "gemini_configured": true,
  "data_handler_configured": true
}
```

## Flujo de Uso Recomendado

### Opción 1: Con Auto-Fetch (Más Simple)

1. El usuario se autentica en tu aplicación y obtiene un JWT token
2. Tu frontend envía la pregunta + el token al endpoint `/api/chat/auto`
3. El chatbot automáticamente:
   - Hace una petición GET a `http://localhost:3000/api/dashboard/all` con el bearer token
   - Obtiene los datos financieros del usuario
   - Genera la respuesta usando Gemini AI
   - Retorna la respuesta

**Ventajas:**

- No necesitas enviar todos los datos financieros desde el frontend
- Siempre usa los datos más actualizados
- Menos payload en las peticiones

### Opción 2: Con Datos Directos

1. Tu frontend obtiene los datos financieros primero
2. Envía los datos + pregunta al endpoint `/api/chat`
3. El chatbot genera la respuesta

**Ventajas:**

- Mayor control sobre qué datos se envían
- Útil para testing o cuando los datos ya están en el frontend

## Ejemplo de Integración

### Con JavaScript/TypeScript:

```typescript
// Usando /api/chat/auto (recomendado)
async function askChatbot(question: string, bearerToken: string) {
  const response = await fetch("http://localhost:8000/api/chat/auto", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question: question,
      bearer_token: bearerToken,
    }),
  });

  const data = await response.json();
  return data.response;
}

// Ejemplo de uso:
const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...";
const answer = await askChatbot("¿Cómo están mis ahorros?", token);
console.log(answer);
```

## Testing

### Ejemplo con curl:

```bash
# Test con auto-fetch
curl -X POST http://localhost:8000/api/chat/auto \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cuál es mi balance actual?",
    "bearer_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJZF9Vc3VhcmlvIjo5LCJDb3JyZW8iOiJsdWlzLnRvcnJlc0BleGFtcGxlLmNvbSIsIlJvbCI6IkFkbWluaXN0cmFkb3IiLCJpYXQiOjE3NjIyNzY3ODAsImV4cCI6MTc2Mjg4MTU4MH0.rK44JNPmNbJq0c65Oo4xYw-EKFpQ_qBW3b9HAgiGXEI"
  }'
```

## Configuración de la API Financiera

El chatbot espera que tu API financiera (por defecto `http://localhost:3000`) tenga este endpoint:

```
GET /api/dashboard/all
Authorization: Bearer {token}
```

Y que retorne datos en este formato:

```json
{
    "success": true,
    "data": {
        "usuario": {
            "id": 9,
            "nombre": "Luis Torres",
            "saldoActual": 2500
        },
        "resumen": {
            "totalIngresos": 300,
            "totalExtras": 300,
            "totalGastos": 0,
            "saldoActual": 2500,
            "ahorroTotal": 900,
            "porcentajeAhorro": 300,
            "balanceNeto": 300
        },
        "detalle": {
            "ingresos": {...},
            "gastos": {...},
            "extras": {...},
            "ahorros": {...}
        },
        "organizacion": {...}
    }
}
```

## Errores Comunes

### Error 401: Token Inválido

```json
{
  "detail": "No se pudieron obtener los datos financieros. Verifica que el token sea válido y que la API esté disponible."
}
```

**Solución:** Verifica que el bearer token sea válido y no haya expirado.

### Error 500: API No Disponible

**Solución:** Asegúrate de que tu API financiera esté corriendo en `http://localhost:3000` (o la URL que configuraste).

### Error 400: Datos Inválidos

**Solución:** Verifica que los datos financieros tengan el formato correcto según los modelos Pydantic.

## Soporte

Para más información, consulta los archivos:

- `app/main.py` - Endpoints de la API
- `app/data_handler.py` - Manejo de datos y cliente API
- `app/prompt_builder.py` - Construcción de prompts
- `app/gemini_client.py` - Integración con Gemini AI
