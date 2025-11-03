"""
Script de prueba para el chatbot financiero.
Permite probar el módulo sin necesidad de tener Node.js corriendo.
"""

import json
import requests
from pathlib import Path

# URL del servidor FastAPI (debe estar corriendo)
API_URL = "http://localhost:8000"

def load_test_data():
    """Carga los datos de prueba desde test_data.json"""
    with open("test_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def test_health():
    """Verifica que el servidor esté corriendo"""
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        print("✅ Servidor en línea")
        print(f"   Estado: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        print(f"   Asegúrate de que el servidor esté corriendo en {API_URL}")
        return False

def test_chat(question: str):
    """Prueba el endpoint del chatbot con una pregunta"""
    print(f"\n🤔 Pregunta: {question}")
    print("-" * 60)
    
    try:
        # Cargar datos de prueba
        financial_data = load_test_data()
        
        # Preparar request
        payload = {
            "question": question,
            "financial_data": financial_data
        }
        
        # Hacer petición
        response = requests.post(
            f"{API_URL}/api/chat",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        # Mostrar respuesta
        result = response.json()
        print(f"\n💬 Respuesta del chatbot:\n")
        print(result["response"])
        print("\n" + "=" * 60)
        
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Timeout: La petición tardó demasiado")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la petición: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Detalles: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Ejecuta las pruebas"""
    print("=" * 60)
    print("🧪 PRUEBAS DEL CHATBOT FINANCIERO")
    print("=" * 60)
    
    # Verificar que el servidor esté corriendo
    if not test_health():
        return
    
    # Preguntas de prueba
    questions = [
        "¿Cómo puedo ahorrar más dinero?",
        "¿En qué categoría gasto más?",
        "¿Estoy en buen camino para alcanzar mi meta de ahorro?",
        "¿Qué suscripciones tengo y cuándo se cobran?",
        "Dame consejos para reducir mis gastos"
    ]
    
    print("\n" + "=" * 60)
    print("📝 EJECUTANDO PRUEBAS")
    print("=" * 60)
    
    for i, question in enumerate(questions, 1):
        print(f"\n[Prueba {i}/{len(questions)}]")
        test_chat(question)
        
        # Pausa entre preguntas para no saturar la API
        if i < len(questions):
            import time
            time.sleep(2)
    
    print("\n" + "=" * 60)
    print("✅ PRUEBAS COMPLETADAS")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas canceladas por el usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")

