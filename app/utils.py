"""
Utilidades auxiliares para el chatbot financiero.
"""

from typing import Dict, Any
from loguru import logger


def format_currency(amount: float) -> str:
    """
    Formatea un monto como moneda.
    
    Args:
        amount: Monto a formatear
        
    Returns:
        String formateado como moneda
    """
    return f"${amount:,.2f}"


def calculate_savings_rate(income: float, expenses: float) -> float:
    """
    Calcula la tasa de ahorro.
    
    Args:
        income: Ingresos totales
        expenses: Gastos totales
        
    Returns:
        Tasa de ahorro como porcentaje (0-100)
    """
    if income == 0:
        return 0.0
    
    savings = income - expenses
    return (savings / income) * 100


def get_top_expense_categories(expenses: Dict[str, Any], limit: int = 3) -> list:
    """
    Obtiene las categorías de gastos más altas.
    
    Args:
        expenses: Diccionario con datos de gastos
        limit: Número máximo de categorías a retornar
        
    Returns:
        Lista de tuplas (categoría, monto) ordenadas por monto descendente
    """
    try:
        categories = expenses.get("categories", {})
        category_list = [
            (cat, data.get("total", 0))
            for cat, data in categories.items()
        ]
        category_list.sort(key=lambda x: x[1], reverse=True)
        return category_list[:limit]
    except Exception as e:
        logger.error(f"Error obteniendo categorías de gastos: {str(e)}")
        return []

