from collections import defaultdict
from models.viaje import Viaje
from utils.enums import MedioPago

class ReporteService:
    def reporte_por_dia(self, viaje: Viaje) -> dict:
        resultado = defaultdict(lambda: {MedioPago.EFECTIVO: 0, MedioPago.TARJETA: 0})
        for gasto in viaje.gastos:
            resultado[gasto.fecha][gasto.medio] += gasto.valor_cop
        return dict(resultado)

    def reporte_por_tipo(self, viaje: Viaje) -> dict:
        resultado = defaultdict(lambda: {MedioPago.EFECTIVO: 0, MedioPago.TARJETA: 0})
        for gasto in viaje.gastos:
            resultado[gasto.tipo][gasto.medio] += gasto.valor_cop
        return dict(resultado)
