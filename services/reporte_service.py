from collections import defaultdict
from models.viaje import Viaje
from utils.enums import MedioPago

class ReporteService:
    """
    Servicio que genera reportes sobre los gastos de un viaje.
    Separa los datos por día o por tipo de gasto, y por medio de pago.
    """
    def reporte_por_dia(self, viaje: Viaje) -> dict:
        """
        Genera un diccionario con los gastos diarios del viaje,
        separando los montos por medio de pago (efectivo y tarjeta).
        """
        resultado = defaultdict(lambda: {MedioPago.EFECTIVO: 0, MedioPago.TARJETA: 0})
        for gasto in viaje.gastos:
            resultado[gasto.fecha][gasto.medio] += gasto.valor_cop
        return dict(resultado)

    def reporte_por_tipo(self, viaje: Viaje) -> dict:
        """
        Genera un diccionario que agrupa los gastos por tipo de gasto (alimentación, transporte, etc.),
        y los separa por medio de pago.
        """
        resultado = defaultdict(lambda: {MedioPago.EFECTIVO: 0, MedioPago.TARJETA: 0})
        for gasto in viaje.gastos:
            resultado[gasto.tipo][gasto.medio] += gasto.valor_cop
        return dict(resultado)
