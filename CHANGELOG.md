# Changelog - Chatbot Financiero Backend

## [1.1.0] - 2025-11-04

### ✨ Nuevas Funcionalidades

#### Endpoint con Auto-Fetch de Datos Financieros

- **Nuevo endpoint**: `POST /api/chat/auto`
  - Obtiene automáticamente los datos financieros desde la API externa
  - Solo requiere la pregunta del usuario y el bearer token
  - Simplifica la integración con el frontend

#### Cliente API Integrado

- Agregado cliente HTTP asíncrono en `DataHandler`
- Soporte para autenticación con Bearer Token
- Manejo de errores robusto (timeout, 401, errores de conexión)
- Configuración de URL base desde variables de entorno

### 🔧 Mejoras

#### Configuración

- Nueva variable de entorno: `FINANCIAL_API_BASE_URL`
  - Permite configurar la URL de la API financiera
  - Default: `http://localhost:3000`

#### Dependencias

- Agregado `httpx==0.27.0` para peticiones HTTP asíncronas
- Mejor compatibilidad con FastAPI async/await

### 📚 Documentación

#### Nuevos Archivos

- **`API_USAGE.md`**: Guía completa de uso de la API
  - Ejemplos de integración
  - Documentación de endpoints
  - Casos de uso y troubleshooting
- **`CHANGELOG.md`**: Historial de cambios del proyecto

#### Actualizaciones

- **`test_requests.http`**: Agregados ejemplos del nuevo endpoint
- **`test_data.json`**: Actualizado con datos de ejemplo más recientes

### 🔄 Cambios en la API

#### Endpoints Disponibles

##### Mantiene Retrocompatibilidad

- `POST /api/chat` - Endpoint original (sin cambios)
  - Recibe datos financieros en el body

##### Nuevos Endpoints

- `POST /api/chat/auto` - Endpoint con auto-fetch
  - Body: `{ "question": string, "bearer_token": string }`
  - Obtiene datos automáticamente de la API

### 📝 Estructura de la API Externa

El chatbot espera que la API financiera tenga este endpoint:

```
GET {FINANCIAL_API_BASE_URL}/api/dashboard/all
Authorization: Bearer {token}
```

Respuesta esperada:

```json
{
    "success": true,
    "data": {
        "usuario": {...},
        "resumen": {...},
        "detalle": {...},
        "organizacion": {...}
    }
}
```

### 🚀 Cómo Actualizar

1. Instalar nuevas dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. (Opcional) Configurar URL de la API en `.env`:

   ```bash
   FINANCIAL_API_BASE_URL=http://localhost:3000
   ```

3. Reiniciar el servidor:
   ```bash
   python -m app.main
   # o
   uvicorn app.main:app --reload
   ```

### 💡 Ejemplos de Uso

#### Endpoint Original (sin cambios)

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cómo están mis finanzas?",
    "financial_data": {...}
  }'
```

#### Nuevo Endpoint con Auto-Fetch

```bash
curl -X POST http://localhost:8000/api/chat/auto \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cómo están mis finanzas?",
    "bearer_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

### 🔐 Seguridad

- El bearer token nunca se almacena en el servidor
- Se usa solo para la petición a la API externa
- Manejo apropiado de errores 401 (token inválido/expirado)

### 🐛 Correcciones

- Ninguna (nueva versión)

### ⚠️ Breaking Changes

- Ninguno (retrocompatible al 100%)

---

## [1.0.0] - 2025-11-03

### Versión Inicial

- Endpoint básico `/api/chat`
- Integración con Gemini AI
- Validación de datos con Pydantic
- Construcción de prompts contextuales
- Sistema de logging
