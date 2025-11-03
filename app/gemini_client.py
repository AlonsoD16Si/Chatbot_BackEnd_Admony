"""
Cliente para interactuar con la API de Gemini.
Se encarga de enviar prompts y recibir respuestas concisas del LLM.
"""

import os
from typing import Optional
from loguru import logger
from google import genai
from dotenv import load_dotenv

load_dotenv()


class GeminiClient:
    """Cliente para interactuar con Google Gemini API."""
    
    def __init__(self):
        """Inicializa el cliente de Gemini con la API key."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no encontrada en variables de entorno")
        
        # Usar el nuevo SDK de Google Gemini
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.0-flash-exp"
        logger.info("Cliente Gemini inicializado correctamente")
    
    def generate_response(
        self, 
        prompt: str, 
        max_tokens: int = 300,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Genera una respuesta usando Gemini API.
        
        Args:
            prompt: El prompt completo a enviar a Gemini
            max_tokens: Máximo de tokens en la respuesta (default: 300 para respuestas cortas)
            temperature: Controla la creatividad (0.0-1.0)
        
        Returns:
            Respuesta generada por Gemini o None si hay error
        """
        try:
            # Configuración de generación
            config = {
                "max_output_tokens": max_tokens,
                "temperature": temperature,
            }
            
            # Usar el nuevo SDK
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            
            # Extraer el texto de la respuesta
            if response and hasattr(response, 'text') and response.text:
                text = response.text.strip()
                if text:
                    logger.info("Respuesta generada exitosamente por Gemini")
                    return text
            
            # Si no hay texto, verificar si fue bloqueado por seguridad
            logger.warning("Respuesta vacía o bloqueada por Gemini")
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'safety_ratings'):
                        logger.warning(f"Safety ratings: {candidate.safety_ratings}")
            return None
                
        except Exception as e:
            logger.error(f"Error al generar respuesta con Gemini: {str(e)}")
            return None

