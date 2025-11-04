

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
            context_parts = []
            
            # Información del usuario
            usuario = financial_data.get("usuario", {})
            if usuario:
                context_parts.append(
                    f"Usuario: {usuario.get('nombre', 'N/A')} (ID: {usuario.get('id', 'N/A')}) - "
                    f"Saldo actual: ${usuario.get('saldoActual', 0):,.2f}"
                )
            
            # Resumen financiero
            resumen = financial_data.get("resumen", {})
            if resumen:
                context_parts.append(
                    f"Resumen: Ingresos ${resumen.get('totalIngresos', 0):,.2f}, "
                    f"Extras ${resumen.get('totalExtras', 0):,.2f}, "
                    f"Gastos ${resumen.get('totalGastos', 0):,.2f}, "
                    f"Balance neto ${resumen.get('balanceNeto', 0):,.2f}"
                )
                context_parts.append(
                    f"Ahorro: ${resumen.get('ahorroTotal', 0):,.2f} "
                    f"({resumen.get('porcentajeAhorro', 0):.1f}% del total)"
                )
            
            # Detalle de ingresos
            detalle = financial_data.get("detalle", {})
            if detalle:
                ingresos = detalle.get("ingresos", {})
                if ingresos:
                    total_ingresos = ingresos.get("total", 0)
                    transacciones_ing = ingresos.get("transacciones", [])
                    context_parts.append(f"Ingresos totales: ${total_ingresos:,.2f}")
                    if transacciones_ing:
                        ing_summary = []
                        for ing in transacciones_ing[:5]:  # Limitar a 5 para no saturar
                            ing_summary.append(
                                f"{ing.get('descripcion', 'N/A')} "
                                f"({ing.get('categoria', 'N/A')}): ${ing.get('monto', 0):,.2f}"
                            )
                        if ing_summary:
                            context_parts.append(f"  - {'; '.join(ing_summary)}")
                
                # Detalle de gastos
                gastos = detalle.get("gastos", {})
                if gastos:
                    total_gastos = gastos.get("total", 0)
                    context_parts.append(f"Gastos totales: ${total_gastos:,.2f}")
                    
                    # Gastos por categoría
                    por_categoria = gastos.get("porCategoria", [])
                    if por_categoria:
                        cat_summary = []
                        for cat in por_categoria:
                            cat_summary.append(
                                f"{cat.get('categoria', 'N/A')}: ${cat.get('total', 0):,.2f}"
                            )
                        if cat_summary:
                            context_parts.append(f"Gastos por categoría: {', '.join(cat_summary)}")
                    
                    # Transacciones de gastos
                    transacciones_gastos = gastos.get("transacciones", [])
                    if transacciones_gastos:
                        gastos_summary = []
                        for gasto in transacciones_gastos[:5]:  # Limitar a 5
                            gastos_summary.append(
                                f"{gasto.get('descripcion', 'N/A')} "
                                f"({gasto.get('categoria', 'N/A')}): ${gasto.get('monto', 0):,.2f}"
                            )
                        if gastos_summary:
                            context_parts.append(f"  - {'; '.join(gastos_summary)}")
                
                # Extras
                extras = detalle.get("extras", {})
                if extras and extras.get("total", 0) > 0:
                    total_extras = extras.get("total", 0)
                    context_parts.append(f"Extras: ${total_extras:,.2f}")
                    transacciones_extras = extras.get("transacciones", [])
                    if transacciones_extras:
                        extras_summary = []
                        for ext in transacciones_extras[:3]:
                            extras_summary.append(
                                f"{ext.get('descripcion', 'N/A')}: ${ext.get('monto', 0):,.2f}"
                            )
                        if extras_summary:
                            context_parts.append(f"  - {'; '.join(extras_summary)}")
                
                # Ahorros y objetivos
                ahorros = detalle.get("ahorros", {})
                if ahorros:
                    total_ahorros = ahorros.get("total", 0)
                    objetivos = ahorros.get("objetivos", [])
                    context_parts.append(f"Ahorros totales: ${total_ahorros:,.2f}")
                    if objetivos:
                        obj_summary = []
                        for obj in objetivos:
                            obj_summary.append(
                                f"{obj.get('objetivo', 'N/A')}: "
                                f"${obj.get('montoAhorrado', 0):,.2f} / "
                                f"${obj.get('montoMeta', 0):,.2f} "
                                f"({obj.get('progreso', 0):.1f}%)"
                            )
                        if obj_summary:
                            context_parts.append(f"Objetivos: {'; '.join(obj_summary)}")
            
            # Alertas
            alertas = financial_data.get("alertas", [])
            if alertas:
                alertas_summary = []
                for alerta in alertas[:3]:  # Limitar a 3 alertas
                    alertas_summary.append(f"{alerta.get('tipo', 'N/A')}: {alerta.get('mensaje', 'N/A')}")
                if alertas_summary:
                    context_parts.append(f"Alertas: {'; '.join(alertas_summary)}")
            
            # Organización (si existe)
            organizacion = financial_data.get("organizacion", {})
            if organizacion:
                context_parts.append(
                    f"Organización: {organizacion.get('nombre', 'N/A')} "
                    f"(Rol: {organizacion.get('rolUsuario', 'N/A')})"
                )
                resumen_org = organizacion.get("resumen", {})
                if resumen_org:
                    context_parts.append(
                        f"Organización - Total miembros: {resumen_org.get('totalMiembros', 0)}, "
                        f"Saldo total: ${resumen_org.get('saldoTotal', 0):,.2f}, "
                        f"Ahorro: ${resumen_org.get('ahorroTotal', 0):,.2f} "
                        f"({resumen_org.get('porcentajeAhorro', 0):.1f}%)"
                    )
                miembros = organizacion.get("miembros", [])
                if miembros:
                    miembros_summary = []
                    for miembro in miembros[:5]:
                        miembros_summary.append(
                            f"{miembro.get('nombre', 'N/A')} "
                            f"({miembro.get('rol', 'N/A')}): ${miembro.get('saldoActual', 0):,.2f}"
                        )
                    if miembros_summary:
                        context_parts.append(f"Miembros: {'; '.join(miembros_summary)}")
            
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

