"""
API FastAPI para el chatbot financiero.
Endpoint principal que orquesta el flujo completo.
"""

import os
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger
from dotenv import load_dotenv

from app.gemini_client import GeminiClient
from app.prompt_builder import PromptBuilder
from app.data_handler import DataHandler

load_dotenv()

# Configurar logging
logger.add("logs/chatbot.log", rotation="10 MB", level="INFO")

app = FastAPI(
    title="Chatbot Financiero API",
    description="API para análisis financiero con Gemini",
    version="1.0.0"
)

# CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar componentes
try:
    gemini_client = GeminiClient()
    data_handler = DataHandler()
    prompt_builder = PromptBuilder()
    logger.info("Componentes inicializados correctamente")
except Exception as e:
    logger.error(f"Error al inicializar componentes: {str(e)}")
    raise


class FinancialDataBody(BaseModel):
    """Modelo para el JSON financiero recibido."""
    user: Dict[str, Any]
    finances: Dict[str, Any]
    insights: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    """Modelo para la petición del chatbot."""
    question: str
    financial_data: FinancialDataBody


@app.get("/")
async def root():
    """Endpoint de salud."""
    return {
        "message": "Chatbot Financiero API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud."""
    return {
        "status": "healthy",
        "gemini_configured": gemini_client is not None,
        "data_handler_configured": data_handler is not None
    }


class ChatResponse(BaseModel):
    """Modelo para la respuesta del chatbot."""
    response: str
    success: bool


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal del chatbot.
    
    Flujo:
    1. Recibe JSON financiero + pregunta del usuario
    2. Valida y procesa los datos financieros
    3. Construye prompt con contexto + pregunta
    4. Envía a Gemini API
    5. Retorna respuesta concisa
    """
    try:
        user_name = request.financial_data.user.get("name", "Usuario")
        logger.info(f"Consulta recibida de {user_name}: {request.question}")
        
        # 1. Validar y procesar datos financieros recibidos
        financial_data_dict = request.financial_data.model_dump()
        financial_data = data_handler.validate_and_process(financial_data_dict)
        
        if not financial_data:
            raise HTTPException(
                status_code=400,
                detail="Los datos financieros recibidos no son válidos"
            )
        
        logger.info(f"Datos financieros validados correctamente")
        
        # 2. Construir prompt con contexto financiero + pregunta
        prompt = prompt_builder.build_prompt(financial_data, request.question)
        logger.debug(f"Prompt construido: {prompt[:200]}...")
        
        # 3. Obtener respuesta de Gemini
        gemini_response = gemini_client.generate_response(
            prompt=prompt,
            max_tokens=300,  # Respuestas cortas y concisas
            temperature=0.7
        )
        
        if not gemini_response:
            raise HTTPException(
                status_code=500,
                detail="Error al generar respuesta con Gemini"
            )
        
        logger.info(f"Respuesta generada exitosamente")
        
        # 4. Retornar respuesta
        return ChatResponse(
            response=gemini_response,
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en endpoint /api/chat: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )

