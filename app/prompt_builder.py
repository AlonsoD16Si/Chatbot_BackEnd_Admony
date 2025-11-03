

from typing import Dict, Any
from loguru import logger


class PromptBuilder:
    
    SYSTEM_PROMPT = """Eres un asistente financiero experto. Tu objetivo es analizar la situación financiera del usuario y proporcionar recomendaciones CONCISAS y PRÁCTICAS.

IMPORTANTE:
- Responde de forma breve y directa (máximo 3-4 oraciones)
- Enfócate en lo esencial y accionable
- Usa datos concretos del contexto proporcionado
- Sé claro y amigable pero profesional
- No inventes información que no esté en el contexto"""

    @staticmethod
    def build_financial_context(financial_data: Dict[str, Any]) -> str:
        """
        Construye el contexto financiero a partir del JSON recibido.
        
        Args:
            financial_data: Diccionario con los datos financieros del usuario
            
        Returns:
            String formateado con el contexto financiero
        """
        try:
            user = financial_data.get("user", {})
            finances = financial_data.get("finances", {})
            
            context_parts = []
            
            # Información del usuario
            if user:
                context_parts.append(f"Usuario: {user.get('name', 'N/A')} - {user.get('job', 'N/A')} en {user.get('city', 'N/A')}")
            
            # Ingresos
            income = finances.get("income", {})
            if income:
                context_parts.append(
                    f"Ingresos totales: ${income.get('total_income', 0):,.2f} "
                    f"(Salario: ${income.get('salary', 0):,.2f}, Otros: ${income.get('other', 0):,.2f}) "
                    f"Período: {income.get('period', 'N/A')}"
                )
            
            # Gastos
            expenses = finances.get("expenses", {})
            if expenses:
                total_expenses = expenses.get("total_expenses", 0)
                context_parts.append(f"Gastos totales: ${total_expenses:,.2f}")
                
                categories = expenses.get("categories", {})
                if categories:
                    category_summary = []
                    for cat, data in categories.items():
                        cat_total = data.get("total", 0)
                        category_summary.append(f"{cat}: ${cat_total:,.2f}")
                    if category_summary:
                        context_parts.append(f"Gastos por categoría: {', '.join(category_summary)}")
            
            # Presupuesto
            budget = finances.get("budget", {})
            if budget:
                context_parts.append(
                    f"Presupuesto: Planificado ${budget.get('planned', 0):,.2f}, "
                    f"Gastado ${budget.get('spent', 0):,.2f}, "
                    f"Restante ${budget.get('remaining', 0):,.2f}"
                )
            
            # Ahorros
            savings = finances.get("savings", {})
            if savings:
                context_parts.append(
                    f"Ahorros: ${savings.get('current', 0):,.2f} / ${savings.get('goal', 0):,.2f} "
                    f"({savings.get('progress_percent', 0)}% del objetivo)"
                )
            
            # Subscripciones
            subscriptions = finances.get("subscriptions", [])
            if subscriptions:
                sub_summary = []
                for sub in subscriptions:
                    sub_summary.append(
                        f"{sub.get('name', 'N/A')}: ${sub.get('amount', 0):,.2f} "
                        f"(próximo cargo: {sub.get('next_charge_date', 'N/A')})"
                    )
                if sub_summary:
                    context_parts.append(f"Suscripciones: {'; '.join(sub_summary)}")
            
            # Insights existentes
            insights = financial_data.get("insights", {})
            if insights:
                weekly_saving = insights.get("weekly_saving_potential", 0)
                if weekly_saving:
                    context_parts.append(f"Potencial de ahorro semanal: ${weekly_saving:,.2f}")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error construyendo contexto financiero: {str(e)}")
            return "Error al procesar datos financieros"
    
    @classmethod
    def build_prompt(cls, financial_data: Dict[str, Any], user_question: str) -> str:
        """
        Construye el prompt completo para enviar a Gemini.
        
        Args:
            financial_data: Datos financieros del usuario
            user_question: Pregunta del usuario
            
        Returns:
            Prompt completo formateado
        """
        financial_context = cls.build_financial_context(financial_data)
        
        prompt = f"""{cls.SYSTEM_PROMPT}

=== CONTEXTO FINANCIERO DEL USUARIO ===
{financial_context}

=== PREGUNTA DEL USUARIO ===
{user_question}

=== RESPUESTA ===
"""
        return prompt

