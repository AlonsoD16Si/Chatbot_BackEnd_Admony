
from __future__ import annotations
from typing import Dict, Any, Optional, List
import httpx
from loguru import logger
from pydantic import BaseModel, ValidationError


class Usuario(BaseModel):
    """Modelo para datos del usuario."""
    id: int
    nombre: str
    saldoActual: float


class Resumen(BaseModel):
    """Modelo para resumen financiero."""
    totalIngresos: float
    totalExtras: float
    totalGastos: float
    saldoActual: float
    ahorroTotal: float
    porcentajeAhorro: float
    balanceNeto: float


class TransaccionIngreso(BaseModel):
    """Modelo para transacción de ingreso."""
    monto: float
    descripcion: str
    categoria: str
    fecha: str


class Ingresos(BaseModel):
    """Modelo para ingresos."""
    total: float
    transacciones: List[TransaccionIngreso] = []


class TransaccionGasto(BaseModel):
    """Modelo para transacción de gasto."""
    monto: float
    descripcion: str
    categoria: Optional[str] = None
    fecha: str


class CategoriaGasto(BaseModel):
    """Modelo para categoría de gasto."""
    categoria: str
    total: float
    transacciones: List[TransaccionGasto] = []


class Gastos(BaseModel):
    """Modelo para gastos."""
    total: float
    porCategoria: List[CategoriaGasto] = []
    transacciones: List[TransaccionGasto] = []


class TransaccionExtra(BaseModel):
    """Modelo para transacción extra."""
    monto: float
    descripcion: str
    fecha: str


class Extras(BaseModel):
    """Modelo para extras."""
    total: float
    transacciones: List[TransaccionExtra] = []


class ObjetivoAhorro(BaseModel):
    """Modelo para objetivo de ahorro."""
    objetivo: str
    montoAhorrado: float
    montoMeta: float
    progreso: float
    descripcion: Optional[str] = None


class Ahorros(BaseModel):
    """Modelo para ahorros."""
    total: float
    objetivos: List[ObjetivoAhorro] = []


class Detalle(BaseModel):
    """Modelo para detalle financiero."""
    ingresos: Ingresos
    gastos: Gastos
    extras: Extras
    ahorros: Ahorros


class CategoriaGrafica(BaseModel):
    """Modelo para gráfica de categorías."""
    categoria: str
    total: float


class EvolucionAhorro(BaseModel):
    """Modelo para evolución de ahorro."""
    mes: str
    ahorro: float


class Graficas(BaseModel):
    """Modelo para gráficas."""
    gastosPorCategoria: List[CategoriaGrafica] = []
    evolucionAhorro: List[EvolucionAhorro] = []


class Alerta(BaseModel):
    """Modelo para alerta."""
    tipo: str
    mensaje: str
    severidad: str


class Tendencias(BaseModel):
    """Modelo para tendencias."""
    mensaje: str
    tipo: str


class Miembro(BaseModel):
    """Modelo para miembro de organización."""
    id: int
    nombre: str
    rol: str
    saldoActual: float


class ResumenOrganizacion(BaseModel):
    """Modelo para resumen de organización."""
    totalMiembros: int
    saldoTotal: float
    ahorroTotal: float
    ingresosMes: float
    gastosMes: float
    balanceNeto: float
    porcentajeAhorro: float


class AnalisisCategoria(BaseModel):
    """Modelo para análisis de categoría."""
    categoria: str
    total: float
    cantidadTransacciones: int


class TopGastador(BaseModel):
    """Modelo para top gastador."""
    nombre: str
    totalGastado: float


class Analisis(BaseModel):
    """Modelo para análisis."""
    gastosPorCategoria: List[AnalisisCategoria] = []
    topGastadores: List[TopGastador] = []


class Organizacion(BaseModel):
    """Modelo para organización."""
    id: int
    nombre: str
    rolUsuario: str
    miembros: List[Miembro] = []
    resumen: ResumenOrganizacion
    analisis: Analisis


class FinancialData(BaseModel):
    """Modelo principal para datos financieros."""
    usuario: Usuario
    resumen: Resumen
    detalle: Detalle
    graficas: Optional[Graficas] = None
    alertas: Optional[List[Alerta]] = []
    tendencias: Optional[Tendencias] = None
    organizacion: Optional[Organizacion] = None


class FinancialDataResponse(BaseModel):
    """Modelo para respuesta completa con success y data."""
    success: bool
    data: FinancialData


class DataHandler:
    """Maneja la validación y procesamiento de datos financieros."""
    
    def __init__(self, api_base_url: Optional[str] = None):
        """
        Inicializa el manejador de datos.
        
        Args:
            api_base_url: URL base de la API financiera externa (opcional)
        """
        self.api_base_url = api_base_url or "http://localhost:3000"
        logger.info(f"DataHandler inicializado con API: {self.api_base_url}")
    
    def validate_and_process(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Valida y procesa los datos financieros recibidos.
        
        Args:
            data: Diccionario con datos financieros del usuario (puede incluir success y data)
            
        Returns:
            Diccionario validado con solo los datos financieros o None si hay error
        """
        try:
            # Si el formato incluye success y data, extraer solo data
            if "success" in data and "data" in data:
                financial_data = data["data"]
                validated_data = FinancialData(**financial_data)
                logger.info("Datos financieros validados correctamente (formato con success/data)")
                return validated_data.model_dump()
            # Si el formato es directo (sin success/data)
            elif "usuario" in data or "resumen" in data:
                validated_data = FinancialData(**data)
                logger.info("Datos financieros validados correctamente (formato directo)")
                return validated_data.model_dump()
            else:
                logger.error("Formato de datos no reconocido")
                return None
            
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
            data: Diccionario con datos financieros (puede incluir success y data)
            
        Returns:
            True si los datos son válidos, False en caso contrario
        """
        try:
            # Si el formato incluye success y data, extraer solo data
            if "success" in data and "data" in data:
                FinancialData(**data["data"])
                return True
            # Si el formato es directo
            elif "usuario" in data or "resumen" in data:
                FinancialData(**data)
                return True
            return False
        except ValidationError:
            return False
    
    async def fetch_financial_data_from_api(self, bearer_token: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene datos financieros desde la API externa usando el bearer token.
        
        Args:
            bearer_token: Token de autenticación Bearer
            
        Returns:
            Diccionario con los datos financieros validados o None si hay error
        """
        try:
            url = f"{self.api_base_url}/api/dashboard/all"
            headers = {
                "Authorization": f"Bearer {bearer_token}",
                "Content-Type": "application/json"
            }
            
            logger.info(f"Solicitando datos financieros desde: {url}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info("Datos financieros obtenidos exitosamente desde la API")
                    
                    # Validar y procesar los datos
                    validated_data = self.validate_and_process(data)
                    if validated_data:
                        return validated_data
                    else:
                        logger.error("Los datos obtenidos de la API no son válidos")
                        return None
                        
                elif response.status_code == 401:
                    logger.error("Token de autenticación inválido o expirado")
                    return None
                    
                else:
                    logger.error(f"Error al obtener datos de la API: {response.status_code} - {response.text}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error("Timeout al conectar con la API financiera")
            return None
        except httpx.RequestError as e:
            logger.error(f"Error de conexión con la API: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado al obtener datos de la API: {str(e)}")
            return None

