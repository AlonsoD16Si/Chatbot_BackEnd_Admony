
from __future__ import annotations
from typing import Dict, Any, Optional
from loguru import logger
from pydantic import BaseModel, ValidationError


class FinancialData(BaseModel):
    
    class User(BaseModel):
        id: int
        name: str
        city: Optional[str] = None
        job: Optional[str] = None
    
    class Income(BaseModel):
        salary: float
        other: float = 0
        total_income: float
        period: Optional[str] = None
    
    class ExpenseCategory(BaseModel):
        total: float
        breakdown: Optional[Dict[str, Any]] = None
    
    class Expenses(BaseModel):
        categories: Dict[str, ExpenseCategory]
        total_expenses: float
    
    class Subscription(BaseModel):
        name: str
        amount: float
        next_charge_date: str
        frequency: Optional[str] = None
    
    class Budget(BaseModel):
        period: Optional[str] = None
        planned: float
        spent: float
        remaining: float
    
    class Savings(BaseModel):
        goal: float
        current: float
        progress_percent: float
    
    class Finances(BaseModel):
        income: Income
        expenses: Expenses
        subscriptions: list[Subscription] = []
        budget: Budget
        savings: Savings
    
    class Insights(BaseModel):
        weekly_saving_potential: Optional[float] = None
        upcoming_expenses: Optional[list[Dict[str, Any]]] = None
        recommendations: Optional[list[str]] = None
    
    user: User
    finances: Finances
    insights: Optional[Insights] = None


class DataHandler:
    """Maneja la validación y procesamiento de datos financieros."""
    
    def __init__(self):
        """Inicializa el manejador de datos."""
        logger.info("DataHandler inicializado")
    
    def validate_and_process(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Valida y procesa los datos financieros recibidos.
        
        Args:
            data: Diccionario con datos financieros del usuario
            
        Returns:
            Diccionario validado o None si hay error
        """
        try:
            # Validar estructura con Pydantic
            validated_data = FinancialData(**data)
            logger.info("Datos financieros validados correctamente")
            return validated_data.model_dump()
            
        except ValidationError as e:
            logger.error(f"Error de validación de datos: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado al procesar datos: {str(e)}")
            return None
    
    def validate_financial_data(self, data: Dict[str, Any]) -> bool:
        """
        Valida que los datos financieros tengan la estructura esperada.
        
        Args:
            data: Diccionario con datos financieros
            
        Returns:
            True si los datos son válidos, False en caso contrario
        """
        try:
            FinancialData(**data)
            return True
        except ValidationError:
            return False

