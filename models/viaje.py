from datetime import date
from models.gasto import Gasto

class Viaje:
    """
    Representa un viaje realizado por el usuario, con un rango de fechas y un presupuesto diario.
    Puede registrar múltiples gastos y determinar si está activo o finalizado.
    """
    def __init__(self, destino_nacional: bool, fecha_inicio: date, fecha_fin: date, presupuesto_diario: float, moneda: str = 'COP'):
        self.destino_nacional = destino_nacional
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.presupuesto_diario = presupuesto_diario
        self.moneda = moneda
        self.gastos: list[Gasto] = []
        self.finalizado = False

    def agregar_gasto(self, gasto: Gasto):
        """
        Agrega un gasto al viaje actual.
        Lanza una excepción si el viaje ya fue finalizado.
        """
        if self.finalizado:
            raise Exception("No se pueden registrar más gastos. El viaje ha finalizado.")
        self.gastos.append(gasto)

    def finalizar(self):
        """
        Marca el viaje como finalizado.
        A partir de este punto, no se pueden registrar más gastos.
        """
        self.finalizado = True
