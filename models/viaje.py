from datetime import date
from models.gasto import Gasto

class Viaje:
    def __init__(self, destino_nacional: bool, fecha_inicio: date, fecha_fin: date, presupuesto_diario: float, moneda: str = 'COP'):
        self.destino_nacional = destino_nacional
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.presupuesto_diario = presupuesto_diario
        self.moneda = moneda
        self.gastos: list[Gasto] = []
        self.finalizado = False

    def agregar_gasto(self, gasto: Gasto):
        if self.finalizado:
            raise Exception("No se pueden registrar más gastos. El viaje ha finalizado.")
        self.gastos.append(gasto)

    def finalizar(self):
        self.finalizado = True
